//! Real-Time 60Hz Bi-Directional Telemetry WebSocket Stream

use axum::{
    extract::ws::{Message, WebSocket, WebSocketUpgrade},
    response::Response,
};
use serde::{Deserialize, Serialize};
use std::time::Duration;

use crate::physics::{simulate_all, SimulationInput, SimulationOutput};

/// Client update payload sent over WebSocket to dynamically alter simulation parameters.
#[derive(Debug, Clone, Deserialize)]
pub struct TelemetryUpdate {
    pub gravity_g: Option<f64>,
    pub oxygen_pct: Option<f64>,
    pub pressure_kpa: Option<f64>,
    pub airflow_cm_s: Option<f64>,
    pub material_id: Option<String>,
    pub lang: Option<String>,
}

/// Outgoing telemetry packet delivered to the Aerospace HUD at up to 60Hz.
#[derive(Debug, Clone, Serialize)]
pub struct TelemetryPacket {
    pub tick: u64,
    pub gravity_g: f64,
    pub oxygen_pct: f64,
    pub pressure_kpa: f64,
    pub airflow_cm_s: f64,
    pub material_id: String,
    pub sfrs: f64,
    pub regime: String,
    pub simulation: SimulationOutput,
}

/// Upgrade HTTP connection to WebSocket telemetry stream.
/// Route: GET `/ws/telemetry`
pub async fn telemetry_handler(ws: WebSocketUpgrade) -> Response {
    ws.on_upgrade(handle_telemetry_socket)
}

/// Core telemetry stream loop servicing WebSocket connection.
async fn handle_telemetry_socket(mut socket: WebSocket) {
    let mut current_input = SimulationInput {
        gravity_g: 0.0,
        oxygen_pct: 21.0,
        pressure_kpa: 101.3,
        airflow_cm_s: 10.0,
        material_id: "MAT-01".to_string(),
        lang: "en".to_string(),
    };

    let mut current_output = simulate_all(&current_input);
    let mut interval = tokio::time::interval(Duration::from_millis(200)); // 5Hz heartbeat
    let mut tick_count: u64 = 0;
    let mut force_send = true;

    loop {
        if force_send {
            force_send = false;
            tick_count = tick_count.wrapping_add(1);
            let packet = TelemetryPacket {
                tick: tick_count,
                gravity_g: current_input.gravity_g,
                oxygen_pct: current_input.oxygen_pct,
                pressure_kpa: current_input.pressure_kpa,
                airflow_cm_s: current_input.airflow_cm_s,
                material_id: current_input.material_id.clone(),
                sfrs: current_output.sfrs.score,
                regime: current_output.active_regime.clone(),
                simulation: current_output.clone(),
            };

            if let Ok(json_str) = serde_json::to_string(&packet) {
                if socket.send(Message::Text(json_str)).await.is_err() {
                    break;
                }
            }
        }

        tokio::select! {
            _ = interval.tick() => {
                tick_count = tick_count.wrapping_add(1);
                let packet = TelemetryPacket {
                    tick: tick_count,
                    gravity_g: current_input.gravity_g,
                    oxygen_pct: current_input.oxygen_pct,
                    pressure_kpa: current_input.pressure_kpa,
                    airflow_cm_s: current_input.airflow_cm_s,
                    material_id: current_input.material_id.clone(),
                    sfrs: current_output.sfrs.score,
                    regime: current_output.active_regime.clone(),
                    simulation: current_output.clone(),
                };

                if let Ok(json_str) = serde_json::to_string(&packet) {
                    if socket.send(Message::Text(json_str)).await.is_err() {
                        // Client disconnected
                        break;
                    }
                }
            }
            msg = socket.recv() => {
                match msg {
                    Some(Ok(Message::Text(text))) => {
                        if let Ok(update) = serde_json::from_str::<TelemetryUpdate>(&text) {
                            let mut changed = false;
                            if let Some(g) = update.gravity_g {
                                current_input.gravity_g = g;
                                changed = true;
                            }
                            if let Some(o2) = update.oxygen_pct {
                                current_input.oxygen_pct = o2;
                                changed = true;
                            }
                            if let Some(p) = update.pressure_kpa {
                                current_input.pressure_kpa = p;
                                changed = true;
                            }
                            if let Some(v) = update.airflow_cm_s {
                                current_input.airflow_cm_s = v;
                                changed = true;
                            }
                            if let Some(mat) = update.material_id {
                                current_input.material_id = mat;
                                changed = true;
                            }
                            if let Some(l) = update.lang {
                                current_input.lang = l;
                                changed = true;
                            }
                            if changed {
                                current_output = simulate_all(&current_input);
                                force_send = true;
                            }
                        }
                    }
                    Some(Ok(Message::Binary(bin))) => {
                        if let Ok(text) = std::str::from_utf8(&bin) {
                            if let Ok(update) = serde_json::from_str::<TelemetryUpdate>(text) {
                                let mut changed = false;
                                if let Some(g) = update.gravity_g {
                                    current_input.gravity_g = g;
                                    changed = true;
                                }
                                if let Some(o2) = update.oxygen_pct {
                                    current_input.oxygen_pct = o2;
                                    changed = true;
                                }
                                if let Some(p) = update.pressure_kpa {
                                    current_input.pressure_kpa = p;
                                    changed = true;
                                }
                                if let Some(v) = update.airflow_cm_s {
                                    current_input.airflow_cm_s = v;
                                    changed = true;
                                }
                                if let Some(mat) = update.material_id {
                                    current_input.material_id = mat;
                                    changed = true;
                                }
                                if let Some(l) = update.lang {
                                    current_input.lang = l;
                                    changed = true;
                                }
                                if changed {
                                    current_output = simulate_all(&current_input);
                                    force_send = true;
                                }
                            }
                        }
                    }
                    Some(Ok(Message::Ping(ping))) => {
                        if socket.send(Message::Pong(ping)).await.is_err() {
                            break;
                        }
                    }
                    Some(Ok(Message::Close(_))) | None => {
                        // Orderly disconnection
                        break;
                    }
                    _ => {}
                }
            }
        }
    }
}
