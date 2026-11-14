# Official NASA Space Apps Challenge 2026 — Demo Video Script (30s Primary + 2-Min Backup)
## Project: Flames in Freefall — SI-Powered Spacecraft Fire Safety Dashboard
**Team:** Bebo ZeroG-X (FPT High School, Hanoi)  
**Team Lead & Architect:** Vu Bao Nam  
**Members:** Do Duy Nam • Luong Duc Tung • Trinh Duc Anh  
**SEPA Compliance Rule:** Official **Project Demo** video must be **<= 30 seconds** (`00:00 - 00:30`), show the **live working application**, cite **NASA PSI datasets**, and display **complete English subtitles** (Vietnamese voiceover is permitted when paired with mandatory English subtitles).

---

## Section 1: Official 30-Second Space Apps Demo Video Script (`00:00 - 00:30`)

### 30-Second Storyboard Timeline
```text
[00:00 - 00:08] (8s) : Live Mission Control HUD + NASA PSI Data Grounding (SoFIE, Saffire, BASS-II, NASA-STD-6001B)
[00:08 - 00:18] (10s): Live Artemis Benchmark Sweep (0.16g, 34% O2, 56.5 kPa, 12 cm/s -> SFRS 78.5 CRITICAL) + 3D WebGL Flame
[00:18 - 00:25] (7s) : ?tab=compare Radar + Dense Semantic RAG + Fine Water Mist Protocol (T+0s / T+15s / T+60s) & %PDF-1.4 Export
[00:25 - 00:30] (5s) : 406/406 Automated Tests Pass + Open-Source GitHub & Live App Close
```

---

### Second-by-Second Shot List, Voiceover & Mandatory English Subtitles

#### Beat 1 (`00:00 - 00:08` | 8s): Live HUD & NASA PSI Grounding
* **Visual (Live Screen Recording):**
  * Show the live Streamlit **Flames in Freefall** Mission Control HUD (`app.py`), hovering briefly over the **Bebo Ignis-0G Mission Patch** and clicking into **`5. NASA PSI Library`** to highlight `sofie_pmma_burn_rates.csv`, `saffire_pressure_oxygen.csv`, `bass_extinction_limits.csv`, and `NASA-STD-6001B`.
* **English Voiceover (Option A — ~19 words):**
  > *"Flames in Freefall transforms NASA PSI datasets—SoFIE, Saffire, BASS-II, and NASA-STD-6001B—into a live spacecraft fire safety dashboard."*
* **Vietnamese Voiceover (Option B — Paired with English Subtitles):**
  > *"Flames in Freefall chuyển hóa dữ liệu NASA PSI—SoFIE, Saffire, BASS-II và chuẩn NASA-STD-6001B—thành trạm điều hành an toàn cháy tàu vũ trụ trực tiếp."*
* **Mandatory English Subtitles (Burned-In):**
  > `Flames in Freefall turns NASA PSI data—SoFIE, Saffire, BASS-II & NASA-STD-6001B—into a live spacecraft fire safety dashboard.`

#### Beat 2 (`00:08 - 00:18` | 10s): Live Artemis Benchmark & 3D WebGL Flame
* **Visual (Live Screen Recording):**
  * Select **Artemis Lunar Cabin** and adjust sliders to **`0.16g`**, **`34% O2`**, **`56.5 kPa`**, **`12 cm/s`**.
  * Show PMMA metrics updating immediately via the Rust `nasa_rust` core: **`SFRS = 78.5 [CRITICAL]`**, **`MOC_eff = 14.8%`**, **`Spread = 0.84 mm/s`**.
  * Switch to **`2. Flame Morphology`** and rotate the live **Three.js 3D WebGL spherical/hemispherical flame**, showing the **Cool Flame (`500–800 K`)** NTC plot.
