use std::f64::consts::PI;
use crate::physics::models::{SurfaceMesh3D, ThermalMesh2D, Vertex3D};

/// 2D and 3D Thermal Field and Geometry Generation Engine
pub struct ThermalMeshEngine;

impl ThermalMeshEngine {
    /// Calculate 60x60 2D temperature field over space coordinates x in [-3.0, 3.0], y in [-2.0, 4.0].
    pub fn calculate_temperature_mesh(
        gravity_g: f64,
        airflow_cm_s: f64,
        peak_temp_k: f64,
        is_extinguished: bool,
    ) -> ThermalMesh2D {
        let grid_n = 60;
        let mut x_pts = Vec::with_capacity(grid_n);
        let mut y_pts = Vec::with_capacity(grid_n);

        let step_x = 6.0 / (grid_n as f64 - 1.0);
        let step_y = 6.0 / (grid_n as f64 - 1.0);

        for i in 0..grid_n {
            x_pts.push(-3.0 + i as f64 * step_x);
            y_pts.push(-2.0 + i as f64 * step_y);
        }

        let g_c = gravity_g.max(0.0);
        let v_c = airflow_cm_s / 25.0;

        let mut z_temp_k = Vec::with_capacity(grid_n);
        let color_scale: Vec<(f64, String)>;

        if is_extinguished {
            color_scale = vec![
                (0.0, "#081326".to_string()),
                (0.5, "#0D2142".to_string()),
                (1.0, "#1A365D".to_string()),
            ];
            for _ in 0..grid_n {
                z_temp_k.push(vec![300.0; grid_n]);
            }
        } else if g_c >= 0.80 {
            color_scale = vec![
                (0.0, "#0C2D57".to_string()),
                (0.2, "#1D4ED8".to_string()),
                (0.45, "#F59E0B".to_string()),
                (0.75, "#EA580C".to_string()),
                (1.0, "#FEF08A".to_string()),
            ];
            for &y in &y_pts {
                let mut row = Vec::with_capacity(grid_n);
                for &x in &x_pts {
                    let dist_sq = (x * 2.2).powi(2) + ((y - 0.5) / 1.6).powi(2);
                    let y_clamp = (1.2 - 0.2 * (y - 0.5)).clamp(0.2, 1.2);
                    let t = 300.0 + (peak_temp_k - 300.0) * (-dist_sq).exp() * y_clamp;
                    row.push(t);
                }
                z_temp_k.push(row);
            }
        } else if g_c <= 0.08 {
            color_scale = vec![
                (0.0, "#0C2D57".to_string()),
                (0.25, "#0369A1".to_string()),
                (0.55, "#00B4D8".to_string()),
                (0.85, "#00F2FF".to_string()),
                (1.0, "#FFFFFF".to_string()),
            ];
            let x_shift = v_c * 0.4;
            for &y in &y_pts {
                let mut row = Vec::with_capacity(grid_n);
                for &x in &x_pts {
                    let dist_sq = (x - x_shift).powi(2) + y.powi(2);
                    let r = dist_sq.sqrt();
                    let t = 300.0 + (peak_temp_k - 300.0) * (-((r - 1.0) / 0.7).powi(2)).exp();
                    row.push(t);
                }
                z_temp_k.push(row);
            }
        } else {
            color_scale = vec![
                (0.0, "#0C2D57".to_string()),
                (0.25, "#1E40AF".to_string()),
                (0.5, "#EF4444".to_string()),
                (0.8, "#F59E0B".to_string()),
                (1.0, "#FEF08A".to_string()),
            ];
            for &y in &y_pts {
                let mut row = Vec::with_capacity(grid_n);
                for &x in &x_pts {
                    let dist_sq = (x / 1.8).powi(2) + ((y - 0.2) / 0.85).powi(2);
                    let t = 300.0 + (peak_temp_k - 300.0) * (-dist_sq).exp();
                    row.push(t);
                }
                z_temp_k.push(row);
            }
        }

        ThermalMesh2D {
            x: x_pts,
            y: y_pts,
            z_temp_k,
            color_scale,
        }
    }

