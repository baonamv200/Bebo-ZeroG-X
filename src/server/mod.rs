//! Axum HTTP & WebSocket Server Module for NASA Bebo Ignis-0G
//! Hosts REST API endpoints, 60Hz telemetry stream, and embedded Aerospace HUD SPA.

pub mod assets;
pub mod handlers;
pub mod ws;

use axum::{
    routing::{get, post},
    Router,
};
use tower_http::cors::{Any, CorsLayer};
use tower_http::trace::TraceLayer;

/// Builds and configures the complete Axum Router with all NASA Bebo Ignis-0G endpoints.
pub fn create_router() -> Router {
    let cors = CorsLayer::new()
        .allow_origin(Any)
        .allow_methods(Any)
        .allow_headers(Any);

    Router::new()
        .route("/_stcore/health", get(handlers::health_check))
        .route("/", get(assets::serve_index))
        .route("/api/materials", get(handlers::get_materials))
        .route("/api/simulate", post(handlers::post_simulate))
        .route("/api/mesh", get(handlers::get_mesh))
        .route("/api/rag/search", post(handlers::post_rag_search))
        .route("/api/suppression", get(handlers::get_suppression_all))
        .route("/api/suppression/:id", get(handlers::get_suppression_by_id))
        .route("/ws/telemetry", get(ws::telemetry_handler))
        .fallback(assets::static_handler)
        .layer(cors)
        .layer(TraceLayer::new_for_http())
}

/// Spawns and runs the NASA Bebo Ignis-0G HTTP & WebSocket server.
pub async fn run_server(addr: std::net::SocketAddr) -> anyhow::Result<()> {
    let app = create_router();
    let listener = tokio::net::TcpListener::bind(addr).await?;
    tracing::info!("NASA Bebo Ignis-0G Server bound to http://{}", addr);
    axum::serve(listener, app).await?;
    Ok(())
}
