//! Test infrastructure and common fixtures for NASA Bebo Ignis-0G E2E test suite.

use std::net::SocketAddr;
use std::sync::Arc;
use axum::{
    extract::{Path, Query, State, WebSocketUpgrade},
    extract::ws::{Message, WebSocket},
    http::StatusCode,
    response::{Html, IntoResponse, Response},
    routing::{get, post},
    Json, Router,
};
use futures_util::{SinkExt, StreamExt};
use serde::{Deserialize, Serialize};
use tokio::sync::oneshot;

use nasa_bebo_ignis::physics::{
    get_embedded_flight_materials, get_flight_material_by_id, simulate_all,
    generate_thermal_mesh, FlightMaterial, SimulationInput, SimulationOutput, ThermalMesh2D,
};

/// Floating point relative comparison tolerance for physics formulas.
pub const PHYSICS_TOLERANCE: f64 = 1e-3;

/// Helper to compare two floats within relative/absolute tolerance.
pub fn approx_eq(a: f64, b: f64, tol: f64) -> bool {
    if a.is_nan() || b.is_nan() {
        return false;
    }
    if a.is_infinite() && b.is_infinite() {
        return a.is_sign_positive() == b.is_sign_positive();
    }
    let diff = (a - b).abs();
    if diff <= tol {
        return true;
    }
    let max_abs = a.abs().max(b.abs());
    if max_abs > 0.0 {
        diff / max_abs <= tol
    } else {
        true
    }
}

/// Query parameters for /api/mesh endpoint
#[derive(Debug, Deserialize)]
pub struct MeshQuery {
    pub g: Option<f64>,
    pub v: Option<f64>,
    pub temp: Option<f64>,
    pub ext: Option<bool>,
}

/// Request payload for RAG search
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct RagSearchRequest {
    pub query: String,
    #[serde(default = "default_lang")]
    pub lang: String,
    #[serde(default = "default_top_k")]
    pub top_k: usize,
}

fn default_lang() -> String {
    "en".to_string()
}

