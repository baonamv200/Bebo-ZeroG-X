use nasa_rust::data_loader::get_embedded_materials;
use nasa_rust::physics::{
    calculate_effective_moc_core, calculate_flame_morphology_metrics_core,
    generate_extinction_curve_core,
};

#[test]
fn test_nan_and_inf_immunity() {
    let materials = get_embedded_materials();
    let pmma = materials.iter().find(|m| m.material_id == "MAT-01").unwrap();

    let inf = f64::INFINITY;

    // Effective MOC with infinite gravity
    let moc_inf = calculate_effective_moc_core(pmma.moc_1g, pmma.moc_microg, inf, 10.0, 101.3);
    assert!(moc_inf.is_finite());
    assert_eq!(moc_inf, 60.0);

    // Negative gravity & airflow resilience in morphology
    let morph_neg = calculate_flame_morphology_metrics_core(-1.0, -5.0, 21.0, 101.325, "vi", false, None);
    assert!(morph_neg.reynolds.is_finite());
    assert!(morph_neg.grashof.is_finite());
    assert!(morph_neg.richardson.is_finite());

    // Extinction curve with zero / negative pressure check
    let (v_sw, moc_sw) = generate_extinction_curve_core(pmma.moc_1g, pmma.moc_microg, 0.0, 50.0);
    assert_eq!(v_sw.len(), 60);
    assert!(moc_sw.iter().all(|val| val.is_finite()));
}

#[test]
fn test_nan_mesh_and_physics_immunity() {
    use nasa_rust::data_loader::load_nasa_psi_data_core;
    use nasa_rust::mesh::calculate_temperature_mesh_core;
    use nasa_rust::physics::{
        calculate_flame_spread_rate_core, calculate_space_fire_risk_score_core,
        detect_cool_flames_core,
    };

    let materials = get_embedded_materials();
    let pmma = materials.iter().find(|m| m.material_id == "MAT-01").unwrap();

    // 1. Mesh with NaN / Inf inputs must produce zero NaNs and stay inside 0g isotropic regime when g=NaN
    let (_x, _y, mesh_nan, _scale) =
        calculate_temperature_mesh_core(f64::NAN, f64::NAN, f64::NAN, false);
    assert_eq!(mesh_nan.len(), 60);
    assert!(
        mesh_nan.iter().all(|row| row.iter().all(|v| v.is_finite())),
        "Temperature mesh must contain zero NaN/Inf values under NaN inputs"
    );

    let (_x2, _y2, mesh_inf, _scale2) =
        calculate_temperature_mesh_core(f64::INFINITY, f64::NEG_INFINITY, f64::INFINITY, false);
    assert!(mesh_inf.iter().all(|row| row.iter().all(|v| v.is_finite())));

    // 2. Effective MOC, spread rate, SFRS, cool flames, extinction curve, morphology with NaN/Inf
    let moc_nan = calculate_effective_moc_core(
        f64::NAN,
        f64::NAN,
        f64::NAN,
        f64::NAN,
        f64::NAN,
    );
    assert!(moc_nan.is_finite() && (8.0..=60.0).contains(&moc_nan));

    let spread_nan = calculate_flame_spread_rate_core(
        f64::NAN,
        f64::NAN,
        f64::NAN,
        f64::NAN,
        f64::NAN,
        f64::NAN,
        f64::NAN,
    );
    assert_eq!(spread_nan, 0.0);

    let (sfrs_nan, tier_nan, _) = calculate_space_fire_risk_score_core(
        16.0,
        f64::NAN,
        f64::NAN,
        f64::NAN,
        f64::NAN,
        f64::NAN,
    );
    assert!(sfrs_nan.is_finite());
    assert_eq!(sfrs_nan, 0.0);
    assert_eq!(tier_nan, "Safe");

    let (cf_nan, _) = detect_cool_flames_core(
        pmma.cool_flame_susceptible,
        16.0,
        f64::NAN,
        f64::NAN,
        16.0,
        f64::INFINITY,
        "en",
    );
    assert!(!cf_nan);

    let morph_nan = calculate_flame_morphology_metrics_core(
        f64::NAN,
        f64::NAN,
        f64::NAN,
        f64::NAN,
        "en",
        false,
        Some(f64::NAN),
    );
    assert!(morph_nan.aspect_ratio.is_finite());
    assert!(morph_nan.peak_temp_k.is_finite());
    assert!(morph_nan.reynolds.is_finite());
    assert!(morph_nan.grashof.is_finite());
    assert!(morph_nan.richardson.is_finite());
    assert!(morph_nan.damkohler.is_finite());
    assert_eq!(morph_nan.regime_code, "SPHERICAL_DIFFUSION");

    let (_v_nan, moc_curve_nan) =
        generate_extinction_curve_core(f64::NAN, f64::NAN, f64::NAN, f64::NAN);
    assert!(moc_curve_nan.iter().all(|v| v.is_finite()));

    // 3. Portable data directory resolution must load CSVs from repo
    let (_mats, sofie, saffire, bass, status) = load_nasa_psi_data_core(None);
    assert_eq!(status, "disk");
    assert!(sofie.is_some() && saffire.is_some() && bass.is_some());
}

#[test]
fn test_negative_gravity_edge_case() {
    let materials = get_embedded_materials();
    let pmma = materials.iter().find(|m| m.material_id == "MAT-01").unwrap();

    let moc_neg = calculate_effective_moc_core(pmma.moc_1g, pmma.moc_microg, -0.1, 10.0, 101.3);
    let moc_zero = calculate_effective_moc_core(pmma.moc_1g, pmma.moc_microg, 0.0, 10.0, 101.3);

    assert!(moc_neg.is_finite());
    assert_eq!(moc_neg, moc_zero, "Negative gravity must be safely clamped to 0.0g degenerate floor");
}
