use nasa_bebo_ignis::physics::{
    get_embedded_flight_materials, get_flight_material_by_id, load_bass_dataset,
    load_saffire_dataset, load_sofie_dataset, resolve_data_directory, simulate_all,
    CfdEngine, CombustionEngine, RiskTier, SimulationInput, SweepEngine, ThermalMeshEngine,
};

#[test]
fn test_csv_dataset_ingestion_and_record_counts() {
    let data_dir = resolve_data_directory();
    assert!(
        data_dir.exists(),
        "Data directory {:?} must exist",
        data_dir
    );

    let sofie_records = load_sofie_dataset(&data_dir.join("sofie_pmma_burn_rates.csv"))
        .expect("Failed to parse sofie_pmma_burn_rates.csv");
    assert_eq!(
        sofie_records.len(),
        26,
        "SoFIE dataset must contain exactly 26 experimental records"
    );

    let saffire_records = load_saffire_dataset(&data_dir.join("saffire_pressure_oxygen.csv"))
        .expect("Failed to parse saffire_pressure_oxygen.csv");
    assert_eq!(
        saffire_records.len(),
        24,
        "Saffire dataset must contain exactly 24 experimental records"
    );

    let bass_records = load_bass_dataset(&data_dir.join("bass_extinction_limits.csv"))
        .expect("Failed to parse bass_extinction_limits.csv");
    assert_eq!(
        bass_records.len(),
        36,
        "BASS dataset must contain exactly 36 experimental records"
    );

    // Verify record contents
    assert_eq!(sofie_records[0].test_id, "SOFIE-GEL-01");
    assert_eq!(saffire_records[0].test_id, "SAFFIRE-I-01");
    assert_eq!(bass_records[0].test_id, "BASS-II-01");
    assert!(bass_records[1].cool_flame_observed); // BASS-II-02 has cool flame True
}

#[test]
fn test_embedded_flight_materials_specifications() {
    let materials = get_embedded_flight_materials();
    assert_eq!(materials.len(), 10, "Must contain exactly 10 flight materials");

    let pmma = get_flight_material_by_id("MAT-01").expect("MAT-01 must exist");
    assert_eq!(pmma.material_name, "PMMA / Acrylic Rod (6.35mm)");
    assert_eq!(pmma.moc_1g, 17.0);
    assert_eq!(pmma.moc_microg, 15.5);
    assert_eq!(pmma.base_spread_rate_mm_s, 0.51);
    assert!(pmma.cool_flame_susceptible);

    let nomex = get_flight_material_by_id("MAT-03").expect("MAT-03 must exist");
    assert_eq!(nomex.moc_1g, 28.0);
    assert_eq!(nomex.moc_microg, 26.0);
    assert!(!nomex.cool_flame_susceptible);

    let teflon = get_flight_material_by_id("MAT-06").expect("MAT-06 must exist");
    assert_eq!(teflon.moc_1g, 43.0);
    assert_eq!(teflon.moc_microg, 40.5);

    let heptane = get_flight_material_by_id("MAT-08").expect("MAT-08 must exist");
    assert!(heptane.cool_flame_susceptible);
}

#[test]
fn test_gravity_boundaries_and_moc_clamping() {
    let materials = get_embedded_flight_materials();
    let gravities = [
        0.0, 1e-6, 1e-4, 0.08, 0.16, 0.38, 0.80, 1.0, 5.0, 10.0, 100.0,
    ];

    for g in gravities {
        for mat in &materials {
            let eff_moc = CombustionEngine::calculate_effective_moc(mat, g, 10.0, 101.3);
            assert!(
                eff_moc.is_finite(),
                "Effective MOC must be finite for g={}, mat={}",
                g,
                mat.material_id
            );
            assert!(
                eff_moc >= 8.0 && eff_moc <= 60.0,
                "Effective MOC {:.2} must be clamped between 8.0 and 60.0",
                eff_moc
            );

            let spread = CombustionEngine::calculate_flame_spread_rate(
                mat, g, 25.0, 101.3, 10.0, eff_moc,
            );
            assert!(spread.is_finite());
            assert!(spread >= 0.0);

            let sfrs = CombustionEngine::calculate_space_fire_risk_score(
                mat, eff_moc, spread, 25.0, 101.3, 10.0,
            );
            assert!(sfrs.score.is_finite());

            let morph = CfdEngine::calculate_flame_morphology_metrics(
                g,
                10.0,
                21.0,
                101.3,
                "en",
                false,
                Some(mat),
            );
            assert!(morph.aspect_ratio.is_finite());
            assert!(morph.peak_temp_k.is_finite());
            assert!(morph.reynolds.is_finite());
            assert!(morph.grashof.is_finite());
            assert!(morph.richardson.is_finite());
            assert!(morph.damkohler.is_finite());
        }
    }

    // Negative gravity clamping test: g = -1.0 must equal g = 0.0
    let pmma = get_flight_material_by_id("MAT-01").unwrap();
    let moc_neg = CombustionEngine::calculate_effective_moc(&pmma, -1.0, 10.0, 101.3);
    let moc_zero = CombustionEngine::calculate_effective_moc(&pmma, 0.0, 10.0, 101.3);
    assert_eq!(
        moc_neg, moc_zero,
        "Negative gravity must clamp to 0.0g floor"
    );

    // Infinite gravity test
    let moc_inf = CombustionEngine::calculate_effective_moc(&pmma, f64::INFINITY, 10.0, 101.3);
    assert_eq!(
        moc_inf, 60.0,
        "Infinite gravity must be clamped to 60.0% MOC upper bound"
    );
}

