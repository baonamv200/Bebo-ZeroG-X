//! Bilingual Internationalization & Localization Engine (i18n)
//! Supporting English (en) and Vietnamese (vi) with 100% key parity,
//! emergency suppression protocols, NASA flight research records, and CFD morphology descriptors.

pub mod research;
pub mod suppression;
pub mod translations;

pub use research::*;
pub use suppression::*;
pub use translations::*;

use serde::{Deserialize, Serialize};

/// Supported interface languages.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, Serialize, Deserialize)]
pub enum Language {
    #[serde(rename = "en")]
    En,
    #[serde(rename = "vi")]
    Vi,
}

impl Default for Language {
    fn default() -> Self {
        Language::En
    }
}

impl Language {
    pub fn as_str(&self) -> &'static str {
        match self {
            Language::En => "en",
            Language::Vi => "vi",
        }
    }

    /// Loose parser from string, defaulting to Vietnamese per legacy `i18n.py:676`.
    pub fn from_str_loose(s: &str) -> Self {
        match s.trim().to_lowercase().as_str() {
            "en" | "english" => Language::En,
            _ => Language::Vi,
        }
    }
}

/// Structured suppression protocol for flight materials.
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct SuppressionProtocol {
    pub name: &'static str,
    pub action_1: &'static str,
    pub optimal_agent: &'static str,
    pub secondary_hazard: &'static str,
    pub decontamination: &'static str,
}

/// Structured research record for NASA PSI flight experiments.
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct ResearchRecord {
    pub experiment: &'static str,
    pub psi_id: &'static str,
    pub pis: &'static str,
    pub facility: &'static str,
    pub finding: &'static str,
    pub citation: &'static str,
}

/// Flame morphology regime descriptors and radiative soot fraction.
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq)]
pub struct MorphologyInfo {
    pub regime_name: String,
    pub morph_desc: String,
    pub soot_fraction: String,
}

/// Primary protocol lookup alias.
pub fn get_protocol(material_id: &str, lang: Language) -> Option<SuppressionProtocol> {
    suppression::get_suppression_protocol(material_id, lang)
}

