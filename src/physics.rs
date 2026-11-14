use crate::models::FlameMorphologyMetrics;

#[inline]
pub fn safe_clamp(val: f64, min_val: f64, max_val: f64) -> f64 {
    if !val.is_finite() {
        if val.is_nan() || val.is_sign_negative() {
            return min_val;
        }
        return max_val;
    }
    if val < min_val {
        min_val
    } else if val > max_val {
        max_val
    } else {
        val
    }
}

#[inline]
fn sanitize_finite(val: f64, default: f64) -> f64 {
    if val.is_finite() {
        val
    } else {
        default
    }
}

pub fn calculate_effective_moc_core(
    moc_1g: f64,
    moc_ug: f64,
    gravity_g: f64,
    airflow_cm_s: f64,
    pressure_kpa: f64,
) -> f64 {
    let moc_1g_c = sanitize_finite(moc_1g, 21.0);
    let moc_ug_c = sanitize_finite(moc_ug, 18.0);
    let g_clamped = if gravity_g.is_nan() || gravity_g < 0.0 {
        0.0
    } else {
        gravity_g
    };
    let v_clean = if airflow_cm_s.is_nan() {
        0.0
    } else {
        airflow_cm_s
    };
    let p_clean = if pressure_kpa.is_nan() {
        101.3
    } else {
        safe_clamp(pressure_kpa, 0.0, 1e4)
    };

    let v_buoyant = 25.0 * g_clamped.sqrt();
    let v_eff = (v_clean.powi(2) + v_buoyant.powi(2)).sqrt();

    let mut delta_quench = 0.0;
    if v_eff < 3.5 {
        delta_quench = 5.0 * (1.0 - (v_eff / 3.5)).powf(1.5);
    }

    let mut delta_blowoff = 0.0;
    if v_eff > 25.0 {
        delta_blowoff = 0.16 * (v_eff - 25.0).powf(1.2);
    }

    let p_ratio = (p_clean / 101.3).max(0.1);
    let delta_pressure = 1.8 * (1.0 - p_ratio.powf(0.35));

    let g_factor = safe_clamp(g_clamped.sqrt(), 0.0, 1.0);
    let base_moc = moc_ug_c + (moc_1g_c - moc_ug_c) * g_factor;

    let effective_moc = base_moc + delta_quench + delta_blowoff + delta_pressure;
    if effective_moc.is_nan() {
        18.0
    } else {
        safe_clamp(effective_moc, 8.0, 60.0)
    }
}

pub fn calculate_flame_spread_rate_core(
    base_spread: f64,
    moc_ug: f64,
    gravity_g: f64,
    oxygen_pct: f64,
    pressure_kpa: f64,
    airflow_cm_s: f64,
    effective_moc: f64,
) -> f64 {
    if !oxygen_pct.is_finite() || !effective_moc.is_finite() {
        return 0.0;
    }
    if oxygen_pct < effective_moc {
        return 0.0;
    }

    let base_c = sanitize_finite(base_spread, 0.0).max(0.0);
    let moc_ug_c = sanitize_finite(moc_ug, 18.0);
    let g_clamped = if !gravity_g.is_finite() || gravity_g < 0.0 {
        0.0
    } else {
        gravity_g
    };
    let p_clean = sanitize_finite(pressure_kpa, 101.3);
    let v_clean = sanitize_finite(airflow_cm_s, 0.0);

    let o2_margin = (oxygen_pct - effective_moc).max(0.01);
    let o2_ref_span = (moc_ug_c * 0.3).max(4.0);
    let o2_scale = (o2_margin / o2_ref_span).powf(1.15);

    let p_scale = (p_clean / 101.3).max(0.1).sqrt();

    let v_b = 25.0 * g_clamped.sqrt();
    let v_total = (v_clean.powi(2) + v_b.powi(2)).sqrt();

    let vent_factor = if g_clamped < 0.1 {
        0.35 + 1.35 * (v_total / 12.0) * (1.0 - (v_total / 12.0)).exp()
    } else {
        0.70 + 0.50 * (v_total / 25.0).powf(0.85)
    };

    let spread_rate = base_c * o2_scale * p_scale * vent_factor;
    if spread_rate.is_finite() {
        spread_rate.max(0.0)
    } else {
        0.0
    }
}

