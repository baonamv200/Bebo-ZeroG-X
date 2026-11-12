use rayon::prelude::*;
use crate::physics::combustion::CombustionEngine;
use crate::physics::models::{FlightMaterial, MaterialRiskRow};

/// Rayon-Parallelized Parameter Sweeps and High-Throughput Matrix Evaluation
pub struct SweepEngine;

impl SweepEngine {
    /// Evaluate all flight materials concurrently across CPU threads,
    /// ranking them from highest Space Fire Risk Score to lowest.
    pub fn evaluate_all_materials_parallel(
        materials: &[FlightMaterial],
        gravity_g: f64,
        oxygen_pct: f64,
        pressure_kpa: f64,
        airflow_cm_s: f64,
        lang: &str,
    ) -> Vec<MaterialRiskRow> {
        let mut results: Vec<MaterialRiskRow> = materials
            .par_iter()
            .map(|mat| {
                let eff_moc = CombustionEngine::calculate_effective_moc(
                    mat,
                    gravity_g,
                    airflow_cm_s,
                    pressure_kpa,
                );
                let spread = CombustionEngine::calculate_flame_spread_rate(
                    mat,
                    gravity_g,
                    oxygen_pct,
                    pressure_kpa,
                    airflow_cm_s,
                    eff_moc,
                );
                let sfrs = CombustionEngine::calculate_space_fire_risk_score(
                    mat,
                    eff_moc,
                    spread,
                    oxygen_pct,
                    pressure_kpa,
                    airflow_cm_s,
                );
                let cool = CombustionEngine::detect_cool_flames(
                    mat,
                    gravity_g,
                    airflow_cm_s,
                    oxygen_pct,
                    pressure_kpa,
                    lang,
                    Some(eff_moc),
                );

                MaterialRiskRow {
                    material_id: mat.material_id.clone(),
                    material_name: if lang == "vi" {
                        mat.material_name_vi.clone()
                    } else {
                        mat.material_name.clone()
                    },
                    effective_moc: (eff_moc * 100.0).round() / 100.0,
                    flame_spread_rate: (spread * 1000.0).round() / 1000.0,
                    sfrs_score: (sfrs.score * 10.0).round() / 10.0,
                    risk_tier: sfrs.tier,
                    cool_flame_susceptible: mat.cool_flame_susceptible,
                    cool_flame_active: cool.active,
                }
            })
            .collect();

        // Sort ranking descending by SFRS score (highest fire hazard first)
        results.sort_by(|a, b| {
            b.sfrs_score
                .partial_cmp(&a.sfrs_score)
                .unwrap_or(std::cmp::Ordering::Equal)
        });

        results
    }

    /// Parallel computation of the microgravity low-flow ventilation paradox curves.
    /// Sweeps velocity from 0.0 to 30.0 cm/s across 35 intervals for 0g, 1g, and current g.
    pub fn calculate_paradox_sweep_parallel(
        material: &FlightMaterial,
        oxygen_pct: f64,
        pressure_kpa: f64,
        gravity_g: f64,
    ) -> (Vec<f64>, Vec<f64>, Vec<f64>, Vec<f64>) {
        let count = 35;
        let v_range: Vec<f64> = (0..count)
            .into_par_iter()
            .map(|i| i as f64 * (30.0 / (count as f64 - 1.0)))
            .collect();

        let (spread_0g, (spread_1g, spread_cg)): (Vec<f64>, (Vec<f64>, Vec<f64>)) = v_range
            .par_iter()
            .map(|&v| {
                // 0.0g orbital freefall
                let moc_0g = CombustionEngine::calculate_effective_moc(material, 0.0, v, pressure_kpa);
                let sp_0g = CombustionEngine::calculate_flame_spread_rate(
                    material,
                    0.0,
                    oxygen_pct,
                    pressure_kpa,
                    v,
                    moc_0g,
                );

                // 1.0g terrestrial reference
                let moc_1g = CombustionEngine::calculate_effective_moc(material, 1.0, v, pressure_kpa);
                let sp_1g = CombustionEngine::calculate_flame_spread_rate(
                    material,
                    1.0,
                    oxygen_pct,
                    pressure_kpa,
                    v,
                    moc_1g,
                );

                // Current ambient gravity
                let sp_cg = if gravity_g >= 0.005 && gravity_g <= 0.995 {
                    let moc_cg =
                        CombustionEngine::calculate_effective_moc(material, gravity_g, v, pressure_kpa);
                    CombustionEngine::calculate_flame_spread_rate(
                        material,
                        gravity_g,
                        oxygen_pct,
                        pressure_kpa,
                        v,
                        moc_cg,
                    )
                } else {
                    0.0
                };

                (sp_0g, (sp_1g, sp_cg))
            })
            .unzip();

        (v_range, spread_0g, spread_1g, spread_cg)
    }

    /// Parallel computation of MOC extinction boundary for multiple materials.
    pub fn generate_extinction_boundary_parallel(
        materials: &[FlightMaterial],
        gravity_g: f64,
        pressure_kpa: f64,
    ) -> Vec<(String, Vec<f64>, Vec<f64>)> {
        materials
            .par_iter()
            .map(|mat| {
                let (v_sweep, moc_sweep) =
                    CombustionEngine::generate_extinction_curve(mat, gravity_g, pressure_kpa);
                (mat.material_id.clone(), v_sweep, moc_sweep)
            })
            .collect()
    }
}
