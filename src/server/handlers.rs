//! HTTP Handlers for NASA Bebo Ignis-0G REST Endpoints

use axum::{
    extract::{Path, Query},
    http::StatusCode,
    Json,
};
use serde::{Deserialize, Serialize};

use crate::i18n::{self, Language};
use crate::physics::{
    generate_thermal_mesh, get_embedded_flight_materials, simulate_all, FlightMaterial,
    SimulationInput, SimulationOutput, ThermalMesh2D,
};
use crate::rag::{query_rag, RagQueryRequest, RankedDocItem};

/// Health check handler returning plain text "ok" for Streamlit parity.
/// Route: GET `/_stcore/health`
pub async fn health_check() -> &'static str {
    "ok"
}

/// Optional query parameters for `/api/materials`
#[derive(Debug, Deserialize)]
pub struct MaterialsQuery {
    pub lang: Option<String>,
}

/// Handler returning all 10 NASA flight specimen materials.
/// Route: GET `/api/materials`
pub async fn get_materials(
    Query(_q): Query<MaterialsQuery>,
) -> Json<Vec<FlightMaterial>> {
    Json(get_embedded_flight_materials())
}

/// Handler for executing complete microgravity combustion simulation.
/// Route: POST `/api/simulate`
pub async fn post_simulate(
    Json(input): Json<SimulationInput>,
) -> Json<SimulationOutput> {
    let output = simulate_all(&input);
    Json(output)
}

/// Query parameters for `/api/mesh`
#[derive(Debug, Deserialize)]
pub struct MeshQueryParams {
    pub g: Option<f64>,
    pub v: Option<f64>,
    pub peak_temp: Option<f64>,
    pub t_peak: Option<f64>,
    pub temp: Option<f64>,
    pub extinguished: Option<bool>,
    pub ext: Option<bool>,
}

/// Handler generating 2D thermal isothermal temperature field (60x60 mesh).
/// Route: GET `/api/mesh`
pub async fn get_mesh(
    Query(q): Query<MeshQueryParams>,
) -> Json<ThermalMesh2D> {
    let g = q.g.unwrap_or(0.0);
    let v = q.v.unwrap_or(10.0);
    let temp = q.peak_temp.or(q.t_peak).or(q.temp).unwrap_or(1380.0);
    let extinguished = q.extinguished.or(q.ext).unwrap_or(false);

    let mesh = generate_thermal_mesh(g, v, temp, extinguished);
    Json(mesh)
}

/// Flexible incoming payload for RAG vector search
#[derive(Debug, Clone, Deserialize)]
pub struct RagSearchPayload {
    pub query: String,
    pub lang: Option<String>,
    pub top_k: Option<usize>,
}

/// Server RAG response payload ensuring 100% test compatibility.
#[derive(Debug, Clone, Serialize)]
pub struct ServerRagResponse {
    pub query: String,
    pub ranked_documents: Vec<RankedDocItem>,
    pub directive_answer: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub directive_details: Option<crate::rag::DirectiveAnswer>,
}

/// Handler for NASA PSI flight research RAG vector search & directive synthesis.
/// Route: POST `/api/rag/search`
pub async fn post_rag_search(
    Json(payload): Json<RagSearchPayload>,
) -> Json<ServerRagResponse> {
    let lang_str = payload.lang.unwrap_or_else(|| "en".to_string());
    let top_k = payload.top_k.unwrap_or(3);

    let req = RagQueryRequest {
        query: payload.query.clone(),
        lang: lang_str,
        top_k,
    };

    let rag_res = query_rag(&req);

    Json(ServerRagResponse {
        query: rag_res.query,
        ranked_documents: rag_res.ranked_documents,
        directive_answer: rag_res.directive_answer.raw_answer.clone(),
        directive_details: Some(rag_res.directive_answer),
    })
}

/// Structured suppression response object matching both SuppressionProtocol and SuppressionProtocolResponse.
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct SuppressionResponse {
    pub material_id: String,
    pub name: String,
    pub action_1: String,
    pub optimal_agent: String,
    pub secondary_hazard: String,
    pub decontamination: String,
}

/// Query parameters for suppression endpoints
#[derive(Debug, Deserialize)]
pub struct SuppressionQueryParams {
    pub material_id: Option<String>,
    pub lang: Option<String>,
}

fn build_suppression_item(material_id: &str, lang: Language) -> Option<SuppressionResponse> {
    let proto = i18n::get_protocol(material_id, lang)?;
    Some(SuppressionResponse {
        material_id: material_id.to_string(),
        name: proto.name.to_string(),
        action_1: proto.action_1.to_string(),
        optimal_agent: proto.optimal_agent.to_string(),
        secondary_hazard: proto.secondary_hazard.to_string(),
        decontamination: proto.decontamination.to_string(),
    })
}

/// Handler returning suppression protocol for a specific material or all materials.
/// Route: GET `/api/suppression`
pub async fn get_suppression_all(
    Query(q): Query<SuppressionQueryParams>,
) -> Result<Json<serde_json::Value>, StatusCode> {
    let lang = Language::from_str_loose(q.lang.as_deref().unwrap_or("en"));

    if let Some(ref id) = q.material_id {
        match build_suppression_item(id, lang) {
            Some(item) => Ok(Json(serde_json::to_value(item).map_err(|_| StatusCode::INTERNAL_SERVER_ERROR)?)),
            None => Err(StatusCode::NOT_FOUND),
        }
    } else {
        let mut list = Vec::new();
        for i in 1..=10 {
            let id = format!("MAT-{:02}", i);
            if let Some(item) = build_suppression_item(&id, lang) {
                list.push(item);
            }
        }
        Ok(Json(serde_json::to_value(list).map_err(|_| StatusCode::INTERNAL_SERVER_ERROR)?))
    }
}

/// Handler returning suppression protocol by URL path parameter `:id`.
/// Route: GET `/api/suppression/:id`
pub async fn get_suppression_by_id(
    Path(id): Path<String>,
    Query(q): Query<SuppressionQueryParams>,
) -> Result<Json<SuppressionResponse>, StatusCode> {
    let lang = Language::from_str_loose(q.lang.as_deref().unwrap_or("en"));
    match build_suppression_item(&id, lang) {
        Some(item) => Ok(Json(item)),
        None => Err(StatusCode::NOT_FOUND),
    }
}