fn default_top_k() -> usize {
    3
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct RagRankedDoc {
    pub doc_id: String,
    pub title: String,
    pub report_id: String,
    pub score: f64,
    pub section: String,
    pub page: i64,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct RagSearchResponse {
    pub query: String,
    pub ranked_documents: Vec<RagRankedDoc>,
    pub directive_answer: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct SuppressionProtocolResponse {
    pub material_id: String,
    pub action_1: String,
    pub optimal_agent: String,
    pub secondary_hazard: String,
    pub decontamination: String,
}

/// Shared state for test server
#[derive(Clone)]
pub struct AppState {
    pub html_content: Arc<String>,
}

/// Handle to a running ephemeral Axum test server.
pub struct TestServerHandle {
    pub base_url: String,
    pub ws_url: String,
    pub port: u16,
    shutdown_tx: Option<oneshot::Sender<()>>,
}

impl Drop for TestServerHandle {
    fn drop(&mut self) {
        if let Some(tx) = self.shutdown_tx.take() {
            let _ = tx.send(());
        }
    }
}

/// Create the Axum Router with all standard NASA Bebo Ignis-0G endpoints.
pub fn create_test_router() -> Router {
    let html_path = std::path::Path::new("index.html");
    let html = if html_path.exists() {
        std::fs::read_to_string(html_path).unwrap_or_else(|_| "<!DOCTYPE html><html><body>NASA HUD</body></html>".to_string())
    } else {
        "<!DOCTYPE html><html><body>NASA Aerospace HUD</body></html>".to_string()
    };

    let state = AppState {
        html_content: Arc::new(html),
    };

    Router::new()
        .route("/_stcore/health", get(health_handler))
        .route("/", get(home_handler))
        .route("/api/simulate", post(simulate_handler))
        .route("/api/materials", get(materials_handler))
        .route("/api/mesh", get(mesh_handler))
        .route("/api/rag/search", post(rag_search_handler))
        .route("/api/suppression/:id", get(suppression_by_path_handler))
        .route("/api/suppression", get(suppression_query_handler))
        .route("/ws/telemetry", get(ws_telemetry_handler))
        .with_state(state)
}

async fn health_handler() -> &'static str {
    "ok"
}

async fn home_handler(State(state): State<AppState>) -> Html<String> {
    Html((*state.html_content).clone())
}

async fn simulate_handler(Json(payload): Json<SimulationInput>) -> Result<Json<SimulationOutput>, StatusCode> {
    let output = simulate_all(&payload);
    Ok(Json(output))
}

async fn materials_handler() -> Json<Vec<FlightMaterial>> {
    Json(get_embedded_flight_materials())
}

async fn mesh_handler(Query(q): Query<MeshQuery>) -> Json<ThermalMesh2D> {
    let g = q.g.unwrap_or(0.0);
    let v = q.v.unwrap_or(10.0);
    let temp = q.temp.unwrap_or(1380.0);
    let ext = q.ext.unwrap_or(false);
    let mesh = generate_thermal_mesh(g, v, temp, ext);
    Json(mesh)
}

async fn rag_search_handler(Json(req): Json<RagSearchRequest>) -> Json<RagSearchResponse> {
    // Generate deterministic response consistent with NASA PSI RAG specifications
    let query_lower = req.query.to_lowercase();
    let mut docs = Vec::new();

    if query_lower.contains("sofie") || query_lower.contains("pmma") {
        docs.push(RagRankedDoc {
            doc_id: "NASA-TM-2023-0014829".to_string(),
            title: "Solid Fuel Ignition and Extinction (SoFIE) Project: Microgravity PMMA Rod Kinetics".to_string(),
            report_id: "NASA/TM-2023-0014829".to_string(),
            score: 0.884,
            section: "Section 4.3: Low-Flow Flammability Anomalies in Thermoplastic Polymers".to_string(),
            page: 42,
        });
    }

    if query_lower.contains("saffire") || query_lower.contains("nomex") || query_lower.contains("cotton") {
        docs.push(RagRankedDoc {
            doc_id: "NASA-CR-2020-220491".to_string(),
            title: "Spacecraft Fire Safety Demonstration Project (Saffire): Large-Scale Material Flammability in Low Gravity".to_string(),
            report_id: "NASA/CR-2020-220491".to_string(),
            score: 0.821,
            section: "Section 2.1: Fabric and Sheet Burning Characteristics under Exploration Atmospheres".to_string(),
            page: 15,
        });
    }

    if query_lower.contains("cool flame") || query_lower.contains("flex") {
        docs.push(RagRankedDoc {
            doc_id: "SCI-FLEX-2012-1593".to_string(),
            title: "Spherical Cool Flames Observed in Droplet Combustion Aboard the ISS".to_string(),
            report_id: "Science 337:1593-1597".to_string(),
            score: 0.865,
            section: "Section 3: Low-Temperature Second-Stage Combustion Regimes".to_string(),
            page: 1594,
        });
    }

    if query_lower.contains("water") || query_lower.contains("extinguish") || query_lower.contains("suppress")
        || query_lower.contains("nuoc") || query_lower.contains("nước") || query_lower.contains("dap lua") || query_lower.contains("dập lửa") || query_lower.contains("chua chay") || query_lower.contains("chữa cháy") {
        docs.push(RagRankedDoc {
            doc_id: "NASA-SP-2024-50021".to_string(),
            title: "NASA Spacecraft Fire Suppression Systems Design Handbook".to_string(),
            report_id: "NASA/SP-2024-50021".to_string(),
            score: 0.912,
            section: "Section 5.2: Water Mist Application vs Direct Stream Dynamics in Microgravity".to_string(),
            page: 88,
        });
    }

    let is_vi = req.lang == "vi";
    let directive = if docs.is_empty() {
        if is_vi {
            "Không tìm thấy tài liệu kỹ thuật NASA PSI nào phù hợp.".to_string()
        } else {
            "No matching NASA PSI documents found for this query.".to_string()
        }
    } else {
        let top = &docs[0];
        if is_vi {
            format!(
                "**Khuyến Cáo An Toàn Tác Chiến [Dựa trên {} - Trang {}]:**\n\n\
                Dựa trên dữ liệu chuyến bay NASA PSI, các tia nước đơn lẻ áp lực cao bị NGHIÊM CẤM TUYỆT ĐỐI. \
                Khuyến nghị: Sương nước siêu mịn (hạt < 50 µm) kết hợp hạ thông gió khoang.",
                top.report_id, top.page
            )
        } else {
            format!(
                "**Executive Safety Advisory [Grounded in {} - Page {}]:**\n\n\
                Based on official NASA PSI flight research data, high-velocity single water jets are STRICTLY PROHIBITED in microgravity. \
                Fine Water Mist (< 50 µm droplets) or total-flooding inert gas must be deployed immediately.",
                top.report_id, top.page
            )
        }
    };

    Json(RagSearchResponse {
        query: req.query,
        ranked_documents: docs,
        directive_answer: directive,
    })
}

#[derive(Debug, Deserialize)]
pub struct SuppressionQuery {
    pub material_id: Option<String>,
    pub lang: Option<String>,
}

pub fn build_suppression_protocol(material_id: &str, lang: &str) -> Option<SuppressionProtocolResponse> {
    let mat = get_flight_material_by_id(material_id)?;
    let is_vi = lang == "vi";

    let (act1, agent, sec, decont) = match mat.material_id.as_str() {
        "MAT-01" => (
            if is_vi { "Ngắt ngay lập tức hệ thống quạt thông gió HVAC trong vòng 3 giây." }
            else { "Immediately shut down sectional HVAC ventilation within 3 seconds to eliminate forced convective oxidizer feed." },
            if is_vi { "Sương nước siêu mịn kết hợp khí trơ N2; NGHIÊM CẤM TUYỆT ĐỐI tia nước đơn lẻ." }
            else { "Fine Water Mist with N2 propellant or Total Flooding CO2; STRICTLY FORBID high-velocity single water jets." },
            if is_vi { "Nguy cơ sinh khí CO độc hại và sol khí hữu cơ; bắt buộc mặt nạ PBE." }
            else { "Toxic CO gas and fine aerosol particulate off-gassing; mandatory crew donning of PBE breathing apparatus." },
            if is_vi { "Kích hoạt lọc khói ECLSS Smoke Eater và kiểm tra nồng độ khí trước khi tháo mặt nạ." }
            else { "Engage ECLSS smoke scrubber loops and verify absence of trace toxic gases before doffing masks." },
        ),
        "MAT-06" => (
            if is_vi { "Khẩn cấp ngắt cầu dao điện chính và cách ly module." }
            else { "Emergency trip main electrical breaker and isolate affected module power." },
            if is_vi { "Khí trơ làm lạnh nhanh hoặc N2; tuyệt đối không dùng bọt nước." }
            else { "Rapid-cooling liquified inert gas or nitrogen flood; avoid water foams." },
            if is_vi { "Phân hủy sinh khí độc chết người Hydrogen Fluoride (HF) và Carbonyl Fluoride (COF2)." }
            else { "Pyrolysis releases lethal Hydrogen Fluoride (HF) and Carbonyl Fluoride (COF2) gases." },
            if is_vi { "Sử dụng vật liệu hấp phụ kiềm trong ECLSS để trung hòa axít HF." }
            else { "Deploy alkaline scrubbing cartridges in ECLSS loop to neutralize acidic HF fumes." },
        ),
        _ => (
            if is_vi { "Hạ lưu lượng gió xuống dưới 2 cm/s để đưa ngọn lửa vào vùng dập tắt bức xạ." }
            else { "Reduce cabin ventilation below 2 cm/s to drive flame into radiative quenching zone." },
            if is_vi { "Bình cứu hỏa CO2 hoặc sương nước siêu mịn được chứng nhận NASA." }
            else { "NASA-certified portable CO2 fire extinguisher or Fine Water Mist extinguisher." },
            if is_vi { "Nguy cơ tích tụ khí cháy chưa cháy hoàn toàn và bùng phát lại." }
            else { "Secondary flashover risk from accumulated unburnt pyrolysis volatiles." },
            if is_vi { "Vận hành vòng tuần hoàn lọc than hoạt tính ECLSS." }
            else { "Run ECLSS activated charcoal adsorption beds and HEPA scrubbers." },
        ),
    };

    Some(SuppressionProtocolResponse {
        material_id: mat.material_id,
        action_1: act1.to_string(),
        optimal_agent: agent.to_string(),
        secondary_hazard: sec.to_string(),
        decontamination: decont.to_string(),
    })
}

async fn suppression_by_path_handler(
    Path(id): Path<String>,
    Query(q): Query<SuppressionQuery>,
) -> Result<Json<SuppressionProtocolResponse>, StatusCode> {
    let lang = q.lang.unwrap_or_else(|| "en".to_string());
    match build_suppression_protocol(&id, &lang) {
        Some(proto) => Ok(Json(proto)),
        None => Err(StatusCode::NOT_FOUND),
    }
}

async fn suppression_query_handler(
    Query(q): Query<SuppressionQuery>,
) -> Result<Json<SuppressionProtocolResponse>, StatusCode> {
    let id = q.material_id.unwrap_or_else(|| "MAT-01".to_string());
    let lang = q.lang.unwrap_or_else(|| "en".to_string());
    match build_suppression_protocol(&id, &lang) {
        Some(proto) => Ok(Json(proto)),
        None => Err(StatusCode::NOT_FOUND),
    }
}

async fn ws_telemetry_handler(ws: WebSocketUpgrade) -> Response {
    ws.on_upgrade(handle_telemetry_socket)
}

async fn handle_telemetry_socket(mut socket: WebSocket) {
    let mut interval = tokio::time::interval(std::time::Duration::from_millis(16)); // ~60Hz
    let mut count = 0;

    loop {
        tokio::select! {
            _ = interval.tick() => {
                count += 1;
                let telemetry_msg = serde_json::json!({
                    "tick": count,
                    "gravity_g": 0.0,
                    "oxygen_pct": 21.0,
                    "pressure_kpa": 101.3,
                    "airflow_cm_s": 10.0,
                    "sfrs": 42.5,
                    "regime": "SPHERICAL_DIFFUSION"
                });
                if socket.send(Message::Text(telemetry_msg.to_string())).await.is_err() {
                    break;
                }
                if count >= 120 {
                    // Send at least 120 packets and then close or keep going
                    break;
                }
            }
            msg = socket.recv() => {
                match msg {
                    Some(Ok(Message::Close(_))) | None => break,
                    _ => {}
                }
            }
        }
    }
}

/// Spawns an ephemeral Axum test server on loopback port `127.0.0.1:0`.
pub async fn spawn_test_server() -> TestServerHandle {
    let listener = tokio::net::TcpListener::bind("127.0.0.1:0")
        .await
        .expect("Failed to bind ephemeral test port 127.0.0.1:0");
    let port = listener.local_addr().unwrap().port();
    let (shutdown_tx, shutdown_rx) = oneshot::channel::<()>();
    let app = create_test_router();

    tokio::spawn(async move {
        axum::serve(listener, app)
            .with_graceful_shutdown(async {
                let _ = shutdown_rx.await;
            })
            .await
            .unwrap();
    });

    TestServerHandle {
        base_url: format!("http://127.0.0.1:{}", port),
        ws_url: format!("ws://127.0.0.1:{}/ws/telemetry", port),
        port,
        shutdown_tx: Some(shutdown_tx),
    }
}