* **English Voiceover (Option A — ~23 words):**
  > *"Powered by Rust, an Artemis cabin at 0.16g, 34% oxygen hits Critical SFRS 78.5, 14.8% MOC, and 0.84 mm/s spread in 3D."*
* **Vietnamese Voiceover (Option B — Paired with English Subtitles):**
  > *"Nhờ lõi Rust, khoang Artemis ở 0.16g, 34% oxy đạt mức nguy kịch SFRS 78.5, MOC 14.8% và tốc độ cháy lan 0.84 mm/s trên mô hình 3D."*
* **Mandatory English Subtitles (Burned-In):**
  > `Powered by Rust PyO3: Artemis (0.16g, 34% O2, 56.5 kPa, 12 cm/s) hits SFRS 78.5 [CRITICAL], 14.8% MOC, 0.84 mm/s spread + 3D WebGL.`

#### Beat 3 (`00:18 - 00:25` | 7s): Scenario Compare, Semantic RAG & Fine Water Mist Protocol
* **Visual (Live Screen Recording):**
  * Open **`?tab=compare`** showing the 5-axis Polar Radar, click **`3. AI Co-Pilot & RAG`** (Dense TF-IDF + `TruncatedSVD` citations) and **`4. Emergency Matrix`** highlighting **`T+0s` HVAC Shutoff**, **`T+15s` Crew PBE**, and **`T+60s` Fine Water Mist (`< 50 um`)**, then click **Download Mission Safety Dossier (`%PDF-1.4`)**.
* **English Voiceover (Option A — ~17 words):**
  > *"Semantic RAG prescribes T+0s HVAC shutoff, Fine Water Mist suppression, and exports a multi-page NASA PDF dossier."*
* **Vietnamese Voiceover (Option B — Paired with English Subtitles):**
  > *"Hệ thống RAG chỉ định ngắt HVAC tại T+0s, phun sương mịn Fine Water Mist và xuất hồ sơ an toàn PDF đa trang."*
* **Mandatory English Subtitles (Burned-In):**
  > `Offline Semantic RAG prescribes T+0s HVAC shutoff, T+15s PBE, T+60s Fine Water Mist (<50 um) & exports a multi-page PDF dossier.`

#### Beat 4 (`00:25 - 00:30` | 5s): 406 Verified Tests & Close
* **Visual (Live Screen Recording / End Card):**
  * Show terminal summary **`406 / 406 automated tests passed (391 pytest + 15 Rust cargo)`**, repo **`github.com/baonamv200/Bebo-ZeroG-X`**, and Team **Bebo ZeroG-X (FPT High School)**.
* **English Voiceover (Option A — ~11 words):**
  > *"Verified by 406 automated tests—open source from Team Bebo ZeroG-X."*
* **Vietnamese Voiceover (Option B — Paired with English Subtitles):**
  > *"Kiểm chứng bởi 406 bài test tự động—mã nguồn mở từ đội Bebo ZeroG-X."*
* **Mandatory English Subtitles (Burned-In):**
  > `406/406 tests passing (391 pytest + 15 Rust). Open source: github.com/baonamv200/Bebo-ZeroG-X — Team Bebo ZeroG-X.`

---

### Ready-to-Import English Subtitle Track (`.srt` for 30s Demo)
```srt
1
00:00:00,000 --> 00:00:08,000
Flames in Freefall turns NASA PSI data—SoFIE, Saffire, BASS-II & NASA-STD-6001B—into a live spacecraft fire safety dashboard.

2
00:00:08,000 --> 00:00:18,000
Powered by Rust PyO3: Artemis (0.16g, 34% O2, 56.5 kPa, 12 cm/s) hits SFRS 78.5 [CRITICAL], 14.8% MOC, 0.84 mm/s spread + 3D WebGL.

3
00:00:18,000 --> 00:00:25,000
Offline Semantic RAG prescribes T+0s HVAC shutoff, T+15s PBE, T+60s Fine Water Mist (<50 um) & exports a multi-page PDF dossier.

4
00:00:25,000 --> 00:00:30,000
406/406 tests passing (391 pytest + 15 Rust). Open source: github.com/baonamv200/Bebo-ZeroG-X — Team Bebo ZeroG-X.
```

