from __future__ import annotations

import html

TRANSLATIONS = {
    "vi": {
        "page_title": "Flames in Freefall | Bebo ZeroG-X",
        "usa_banner_1": "BÀI DỰ THI CHÍNH THỨC NASA SPACE APPS CHALLENGE 2026",
        "usa_banner_2": "Đội thi: Bebo ZeroG-X (THPT FPT) • Lead: Vũ Bảo Nam • Thành viên: Đỗ Duy Nam, Lương Đức Tùng, Trịnh Đức Anh",
        "nav_agency_title": "BEBO ZEROG-X • THPT FPT",
        "nav_agency_sub": "TRÍ TUỆ NHÂN TẠO AN TOÀN CHÁY VŨ TRỤ • NASA SPACE APPS 2026",
        "disk_active": "KHO DỮ LIỆU ĐĨA HOẠT ĐỘNG",
        "cache_active": "BỘ NHỚ ĐỆM NASA PSI CHÍNH THỨC HOẠT ĐỘNG",
        "hero_pill": "NASA SPACE APPS CHALLENGE 2026 • AN TOÀN HÀNG KHÔNG VŨ TRỤ TIÊN TIẾN",
        "hero_title": "SI Đánh giá An toàn Cháy Tàu Vũ trụ (Super Intelligence)",
        "hero_desc": (
            "Nghiên cứu động học đốt cháy phi tuyến tính, nghịch lý bốc cháy dưới luồng khí thông gió thấp và hiểm họa "
            "ngọn lửa lạnh nhằm bảo vệ môi trường sống của phi hành gia trên Trạm ISS, Căn cứ Mặt Trăng Artemis và Tàu du hành Sao Hỏa."
        ),
        
        "card_atm_title": "Hồ sơ Khí quyển Đang chọn",
        "card_threat_title": "Nguy cơ Cháy Đỉnh điểm",
        "threat_critical": "NGUY CƠ NGUY HIỂM",
        "threat_high": "NGUY CƠ CAO",
        "threat_moderate": "NGUY CƠ TRUNG BÌNH",
        "threat_safe": "ĐẠT CHUẨN / AN TOÀN",
        "card_ignitable_title": "Vật liệu Dễ Bốc cháy",
        "card_tested_sub": "Đã khảo nghiệm",
        "card_critical_high_sub": "{critical} Nguy cấp • {high} Rủi ro cao",
        "card_cool_flame_title": "Bất thường Ngọn Lửa Lạnh",
        "cool_flame_materials": "Vật liệu",
        "cool_flame_active": "BẤT THƯỜNG HOẠT ĐỘNG",
        "cool_flame_nominal": "BÌNH THƯỜNG / ĐÃ DẬP",
        
        "sidebar_lang_title": "🌐 Ngôn ngữ / Language",
        "sidebar_control_title": "BEBO IGNIS-0G",
        "sidebar_control_sub": "BỘ GIẢ LẬP MÔI TRƯỜNG KHOANG VŨ TRỤ",
        "presets_header": "🚀 Kịch bản Bay (Thiết lập sẵn)",
        "preset_select_label": "Chọn Môi trường Khoang Phi thuyền",
        "preset_iss": "🛰️ Trạm ISS (0.0g • Vi trọng lực)",
        "preset_artemis": "🌙 Khoang Artemis (0.16g • Mặt Trăng)",
        "preset_mars": "🔴 Tàu Sao Hỏa (0.38g • Quá cảnh)",
        "preset_earth": "🌍 Chuẩn Trái Đất (1.0g • Mặt đất)",
        "preset_custom": "⚙️ Tùy chỉnh Thông số Bay",
        "controls_header": "🎛️ Điều khiển Khí quyển & Trọng lực",
        "gravity_label": "Mức Trọng lực (g)",
        "gravity_help": "0.0g = Quỹ đạo ISS, 0.16g = Bề mặt Mặt Trăng, 0.38g = Bề mặt Sao Hỏa, 1.0g = Chuẩn Trái Đất.",
        "oxygen_label": "Nồng độ Oxy trong Khoang (Vol %)",
        "oxygen_help": "Không khí Trái Đất & ISS chuẩn là 21%. Khí quyển Khám phá Artemis dùng 34% O2 ở áp suất giảm.",
        "pressure_label": "Tổng Áp suất Khoang (kPa)",
        "pressure_help": "Mực nước biển chuẩn là 101.3 kPa. Khoang Mặt Trăng Artemis hoạt động ở 56.5 kPa (8.2 psi).",
        "airflow_label": "Vận tốc Gió Thông gió (cm/s)",
        "airflow_help": "Hệ thống thông gió khoang thường duy trì gió từ 5 đến 20 cm/s để tránh túi tích tụ CO2.",
        "ai_header": "🧠 Động cơ Trợ lý AI Co-Pilot",
        "ai_provider_label": "Nguồn Trí tuệ Nhân tạo",
        "ai_mode_offline": "⚡ Chuyên gia Cục bộ (Offline • 0s)",
        "ai_mode_online": "🌐 Trực tuyến Cloud (Gemini / OpenAI)",
        "api_key_label": "Nhập API Key {provider}",
        "api_key_placeholder": "AIzaSy... hoặc sk-...",
        "api_key_help": "Nếu để trống hoặc không hợp lệ, hệ thống sẽ tự động dùng Động cơ Chuyên gia Cục bộ.",
        "ref_experiments_title": "Tham chiếu Thí nghiệm NASA PSI:",
        
        "tab_sim": "📊 1. Giả lập Môi trường",
        "tab_morph": "🔥 2. Hình thái Lửa",
        "tab_rag": "🤖 3. AI Co-Pilot & RAG",
        "tab_matrix": "🚨 4. Ma trận Khẩn cấp",
        "tab_research": "📚 5. Thư viện NASA PSI",
        
        "tab1_ranking_title": "📊 Xếp hạng Nguy cơ Cháy Vật liệu Hàng không Vũ trụ",
        "tab1_ranking_caption": "Sắp xếp động theo Điểm Nguy cơ Cháy Vũ trụ (SFRS: 0-100). Đánh giá biên độ bắt cháy, gia tốc thông gió và quy đổi áp suất.",
        "th_rank": "THỨ HẠNG",
        "th_material": "VẬT LIỆU BAY",
        "th_moc": "MOC (HIỆU DỤNG)",
        "th_spread": "TỐC ĐỘ LAN",
        "th_sfrs": "ĐIỂM SFRS",
        "th_status": "TRẠNG THÁI",
        "cool_flame_legend": "🟣 = Bất thường ngọn lửa lạnh âm ỉ đang kích hoạt dưới điều kiện gió thấp / vi trọng lực hiện tại.",
        "tab1_physics_title": "📈 Phân tích Động học Đốt cháy",
        "sim_tunnel_badge": "BUỒNG MÔ PHỎNG KHÍ ĐỘNG HỌC & ĐỐT CHÁY VI TRỌNG LỰC",
        "sim_tunnel_sub": "BEBO IGNIS-0G • CFD & FLAME DYNAMICS REAL-TIME SIMULATOR",
        "sim_damkohler_label": "SỐ DAMKÖHLER (Da)",
        "sim_reynolds_label": "SỐ REYNOLDS (Re)",
        "sim_air_velocity": "VẬN TỐC DÒNG KHÍ",
        "sim_flame_spread": "TỐC ĐỘ LAN TRUYỀN",
        "sim_safety_margin": "BIÊN ĐỘ BẮT CHÁY (Δ)",
        "sim_sample_specimen": "MẪU THỬ BAY",
        "sim_status_quench": "⚠️ VÙNG TỰ DẬP BỨC XẠ (GIÓ YẾU < 2 cm/s)",
        "sim_status_paradox": "⚡ NGHỊCH LÝ 0G - TỐC ĐỘ CHÁY CỰC ĐẠI",
        "sim_status_blowoff": "💨 NGUY CƠ THỔI TẮT ĐỐI LƯU (GIÓ CAO)",
        "sim_status_lunar": "🌙 ĐỐT CHÁY BÁN TRỌNG LỰC (LUNAR/MARTIAN)",
        "sim_status_normal": "🌍 ĐỐT CHÁY ĐỐI LƯU TỰ NHIÊN (1.0g)",
        "chart_sfrs_title": "Điểm Nguy cơ Cháy Vũ trụ (SFRS) theo Vật liệu Bay",
        "chart_sfrs_yaxis": "Chỉ số SFRS",
        "chart_paradox_title": "Nghịch lý Bốc cháy Luồng gió Thấp (Low-Flow Paradox)",
        "chart_paradox_xaxis": "Vận tốc Gió Thông gió Cưỡng bức (cm/s)",
        "chart_paradox_yaxis": "Tốc độ Lan truyền Ngọn lửa (mm/s)",
        "legend_0g": "Vi trọng lực (0g) - Dòng khí cưỡng bức",
        "legend_1g": "Chuẩn Đối chiếu Mặt Đất (1g)",
        "legend_current_g": "Trọng lực Hiện tại ({g:.2f}g)",
        "legend_current_pt": "Điểm Vận hành Hiện tại ({v:.0f} cm/s)",
        "tab1_boundary_title": "🗺️ Bản đồ Ranh giới Dập tắt: Vùng Tự Tắt Bức Xạ vs Bị Thổi Tắt Đối Lưu",
        "tab1_boundary_caption": "Trực quan hóa đường biên dạng chữ U. Khi thông số khoang nằm trong vùng tô màu, đám cháy được duy trì. Dưới đường cong, lửa tự tắt.",
        "select_boundary_mat": "Chọn Vật liệu để Phân tích Ranh giới",
        "boundary_burn": "ĐANG CHÁY",
        "boundary_extinguished": "ĐÃ TỰ DẬP TẮT",
        "boundary_xaxis": "Vận tốc Gió Cưỡng bức (cm/s)",
        "boundary_yaxis": "Nồng độ Oxy (Vol %)",
        "annotation_quench": "Nhánh Tự Tắt Bức Xạ (Gió Thấp)",
        "annotation_blowoff": "Nhánh Bị Thổi Tắt Đối Lưu (Gió Cao)",
        "base_terrestrial_moc": "MOC Chuẩn Mặt Đất (1g):",
        "base_microg_moc": "MOC Vi Trọng Lực (0g):",
        "quenching_mode_label": "Cơ chế Dập tắt:",
        
        "tab2_title": "🔥 Trình mô phỏng Chuyển đổi Hình thái Lửa Động (Dynamic Flame Morphology Visualizer)",
        "tab2_caption": "Khám phá sự chuyển biến hình học, trường nhiệt độ và phát xạ bức xạ ngọn lửa theo trọng lực (1.0g Giọt nước -> 0.0g Hình cầu xanh -> 0.16g/0.38g Bán cầu bành trướng) và vận tốc thông gió.",
        "active_regime_badge": "CHẾ ĐỘ HÌNH THÁI HIỆN TẠI",
        "peak_temp_label": "Nhiệt độ Đỉnh:",
        "soot_vol_label": "Tỷ lệ Thể tích Bồ hóng:",
        "aspect_ratio_card": "Tỷ số Dạng L/W (Aspect Ratio)",
        "cross_section_title": "🎨 Trực quan hóa Hình thái Học Cắt lớp (Cross-Section Rendering)",
        "cross_section_caption": "Mô phỏng hình học ngọn lửa thực tế dưới tương tác giữa Lực đẩy Ác-si-mét và Khuếch tán phân tử.",
        "temp_contour_title": "🌡️ Bản đồ Đẳng nhiệt & Mô hình 3D",
        "view_2d_contour": "📊 Bản đồ Đẳng nhiệt 2D",
        "view_3d_model": "🌐 Mô hình Không gian 3D",
        "view_isometric": "🪐 Xiên 3D (Isometric)",
        "view_top": "🔝 Nhìn Từ Trên (Top)",
        "view_side": "📐 Cắt Ngang (Side)",
        "open_3d_btn_label": "Kích hoạt Mô hình 3D Tương tác",
        "help_3d_tip": "💡 Mẹo: Nhấp giữ chuột trái hoặc vuốt màn hình để xoay 360°, cuộn chuột để phóng to / thu nhỏ mô hình 3D.",
        "model_3d_specs": "Mô hình Vật lý 3D: Trường nhiệt thể tích, vỏ phản ứng hóa phát quang & thanh nhiên liệu",
        "temp_contour_caption": "Trường phân bố nhiệt độ Kelvin (T) và phát xạ quang phổ theo phương trình truyền nhiệt vi trọng lực.",
        "fuel_rod_label": "THANH VẬT LIỆU",
        "vent_flow_label": "GIÓ V={v:.0f} cm/s",
        "active_morph_label": "Hình thái Hoạt động:",
        "contour_temp_bar": "Nhiệt độ (K)",
        "contour_radial_x": "Tọa độ Bán kính (cm)",
        "contour_axial_y": "Tọa độ Trục đứng (cm)",
        "comparison_table_title": "🔬 Bảng Đối Chiếu Động Học Đốt Cháy: Trái Đất (1g) vs Vi Trọng Lực (0g) vs Trọng Lực Mặt Trăng/Sao Hỏa",
        
        "tab3_title": "🤖 Module RAG Thực chiến & Tra cứu Tài liệu NASA PSI",
        "tab3_caption": "Semantic Vector Search Engine tích hợp kho văn bản nghiên cứu gốc NASA PSI (SoFIE, Saffire, BASS-II, FLEX-2, NASA-STD-6001B). Trích xuất đoạn văn chuẩn xác kèm số trang, mã báo cáo và tên tác giả.",
        "sample_queries_label": "💡 Câu hỏi mẫu thường gặp (Nhấp để tra cứu nhanh):",
        "q1_btn": "PMMA dưới gió thấp?",
        "q2_btn": "Nguy cơ tia nước chữa cháy?",
        "q3_btn": "Ngọn lửa lạnh là gì?",
        "q4_btn": "Cháy trên Mặt Trăng 0.16g vs 0g?",
        "q1_text": "Điều gì xảy ra với tốc độ cháy của nhựa PMMA dưới luồng gió thông gió thấp trong vi trọng lực?",
        "q2_text": "Tại sao tia nước chữa cháy áp lực cao đơn lẻ bị nghiêm cấm tuyệt đối trên tàu vũ trụ?",
        "q3_text": "Hiện tượng Ngọn lửa lạnh (Cool Flames) là gì và được phát hiện trên trạm ISS như thế nào?",
        "q4_text": "Nguy cơ cháy ở trọng lực bán phần trên Mặt Trăng (0.16g) nguy hiểm hơn môi trường 0g ra sao?",
        "search_input_label": "🔎 Nhập câu hỏi tự do về An toàn Cháy & Tài liệu NASA PSI:",
        "search_input_help": "Hệ thống thực hiện vector embedding, tính cosine similarity và trích xuất đoạn văn liên quan nhất từ kho báo cáo NASA PSI.",
        "ai_answer_title": "🧠 Câu trả lời Tổng hợp từ Chuyên gia NASA Safety",
        "grounded_evidence_badge": "● CĂN CỨ VÀO DỮ LIỆU BAY THỰC TẾ",
        "rag_specs_title": "📌 Thông số Kỹ thuật Hệ thống RAG:",
        "retrieved_passages_title": "📄 Các đoạn Văn bản Trích xuất Liên quan nhất (Retrieved Passages)",
        "report_id_lbl": "MÃ BÁO CÁO:",
        "page_lbl": "SỐ TRANG:",
        "section_lbl": "PHÂN ĐOẠN:",
        "authors_lbl": "Tác giả / PIs:",
        "facility_lbl": "Thiết bị Vũ trụ:",
        "deep_dive_title": "🔬 Deep-Dive Material AI Co-Pilot & Chẩn đoán Ngọn Lửa Lạnh",
        "deep_dive_caption": "Khám phá chuyên sâu động học vi trọng lực, nguy cơ ngọn lửa lạnh và khuyến cáo NASA-STD-6001B cho từng vật liệu bay.",
        "select_material_copilot": "Chọn Vật liệu Bay để Phân tích & Chẩn đoán",
        "cool_flame_alert_heading": "CẢNH BÁO AN TOÀN BAY: VÙNG NGỌN LỬA LẠNH (COOL FLAMES)",
        
        "tab4_title": "🚨 Ma trận Ứng phó Khủng hoảng & Dập lửa Tự động (Automated Emergency Suppression & Mitigation)",
        "tab4_caption": "Bảng khuyến cáo kỹ thuật 3 cột tự động sinh ra cho các vật liệu xếp hạng Đỏ (Critical Risk) và Cam (High Risk) dưới môi trường giả lập hiện tại.",
        "no_critical_title": "✅ KHÔNG CÓ VẬT LIỆU XẾP HẠNG NGUY CƠ ĐỎ / CAO",
        "no_critical_desc": "Dưới môi trường hiện tại, toàn bộ các vật liệu được khảo sát đều tự dập tắt (Self-Extinguishing) hoặc nằm trong ngưỡng an toàn.",
        "critical_alert": "CẢNH BÁO: Phát hiện {count} vật liệu trong khoang đạt ngưỡng Nguy cơ Bùng cháy Cấp độ Đỏ / Cao.",
        "critical_alert_sub": "Quy trình ứng phó khẩn cấp phải tuân thủ nghiêm ngặt quy định không kích thích dòng khí và cấm dùng tia nước đơn lẻ.",
        "th_matrix_mat": "VẬT LIỆU NGUY CƠ",
        "th_matrix_act1": "HÀNH ĐỘNG KHẨN CẤP SỐ 1",
        "th_matrix_agent": "TÁC NHÂN DẬP LỬA TỐI ƯU",
        "th_matrix_haz": "NGUY CƠ PHỤ & ĐỘC TÍNH PHI HÀNH GIA",
        "col1_hdr": "⚡ CỘT 1: HÀNH ĐỘNG KHẨN CẤP SỐ 1 (T+0s - T+3s)",
        "col2_hdr": "🧯 CỘT 2: TÁC NHÂN DẬP LỬA TỐI ƯU",
        "col3_hdr": "⚠️ CỘT 3: NGUY CƠ PHỤ & ĐỘC TÍNH",
        "dossiers_title": "📑 Sổ tay Xử lý Khủng hoảng & Hút lọc Khí độc Chi tiết (Decontamination Dossiers)",
        "act1_label": "Hành động tức thời (T+0s):",
        "agent_label": "Tác nhân dập lửa chỉ định:",
        "hazard_label": "Hiểm họa thứ cấp đối với ECLSS:",
        "decon_label": "Quy trình Phục hồi & Khử độc khí quyển trạm:",
        "export_title": "📋 Xuất Báo cáo Kỹ thuật & Bản tóm tắt Khẩn cấp (Technical Briefing Export)",
        "btn_download_json": "💾 Tải Toàn bộ Ma trận Khẩn cấp (JSON Payload)",
        "btn_download_md": "📄 Tải Bản tóm tắt Khẩn cấp (Markdown Briefing)",
        
        "tab5_title": "📚 Thư viện Nghiên cứu NASA PSI & Dữ liệu Thực nghiệm Gốc",
        "tab5_caption": "Tổng hợp các công bố khoa học bình duyệt, thông tin PIs, liên kết DOI và dữ liệu đo đạc CSV từ các nhiệm vụ SoFIE, Saffire, BASS-II và FLEX.",
        "finding_lbl": "Đóng góp Khoa học Cốt lõi:",
        "citation_lbl": "Trích dẫn Chuẩn Quốc tế:",
        "raw_explorer_title": "📂 Khảo sát Dữ liệu Thực nghiệm Thô (Raw PSI Telemetry Explorer)",
        "raw_explorer_caption": "Kết nối trực tiếp ống dẫn dữ liệu CSV từ Physical Sciences Informatics (PSI) nạp từ ổ đĩa.",
        "view_sofie_expander": "🔬 Xem Dữ liệu Đo đạc: NASA SoFIE PMMA Burn Rate Dataset (CIR / ISS)",
        "view_saffire_expander": "🚀 Xem Dữ liệu Đo đạc: NASA Saffire Large-Scale Flame Growth Dataset (Cygnus)",
        "view_bass_expander": "🧤 Xem Dữ liệu Đo đạc: NASA BASS-II & FLEX Extinction Limit Dataset (MSG / MDCA)",
        "download_raw_title": "💾 Dữ liệu Thực nghiệm Thô (Raw PSI Datasets)",
        "btn_download_sofie": "📥 Tải SoFIE PMMA Data (CSV)",
        "btn_download_saffire": "📥 Tải Saffire Large-Scale Data (CSV)",
        "btn_download_bass": "📥 Tải BASS-II Extinction Data (CSV)",
        
        "footer_mission_text": "NASA khám phá những điều chưa biết trong không gian và trên bầu trời, đổi mới vì lợi ích của nhân loại và truyền cảm hứng cho thế giới thông qua những khám phá.",
        "footer_official_lbl": "Đại diện NASA:",
        "footer_curator_lbl": "Cơ quan Phụ trách:",
        "footer_updated_lbl": "Cập nhật Lần cuối:",
        "footer_entry_text": "Bài dự thi chính thức cho <b>NASA Space Apps Challenge 2026</b>",
        "dossier_title": "HỒ SƠ THỰC NGHIỆM NASA PSI",
        "dossier_flight_mission": "Sứ mệnh Khảo nghiệm:",
        "dossier_category": "Phân loại Ứng dụng:",
        "dossier_geometry": "Hình học Nhiên liệu:",
        "dossier_formula": "Công thức Hóa học:",
        "dossier_heat_combustion": "Nhiệt trị Đốt cháy:",
        "dossier_1g_moc": "MOC Trái Đất (1G):",
        "dossier_ug_moc": "MOC Vi trọng lực (0G):",
        "dossier_base_spread": "Tốc độ Cháy Cơ sở:",
        "dossier_flame_morphology": "Hình thái Ngọn lửa:",
        "target_specimen_label": "🎯 Vật liệu Khảo sát trong Buồng đốt:",
        "mobile_swipe_hint": "👉 Vuốt ngang để xem đủ 6 cột dữ liệu (SFRS & Chuẩn NASA)",
        "temp_label": "Nhiệt độ Khoang",
        "temp_help": "Nhiệt độ môi trường khoang tàu (°C). Ảnh hưởng đến áp suất hơi bão hòa và quá trình gia nhiệt sơ bộ vật liệu.",
        "rh_label": "Độ ẩm Tương đối (RH)",
        "rh_help": "Độ ẩm tương đối (%). Ảnh hưởng pha loãng hơi nước và dung nhiệt đối lưu (Arden Buck).",
        "audio_mute_label": "🔇 Tắt âm Cảnh báo SFRS > 85",
        "audio_unmuted_status": "🔊 Âm thanh cảnh báo đang BẬT (880Hz/1046Hz khi SFRS > 85)",
        "audio_muted_status": "🔇 Âm thanh cảnh báo đã TẮT (chỉ hiển thị viền đỏ nhấp nháy)",
        "nasa_6001b_table_title": "Bảng Hiệu chuẩn Tiêu chuẩn NASA-STD-6001B (Test 1 & Test 2)",
        "nasa_6001b_table_caption": "Đối chiếu ngưỡng thử nghiệm cháy lan dọc (Test 1) và tốc độ tỏa nhiệt HRR (Test 2) theo NASA-STD-6001B.",
        "custom_mat_expander_title": "🧪 Đánh giá Vật liệu Composite Tùy chỉnh (Custom Specimen)",
        "custom_mat_submit_btn": "➕ Tính toán & Thêm vào Bảng Đánh giá",
        "scenario_comp_expander_title": "⚖️ So sánh Song song Hai Kịch bản Môi trường (Side-by-Side Diff & Radar)",
        "webgl_3d_mode_label": "🌐 Chế độ WebGL 3D Tương tác (Three.js 360°)",
        "ntc_kinetics_title": "Động học Ngọn lửa Lạnh 2-Bước (Cool Flame NTC Oscillatory Kinetics)",
        "ntc_kinetics_caption": "Mô phỏng phương trình vi phân liên kết nhiệt độ T(t) và nồng độ gốc CO [CO](t) trong vùng NTC.",
        "rag_upload_label": "📄 Tải lên Tài liệu Nghiên cứu (PDF / TXT / MD) để lập Chỉ mục Offline",
        "rag_clear_chat_btn": "🗑️ Xóa Lịch sử Hội thoại RAG",
        "rag_chat_history_title": "💬 Lịch sử Phân tích Đa lượt (Multi-Turn Session)",
        "btn_download_pdf": "📑 Tải Hồ sơ An toàn Sứ mệnh (NASA TM PDF)",
        
    },
    
    "en": {
        "page_title": "Flames in Freefall | Bebo ZeroG-X Fire Safety",
        "usa_banner_1": "OFFICIAL ENTRY FOR NASA SPACE APPS CHALLENGE 2026",
        "usa_banner_2": "Team: Bebo ZeroG-X (FPT High School) • Lead: Vu Bao Nam • Members: Do Duy Nam, Luong Duc Tung, Trinh Duc Anh",
        "nav_agency_title": "BEBO ZEROG-X • FPT HIGH SCHOOL",
        "nav_agency_sub": "AEROSPACE FIRE SAFETY AI • NASA SPACE APPS 2026",
        "disk_active": "DISK REPOSITORY ACTIVE",
        "cache_active": "OFFICIAL NASA PSI CACHE ACTIVE",
        "hero_pill": "NASA SPACE APPS CHALLENGE 2026 • ADVANCED AEROSPACE SAFETY",
        "hero_title": "SI-Powered Spacecraft Fire Safety (Super Intelligence & Physics AI)",
        "hero_desc": (
            "Investigating non-linear combustion kinetics, low-velocity ventilation flammability paradoxes, and hazardous "
            "cool flame transitions to safeguard long-duration crew habitats across the International Space Station, "
            "Artemis Lunar Base, and deep space Mars transit vehicles."
        ),
        
        "card_atm_title": "Active Atmosphere Profile",
        "card_threat_title": "Peak Space Fire Threat",
        "threat_critical": "CRITICAL HAZARD",
        "threat_high": "HIGH HAZARD",
        "threat_moderate": "MODERATE",
        "threat_safe": "NOMINAL / SAFE",
        "card_ignitable_title": "Ignitable Materials",
        "card_tested_sub": "Tested Materials",
        "card_critical_high_sub": "{critical} Critical • {high} High Risk",
        "card_cool_flame_title": "Cool Flame Anomaly",
        "cool_flame_materials": "Materials",
        "cool_flame_active": "ACTIVE ANOMALY",
        "cool_flame_nominal": "NORMAL / QUENCHED",
        
        "sidebar_lang_title": "🌐 Language / Ngôn ngữ",
        "sidebar_control_title": "BEBO IGNIS-0G",
        "sidebar_control_sub": "SPACE FLIGHT HABITAT SIMULATOR",
        "presets_header": "🚀 Flight Scenarios (Presets)",
        "preset_select_label": "Select Spacecraft Habitat Environment",
        "preset_iss": "🛰️ ISS Station (0.0g • Microgravity)",
        "preset_artemis": "🌙 Artemis Cabin (0.16g • Lunar)",
        "preset_mars": "🔴 Mars Transit (0.38g • Partial)",
        "preset_earth": "🌍 Earth Baseline (1.0g • Terrestrial)",
        "preset_custom": "⚙️ Custom Flight Parameters",
        "controls_header": "🎛️ Atmospheric & Gravity Controls",
        "gravity_label": "Gravity Level (g)",
        "gravity_help": "0.0g = ISS orbit, 0.16g = Moon surface, 0.38g = Mars surface, 1.0g = Earth standard.",
        "oxygen_label": "Cabin Oxygen Concentration (Vol %)",
        "oxygen_help": "Normal Earth & ISS air is 21%. Artemis Exploration Atmosphere uses 34% O2 at reduced pressure.",
        "pressure_label": "Total Cabin Pressure (kPa)",
        "pressure_help": "Standard sea level is 101.3 kPa. Artemis Lunar Habitat operates at 56.5 kPa (8.2 psi).",
        "airflow_label": "Ventilation Airflow Velocity (cm/s)",
        "airflow_help": "Cabin ventilation typically moves air between 5 and 20 cm/s to avoid CO2 pockets.",
        "ai_header": "🧠 AI Co-Pilot Engine",
        "ai_provider_label": "Intelligence Provider",
        "ai_mode_offline": "⚡ Local Expert (Offline • 0s)",
        "ai_mode_online": "🌐 Online Cloud (Gemini / OpenAI)",
        "api_key_label": "Enter {provider} API Key",
        "api_key_placeholder": "AIzaSy... or sk-...",
        "api_key_help": "If key is omitted or invalid, automatically falls back to the deterministic Aerospace Expert Engine.",
        "ref_experiments_title": "NASA PSI Experiment Reference:",
        
        "tab_sim": "📊 1. Environment Sim",
        "tab_morph": "🔥 2. Flame Morphology",
        "tab_rag": "🤖 3. AI Co-Pilot & RAG",
        "tab_matrix": "🚨 4. Emergency Matrix",
        "tab_research": "📚 5. NASA PSI Library",
        
        "tab1_ranking_title": "📊 Aerospace Materials Fire Hazard Ranking",
        "tab1_ranking_caption": "Ordered dynamically by Space Fire Risk Score (0-100). Evaluates ignition margin, ventilation acceleration, and pressure scaling.",
        "th_rank": "RANK",
        "th_material": "AEROSPACE MATERIAL",
        "th_moc": "MOC (EFF)",
        "th_spread": "SPREAD",
        "th_sfrs": "SFRS",
        "th_status": "STATUS",
        "cool_flame_legend": "🟣 = Cool Flame smoldering anomaly active under current low-airflow/microgravity conditions.",
        "tab1_physics_title": "📈 Combustion Physics Analytics",
        "sim_tunnel_badge": "MICROGRAVITY COMBUSTION & AERODYNAMIC TUNNEL",
        "sim_tunnel_sub": "BEBO IGNIS-0G • CFD & FLAME DYNAMICS REAL-TIME SIMULATOR",
        "sim_damkohler_label": "DAMKÖHLER NUMBER (Da)",
        "sim_reynolds_label": "REYNOLDS NUMBER (Re)",
        "sim_air_velocity": "AIRFLOW VELOCITY",
        "sim_flame_spread": "FLAME SPREAD RATE",
        "sim_safety_margin": "IGNITION MARGIN (Δ)",
        "sim_sample_specimen": "TEST SPECIMEN",
        "sim_status_quench": "⚠️ RADIATIVE QUENCHING ZONE (LOW FLOW < 2 cm/s)",
        "sim_status_paradox": "⚡ 0G LOW-FLOW PARADOX - PEAK SPREAD REGIME",
        "sim_status_blowoff": "💨 CONVECTIVE BLOW-OFF HAZARD (HIGH FLOW)",
        "sim_status_lunar": "🌙 PARTIAL GRAVITY COMBUSTION (LUNAR/MARTIAN)",
        "sim_status_normal": "🌍 NATURAL BUOYANT CONVECTION (1.0g)",
        "chart_sfrs_title": "Space Fire Risk Score (SFRS) by Flight Material",
        "chart_sfrs_yaxis": "SFRS Index",
        "chart_paradox_title": "The Low-Flow Ventilation Paradox",
        "chart_paradox_xaxis": "Forced Ventilation Airflow (cm/s)",
        "chart_paradox_yaxis": "Flame Spread Rate (mm/s)",
        "legend_0g": "Microgravity (0g) - Forced Flow",
        "legend_1g": "Terrestrial Baseline (1g)",
        "legend_current_g": "Current Gravity ({g:.2f}g)",
        "legend_current_pt": "Current Operating Point ({v:.0f} cm/s)",
        "tab1_boundary_title": "🗺️ Extinction Boundary Map: Quenching vs Blowoff Envelope",
        "tab1_boundary_caption": "Visualizing the U-shaped flammability boundary. When cabin conditions lie inside the colored envelope, combustion is sustained. Below the curve, fires extinguish spontaneously.",
        "select_boundary_mat": "Select Material for Boundary Analysis",
        "boundary_burn": "BURNING FLAME",
        "boundary_extinguished": "EXTINGUISHED",
        "boundary_xaxis": "Forced Airflow Velocity (cm/s)",
        "boundary_yaxis": "Oxygen Concentration (Vol %)",
        "annotation_quench": "Radiative Quenching Branch (Low Flow)",
        "annotation_blowoff": "Convective Blowoff Branch (High Flow)",
        "base_terrestrial_moc": "Base Terrestrial MOC (1g):",
        "base_microg_moc": "Base Microgravity MOC (0g):",
        "quenching_mode_label": "Quenching Mode:",
        
        "tab2_title": "🔥 Dynamic Flame Morphology Visualizer",
        "tab2_caption": "Explore geometrical transitions, temperature contours, and radiative emissions across gravities (1.0g Teardrop -> 0.0g Blue Sphere -> 0.16g/0.38g Expanding Hemisphere) and airflow velocities.",
        "active_regime_badge": "ACTIVE FLAME REGIME",
        "peak_temp_label": "Peak Temperature:",
        "soot_vol_label": "Soot Volume Fraction:",
        "aspect_ratio_card": "Flame Aspect Ratio (L/W)",
        "cross_section_title": "🎨 Cross-Section Morphology Rendering",
        "cross_section_caption": "Simulating physical flame geometry under the interplay of buoyancy and molecular diffusion.",
        "temp_contour_title": "🌡️ Temperature Contour & 3D Spatial Model",
        "view_2d_contour": "📊 2D Contour Map",
        "view_3d_model": "🌐 3D Spatial Model",
        "view_isometric": "🪐 Isometric 3D",
        "view_top": "🔝 Top-Down",
        "view_side": "📐 Side View",
        "open_3d_btn_label": "Activate Interactive 3D Model",
        "help_3d_tip": "💡 Tip: Click & drag or swipe to rotate 360°, scroll wheel or pinch to zoom into the 3D flame model.",
        "model_3d_specs": "3D Physical Model: Volumetric thermal field, chemiluminescent reaction shell & fuel rod",
        "temp_contour_caption": "Kelvin temperature distribution (T) and spectral emissions governed by microgravity heat transfer.",
        "fuel_rod_label": "FUEL ROD",
        "vent_flow_label": "VENT V={v:.0f} cm/s",
        "active_morph_label": "Active Morphology:",
        "contour_temp_bar": "Temp (K)",
        "contour_radial_x": "Radial Coordinate (cm)",
        "contour_axial_y": "Axial Coordinate (cm)",
        "comparison_table_title": "🔬 Combustion Kinetics Matrix: Earth (1g) vs ISS Microgravity (0g) vs Lunar/Mars Partial Gravity",
        
        "tab3_title": "🤖 RAG Semantic Search & Ask NASA PSI Docs",
        "tab3_caption": "Semantic Vector Search Engine pre-indexed with peer-reviewed NASA PSI flight research (SoFIE, Saffire, BASS-II, FLEX-2, NASA-STD-6001B). Extracts exact passages with page numbers, report IDs, and authors.",
        "sample_queries_label": "💡 Frequently Asked Questions (Click to search):",
        "q1_btn": "PMMA under low airflow?",
        "q2_btn": "Water jet extinguisher risk?",
        "q3_btn": "What are Cool Flames?",
        "q4_btn": "Moon 0.16g vs 0g fire danger?",
        "q1_text": "What happens to PMMA burning rate under low airflow in microgravity?",
        "q2_text": "Why are single high-velocity water jets strictly prohibited for spacecraft fire suppression?",
        "q3_text": "What are Cool Flames and how were they discovered on the ISS in FLEX?",
        "q4_text": "How does partial gravity on the Moon (0.16g) compare to zero-g fire behavior?",
        "search_input_label": "🔎 Ask any question about NASA Space Fire Safety & PSI Docs:",
        "search_input_help": "Vector embedding calculates cosine similarity to retrieve the most authoritative passages from the NASA PSI corpus.",
        "ai_answer_title": "🧠 Synthesized NASA Safety Officer Briefing",
        "grounded_evidence_badge": "● GROUNDED IN FLIGHT EVIDENCE",
        "rag_specs_title": "📌 RAG System Technical Specifications:",
        "retrieved_passages_title": "📄 Top Relevant Retrieved Passages",
        "report_id_lbl": "REPORT ID:",
        "page_lbl": "PAGE:",
        "section_lbl": "SECTION:",
        "authors_lbl": "Authors / PIs:",
        "facility_lbl": "Flight Facility:",
        "deep_dive_title": "🔬 Deep-Dive Material AI Co-Pilot & Cool Flame Diagnostics",
        "deep_dive_caption": "In-depth investigation of microgravity kinetics, cool flame risks, and NASA-STD-6001B compliance for each flight material.",
        "select_material_copilot": "Select Flight Material for Diagnostic Dossier",
        "cool_flame_alert_heading": "CRITICAL FLIGHT SAFETY ANOMALY: COOL FLAMES REGION",
        
        "tab4_title": "🚨 Automated Crisis Matrix & Emergency Fire Suppression",
        "tab4_caption": "Dynamic 3-column technical action matrix generated for all Critical (Red) and High Risk (Orange) materials under current simulated conditions.",
        "no_critical_title": "✅ NO CRITICAL / HIGH RISK MATERIALS DETECTED",
        "no_critical_desc": "Under current cabin conditions, all evaluated materials are self-extinguishing or remain within safe thresholds.",
        "critical_alert": "CRITICAL ALERT: Detected {count} materials exceeding Red / High Risk Flammability Thresholds.",
        "critical_alert_sub": "Emergency protocols strictly prohibit convective air excitation and forbid single high-velocity water jets.",
        "th_matrix_mat": "FLIGHT MATERIAL",
        "th_matrix_act1": "IMMEDIATE ACTION #1",
        "th_matrix_agent": "OPTIMAL SUPPRESSION AGENT",
        "th_matrix_haz": "SECONDARY HAZARD & CREW TOXICITY",
        "col1_hdr": "⚡ COLUMN 1: IMMEDIATE ACTION #1 (T+0s - T+3s)",
        "col2_hdr": "🧯 COLUMN 2: OPTIMAL SUPPRESSION AGENT",
        "col3_hdr": "⚠️ COLUMN 3: SECONDARY HAZARD & TOXICITY",
        "dossiers_title": "📑 Detailed Crisis Decontamination Dossiers",
        "act1_label": "Immediate Action (T+0s):",
        "agent_label": "Designated Suppression Agent:",
        "hazard_label": "Secondary ECLSS Hazard:",
        "decon_label": "Atmospheric Decontamination Protocol:",
        "export_title": "📋 Export Technical Briefing & Emergency Dossiers",
        "btn_download_json": "💾 Download Complete Emergency Matrix (JSON Payload)",
        "btn_download_md": "📄 Download Emergency Briefing (Markdown Briefing)",
        
        "tab5_title": "📚 NASA PSI Research Library & Flight Datasets",
        "tab5_caption": "Peer-reviewed publications, Principal Investigators (PIs), DOI citations, and telemetry CSV datasets from SoFIE, Saffire, BASS-II, and FLEX missions.",
        "finding_lbl": "Core Scientific Contribution:",
        "citation_lbl": "International Peer-Reviewed Citation:",
        "raw_explorer_title": "📂 Raw NASA PSI Experimental Telemetry Explorer",
        "raw_explorer_caption": "Live connection to Physical Sciences Informatics (PSI) CSV data pipeline ingested from disk.",
        "view_sofie_expander": "🔬 View Live Telemetry: NASA SoFIE PMMA Burn Rate Dataset (CIR / ISS)",
        "view_saffire_expander": "🚀 View Live Telemetry: NASA Saffire Large-Scale Flame Growth Dataset (Cygnus)",
        "view_bass_expander": "🧤 View Live Telemetry: NASA BASS-II & FLEX Extinction Limit Dataset (MSG / MDCA)",
        "download_raw_title": "💾 Raw Experimental Telemetry Datasets",
        "btn_download_sofie": "📥 Download SoFIE PMMA Data (CSV)",
        "btn_download_saffire": "📥 Download Saffire Large-Scale Data (CSV)",
        "btn_download_bass": "📥 Download BASS-II Extinction Data (CSV)",
        
        "footer_mission_text": "NASA explores the unknown in air and space, innovates for the benefit of humanity, and inspires the world through discovery.",
        "footer_official_lbl": "NASA Official:",
        "footer_curator_lbl": "Curator:",
        "footer_updated_lbl": "Page Last Updated:",
        "footer_entry_text": "Official Entry for <b>NASA Space Apps Challenge 2026</b>",
        "dossier_title": "NASA PSI FLIGHT DOSSIER",
        "dossier_flight_mission": "Flight Mission:",
        "dossier_category": "Aerospace Category:",
        "dossier_geometry": "Fuel Geometry:",
        "dossier_formula": "Chemical Formula:",
        "dossier_heat_combustion": "Heat of Combustion:",
        "dossier_1g_moc": "1G Earth MOC:",
        "dossier_ug_moc": "Microgravity MOC:",
        "dossier_base_spread": "Base Spread Rate:",
        "dossier_flame_morphology": "Flame Morphology:",
        "target_specimen_label": "🎯 Combustion Specimen in Tunnel:",
        "mobile_swipe_hint": "👉 Swipe horizontally to view all 6 columns (SFRS & NASA Standards)",
        "temp_label": "Cabin Temperature",
        "temp_help": "Ambient cabin temperature (°C). Influences saturation vapor pressure and fuel pre-heating enthalpy.",
        "rh_label": "Relative Humidity (RH)",
        "rh_help": "Relative humidity (%). Modulates water-vapor molar dilution and inerting capacity (Arden Buck).",
        "audio_mute_label": "🔇 Mute Critical Alert Audio (SFRS > 85)",
        "audio_unmuted_status": "🔊 Critical alert chime ARMED (880Hz/1046Hz when SFRS > 85)",
        "audio_muted_status": "🔇 Alert audio MUTED (visual red perimeter pulse remains active)",
        "nasa_6001b_table_title": "NASA-STD-6001B Calibration Matrix (Test 1 & Test 2)",
        "nasa_6001b_table_caption": "Formal upward flame propagation pass/fail thresholds (Test 1) and cone calorimeter HRR limits (Test 2).",
        "custom_mat_expander_title": "🧪 Custom Composite Material Evaluation (NASA-STD-6001B Screening)",
        "custom_mat_submit_btn": "➕ Evaluate & Append to Matrix",
        "scenario_comp_expander_title": "⚖️ Side-by-Side Scenario Comparison (Delta Diff & 5-Axis Radar)",
        "webgl_3d_mode_label": "🌐 Interactive 3D WebGL Engine (Three.js 360°)",
        "ntc_kinetics_title": "2-Step Cool Flame NTC Oscillatory Kinetics ODE",
        "ntc_kinetics_caption": "Coupled differential evolution of gas temperature T(t) and CO intermediate radical concentration [CO](t).",
        "rag_upload_label": "📄 Upload Research Paper (PDF / TXT / MD) to Offline Vector Index",
        "rag_clear_chat_btn": "🗑️ Reset RAG Conversation History",
        "rag_chat_history_title": "💬 Multi-Turn Flight Safety Consultation History",
        "btn_download_pdf": "📑 Download Mission Safety Dossier (NASA TM PDF)",
        
    }
}


