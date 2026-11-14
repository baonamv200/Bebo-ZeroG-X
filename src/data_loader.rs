use std::collections::HashMap;
use std::fs::File;
use std::path::{Path, PathBuf};
use crate::models::Material;

pub fn get_embedded_materials() -> Vec<Material> {
    vec![
        Material {
            material_id: "MAT-01".to_string(),
            material_name: "PMMA / Acrylic Rod (6.35mm)".to_string(),
            material_name_vi: "Thanh nhựa Acrylic / PMMA (6.35mm)".to_string(),
            psi_id: "PSI-SOFIE-GEL-412".to_string(),
            mission: "NASA SoFIE (Growth & Extinction Limit)".to_string(),
            category: "Structural Polymer / Optical Window".to_string(),
            category_vi: "Polymer cấu trúc / Cửa sổ quang học".to_string(),
            geometry: "Solid Cylindrical Rod".to_string(),
            geometry_vi: "Thanh trụ tròn đặc (6.35mm)".to_string(),
            moc_1g: 17.0,
            moc_microg: 15.5,
            base_spread_rate_mm_s: 0.51,
            chemical_formula: "[C5O2H8]n".to_string(),
            heat_of_combustion_mj_kg: 26.2,
            cool_flame_susceptible: true,
            flame_morphology: "Spherical Blue Cap with Downstream Soot Tail".to_string(),
            flame_morphology_vi: "Chỏm cầu xanh lam kèm đuôi bồ hóng xuôi dòng".to_string(),
            quenching_mode: "Radiative Quenching at V < 2 cm/s; Blowoff at V > 45 cm/s".to_string(),
            quenching_mode_vi: "Tự dập bức xạ ở V < 2 cm/s; Thổi tắt đối lưu ở V > 45 cm/s".to_string(),
            summary_notes: "Benchmark thermoplastic studied across SoFIE and BASS. In 0g with 10 cm/s airflow, burns intensely without buoyant convection cooling. Capable of low-temperature smolder transition.".to_string(),
        },
        Material {
            material_id: "MAT-02".to_string(),
            material_name: "Cotton-Fiberglass Blend (75/25)".to_string(),
            material_name_vi: "Vải dệt Cotton - Sợi thủy tinh (75/25)".to_string(),
            psi_id: "PSI-SAFFIRE-I-084".to_string(),
            mission: "NASA Saffire-I & Saffire-IV (Large Scale)".to_string(),
            category: "Cabin Fabric / Acoustic Blanket".to_string(),
            category_vi: "Vải cabin / Đệm cách âm".to_string(),
            geometry: "Woven Fabric Sheet (0.4m x 1.0m)".to_string(),
            geometry_vi: "Tấm vải dệt phẳng (0.4m x 1.0m)".to_string(),
            moc_1g: 16.0,
            moc_microg: 14.8,
            base_spread_rate_mm_s: 0.85,
            chemical_formula: "Cellulose / SiO2 Matrix".to_string(),
            heat_of_combustion_mj_kg: 17.5,
            cool_flame_susceptible: false,
            flame_morphology: "Wide Planar Flame Front with Vigorous Glowing Char".to_string(),
            flame_morphology_vi: "Mặt lửa phẳng rộng kèm lớp than hồng phát sáng mạnh".to_string(),
            quenching_mode: "Quenches when oxygen drops below 14.8% under forced flow".to_string(),
            quenching_mode_vi: "Tự tắt khi nồng độ Oxy giảm dưới 14.8% trong luồng gió cưỡng bức".to_string(),
            summary_notes: "Saffire-I validated that large-scale cloth samples burn faster in microgravity under ventilation (0.85-1.85 mm/s) due to efficient oxidizer entrainment without buoyant heat plume loss.".to_string(),
        },
        Material {
            material_id: "MAT-03".to_string(),
            material_name: "Nomex HT90-40 Aramid".to_string(),
            material_name_vi: "Vải chống cháy Aramid Nomex HT90-40".to_string(),
            psi_id: "PSI-SAFFIRE-II-NOM-90".to_string(),
            mission: "NASA Saffire-II & BASS-II".to_string(),
            category: "Flight Suit / Cargo Container Liner".to_string(),
            category_vi: "Đồ bay / Lớp lót túi hàng hóa".to_string(),
            geometry: "High-Density Aramid Fabric".to_string(),
            geometry_vi: "Vải dệt sợi Aramid mật độ cao".to_string(),
            moc_1g: 28.0,
            moc_microg: 26.0,
            base_spread_rate_mm_s: 0.35,
            chemical_formula: "[C14H10N2O2]n".to_string(),
            heat_of_combustion_mj_kg: 29.0,
            cool_flame_susceptible: false,
            flame_morphology: "Self-Terminating Char Barrier, Pale Violet Chemiluminescence".to_string(),
            flame_morphology_vi: "Lớp than hóa tự ngắt lửa, phát quang hóa học ánh tím nhạt".to_string(),
            quenching_mode: "Rapid Self-Extinction at standard ISS atmosphere (21% O2)".to_string(),
            quenching_mode_vi: "Tự dập tắt tức thì trong khí quyển chuẩn ISS (21% O2)".to_string(),
            summary_notes: "Gold-standard aerospace flame-resistant fabric. Does not sustain combustion in standard ISS (21% O2), but becomes FLAMMABLE in enriched Artemis cabin atmospheres (34% O2, 56.5 kPa)!".to_string(),
        },
        Material {
            material_id: "MAT-04".to_string(),
            material_name: "Silicone Elastomer RTV".to_string(),
            material_name_vi: "Gioăng cao su Silicone RTV".to_string(),
            psi_id: "PSI-BASS-II-SIL-22".to_string(),
            mission: "NASA BASS-II (Burning & Suppression)".to_string(),
            category: "Gasket / Hatch Seal / Potting Compound".to_string(),
            category_vi: "Gioăng cửa Hatch / Vật liệu bịt kín".to_string(),
            geometry: "Extruded Gasket Strip".to_string(),
            geometry_vi: "Dải gioăng cao su đùn định hình".to_string(),
            moc_1g: 24.0,
            moc_microg: 21.5,
            base_spread_rate_mm_s: 0.48,
            chemical_formula: "[R2SiO]n (Polydimethylsiloxane)".to_string(),
            heat_of_combustion_mj_kg: 19.8,
            cool_flame_susceptible: true,
            flame_morphology: "White Silica Ash Filament with Low-Luminosity Blue Core".to_string(),
            flame_morphology_vi: "Sợi tro Silica trắng bao bọc lõi lửa xanh lam độ sáng thấp".to_string(),
            quenching_mode: "Silica crust barrier extinction or radiative quenching".to_string(),
            quenching_mode_vi: "Tự tắt do lớp vỏ xỉ Silica cản oxy hoặc mất nhiệt bức xạ".to_string(),
            summary_notes: "Forms a porous SiO2 ash crust during combustion. Under slow airflow (< 5 cm/s), can undergo prolonged low-temperature smolder emitting toxic CO and siloxane oligomers into cabin life support.".to_string(),
        },
        Material {
            material_id: "MAT-05".to_string(),
            material_name: "Ultem 1000 Polyetherimide (PEI)".to_string(),
            material_name_vi: "Tấm Polymer chịu nhiệt PEI Ultem 1000".to_string(),
            psi_id: "PSI-BASS-II-ULT-101".to_string(),
            mission: "NASA BASS-II & Spacecraft Hardware".to_string(),
            category: "Structural Bracket / Avionics Enclosure".to_string(),
            category_vi: "Hộp bảo vệ thiết bị / Cấu trúc chịu lực".to_string(),
            geometry: "Solid Machined Plate (3.0mm)".to_string(),
            geometry_vi: "Tấm nhựa đặc gia công cơ khí (3.0mm)".to_string(),
            moc_1g: 32.0,
            moc_microg: 29.0,
            base_spread_rate_mm_s: 0.22,
            chemical_formula: "[C37H24N2O6]n".to_string(),
            heat_of_combustion_mj_kg: 31.5,
            cool_flame_susceptible: false,
            flame_morphology: "Intumescent Foaming Char with Micro-Jets of Pyrolysis Gas".to_string(),
            flame_morphology_vi: "Lớp than phồng rộp cách nhiệt kèm tia khí nhiệt phân vi mô".to_string(),
            quenching_mode: "Strong intumescent self-insulation and thermal quenching".to_string(),
            quenching_mode_vi: "Tự cách nhiệt bằng lớp than trương nở và dập tắt nhiệt học".to_string(),
            summary_notes: "High-performance thermoplastic certified under NASA-STD-6001B Test 1. Extinguishes immediately at 21% O2. Only exhibits persistent flame spread under extreme over-oxygenation (> 30% O2).".to_string(),
        },
        Material {
            material_id: "MAT-06".to_string(),
            material_name: "Teflon / PTFE Fluoropolymer".to_string(),
            material_name_vi: "Vỏ bọc cách điện Fluoropolymer Teflon / PTFE".to_string(),
            psi_id: "PSI-BASS-II-PTFE-07".to_string(),
            mission: "NASA BASS-II & Wiring Insulation Tests".to_string(),
            category: "High-Voltage Wire Harness / Valve Seat".to_string(),
            category_vi: "Bó dây cao áp / Đế van".to_string(),
            geometry: "Cylindrical Wire Insulation Jacket".to_string(),
            geometry_vi: "Lớp vỏ bọc cách điện dây cáp hình trụ".to_string(),
            moc_1g: 43.0,
            moc_microg: 40.5,
            base_spread_rate_mm_s: 0.05,
            chemical_formula: "[CF2-CF2]n".to_string(),
            heat_of_combustion_mj_kg: 5.1,
            cool_flame_susceptible: false,
            flame_morphology: "Transparent Whispering Glow, Toxic Fluorocarbon Vapor".to_string(),
            flame_morphology_vi: "Quầng sáng trong suốt mờ nhạt, giải phóng hơi Fluorocarbon độc".to_string(),
            quenching_mode: "Endothermic depolymerization causes immediate flame collapse".to_string(),
            quenching_mode_vi: "Phản ứng giải trùng hợp thu nhiệt làm ngọn lửa sụp đổ tức thì".to_string(),
            summary_notes: "Exceptionally safe against direct open flames due to MOC > 40%. However, upon forced external overheating (> 500°C), emits highly lethal HF and carbonyl fluoride vapors without visible flame.".to_string(),
        },
        Material {
            material_id: "MAT-07".to_string(),
            material_name: "Sibal Cotton Fabric".to_string(),
            material_name_vi: "Vải chuẩn Cotton Sibal (0.15mm)".to_string(),
            psi_id: "PSI-BASS-II-SIB-310".to_string(),
            mission: "NASA BASS-II (Standard Calibration Fuel)".to_string(),
            category: "Thin Solid Standard / Crew Clothing".to_string(),
            category_vi: "Nhiên liệu mỏng chuẩn hóa / Trang phục".to_string(),
            geometry: "Thermally Thin Sheet (0.15mm)".to_string(),
            geometry_vi: "Tấm nhiên liệu mỏng nhiệt học (0.15mm)".to_string(),
            moc_1g: 15.0,
            moc_microg: 13.0,
            base_spread_rate_mm_s: 1.75,
            chemical_formula: "C6H10O5".to_string(),
            heat_of_combustion_mj_kg: 16.8,
            cool_flame_susceptible: false,
            flame_morphology: "Rapid Propagating Parabolic Flame Sheet".to_string(),
            flame_morphology_vi: "Màng lửa hình parabol lan truyền tốc độ cao".to_string(),
            quenching_mode: "Convective blowoff at V > 38 cm/s".to_string(),
            quenching_mode_vi: "Thổi tắt đối lưu động học khi vận tốc gió V > 38 cm/s".to_string(),
            summary_notes: "Standardized thin solid fuel for microgravity research. Demonstrates extreme vulnerability: flame spread rate triples under cabin ventilation airflow compared to stagnant terrestrial air.".to_string(),
        },
        Material {
            material_id: "MAT-08".to_string(),
            material_name: "Heptane Droplet / Alkane Fuel".to_string(),
            material_name_vi: "Giọt nhiên liệu n-Heptane lơ lửng (2-4mm)".to_string(),
            psi_id: "PSI-FLEX-ICE-102".to_string(),
            mission: "NASA FLEX-2 & BASS-II (Droplet Rig)".to_string(),
            category: "Liquid Hydrocarbon / Propellant Simulant".to_string(),
            category_vi: "Chất lỏng hydrocacbon / Giả lập nhiên liệu đẩy".to_string(),
            geometry: "Free-floating Spherical Droplet (2-4mm)".to_string(),
            geometry_vi: "Giọt chất lỏng hình cầu lơ lửng tự do (2-4mm)".to_string(),
            moc_1g: 14.5,
            moc_microg: 13.8,
            base_spread_rate_mm_s: 2.10,
            chemical_formula: "C7H16".to_string(),
            heat_of_combustion_mj_kg: 44.6,
            cool_flame_susceptible: true,
            flame_morphology: "Spherically Symmetric Dual-Regime (Hot Blue Flame to Cool Invisible Flame)".to_string(),
            flame_morphology_vi: "Cầu đối xứng hai chế độ (Lửa nóng xanh lam sang Lửa lạnh vô hình)".to_string(),
            quenching_mode: "Transitions from hot flame extinction to second-stage cool flame".to_string(),
            quenching_mode_vi: "Chuyển tiếp từ tắt lửa nóng sang cháy âm ỉ Ngọn lửa lạnh giai đoạn 2".to_string(),
            summary_notes: "Historic NASA FLEX discovery: After hot flame extinguishes (radiation quenching), combustion continues invisibly at 600-800 K (cool flame) consuming all fuel droplet mass and generating high CO!".to_string(),
        },
        Material {
            material_id: "MAT-09".to_string(),
            material_name: "Polycarbonate Lexan".to_string(),
            material_name_vi: "Tấm nhựa Polycarbonate Lexan (4mm)".to_string(),
            psi_id: "PSI-BASS-II-LEX-55".to_string(),
            mission: "NASA BASS-II & Habitation Materials".to_string(),
            category: "Cupola Viewport / Blast Shield / Visor".to_string(),
            category_vi: "Cửa sổ vòm Cupola / Mặt nạ mũ du hành".to_string(),
            geometry: "Transparent Sheet (4.0mm)".to_string(),
            geometry_vi: "Tấm kính nhựa trong suốt (4.0mm)".to_string(),
            moc_1g: 26.0,
            moc_microg: 23.5,
            base_spread_rate_mm_s: 0.40,
            chemical_formula: "[C16H14O3]n".to_string(),
            heat_of_combustion_mj_kg: 30.8,
            cool_flame_susceptible: false,
            flame_morphology: "Dripping Viscous Melt with Dense Black Soot Aerosols".to_string(),
            flame_morphology_vi: "Nhựa nóng chảy nhỏ giọt kèm cột khói bồ hóng đen đặc".to_string(),
            quenching_mode: "Sustained in microgravity with 8-15 cm/s ventilation".to_string(),
            quenching_mode_vi: "Duy trì cháy trong vi trọng lực dưới luồng thông gió 8-15 cm/s".to_string(),
            summary_notes: "Produces intense smoke and dripping burning droplets in partial gravity (Lunar/Mars). In 0g, soot aggregates into long filamentary tendrils that clog spacecraft HEPA filtration banks.".to_string(),
        },
        Material {
            material_id: "MAT-10".to_string(),
            material_name: "Kapton HN Polyimide".to_string(),
            material_name_vi: "Màng cách nhiệt nhiều lớp Kapton HN Polyimide".to_string(),
            psi_id: "PSI-BASS-II-KAP-99".to_string(),
            mission: "NASA BASS-II & Spacecraft Thermal MLI".to_string(),
            category: "Multi-Layer Thermal Blanket / Solar Array Substrate".to_string(),
            category_vi: "Tấm cách nhiệt MLI / Đế pin mặt trời".to_string(),
            geometry: "Thin Metalized Film (0.05mm)".to_string(),
            geometry_vi: "Màng mỏng mạ kim loại cách nhiệt (0.05mm)".to_string(),
            moc_1g: 38.0,
            moc_microg: 36.0,
            base_spread_rate_mm_s: 0.12,
            chemical_formula: "[C22H10N2O5]n".to_string(),
            heat_of_combustion_mj_kg: 21.0,
            cool_flame_susceptible: false,
            flame_morphology: "Localized Smoldering Ring, Negligible Open Flame".to_string(),
            flame_morphology_vi: "Vòng âm ỉ cục bộ, hầu như không phát sinh ngọn lửa hở".to_string(),
            quenching_mode: "Self-extinguishes across all standard cabin environments".to_string(),
            quenching_mode_vi: "Tự dập tắt hoàn toàn trong mọi môi trường khoang tiêu chuẩn".to_string(),
            summary_notes: "NASA mission-critical thermal control insulation. Immune to ignition in ISS air. Can sustain localized smolder only if combined with high radiant flux and oxygen concentrations exceeding 36%.".to_string(),
        },
    ]
}