---

## Section 2: Optional Q&A / 2-Minute Pitch Backup Script (120 Seconds)
*(For live Q&A, extended judging walkthroughs, or non-30s supplementary overview — DO NOT upload this 2-minute version to the 30-second SEPA Project Demo slot.)*

### Storyboard Timeline (120s Backup)

```text
[00:00 - 00:15] (15s) : Hook & Introduction to the Microgravity Fire Nightmare
[00:15 - 00:40] (25s) : NASA PSI Datasets & The Low-Flow Ventilation Paradox
[00:40 - 01:10] (30s) : Live Demo of Flames in Freefall (Streamlit, Rust PyO3 & 3D WebGL)
[01:10 - 01:40] (30s) : Artemis Test Case & Offline Semantic RAG Fire Suppression Protocol
[01:40 - 02:00] (20s) : Artemis/Mars Mission Impact, Open Source & Closing
```

---

### Detailed 2-Minute Backup Breakdown

#### Scene 1: Opening Hook (00:00 - 00:15 | 15s)
* **Visual:** Presenter Vu Bao Nam on camera with the live **Flames in Freefall** dashboard behind; lower-third card: *Vu Bao Nam - Team Lead & Architect, Team Bebo ZeroG-X (FPT High School)*.
* **Vietnamese Voiceover:**
  > *"Kính chào Ban giám khảo NASA Space Apps Challenge 2026! Tôi là Vũ Bảo Nam. Bạn có biết: Trong không gian, hỏa hoạn là cơn ác mộng kinh hoàng nhất của phi hành đoàn, bởi ngọn lửa không hề bốc lên trên như ở Trái Đất, mà cuộn tròn thành khối cầu xanh tĩnh lặng và cháy âm ỉ không thể nhìn thấy bằng mắt thường!"*
* **English Subtitles:**
  > *"Greetings NASA Space Apps Challenge judges! I am Vu Bao Nam. In space, fire is an astronaut's ultimate nightmare—because without buoyancy, flames turn into silent, soot-free blue spheres that smolder invisibly!"*

#### Scene 2: NASA PSI Data & Ventilation Paradox (00:15 - 00:40 | 25s)
* **Visual:** Screen recording showing `data/sofie_pmma_burn_rates.csv`, `data/saffire_pressure_oxygen.csv`, `data/bass_extinction_limits.csv`, and 1.0g vs 0.0g comparison.
* **Vietnamese Voiceover:**
  > *"Khai thác nguồn dữ liệu thực nghiệm quý giá từ NASA Physical Sciences Informatics – gồm các sứ mệnh SoFIE trên trạm ISS, Saffire trên tàu Cygnus và BASS-II – tôi nhận ra một 'Nghịch lý thông gió' chết người: Hệ thống quạt gió bắt buộc trong tàu vũ trụ vô tình biến thành nguồn thổi oxy liên tục, kích hoạt đám cháy bùng phát dữ dội ở nồng độ oxy thấp hơn nhiều so với mặt đất!"*
* **English Subtitles:**
  > *"Mining experimental data from NASA Physical Sciences Informatics—including SoFIE on the ISS, Saffire on Cygnus, and BASS-II—we modeled the lethal 'Ventilation Paradox', where mandatory cabin fans supply forced oxidizer, causing materials to burn at far lower oxygen thresholds than on Earth."*