BILINGUAL_SUPPRESSION_DATABASE = {
    "MAT-01": {
        "name": "PMMA / Acrylic Rod (6.35mm)",
        "vi": {
            "action_1": "Ngắt ngay lập tức quạt thông gió HVAC phân khu trong 3 giây đầu tiên để đưa vận tốc dòng khí từ 10 cm/s về < 2 cm/s, đẩy ngọn lửa vào Vùng Tự Dập Bức Xạ (Radiative Quenching).",
            "optimal_agent": "Sương nước siêu mịn (Fine Water Mist, giọt < 50 µm) đẩy bằng khí trơ N2; TUYỆT ĐỐI KHÔNG dùng tia nước đơn lẻ áp lực cao vì lực xung kích sẽ bắn tung polyme nóng chảy và tàn lửa khắp khoang vi trọng lực.",
            "secondary_hazard": "Sinh ra khí độc CO nồng độ cao và monomer Methyl Methacrylate bay hơi; bắt buộc phi hành gia đeo mặt nạ dưỡng khí PBE/SCBA áp dương tối thiểu 45 phút.",
            "decontamination": "Kích hoạt cụm lọc khói cơ động (Smoke Eater Canister) và chu trình hấp phụ carbon than hoạt tính của hệ thống ECLSS trong 12 giờ."
        },
        "en": {
            "action_1": "Immediately shut down sectional HVAC ventilation within 3 seconds to reduce airflow from 10 cm/s to < 2 cm/s, forcing the flame front into the Radiative Quenching Zone.",
            "optimal_agent": "Fine Water Mist (droplet diameter < 50 µm) propelled by gaseous N2; STRICTLY FORBID high-velocity single water jets to prevent hydrodynamic momentum from scattering molten polymers and embers across microgravity.",
            "secondary_hazard": "Generates high CO concentrations and vaporized Methyl Methacrylate monomer; mandatory crew donning of positive-pressure PBE/SCBA breathing masks for a minimum of 45 minutes.",
            "decontamination": "Deploy portable Smoke Eater canisters and engage ECLSS activated carbon adsorption scrubbing loop for 12 hours."
        }
    },
    "MAT-02": {
        "name": "Cotton-Fiberglass Blend (75/25)",
        "vi": {
            "action_1": "Đóng sập cửa khoang khí quyển (Cabin Hatch Barrier) và ngắt van thông gió phân khu; che phủ bề mặt vải cháy bằng chăn chống cháy Nomex dập bùng.",
            "optimal_agent": "Khí CO2 tràn ngập toàn khoang (Total Flooding CO2) hoặc bọt trơ dập bề mặt để triệt tiêu than hồng âm ỉ (smoldering glow) ngấm sâu trong lõi sợi thủy tinh.",
            "secondary_hazard": "Sợi thủy tinh siêu mịn bị vỡ vụn phát tán dưới dạng hạt khí dung lơ lửng gây tắc nghẽn bộ lọc HEPA của hệ thống ECLSS và đâm rách phế nang phổi phi hành gia.",
            "decontamination": "Thay thế khẩn cấp tiền màng lọc HEPA; sử dụng máy hút bụi chân không chuyên dụng HEPA quét sạch bề mặt cabin."
        },
        "en": {
            "action_1": "Seal cabin hatch barrier and shut isolation ventilation valves; smother burning fabric surface using Nomex fire-blanket.",
            "optimal_agent": "Total Flooding CO2 or surface inert foam to extinguish deep-seated glowing smolder trapped inside the fiberglass matrix.",
            "secondary_hazard": "Fractured fiberglass micro-particulates aerosolize into suspension, blinding ECLSS HEPA filters and posing severe crew pulmonary alveolar laceration hazards.",
            "decontamination": "Perform emergency replacement of HEPA pre-filters; deploy specialized sealed HEPA vacuum to clean all cabin surfaces."
        }
    },
    "MAT-03": {
        "name": "Nomex HT90-40 Aramid",
        "vi": {
            "action_1": "Hạ tức thời nồng độ oxy khoang xuống < 25% nếu đang ở cấu hình Artemis Cabin (34% O2); ngắt nguồn điện qua buồng hàng.",
            "optimal_agent": "Khí trơ N2 hoặc bình chữa cháy bọt bọc màng nước AFFF; chất ức chế gốc tự do Halotron/FE-36.",
            "secondary_hazard": "Pyrolysis giải phóng khí Hydrogen Cyanide (HCN) và Nitrogen Oxides (NOx) cực độc; cấm tháo mặt nạ thở khi chưa kiểm tra nồng độ khí bằng sắc ký.",
            "decontamination": "Sử dụng vật liệu hấp phụ acid gas trong hệ thống TCCS để trung hòa vết HCN."
        },
        "en": {
            "action_1": "Immediately depressurize / dilute cabin oxygen below 25% if operating in enriched Artemis cabin atmosphere (34% O2); de-energize cargo bay electrical circuits.",
            "optimal_agent": "Inert gaseous N2 or AFFF water-mist; free radical inhibitor Halotron/FE-36.",
            "secondary_hazard": "Pyrolysis off-gasses lethal Hydrogen Cyanide (HCN) and Nitrogen Oxides (NOx); crew must not doff breathing masks until gas chromatography confirms safe levels.",
            "decontamination": "Utilize acid-gas chemisorbent beds in the ECLSS Trace Contaminant Control Subsystem (TCCS) to scrub HCN."
        }
    },
    "MAT-04": {
        "name": "Silicone Elastomer RTV",
        "vi": {
            "action_1": "Cô lập thanh dẫn điện (electrical bus) cấp nhiệt cho khung cửa hatch; giảm chênh áp khoang để tránh rách gioăng làm thất thoát khí.",
            "optimal_agent": "Khối khí N2 trơ áp suất thấp hoặc bình dập bụi hóa học khô NASA; NGHIÊM CẤM xịt nước lạnh gây sốc nhiệt nứt vỡ kim loại cấu trúc cửa hatch.",
            "secondary_hazard": "Phân hủy tạo lớp tro xốp silica (SiO2) kèm khí siloxane bay hơi và CO nồng độ chết người âm ỉ kéo dài nhiều giờ (Cool Flame smolder).",
            "decontamination": "Cạo bỏ lớp tro silica sau khi làm nguội; vệ sinh bề mặt kim loại bằng dung môi isopropyl alcohol hàng không vũ trụ."
        },
        "en": {
            "action_1": "Isolate electrical bus supplying heat to hatch frame; reduce cabin pressure differential to prevent seal blowout.",
            "optimal_agent": "Low-pressure inert N2 flood or dry chemical agent; STRICTLY FORBID cold water spray to prevent thermal shock and structural hatch metal fracturing.",
            "secondary_hazard": "Forms porous white silica (SiO2) ash crust trapping heat, releasing volatile siloxanes and lethal CO concentrations in a prolonged invisible smolder.",
            "decontamination": "Scrape off silica ash once cooled; sanitize metal sealing surfaces using aerospace-grade isopropyl alcohol."
        }
    },
    "MAT-05": {
        "name": "Ultem 1000 Polyetherimide (PEI)",
        "vi": {
            "action_1": "Ngắt nguồn cung cấp nhiệt bức xạ bên ngoài; duy trì luồng khí trôi chậm để hỗ trợ lớp than phồng intumescent tự cách nhiệt.",
            "optimal_agent": "Bình xịt khí CO2 cục bộ hoặc Fine Water Mist; PEI có khả năng tự dập tắt cao khi cắt nguồn nhiệt.",
            "secondary_hazard": "Khí khói chứa vết sulfur dioxide (SO2) và phenol; kích ứng niêm mạc mắt phi hành gia nếu tiếp xúc trực tiếp.",
            "decontamination": "Chạy quạt lọc xúc tác oxy hóa nhiệt độ thấp của trạm để phân hủy khí phenol."
        },
        "en": {
            "action_1": "Cut external radiant heat source; maintain slow ambient drift to facilitate intumescent self-insulating char formation.",
            "optimal_agent": "Localized CO2 stream or Fine Water Mist; PEI exhibits rapid self-extinction once radiant flux is removed.",
            "secondary_hazard": "Smoke plume contains trace sulfur dioxide (SO2) and phenol vapors; causes acute ocular and mucosal irritation.",
            "decontamination": "Operate low-temperature ambient catalytic oxidizer scrubbers to decompose airborne phenol vapors."
        }
    },
    "MAT-06": {
        "name": "Teflon / PTFE Fluoropolymer",
        "vi": {
            "action_1": "Cắt khẩn cấp cầu dao điện chính của cụm bó dây (wire harness) bị quá nhiệt trong vòng 1 giây; ngắt nguồn sạc pin lithium liền kề.",
            "optimal_agent": "Khí trơ hóa lỏng làm lạnh nhanh (N2/CO2); TUYỆT ĐỐI KHÔNG dùng nước tạo phản ứng thủy phân axit flohydric bốc khói.",
            "secondary_hazard": "Phát tán khí kịch độc Carbonyl Fluoride (COF2), Hydrogen Fluoride (HF) và PFIB gây phù phổi cấp tử vong ngay cả ở nồng độ cực nhỏ (vài ppm).",
            "decontamination": "Súc rửa khí quyển khoang bằng cụm hấp phụ đá vôi bazơ kiềm; phi hành gia chuyển sang khoang lánh nạn an toàn."
        },
        "en": {
            "action_1": "Emergency trip main electrical breaker of overheating wire harness within 1 second; isolate adjacent lithium battery chargers.",
            "optimal_agent": "Rapid-cooling liquified inert gas (N2/CO2); NEVER use water which hydrolyzes into lethal fuming hydrofluoric acid.",
            "secondary_hazard": "Releases ultra-lethal Carbonyl Fluoride (COF2), Hydrogen Fluoride (HF), and PFIB, inducing fatal pulmonary edema even at trace concentrations (< 1 ppm).",
            "decontamination": "Flush cabin atmosphere through basic lime chemisorption filters; evacuate crew immediately to safe refuge module."
        }
    },
    "MAT-07": {
        "name": "Sibal Cotton Fabric",
        "vi": {
            "action_1": "Dập tắt quạt gió phân khu tức thì; phủ kín vùng cháy bằng màng chịu nhiệt chống cháy Kapton.",
            "optimal_agent": "Bình sương nước mịn Water Mist Extinguisher có bổ sung chất hoạt động bề mặt để thấm ướt tức thì các vi sợi cellulose.",
            "secondary_hazard": "Khói xơ bông phân tán cực nhanh làm tê liệt cảm biến quang học khói toàn khoang (optical sensor blindness) và sinh lượng lớn tro bay.",
            "decontamination": "Hút sạch tro xơ lơ lửng bằng máy lọc hạt tích điện tĩnh và thay cartridge lọc HEPA."
        },
        "en": {
            "action_1": "Cut section ventilation fans instantly; smother flame front using flame-retardant Kapton film.",
            "optimal_agent": "Water Mist Extinguisher augmented with surfactant agent to immediately penetrate and wet cellulosic microfibers.",
            "secondary_hazard": "Rapid dispersion of fibrous smoke blinds cabin optical smoke detectors and produces large clouds of airborne fly-ash.",
            "decontamination": "Vacuum airborne fibrous ash with electrostatic particulate scrubbers and replace HEPA filter cartridges."
        }
    },
    "MAT-08": {
        "name": "Heptane Droplet / Alkane Fuel",
        "vi": {
            "action_1": "Ngắt van cấp nhiên liệu dòng lỏng (Quick Disconnect shutoff); kích hoạt van hút chân không cục bộ của buồng thí nghiệm.",
            "optimal_agent": "Khí trơ N2 xả tràn thể tích kết hợp hạ nhiệt buồng đốt; CẤM DÙNG nước gây sôi nổ bắn tóe nhiên liệu lỏng ra môi trường xung quanh.",
            "secondary_hazard": "Hiệu ứng Ngọn Lửa Lạnh (Cool Flame) vô hình ở 600-800K tiếp tục tiêu thụ nhiên liệu sinh lượng CO khổng lồ không phát ra ánh sáng cảnh báo.",
            "decontamination": "Giám sát nồng độ CO bằng cảm biến điện hóa đa kênh; súc xả buồng đốt ra khoảng không vũ trụ trước khi mở cửa khoang."
        },
        "en": {
            "action_1": "Trigger liquid fuel Quick Disconnect emergency shutoff valve; open chamber vacuum vent valve to space.",
            "optimal_agent": "Total volume N2 inerting combined with chamber thermal quenching; PROHIBIT water which induces steam explosions and liquid droplet splatter.",
            "secondary_hazard": "Invisible Cool Flame regime active at 600-800K continues consuming fuel and generating massive toxic CO without visible light.",
            "decontamination": "Monitor CO concentrations via multichannel electrochemical sensors; vent chamber to space vacuum before hatch opening."
        }
    },
    "MAT-09": {
        "name": "Polycarbonate Lexan",
        "vi": {
            "action_1": "Tắt quạt thông gió hướng vào cửa sổ / kính vòm; di tản phi hành gia khỏi vùng nhỏ giọt nhựa nóng chảy lơ lửng.",
            "optimal_agent": "Khí CO2 xả chậm hoặc bọt dập màng nước AFFF chuyên dụng hàng không vũ trụ.",
            "secondary_hazard": "Hạt mồ hóng đen dày đặc (dense soot tendrils) kết tụ thành chuỗi dài trong vi trọng lực làm mù camera quan sát và tắc nghẽn bộ hấp phụ carbon trạm.",
            "decontamination": "Thay thế bộ lọc khói sơ cấp; lau chùi bề mặt thấu kính quang học bằng khăn chuyên dụng chống tĩnh điện."
        },
        "en": {
            "action_1": "Shut ventilation directed toward viewports/cupola; evacuate crew from area of free-floating molten polymer droplets.",
            "optimal_agent": "Low-velocity CO2 discharge or aerospace-grade AFFF water-film foam.",
            "secondary_hazard": "Dense black soot tendrils aggregate into long chains in zero-g, blinding optical cameras and clogging carbon scrubbers.",
            "decontamination": "Replace primary smoke filters; clean optical viewport lenses with antistatic lint-free aerospace wipes."
        }
    },
    "MAT-10": {
        "name": "Kapton HN Polyimide",
        "vi": {
            "action_1": "Tách tấm cách nhiệt MLI khỏi nguồn phóng điện hồ quang (arc tracking); ngắt tải điện cực dương pin mặt trời.",
            "optimal_agent": "Khí CO2 cục bộ hoặc N2; vật liệu tự dập tắt ngay khi ngắt hồ quang điện.",
            "secondary_hazard": "Carbon hóa tạo đường dẫn điện (conductive carbon char) có thể gây chập mạch thứ cấp nếu tái đóng điện.",
            "decontamination": "Cách ly đoạn cáp bị cháy; đo điện trở cách điện bằng Megohmmeter trước khi tái cấp điện."
        },
        "en": {
            "action_1": "Isolate MLI thermal blanket from electrical arc tracking path; decouple solar array positive power bus.",
            "optimal_agent": "Localized CO2 stream or gaseous N2; material self-extinguishes promptly once electrical arc is de-energized.",
            "secondary_hazard": "Carbonization generates conductive char tracks causing secondary short circuits upon electrical re-energization.",
            "decontamination": "Isolate damaged cable harness section; verify insulation resistance with a megohmmeter before restoring power."
        }
    }
}


