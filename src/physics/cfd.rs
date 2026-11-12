use crate::physics::models::{FlightMaterial, MorphologyMetrics};

pub const CHAR_L: f64 = 0.05; // 5.0 cm characteristic length
pub const NU_0: f64 = 1.5e-5; // Kinematic viscosity at 1 atm (m^2/s)
pub const ALPHA_0: f64 = 2.2e-5; // Thermal diffusivity at 1 atm (m^2/s)
pub const P_0: f64 = 101.325; // Standard atmospheric pressure (kPa)
pub const G_0: f64 = 9.81; // Standard gravitational acceleration (m/s^2)

/// Computational Fluid Dynamics (CFD) and Flame Morphology Engine
pub struct CfdEngine;

impl CfdEngine {
    /// Calculate dimensionless fluid dynamics numbers and morphology metrics.
    pub fn calculate_flame_morphology_metrics(
        gravity_g: f64,
        airflow_cm_s: f64,
        oxygen_pct: f64,
        pressure_kpa: f64,
        lang: &str,
        is_extinguished: bool,
        material: Option<&FlightMaterial>,
    ) -> MorphologyMetrics {
        let p_ratio = (pressure_kpa / P_0).max(0.1);
        let v_m_s = (airflow_cm_s / 100.0).max(0.001);

        // Reynolds number (ratio of inertial to viscous forces)
        let reynolds = (v_m_s * CHAR_L / NU_0) * p_ratio;

        // Grashof number (ratio of buoyancy to viscous forces)
        let g_accel = gravity_g.max(0.0) * G_0;
        let grashof =
            (g_accel * (1.0 / 300.0) * 1200.0 * CHAR_L.powi(3) / NU_0.powi(2)) * p_ratio.powi(2);

        // Richardson number (ratio of buoyancy to flow shear, Ri = Gr / Re^2)
        let richardson = if reynolds > 0.0 {
            grashof / reynolds.powi(2)
        } else {
            0.0
        };

        // Péclet number (ratio of advective to diffusive heat transport rate)
        let peclet = (v_m_s * CHAR_L / ALPHA_0) * p_ratio;

        // Damköhler number (ratio of chemical reaction rate to mass transport rate)
        let v_buoyant = 25.0 * gravity_g.max(0.0).sqrt();
        let v_eff = (airflow_cm_s.powi(2) + v_buoyant.powi(2)).sqrt().max(0.2);
        let damkohler = (12.0 / v_eff) * (oxygen_pct / 21.0).powf(1.2) * p_ratio.powf(0.8);

        if is_extinguished {
            let regime_code = "EXTINGUISHED".to_string();
            let aspect_ratio = 0.0;
            let color_theme = "#64748B".to_string();
            let peak_temp_k = 300.0;
            let (regime_name, morph_desc, soot_fraction) =
                Self::get_morphology_regime_info(&regime_code, gravity_g, lang);

            return MorphologyMetrics {
                grashof,
                reynolds,
                richardson,
                peclet,
                damkohler,
                aspect_ratio,
                regime_code,
                regime_name,
                color_theme,
                peak_temp_k,
                soot_fraction,
                morph_desc,
            };
        }

        // Regime transition weighting functions (clamped to physical degenerate floor >= 0.0g)
        let g_safe = gravity_g.max(0.0);
        let w_0g = (-(g_safe / 0.12).powi(2)).exp();
        let w_1g = 1.0 / (1.0 + (-10.0 * (g_safe - 0.55)).exp());
        let w_part = (1.0 - w_0g - w_1g).max(0.0);

        // Aspect ratio interpolation across regimes
        let ar_0g = 1.00 + 0.015 * airflow_cm_s;
        let ar_pg = 0.65 + 0.45 * g_safe.sqrt();
        let ar_1g = (3.20 - 0.02 * airflow_cm_s).max(2.2);
        let aspect_ratio = w_0g * ar_0g + w_part * ar_pg + w_1g * ar_1g;

        // Flame peak temperature computation
        let delta_t_o2 = 8.0 * (oxygen_pct - 21.0);
        let mut t_base = w_0g * 1380.0 + w_part * 1600.0 + w_1g * 1850.0;
        if let Some(mat) = material {
            let hoc = mat.heat_of_combustion_mj_kg;
            let delta_hoc = ((hoc - 25.0) * 8.5).clamp(-200.0, 250.0);
            t_base += delta_hoc;
        }
        let peak_temp_k = t_base + delta_t_o2;

        let (regime_code, color_theme) = if gravity_g >= 0.80 {
            ("BUOYANT_TEARDROP".to_string(), "#F59E0B".to_string())
        } else if gravity_g <= 0.08 {
            ("SPHERICAL_DIFFUSION".to_string(), "#00F2FF".to_string())
        } else {
            ("EXPANDING_HEMISPHERE".to_string(), "#E03C31".to_string())
        };

        let (regime_name, morph_desc, soot_fraction) =
            Self::get_morphology_regime_info(&regime_code, gravity_g, lang);

        MorphologyMetrics {
            grashof,
            reynolds,
            richardson,
            peclet,
            damkohler,
            aspect_ratio,
            regime_code,
            regime_name,
            color_theme,
            peak_temp_k,
            soot_fraction,
            morph_desc,
        }
    }

