use nasa_rust::mesh::calculate_temperature_mesh_core;

#[test]
fn test_temperature_mesh_dimensions_and_regimes() {
    let temp_levels = [300.0, 600.0, 1380.0, 1850.0, 3000.0, 5000.0];
    let gravities = [0.0, 0.16, 1.0, 5.0];

    for &temp in &temp_levels {
        for &g in &gravities {
            // Active flame mesh
            let (x, y, t, scale) = calculate_temperature_mesh_core(g, 10.0, temp, false);
            assert_eq!(x.len(), 60);
            assert_eq!(y.len(), 60);
            assert_eq!(t.len(), 60);
            assert_eq!(t[0].len(), 60);
            assert!(!scale.is_empty());

            let mut min_t = f64::MAX;
            let mut max_t = f64::MIN;
            for row in &t {
                for &val in row {
                    assert!(!val.is_nan());
                    if val < min_t { min_t = val; }
                    if val > max_t { max_t = val; }
                }
            }
            assert!(min_t >= 290.0, "Min temp must be >= 290.0 K, got {}", min_t);

            // Extinguished mesh
            let (x_e, y_e, t_e, scale_e) = calculate_temperature_mesh_core(g, 10.0, temp, true);
            assert_eq!(x_e.len(), 60);
            assert_eq!(y_e.len(), 60);
            assert_eq!(scale_e.len(), 3);
            for row in &t_e {
                for &val in row {
                    assert_eq!(val, 300.0, "Extinguished mesh must be uniformly 300.0 K");
                }
            }
        }
    }
}
