pub mod cfd;
pub mod combustion;
pub mod datasets;
pub mod models;
pub mod sweeps;
pub mod thermal_mesh;

pub use cfd::CfdEngine;
pub use combustion::CombustionEngine;
pub use datasets::{
    get_embedded_flight_materials, get_flight_material_by_id, load_all_datasets,
    load_bass_dataset, load_saffire_dataset, load_sofie_dataset, resolve_data_directory,
};
pub use models::*;
pub use sweeps::SweepEngine;
pub use thermal_mesh::ThermalMeshEngine;

/// Top-level facade running complete microgravity combustion simulation,
/// Rayon parallel flammability ranking, and CFD morphology analysis.
pub fn simulate_all(input: &SimulationInput) -> SimulationOutput {
    let materials = get_embedded_flight_materials();
    let selected_material = get_flight_material_by_id(&input.material_id)
        .unwrap_or_else(|| materials[0].clone());

    let effective_moc = CombustionEngine::calculate_effective_moc(
        &selected_material,
        input.gravity_g,
        input.airflow_cm_s,
        input.pressure_kpa,
    );

    let flame_spread_rate = CombustionEngine::calculate_flame_spread_rate(
        &selected_material,
        input.gravity_g,
        input.oxygen_pct,
        input.pressure_kpa,
        input.airflow_cm_s,
        effective_moc,
    );

    let sfrs = CombustionEngine::calculate_space_fire_risk_score(
        &selected_material,
        effective_moc,
        flame_spread_rate,
        input.oxygen_pct,
        input.pressure_kpa,
        input.airflow_cm_s,
    );

    let cool_flames = CombustionEngine::detect_cool_flames(
        &selected_material,
        input.gravity_g,
        input.airflow_cm_s,
        input.oxygen_pct,
        input.pressure_kpa,
        &input.lang,
        Some(effective_moc),
    );

    let is_extinguished = input.oxygen_pct < effective_moc;
    let morphology = CfdEngine::calculate_flame_morphology_metrics(
        input.gravity_g,
        input.airflow_cm_s,
        input.oxygen_pct,
        input.pressure_kpa,
        &input.lang,
        is_extinguished,
        Some(&selected_material),
    );

    let active_regime = morphology.regime_code.clone();

    let materials_ranking = SweepEngine::evaluate_all_materials_parallel(
        &materials,
        input.gravity_g,
        input.oxygen_pct,
        input.pressure_kpa,
        input.airflow_cm_s,
        &input.lang,
    );

    SimulationOutput {
        materials_ranking,
        selected_material,
        effective_moc: (effective_moc * 100.0).round() / 100.0,
        flame_spread_rate: (flame_spread_rate * 1000.0).round() / 1000.0,
        sfrs,
        cool_flames,
        morphology,
        active_regime,
    }
}

/// Facade for generating 2D thermal isothermal mesh.
pub fn generate_thermal_mesh(
    g: f64,
    v: f64,
    peak_temp: f64,
    extinguished: bool,
) -> ThermalMesh2D {
    ThermalMeshEngine::calculate_temperature_mesh(g, v, peak_temp, extinguished)
}
