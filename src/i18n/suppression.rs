//! Bilingual Emergency Suppression Database for 10 aerospace materials (MAT-01 to MAT-10)
//! Matching i18n.py:440-591.

use super::{Language, SuppressionProtocol};

pub fn get_suppression_protocol(material_id: &str, lang: Language) -> Option<SuppressionProtocol> {
    match (material_id, lang) {
        ("MAT-01", Language::En) => Some(SuppressionProtocol {
            name: "PMMA / Acrylic Rod (6.35mm)",
            action_1: "Immediately shut down sectional HVAC ventilation within 3 seconds to reduce airflow from 10 cm/s to < 2 cm/s, forcing the flame front into the Radiative Quenching Zone.",
            optimal_agent: "Fine Water Mist (droplet diameter < 50 µm) propelled by gaseous N2; STRICTLY FORBID high-velocity single water jets to prevent hydrodynamic momentum from scattering molten polymers and embers across microgravity.",
            secondary_hazard: "Generates high CO concentrations and vaporized Methyl Methacrylate monomer; mandatory crew donning of positive-pressure PBE/SCBA breathing masks for a minimum of 45 minutes.",
            decontamination: "Deploy portable Smoke Eater canisters and engage ECLSS activated carbon adsorption scrubbing loop for 12 hours.",
        }),
        ("MAT-01", Language::Vi) => Some(SuppressionProtocol {
            name: "PMMA / Acrylic Rod (6.35mm)",
            action_1: "Ngắt ngay lập tức quạt thông gió HVAC phân khu trong 3 giây đầu tiên để đưa vận tốc dòng khí từ 10 cm/s về < 2 cm/s, đẩy ngọn lửa vào Vùng Tự Dập Bức Xạ (Radiative Quenching).",
            optimal_agent: "Sương nước siêu mịn (Fine Water Mist, giọt < 50 µm) đẩy bằng khí trơ N2; TUYỆT ĐỐI KHÔNG dùng tia nước đơn lẻ áp lực cao vì lực xung kích sẽ bắn tung polyme nóng chảy và tàn lửa khắp khoang vi trọng lực.",
            secondary_hazard: "Sinh ra khí độc CO nồng độ cao và monomer Methyl Methacrylate bay hơi; bắt buộc phi hành gia đeo mặt nạ dưỡng khí PBE/SCBA áp dương tối thiểu 45 phút.",
            decontamination: "Kích hoạt cụm lọc khói cơ động (Smoke Eater Canister) và chu trình hấp phụ carbon than hoạt tính của hệ thống ECLSS trong 12 giờ.",
        }),
        ("MAT-02", Language::En) => Some(SuppressionProtocol {
            name: "Cotton-Fiberglass Blend (75/25)",
            action_1: "Seal cabin hatch barrier and shut isolation ventilation valves; smother burning fabric surface using Nomex fire-blanket.",
            optimal_agent: "Total Flooding CO2 or surface inert foam to extinguish deep-seated glowing smolder trapped inside the fiberglass matrix.",
            secondary_hazard: "Fractured fiberglass micro-particulates aerosolize into suspension, blinding ECLSS HEPA filters and posing severe crew pulmonary alveolar laceration hazards.",
            decontamination: "Perform emergency replacement of HEPA pre-filters; deploy specialized sealed HEPA vacuum to clean all cabin surfaces.",
        }),
        ("MAT-02", Language::Vi) => Some(SuppressionProtocol {
            name: "Cotton-Fiberglass Blend (75/25)",
            action_1: "Đóng sập cửa khoang khí quyển (Cabin Hatch Barrier) và ngắt van thông gió phân khu; che phủ bề mặt vải cháy bằng chăn chống cháy Nomex dập bùng.",
            optimal_agent: "Khí CO2 tràn ngập toàn khoang (Total Flooding CO2) hoặc bọt trơ dập bề mặt để triệt tiêu than hồng âm ỉ (smoldering glow) ngấm sâu trong lõi sợi thủy tinh.",
            secondary_hazard: "Sợi thủy tinh siêu mịn bị vỡ vụn phát tán dưới dạng hạt khí dung lơ lửng gây tắc nghẽn bộ lọc HEPA của hệ thống ECLSS và đâm rách phế nang phổi phi hành gia.",
            decontamination: "Thay thế khẩn cấp tiền màng lọc HEPA; sử dụng máy hút bụi chân không chuyên dụng HEPA quét sạch bề mặt cabin.",
        }),
        ("MAT-03", Language::En) => Some(SuppressionProtocol {
            name: "Nomex HT90-40 Aramid",
            action_1: "Immediately depressurize / dilute cabin oxygen below 25% if operating in enriched Artemis cabin atmosphere (34% O2); de-energize cargo bay electrical circuits.",
            optimal_agent: "Inert gaseous N2 or AFFF water-mist; free radical inhibitor Halotron/FE-36.",
            secondary_hazard: "Pyrolysis off-gasses lethal Hydrogen Cyanide (HCN) and Nitrogen Oxides (NOx); crew must not doff breathing masks until gas chromatography confirms safe levels.",
            decontamination: "Utilize acid-gas chemisorbent beds in the ECLSS Trace Contaminant Control Subsystem (TCCS) to scrub HCN.",
        }),
        ("MAT-03", Language::Vi) => Some(SuppressionProtocol {
            name: "Nomex HT90-40 Aramid",
            action_1: "Hạ tức thời nồng độ oxy khoang xuống < 25% nếu đang ở cấu hình Artemis Cabin (34% O2); ngắt nguồn điện qua buồng hàng.",
            optimal_agent: "Khí trơ N2 hoặc bình chữa cháy bọt bọc màng nước AFFF; chất ức chế gốc tự do Halotron/FE-36.",
            secondary_hazard: "Pyrolysis giải phóng khí Hydrogen Cyanide (HCN) và Nitrogen Oxides (NOx) cực độc; cấm tháo mặt nạ thở khi chưa kiểm tra nồng độ khí bằng sắc ký.",
            decontamination: "Sử dụng vật liệu hấp phụ acid gas trong hệ thống TCCS để trung hòa vết HCN.",
        }),
        ("MAT-04", Language::En) => Some(SuppressionProtocol {
            name: "Silicone Elastomer RTV",
            action_1: "Isolate electrical bus supplying heat to hatch frame; reduce cabin pressure differential to prevent seal blowout.",
            optimal_agent: "Low-pressure inert N2 flood or dry chemical agent; STRICTLY FORBID cold water spray to prevent thermal shock and structural hatch metal fracturing.",
            secondary_hazard: "Forms porous white silica (SiO2) ash crust trapping heat, releasing volatile siloxanes and lethal CO concentrations in a prolonged invisible smolder.",
            decontamination: "Scrape off silica ash once cooled; sanitize metal sealing surfaces using aerospace-grade isopropyl alcohol.",
        }),
        ("MAT-04", Language::Vi) => Some(SuppressionProtocol {
            name: "Silicone Elastomer RTV",
            action_1: "Cô lập thanh dẫn điện (electrical bus) cấp nhiệt cho khung cửa hatch; giảm chênh áp khoang để tránh rách gioăng làm thất thoát khí.",
            optimal_agent: "Khối khí N2 trơ áp suất thấp hoặc bình dập bụi hóa học khô NASA; NGHIÊM CẤM xịt nước lạnh gây sốc nhiệt nứt vỡ kim loại cấu trúc cửa hatch.",
            secondary_hazard: "Phân hủy tạo lớp tro xốp silica (SiO2) kèm khí siloxane bay hơi và CO nồng độ chết người âm ỉ kéo dài nhiều giờ (Cool Flame smolder).",
            decontamination: "Cạo bỏ lớp tro silica sau khi làm nguội; vệ sinh bề mặt kim loại bằng dung môi isopropyl alcohol hàng không vũ trụ.",
        }),
        ("MAT-05", Language::En) => Some(SuppressionProtocol {
            name: "Ultem 1000 Polyetherimide (PEI)",
            action_1: "Cut external radiant heat source; maintain slow ambient drift to facilitate intumescent self-insulating char formation.",
            optimal_agent: "Localized CO2 stream or Fine Water Mist; PEI exhibits rapid self-extinction once radiant flux is removed.",
            secondary_hazard: "Smoke plume contains trace sulfur dioxide (SO2) and phenol vapors; causes acute ocular and mucosal irritation.",
            decontamination: "Operate low-temperature ambient catalytic oxidizer scrubbers to decompose airborne phenol vapors.",
        }),
        ("MAT-05", Language::Vi) => Some(SuppressionProtocol {
            name: "Ultem 1000 Polyetherimide (PEI)",
            action_1: "Ngắt nguồn cung cấp nhiệt bức xạ bên ngoài; duy trì luồng khí trôi chậm để hỗ trợ lớp than phồng intumescent tự cách nhiệt.",
            optimal_agent: "Bình xịt khí CO2 cục bộ hoặc Fine Water Mist; PEI có khả năng tự dập tắt cao khi cắt nguồn nhiệt.",
            secondary_hazard: "Khí khói chứa vết sulfur dioxide (SO2) và phenol; kích ứng niêm mạc mắt phi hành gia nếu tiếp xúc trực tiếp.",
            decontamination: "Chạy quạt lọc xúc tác oxy hóa nhiệt độ thấp của trạm để phân hủy khí phenol.",
        }),
        ("MAT-06", Language::En) => Some(SuppressionProtocol {
            name: "Teflon / PTFE Fluoropolymer",
            action_1: "Emergency trip main electrical breaker of overheating wire harness within 1 second; isolate adjacent lithium battery chargers.",
            optimal_agent: "Rapid-cooling liquified inert gas (N2/CO2); NEVER use water which hydrolyzes into lethal fuming hydrofluoric acid.",
            secondary_hazard: "Releases ultra-lethal Carbonyl Fluoride (COF2), Hydrogen Fluoride (HF), and PFIB, inducing fatal pulmonary edema even at trace concentrations (< 1 ppm).",
            decontamination: "Flush cabin atmosphere through basic lime chemisorption filters; evacuate crew immediately to safe refuge module.",
        }),
        ("MAT-06", Language::Vi) => Some(SuppressionProtocol {
            name: "Teflon / PTFE Fluoropolymer",
            action_1: "Cắt khẩn cấp cầu dao điện chính của cụm bó dây (wire harness) bị quá nhiệt trong vòng 1 giây; ngắt nguồn sạc pin lithium liền kề.",
            optimal_agent: "Khí trơ hóa lỏng làm lạnh nhanh (N2/CO2); TUYỆT ĐỐI KHÔNG dùng nước tạo phản ứng thủy phân axit flohydric bốc khói.",
            secondary_hazard: "Phát tán khí kịch độc Carbonyl Fluoride (COF2), Hydrogen Fluoride (HF) và PFIB gây phù phổi cấp tử vong ngay cả ở nồng độ cực nhỏ (vài ppm).",
            decontamination: "Súc rửa khí quyển khoang bằng cụm hấp phụ đá vôi bazơ kiềm; phi hành gia chuyển sang khoang lánh nạn an toàn.",
        }),
        ("MAT-07", Language::En) => Some(SuppressionProtocol {
            name: "Sibal Cotton Fabric",
            action_1: "Cut section ventilation fans instantly; smother flame front using flame-retardant Kapton film.",
            optimal_agent: "Water Mist Extinguisher augmented with surfactant agent to immediately penetrate and wet cellulosic microfibers.",
            secondary_hazard: "Rapid dispersion of fibrous smoke blinds cabin optical smoke detectors and produces large clouds of airborne fly-ash.",
            decontamination: "Vacuum airborne fibrous ash with electrostatic particulate scrubbers and replace HEPA filter cartridges.",
        }),
        ("MAT-07", Language::Vi) => Some(SuppressionProtocol {
            name: "Sibal Cotton Fabric",
            action_1: "Dập tắt quạt gió phân khu tức thì; phủ kín vùng cháy bằng màng chịu nhiệt chống cháy Kapton.",
            optimal_agent: "Bình sương nước mịn Water Mist Extinguisher có bổ sung chất hoạt động bề mặt để thấm ướt tức thì các vi sợi cellulose.",
            secondary_hazard: "Khói xơ bông phân tán cực nhanh làm tê liệt cảm biến quang học khói toàn khoang (optical sensor blindness) và sinh lượng lớn tro bay.",
            decontamination: "Hút sạch tro xơ lơ lửng bằng máy lọc hạt tích điện tĩnh và thay cartridge lọc HEPA.",
        }),
        ("MAT-08", Language::En) => Some(SuppressionProtocol {
            name: "Heptane Droplet / Alkane Fuel",
            action_1: "Trigger liquid fuel Quick Disconnect emergency shutoff valve; open chamber vacuum vent valve to space.",
            optimal_agent: "Total volume N2 inerting combined with chamber thermal quenching; PROHIBIT water which induces steam explosions and liquid droplet splatter.",
            secondary_hazard: "Invisible Cool Flame regime active at 600-800K continues consuming fuel and generating massive toxic CO without visible light.",
            decontamination: "Monitor CO concentrations via multichannel electrochemical sensors; vent chamber to space vacuum before hatch opening.",
        }),
        ("MAT-08", Language::Vi) => Some(SuppressionProtocol {
            name: "Heptane Droplet / Alkane Fuel",
            action_1: "Ngắt van cấp nhiên liệu dòng lỏng (Quick Disconnect shutoff); kích hoạt van hút chân không cục bộ của buồng thí nghiệm.",
            optimal_agent: "Khí trơ N2 xả tràn thể tích kết hợp hạ nhiệt buồng đốt; CẤM DÙNG nước gây sôi nổ bắn tóe nhiên liệu lỏng ra môi trường xung quanh.",
            secondary_hazard: "Hiệu ứng Ngọn Lửa Lạnh (Cool Flame) vô hình ở 600-800K tiếp tục tiêu thụ nhiên liệu sinh lượng CO khổng lồ không phát ra ánh sáng cảnh báo.",
            decontamination: "Giám sát nồng độ CO bằng cảm biến điện hóa đa kênh; súc xả buồng đốt ra khoảng không vũ trụ trước khi mở cửa khoang.",
        }),
        ("MAT-09", Language::En) => Some(SuppressionProtocol {
            name: "Polycarbonate Lexan",
            action_1: "Shut ventilation directed toward viewports/cupola; evacuate crew from area of free-floating molten polymer droplets.",
            optimal_agent: "Low-velocity CO2 discharge or aerospace-grade AFFF water-film foam.",
            secondary_hazard: "Dense black soot tendrils aggregate into long chains in zero-g, blinding optical cameras and clogging carbon scrubbers.",
            decontamination: "Replace primary smoke filters; clean optical viewport lenses with antistatic lint-free aerospace wipes.",
        }),
        ("MAT-09", Language::Vi) => Some(SuppressionProtocol {
            name: "Polycarbonate Lexan",
            action_1: "Tắt quạt thông gió hướng vào cửa sổ / kính vòm; di tản phi hành gia khỏi vùng nhỏ giọt nhựa nóng chảy lơ lửng.",
            optimal_agent: "Khí CO2 xả chậm hoặc bọt dập màng nước AFFF chuyên dụng hàng không vũ trụ.",
            secondary_hazard: "Hạt mồ hóng đen dày đặc (dense soot tendrils) kết tụ thành chuỗi dài trong vi trọng lực làm mù camera quan sát và tắc nghẽn bộ hấp phụ carbon trạm.",
            decontamination: "Thay thế bộ lọc khói sơ cấp; lau chùi bề mặt thấu kính quang học bằng khăn chuyên dụng chống tĩnh điện.",
        }),
        ("MAT-10", Language::En) => Some(SuppressionProtocol {
            name: "Kapton HN Polyimide",
            action_1: "Isolate MLI thermal blanket from electrical arc tracking path; decouple solar array positive power bus.",
            optimal_agent: "Localized CO2 stream or gaseous N2; material self-extinguishes promptly once electrical arc is de-energized.",
            secondary_hazard: "Carbonization generates conductive char tracks causing secondary short circuits upon electrical re-energization.",
            decontamination: "Isolate damaged cable harness section; verify insulation resistance with a megohmmeter before restoring power.",
        }),
        ("MAT-10", Language::Vi) => Some(SuppressionProtocol {
            name: "Kapton HN Polyimide",
            action_1: "Tách tấm cách nhiệt MLI khỏi nguồn phóng điện hồ quang (arc tracking); ngắt tải điện cực dương pin mặt trời.",
            optimal_agent: "Khí CO2 cục bộ hoặc N2; vật liệu tự dập tắt ngay khi ngắt hồ quang điện.",
            secondary_hazard: "Carbon hóa tạo đường dẫn điện (conductive carbon char) có thể gây chập mạch thứ cấp nếu tái đóng điện.",
            decontamination: "Cách ly đoạn cáp bị cháy; đo điện trở cách điện bằng Megohmmeter trước khi tái cấp điện.",
        }),
        _ => None,
    }
}

pub const ALL_SUPPRESSION_MATERIAL_IDS: &[&str] = &[
    "MAT-01", "MAT-02", "MAT-03", "MAT-04", "MAT-05",
    "MAT-06", "MAT-07", "MAT-08", "MAT-09", "MAT-10",
];