BILINGUAL_RESEARCH_RECORDS = [
    {
        "experiment": "NASA SoFIE (Solid Fuel Ignition and Extinction)",
        "psi_id": "PSI-SOFIE-GEL-412",
        "pis": "Dr. David Urban (NASA GRC), Prof. Carlos Fernandez-Pello (UC Berkeley)",
        "facility": "ISS Combustion Integrated Rack (CIR)",
        "finding": {
            "vi": "Xác định hiện tượng nghịch lý: dưới dòng khí thông gió thấp (5-12 cm/s), tốc độ lan truyền ngọn lửa PMMA đạt đỉnh cục bộ cao hơn cả khi đốt trên mặt đất do không bị tổn hao nhiệt đối lưu.",
            "en": "Identified low-flow paradox: under low ventilation airflows (5-12 cm/s), PMMA flame spread rate reaches a local maximum exceeding terrestrial burning rates due to lack of convective heat loss."
        },
        "citation": "Urban, D. et al., 'The Solid Fuel Ignition and Extinction (SoFIE) Project', Combustion and Flame, Vol. 245, 2022."
    },
    {
        "experiment": "NASA Saffire (Spacecraft Fire Safety Demonstration)",
        "psi_id": "PSI-SAFFIRE-I-IV",
        "pis": "Dr. David Urban (NASA GRC), Dr. Gary Ruff (NASA GRC), Prof. James S. T'ien (CWRU)",
        "facility": "Northrop Grumman Cygnus Spacecraft (Post-ISS Unberthing)",
        "finding": {
            "vi": "Thực nghiệm đốt mẫu vải khổ lớn (0.4m x 1.0m) đầu tiên trong lịch sử hàng không vũ trụ. Chứng minh ngọn lửa trong tàu vũ trụ cháy bền bỉ hơn và lan rộng hơn nhiều so với dự báo mặt đất.",
            "en": "First large-scale fabric burn tests (0.4m x 1.0m) in aerospace history inside Cygnus cargo ships. Proved low-g fires grow significantly larger and persist at lower oxygen levels than terrestrial 1g tests predict."
        },
        "citation": "Ruff, G. A., Urban, D. L., et al., 'Large-Scale Fire Safety Experiments in Space: Saffire-I through IV', Proc. Combust. Inst., 2020."
    },
    {
        "experiment": "NASA BASS & BASS-II (Burning and Suppression of Solids)",
        "psi_id": "PSI-BASS-II-P849",
        "pis": "Dr. Sandra Olson (NASA GRC), Paul Ferketič (ZIN Technologies)",
        "facility": "ISS Microgravity Science Glovebox (MSG)",
        "finding": {
            "vi": "Lập bản đồ giới hạn dập tắt (Extinction Limit) cho Nomex, Silicone RTV và PMMA. Xác định nồng độ oxy giới hạn (LOI) giảm mạnh trong môi trường vi trọng lực.",
            "en": "Mapped extinction boundaries for Nomex, Silicone RTV, and PMMA in the ISS MSG. Established that the Limiting Oxygen Index (LOI) shifts downward in microgravity under moderate airflow."
        },
        "citation": "Olson, S. L., & Ferketič, P., 'Extinction Limits of Solid Fuel Combustion in Microgravity', Combust. Flame, Vol. 162, 2015."
    },
    {
        "experiment": "NASA FLEX & FLEX-2 (Flame Extinction Experiment)",
        "psi_id": "PSI-FLEX-ICE-102",
        "pis": "Prof. Forman A. Williams (UC San Diego), Dr. Vedat Nayagam (NCSU)",
        "facility": "ISS Multi-User Droplet Combustion Apparatus (MDCA)",
        "finding": {
            "vi": "Phát hiện hiện tượng 'Ngọn Lửa Lạnh' (Cool Flames) hình cầu trong giọt alkane tự do. Sau khi ngọn lửa nóng bị dập tắt, phản ứng oxy hóa nhiệt độ thấp (600K) tiếp tục tiêu thụ nhiên liệu và sinh CO vô hình.",
            "en": "Discovered spherical 'Cool Flames' in free-floating alkane droplets. After hot flame extinction, low-temperature oxidation (600-800K) continues invisibly, consuming fuel and generating high CO."
        },
        "citation": "Williams, F. A., Nayagam, V., et al., 'Spherical Cool Flames in Microgravity', Science, Vol. 338, Iss. 6114, pp. 1593-1596, 2012."
    },
    {
        "experiment": "NASA ACME (BRE, CFI-G 85% O₂, E-FIELD Flames)",
        "psi_id": "PSI-ACME-CIR-401",
        "pis": "Prof. J. Quintiere (UMD), Prof. R. Axelbaum (WUSTL), Prof. D. Dunn-Rankin (UCI), Dr. D. Stocker (NASA GRC)",
        "facility": "ISS Combustion Integrated Rack (CIR) - Modular ACME Hardware",
        "finding": {
            "vi": "Thực hiện 6 thí nghiệm lửa khí trên cùng bộ phần cứng module ACME trong CIR: BRE giả lập độ cháy vật liệu rắn bằng nhiên liệu khí; CFI-G thử nghiệm nồng độ oxy cao nhất (lên tới 85% O2) tạo ngọn lửa lộn ngược (inside-out flame); E-FIELD Flames dùng điện trường tác động lên ion lửa để giả lập trọng lực bán phần (do PSI hiện chưa có dữ liệu trọng lực bán phần thực tế cho tới khi có sứ mệnh LUCI và FM2).",
            "en": "Six gaseous flame experiments using shared modular ACME hardware in the CIR: BRE emulated solid material flammability using gas burners; CFI-G tested up to 85% O2 creating inside-out spherical flames; E-FIELD Flames used electric fields on flame ions to mimic partial gravity (bridging the gap until future lunar LUCI and FM2 partial-g data enter PSI)."
        },
        "citation": "Stocker, D. P., Quintiere, J. G., Axelbaum, R. L., et al., 'Advanced Combustion via Microgravity Experiments (ACME)', NASA/TM-2022-0008543, 2022."
    },
    {
        "experiment": "NASA SPICE, SLICE, SAME/SAME-R & DAFT/DAFT-2",
        "psi_id": "PSI-MSG-FLOW-512",
        "pis": "Dr. David L. Urban (NASA GRC), Dr. Gary A. Ruff (NASA GRC), Dr. Sandra L. Olson (NASA GRC)",
        "facility": "ISS Microgravity Science Glovebox (MSG) - Modular SPICE Fan-Driven Flow Duct",
        "finding": {
            "vi": "BASS, BASS-II, SPICE (Smoke Point In Co-flow Experiment) và SLICE (Structure & Liftoff In Combustion Experiment) dùng chung ống dẫn quạt gió của SPICE trong buồng MSG cho cả nhiên liệu rắn và khí. Đồng thời, thiết bị đo khói từ SAME/SAME-R đã được tái sử dụng để đo bụi trong DAFT & DAFT-2, đặt nền móng cho đầu báo khói thông minh và trang bị lính cứu hỏa trên Trái Đất.",
            "en": "BASS, BASS-II, SPICE (Smoke Point In Co-flow Experiment), and SLICE (Structure & Liftoff In Combustion Experiment) shared the SPICE fan-driven flow duct inside the MSG for solid and gaseous fuels. Additionally, smoke detection hardware from SAME/SAME-R was repurposed for dust monitoring in DAFT & DAFT-2, driving Earth spin-offs in smart smoke detectors and firefighter gear."
        },
        "citation": "Urban, D. L., Ruff, G. A., Olson, S. L., 'Spacecraft Fire Detection and Flow Duct Combustion in MSG', NASA/TP-2023-221450, 2023."
    },
    {
        "experiment": "NASA Flammability Standard (NASA-STD-6001B Test 1)",
        "psi_id": "NASA-STD-6001B-REV-B",
        "pis": "NASA Materials & Processes Technical Branch (MSFC / JSC / WSTF)",
        "facility": "NASA White Sands Test Facility (WSTF)",
        "finding": {
            "vi": "Quy định thử nghiệm bắt buộc lan truyền lửa hướng lên cho vật liệu cabin. Cảnh báo vật liệu đạt chuẩn tại 21% O2 mặt đất trở nên cực kỳ nguy hiểm trong khí quyển Artemis (34% O2, 56.5 kPa).",
            "en": "Mandatory upward flame propagation qualification standard. Proves materials certified at 21% O2 become highly flammable in enriched exploration atmospheres (Artemis 34% O2, 56.5 kPa)."
        },
        "citation": "NASA Technical Standard NASA-STD-6001B, 'Flammability, Odor, Offgassing Requirements for Spacecraft Habitats', NASA MSFC, 2021."
    }
]