#[test]
fn test_sub_moc_extinction_condition() {
    let materials = get_embedded_flight_materials();
    for mat in &materials {
        let eff_moc = CombustionEngine::calculate_effective_moc(mat, 0.0, 10.0, 101.3);

        // Sub-MOC: O2 strictly below effective MOC
        let sub_o2 = eff_moc - 1.0;
        let spread = CombustionEngine::calculate_flame_spread_rate(
            mat, 0.0, sub_o2, 101.3, 10.0, eff_moc,
        );
        assert_eq!(
            spread, 0.0,
            "Spread rate must be strictly 0.0 mm/s when O2 < MOC"
        );

        let sfrs = CombustionEngine::calculate_space_fire_risk_score(
            mat, eff_moc, spread, sub_o2, 101.3, 10.0,
        );
        assert_eq!(sfrs.score, 0.0, "SFRS must be strictly 0.0 when O2 < MOC");
        assert_eq!(sfrs.tier, RiskTier::Safe);
        assert_eq!(sfrs.color_code, "#10B981");
    }
}

#[test]
fn test_low_flow_paradox_peak_at_twelve_cm_per_s() {
    let pmma = get_flight_material_by_id("MAT-01").unwrap();
    let o2 = 25.0;
    let p = 101.3;
    let g = 0.0; // ISS microgravity

    let eff_moc = CombustionEngine::calculate_effective_moc(&pmma, g, 12.0, p);

    let spread_at_12 = CombustionEngine::calculate_flame_spread_rate(&pmma, g, o2, p, 12.0, eff_moc);
    let spread_at_2 = CombustionEngine::calculate_flame_spread_rate(&pmma, g, o2, p, 2.0, eff_moc);
    let spread_at_30 = CombustionEngine::calculate_flame_spread_rate(&pmma, g, o2, p, 30.0, eff_moc);

    assert!(
        spread_at_12 > spread_at_2,
        "Spread at 12 cm/s ({:.3}) must exceed spread at 2 cm/s ({:.3}) due to paradox",
        spread_at_12,
        spread_at_2
    );
    assert!(
        spread_at_12 > spread_at_30,
        "Spread at 12 cm/s ({:.3}) must exceed spread at 30 cm/s ({:.3})",
        spread_at_12,
        spread_at_30
    );
}

#[test]
fn test_cfd_metrics_numerical_stability() {
    // Airflow = 0.0 cm/s, Gravity = 0.0g: Re must remain > 0 (v_min = 0.001 m/s), Ri must not be NaN
    let morph = CfdEngine::calculate_flame_morphology_metrics(0.0, 0.0, 21.0, 101.325, "en", false, None);
    assert!(morph.reynolds > 0.0, "Reynolds number must be > 0.0");
    assert!(!morph.richardson.is_nan(), "Richardson number must not be NaN");
    assert!(!morph.damkohler.is_nan(), "Damkohler number must not be NaN");
    assert_eq!(morph.regime_code, "SPHERICAL_DIFFUSION");

    // Earth 1.0g regime
    let morph_1g = CfdEngine::calculate_flame_morphology_metrics(1.0, 10.0, 21.0, 101.325, "en", false, None);
    assert_eq!(morph_1g.regime_code, "BUOYANT_TEARDROP");

    // Lunar 0.16g regime
    let morph_lunar = CfdEngine::calculate_flame_morphology_metrics(0.16, 10.0, 21.0, 101.325, "en", false, None);
    assert_eq!(morph_lunar.regime_code, "EXPANDING_HEMISPHERE");

    // Extinguished state
    let morph_ext = CfdEngine::calculate_flame_morphology_metrics(0.0, 10.0, 10.0, 101.325, "en", true, None);
    assert_eq!(morph_ext.regime_code, "EXTINGUISHED");
    assert_eq!(morph_ext.aspect_ratio, 0.0);
    assert_eq!(morph_ext.peak_temp_k, 300.0);
}