#### Scene 3: Live Dashboard & 3D WebGL Demo (00:40 - 01:10 | 30s)
* **Visual:** Sweep **Gravity (`0.16g`)**, **Oxygen (`34%`)**, **Pressure (`56.5 kPa`)**, **Airflow (`12 cm/s`)**. Show 3D WebGL flame rotation and **SFRS** jumping to `78.5 / 100 [CRITICAL RISK]`.
* **Vietnamese Voiceover:**
  > *"Để giải quyết bài toán này, nhóm đã xây dựng 'Flames in Freefall' – nền tảng điều hành an toàn hỏa hoạn vận hành bởi động cơ Rust PyO3 và Python Bebo Ignis-0G. Chỉ với vài thao tác kéo thanh trượt môi trường hoặc chọn preset trạm Mặt Trăng Artemis hay Sao Hỏa, hệ thống lập tức tái hiện ngọn lửa 3D và tính toán điểm nguy cơ SFRS theo thời gian thực!"*
* **English Subtitles:**
  > *"To solve this, we engineered 'Flames in Freefall', powered by a Rust PyO3 and Python physics engine. With dynamic parameter sweeps across Artemis Lunar and Mars habitats, the dashboard renders a 3D WebGL flame and evaluates the Space Fire Risk Score in real time!"*

#### Scene 4: Verification & Semantic RAG Suppression (01:10 - 01:40 | 30s)
* **Visual:** Open **AI Co-Pilot & RAG** (`TF-IDF + TruncatedSVD`) and **Emergency Matrix**, citing `NASA-STD-6001B`, prohibiting water jets, and activating **Fine Water Mist (`< 50 um`)** + `%PDF-1.4` Dossier export.
* **Vietnamese Voiceover:**
  > *"Thử nghiệm thực tế với nhựa PMMA trong khoang Artemis: Điểm rủi ro đạt 78.5 mức Báo động đỏ. Hệ thống AI RAG tích hợp sẵn sàng đưa ra phương án dập lửa khẩn cấp: Tuyệt đối cấm phun tia nước áp lực cao để tránh làm bắn tung tóe nhựa nóng chảy; bắt buộc ngắt quạt gió cabin tại T+0 giây, đeo PBE tại T+15 giây và kích hoạt sương nước siêu mịn tại T+60 giây."*
* **English Subtitles:**
  > *"Testing PMMA in an Artemis cabin yields a Critical 78.5 SFRS score. Our offline Semantic RAG instantly prescribes emergency guidance: strictly prohibit water jets to prevent molten polymer splatter, isolate cabin HVAC at T+0s, don PBE at T+15s, and deploy Fine Water Mist (<50 um) at T+60s."*

#### Scene 5: Mission Impact & Closing (01:40 - 02:00 | 20s)
* **Visual:** Presenter on screen beside QR / URL `github.com/baonamv200/Bebo-ZeroG-X` and live app link `flames-in-freefall.streamlit.app`.
* **Vietnamese Voiceover:**
  > *"Flames in Freefall bảo vệ sinh mạng phi hành đoàn cho sứ mệnh Artemis và tương lai đa hành tinh của nhân loại. Toàn bộ mã nguồn mở đã được kiểm chứng qua 406 bài test tự động và sẵn sàng tại github.com/baonamv200/Bebo-ZeroG-X. Cảm ơn Ban giám khảo đã lắng nghe!"*
* **English Subtitles:**
  > *"Flames in Freefall safeguards astronaut lives for Artemis and our multi-planetary future. Verified by 406 automated tests, our open-source codebase is available at github.com/baonamv200/Bebo-ZeroG-X. Thank you for your consideration!"*

---

### Recording Tips for Maximum Clarity
1. **Strict 30s Clock for Project Demo:** Keep a timer visible and finish spoken delivery by **`00:28.5`** so the final GitHub/Bebo ZeroG-X card stays readable through **`00:30.0`**.
2. **Readable UI Zoom:** Zoom browser to `110–125%` before screen recording so sliders, `SFRS = 78.5`, 3D WebGL flame, and citations stay sharp even on compressed video streams.
3. **Always Burn In English Subtitles:** Use high-contrast white text with a dark pill background at the lower edge so judges can read every NASA PSI citation effortlessly.
