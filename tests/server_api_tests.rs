//! Integration Tests for NASA Bebo Ignis-0G Axum Web Server & Telemetry Stream

use futures_util::{SinkExt, StreamExt};
use serde_json::Value;
use std::time::Duration;
use tokio::sync::oneshot;

use nasa_bebo_ignis::physics::{FlightMaterial, SimulationInput, SimulationOutput, ThermalMesh2D};
use nasa_bebo_ignis::server::create_router;

/// Test server fixture handle providing ephemeral addresses and clean drop shutdown.
struct TestServerHandle {
    pub base_url: String,
    pub ws_url: String,
    shutdown_tx: Option<oneshot::Sender<()>>,
}

impl Drop for TestServerHandle {
    fn drop(&mut self) {
        if let Some(tx) = self.shutdown_tx.take() {
            let _ = tx.send(());
        }
    }
}

/// Spawns an ephemeral instance of the real production Axum server on port 0.
async fn spawn_production_server() -> TestServerHandle {
    let app = create_router();
    let listener = tokio::net::TcpListener::bind("127.0.0.1:0")
        .await
        .expect("Failed to bind ephemeral test socket 127.0.0.1:0");
    let port = listener.local_addr().unwrap().port();
    let (shutdown_tx, shutdown_rx) = oneshot::channel();

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
        shutdown_tx: Some(shutdown_tx),
    }
}

#[tokio::test]
async fn test_health_check_endpoint() {
    let server = spawn_production_server().await;
    let client = reqwest::Client::new();

    let res = client
        .get(format!("{}/_stcore/health", server.base_url))
        .send()
        .await
        .expect("Health request failed");

    assert_eq!(res.status(), 200);
    let body = res.text().await.expect("Valid body text");
    assert_eq!(body.trim(), "ok");
}

#[tokio::test]
async fn test_root_serves_hud_spa() {
    let server = spawn_production_server().await;
    let client = reqwest::Client::new();

    let res = client
        .get(&server.base_url)
        .send()
        .await
        .expect("Root request failed");

    assert_eq!(res.status(), 200);
    let content_type = res.headers().get("content-type").unwrap().to_str().unwrap();
    assert!(content_type.contains("text/html"));

    let body = res.text().await.expect("Valid HTML text");
    assert!(body.contains("<!DOCTYPE html>") || body.contains("<html"));
}

#[tokio::test]
async fn test_materials_endpoint() {
    let server = spawn_production_server().await;
    let client = reqwest::Client::new();

    let res = client
        .get(format!("{}/api/materials", server.base_url))
        .send()
        .await
        .expect("Materials request failed");

    assert_eq!(res.status(), 200);
    let materials: Vec<FlightMaterial> = res.json().await.expect("Valid FlightMaterial JSON array");
    assert_eq!(materials.len(), 10);
    assert_eq!(materials[0].material_id, "MAT-01");
    assert_eq!(materials[9].material_id, "MAT-10");
}

#[tokio::test]
async fn test_simulate_endpoint() {
    let server = spawn_production_server().await;
    let client = reqwest::Client::new();

    let payload = SimulationInput {
        gravity_g: 0.0,
        oxygen_pct: 21.0,
        pressure_kpa: 101.3,
        airflow_cm_s: 10.0,
        material_id: "MAT-01".to_string(),
        lang: "en".to_string(),
    };

    let res = client
        .post(format!("{}/api/simulate", server.base_url))
        .json(&payload)
        .send()
        .await
        .expect("Simulate request failed");

    assert_eq!(res.status(), 200);
    let output: SimulationOutput = res.json().await.expect("Valid SimulationOutput JSON");
    assert_eq!(output.selected_material.material_id, "MAT-01");
    assert!(output.effective_moc > 0.0);
    assert!(output.flame_spread_rate >= 0.0);
    assert_eq!(output.materials_ranking.len(), 10);
    assert_eq!(output.active_regime, "SPHERICAL_DIFFUSION");
}

#[tokio::test]
async fn test_mesh_endpoint() {
    let server = spawn_production_server().await;
    let client = reqwest::Client::new();

    let res = client
        .get(format!("{}/api/mesh?g=0.0&v=10.0&peak_temp=1380.0&extinguished=false", server.base_url))
        .send()
        .await
        .expect("Mesh request failed");

    assert_eq!(res.status(), 200);
    let mesh: ThermalMesh2D = res.json().await.expect("Valid ThermalMesh2D JSON");
    assert_eq!(mesh.x.len(), 60);
    assert_eq!(mesh.y.len(), 60);
    assert_eq!(mesh.z_temp_k.len(), 60);
    assert_eq!(mesh.z_temp_k[0].len(), 60);
}

