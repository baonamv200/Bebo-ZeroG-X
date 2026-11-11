# NASA Space Apps Challenge 2026 // Official Project Submission Dossier
## Project: Flames in Freefall — SI-Powered Spacecraft Fire Safety Dashboard

> **Challenge Category:** Microgravity Physical Sciences / Space Exploration Fire Safety  
> **Team Name:** Bebo ZeroG-X  
> **Team Lead & Architect:** Vũ Bảo Nam (Vu Bao Nam)  
> **Team Members:** Đỗ Duy Nam • Lương Đức Tùng • Trịnh Đức Anh  
> **Institution:** Trường THPT FPT (FPT High School)  
> **Source Code Repository:** [github.com/baonamv200/nasa](https://github.com/baonamv200/nasa)  
> **Live Web Application:** [flames-in-freefall.streamlit.app](https://flames-in-freefall.streamlit.app)  

---

### 1. High-Level Project Summary (Tóm Tắt Cấp Cao)
* **English:**  
  *Flames in Freefall* is an aerospace-grade interactive Mission Control platform built with Python, Streamlit, and Plotly 3D to evaluate, rank, and simulate fire behavior in extreme spaceflight environments (ISS, Artemis Lunar Habitat, Mars Transit). Powered by the custom **Bebo Ignis-0G** physics combustion engine and a pure-Python TF-IDF vector RAG engine, the platform translates raw experimental datasets from **NASA Physical Sciences Informatics (PSI)** (SoFIE, Saffire, BASS-II) into instant fire risk scores (SFRS 0–100), Cool Flame detections, and deterministic emergency fire suppression workflows.
* **Tiếng Việt:**  
  *Flames in Freefall* là trạm điều hành an toàn hỏa hoạn tàu vũ trụ tương tác cao cấp, được xây dựng bằng Python, Streamlit và Plotly 3D để mô phỏng và đánh giá rủi ro cháy trong môi trường không gian khắc nghiệt (trạm ISS, khoang đổ bộ Mặt Trăng Artemis, tàu thám hiểm Sao Hỏa). Vận hành bởi động cơ toán lý **Bebo Ignis-0G** và hệ thống RAG tìm kiếm vector tài liệu kỹ thuật NASA, dự án biến các tập dữ liệu thực nghiệm thô từ **NASA PSI** thành công cụ đánh giá rủi ro hỏa hoạn tức thời (SFRS 0–100), phát hiện ngọn lửa lạnh và quy chuẩn dập lửa khẩn cấp cho phi hành đoàn.

---

### 2. Detailed Project Description & Problem Alignment (Đúng Đề: Động Lực Học Cháy Vi Trọng Lực)
Fire in microgravity is an astronaut's worst nightmare. On Earth ($1.0g$), natural buoyant convection pulls hot, low-density gases upward, feeding fresh oxidizer into the flame base and creating the classic elongated teardrop plume. In microgravity ($0.0g$), buoyancy ceases completely:
1. **Spherical Flame Geometry:** Flames transition into quiet, soot-free blue spheres where combustion is throttled by 3D molecular diffusion alone.
2. **The Ventilation Paradox:** To keep astronauts alive, spacecraft cabins maintain forced air circulation ($5–20\text{ cm/s}$). This forced velocity paradoxically strips away inert $CO_2$ blankets and supplies fresh oxygen to burning materials, lowering their Minimum Oxygen Concentration (MOC) and causing materials to ignite far more aggressively than on Earth.
3. **Cool Flames Hazard:** At low temperatures ($500–800\text{ K}$), invisible smoldering reactions emit copious amounts of toxic Carbon Monoxide ($CO$) without visible light, defying conventional optical smoke detectors.

**Flames in Freefall** directly tackles this aerospace challenge by giving flight controllers, astronauts, and spacecraft designers an interactive simulator to visualize non-linear combustion kinetics, calculate the U-shaped extinction boundary (Radiative Quenching vs. Convective Blowoff), and prevent catastrophic spacecraft fires.

---

### 3. NASA Open Data & Resources Integration (Có Nguồn Rõ: Khai Thác Dữ Liệu NASA PSI)
Our platform strictly ingests, standardizes, and calibrates against peer-reviewed experimental datasets from **NASA Physical Sciences Informatics (PSI)**:
* **NASA SoFIE (Solid Fuel Ignition and Extinction):** Extracted experimental burn rate and forced airflow velocity data for PMMA polymer rods tested inside the ISS Combustion Integrated Rack (CIR) (`data/sofie_pmma_burn_rates.csv`). Principal Investigators: Dr. David Urban, Paul Ferketič (NASA Glenn Research Center).
* **NASA Saffire (Spacecraft Fire Safety):** Large-scale fabric flammability data conducted inside Northrop Grumman Cygnus resupply craft after unberthing from the ISS, under reduced cabin pressures ($56–70\text{ kPa}$) and enriched oxygen ($26–34\%$) (`data/saffire_pressure_oxygen.csv`).
* **NASA BASS-II & FLEX-2:** Extinction limits and Limiting Oxygen Index (LOI) measurements across 15+ spacecraft polymers (`data/bass_extinction_limits.csv`).
* **Official NASA Standards & Technical Reports:** 14 full-text NASA Technical Reports (NASA/TM, NASA/CR) and `NASA-STD-6001B` indexed into our pure-Python TF-IDF vector database for sub-4ms semantic retrieval.

---

### 4. Verification, Test Runs & Reproducibility (Có Thể Kiểm Tra: Thử Nghiệm Thực Chứng)
Anyone can independently verify the calculations and safety predictions:
* **Live Web Demonstration:** Available at [flames-in-freefall.streamlit.app](https://flames-in-freefall.streamlit.app).
* **Concrete Verification Test Case (Artemis Lunar Cabin):**
  * *Parameters:* Gravity $0.16g$, Oxygen $34.0\%$, Cabin Pressure $56.5\text{ kPa}$, Forced Airflow $15.0\text{ cm/s}$, Material: PMMA (NASA SoFIE).
  * *Prediction Output:* **Space Fire Risk Score (SFRS) = 78.5 / 100 [CRITICAL HAZARD]**, Effective MOC drops to $14.8\%\ O_2$, Flame Spread Rate $= 0.84\text{ mm/s}$, Cool Flame Alert triggered ($T = 680\text{ K}$).
  * *Automated Emergency Action:* Mandatory HVAC ventilation shutoff within $3$ seconds to starve convective airflow; prohibition of pressurized water jets to avoid splashing burning molten polymer droplets in microgravity; directive to flood compartment with Fine Water Mist ($< 50\ \mu\text{m}$) propelled by Nitrogen.
* **Automated Test Suite:** Includes `tests/test_adversarial_physics_security.py` (over 20KB of unit and property tests verifying mathematical stability, division-by-zero guards, and boundary consistency).

---

### 5. Target Beneficiaries & Impact (Có Người Cần Dùng: Đối Tượng Hưởng Lợi)
1. **Spacecraft Design & Mission Architecture Teams (NASA, ESA, JAXA, Commercial Spaceflight):** Rapidly screen candidate flight materials against NASA-STD-6001B for next-generation Artemis moon bases and Mars transit vehicles.
2. **Flight Operations & Astronaut Crew:** Immediate access to an emergency response matrix that eliminates life-threatening suppression mistakes (e.g., using improper extinguishers that aerosolize burning molten polymer).
3. **Global STEM Educators & Students:** Democratizes elite NASA zero-g research into an intuitive, visually stunning 3D platform that sparks passion for aerospace engineering.

---

### 6. Team & Individual Attribution (Nói Rõ Phần Mình Làm: Đội Bebo ZeroG-X)
* **Team Name:** **Bebo ZeroG-X**
* **Institution:** Trường THPT FPT (FPT High School)
* **Individual Roles & Concrete Contributions:**
  1. **Vũ Bảo Nam (Team Lead & Lead System Architect):**
     * Researched the governing aerodynamic and chemical kinetic equations for microgravity combustion.
     * Formulated and coded the `Bebo Ignis-0G` combustion simulation engine.
     * Implemented the pure-Python TF-IDF and Cosine Similarity RAG vector search engine from scratch.
     * Designed the modern, responsive NASA Web Design System-compliant UI using Streamlit and Plotly 3D.
  2. **Đỗ Duy Nam (Data Engineer - NASA PSI Data Processing):**
     * Extracted, cleaned, and standardized raw experimental CSV datasets from NASA PSI (`SoFIE`, `Saffire`, `BASS-II`).
     * Handled SI unit conversion and telemetry data ingestion pipelines.
  3. **Lương Đức Tùng (Combustion Safety & Suppression Protocols Specialist):**
     * Formulated the 3-column Emergency Fire Suppression Matrix according to `NASA-STD-6001B`.
     * Established chemical toxicity and off-gassing hazard metrics for spacecraft materials.
  4. **Trịnh Đức Anh (Testing & Quality Assurance):**
     * Engineered the automated test suite `tests/test_adversarial_physics_security.py` to stress-test physical edge cases.
     * Curated technical documentation and bilingual language dictionaries (`i18n.py`).

---

### 7. Links & Resources
* 💻 **GitHub Repository:** [https://github.com/baonamv200/nasa](https://github.com/baonamv200/nasa)
* 🌐 **Live Web Demo:** [https://flames-in-freefall.streamlit.app](https://flames-in-freefall.streamlit.app)
* 🎥 **2-Minute Video Pitch:** [YouTube Demo Link Placeholder / Video Link]

