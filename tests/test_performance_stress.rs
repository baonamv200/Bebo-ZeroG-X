use std::time::Instant;
use nasa_rust::data_loader::get_embedded_materials;
use nasa_rust::physics::{
    calculate_effective_moc_core, calculate_flame_morphology_metrics_core,
    calculate_flame_spread_rate_core, calculate_space_fire_risk_score_core,
};

#[test]
fn test_rapid_physics_iterations() {
    let materials = get_embedded_materials();
    let pmma = materials.iter().find(|m| m.material_id == "MAT-01").unwrap();

    let iterations = 50_000;
    let start = Instant::now();

    for i in 0..iterations {
        let g = ((i % 20) as f64) / 10.0;
        let flow = (i % 50) as f64;
        let o2 = 15.0 + ((i % 30) as f64);
        let p = 50.0 + ((i % 60) as f64);

        let eff_moc = calculate_effective_moc_core(pmma.moc_1g, pmma.moc_microg, g, flow, p);
        let spread = calculate_flame_spread_rate_core(
            pmma.base_spread_rate_mm_s,
            pmma.moc_microg,
            g,
            o2,
            p,
            flow,
            eff_moc,
        );
        let _ = calculate_space_fire_risk_score_core(
            eff_moc,
            spread,
            o2,
            p,
            flow,
            pmma.heat_of_combustion_mj_kg,
        );
        let _ = calculate_flame_morphology_metrics_core(
            g,
            flow,
            o2,
            p,
            "vi",
            false,
            Some(pmma.heat_of_combustion_mj_kg),
        );
    }

    let elapsed = start.elapsed();
    println!(
        "Completed {} iterations in {:?}, avg {:?} per iteration",
        iterations,
        elapsed,
        elapsed / (iterations as u32)
    );

    // 50,000 iterations must easily finish under 1.0 second in release or debug mode
    assert!(
        elapsed.as_secs_f64() < 2.0,
        "Performance threshold exceeded: {:?} for {} iterations",
        elapsed,
        iterations
    );
}