def get_i18n(lang: str = "vi"):
    return TRANSLATIONS.get(lang, TRANSLATIONS["vi"])


def get_protocol(material_id: str, lang: str = "vi"):
    data = BILINGUAL_SUPPRESSION_DATABASE.get(material_id)
    if data and lang in data:
        return data[lang]
    elif data and "vi" in data:
        return data["vi"]
    else:
        if lang == "en":
            return {
                "action_1": "Immediately shut down sectional HVAC ventilation within 3 seconds to eliminate forced convective oxidizer feed.",
                "optimal_agent": "Fine Water Mist with N2 propellant or Total Flooding CO2; STRICTLY FORBID high-velocity single water jets.",
                "secondary_hazard": "Toxic CO gas and fine aerosol particulate off-gassing; mandatory crew donning of PBE breathing apparatus.",
                "decontamination": "Engage ECLSS smoke scrubber loops and verify absence of trace toxic gases before doffing masks."
            }
        else:
            return {
                "action_1": "Ngắt quạt thông gió phân khu trong 3 giây đầu tiên để triệt tiêu dòng cấp oxy cưỡng bức.",
                "optimal_agent": "Fine Water Mist với khí N2 đẩy hoặc bình CO2 xả tràn; CẤM dùng tia nước áp lực cao đơn lẻ.",
                "secondary_hazard": "Khí độc CO và khói hạt mịn; bắt buộc phi hành gia đeo mặt nạ dưỡng khí PBE.",
                "decontamination": "Chạy hệ thống lọc khói ECLSS và kiểm tra nồng độ khí độc trước khi tháo mặt nạ."
            }


