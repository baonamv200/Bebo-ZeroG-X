//! NASA Bebo Ignis-0G Aerospace HUD & Microgravity Simulation Server Launcher

use std::net::SocketAddr;
use tracing_subscriber::{layer::SubscriberExt, util::SubscriberInitExt};

#[tokio::main]
async fn main() -> anyhow::Result<()> {
    // Initialize tracing/logging with sensible defaults
    let _ = tracing_subscriber::registry()
        .with(
            tracing_subscriber::EnvFilter::try_from_default_env()
                .unwrap_or_else(|_| "nasa_bebo_ignis=info,tower_http=info".into()),
        )
        .with(tracing_subscriber::fmt::layer())
        .try_init();

    let port: u16 = std::env::var("PORT")
        .ok()
        .and_then(|p| p.parse().ok())
        .unwrap_or(8501);

    let host = std::env::var("HOST").unwrap_or_else(|_| "0.0.0.0".to_string());
    let addr: SocketAddr = format!("{}:{}", host, port).parse()?;

    println!("============================================================");
    println!("  NASA Bebo Ignis-0G: Aerospace HUD & Axum Server (Rust)    ");
    println!("============================================================");
    println!("* Mission: ISS Microgravity Combustion & CFD Flame Morphology");
    println!("* Engine: 10 Flight Materials, 14 Research Docs, 201 i18n Keys");
    println!("* Server bound on: http://127.0.0.1:{}", port);
    println!("* Aerospace HUD SPA: http://localhost:{}/", port);
    println!("* Streamlit Parity Health: http://localhost:{}/_stcore/health", port);
    println!("* 60Hz Telemetry Stream: ws://localhost:{}/ws/telemetry", port);
    println!("============================================================");

    nasa_bebo_ignis::server::run_server(addr).await?;

    Ok(())
}
