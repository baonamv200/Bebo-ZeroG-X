use crate::physics::{calculate_effective_moc_core, calculate_flame_spread_rate_core, generate_extinction_curve_core};

pub fn calculate_cached_paradox_sweep_core(
    moc_1g: f64,
    moc_ug: f64,
    base_spread: f64,
    oxygen_pct: f64,
    pressure_kpa: f64,
    gravity_g: f64,
) -> (Vec<f64>, Vec<f64>, Vec<f64>, Vec<f64>) {
    let n = 35;
    let mut v_range = Vec::with_capacity(n);
    let mut spread_0g = Vec::with_capacity(n);
    let mut spread_1g = Vec::with_capacity(n);
    let mut spread_cg = Vec::with_capacity(n);

    let has_cg = gravity_g >= 0.005 && gravity_g <= 0.995;

    for i in 0..n {
        let v_val = 0.0 + (i as f64) * (30.0 / (n as f64 - 1.0));
        v_range.push(v_val);

        let moc_0 = calculate_effective_moc_core(moc_1g, moc_ug, 0.0, v_val, pressure_kpa);
        let sp_0 = calculate_flame_spread_rate_core(base_spread, moc_ug, 0.0, oxygen_pct, pressure_kpa, v_val, moc_0);
        spread_0g.push(sp_0);

        let moc_1 = calculate_effective_moc_core(moc_1g, moc_ug, 1.0, v_val, pressure_kpa);
        let sp_1 = calculate_flame_spread_rate_core(base_spread, moc_ug, 1.0, oxygen_pct, pressure_kpa, v_val, moc_1);
        spread_1g.push(sp_1);

        if has_cg {
            let moc_c = calculate_effective_moc_core(moc_1g, moc_ug, gravity_g, v_val, pressure_kpa);
            let sp_c = calculate_flame_spread_rate_core(base_spread, moc_ug, gravity_g, oxygen_pct, pressure_kpa, v_val, moc_c);
            spread_cg.push(sp_c);
        }
    }

    (v_range, spread_0g, spread_1g, spread_cg)
}

pub fn calculate_cached_boundary_sweep_core(
    moc_1g: f64,
    moc_ug: f64,
    gravity_g: f64,
    pressure_kpa: f64,
) -> (Vec<f64>, Vec<f64>) {
    generate_extinction_curve_core(moc_1g, moc_ug, gravity_g, pressure_kpa)
}