def get_morphology_regime_info(regime_code: str, gravity_g: float, airflow_cm_s: float, oxygen_pct: float, lang: str = "vi"):
    if regime_code == "EXTINGUISHED":
        if lang == "vi":
            regime_name = "DẬP TẮT HOÀN TOÀN (EXTINGUISHED)"
            morph_desc = (
                "TRẠNG THÁI AN TOÀN: Nồng độ oxy hoặc tốc độ thông gió nằm ngoài giới hạn duy trì ngọn lửa "
                "(Oxy thấp hơn MOC hiệu dụng hoặc dập tắt do bức xạ / thổi tắt đối lưu). "
                "Không có phản ứng oxy hóa hoạt động; nhiệt độ ở mức môi trường khoang (~300K)."
            )
            soot_fraction = "0.0 (Không có phản ứng cháy)"
        else:
            regime_name = "COMPLETE EXTINCTION (EXTINGUISHED)"
            morph_desc = (
                "SAFE QUENCHED STATE: Ambient cabin oxygen or ventilation flow is outside the flammability envelope "
                "(O2 below effective MOC or quenched via radiative heat loss / convective blowoff). "
                "Zero ongoing chemical combustion; temperature equals ambient cabin background (~300K)."
            )
            soot_fraction = "0.0 (Zero Active Combustion)"
        return regime_name, morph_desc, soot_fraction
    elif regime_code == "BUOYANT_TEARDROP":
        if lang == "vi":
            regime_name = "Hình Giọt Nước Đối Lưu do Lực Nổi (1.0g Mặt Đất)"
            morph_desc = (
                "Lực nổi tự nhiên mạnh mẽ (V_buoyant ~ 25 cm/s) kéo các sản phẩm cháy nóng lên trên tạo thành cột khói hình giọt nước "
                "thuôn dài hẹp. Dòng đối lưu cuốn oxy mạnh mẽ vào tâm lửa, tạo ra vệt bồ hóng phát sáng màu vàng cam bức xạ nhiệt mạnh trong dải hồng ngoại."
            )
            soot_fraction = "Cao (1.2 × 10⁻⁶)"
        else:
            regime_name = "Buoyancy-Driven Convective Teardrop (1.0g)"
            morph_desc = (
                "Strong natural buoyant updraft (V_buoyant ~ 25 cm/s) draws hot combustion gases upward into a narrow, "
                "elongated teardrop plume. Rapid convective entrainment feeds oxygen and creates an incandescent yellow-orange "
                "soot trail radiating heavily in the infrared spectrum."
            )
            soot_fraction = "High (1.2 × 10⁻⁶)"
    elif regime_code == "SPHERICAL_DIFFUSION":
        if lang == "vi":
            regime_name = "Hình Cầu Xanh Lam Thuần Khuếch Tán (0.0g Vi Trọng Lực)"
            morph_desc = (
                "Sự biến mất hoàn toàn của lực nổi khiến quá trình vận chuyển oxy chỉ còn dựa vào khuếch tán phân tử 3D đẳng hướng. "
                "Ngọn lửa chuyển thành lớp vỏ hình cầu êm đềm, đối xứng hoàn hảo. Nhiệt độ thấp hơn (~1380K), "
                "ngăn chặn quá trình tinh thể hóa bồ hóng carbon và phát ra ánh sáng xanh lam thuần khiết từ các gốc kích thích CH* và C2*."
            )
            soot_fraction = "Không đáng kể (< 0.05 × 10⁻⁶, Không bồ hóng)"
        else:
            regime_name = "Diffusion-Limited Pure Blue Sphere (0.0g)"
            morph_desc = (
                "Complete absence of buoyancy causes oxidizer transport to rely purely on isotropic 3D molecular diffusion. "
                "The flame assumes a calm, perfectly symmetrical spherical shell. Temperatures remain cooler (~1380K), "
                "preventing carbon soot crystallization and emitting pure blue chemiluminescence from excited CH* and C2* radicals."
            )
            soot_fraction = "Negligible (< 0.05 × 10⁻⁶, Soot-Free)"
    else:
        if lang == "vi":
            regime_name = f"Hình Bán Cầu Bành Trướng Nguy Hiểm ({gravity_g:.2f}g Trọng Lực Một Phần)"
            morph_desc = (
                "HIỂM HỌA KHÔNG GIAN CỰC NGUY HIỂM: Trong trọng lực một phần (Mặt Trăng 0.16g, Sao Hỏa 0.38g), lực nổi quá yếu để tạo thành cột khói đối lưu thẳng đứng, "
                "nhưng đủ mạnh để phá vỡ tính đối xứng hình cầu. Khí cháy nóng bành trướng ngang thành hình vòm bán cầu với diện tích tiếp xúc chân lửa loang rộng, "
                "làm tăng diện tích bắt cháy bề mặt các cấu trúc xung quanh lên tới 240%!"
            )
            soot_fraction = "Trung bình (0.75 × 10⁻⁶, Màn khói bồ hóng lơ lửng)"
        else:
            regime_name = f"Hazardous Expanding Hemispherical Dome ({gravity_g:.2f}g Partial Gravity)"
            morph_desc = (
                "CRITICAL SPACE HAZARD: In partial gravity (Moon 0.16g, Mars 0.38g), buoyant forces are too weak to form "
                "a vertical convective chimney, yet strong enough to destabilize spherical symmetry. Hot combustion gases "
                "mushroom laterally into an expanding hemispherical dome with a broad contact footprint, severely increasing "
                "the surface ignition area on surrounding spacecraft structures by up to 240%."
            )
            soot_fraction = "Moderate (0.75 × 10⁻⁶, Lingering Smoke Blanket)"
            
    return regime_name, morph_desc, soot_fraction


