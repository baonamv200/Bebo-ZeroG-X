[OPEN: Team selection - small focused team or full team?] Chỉnh sửa lỗi font chữ trong Tab 2 (Dynamic Flame Morphology Visualizer) tại file d:\ai\nasa\app.py: đồng bộ font 'Plus Jakarta Sans', sans-serif chuẩn NASA aerospace HUD.

Working directory: d:\ai\nasa
Integrity mode: [OPEN: integrity mode]

## Requirements

### R1. Khắc phục lỗi font tại Card "SOOT & ECLSS (FILTER LOAD)" và stats box của Flame Regime banner
Tại card "SOOT & ECLSS (FILTER LOAD)" và top-right stats box của Flame Regime banner, thay thế font monospace/courier thô kệch bằng font 'Plus Jakarta Sans', sans-serif đồng bộ với toàn bộ ứng dụng.

### R2. Rà soát và đồng bộ CSS/HTML toàn bộ Tab 2 Morphology banner và 4 thẻ metric
Kiểm tra toàn bộ CSS/HTML của phần Tab 2 Morphology banner và 4 thẻ metric (Peak Temperature, Flame Aspect Ratio, Dimensionless Transport, Soot & ECLSS), đảm bảo font chữ đồng bộ đẹp mắt chuẩn NASA aerospace HUD ('Plus Jakarta Sans', sans-serif).

## Acceptance Criteria

### Font Consistency & Visual Styling
- [ ] Card "SOOT & ECLSS (FILTER LOAD)" không còn font monospace/courier; các giá trị số và nhãn hiển thị bằng 'Plus Jakarta Sans', sans-serif.
- [ ] Top-right stats box của Flame Regime banner sử dụng font 'Plus Jakarta Sans', sans-serif đồng bộ.
- [ ] 4 thẻ metric (Peak Temperature, Flame Aspect Ratio, Dimensionless Transport, Soot & ECLSS) và banner trong Tab 2 hiển thị font đồng bộ 'Plus Jakarta Sans'.

### Code Integrity
- [ ] File `d:\ai\nasa\app.py` không phát sinh lỗi cú pháp (syntax error) và ứng dụng chạy bình thường.
