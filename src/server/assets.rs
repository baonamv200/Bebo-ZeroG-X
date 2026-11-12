//! Static Asset Embedding and Delivery for NASA Aerospace HUD SPA
//! Uses rust-embed to embed HUD HTML5/SVG/JS/CSS assets into binary.

use axum::{
    body::Body,
    http::{header, StatusCode, Uri},
    response::{IntoResponse, Response},
};
use rust_embed::Embed;

/// Embedded static assets including NASA Aerospace HUD Single Page App.
#[derive(Embed)]
#[folder = "static/"]
pub struct Assets;

/// Helper function to guess MIME content-type from file extension.
fn guess_mime(path: &str) -> &'static str {
    let lower = path.to_lowercase();
    if lower.ends_with(".html") || lower.ends_with(".htm") {
        "text/html; charset=utf-8"
    } else if lower.ends_with(".css") {
        "text/css; charset=utf-8"
    } else if lower.ends_with(".js") || lower.ends_with(".mjs") {
        "application/javascript; charset=utf-8"
    } else if lower.ends_with(".json") {
        "application/json"
    } else if lower.ends_with(".svg") {
        "image/svg+xml"
    } else if lower.ends_with(".png") {
        "image/png"
    } else if lower.ends_with(".jpg") || lower.ends_with(".jpeg") {
        "image/jpeg"
    } else if lower.ends_with(".gif") {
        "image/gif"
    } else if lower.ends_with(".ico") {
        "image/x-icon"
    } else if lower.ends_with(".woff2") {
        "font/woff2"
    } else if lower.ends_with(".woff") {
        "font/woff"
    } else if lower.ends_with(".ttf") {
        "font/ttf"
    } else if lower.ends_with(".wasm") {
        "application/wasm"
    } else {
        "application/octet-stream"
    }
}

/// Handler serving `index.html` on root `/` with `Content-Type: text/html`.
pub async fn serve_index() -> impl IntoResponse {
    // 1. Check filesystem first for live hot-reloading if file exists on disk
    if let Ok(content) = std::fs::read("static/index.html")
        .or_else(|_| std::fs::read("index.html"))
    {
        return Response::builder()
            .status(StatusCode::OK)
            .header(header::CONTENT_TYPE, "text/html; charset=utf-8")
            .body(Body::from(content))
            .unwrap();
    }

    // 2. Fallback to embedded asset
    if let Some(file) = Assets::get("index.html") {
        return Response::builder()
            .status(StatusCode::OK)
            .header(header::CONTENT_TYPE, "text/html; charset=utf-8")
            .body(Body::from(file.data))
            .unwrap();
    }

    Response::builder()
        .status(StatusCode::NOT_FOUND)
        .header(header::CONTENT_TYPE, "text/plain; charset=utf-8")
        .body(Body::from("404 Not Found: NASA HUD index.html"))
        .unwrap()
}

/// Fallback static asset handler for secondary files (CSS, JS, images, fonts).
pub async fn static_handler(uri: Uri) -> impl IntoResponse {
    let path = uri.path().trim_start_matches('/');
    let target = if path.is_empty() { "index.html" } else { path };

    // Prevent directory traversal attacks: disallow relative parent paths and backslashes
    if target.contains("..") || target.contains('\\') || target.starts_with('/') {
        return Response::builder()
            .status(StatusCode::FORBIDDEN)
            .header(header::CONTENT_TYPE, "text/plain; charset=utf-8")
            .body(Body::from("403 Forbidden: Invalid file path traversal"))
            .unwrap();
    }

    // 1. Check embedded assets
    if let Some(file) = Assets::get(target) {
        return Response::builder()
            .status(StatusCode::OK)
            .header(header::CONTENT_TYPE, guess_mime(target))
            .body(Body::from(file.data))
            .unwrap();
    }

    // 2. Check filesystem safely strictly inside static/ directory
    let safe_fs_path = std::path::Path::new("static").join(target);
    if safe_fs_path.is_file() {
        if let Ok(content) = std::fs::read(&safe_fs_path) {
            return Response::builder()
                .status(StatusCode::OK)
                .header(header::CONTENT_TYPE, guess_mime(target))
                .body(Body::from(content))
                .unwrap();
        }
    }

    // 3. Fallback to index.html for SPA routing
    serve_index().await.into_response()
}