    /// Generate 3D parametric flame shell surfaces and sample fuel rod geometry.
    pub fn generate_3d_flame_surfaces(
        gravity_g: f64,
        _airflow_cm_s: f64,
        peak_temp_k: f64,
        is_extinguished: bool,
        lang: &str,
    ) -> Vec<SurfaceMesh3D> {
        let g_c = gravity_g.max(0.0);
        let t_peak = peak_temp_k;

        let u_steps = 36;
        let v_steps = 48;
        let mut u_vals = Vec::with_capacity(u_steps);
        let mut v_vals = Vec::with_capacity(v_steps);

        for i in 0..u_steps {
            u_vals.push(i as f64 * PI / (u_steps as f64 - 1.0));
        }
        for j in 0..v_steps {
            v_vals.push(j as f64 * (2.0 * PI) / (v_steps as f64 - 1.0));
        }

        let mut meshes = Vec::new();

        if is_extinguished {
            let r = 1.05;
            let z_c = 0.50;
            let mut grid = Vec::with_capacity(v_steps);

            for &v in &v_vals {
                let mut row = Vec::with_capacity(u_steps);
                for &u in &u_vals {
                    row.push(Vertex3D {
                        x: r * u.sin() * v.cos(),
                        y: r * u.sin() * v.sin(),
                        z: r * u.cos() + z_c,
                        temp_k: 300.0,
                    });
                }
                grid.push(row);
            }

            meshes.push(SurfaceMesh3D {
                name: if lang == "vi" {
                    "Khu vực Đã Dập Tắt (Nhiệt độ 300K)".to_string()
                } else {
                    "Extinguished / Cold Zone (300K)".to_string()
                },
                vertices: grid,
                opacity: 0.35,
                color_scale: vec![
                    (0.0, "#1E293B".to_string()),
                    (0.5, "#334155".to_string()),
                    (1.0, "#475569".to_string()),
                ],
            });
        } else if g_c <= 0.08 {
            // Microgravity 0g: Concentric spherical diffusion shell
            let r_flame = 1.35;
            let z_c = 0.50;
            let mut shell_grid = Vec::with_capacity(v_steps);

            for &v in &v_vals {
                let mut row = Vec::with_capacity(u_steps);
                for &u in &u_vals {
                    let temp = t_peak - 70.0 * (1.0 - u.cos());
                    row.push(Vertex3D {
                        x: r_flame * u.sin() * v.cos(),
                        y: r_flame * u.sin() * v.sin(),
                        z: r_flame * u.cos() + z_c,
                        temp_k: temp,
                    });
                }
                shell_grid.push(row);
            }

            meshes.push(SurfaceMesh3D {
                name: if lang == "vi" {
                    "Vỏ Xanh Lam Thuần CH*/C2*".to_string()
                } else {
                    "Pure Blue CH*/C2* Shell".to_string()
                },
                vertices: shell_grid,
                opacity: 0.88,
                color_scale: vec![
                    (0.0, "#082F49".to_string()),
                    (0.2, "#0369A1".to_string()),
                    (0.5, "#0284C7".to_string()),
                    (0.8, "#00E5FF".to_string()),
                    (1.0, "#E0F2FE".to_string()),
                ],
            });

            // Inner diffusion core (r = 0.70)
            let r_core = 0.70;
            let mut core_grid = Vec::with_capacity(v_steps);
            for &v in &v_vals {
                let mut row = Vec::with_capacity(u_steps);
                for &u in &u_vals {
                    row.push(Vertex3D {
                        x: r_core * u.sin() * v.cos(),
                        y: r_core * u.sin() * v.sin(),
                        z: r_core * u.cos() + z_c,
                        temp_k: t_peak * 0.72,
                    });
                }
                core_grid.push(row);
            }

            meshes.push(SurfaceMesh3D {
                name: if lang == "vi" {
                    "Lõi Khuếch Tán Đồng Tâm".to_string()
                } else {
                    "Concentric Diffusion Core".to_string()
                },
                vertices: core_grid,
                opacity: 0.60,
                color_scale: vec![
                    (0.0, "#020617".to_string()),
                    (0.5, "#0B192C".to_string()),
                    (1.0, "#1E3E62".to_string()),
                ],
            });
        } else if g_c >= 0.80 {
            // Terrestrial 1.0g: Buoyant teardrop
            let h_flame = 3.65;
            let r_max = 1.15;
            let mut shell_grid = Vec::with_capacity(v_steps);

            for &v in &v_vals {
                let mut row = Vec::with_capacity(u_steps);
                for &u in &u_vals {
                    let z_norm = (1.0 - u.cos()) / 2.0;
                    let z = 0.05 + (1.0 - z_norm) * h_flame;
                    let height_factor = 1.0 - z_norm;
                    let mut r_envelope = r_max
                        * 2.6
                        * (height_factor + 1e-4).max(0.0).sqrt()
                        * (1.0 - height_factor + 0.18)
                        * (u / 2.0).sin();
                    r_envelope = r_envelope.max(0.04);

                    let t_surf = 300.0
                        + (t_peak - 300.0) * (0.45 + 0.55 * (-((z - 0.8) / 1.1).powi(2)).exp());

                    row.push(Vertex3D {
                        x: r_envelope * v.cos(),
                        y: r_envelope * v.sin(),
                        z,
                        temp_k: t_surf,
                    });
                }
                shell_grid.push(row);
            }

            meshes.push(SurfaceMesh3D {
                name: if lang == "vi" {
                    "Ngọn Lửa Giọt Nước Đối Lưu".to_string()
                } else {
                    "Buoyant Teardrop Plume".to_string()
                },
                vertices: shell_grid,
                opacity: 0.92,
                color_scale: vec![
                    (0.0, "#450A0A".to_string()),
                    (0.2, "#991B1B".to_string()),
                    (0.45, "#EA580C".to_string()),
                    (0.75, "#FBBF24".to_string()),
                    (1.0, "#FEF08A".to_string()),
                ],
            });
        } else {
            // Partial gravity (Lunar / Mars): Expanding hemispherical dome
            let h_dome = 1.40;
            let r_base = 1.55;
            let rod_radius = 0.35;
            let mut dome_grid = Vec::with_capacity(v_steps);

            for &v in &v_vals {
                let mut row = Vec::with_capacity(u_steps);
                for &u in &u_vals {
                    let (z, r_env, t_surf) = if u <= PI / 2.0 {
                        let z_val = 0.02 + h_dome * (1.0 - (u / (PI / 2.0)).powf(1.5));
                        let r_val = r_base * u.sin();
                        let u_norm = (u / (PI / 2.0)).clamp(0.0, 1.0);
                        let temp = 300.0 + (t_peak - 300.0) * (0.60 + 0.40 * (u_norm * 0.9).cos());
                        (z_val, r_val, temp)
                    } else {
                        let z_val = 0.02;
                        let s = ((u - PI / 2.0) / (PI / 2.0)).clamp(0.0, 1.0);
                        let r_val = r_base * (1.0 - s) + rod_radius * s;
                        let temp = 300.0 + (t_peak - 300.0) * 0.55 * (1.0 - 0.45 * s);
                        (z_val, r_val, temp)
                    };

                    row.push(Vertex3D {
                        x: r_env * v.cos(),
                        y: r_env * v.sin(),
                        z,
                        temp_k: t_surf,
                    });
                }
                dome_grid.push(row);
            }

            meshes.push(SurfaceMesh3D {
                name: if lang == "vi" {
                    "Vòm Bán Cầu Bành Trướng".to_string()
                } else {
                    "Expanding Hemispherical Dome".to_string()
                },
                vertices: dome_grid,
                opacity: 0.94,
                color_scale: vec![
                    (0.0, "#0C2340".to_string()),
                    (0.2, "#1D4ED8".to_string()),
                    (0.45, "#991B1B".to_string()),
                    (0.70, "#EA580C".to_string()),
                    (0.90, "#F59E0B".to_string()),
                    (1.0, "#FDE047".to_string()),
                ],
            });
        }

        // Add fuel sample rod cylinder
        let rod_radius = 0.35;
        let rod_levels = 12;
        let rod_theta_steps = 32;
        let mut rod_grid = Vec::with_capacity(rod_theta_steps);

        for j in 0..rod_theta_steps {
            let theta = j as f64 * (2.0 * PI) / (rod_theta_steps as f64 - 1.0);
            let mut row = Vec::with_capacity(rod_levels);
            for i in 0..rod_levels {
                let z = -1.30 + i as f64 * (1.35 / (rod_levels as f64 - 1.0));
                row.push(Vertex3D {
                    x: rod_radius * theta.cos(),
                    y: rod_radius * theta.sin(),
                    z,
                    temp_k: 350.0,
                });
            }
            rod_grid.push(row);
        }

        meshes.push(SurfaceMesh3D {
            name: if lang == "vi" {
                "Thanh Mẫu Nhiên Liệu".to_string()
            } else {
                "Fuel Sample Rod".to_string()
            },
            vertices: rod_grid,
            opacity: 0.95,
            color_scale: vec![
                (0.0, "#334155".to_string()),
                (0.5, "#475569".to_string()),
                (1.0, "#64748B".to_string()),
            ],
        });

        meshes
    }
}
