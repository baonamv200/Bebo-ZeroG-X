# Kịch Bản Quay Video Pitch 2 Phút (120 Giây)
## NASA Space Apps Challenge 2026 // Dự án: Flames in Freefall
**Đội thi:** Bebo ZeroG-X (Trường THPT FPT)  
**Trưởng nhóm & Trình bày:** Vũ Bảo Nam  
**Thành viên:** Đỗ Duy Nam • Lương Đức Tùng • Trịnh Đức Anh  
**Thời lượng chuẩn:** Chính xác 120 giây (Tuân thủ nghiêm ngặt quy định 2 phút của NASA)

---

### TỔNG QUAN PHÂN BỔ THỜI GIAN (STORYBOARD TIMELINE)

```text
[00:00 - 00:15] (15s) : Hook & Giới thiệu bài toán ác mộng của ngọn lửa vi trọng lực
[00:15 - 00:40] (25s) : Kho dữ liệu NASA PSI & Nghịch lý thông gió (Ventilation Paradox)
[00:40 - 01:10] (30s) : Live Demo sản phẩm Flames in Freefall (Streamlit & Plotly 3D)
[01:10 - 01:40] (30s) : Test Case kiểm chứng thực tế & Hệ thống AI RAG cứu hỏa khẩn cấp
[01:40 - 02:00] (20s) : Tác động thực tiễn Artemis/Mars, Mã nguồn mở & Lời chào kết
```

---

### KỊCH BẢN CHI TIẾT TỪNG GIÂY

#### 🎬 PHÂN CẢNH 1: MỞ ĐẦU ẤN TƯỢNG (00:00 – 00:15 | 15 giây)
* **Hình ảnh trên màn hình (Visual):** 
  * Cảnh quay tác giả Vũ Bảo Nam tự tin trước camera, nền phía sau là màn hình hiển thị logo NASA Space Apps Challenge 2026 và giao diện app đang chạy.
  * Góc dưới màn hình hiện Title Card: *Vũ Bảo Nam – Team Lead & Architect, Đội Bebo ZeroG-X (THPT FPT)*.
* **Lời thoại (Speaker Audio - Tiếng Việt):**
  > *"Kính chào Ban giám khảo NASA Space Apps Challenge 2026! Tôi là Vũ Bảo Nam. Bạn có biết: Trong không gian, hỏa hoạn là cơn ác mộng kinh hoàng nhất của phi hành đoàn, bởi ngọn lửa không hề bốc lên trên như ở Trái Đất, mà cuộn tròn thành khối cầu xanh tĩnh lặng và cháy âm ỉ không thể nhìn thấy bằng mắt thường!"*
* **Phụ đề tiếng Anh (English Subtitles):**
  > *"Greetings NASA Space Apps Challenge judges! I am Vu Bao Nam. In space, fire is an astronaut's ultimate nightmare—because without buoyancy, flames turn into silent, soot-free blue spheres that smolder invisibly!"*

---

#### 🎬 PHÂN CẢNH 2: NGUỒN DỮ LIỆU NASA PSI & NGHỊCH LÝ THÔNG GIÓ (00:15 – 00:40 | 25 giây)
* **Hình ảnh trên màn hình (Visual):** 
  * Chuyển cảnh sang màn hình máy tính (Screen Recording): Lướt nhanh qua các thư mục dữ liệu `data/sofie_pmma_burn_rates.csv`, `data/saffire_pressure_oxygen.csv` và hình ảnh buồng đốt CIR trên trạm ISS.
  * Xuất hiện sơ đồ đối chiếu: Ngọn lửa Trái Đất (1g) vs Ngọn lửa Vi trọng lực (0g).
* **Lời thoại (Speaker Audio):**
  > *"Khai thác nguồn dữ liệu thực nghiệm quý giá từ NASA Physical Sciences Informatics – gồm các sứ mệnh SoFIE trên trạm ISS và Saffire trên tàu Cygnus – tôi nhận ra một 'Nghịch lý thông gió' chết người: Hệ thống quạt gió bắt buộc trong tàu vũ trụ vô tình biến thành nguồn thổi oxy liên tục, kích hoạt đám cháy bùng phát dữ dội ở nồng độ oxy thấp hơn nhiều so với mặt đất!"*
* **Phụ đề tiếng Anh:**
  > *"Mining experimental data from NASA Physical Sciences Informatics—including SoFIE on the ISS and Saffire on Cygnus—I modeled the lethal 'Ventilation Paradox', where mandatory cabin fans supply forced oxidizer, causing materials to burn at far lower oxygen thresholds than on Earth."*

---

#### 🎬 PHÂN CẢNH 3: LIVE DEMO BẢNG ĐIỀU KHIỂN & PLOTLY 3D (00:40 – 01:10 | 30 giây)
* **Hình ảnh trên màn hình (Visual):** 
  * Quay màn hình trực tiếp Web App đang chạy mượt mà:
  * Thao tác chuột gạt thanh trượt **Gravity (0.16g)**, **Oxygen (34%)**, **Pressure (56.5 kPa)**, **Airflow (15 cm/s)**.
  * Hiển thị biểu đồ Plotly 3D ngọn lửa hình cầu xoay lật 360 độ và đồng hồ đo rủi ro **Space Fire Risk Score (SFRS)** nhảy số lên `78.5 / 100 [CRITICAL RISK]`.