/// Retrieve regime description, morphology summary, and soot fraction.
/// Matches `i18n.py:702-773`.
pub fn get_morphology_regime_info(
    regime_code: &str,
    gravity_g: f64,
    _airflow_cm_s: f64,
    _oxygen_pct: f64,
    lang: Language,
) -> MorphologyInfo {
    match regime_code {
        "EXTINGUISHED" => match lang {
            Language::Vi => MorphologyInfo {
                regime_name: "DẬP TẮT HOÀN TOÀN (EXTINGUISHED)".to_string(),
                morph_desc: "TRẠNG THÁI AN TOÀN: Nồng độ oxy hoặc tốc độ thông gió nằm ngoài giới hạn duy trì ngọn lửa (Oxy thấp hơn MOC hiệu dụng hoặc dập tắt do bức xạ / thổi tắt đối lưu). Không có phản ứng oxy hóa hoạt động; nhiệt độ ở mức môi trường khoang (~300K).".to_string(),
                soot_fraction: "0.0 (Không có phản ứng cháy)".to_string(),
            },
            Language::En => MorphologyInfo {
                regime_name: "COMPLETE EXTINCTION (EXTINGUISHED)".to_string(),
                morph_desc: "SAFE QUENCHED STATE: Ambient cabin oxygen or ventilation flow is outside the flammability envelope (O2 below effective MOC or quenched via radiative heat loss / convective blowoff). Zero ongoing chemical combustion; temperature equals ambient cabin background (~300K).".to_string(),
                soot_fraction: "0.0 (Zero Active Combustion)".to_string(),
            },
        },
        "BUOYANT_TEARDROP" => match lang {
            Language::Vi => MorphologyInfo {
                regime_name: "Hình Giọt Nước Đối Lưu do Lực Nổi (1.0g Mặt Đất)".to_string(),
                morph_desc: "Lực nổi tự nhiên mạnh mẽ (V_buoyant ~ 25 cm/s) kéo các sản phẩm cháy nóng lên trên tạo thành cột khói hình giọt nước thuôn dài hẹp. Dòng đối lưu cuốn oxy mạnh mẽ vào tâm lửa, tạo ra vệt bồ hóng phát sáng màu vàng cam bức xạ nhiệt mạnh trong dải hồng ngoại.".to_string(),
                soot_fraction: "Cao (1.2 × 10⁻⁶)".to_string(),
            },
            Language::En => MorphologyInfo {
                regime_name: "Buoyancy-Driven Convective Teardrop (1.0g)".to_string(),
                morph_desc: "Strong natural buoyant updraft (V_buoyant ~ 25 cm/s) draws hot combustion gases upward into a narrow, elongated teardrop plume. Rapid convective entrainment feeds oxygen and creates an incandescent yellow-orange soot trail radiating heavily in the infrared spectrum.".to_string(),
                soot_fraction: "High (1.2 × 10⁻⁶)".to_string(),
            },
        },
        "SPHERICAL_DIFFUSION" => match lang {
            Language::Vi => MorphologyInfo {
                regime_name: "Hình Cầu Xanh Lam Thuần Khuếch Tán (0.0g Vi Trọng Lực)".to_string(),
                morph_desc: "Sự biến mất hoàn toàn của lực nổi khiến quá trình vận chuyển oxy chỉ còn dựa vào khuếch tán phân tử 3D đẳng hướng. Ngọn lửa chuyển thành lớp vỏ hình cầu êm đềm, đối xứng hoàn hảo. Nhiệt độ thấp hơn (~1380K), ngăn chặn quá trình tinh thể hóa bồ hóng carbon và phát ra ánh sáng xanh lam thuần khiết từ các gốc kích thích CH* và C2*.".to_string(),
                soot_fraction: "Không đáng kể (< 0.05 × 10⁻⁶, Không bồ hóng)".to_string(),
            },
            Language::En => MorphologyInfo {
                regime_name: "Diffusion-Limited Pure Blue Sphere (0.0g)".to_string(),
                morph_desc: "Complete absence of buoyancy causes oxidizer transport to rely purely on isotropic 3D molecular diffusion. The flame assumes a calm, perfectly symmetrical spherical shell. Temperatures remain cooler (~1380K), preventing carbon soot crystallization and emitting pure blue chemiluminescence from excited CH* and C2* radicals.".to_string(),
                soot_fraction: "Negligible (< 0.05 × 10⁻⁶, Soot-Free)".to_string(),
            },
        },
        _ => match lang {
            Language::Vi => MorphologyInfo {
                regime_name: format!("Hình Bán Cầu Bành Trướng Nguy Hiểm ({gravity_g:.2}g Trọng Lực Một Phần)"),
                morph_desc: "HIỂM HỌA KHÔNG GIAN CỰC NGUY HIỂM: Trong trọng lực một phần (Mặt Trăng 0.16g, Sao Hỏa 0.38g), lực nổi quá yếu để tạo thành cột khói đối lưu thẳng đứng, nhưng đủ mạnh để phá vỡ tính đối xứng hình cầu. Khí cháy nóng bành trướng ngang thành hình vòm bán cầu với diện tích tiếp xúc chân lửa loang rộng, làm tăng diện tích bắt cháy bề mặt các cấu trúc xung quanh lên tới 240%!".to_string(),
                soot_fraction: "Trung bình (0.75 × 10⁻⁶, Màn khói bồ hóng lơ lửng)".to_string(),
            },
            Language::En => MorphologyInfo {
                regime_name: format!("Hazardous Expanding Hemispherical Dome ({gravity_g:.2}g Partial Gravity)"),
                morph_desc: "CRITICAL SPACE HAZARD: In partial gravity (Moon 0.16g, Mars 0.38g), buoyant forces are too weak to form a vertical convective chimney, yet strong enough to destabilize spherical symmetry. Hot combustion gases mushroom laterally into an expanding hemispherical dome with a broad contact footprint, severely increasing the surface ignition area on surrounding spacecraft structures by up to 240%.".to_string(),
                soot_fraction: "Moderate (0.75 × 10⁻⁶, Lingering Smoke Blanket)".to_string(),
            },
        },
    }
}

/// Direct alias matching SCOPE.md interface contract.
pub fn get_regime_info(
    regime_code: &str,
    gravity_g: f64,
    airflow_cm_s: f64,
    oxygen_pct: f64,
    lang: Language,
) -> MorphologyInfo {
    get_morphology_regime_info(regime_code, gravity_g, airflow_cm_s, oxygen_pct, lang)
}