pub fn parse_csv_file(path: &Path) -> Option<Vec<HashMap<String, String>>> {
    if !path.exists() {
        return None;
    }
    let file = File::open(path).ok()?;
    let mut rdr = csv::ReaderBuilder::new().trim(csv::Trim::All).from_reader(file);
    let headers = rdr.headers().ok()?.clone();
    let col_names: Vec<String> = headers.iter().map(|s| s.trim().to_string()).collect();

    let mut records = Vec::new();
    for result in rdr.records() {
        if let Ok(rec) = result {
            let mut row = HashMap::new();
            for (i, field) in rec.iter().enumerate() {
                if i < col_names.len() {
                    row.insert(col_names[i].clone(), field.trim().to_string());
                }
            }
            records.push(row);
        }
    }
    Some(records)
}

fn resolve_data_dir(custom_dir: Option<&str>) -> PathBuf {
    if let Some(d) = custom_dir {
        return PathBuf::from(d);
    }
    if let Some(env_dir) = std::env::var_os("NASA_DATA_DIR") {
        let p = PathBuf::from(env_dir);
        if p.exists() {
            return p;
        }
    }
    let rel_data = PathBuf::from("data");
    if rel_data.exists() {
        return rel_data;
    }
    if let Ok(cwd) = std::env::current_dir() {
        for ancestor in cwd.ancestors() {
            let candidate = ancestor.join("data");
            if candidate.join("sofie_pmma_burn_rates.csv").exists() {
                return candidate;
            }
        }
    }
    if let Ok(exe_path) = std::env::current_exe() {
        for ancestor in exe_path.ancestors() {
            let candidate = ancestor.join("data");
            if candidate.join("sofie_pmma_burn_rates.csv").exists() {
                return candidate;
            }
        }
    }
    rel_data
}

pub fn load_nasa_psi_data_core(
    custom_dir: Option<&str>,
) -> (
    Vec<Material>,
    Option<Vec<HashMap<String, String>>>,
    Option<Vec<HashMap<String, String>>>,
    Option<Vec<HashMap<String, String>>>,
    String,
) {
    let embedded = get_embedded_materials();

    let data_dir = resolve_data_dir(custom_dir);

    let sofie_path = data_dir.join("sofie_pmma_burn_rates.csv");
    let saffire_path = data_dir.join("saffire_pressure_oxygen.csv");
    let bass_path = data_dir.join("bass_extinction_limits.csv");

    let sofie = parse_csv_file(&sofie_path);
    let saffire = parse_csv_file(&saffire_path);
    let bass = parse_csv_file(&bass_path);

    let status = if sofie.is_some() && saffire.is_some() && bass.is_some() {
        "disk".to_string()
    } else {
        "cache".to_string()
    };

    (embedded, sofie, saffire, bass, status)
}