* **Lời thoại (Speaker Audio):**
  > *"Để giải quyết bài toán này, tôi đã tự tay xây dựng 'Flames in Freefall' – nền tảng điều hành an toàn hỏa hoạn vận hành bởi động cơ toán lý Bebo Ignis-0G. Chỉ với vài thao tác kéo thanh trượt môi trường hoặc chọn preset trạm Mặt Trăng Artemis hay Sao Hỏa, hệ thống lập tức tái hiện ngọn lửa 3D nhiệt độ cao và tính toán điểm nguy cơ SFRS theo thời gian thực!"*
* **Phụ đề tiếng Anh:**
  > *"To solve this, I engineered 'Flames in Freefall', powered by the Bebo Ignis-0G physics engine. With dynamic parameter sweeps across Artemis Lunar and Mars habitats, the dashboard simulates 3D thermal flame morphology and evaluates the Space Fire Risk Score in real time!"*

---

#### 🎬 PHÂN CẢNH 4: THỬ NGHIỆM THỰC CHỨNG & AI RAG CỨU HỎA (01:10 – 01:40 | 30 giây)
* **Hình ảnh trên màn hình (Visual):** 
  * Màn hình mở tab tra cứu tài liệu **Ask NASA PSI Docs**: Nhập câu hỏi, hệ thống trả lời ngay trong 4ms kèm trích dẫn chuẩn `NASA-STD-6001B`.
  * Highlight bảng quy chuẩn dập lửa: Biểu tượng cấm vòi nước áp lực cao, biểu tượng kích hoạt sương nước siêu mịn Fine Water Mist ($< 50\ \mu\text{m}$).
* **Lời thoại (Speaker Audio):**
  > *"Thử nghiệm thực tế với nhựa PMMA trong khoang Artemis: Điểm rủi ro đạt 78.5 mức Báo động đỏ. Hệ thống AI RAG tích hợp sẵn sàng đưa ra phương án dập lửa khẩn cấp: Tuyệt đối cấm phun tia nước áp lực cao để tránh làm bắn tung tóe nhựa nóng chảy; bắt buộc ngắt quạt gió cabin tại T+0 giây và kích hoạt hệ thống sương nước siêu mịn để dập tắt ngọn lửa."*
* **Phụ đề tiếng Anh:**
  > *"Testing PMMA in an Artemis cabin yields a Critical 78.5 SFRS score. Our built-in RAG assistant instantly issues emergency guidance: strictly prohibit water jets to prevent molten polymer splatter, isolate cabin HVAC at T+0s, and deploy Nitrogen-propelled Fine Water Mist."*

---

#### 🎬 PHÂN CẢNH 5: Ý NGHĨA SỨ MỆNH & KẾT LUẬN (01:40 – 02:00 | 20 giây)
* **Hình ảnh trên màn hình (Visual):** 
  * Camera quay trở lại tác giả Vũ Bảo Nam, bên cạnh là mã QR dẫn đến GitHub `github.com/baonamv200/nasa` và link web trực tuyến.
  * Hiện logo NASA Space Apps Challenge 2026, dòng chữ cảm ơn và chữ ký số.
* **Lời thoại (Speaker Audio):**
  > *"Flames in Freefall bảo vệ sinh mạng phi hành đoàn cho sứ mệnh Artemis và tương lai đa hành tinh của nhân loại. Toàn bộ mã nguồn mở đã sẵn sàng tại github.com/baonamv200/nasa. Tôi là Vũ Bảo Nam. Cảm ơn Ban giám khảo đã lắng nghe!"*
* **Phụ đề tiếng Anh:**
  > *"Flames in Freefall safeguards astronaut lives for Artemis and our multi-planetary future. Open source code is available at github.com/baonamv200/nasa. I am Vu Bao Nam. Thank you for your consideration!"*

---

### 💡 MẸO QUAY VIDEO ĐỂ ĐẠT ĐIỂM TỐI ĐA (PITCH TIPS):
1. **Âm thanh & Ánh sáng:** Dùng micro cài áo hoặc tai nghe có mic chống ồn; chiếu đèn sáng vào mặt, ánh mắt nhìn thẳng vào ống kính máy quay.
2. **Tốc độ nói:** Tự tin, dứt khoát, hào hứng nhưng không nói quá nhanh (khoảng 130–140 từ/phút).
3. **Chèn Screen Recording:** Khi quay demo app, phóng to các thanh trượt và hình ngọn lửa 3D để BGK nhìn thấy rõ sự chuyển động.
4. **Đồng hồ bấm giờ:** Đặt đồng hồ đếm ngược trước mặt để đảm bảo kết thúc trong khoảng 1 phút 55 giây đến 1 phút 59 giây (tuyệt đối không để vượt quá 120 giây).

