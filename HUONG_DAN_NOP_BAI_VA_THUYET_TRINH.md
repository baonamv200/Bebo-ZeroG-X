# Hướng Dẫn Nộp Bài & Kịch Bản Thuyết Trình NASA Space Apps Hà Nội 2026
**Dự án:** Flames in Freefall — SI-Powered Spacecraft Fire Safety Dashboard  
**Đội thi:** Bebo ZeroG-X (Trường THPT FPT, Hà Nội)  
**Địa điểm thi:** Trường THCS Trưng Vương, 26 Hàng Bài, Hoàn Kiếm, Hà Nội / Zoom Meeting ID `940 8456 9142`  
**Giấy phép mã nguồn mở:** Dual-Licensed under Apache License 2.0 / MIT License *(mặc định Apache License 2.0 theo Quy định số 7 của SEPA — xem [LICENSE](file:///e:/nasa/LICENSE))*

---

## ⏰ 1. CÁC MỐC THỜI GIAN QUAN TRỌNG

| Thời gian | Sự kiện | Lưu ý & Hành động |
| :--- | :--- | :--- |
| **09:00, Thứ Bảy 14/11** | Khai mạc & Mở cổng nộp bài | Đăng nhập [spaceappschallenge.org](https://www.spaceappschallenge.org/), vào trang đội, chọn thử thách. |
| **08:00 – 09:00, CN 15/11** | **Chiến thuật nộp sớm của BTC** | **BẤM SUBMIT NGAY BẢN ĐẦU TIÊN** (dù chưa hoàn chỉnh). Sau đó nhấn `Edit` sửa thoải mái đến trước 11:00. |
| **11:00, Chủ nhật 15/11** | **HẠN CHÓT NỘP BÀI XÉT GIẢI HÀ NỘI** | Cổng nộp bài xét giải Hà Nội đóng. Nộp sau 11:00 chỉ được tính xét giải toàn cầu. |
| **11:00 – 15:00, CN 15/11** | Ban giám khảo chấm thi | Có mặt trước phòng chấm hoặc vào Zoom trước 10 phút. |
| **16:30, Chủ nhật 15/11** | Bế mạc & Trao giải | Trao các giải thưởng Hà Nội và công bố các đội Global Nominee. |
| **23:59, Chủ nhật 15/11** | Hạn nộp toàn cầu của NASA | Đội được tiếp tục cập nhật và hoàn thiện lần cuối cho giám khảo quốc tế. |

---

## 🔍 2. CÁC LƯU Ý KỸ THUẬT QUAN TRỌNG TỪ BAN TỔ CHỨC SEPA

1. **Về Slide hoặc Video Demo (Ô Project Demo):**
   - **Slide thuyết trình (`Flames_in_Freefall_Presentation.pptx`):** Tối đa **7 trang (tính cả trang bìa)** và **100% bằng tiếng Anh** theo quy định SEPA.
   - **Video demo (`VIDEO_PITCH_SCRIPT_2MIN.md`):** Tối đa **30 giây** theo kịch bản chính 30s live-demo quay trực tiếp ứng dụng đang chạy, **bắt buộc có phụ đề tiếng Anh & trích dẫn dữ liệu NASA PSI** (kèm kịch bản pitch 2 phút tùy chọn làm bản backup).
   - **Quyền truy cập đường link:** Mọi link (Google Drive, YouTube, GitHub, Streamlit) **phải đặt ở chế độ "Bất kỳ ai có đường liên kết" (Anyone with the link can view)**.
   - *Mẹo:* Mở thử link bằng cửa sổ trình duyệt ẩn danh (Incognito) để kiểm tra người ngoài xem được mà không cần đăng nhập.

2. **Về Khai báo Sử dụng AI (Ô Use of AI):**
   - NASA cho phép và khuyến khích dùng AI, nhưng bắt buộc phải minh bạch.
   - Tuyệt đối không để trống hoặc ghi chung chung. Bài nộp thiếu nguồn trích dẫn hoặc giấu thông tin AI có thể bị thu hồi đề cử/giải thưởng.
   - Đã có sẵn mẫu khai báo tiếng Anh chuẩn mực trong file [NASA_SUBMISSION_CHECKLIST.md](file:///e:/nasa/NASA_SUBMISSION_CHECKLIST.md).

3. **Về Tài nguyên Dữ liệu NASA (Ô NASA Data):**
   - Bắt buộc có ít nhất 1 bộ dữ liệu của NASA kèm đường link URL cụ thể.
   - Đã chuẩn bị sẵn link trực tiếp tới NASA PSI, SoFIE, Saffire, BASS-II và chuẩn NASA-STD-6001B.

4. **Kiểm tra Thành viên (Tab Members):**
   - Đảm bảo tất cả 4 thành viên (Vũ Bảo Nam, Đỗ Duy Nam, Lương Đức Tùng, Trịnh Đức Anh) đều đã đăng ký điểm thi **Hanoi, Vietnam** và có tên ở tab Members của đội trước khi cổng nộp bài đóng. Sau hạn chót sẽ không thể thêm người.

5. **Tuân thủ Bản quyền, Nhãn hiệu & Kiểm thử Kỹ thuật:**
   - **Giấy phép kép (SEPA Rule 7):** Dự án áp dụng **Dual-Licensed under Apache License 2.0 / MIT License** ([LICENSE](file:///e:/nasa/LICENSE)), trong đó **Apache License 2.0** là giấy phép mặc định cho bài dự thi NASA Space Apps Challenge 2026.
   - **Tuân thủ giao diện & kỹ thuật:** Đã thay thế hoàn toàn logo NASA Meatball ngoài (Wikimedia) bằng **huy hiệu Bebo Ignis-0G Mission Patch dạng inline SVG tự chứa**, nâng tương phản chữ đạt chuẩn **WCAG AA `#94A3B8`**, hỗ trợ deep-link **`?tab=compare`** mở bảng so sánh kịch bản, xuất hồ sơ **PDF `%PDF-1.4` nhiều trang** và vượt qua **406 bài test tự động** (`391` pytest + `15` Rust cargo tests).

---

## ✅ 3. CHECKLIST TỪNG BƯỚC THỰC HIỆN KHI NỘP BÀI

- [ ] **Bước 1:** Trưởng nhóm (Team Owner) đăng nhập vào [www.spaceappschallenge.org](https://www.spaceappschallenge.org/) và vào trang của đội.
- [ ] **Bước 2:** Mở tab **Project**, bấm nút **Edit**.
- [ ] **Bước 3:** Mở song song file [NASA_SUBMISSION_CHECKLIST.md](file:///e:/nasa/NASA_SUBMISSION_CHECKLIST.md) (file này đã được lọc sạch 100%, chỉ chứa nội dung thuần để copy-paste).
- [ ] **Bước 4:** Lần lượt copy từng ô (từ Box 1 đến Box 8) dán vào form trên web (đã cập nhật đầy đủ giấy phép `Dual-Licensed under Apache License 2.0 / MIT License`, slide 7 trang tiếng Anh `Flames_in_Freefall_Presentation.pptx`, kịch bản video demo 30 giây `VIDEO_PITCH_SCRIPT_2MIN.md`, huy hiệu inline SVG `Bebo Ignis-0G Mission Patch`, tương phản WCAG AA `#94A3B8`, deep-link `?tab=compare`, các tính năng M1–M6, lõi Rust `PyO3`, Dense SVD RAG, WebGL 3D, Web Audio `880/1046 Hz`, Cool Flames, Composite & Scenario Diff, PDF `%PDF-1.4` nhiều trang và bộ kiểm thử `406` bài test: `391` pytest + `15` Rust cargo tests).
- [ ] **Bước 5:** Tích 2 ô cam kết ở cuối trang (Đã đọc điều khoản cuộc thi; Bài là sản phẩm của đội và đã ghi nguồn đầy đủ).
- [ ] **Bước 6:** Bấm nút **Submit**.
- [ ] **Bước 7:** Quay lại trang chính của đội, đảm bảo dự án đã hiện trạng thái **Submitted** (Đã nộp thành công).

---

## 🎤 4. KỊCH BẢN THUYẾT TRÌNH 15 PHÚT TRƯỚC BAN GIÁM KHẢO

Thời gian: **15 phút** (gồm **5–7 phút thuyết trình** + **8–10 phút hỏi đáp Q&A**).  
Ngôn ngữ: Tiếng Việt hoặc tiếng Anh tuỳ đội lựa chọn.

### A. Kịch bản phân bổ 5–7 phút:
1. **Phút 0:00 – 1:00 (Mở đầu & Nỗi đau):**
   - "Kính chào Ban giám khảo, chúng em là đội Bebo ZeroG-X từ Trường THPT FPT Hà Nội. Dự án của chúng em là *Flames in Freefall*."
   - "Hỏa hoạn trên tàu vũ trụ là thảm họa nguy hiểm nhất đối với phi hành gia. Nhưng cháy trong không gian hoàn toàn khác Trái Đất: không có trọng lực thì không có đối lưu tự nhiên, ngọn lửa trở thành hình cầu và xuất hiện nghịch lý: khi bật quạt thông gió nhẹ để phi hành gia thở, ngọn lửa lại bùng cháy nhanh hơn và dữ dội hơn!"
2. **Phút 1:00 – 2:30 (Dữ liệu NASA PSI & Giải pháp):**
   - "Để giải quyết bài toán này, nhóm đã khai thác 3 bộ dữ liệu bay thực nghiệm thật từ NASA Physical Sciences Informatics (PSI): SoFIE (cháy thanh PMMA trên trạm ISS), Saffire (cháy vải trên tàu Cygnus ở áp suất thấp 56 kPa, giàu oxy 34%) và BASS-II."
   - "Chúng em xây dựng *Flames in Freefall* như một trạm điều hành an toàn hỏa hoạn số, tính toán tức thì chỉ số rủi ro hỏa hoạn SFRS từ 0 đến 100 và phát hiện ngọn lửa lạnh vô hình."
3. **Phút 2:30 – 4:30 (Live Demo & Điểm nhấn Kỹ thuật):**
   - Trình chiếu trực tiếp giao diện Mission Control (trên Streamlit với `@st.fragment` cách ly tab không giật lag, deep-link URL `?tab=&preset=&g=&o2=&p=&v=&t=&rh=` cùng `?tab=compare` tự động mở bảng so sánh, lưu cấu hình F5 qua `localStorage`, huy hiệu inline SVG **Bebo Ignis-0G Mission Patch** không phụ thuộc logo ngoài, chữ đạt chuẩn tương phản WCAG AA `#94A3B8`, tooltip song ngữ `i18n.py`, cảnh báo Web Audio `880/1046 Hz` + viền đỏ `#EF4444` khi `SFRS > 85`, mô hình ngọn lửa cầu WebGL Three.js 360° với 450 hạt nhiệt, đồ thị dao động Cool Flame NTC $500–800\text{ K}$, form thử nghiệm composite `NASA-STD-6001B`, so sánh 2 kịch bản kèm Radar 5 trục, và xuất hồ sơ PDF `%PDF-1.4` nhiều trang).
   - Kéo các thanh trượt vi trọng lực ($0.16g$ Mặt Trăng, $34\%\ O_2$ Artemis, $12\text{ cm/s}$ gió cabin, nhiệt độ $T$ và độ ẩm $RH$ theo phương trình Arden Buck).
   - *Điểm nhấn công nghệ:* Lõi tính toán backend viết bằng **Rust (`PyO3` / `nasa_rust`)** đạt tốc độ tính toán vật lý vi giây ($<0.25\text{ ms}$), kết hợp hệ thống tìm kiếm vector ngữ nghĩa **Dense TF-IDF + `TruncatedSVD` (RAG)** hỗ trợ nạp thêm PDF/TXT/MD, ghi nhớ hội thoại đa lượt và xuất phác đồ 3 khối chuẩn `NASA-STD-6001B` hoàn toàn offline.
4. **Phút 4:30 – 6:00 (Khuyến nghị Thực tế & Ý nghĩa):**
   - "Từ dữ liệu mô phỏng, hệ thống đưa ra phác đồ cấp cứu: Cấm phi hành gia dùng vòi nước áp lực cao (vì sẽ làm văng các giọt nhựa nóng chảy trong vi trọng lực), bắt buộc dùng sương nước mịn phun bằng $N_2$."
   - "Giải pháp này trực tiếp bảo vệ an toàn cho các sứ mệnh Artemis lên Mặt Trăng và thám hiểm Sao Hỏa trong tương lai."

### B. Bộ câu hỏi Ban giám khảo thường hỏi & Gợi ý trả lời:
1. **Giám khảo hỏi: Dữ liệu NASA được đưa vào hệ thống như thế nào?**
   - *Trả lời:* "Dạ toàn bộ dữ liệu thực nghiệm từ các file CSV của NASA SoFIE, Saffire và BASS-II được chuẩn hóa đơn vị SI và đưa vào làm tham số hiệu chuẩn cho phương trình lan truyền De Ris / Fernandez-Pello và phương trình tính MOC_eff (có hiệu chỉnh nhiệt độ T và độ ẩm RH theo Arden Buck) trong lõi Rust và engine Python song hành của hệ thống."
2. **Giám khảo hỏi: Dự án này có dùng AI không?**
   - *Trả lời:* "Dạ nhóm có dùng AI như một công cụ kỹ thuật số hỗ trợ dịch thuật thuật ngữ song ngữ, rà soát công thức toán và hỗ trợ kiểm thử tự động. Còn toàn bộ kiến trúc lõi Rust, thuật toán tính điểm rủi ro SFRS và xử lý dữ liệu NASA thật là do 4 thành viên con người tự tay thiết kế và kiểm chứng 100% qua 406 bài test tự động (391 bài test Python pytest 5 tầng và 15 bài test tích hợp Rust cargo)."
3. **Giám khảo hỏi: Tại sao lại chọn viết lõi tính toán bằng Rust?**
   - *Trả lời:* "Dạ vì trong điều kiện khẩn cấp trên trạm vũ trụ, hệ thống Mission Control cần tính toán ma trận nhiệt độ và quét đường cong dập tắt tức thì với độ trễ vi giây mà không bị rò rỉ bộ nhớ hay giật lag giao diện, do đó Rust là lựa chọn tối ưu nhất về hiệu năng và độ an toàn bộ nhớ."