pub fn calculate_space_fire_risk_score_core(
    effective_moc: f64,
    spread_rate: f64,
    oxygen_pct: f64,
    _pressure_kpa: f64,
    _airflow_cm_s: f64,
    hoc: f64,
) -> (f64, String, String) {
    if !oxygen_pct.is_finite() || !effective_moc.is_finite() {
        return (0.0, "Safe".to_string(), "#10B981".to_string());
    }
    if oxygen_pct < effective_moc {
        return (0.0, "Safe".to_string(), "#10B981".to_string());
    }

    let spread_c = if spread_rate.is_finite() {
        spread_rate.max(0.0)
    } else if spread_rate.is_nan() {
        0.0
    } else if spread_rate.is_sign_positive() {
        1e6
    } else {
        0.0
    };
    let hoc_c = if hoc.is_finite() {
        hoc.max(0.0)
    } else if hoc.is_nan() {
        25.0
    } else if hoc.is_sign_positive() {
        100.0
    } else {
        0.0
    };

    let o2_overage = oxygen_pct - effective_moc;
    let score_o2 = (o2_overage * 2.8).min(35.0);
    let score_spread = (spread_c * 20.0).min(35.0);
    let score_energy = ((hoc_c / 45.0) * 15.0).min(15.0);
    let cabin_o2_penalty = 15.0 * ((oxygen_pct - 21.0) / 19.0).max(0.0);

    let sfrs = score_o2 + score_spread + score_energy + cabin_o2_penalty;
    let sfrs = safe_clamp(sfrs, 5.0, 100.0);

    let (tier, color) = if sfrs >= 70.0 {
        ("Critical", "#E03C31")
    } else if sfrs >= 45.0 {
        ("High", "#F59E0B")
    } else if sfrs >= 20.0 {
        ("Moderate", "#38BDF8")
    } else {
        ("Safe", "#10B981")
    };

    (sfrs, tier.to_string(), color.to_string())
}

pub fn detect_cool_flames_core(
    cool_flame_susceptible: bool,
    eff_moc: f64,
    gravity_g: f64,
    airflow_cm_s: f64,
    oxygen_pct: f64,
    pressure_kpa: f64,
    lang: &str,
) -> (bool, String) {
    if !cool_flame_susceptible {
        let msg = if lang == "vi" {
            "Không nhạy cảm với chuyển dịch ngọn lửa lạnh."
        } else {
            "Not susceptible to cool flame transition."
        };
        return (false, msg.to_string());
    }

    if !eff_moc.is_finite()
        || !gravity_g.is_finite()
        || !airflow_cm_s.is_finite()
        || !oxygen_pct.is_finite()
        || !pressure_kpa.is_finite()
    {
        let msg = if lang == "vi" {
            "Chế độ đốt cháy tiêu chuẩn hoặc đã dập tắt."
        } else {
            "Standard combustion regime or quenched."
        };
        return (false, msg.to_string());
    }

    let g_c = gravity_g.max(0.0);
    let v_c = airflow_cm_s.max(0.0);

    if g_c <= 0.08
        && v_c <= 4.0
        && pressure_kpa >= 35.0
        && oxygen_pct >= eff_moc - 2.5
        && oxygen_pct <= eff_moc + 2.0
    {
        let msg = if lang == "vi" {
            "CẢNH BÁO NGUY HIỂM: Chế độ Ngọn Lửa Lạnh Đang Hoạt động. Tổn thất nhiệt bức xạ dập tắt vùng phản ứng nhiệt độ cao, đưa nhiên liệu vào quá trình oxy hóa hóa học vô hình, phát xạ thấp (600-800K). Sinh ra nồng độ khí Carbon Monoxide (CO) và formaldehyde kịch độc mà không phát ra ánh sáng cảnh báo cho phi hành đoàn."
        } else {
            "CRITICAL ALERT: Cool Flames Regime Active. Radiative heat loss suppresses the high-temperature reaction zone, transitioning fuel into an invisible, low-luminosity chemical oxidation process (600-800K). Generates high levels of toxic Carbon Monoxide (CO) and formaldehydes without visible crew warning."
        };
        (true, msg.to_string())
    } else {
        let msg = if lang == "vi" {
            "Chế độ đốt cháy tiêu chuẩn hoặc đã dập tắt."
        } else {
            "Standard combustion regime or quenched."
        };
        (false, msg.to_string())
    }
}

pub fn generate_extinction_curve_core(
    moc_1g: f64,
    moc_ug: f64,
    gravity_g: f64,
    pressure_kpa: f64,
) -> (Vec<f64>, Vec<f64>) {
    let moc_1g_c = sanitize_finite(moc_1g, 21.0);
    let moc_ug_c = sanitize_finite(moc_ug, 18.0);
    let g_c = if !gravity_g.is_finite() || gravity_g < 0.0 {
        0.0
    } else {
        gravity_g
    };
    let p_c = sanitize_finite(pressure_kpa, 101.3);

    let n = 60;
    let mut v_sweep = Vec::with_capacity(n);
    let mut moc_sweep = Vec::with_capacity(n);

    for i in 0..n {
        let v = 0.0 + (i as f64) * (50.0 / 59.0);
        let moc_val = calculate_effective_moc_core(moc_1g_c, moc_ug_c, g_c, v, p_c);
        v_sweep.push(v);
        moc_sweep.push(moc_val);
    }

    (v_sweep, moc_sweep)
}

