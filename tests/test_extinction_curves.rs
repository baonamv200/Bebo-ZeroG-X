use nasa_rust::data_loader::get_embedded_materials;
use nasa_rust::sweeps::{calculate_cached_boundary_sweep_core, calculate_cached_paradox_sweep_core};

#[test]
fn test_paradox_and_boundary_sweeps() {
    let materials = get_embedded_materials();
    let pmma = materials.iter().find(|m| m.material_id == "MAT-01").unwrap();

    // 1. Paradox sweep (35 velocity steps)
    let (v_rng, sp_0g, sp_1g, sp_cg) = calculate_cached_paradox_sweep_core(
        pmma.moc_1g,
        pmma.moc_microg,
        pmma.base_spread_rate_mm_s,
        30.0,
        101.3,
        0.16,
    );

    assert_eq!(v_rng.len(), 35);
    assert_eq!(sp_0g.len(), 35);
    assert_eq!(sp_1g.len(), 35);
    assert_eq!(sp_cg.len(), 35);

    assert!(sp_0g.iter().all(|x| x.is_finite()));
    assert!(sp_1g.iter().all(|x| x.is_finite()));
    assert!(sp_cg.iter().all(|x| x.is_finite()));

    // 2. Boundary sweep (60 extinction steps)
    let (v_sw, moc_sw) = calculate_cached_boundary_sweep_core(pmma.moc_1g, pmma.moc_microg, 0.16, 101.3);
    assert_eq!(v_sw.len(), 60);
    assert_eq!(moc_sw.len(), 60);
    assert!(moc_sw.iter().all(|x| x.is_finite()));
}