    /// Retrieve bilingual morphological regime description and metadata.
    pub fn get_morphology_regime_info(
        regime_code: &str,
        gravity_g: f64,
        lang: &str,
    ) -> (String, String, String) {
        if regime_code == "EXTINGUISHED" {
            if lang == "vi" {
                (
                    "DẬP TẮT HOÀN TOÀN (EXTINGUISHED)".to_string(),
                    "TRẠNG THÁI AN TOÀN: Nồng độ oxy hoặc tốc độ thông gió nằm ngoài giới hạn duy trì ngọn lửa (Oxy thấp hơn MOC hiệu dụng hoặc dập tắt do bức xạ / thổi tắt đối lưu). Không có phản ứng oxy hóa hoạt động; nhiệt độ ở mức môi trường khoang (~300K).".to_string(),
                    "0.0 (Không có phản ứng cháy)".to_string(),
                )
            } else {
                (
                    "COMPLETE EXTINCTION (EXTINGUISHED)".to_string(),
                    "SAFE QUENCHED STATE: Ambient cabin oxygen or ventilation flow is outside the flammability envelope (O2 below effective MOC or quenched via radiative heat loss / convective blowoff). Zero ongoing chemical combustion; temperature equals ambient cabin background (~300K).".to_string(),
                    "0.0 (Zero Active Combustion)".to_string(),
                )
            }
        } else if regime_code == "BUOYANT_TEARDROP" {
            if lang == "vi" {
                (
                    "Hình Giọt Nước Đối Lưu do Lực Nổi (1.0g Mặt Đất)".to_string(),
                    "Lực nổi tự nhiên mạnh mẽ (V_buoyant ~ 25 cm/s) kéo các sản phẩm cháy nóng lên trên tạo thành cột khói hình giọt nước thuôn dài hẹp. Dòng đối lưu cuốn oxy mạnh mẽ vào tâm lửa, tạo ra vệt bồ hóng phát sáng màu vàng cam bức xạ nhiệt mạnh trong dải hồng ngoại.".to_string(),
                    "Cao (1.2 × 10⁻⁶)".to_string(),
                )
            } else {
                (
                    "Buoyancy-Driven Convective Teardrop (1.0g)".to_string(),
                    "Strong natural buoyant updraft (V_buoyant ~ 25 cm/s) draws hot combustion gases upward into a narrow, elongated teardrop plume. Rapid convective entrainment feeds oxygen and creates an incandescent yellow-orange soot trail radiating heavily in the infrared spectrum.".to_string(),
                    "High (1.2 × 10⁻⁶)".to_string(),
                )
            }
        } else if regime_code == "SPHERICAL_DIFFUSION" {
            if lang == "vi" {
                (
                    "Hình Cầu Xanh Lam Thuần Khuếch Tán (0.0g Vi Trọng Lực)".to_string(),
                    "Sự biến mất hoàn toàn của lực nổi khiến quá trình vận chuyển oxy chỉ còn dựa vào khuếch tán phân tử 3D đẳng hướng. Ngọn lửa chuyển thành lớp vỏ hình cầu êm đềm, đối xứng hoàn hảo. Nhiệt độ thấp hơn (~1380K), ngăn chặn quá trình tinh thể hóa bồ hóng carbon và phát ra ánh sáng xanh lam thuần khiết từ các gốc kích thích CH* và C2*.".to_string(),
                    "Không đáng kể (< 0.05 × 10⁻⁶, Không bồ hóng)".to_string(),
                )
            } else {
                (
                    "Diffusion-Limited Pure Blue Sphere (0.0g)".to_string(),
                    "Complete absence of buoyancy causes oxidizer transport to rely purely on isotropic 3D molecular diffusion. The flame assumes a calm, perfectly symmetrical spherical shell. Temperatures remain cooler (~1380K), preventing carbon soot crystallization and emitting pure blue chemiluminescence from excited CH* and C2* radicals.".to_string(),
                    "Negligible (< 0.05 × 10⁻⁶, Soot-Free)".to_string(),
                )
            }
        } else {
            if lang == "vi" {
                (
                    format!("Hình Bán Cầu Bành Trướng Nguy Hiểm ({:.2}g Trọng Lực Một Phần)", gravity_g),
                    "HIỂM HỌA KHÔNG GIAN CỰC NGUY HIỂM: Trong trọng lực một phần (Mặt Trăng 0.16g, Sao Hỏa 0.38g), lực nổi quá yếu để tạo thành cột khói đối lưu thẳng đứng, nhưng đủ mạnh để phá vỡ tính đối xứng hình cầu. Khí cháy nóng bành trướng ngang thành hình vòm bán cầu với diện tích tiếp xúc chân lửa loang rộng, làm tăng diện tích bắt cháy bề mặt các cấu trúc xung quanh lên tới 240%!".to_string(),
                    "Trung bình (0.75 × 10⁻⁶, Màn khói bồ hóng lơ lửng)".to_string(),
                )
            } else {
                (
                    format!("Hazardous Expanding Hemispherical Dome ({:.2}g Partial Gravity)", gravity_g),
                    "CRITICAL SPACE HAZARD: In partial gravity (Moon 0.16g, Mars 0.38g), buoyant forces are too weak to form a vertical convective chimney, yet strong enough to destabilize spherical symmetry. Hot combustion gases mushroom laterally into an expanding hemispherical dome with a broad contact footprint, severely increasing the surface ignition area on surrounding spacecraft structures by up to 240%.".to_string(),
                    "Moderate (0.75 × 10⁻⁶, Lingering Smoke Blanket)".to_string(),
                )
            }
        }
    }
}
