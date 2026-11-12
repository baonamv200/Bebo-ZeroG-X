//! Bilingual NASA Flight Research Records (7 NASA flight projects)
//! Matching i18n.py:594-672.

use super::{Language, ResearchRecord};

pub fn get_research_records(lang: Language) -> Vec<ResearchRecord> {
    match lang {
        Language::Vi => vec![
            ResearchRecord {
                experiment: "NASA SoFIE (Solid Fuel Ignition and Extinction)",
                psi_id: "PSI-SOFIE-GEL-412",
                pis: "Dr. David Urban (NASA GRC), Prof. Carlos Fernandez-Pello (UC Berkeley)",
                facility: "ISS Combustion Integrated Rack (CIR)",
                finding: "Xác định hiện tượng nghịch lý: dưới dòng khí thông gió thấp (5-12 cm/s), tốc độ lan truyền ngọn lửa PMMA đạt đỉnh cục bộ cao hơn cả khi đốt trên mặt đất do không bị tổn hao nhiệt đối lưu.",
                citation: "Urban, D. et al., 'The Solid Fuel Ignition and Extinction (SoFIE) Project', Combustion and Flame, Vol. 245, 2022.",
            },
            ResearchRecord {
                experiment: "NASA Saffire (Spacecraft Fire Safety Demonstration)",
                psi_id: "PSI-SAFFIRE-I-IV",
                pis: "Dr. David Urban (NASA GRC), Dr. Gary Ruff (NASA GRC), Prof. James S. T'ien (CWRU)",
                facility: "Northrop Grumman Cygnus Spacecraft (Post-ISS Unberthing)",
                finding: "Thực nghiệm đốt mẫu vải khổ lớn (0.4m x 1.0m) đầu tiên trong lịch sử hàng không vũ trụ. Chứng minh ngọn lửa trong tàu vũ trụ cháy bền bỉ hơn và lan rộng hơn nhiều so với dự báo mặt đất.",
                citation: "Ruff, G. A., Urban, D. L., et al., 'Large-Scale Fire Safety Experiments in Space: Saffire-I through IV', Proc. Combust. Inst., 2020.",
            },
            ResearchRecord {
                experiment: "NASA BASS & BASS-II (Burning and Suppression of Solids)",
                psi_id: "PSI-BASS-II-P849",
                pis: "Dr. Sandra Olson (NASA GRC), Paul Ferketič (ZIN Technologies)",
                facility: "ISS Microgravity Science Glovebox (MSG)",
                finding: "Lập bản đồ giới hạn dập tắt (Extinction Limit) cho Nomex, Silicone RTV và PMMA. Xác định nồng độ oxy giới hạn (LOI) giảm mạnh trong môi trường vi trọng lực.",
                citation: "Olson, S. L., & Ferketič, P., 'Extinction Limits of Solid Fuel Combustion in Microgravity', Combust. Flame, Vol. 162, 2015.",
            },
            ResearchRecord {
                experiment: "NASA FLEX & FLEX-2 (Flame Extinction Experiment)",
                psi_id: "PSI-FLEX-ICE-102",
                pis: "Prof. Forman A. Williams (UC San Diego), Dr. Vedat Nayagam (NCSU)",
                facility: "ISS Multi-User Droplet Combustion Apparatus (MDCA)",
                finding: "Phát hiện hiện tượng 'Ngọn Lửa Lạnh' (Cool Flames) hình cầu trong giọt alkane tự do. Sau khi ngọn lửa nóng bị dập tắt, phản ứng oxy hóa nhiệt độ thấp (600K) tiếp tục tiêu thụ nhiên liệu và sinh CO vô hình.",
                citation: "Williams, F. A., Nayagam, V., et al., 'Spherical Cool Flames in Microgravity', Science, Vol. 338, Iss. 6114, pp. 1593-1596, 2012.",
            },
            ResearchRecord {
                experiment: "NASA ACME (BRE, CFI-G 85% O₂, E-FIELD Flames)",
                psi_id: "PSI-ACME-CIR-401",
                pis: "Prof. J. Quintiere (UMD), Prof. R. Axelbaum (WUSTL), Prof. D. Dunn-Rankin (UCI), Dr. D. Stocker (NASA GRC)",
                facility: "ISS Combustion Integrated Rack (CIR) - Modular ACME Hardware",
                finding: "Thực hiện 6 thí nghiệm lửa khí trên cùng bộ phần cứng module ACME trong CIR: BRE giả lập độ cháy vật liệu rắn bằng nhiên liệu khí; CFI-G thử nghiệm nồng độ oxy cao nhất (lên tới 85% O2) tạo ngọn lửa lộn ngược (inside-out flame); E-FIELD Flames dùng điện trường tác động lên ion lửa để giả lập trọng lực bán phần (do PSI hiện chưa có dữ liệu trọng lực bán phần thực tế cho tới khi có sứ mệnh LUCI và FM2).",
                citation: "Stocker, D. P., Quintiere, J. G., Axelbaum, R. L., et al., 'Advanced Combustion via Microgravity Experiments (ACME)', NASA/TM-2022-0008543, 2022.",
            },
            ResearchRecord {
                experiment: "NASA SPICE, SLICE, SAME/SAME-R & DAFT/DAFT-2",
                psi_id: "PSI-MSG-FLOW-512",
                pis: "Dr. David L. Urban (NASA GRC), Dr. Gary A. Ruff (NASA GRC), Dr. Sandra L. Olson (NASA GRC)",
                facility: "ISS Microgravity Science Glovebox (MSG) - Modular SPICE Fan-Driven Flow Duct",
                finding: "BASS, BASS-II, SPICE (Smoke Point In Co-flow Experiment) và SLICE (Structure & Liftoff In Combustion Experiment) dùng chung ống dẫn quạt gió của SPICE trong buồng MSG cho cả nhiên liệu rắn và khí. Đồng thời, thiết bị đo khói từ SAME/SAME-R đã được tái sử dụng để đo bụi trong DAFT & DAFT-2, đặt nền móng cho đầu báo khói thông minh và trang bị lính cứu hỏa trên Trái Đất.",
                citation: "Urban, D. L., Ruff, G. A., Olson, S. L., 'Spacecraft Fire Detection and Flow Duct Combustion in MSG', NASA/TP-2023-221450, 2023.",
            },
            ResearchRecord {
                experiment: "NASA Flammability Standard (NASA-STD-6001B Test 1)",
                psi_id: "NASA-STD-6001B-REV-B",
                pis: "NASA Materials & Processes Technical Branch (MSFC / JSC / WSTF)",
                facility: "NASA White Sands Test Facility (WSTF)",
                finding: "Quy định thử nghiệm bắt buộc lan truyền lửa hướng lên cho vật liệu cabin. Cảnh báo vật liệu đạt chuẩn tại 21% O2 mặt đất trở nên cực kỳ nguy hiểm trong khí quyển Artemis (34% O2, 56.5 kPa).",
                citation: "NASA Technical Standard NASA-STD-6001B, 'Flammability, Odor, Offgassing Requirements for Spacecraft Habitats', NASA MSFC, 2021.",
            },
        ],
        Language::En => vec![
            ResearchRecord {
                experiment: "NASA SoFIE (Solid Fuel Ignition and Extinction)",
                psi_id: "PSI-SOFIE-GEL-412",
                pis: "Dr. David Urban (NASA GRC), Prof. Carlos Fernandez-Pello (UC Berkeley)",
                facility: "ISS Combustion Integrated Rack (CIR)",
                finding: "Identified low-flow paradox: under low ventilation airflows (5-12 cm/s), PMMA flame spread rate reaches a local maximum exceeding terrestrial burning rates due to lack of convective heat loss.",
                citation: "Urban, D. et al., 'The Solid Fuel Ignition and Extinction (SoFIE) Project', Combustion and Flame, Vol. 245, 2022.",
            },
            ResearchRecord {
                experiment: "NASA Saffire (Spacecraft Fire Safety Demonstration)",
                psi_id: "PSI-SAFFIRE-I-IV",
                pis: "Dr. David Urban (NASA GRC), Dr. Gary Ruff (NASA GRC), Prof. James S. T'ien (CWRU)",
                facility: "Northrop Grumman Cygnus Spacecraft (Post-ISS Unberthing)",
                finding: "First large-scale fabric burn tests (0.4m x 1.0m) in aerospace history inside Cygnus cargo ships. Proved low-g fires grow significantly larger and persist at lower oxygen levels than terrestrial 1g tests predict.",
                citation: "Ruff, G. A., Urban, D. L., et al., 'Large-Scale Fire Safety Experiments in Space: Saffire-I through IV', Proc. Combust. Inst., 2020.",
            },
            ResearchRecord {
                experiment: "NASA BASS & BASS-II (Burning and Suppression of Solids)",
                psi_id: "PSI-BASS-II-P849",
                pis: "Dr. Sandra Olson (NASA GRC), Paul Ferketič (ZIN Technologies)",
                facility: "ISS Microgravity Science Glovebox (MSG)",
                finding: "Mapped extinction boundaries for Nomex, Silicone RTV, and PMMA in the ISS MSG. Established that the Limiting Oxygen Index (LOI) shifts downward in microgravity under moderate airflow.",
                citation: "Olson, S. L., & Ferketič, P., 'Extinction Limits of Solid Fuel Combustion in Microgravity', Combust. Flame, Vol. 162, 2015.",
            },
            ResearchRecord {
                experiment: "NASA FLEX & FLEX-2 (Flame Extinction Experiment)",
                psi_id: "PSI-FLEX-ICE-102",
                pis: "Prof. Forman A. Williams (UC San Diego), Dr. Vedat Nayagam (NCSU)",
                facility: "ISS Multi-User Droplet Combustion Apparatus (MDCA)",
                finding: "Discovered spherical 'Cool Flames' in free-floating alkane droplets. After hot flame extinction, low-temperature oxidation (600-800K) continues invisibly, consuming fuel and generating high CO.",
                citation: "Williams, F. A., Nayagam, V., et al., 'Spherical Cool Flames in Microgravity', Science, Vol. 338, Iss. 6114, pp. 1593-1596, 2012.",
            },
            ResearchRecord {
                experiment: "NASA ACME (BRE, CFI-G 85% O₂, E-FIELD Flames)",
                psi_id: "PSI-ACME-CIR-401",
                pis: "Prof. J. Quintiere (UMD), Prof. R. Axelbaum (WUSTL), Prof. D. Dunn-Rankin (UCI), Dr. D. Stocker (NASA GRC)",
                facility: "ISS Combustion Integrated Rack (CIR) - Modular ACME Hardware",
                finding: "Six gaseous flame experiments using shared modular ACME hardware in the CIR: BRE emulated solid material flammability using gas burners; CFI-G tested up to 85% O2 creating inside-out spherical flames; E-FIELD Flames used electric fields on flame ions to mimic partial gravity (bridging the gap until future lunar LUCI and FM2 partial-g data enter PSI).",
                citation: "Stocker, D. P., Quintiere, J. G., Axelbaum, R. L., et al., 'Advanced Combustion via Microgravity Experiments (ACME)', NASA/TM-2022-0008543, 2022.",
            },
            ResearchRecord {
                experiment: "NASA SPICE, SLICE, SAME/SAME-R & DAFT/DAFT-2",
                psi_id: "PSI-MSG-FLOW-512",
                pis: "Dr. David L. Urban (NASA GRC), Dr. Gary A. Ruff (NASA GRC), Dr. Sandra L. Olson (NASA GRC)",
                facility: "ISS Microgravity Science Glovebox (MSG) - Modular SPICE Fan-Driven Flow Duct",
                finding: "BASS, BASS-II, SPICE (Smoke Point In Co-flow Experiment), and SLICE (Structure & Liftoff In Combustion Experiment) shared the SPICE fan-driven flow duct inside the MSG for solid and gaseous fuels. Additionally, smoke detection hardware from SAME/SAME-R was repurposed for dust monitoring in DAFT & DAFT-2, driving Earth spin-offs in smart smoke detectors and firefighter gear.",
                citation: "Urban, D. L., Ruff, G. A., Olson, S. L., 'Spacecraft Fire Detection and Flow Duct Combustion in MSG', NASA/TP-2023-221450, 2023.",
            },
            ResearchRecord {
                experiment: "NASA Flammability Standard (NASA-STD-6001B Test 1)",
                psi_id: "NASA-STD-6001B-REV-B",
                pis: "NASA Materials & Processes Technical Branch (MSFC / JSC / WSTF)",
                facility: "NASA White Sands Test Facility (WSTF)",
                finding: "Mandatory upward flame propagation qualification standard. Proves materials certified at 21% O2 become highly flammable in enriched exploration atmospheres (Artemis 34% O2, 56.5 kPa).",
                citation: "NASA Technical Standard NASA-STD-6001B, 'Flammability, Odor, Offgassing Requirements for Spacecraft Habitats', NASA MSFC, 2021.",
            },
        ],
    }
}