#[tokio::test]
async fn test_rag_search_endpoint() {
    let server = spawn_production_server().await;
    let client = reqwest::Client::new();

    let req_body = serde_json::json!({
        "query": "water mist fire extinguisher",
        "lang": "en",
        "top_k": 3
    });

    let res = client
        .post(format!("{}/api/rag/search", server.base_url))
        .json(&req_body)
        .send()
        .await
        .expect("RAG request failed");

    assert_eq!(res.status(), 200);
    let body: Value = res.json().await.expect("Valid JSON response");
    assert!(body["ranked_documents"].is_array());
    assert!(!body["ranked_documents"].as_array().unwrap().is_empty());
    assert!(body["directive_answer"].is_string());
    let answer = body["directive_answer"].as_str().unwrap();
    assert!(answer.contains("STRICTLY PROHIBITED") || answer.contains("Fine Water Mist"));
}

#[tokio::test]
async fn test_suppression_endpoints() {
    let server = spawn_production_server().await;
    let client = reqwest::Client::new();

    // 1. Get all materials suppression
    let res_all = client
        .get(format!("{}/api/suppression?lang=en", server.base_url))
        .send()
        .await
        .expect("Suppression all request failed");

    assert_eq!(res_all.status(), 200);
    let list: Vec<Value> = res_all.json().await.expect("Valid suppression array");
    assert_eq!(list.len(), 10);

    // 2. Get specific material suppression by path
    let res_mat1 = client
        .get(format!("{}/api/suppression/MAT-01?lang=en", server.base_url))
        .send()
        .await
        .expect("Suppression MAT-01 request failed");

    assert_eq!(res_mat1.status(), 200);
    let mat1: Value = res_mat1.json().await.expect("Valid suppression object");
    assert_eq!(mat1["material_id"], "MAT-01");
    assert!(mat1["action_1"].as_str().unwrap().contains("HVAC"));

    // 3. Get specific material suppression by query param
    let res_mat6 = client
        .get(format!("{}/api/suppression?material_id=MAT-06&lang=vi", server.base_url))
        .send()
        .await
        .expect("Suppression query request failed");

    assert_eq!(res_mat6.status(), 200);
    let mat6: Value = res_mat6.json().await.expect("Valid suppression object");
    assert_eq!(mat6["material_id"], "MAT-06");

    // 4. Non-existent material returns 404
    let res_mat99 = client
        .get(format!("{}/api/suppression/MAT-99", server.base_url))
        .send()
        .await
        .expect("Suppression MAT-99 request failed");

    assert_eq!(res_mat99.status(), 404);
}

#[tokio::test]
async fn test_ws_telemetry_streaming() {
    let server = spawn_production_server().await;

    let (mut ws_stream, _) = tokio_tungstenite::connect_async(&server.ws_url)
        .await
        .expect("Failed to connect to WebSocket telemetry stream");

    // Receive first 60Hz tick packet
    let first = tokio::time::timeout(Duration::from_secs(2), ws_stream.next())
        .await
        .expect("Timeout waiting for first telemetry packet")
        .expect("Stream ended unexpectedly")
        .expect("WebSocket error");

    assert!(first.is_text());
    let first_json: Value = serde_json::from_str(first.to_text().unwrap()).unwrap();
    assert!(first_json["tick"].is_number());
    assert_eq!(first_json["gravity_g"], 0.0);
    assert_eq!(first_json["regime"], "SPHERICAL_DIFFUSION");

    // Send parameter update: transition to Lunar Rover (0.16g)
    let update_msg = serde_json::json!({
        "gravity_g": 0.16,
        "oxygen_pct": 24.0,
        "airflow_cm_s": 5.0
    });

    ws_stream
        .send(tokio_tungstenite::tungstenite::Message::Text(update_msg.to_string()))
        .await
        .expect("Failed to send telemetry update");

    // Wait for packet reflecting new lunar conditions
    let mut updated_seen = false;
    for _ in 0..20 {
        if let Ok(Some(Ok(msg))) = tokio::time::timeout(Duration::from_millis(100), ws_stream.next()).await {
            if let Ok(parsed) = serde_json::from_str::<Value>(msg.to_text().unwrap_or("")) {
                if (parsed["gravity_g"].as_f64().unwrap_or(0.0) - 0.16).abs() < 1e-4 {
                    updated_seen = true;
                    assert!(parsed["regime"].as_str().unwrap().contains("HEMISPHERE"));
                    break;
                }
            }
        }
    }

    assert!(updated_seen, "Should have received telemetry packet with updated gravity 0.16g");

    // Close connection gracefully
    ws_stream
        .close(None)
        .await
        .expect("Failed to close WebSocket connection cleanly");
}
