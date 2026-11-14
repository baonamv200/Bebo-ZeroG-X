use crate::physics::safe_clamp;

pub fn calculate_temperature_mesh_core(
    gravity_g: f64,
    airflow_cm_s: f64,
    peak_temp_k: f64,
    is_extinguished: bool,
) -> (Vec<f64>, Vec<f64>, Vec<Vec<f64>>, Vec<(f64, String)>) {
    let grid_n = 60;
    let mut x_pts = Vec::with_capacity(grid_n);
    let mut y_pts = Vec::with_capacity(grid_n);

    for i in 0..grid_n {
        let x = -3.0 + (i as f64) * (6.0 / (grid_n as f64 - 1.0));
        x_pts.push(x);
    }
    for j in 0..grid_n {
        let y = -2.0 + (j as f64) * (6.0 / (grid_n as f64 - 1.0));
        y_pts.push(y);
    }

    let g_c = if !gravity_g.is_finite() || gravity_g < 0.0 {
        0.0
    } else {
        gravity_g
    };
    let v_raw = if !airflow_cm_s.is_finite() || airflow_cm_s < 0.0 {
        0.0
    } else {
        airflow_cm_s
    };
    let v_c = v_raw / 25.0;
    let peak_t = if peak_temp_k.is_finite() {
        peak_temp_k.max(290.0)
    } else {
        1800.0
    };

    let mut t = vec![vec![0.0_f64; grid_n]; grid_n];
    let c_scale: Vec<(f64, String)>;

    if is_extinguished {
        for row in t.iter_mut() {
            for val in row.iter_mut() {
                *val = 300.0;
            }
        }
        c_scale = vec![
            (0.0, "#081326".to_string()),
            (0.5, "#0D2142".to_string()),
            (1.0, "#1A365D".to_string()),
        ];
    } else if g_c >= 0.80 {
        for j in 0..grid_n {
            let y = y_pts[j];
            let decay = safe_clamp(1.2 - 0.2 * (y - 0.5), 0.2, 1.2);
            for i in 0..grid_n {
                let x = x_pts[i];
                let dist_sq = (x * 2.2).powi(2) + ((y - 0.5) / 1.6).powi(2);
                t[j][i] = 300.0 + (peak_t - 300.0) * (-dist_sq).exp() * decay;
            }
        }
        c_scale = vec![
            (0.0, "#0C2D57".to_string()),
            (0.2, "#1D4ED8".to_string()),
            (0.45, "#F59E0B".to_string()),
            (0.75, "#EA580C".to_string()),
            (1.0, "#FEF08A".to_string()),
        ];
    } else if g_c <= 0.08 {
        let x_shift = v_c * 0.4;
        for j in 0..grid_n {
            let y = y_pts[j];
            for i in 0..grid_n {
                let x = x_pts[i];
                let dist_sq = (x - x_shift).powi(2) + y.powi(2);
                let r = dist_sq.sqrt();
                t[j][i] = 300.0 + (peak_t - 300.0) * (-((r - 1.0) / 0.7).powi(2)).exp();
            }
        }
        c_scale = vec![
            (0.0, "#0C2D57".to_string()),
            (0.25, "#0369A1".to_string()),
            (0.55, "#00B4D8".to_string()),
            (0.85, "#00F2FF".to_string()),
            (1.0, "#FFFFFF".to_string()),
        ];
    } else {
        for j in 0..grid_n {
            let y = y_pts[j];
            for i in 0..grid_n {
                let x = x_pts[i];
                let dist_sq = (x / 1.8).powi(2) + ((y - 0.2) / 0.85).powi(2);
                t[j][i] = 300.0 + (peak_t - 300.0) * (-dist_sq).exp();
            }
        }
        c_scale = vec![
            (0.0, "#0C2D57".to_string()),
            (0.25, "#1E40AF".to_string()),
            (0.5, "#EF4444".to_string()),
            (0.8, "#F59E0B".to_string()),
            (1.0, "#FEF08A".to_string()),
        ];
    }

    (x_pts, y_pts, t, c_scale)
}
