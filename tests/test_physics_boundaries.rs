use nasa_rust::data_loader::get_embedded_materials;
use nasa_rust::physics::{
    calculate_effective_moc_core, calculate_flame_morphology_metrics_core,
    calculate_flame_spread_rate_core, calculate_space_fire_risk_score_core, detect_cool_flames_core,
};

#[test]
fn test_gravity_boundaries() {
    let materials = get_embedded_materials();
    let gravities = [0.0, 1e-6, 1e-4, 0.08, 0.16, 0.38, 0.80, 1.0, 5.0, 10.0, 100.0];

    for &g in &gravities {
        for mat in &materials {
            // 1. Effective MOC
            let eff_moc = calculate_effective_moc_core(mat.moc_1g, mat.moc_microg, g, 10.0, 101.3);
            assert!(eff_moc.is_finite(), "eff_moc not finite for g={}, mat={}", g, mat.material_id);
            assert!(eff_moc >= 8.0, "eff_moc below 8.0 clamp");
            assert!(eff_moc <= 60.0, "eff_moc above 60.0 clamp");

            // 2. Flame Spread Rate
            let spread = calculate_flame_spread_rate_core(
                mat.base_spread_rate_mm_s,
                mat.moc_microg,
                g,
                25.0,
                101.3,
                10.0,
                eff_moc,
            );
            assert!(spread.is_finite());
            assert!(spread >= 0.0);

            // 3. SFRS
            let (score, tier, color) = calculate_space_fire_risk_score_core(
                eff_moc,
                spread,
                25.0,
                101.3,
                10.0,
                mat.heat_of_combustion_mj_kg,
            );
            assert!(score.is_finite());
            assert!(["Safe", "Moderate", "High", "Critical"].contains(&tier.as_str()));
            assert!(color.starts_with('#'));

            // 4. Morphology
            let morph = calculate_flame_morphology_metrics_core(
                g,
                10.0,
                21.0,
                101.3,
                "vi",
                false,
                Some(mat.heat_of_combustion_mj_kg),
            );
            assert!(morph.aspect_ratio.is_finite());
            assert!(morph.peak_temp_k.is_finite());
            assert!(morph.reynolds.is_finite());
            assert!(morph.grashof.is_finite());
            assert!(morph.richardson.is_finite());
            assert!(morph.damkohler.is_finite());
        }
    }
}

#[test]
fn test_oxygen_boundaries() {
    let materials = get_embedded_materials();
    let pmma = materials.iter().find(|m| m.material_id == "MAT-01").unwrap();
    let nomex = materials.iter().find(|m| m.material_id == "MAT-03").unwrap();

    let o2_levels = [0.0, 0.5, 10.0, 15.0, 21.0, 34.0, 50.0, 85.0, 100.0];

    for &mat in &[pmma, nomex] {
        let eff_moc = calculate_effective_moc_core(mat.moc_1g, mat.moc_microg, 0.0, 10.0, 101.3);

        for &o2 in &o2_levels {
            let spread = calculate_flame_spread_rate_core(
                mat.base_spread_rate_mm_s,
                mat.moc_microg,
                0.0,
                o2,
                101.3,
                10.0,
                eff_moc,
            );
            let (score, tier, _) = calculate_space_fire_risk_score_core(
                eff_moc,
                spread,
                o2,
                101.3,
                10.0,
                mat.heat_of_combustion_mj_kg,
            );

            if o2 < eff_moc {
                assert_eq!(spread, 0.0, "Spread rate must be 0 below MOC for o2={}", o2);
                assert_eq!(score, 0.0, "SFRS must be 0 below MOC for o2={}", o2);
                assert_eq!(tier, "Safe");
            } else {
                assert!(spread >= 0.0);
                assert!(score >= 0.0);
            }
        }
    }
}

#[test]
fn test_airflow_stagnant_and_extreme() {
    let materials = get_embedded_materials();
    let pmma = materials.iter().find(|m| m.material_id == "MAT-01").unwrap();

    let flows = [0.0, 1e-5, 0.5, 2.0, 5.0, 10.0, 25.0, 50.0, 100.0, 200.0];

    for &flow in &flows {
        let eff_moc = calculate_effective_moc_core(pmma.moc_1g, pmma.moc_microg, 0.0, flow, 101.3);
        assert!(eff_moc.is_finite());

        // Radiative quenching penalty under slow flow (< 3.5 cm/s)
        if flow < 3.5 {
            assert!(
                eff_moc > pmma.moc_microg,
                "Quenching delta must increase MOC in stagnant flow: eff_moc={}, base={}",
                eff_moc,
                pmma.moc_microg
            );
        }

        let morph = calculate_flame_morphology_metrics_core(
            0.0,
            flow,
            30.0,
            101.3,
            "en",
            false,
            Some(pmma.heat_of_combustion_mj_kg),
        );
        assert!(!morph.damkohler.is_nan());
        assert!(!morph.richardson.is_nan());
        assert!(morph.reynolds > 0.0);
    }
}

#[test]
fn test_cool_flames_boundary() {
    let materials = get_embedded_materials();
    let pmma = materials.iter().find(|m| m.material_id == "MAT-01").unwrap();
    let nomex = materials.iter().find(|m| m.material_id == "MAT-03").unwrap();

    // 1. Susceptible material (PMMA) inside window: g<=0.08, v<=4, p>=35, O2 near MOC
    let moc = calculate_effective_moc_core(pmma.moc_1g, pmma.moc_microg, 0.0, 2.0, 101.3);
    let (active_en, msg_en) = detect_cool_flames_core(pmma.cool_flame_susceptible, moc, 0.0, 2.0, moc, 101.3, "en");
    assert!(active_en);
    assert!(msg_en.contains("Cool Flames"));

    let (active_vi, msg_vi) = detect_cool_flames_core(pmma.cool_flame_susceptible, moc, 0.0, 2.0, moc, 101.3, "vi");
    assert!(active_vi);
    assert!(msg_vi.contains("Ngọn Lửa Lạnh"));

    // 2. Non-susceptible material (Nomex) must never trigger cool flames
    let (active_nomex, _) = detect_cool_flames_core(nomex.cool_flame_susceptible, moc, 0.0, 2.0, moc, 101.3, "en");
    assert!(!active_nomex);

    // 3. High gravity (1.0g) must never trigger cool flames
    let (active_1g, _) = detect_cool_flames_core(pmma.cool_flame_susceptible, moc, 1.0, 2.0, moc, 101.3, "en");
    assert!(!active_1g);
}
