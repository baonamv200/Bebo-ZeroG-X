use nasa_rust::data_loader::{get_embedded_materials, load_nasa_psi_data_core};

#[test]
fn test_all_10_materials_embedded() {
    let materials = get_embedded_materials();
    assert_eq!(materials.len(), 10, "Must have exactly 10 NASA specimens");

    for i in 1..=10 {
        let expected_id = format!("MAT-{:02}", i);
        let mat = materials.iter().find(|m| m.material_id == expected_id);
        assert!(mat.is_some(), "Missing material specimen {}", expected_id);

        let m = mat.unwrap();
        assert!(!m.material_name.is_empty());
        assert!(!m.material_name_vi.is_empty());
        assert!(m.moc_1g >= 8.0 && m.moc_1g <= 60.0);
        assert!(m.moc_microg >= 8.0 && m.moc_microg <= 60.0);
        assert!(m.base_spread_rate_mm_s > 0.0);
        assert!(m.heat_of_combustion_mj_kg > 0.0);
    }
}

#[test]
fn test_csv_loading() {
    let (embedded, sofie, saffire, bass, status) = load_nasa_psi_data_core(None);
    assert_eq!(embedded.len(), 10);
    assert_eq!(status, "disk");

    let sofie_recs = sofie.expect("sofie_pmma_burn_rates.csv must be loaded");
    assert!(!sofie_recs.is_empty());
    assert!(sofie_recs[0].contains_key("material"));

    let saffire_recs = saffire.expect("saffire_pressure_oxygen.csv must be loaded");
    assert!(!saffire_recs.is_empty());
    assert!(saffire_recs[0].contains_key("material"));

    let bass_recs = bass.expect("bass_extinction_limits.csv must be loaded");
    assert!(!bass_recs.is_empty());
    assert!(bass_recs[0].contains_key("material"));
}
