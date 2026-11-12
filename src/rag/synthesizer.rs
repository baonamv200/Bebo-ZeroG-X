//! Deterministic NASA Directive 3-Block Answer Generator & Fallback Synthesizer
//! Matching app.py:1992-2091 & 4725-4945.

use serde::{Deserialize, Serialize};
use crate::i18n::Language;
use super::tfidf::normalize_vn_text;
use super::SearchResult;

/// NASA Operational Directive Answer containing Docket, Classification, 3 distinct blocks, and raw text.
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct DirectiveAnswer {
    pub directive_code: String,
    pub classification: String,
    pub kinetics_block: String,
    pub standards_block: String,
    pub emergency_block: String,
    pub raw_answer: String,
}

pub fn synthesize_directive_answer(
    query_text: &str,
    ranked_results: &[SearchResult],
    lang: Language,
) -> DirectiveAnswer {
    if ranked_results.is_empty() {
        let msg = match lang {
            Language::Vi => "Không tìm thấy tài liệu kỹ thuật NASA PSI nào phù hợp.",
            Language::En => "No matching NASA PSI documents found for this query.",
        };
        return DirectiveAnswer {
            directive_code: "NASA-DIR-STANDBY".to_string(),
            classification: "OPERATIONAL SAFETY DIRECTIVE • PRIORITY 1".to_string(),
            kinetics_block: msg.to_string(),
            standards_block: String::new(),
            emergency_block: String::new(),
            raw_answer: msg.to_string(),
        };
    }

    let top_doc = &ranked_results[0].document;
    let doc_rep_id = top_doc.report_id;
    let directive_code = format!("NASA-DIR-{}", doc_rep_id.replace('/', "-"));
    let classification = "OPERATIONAL SAFETY DIRECTIVE • PRIORITY 1".to_string();

    let q_norm = normalize_vn_text(query_text);
    let q_low = query_text.to_lowercase();

    // Check Topic 1: Water suppression ban
    let is_water = ["nuoc", "suong nuoc", "tia nuoc", "chua chay", "dap lua", "dap hoa hoan", "binh chua chay", "water", "extinguish", "suppress", "foam", "mist", "spray"]
        .iter().any(|k| q_norm.contains(k) || q_low.contains(k));

    // Check Topic 2: Cool flames
    let is_cool_flame = ["lanh", "ngon lua lanh", "lua lanh", "cool flame", "cool flames", "flex", "giot", "droplet", "second-stage"]
        .iter().any(|k| q_norm.contains(k) || q_low.contains(k));

    // Check Topic 3: Moon / Mars
    let is_moon_mars = ["mat trang", "moon", "lunar", "0.16", "sao hoa", "mars", "0.38", "ban phan", "mot phan", "vom ban cau", "partial", "dome"]
        .iter().any(|k| q_norm.contains(k) || q_low.contains(k));

    // Check Topic 4: PMMA Paradox
    let is_pmma = ["pmma", "acrylic", "gio thap", "thong gio thap", "luong gio thap", "nghich ly", "paradox", "low-velocity", "low-flow", "ventilation paradox", "forced flow"]
        .iter().any(|k| q_norm.contains(k) || q_low.contains(k))
        || ((q_norm.contains("toc do chay") || q_norm.contains("chay")) && ["gio", "thong gio", "pmma", "tang toc", "cuc dai"].iter().any(|w| q_norm.contains(w)))
        || (q_low.contains("burn") && q_low.contains("flow"));

    let (kinetics_block, standards_block, emergency_block, raw_answer) = if is_water {
        match lang {
            Language::Vi => {
                let kin = "Trong vi trọng lực, tia nước áp lực cao đơn lẻ ($F = \\dot{m}v$) tạo lực xung kích thủy động cực lớn làm vỡ vụn các mảng polyme nóng chảy đang cháy. Lực này bắn tung hàng nghìn giọt nhựa cháy và tàn lửa lơ lửng khắp thể tích cabin 3D, biến đám cháy cục bộ thành thảm họa phân tán và gây chập mạch thảm khốc hệ thống điện tử hàng không (Avionics).".to_string();
                let std = "Theo Công bố Kỹ thuật NASA <b>NASA/SP-2024-50021</b> và tiêu chuẩn <b>NASA-STD-6001B</b>, nghiêm cấm tuyệt đối bình cứu hỏa phun tia nước thẳng trên toàn bộ phương tiện bay có người lái. Bắt buộc trang bị <b>Bình Chữa Cháy Sương Nước Siêu Mịn (Fine Water Mist, kích thước giọt &lt; 50 µm)</b> đẩy bằng khí trơ N₂, hoặc hệ thống xả tràn khí CO₂/N₂ toàn phần (Total Flooding) cho các khoang kín.".to_string();
                let emg = "1. <b>BẢO VỆ PHI HÀNH ĐOÀN (T+0s):</b> Lập tức đeo Thiết bị Dưỡng khí Khẩn cấp (PBE/SCBA) trong vòng 15 giây để chống khói độc.<br>2. <b>CÔ LẬP KHẨN CẤP (T+30s):</b> Đóng kín vách ngăn khoang (Hatch Seal) và cắt quạt thông gió HVAC phân khu để triệt tiêu dòng cấp khí.<br>3. <b>TRIỂN KHAI PHUN SƯƠNG (T+60s):</b> Kích hoạt bình sương nước siêu mịn ở cự ly 1.0 - 1.5m với góc xòe rộng, sau đó kích hoạt chế độ lọc bồ hóng ECLSS Scrubber.".to_string();
                let raw = format!(
                    "**Bản Khuyến cáo Kỹ thuật An toàn Bay [Căn cứ Báo cáo {} - Trang {}]:**\n\nTheo Công bố Kỹ thuật NASA NASA/SP-2024-50021, **các tia nước đơn lẻ áp lực cao bị NGHIÊM CẤM TUYỆT ĐỐI** bên trong khoang phi thuyền. Trong vi trọng lực, lực xung kích thủy động học sẽ làm vỡ vụn các mảng polyme nóng chảy đang cháy, bắn tung các giọt nhựa cháy và tàn lửa vào thể tích không khí, đồng thời gây nguy cơ chập cháy thảm khốc toàn bộ hệ thống điện tử hàng không.\n\nPhương pháp được chứng nhận bay là **Sương nước siêu mịn (hạt < 50 µm)** đẩy bằng khí trơ N2, giúp thu nhiệt hóa hơi tức thì mà không tạo động lượng dịch chuyển. Đối với các khoang thiết bị kín, bắt buộc xả tràn khí CO2 hoặc N2, đồng thời phi hành đoàn phải lập tức đeo Thiết bị Dưỡng khí Khẩn cấp (PBE).\n\n*Trích dẫn chính: {}, '{}', {}, tr. {}.*",
                    top_doc.report_id, top_doc.page, top_doc.authors, top_doc.title, top_doc.report_id, top_doc.page
                );
                (kin, std, emg, raw)
            }
            Language::En => {
                let kin = "In zero gravity, single high-velocity water jets generate massive hydrodynamic impact forces ($F = \\dot{m}v$) that shatter burning molten polymer matrices, scattering flaming droplets and incandescent embers throughout the 3D cabin volume while inducing catastrophic avionics short-circuits.".to_string();
                let std = "Per NASA Technical Publication <b>NASA/SP-2024-50021</b> and <b>NASA-STD-6001B</b>, single water jets are strictly prohibited on all crewed spacecraft. Flight certification mandates <b>Fine Water Mist (&lt; 50 µm droplets)</b> propelled by gaseous N₂, or total flooding with gaseous CO₂/N₂ for sealed equipment racks.".to_string();
                let emg = "1. <b>CREW PROTECTION (T+0s):</b> Immediately don Emergency Personal Breathing Equipment (PBE/SCBA) within 15 seconds.<br>2. <b>CABIN ISOLATION (T+30s):</b> Seal inter-module hatches and shut down localized HVAC fans to eliminate forced draft.<br>3. <b>MIST DISCHARGE (T+60s):</b> Deploy fine water mist extinguisher at 1.0-1.5m stand-off with wide cone dispersion, then activate ECLSS smoke scrubber.".to_string();
                let raw = format!(
                    "**Executive Safety Advisory [Grounded in {} - Page {}]:**\n\nAccording to NASA Technical Publication NASA/SP-2024-50021, **high-velocity single water jets are STRICTLY PROHIBITED** inside spacecraft cabins. In zero gravity, hydrodynamic impact forces shatter burning plastics, scattering flaming molten droplets and incandescent embers into the air volume while risking catastrophic avionics short-circuits.\n\nThe flight-certified method is **Fine Water Mist (< 50 µm droplets)** propelled by gaseous N2, which extracts latent heat instantly without momentum displacement. For sealed equipment bays, total flooding with gaseous CO2 or N2 is mandated, requiring crew to immediately don Emergency Personal Breathing Equipment (PBE).\n\n*Primary Citation: {}, '{}', {}, p. {}.*",
                    top_doc.report_id, top_doc.page, top_doc.authors, top_doc.title, top_doc.report_id, top_doc.page
                );
                (kin, std, emg, raw)
            }
        }
    } else if is_cool_flame {
        match lang {
            Language::Vi => {
                let kin = "Hiện tượng 'Ngọn Lửa Lạnh' (Cool Flames) được phát hiện trong thí nghiệm lịch sử NASA FLEX trên trạm ISS. Khi tổn thất nhiệt bức xạ dập tắt ngọn lửa nóng nhìn thấy (~1800 K), phản ứng đốt cháy oxy hóa giai đoạn hai vẫn tiếp diễn âm ỉ ở nhiệt độ thấp 600 - 800 K nhờ chuỗi phản ứng gốc tự do peroxy ($RO_2^\\bullet$). Ngọn lửa này hoàn toàn vô hình trước mắt thường và camera quang học.".to_string();
                let std = "Theo tiêu chuẩn <b>NASA-STD-6001B</b>, hệ thống an toàn không được phụ thuộc đơn thuần vào cảm biến khói quang học hoặc cảm biến ngọn lửa UV/IR dải thường. Bắt buộc tích hợp <b>Camera hồng ngoại nhiệt bước sóng dài (LWIR Thermal Imager)</b> và <b>Cảm biến điện hóa đo khí Carbon Monoxide (CO ppm sensor)</b> với ngưỡng cảnh báo sớm &lt; 10 ppm.".to_string();
                let emg = "1. <b>CẤM MỞ NẮP KHOANG:</b> Nghiêm cấm mở buồng đốt hoặc tháo dỡ thiết bị khi nhiệt độ vỏ chưa giảm dưới 50°C ngay cả khi không còn thấy lửa.<br>2. <b>BƠM KHÍ TRƠ TRIỆT TIÊU:</b> Xả khí Nitrogen hoặc Argon vào buồng để giảm nồng độ oxy xuống dưới 5% nhằm bẻ gãy chuỗi phản ứng lạnh.<br>3. <b>THEO DÕI NỒNG ĐỘ CO:</b> Giám sát liên tục chỉ số CO qua telemetry ECLSS cho đến khi nồng độ trở về mức danh định an toàn (&lt; 5 ppm).".to_string();
                let raw = format!(
                    "**Bản Khuyến cáo Kỹ thuật An toàn Bay [Căn cứ Báo cáo {} - Trang {}]:**\n\nĐược ghi nhận trong các thí nghiệm lịch sử NASA FLEX (tạp chí Science Vol. 338), 'Ngọn Lửa Lạnh' (Cool Flames) là chế độ đốt cháy giai đoạn hai vô cùng nguy hiểm trong vi trọng lực. Khi tổn thất bức xạ dập tắt ngọn lửa nóng nhìn thấy (~1800 K), phản ứng đốt cháy vẫn tiếp diễn vô hình ở 600 - 800 K. Phản ứng hóa học nhiệt độ thấp này không phát ra ánh sáng nhìn thấy và vô hiệu hóa cảm biến khói quang học, nhưng vẫn tiêu thụ khối lượng nhiên liệu nhanh chóng và sinh ra lượng khí độc Carbon Monoxide (CO) chết người.\n\n*Trích dẫn chính: {}, '{}', {}, tr. {}.*",
                    top_doc.report_id, top_doc.page, top_doc.authors, top_doc.title, top_doc.report_id, top_doc.page
                );
                (kin, std, emg, raw)
            }
            Language::En => {
                let kin = "Discovered in NASA FLEX experiments aboard the ISS, 'Cool Flames' represent a hazardous second-stage combustion regime in microgravity. When radiative heat loss quenches the visible hot flame (~1800 K), low-temperature chemical oxidation sustains invisibly at 600 - 800 K via peroxy radical pathways ($RO_2^\\bullet$), emitting zero visible light while generating deadly Carbon Monoxide (CO).".to_string();
                let std = "Under <b>NASA-STD-6001B</b>, flight safety cannot rely solely on optical smoke detectors or standard UV/IR sensors. Integration of <b>Long-Wave Infrared (LWIR) thermal imagers</b> and <b>electrochemical trace Carbon Monoxide (CO) sensors</b> with detection thresholds &lt; 10 ppm is mandatory for flight payloads.".to_string();
                let emg = "1. <b>CONTAINMENT LOCKDOWN:</b> Strictly prohibit opening experimental chamber until surface temperature falls below 50°C.<br>2. <b>INERT GAS PURGE:</b> Flood with gaseous N₂ or Argon to depress O₂ below 5%, extinguishing radical chain reactions.<br>3. <b>CO TELEMETRY MONITORING:</b> Continuously monitor ECLSS trace gas telemetry until CO levels stabilize below 5 ppm.".to_string();
                let raw = format!(
                    "**Executive Safety Advisory [Grounded in {} - Page {}]:**\n\nAs documented in the historic NASA FLEX experiments (Science Vol. 338), 'Cool Flames' represent a dangerous second-stage combustion regime in microgravity. When radiative heat loss extinguishes the visible hot flame (~1800 K), combustion continues invisibly at 600 - 800 K. This low-temperature chemical reaction gives off zero visible crew light and bypasses optical smoke detectors, yet rapidly depletes fuel mass and generates deadly levels of toxic Carbon Monoxide (CO).\n\n*Primary Citation: {}, '{}', {}, p. {}.*",
                    top_doc.report_id, top_doc.page, top_doc.authors, top_doc.title, top_doc.report_id, top_doc.page
                );
                (kin, std, emg, raw)
            }
        }
    } else if is_moon_mars {
        match lang {
            Language::Vi => {
                let kin = "Công bố trên Combustion Institute Paper CI-2022-88 xác nhận trọng lực bán phần (0.16g Mặt Trăng, 0.38g Sao Hỏa) tạo ra nghịch lý nguy hiểm nhất: Lực nổi quá yếu để kéo khí nóng lên thành cột thẳng đứng hẹp, nhưng vừa đủ để cuốn khí oxy mới vào chân ngọn lửa. Hậu quả là ngọn lửa bành trướng thành <b>vòm bán cầu mở rộng (Hemispherical Dome)</b>, làm diện tích tiếp xúc với các vách ngăn xung quanh tăng vọt <b>240%</b>!".to_string();
                let std = "Quy chuẩn thiết kế căn cứ bề mặt <b>NASA-STD-6001B</b> quy định khoảng cách an toàn cách ly nhiệt giữa các giá thiết bị trên Mặt Trăng/Sao Hỏa phải tăng tối thiểu <b>2.5 lần</b> so với trạm ISS. Bắt buộc lắp đặt <b>vách ngăn chống cháy chịu nhiệt &gt; 1200°C</b> và sơn phủ phồng nở (intumescent barrier) ngăn bắt lửa lan đáy.".to_string();
                let emg = "1. <b>THOÁT HIỂM TẦNG CAO:</b> Khói trên Mặt Trăng lơ lửng sát sàn nhà và ngang tầm ngực; phi hành đoàn phải di chuyển ở tư thế đứng theo dây thoát hiểm.<br>2. <b>XẢ ÁP SUẤT KHOANG SỐNG:</b> Hạ áp suất môi trường sống (Depressurization) nếu được phép để giảm mật độ oxy tuyệt đối ($P_{O2} &lt; 10\\text{ kPa}$).<br>3. <b>HÚT KHÓI TẦNG SÀN:</b> Khởi động quạt hút lọc khói tầng sàn của trạm căn cứ để thu gom bụi bồ hóng tích tụ.".to_string();
                let raw = format!(
                    "**Bản Khuyến cáo Kỹ thuật An toàn Bay [Căn cứ Báo cáo {} - Trang {}]:**\n\nNghiên cứu công bố trên Combustion Institute Paper CI-2022-88 chỉ ra rằng môi trường trọng lực một phần (0.16g Mặt Trăng, 0.38g Sao Hỏa) nguy hiểm hơn cả 0g lẫn 1g. Lực nổi không đủ mạnh để kéo khí cháy nóng lên thành cột thẳng đứng, khiến ngọn lửa bành trướng ngang thành một **vòm bán cầu mở rộng**. Hình thái này làm tăng diện tích tiếp xúc trực tiếp với các vách và cấu trúc lân cận lên đến 240%, tạo ra dấu chân bắt cháy lan rộng khó kiểm soát.\n\n*Trích dẫn chính: {}, '{}', {}, tr. {}.*",
                    top_doc.report_id, top_doc.page, top_doc.authors, top_doc.title, top_doc.report_id, top_doc.page
                );
                (kin, std, emg, raw)
            }
            Language::En => {
                let kin = "Combustion Institute Paper CI-2022-88 proves partial gravity (0.16g Moon, 0.38g Mars) is paradoxically more hazardous than 0g or 1g. Buoyancy is too weak to loft hot gases into a narrow vertical plume, yet strong enough to continuously supply oxygen to the base. The flame flares into an <b>expanding hemispherical dome</b>, expanding surface contact footprint by <b>240%</b>.".to_string();
                let std = "Surface habitat architecture under <b>NASA-STD-6001B</b> requires safety clearance between equipment racks to increase by <b>2.5×</b> compared to ISS standards. <b>Fire barrier bulkheads rated &gt; 1200°C</b> and intumescent thermal barrier coatings are mandatory.".to_string();
                let emg = "1. <b>UPRIGHT EVACUATION:</b> Smoke hovers near floor and chest levels; crew must navigate upright using tactile guideline tethers.<br>2. <b>HABITAT DEPRESSURIZATION:</b> Execute emergency cabin depressurization if authorized to suppress absolute oxygen partial pressure ($P_{O2} &lt; 10\\text{ kPa}$).<br>3. <b>LOW-LEVEL SMOKE SCRUBBING:</b> Activate floor-level intake scrubbers to capture settling soot particles.".to_string();
                let raw = format!(
                    "**Executive Safety Advisory [Grounded in {} - Page {}]:**\n\nResearch published in Combustion Institute Paper CI-2022-88 establishes that partial gravity environments (0.16g Moon, 0.38g Mars) are paradoxically more dangerous than either 0g or 1g. Buoyancy is insufficient to loft hot combustion gases into a narrow vertical plume, causing the flame to flare laterally into an **expanded hemispherical dome**. This geometry increases direct contact with adjacent walls and bulkheads by up to 240%, creating an extended ignition footprint.\n\n*Primary Citation: {}, '{}', {}, p. {}.*",
                    top_doc.report_id, top_doc.page, top_doc.authors, top_doc.title, top_doc.report_id, top_doc.page
                );
                (kin, std, emg, raw)
            }
        }
    } else if is_pmma {
        match lang {
            Language::Vi => {
                let kin = "Dữ liệu thực nghiệm bay NASA SoFIE (Solid Fuel Ignition and Extinction) từ Giá tích hợp Đốt cháy CIR trên ISS chỉ ra rằng: Trong vi trọng lực tĩnh (< 2 cm/s), PMMA tự dập tắt do tổn thất nhiệt bức xạ. Tuy nhiên dưới luồng thông gió khoang từ <b>5 đến 12 cm/s</b>, tốc độ cháy đạt đỉnh cực đại cục bộ (<b>0.51 - 0.78 mm/s</b>), thậm chí <b>nhanh hơn đốt cháy hướng xuống trên Trái Đất</b> do dòng gió liên tục bù oxy tươi mà không gây thổi nguội đối lưu (chế độ số Peclet tối ưu).".to_string();
                let std = "Theo tiêu chuẩn <b>NASA-STD-6001B Test 1</b>, PMMA không đạt chứng chỉ bay cho các vị trí có lưu thông khí > 5 cm/s. Khuyến nghị thay thế bắt buộc: Chuyển sang dùng <b>Polyimide (Kapton HN)</b>, <b>Fluoropolymer (PTFE/Teflon)</b>, hoặc tinh thể <b>Sapphire</b> nhân tạo cho các cửa sổ quan sát quang học.".to_string();
                let emg = "1. <b>CẮT GIÓ HVAC TỨC THÌ (T+0s):</b> Tắt quạt thông gió khoang phân khu để hạ vận tốc gió về &lt; 2 cm/s, đẩy ngọn lửa vào vùng tự dập tắt bức xạ.<br>2. <b>ĐEO MẶT NẠ DƯỠNG KHÍ (T+15s):</b> Phi hành đoàn lập tức đeo mặt nạ PBE tránh hít phải khí độc methyl methacrylate phân hủy nhiệt.<br>3. <b>PHUN SƯƠNG NƯỚC LÀM NGUỘI:</b> Sử dụng bình sương nước siêu mịn để hấp thụ nhiệt ẩn bề mặt polyme mà không tạo động lượng vỡ vụn.".to_string();
                let raw = format!(
                    "**Bản Khuyến cáo Kỹ thuật An toàn Bay [Căn cứ Báo cáo {} - Trang {}]:**\n\nDựa trên dữ liệu thực nghiệm bay NASA SoFIE (Solid Fuel Ignition and Extinction) từ Giá tích hợp Đốt cháy CIR trên trạm ISS, PMMA không tuân theo các quy luật đốt cháy mặt đất. Trong vi trọng lực tĩnh (< 2 cm/s), ngọn lửa tự dập tắt do tổn thất nhiệt bức xạ vượt quá nhiệt lượng sinh ra từ phản ứng hóa học. Tuy nhiên, dưới luồng thông gió khoang từ **5 đến 12 cm/s**, tốc độ cháy đạt đỉnh cực đại cục bộ (**0.51 - 0.78 mm/s**), thậm chí **nhanh hơn cả khi đốt cháy hướng xuống trên Trái Đất**! Điều này xảy ra do dòng thông gió liên tục bổ sung oxy tươi vào vùng phản ứng mà không gây làm nguội thổi tắt đối lưu.\n\n*Trích dẫn chính: {}, '{}', {}, Phần {}, tr. {}.*",
                    top_doc.report_id, top_doc.page, top_doc.authors, top_doc.title, top_doc.report_id, top_doc.section.split(':').next().unwrap_or("Section 4.3"), top_doc.page
                );
                (kin, std, emg, raw)
            }
            Language::En => {
                let kin = "NASA SoFIE flight data from the ISS Combustion Integrated Rack (CIR) proves PMMA exhibits a striking ventilation paradox: Spontaneously extinguishing in quiescent drift (< 2 cm/s) due to radiative loss, it accelerates to an alarming peak burning rate (<b>0.51 - 0.78 mm/s</b>) under <b>5 - 12 cm/s</b> airflow—exceeding downward burning on Earth as oxygen is replenished without blowoff cooling.".to_string();
                let std = "Under <b>NASA-STD-6001B Test 1</b>, PMMA fails flight clearance for compartments with forced ventilation > 5 cm/s. Mandatory substitution: Deploy <b>Polyimide (Kapton HN)</b>, <b>Fluoropolymer (PTFE)</b>, or optical-grade synthetic <b>Sapphire crystals</b>.".to_string();
                let emg = "1. <b>IMMEDIATE HVAC CUT-OFF (T+0s):</b> Cut ventilation fans below 2 cm/s to force the flame into radiative quenching regime.<br>2. <b>PBE DONNING (T+15s):</b> Don Emergency Personal Breathing Equipment against pyrolyzed methyl methacrylate toxic vapor.<br>3. <b>FINE MIST COOLING:</b> Apply fine water mist to extract sensible heat from polymer surface without mechanical shattering.".to_string();
                let raw = format!(
                    "**Executive Safety Advisory [Grounded in {} - Page {}]:**\n\nBased on the NASA SoFIE (Solid Fuel Ignition and Extinction) flight data from the ISS Combustion Integrated Rack (CIR), PMMA does not follow terrestrial burning patterns. In quiescent microgravity (< 2 cm/s), the flame extinguishes spontaneously due to radiative heat loss exceeding heat release. However, under cabin ventilation airflows of **5 to 12 cm/s**, the burning rate reaches an alarming local peak (**0.51 - 0.78 mm/s**), which is actually **faster than downward burning on Earth**! This occurs because forced airflow continuously replenishes oxygen to the reaction envelope without imparting convective blowoff cooling.\n\n*Primary Citation: {}, '{}', {}, Section {}, p. {}.*",
                    top_doc.report_id, top_doc.page, top_doc.authors, top_doc.title, top_doc.report_id, top_doc.section.split(':').next().unwrap_or("Section 4.3"), top_doc.page
                );
                (kin, std, emg, raw)
            }
        }
    } else {
        // Fallback: quotes top retrieved document with citation
        match lang {
            Language::Vi => {
                let kin = format!("Tổng hợp phân tích từ hồ sơ kỹ thuật chuyên sâu NASA PSI ({}): Trọng tâm nghiên cứu ({}). Trong môi trường trọng lực biến đổi và vi trọng lực, động học đốt cháy và ranh giới dập tắt của vật liệu tuân theo các quy luật phi tuyến tính. Báo cáo xác định các ranh giới tới hạn phụ thuộc vào áp suất khoang, nồng độ oxy và vận tốc thông gió cưỡng bức của hệ thống ECLSS.", top_doc.report_id, top_doc.title);
                let std = "Tuân thủ nghiêm ngặt tiêu chuẩn kiểm tra độ bắt cháy vật liệu theo NASA-STD-6001B và chỉ định phân loại rủi ro bay.".to_string();
                let emg = "1. Cô lập thông gió phân khu tức thời. 2. Phi hành đoàn trang bị dưỡng khí PBE. 3. Xả khí trơ hoặc phun sương nước siêu mịn.".to_string();
                let raw = format!(
                    "Tổng hợp phân tích từ hồ sơ kỹ thuật chuyên sâu NASA PSI ({}):\n\n**Trọng tâm nghiên cứu ({}):**\nTrong môi trường trọng lực biến đổi và vi trọng lực, động học đốt cháy và ranh giới dập tắt của vật liệu tuân theo các quy luật phi tuyến tính. Báo cáo kỹ thuật xác định các ranh giới tới hạn phụ thuộc vào áp suất khoang, nồng độ oxy và vận tốc thông gió cưỡng bức của hệ thống ECLSS.\n\n*Trích dẫn nguyên văn hồ sơ bay:* \"{}\"\n\n*Nguồn: {}, '{}', {}, {}, Trang {} ({}).*",
                    top_doc.report_id, top_doc.title, top_doc.text, top_doc.authors, top_doc.title, top_doc.report_id, top_doc.section, top_doc.page, top_doc.year
                );
                (kin, std, emg, raw)
            }
            Language::En => {
                let kin = format!("Synthesizing retrieved NASA PSI technical documentation ({}): {}", top_doc.report_id, top_doc.text);
                let std = "Strict adherence to NASA-STD-6001B material flammability certification standards and flight qualification.".to_string();
                let emg = "1. Immediate compartmental ventilation shutdown. 2. Crew dons PBE breathing gear. 3. Inert gas flooding or fine water mist suppression.".to_string();
                let raw = format!(
                    "Synthesizing retrieved NASA PSI technical documentation ({}):\n\n{}\n\n*Source: {}, '{}', {}, {}, Page {} ({}).*",
                    top_doc.report_id, top_doc.text, top_doc.authors, top_doc.title, top_doc.report_id, top_doc.section, top_doc.page, top_doc.year
                );
                (kin, std, emg, raw)
            }
        }
    };

    DirectiveAnswer {
        directive_code,
        classification,
        kinetics_block,
        standards_block,
        emergency_block,
        raw_answer,
    }
}