pub fn get_morphology_regime_info(
    regime_code: &str,
    gravity_g: f64,
    _airflow_cm_s: f64,
    _oxygen_pct: f64,
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
                "Trung bình (0.35 × 10⁻⁶)".to_string(),
            )
        } else {
            (
                format!("Lateral Expanding Hemispherical Dome ({:.2}g Partial)", gravity_g),
                "HIGH-RISK SPACE HAZARD: Under fractional gravity (Moon 0.16g, Mars 0.38g), buoyant updraft is insufficient to create a vertical plume, yet strong enough to break spherical symmetry. Hot reacting gases flare laterally into an expanded hemispherical dome, expanding the flame contact footprint with adjacent surfaces by up to 240%!".to_string(),
                "Moderate (0.35 × 10⁻⁶)".to_string(),
            )
        }
    }
}

pub fn calculate_flame_morphology_metrics_core(
    gravity_g: f64,
    airflow_cm_s: f64,
    oxygen_pct: f64,
    pressure_kpa: f64,
    lang: &str,
    is_extinguished: bool,
    hoc: Option<f64>,
) -> FlameMorphologyMetrics {
    let g_clamped = if !gravity_g.is_finite() || gravity_g < 0.0 {
        0.0
    } else {
        gravity_g
    };
    let v_in = if airflow_cm_s.is_finite() {
        airflow_cm_s.max(0.0)
    } else {
        0.0
    };
    let o2_in = if oxygen_pct.is_finite() {
        oxygen_pct.clamp(0.0, 100.0)
    } else {
        21.0
    };
    let p_in = if pressure_kpa.is_finite() {
        pressure_kpa.clamp(10.0, 1e4)
    } else {
        101.325
    };

    let p_ratio = (p_in / 101.325).max(0.1);
    let v_m_s = (v_in / 100.0).max(0.001);
    let char_l = 0.05_f64;
    let nu_0 = 1.5e-5_f64;
    let alpha_0 = 2.2e-5_f64;

    let reynolds = (v_m_s * char_l / nu_0) * p_ratio;
    let g_accel = g_clamped * 9.81;
    let grashof =
        (g_accel * (1.0 / 300.0) * 1200.0 * (char_l.powi(3)) / (nu_0.powi(2))) * (p_ratio.powi(2));
    let richardson = if reynolds > 0.0 {
        grashof / (reynolds.powi(2))
    } else {
        0.0
    };
    let peclet = (v_m_s * char_l / alpha_0) * p_ratio;

    let v_buoyant = 25.0 * g_clamped.sqrt();
    let v_eff = (v_in.powi(2) + v_buoyant.powi(2)).sqrt().max(0.2);
    let damkohler = (12.0 / v_eff) * (o2_in / 21.0).max(0.0).powf(1.2) * p_ratio.powf(0.8);

    if is_extinguished {
        let regime_code = "EXTINGUISHED";
        let aspect_ratio = 0.0;
        let color_theme = "#64748B";
        let peak_temp_k = 300.0;
        let (regime_name, morph_desc, soot_fraction) =
            get_morphology_regime_info(regime_code, g_clamped, v_in, o2_in, lang);
        return FlameMorphologyMetrics {
            grashof,
            reynolds,
            richardson,
            peclet,
            damkohler,
            aspect_ratio,
            regime_code: regime_code.to_string(),
            regime_name,
            color_theme: color_theme.to_string(),
            peak_temp_k,
            soot_fraction,
            morph_desc,
        };
    }

    let w_0g = (-(g_clamped / 0.12).powi(2)).exp();
    let w_1g = 1.0 / (1.0 + (-10.0 * (g_clamped - 0.55)).exp());
    let w_part = (1.0 - w_0g - w_1g).max(0.0);

    let ar_0g = 1.00 + 0.015 * v_in;
    let ar_pg = 0.65 + 0.45 * g_clamped.sqrt();
    let ar_1g = (3.20 - 0.02 * v_in).max(2.2);
    let aspect_ratio = w_0g * ar_0g + w_part * ar_pg + w_1g * ar_1g;

    let delta_t_o2 = 8.0 * (o2_in - 21.0);
    let mut t_base = w_0g * 1380.0 + w_part * 1600.0 + w_1g * 1850.0;
    if let Some(h) = hoc {
        if h.is_finite() {
            let delta_hoc = safe_clamp((h - 25.0) * 8.5, -200.0, 250.0);
            t_base += delta_hoc;
        }
    }
    let peak_temp_k = t_base + delta_t_o2;

    let (regime_code, color_theme) = if g_clamped >= 0.80 {
        ("BUOYANT_TEARDROP", "#F59E0B")
    } else if g_clamped <= 0.08 {
        ("SPHERICAL_DIFFUSION", "#00F2FF")
    } else {
        ("EXPANDING_HEMISPHERE", "#E03C31")
    };

    let (regime_name, morph_desc, soot_fraction) =
        get_morphology_regime_info(regime_code, g_clamped, v_in, o2_in, lang);

    FlameMorphologyMetrics {
        grashof,
        reynolds,
        richardson,
        peclet,
        damkohler,
        aspect_ratio,
        regime_code: regime_code.to_string(),
        regime_name,
        color_theme: color_theme.to_string(),
        peak_temp_k,
        soot_fraction,
        morph_desc,
    }
}