# ==============================================================================
# FEATURE 7: AEROSPACE ACRONYM TOOLTIP LIBRARY (WCAG 2.1 AA)
# ==============================================================================
ACRONYM_DICTIONARY = {
    "Da": {
        "term": {
            "en": "Damköhler Number",
            "vi": "Số Damköhler"
        },
        "full_abbr": "Da",
        "description": {
            "en": "Ratio of fluid flow timescale to chemical reaction timescale. When Da < 1, high airflow blows out the flame (convective blowoff). When Da >> 1, combustion is vigorous and diffusion-controlled.",
            "vi": "Tỷ số giữa thời gian đặc trưng dòng chảy và thời gian phản ứng hóa học. Khi Da < 1, gió mạnh thổi tắt ngọn lửa (blowoff). Khi Da >> 1, phản ứng cháy mãnh liệt và phụ thuộc khuếch tán."
        },
        "formula": "Da = τ_flow / τ_chem ∝ (1/v_eff) · (O₂/21.0)^1.2 · (P/P₀)^0.8"
    },
    "Re": {
        "term": {
            "en": "Reynolds Number",
            "vi": "Số Reynolds"
        },
        "full_abbr": "Re",
        "description": {
            "en": "Ratio of inertial forces to viscous forces in fluid flow. Spacecraft cabin ventilation (5–20 cm/s) maintains smooth, laminar boundary layer flow (Re < 500), avoiding turbulent flame disturbance.",
            "vi": "Tỷ số giữa lực quán tính và lực nhớt trong dòng chảy. Hệ thống thông gió cabin tàu vũ trụ (5–20 cm/s) duy trì dòng chảy tầng êm (Re < 500), không gây xáo trộn cuộn xoáy ngọn lửa."
        },
        "formula": "Re = (v · L) / ν"
    },
    "Pe": {
        "term": {
            "en": "Péclet Number",
            "vi": "Số Péclet"
        },
        "full_abbr": "Pe",
        "description": {
            "en": "Ratio of advective transport rate to molecular thermal/mass diffusion rate (Pe = Re · Pr). Governs the peak burning rate at low ventilation velocities (Low-Flow Ventilation Paradox) in microgravity.",
            "vi": "Tỷ số giữa tốc độ đối lưu cưỡng bức và tốc độ khuếch tán nhiệt/khối phân tử (Pe = Re · Pr). Quyết định nghịch lý cháy đỉnh ở vận tốc gió thấp (Ventilation Paradox) trong vi trọng lực."
        },
        "formula": "Pe = (v · L) / α"
    },
    "Ri": {
        "term": {
            "en": "Richardson Number",
            "vi": "Số Richardson"
        },
        "full_abbr": "Ri",
        "description": {
            "en": "Ratio of buoyant natural convection to forced flow (Ri = Gr / Re²). In microgravity (0g), Ri = 0. In Moon (0.16g) and Mars (0.38g) partial gravity, Ri ~ 0.1–5 causes flame contact footprint to mushroom laterally by up to 240%.",
            "vi": "Tỷ số giữa lực nổi đối lưu tự nhiên và dòng chảy cưỡng bức (Ri = Gr / Re²). Trong 0g, Ri = 0. Ở Mặt Trăng (0.16g) và Sao Hỏa (0.38g), Ri ~ 0.1–5 khiến ngọn lửa bè rộng thành bán cầu nguy hiểm (diện tích tiếp xúc tăng 240%)."
        },
        "formula": "Ri = Gr / Re² = (g · β · ΔT · L) / v²"
    },
    "SFRS": {
        "term": {
            "en": "Spacecraft Fire Risk Score",
            "vi": "Điểm Nguy cơ Cháy Tàu Vũ trụ"
        },
        "full_abbr": "SFRS",
        "description": {
            "en": "NASA composite flammability safety metric (0–100) combining oxygen margin (ΔO₂%), flame spread rate (V_spread), heat of combustion (HOC), and ventilation regime. Scores > 85 indicate critical hazard requiring ECLSS HVAC isolation.",
            "vi": "Thang điểm an toàn cháy tổng hợp của NASA (0–100) kết hợp biên độ oxy (ΔO₂%), tốc độ lan truyền ngọn lửa, nhiệt lượng cháy (HOC) và hiểm họa dòng thông gió. Điểm > 85 là mức nguy cấp yêu cầu ngắt thông gió ECLSS."
        },
        "formula": "SFRS = f(ΔO₂, V_spread, HOC, P, v)"
    },
    "MOC": {
        "term": {
            "en": "Maximum Oxygen Concentration",
            "vi": "Nồng độ Oxy Cực đại Tự tắt"
        },
        "full_abbr": "MOC",
        "description": {
            "en": "Lowest volumetric oxygen concentration supporting sustained combustion (NASA-STD-6001B Test 1). In microgravity low-flow conditions, effective MOC drops by 2–4%, allowing materials certified safe on Earth to ignite in space.",
            "vi": "Nồng độ oxy thể tích thấp nhất duy trì sự lan truyền đám cháy (NASA-STD-6001B Thí nghiệm 1). Trong vi trọng lực gió chậm, MOC hiệu dụng giảm 2–4%, khiến vật liệu an toàn trên Trái Đất có thể bốc cháy trong vũ trụ."
        },
        "formula": "MOC_eff = MOC_1g - Δ_env"
    },
    "ΔO2%": {
        "term": {
            "en": "Oxygen Safety Margin",
            "vi": "Biên độ An toàn Oxy"
        },
        "full_abbr": "ΔO₂%",
        "description": {
            "en": "Difference between ambient cabin oxygen concentration and the material's extinction threshold: ΔO₂% = Cabin_O₂ - MOC_eff. Negative values indicate self-extinguishment; positive values indicate sustained fire hazard.",
            "vi": "Chênh lệch giữa nồng độ oxy khoang thực tế và ngưỡng dập tắt hiệu dụng của vật liệu: ΔO₂% = O₂_khoang - MOC_eff. Giá trị âm thể hiện đám cháy tự dập tắt; giá trị dương cảnh báo nguy cơ cháy duy trì."
        },
        "formula": "ΔO₂% = O₂_cabin - MOC_eff"
    }
}


