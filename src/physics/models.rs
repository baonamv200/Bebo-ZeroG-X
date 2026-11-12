use serde::{Deserialize, Deserializer, Serialize};

/// Custom deserializer for booleans accepting True, False, true, false, 1, 0, yes, no.
pub fn deserialize_bool_flexible<'de, D>(deserializer: D) -> Result<bool, D::Error>
where
    D: Deserializer<'de>,
{
    let s = String::deserialize(deserializer)?;
    match s.trim().to_lowercase().as_str() {
        "true" | "1" | "yes" => Ok(true),
        "false" | "0" | "no" => Ok(false),
        other => Err(serde::de::Error::custom(format!(
            "invalid boolean literal: '{}'",
            other
        ))),
    }
}

/// Standardized NASA Flight Material Specification (MAT-01 to MAT-10)
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct FlightMaterial {
    pub material_id: String,
    pub material_name: String,
    pub material_name_vi: String,
    pub psi_id: String,
    pub mission: String,
    pub category: String,
    pub category_vi: String,
    pub geometry: String,
    pub geometry_vi: String,
    pub moc_1g: f64,
    pub moc_microg: f64,
    pub base_spread_rate_mm_s: f64,
    pub chemical_formula: String,
    pub heat_of_combustion_mj_kg: f64,
    pub cool_flame_susceptible: bool,
    pub flame_morphology: String,
    pub flame_morphology_vi: String,
    pub quenching_mode: String,
    pub quenching_mode_vi: String,
    pub summary_notes: String,
}

/// NASA SoFIE (Solid Fuel Ignition and Extinction) PMMA Test Record
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct SofieRecord {
    pub test_id: String,
    pub material: String,
    pub gravity_level: String,
    pub oxygen_pct: f64,
    pub airflow_velocity_cm_s: f64,
    pub pressure_kpa: f64,
    pub flame_spread_rate_mm_s: f64,
    pub flame_length_mm: f64,
    pub flame_temp_k: f64,
    pub soot_volume_fraction_ppm: f64,
    #[serde(deserialize_with = "deserialize_bool_flexible")]
    pub quenching_observed: bool,
    #[serde(deserialize_with = "deserialize_bool_flexible")]
    pub cool_flame_transition: bool,
}

/// NASA Saffire (Spacecraft Fire Safety Experiment) Large-Scale Flammability Record
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct SaffireRecord {
    pub test_id: String,
    pub material: String,
    pub mission: String,
    pub pressure_kpa: f64,
    pub oxygen_pct: f64,
    pub airflow_velocity_cm_s: f64,
    pub gravity_g: f64,
    pub flame_spread_rate_mm_s: f64,
    pub radiant_heat_flux_kw_m2: f64,
    pub pyrolyzed_area_cm2: f64,
    pub peak_heat_release_rate_kw: f64,
    pub extinction_mode: String,
}

/// NASA BASS (Burning and Suppression of Solids) Microgravity Test Record
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct BassRecord {
    pub test_id: String,
    pub material: String,
    pub geometry: String,
    pub airflow_velocity_cm_s: f64,
    pub limiting_oxygen_index_pct: f64,
    pub extinction_mechanism: String,
    #[serde(deserialize_with = "deserialize_bool_flexible")]
    pub cool_flame_observed: bool,
    pub nasa_psi_experiment_id: String,
}

/// Space Fire Risk Score (SFRS) Threat Tier
#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
pub enum RiskTier {
    Safe,
    Moderate,
    High,
    Critical,
}

impl RiskTier {
    pub fn as_str(&self) -> &'static str {
        match self {
            RiskTier::Safe => "Safe",
            RiskTier::Moderate => "Moderate",
            RiskTier::High => "High",
            RiskTier::Critical => "Critical",
        }
    }

    pub fn color_hex(&self) -> &'static str {
        match self {
            RiskTier::Safe => "#10B981",
            RiskTier::Moderate => "#38BDF8",
            RiskTier::High => "#F59E0B",
            RiskTier::Critical => "#E03C31",
        }
    }
}

/// Full Assessment Breakdown for Space Fire Risk Score
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct SfrsAssessment {
    pub score: f64,
    pub tier: RiskTier,
    pub color_code: String,
    pub score_o2: f64,
    pub score_spread: f64,
    pub score_energy: f64,
    pub penalty_cabin: f64,
}

/// Cool Flame Detection Outcome
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct CoolFlameResult {
    pub active: bool,
    pub message: String,
}

/// Fluid Dynamics and Combustion Morphology Metrics
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct MorphologyMetrics {
    pub grashof: f64,
    pub reynolds: f64,
    pub richardson: f64,
    pub peclet: f64,
    pub damkohler: f64,
    pub aspect_ratio: f64,
    pub regime_code: String,
    pub regime_name: String,
    pub color_theme: String,
    pub peak_temp_k: f64,
    pub soot_fraction: String,
    pub morph_desc: String,
}

/// 2D Thermal Temperature Mesh (60x60 grid)
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct ThermalMesh2D {
    pub x: Vec<f64>,
    pub y: Vec<f64>,
    pub z_temp_k: Vec<Vec<f64>>,
    pub color_scale: Vec<(f64, String)>,
}

/// 3D Geometric Vertex
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct Vertex3D {
    pub x: f64,
    pub y: f64,
    pub z: f64,
    pub temp_k: f64,
}

/// 3D Parametric Flame Surface Mesh
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct SurfaceMesh3D {
    pub name: String,
    pub vertices: Vec<Vec<Vertex3D>>,
    pub opacity: f64,
    pub color_scale: Vec<(f64, String)>,
}

/// Material Risk Ranking Row for HUD Table
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct MaterialRiskRow {
    pub material_id: String,
    pub material_name: String,
    pub effective_moc: f64,
    pub flame_spread_rate: f64,
    pub sfrs_score: f64,
    pub risk_tier: RiskTier,
    pub cool_flame_susceptible: bool,
    pub cool_flame_active: bool,
}

/// Top-Level Simulation Input Contract
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct SimulationInput {
    pub gravity_g: f64,
    pub oxygen_pct: f64,
    pub pressure_kpa: f64,
    pub airflow_cm_s: f64,
    pub material_id: String,
    pub lang: String,
}

/// Top-Level Simulation Output Contract
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct SimulationOutput {
    pub materials_ranking: Vec<MaterialRiskRow>,
    pub selected_material: FlightMaterial,
    pub effective_moc: f64,
    pub flame_spread_rate: f64,
    pub sfrs: SfrsAssessment,
    pub cool_flames: CoolFlameResult,
    pub morphology: MorphologyMetrics,
    pub active_regime: String,
}