#[test]
fn test_cool_flames_detection_logic() {
    let pmma = get_flight_material_by_id("MAT-01").unwrap();
    let nomex = get_flight_material_by_id("MAT-03").unwrap();

    let moc_pmma = CombustionEngine::calculate_effective_moc(&pmma, 0.0, 2.0, 101.3);

    // PMMA under microgravity (g=0.0), low airflow (v=2.0), P=101.3, O2 near MOC -> cool flame active!
    let cool_pmma = CombustionEngine::detect_cool_flames(
        &pmma,
        0.0,
        2.0,
        moc_pmma,
        101.3,
        "en",
        Some(moc_pmma),
    );
    assert!(cool_pmma.active, "Cool flames must trigger for PMMA near MOC in micro-g");
    assert!(cool_pmma.message.contains("Cool Flames Regime Active"));

    // Nomex is not susceptible -> must not trigger
    let cool_nomex = CombustionEngine::detect_cool_flames(
        &nomex,
        0.0,
        2.0,
        moc_pmma,
        101.3,
        "en",
        Some(moc_pmma),
    );
    assert!(!cool_nomex.active, "Nomex must never trigger cool flames");

    // PMMA at 1.0g terrestrial -> must not trigger
    let cool_1g = CombustionEngine::detect_cool_flames(
        &pmma,
        1.0,
        2.0,
        moc_pmma,
        101.3,
        "en",
        Some(moc_pmma),
    );
    assert!(!cool_1g.active, "Cool flames must not trigger under terrestrial 1.0g");
}

#[test]
fn test_thermal_mesh_2d_and_3d_generation() {
    let mesh_0g = ThermalMeshEngine::calculate_temperature_mesh(0.0, 10.0, 1380.0, false);
    assert_eq!(mesh_0g.x.len(), 60);
    assert_eq!(mesh_0g.y.len(), 60);
    assert_eq!(mesh_0g.z_temp_k.len(), 60);
    assert_eq!(mesh_0g.z_temp_k[0].len(), 60);

    for row in &mesh_0g.z_temp_k {
        for &temp in row {
            assert!(temp.is_finite());
            assert!(temp >= 290.0, "Temperature {:.1} K below minimum physical floor", temp);
        }
    }

    // Extinguished mesh
    let mesh_ext = ThermalMeshEngine::calculate_temperature_mesh(0.0, 10.0, 1380.0, true);
    for row in &mesh_ext.z_temp_k {
        for &temp in row {
            assert_eq!(temp, 300.0);
        }
    }

    // 3D flame surfaces
    let surfaces_0g = ThermalMeshEngine::generate_3d_flame_surfaces(0.0, 10.0, 1380.0, false, "en");
    assert_eq!(surfaces_0g.len(), 3); // shell, core, rod

    let surfaces_1g = ThermalMeshEngine::generate_3d_flame_surfaces(1.0, 10.0, 1850.0, false, "en");
    assert_eq!(surfaces_1g.len(), 2); // teardrop shell, rod

    let surfaces_lunar = ThermalMeshEngine::generate_3d_flame_surfaces(0.16, 10.0, 1600.0, false, "en");
    assert_eq!(surfaces_lunar.len(), 2); // dome shell, rod
}

#[test]
fn test_rayon_parallel_material_evaluations_and_sweeps() {
    let materials = get_embedded_flight_materials();
    let ranking = SweepEngine::evaluate_all_materials_parallel(
        &materials,
        0.0,
        21.0,
        101.3,
        10.0,
        "en",
    );

    assert_eq!(ranking.len(), 10);
    // Verify sorted descending by SFRS score
    for i in 1..ranking.len() {
        assert!(
            ranking[i - 1].sfrs_score >= ranking[i].sfrs_score,
            "Materials must be ranked in descending order of SFRS: {} ({}) vs {} ({})",
            ranking[i - 1].material_name,
            ranking[i - 1].sfrs_score,
            ranking[i].material_name,
            ranking[i].sfrs_score
        );
    }

    // Parallel paradox sweep
    let pmma = &materials[0];
    let (v_range, sp_0g, sp_1g, sp_cg) =
        SweepEngine::calculate_paradox_sweep_parallel(pmma, 21.0, 101.3, 0.16);
    assert_eq!(v_range.len(), 35);
    assert_eq!(sp_0g.len(), 35);
    assert_eq!(sp_1g.len(), 35);
    assert_eq!(sp_cg.len(), 35);
}

#[test]
fn test_top_level_simulate_all_facade() {
    let input = SimulationInput {
        gravity_g: 0.16,
        oxygen_pct: 28.0,
        pressure_kpa: 70.3,
        airflow_cm_s: 15.0,
        material_id: "MAT-01".to_string(),
        lang: "vi".to_string(),
    };

    let output = simulate_all(&input);
    assert_eq!(output.selected_material.material_id, "MAT-01");
    assert!(output.effective_moc > 0.0);
    assert!(output.flame_spread_rate > 0.0);
    assert!(output.sfrs.score > 0.0);
    assert_eq!(output.active_regime, "EXPANDING_HEMISPHERE");
    assert_eq!(output.materials_ranking.len(), 10);
}