def _sanitize_tooltip_text(text: str) -> str:
    """Escape HTML/attribute metacharacters while preserving explicit <b>/</b> emphasis tags."""
    if text is None:
        return ""
    escaped = html.escape(str(text), quote=True)
    return escaped.replace("&lt;b&gt;", "<b>").replace("&lt;/b&gt;", "</b>")


def render_acronym_tooltip(acronym_key: str, lang: str = "en", display_text: str | None = None) -> str:
    """
    Renders an accessible, hoverable/tap-friendly HTML acronym tooltip badge.
    Complies with WCAG 2.1 AA keyboard focus, screen reader, and XSS sanitization standards.
    """
    if not acronym_key or not isinstance(acronym_key, str):
        return _sanitize_tooltip_text(display_text) if display_text is not None else ""

    key = acronym_key.strip()
    if key in ["Delta_O2", "dO2", "delta_o2", "ΔO2", "ΔO2%", "delta_o2_pct", "Delta_O2_pct"]:
        key = "ΔO2%"
    info = ACRONYM_DICTIONARY.get(key)
    if not info:
        raw_fallback = display_text if display_text is not None else acronym_key
        return _sanitize_tooltip_text(raw_fallback)

    term_dict = info.get("term", {})
    term_name = term_dict.get(lang, term_dict.get("en", key))
    desc_dict = info.get("description", {})
    desc = desc_dict.get(lang, desc_dict.get("en", ""))
    formula = info.get("formula", "")
    disp = _sanitize_tooltip_text(display_text) if display_text is not None else _sanitize_tooltip_text(info.get("full_abbr", key))

    safe_key = html.escape(str(key), quote=True)
    safe_term = html.escape(str(term_name), quote=True)
    safe_desc = html.escape(str(desc), quote=True)
    safe_formula = _sanitize_tooltip_text(formula)
    formula_html = f'<div class="nasa-tt-formula">{safe_formula}</div>' if formula else ""

    return (
        f'<abbr class="nasa-acronym-abbr" tabindex="0" aria-label="{safe_term}: {safe_desc}" title="{safe_term} — {safe_desc}">'
        f'<span class="nasa-acronym-text">{disp}</span>'
        f'<span class="nasa-tt-card" role="tooltip">'
        f'<span class="nasa-tt-badge">{safe_key}</span>'
        f'<span class="nasa-tt-title">{safe_term}</span>'
        f'<span class="nasa-tt-desc">{safe_desc}</span>'
        f'{formula_html}'
        f'</span>'
        f'</abbr>'
    )

