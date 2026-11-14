# Flames in Freefall: SI-Powered Spacecraft Fire Safety Dashboard
### NASA Space Apps Challenge 2026 - Aerospace Microgravity Combustion Intelligence
**Team:** Bebo ZeroG-X | **Institution:** Trường THPT FPT (FPT High School)  
**Team Lead & System Architect:** Vũ Bảo Nam (Vu Bao Nam)  
**Members:** Đỗ Duy Nam • Lương Đức Tùng • Trịnh Đức Anh  
**Core Combustion Engine:** `Bebo Ignis-0G` Microgravity Combustion Physics & RAG Engine  
**License:** Dual-Licensed under Apache License 2.0 / MIT License ([LICENSE](LICENSE) — Apache 2.0 default per NASA Space Apps SEPA Rule 7)

---

An expert-grade interactive Mission Control safety platform built with **Streamlit** and **Plotly** to evaluate, rank, and simulate fire behavior in extreme spaceflight environments (ISS, Lunar Artemis Habitat, Mars Transit) using real NASA Physical Sciences Informatics (PSI) research datasets (SoFIE, Saffire, BASS-II, FLEX-2).

---

## 👨‍🚀 Team & Author Attribution

- **Team Name:** Bebo ZeroG-X
- **Team Lead & System Architect:** Vũ Bảo Nam (Vu Bao Nam)
- **Team Members:**
  - **Vũ Bảo Nam** — Team Lead, System Architecture & Full-stack Engineering
  - **Đỗ Duy Nam** — Microgravity Combustion Data & Physics Analytics
  - **Lương Đức Tùng** — Non-linear Flame Spread Kinetics & CFD Modeling
  - **Trịnh Đức Anh** — Aerospace UI/UX Design & Mission Documentation
- **Institution:** Trường THPT FPT (FPT High School)
- **Project Topic:** *Flames in Freefall: SI-Powered Fire Safety Insights from Microgravity Combustion Data*
- **Competition:** Official Entry for **NASA Space Apps Challenge 2026**
- **Core Engine:** **Bebo Ignis-0G** Microgravity Combustion Physics & RAG Vector Space Engine
- **Open-Source License:** Dual-Licensed under Apache License 2.0 / MIT License ([LICENSE](LICENSE))

---

## 🖥️ Live Demo & Competition Assets

- 🌐 **Live Web Application:** [https://flames-in-freefall.streamlit.app](https://flames-in-freefall.streamlit.app)
- 📊 **Presentation Deck:** [https://canva.link/cqtpja7dk2lbitk](https://canva.link/cqtpja7dk2lbitk)

---

## 📂 Project Architecture

```text
Bebo-ZeroG-X/
│
├── app.py                              # Mission Control HUD: @st.fragment tabs, F5 persistence, ?tab=compare URL sync, inline SVG patch, WCAG AA #94A3B8, alerts
├── i18n.py                             # Bilingual EN/VI dictionary (220 keys), 7 ARIA acronym tooltips, emergency suppression matrix
├── physics_models.py                   # Arden Buck T/RH vapor dilution, NTC Cool Flame kinetics, NASA-STD-6001B, custom composite & diff
├── rag_engine.py                       # Dense TF-IDF + TruncatedSVD LSI vector RAG, PDF/TXT/MD chunking, multi-turn history & directives
├── pdf_dossier.py                      # Pure-Python multi-page %PDF-1.4 Mission Safety Dossier writer (NaN/Inf guarded)
├── threejs_flame.py                    # Self-contained Three.js 360° WebGL spherical/buoyant flame & 450-particle emitter
├── LICENSE                             # Dual-Licensed under Apache License 2.0 (SEPA Rule 7 default) / MIT License
├── Flames_in_Freefall_Presentation.pptx # Official English SEPA presentation deck
├── requirements.txt                    # Production Python package dependencies
├── pyproject.toml                      # Maturin build config & pytest discovery settings
├── Cargo.toml                          # Rust PyO3 0.24 extension crate manifest (nasa_rust)
├── .streamlit/config.toml              # NASA theme config & telemetry opt-out (gatherUsageStats = false)
│
├── src/                                # Compiled Rust native core (nasa_rust via PyO3 + maturin)
│   ├── lib.rs                          # PyO3 module exports & health check
│   ├── physics.rs                      # Core microgravity combustion equations & finite-float guards
│   ├── mesh.rs                         # Sub-millisecond 60x60 2D isothermal field solver
│   ├── models.rs                       # Material & curve data structures
│   ├── sweeps.rs                       # Cached paradox & boundary parameter sweep evaluators
│   ├── vector_db.rs                    # Fast Rust-backed vector similarity index
│   └── data_loader.rs                  # Portable PSI CSV resolver (NASA_DATA_DIR & ancestor search)
│
├── data/                               # NASA Physical Sciences Informatics (PSI) experimental datasets
│   ├── sofie_pmma_burn_rates.csv       # NASA SoFIE microgravity PMMA rod burn rate & airflow data
│   ├── saffire_pressure_oxygen.csv     # NASA Saffire large-scale fabric burns in Cygnus resupply craft
│   └── bass_extinction_limits.csv      # NASA BASS-II & FLEX extinction boundaries & LOI measurements
│
└── tests/                              # 406 automated tests (391 Python pytest across 5 tiers + 15 Rust cargo integration tests)
```

---

## 🚀 Key Highlights & Physics Features

1. **Space Fire Risk Score (SFRS, 0–100) & NASA-STD-6001B Calibration:**
   - Evaluates non-linear microgravity combustion where low-velocity ventilation ($5–20\text{ cm/s}$) eliminates buoyant heat loss while feeding fresh oxidizer, lowering Minimum Oxygen Concentration ($\text{MOC}_{\text{eff}}$) below terrestrial $1.0g$ limits and calibrating material risk against `NASA-STD-6001B` Test 1 & Test 2.
2. **Environmental $T$ & $RH$ Coupling & Cool Flame NTC Oscillations:**
   - Incorporates Arden Buck ambient Temperature ($T$) and Relative Humidity ($RH$) water-vapor dilution across curves, sweeps, and material evaluations.
   - Simulates twin extinction branches (**Radiative Quenching** $< 3\text{ cm/s}$ and **Convective Blowoff** $> 35\text{ cm/s}$) and dynamic Negative Temperature Coefficient (**Cool Flames**, $500–800\text{ K}$) oscillatory $T(t)$ and $[\text{CO}](t)$ profiles.
3. **Zero-Rerun State Engine, Brand Compliance & Multi-Sensory Cockpit Alerts:**
   - `@st.fragment` tab isolation paired with `localStorage` F5 persistence, bidirectional URL deep-linking (`?tab=&preset=&g=&o2=&p=&v=&t=&rh=`, including `?tab=compare` deep-link expander support that maps to `sim` and auto-expands Side-by-Side Scenario Comparison), paired sliders & exact numeric inputs, mobile responsive CSS reflow, and 7 WCAG/ARIA acronym tooltips (`Da`, `Re`, `Pe`, `Ri`, `SFRS`, `MOC`, `ΔO2%`) across 220 EN/VI keys.
   - Uses a self-contained inline SVG **Bebo Ignis-0G Mission Patch** (no external Wikimedia NASA Meatball logo dependency) and **WCAG AA `#94A3B8`** foreground text contrast (`6.83:1` against `#0D1930`).
   - Emits Web Audio `880/1046 Hz` alarm chimes and pulsing `#EF4444` emergency viewport borders (`nasaCriticalBorderPulse` / `screenBorderEmergencyPulse`) when `SFRS > 85.0`.
4. **Custom Composite Screening, Scenario Comparison & Multi-Page PDF Dossier:**
   - Evaluates custom composite polymers ($\rho, c_p, k, T_{\text{ign}}, \text{MOC}, \text{HOC}$) against `NASA-STD-6001B`, compares any two mission scenarios side-by-side with a 5-axis Polar Radar chart (`?tab=compare`), and exports multi-page `%PDF-1.4` Mission Safety Dossiers (`pdf_dossier.py`).
5. **Dual-Engine AI Co-Pilot & Dense Semantic Vector RAG:**
   - **Offline Dense Semantic Vector Search:** Normalized TF-IDF + `TruncatedSVD` LSI indexing 14 NASA Technical Reports (`NASA/TM`, `NASA/CR`, `NASA-STD-6001B`), with custom PDF/TXT/MD document ingestion (300-word sliding window, 50-word overlap), multi-turn query reformulation, and dynamically grounded 3-block safety directives.
   - **Online LLM Bridge:** Optional `gemini-2.5-flash` or OpenAI integration with timeout/`SAFETY`/empty-response resilience and hashed cache isolation.

---

## 🌟 Advanced Aerospace Modules

### 🤖 1. Dense Semantic Vector RAG & Custom Upload Co-Pilot ("Ask NASA PSI Docs")
- **Hybrid LSI Vector Search Engine:** Normalized TF-IDF + `TruncatedSVD` semantic retrieval indexing 14 official NASA technical reports (`NASA/TM`, `NASA/CR`, `NASA-STD-6001B`) plus live user-uploaded PDF/TXT/MD papers.
- **Multi-Turn Memory & Grounded Safety Directives:** Expands follow-up queries with prior session history and synthesizes 3-block safety directives (*Combustion Kinetics*, *NASA-STD-6001B Compliance*, *T+0s / T+15s / T+60s Crew Protocol*) with HTML-escaped citation cards.

### 🔥 2. Dynamic Flame Morphology & 3D WebGL Spherical Rig
- **Morphological Geometry Transition:**
  - **Earth ($1.0g$):** Elongated buoyant teardrop plume ($L/W \approx 3.2$, $T \approx 1850\text{ K}$) radiating bright yellow-orange soot.
  - **Space Station ($0.0g$):** Strictly isotropic pure blue spherical diffusion shell ($L/W \approx 1.0$, $T \approx 1380\text{ K}$) driven by 3D molecular diffusion with zero soot.
  - **Moon/Mars ($0.16g–0.38g$):** **Hazardous expanding hemispherical dome** ($L/W \approx 0.65–0.85$, $T \approx 1600\text{ K}$) flaring laterally into a $+240\%$ broader surface contact area.
- **3D WebGL & Thermal Contours:** Interactive Three.js 360° spherical flame (`OrbitControls` + 450 heat particles) paired with sub-millisecond Rust 2D isothermal maps and $Gr$, $Ri$, $Pe$, $Re$, $Da$ telemetry.

### 🚨 3. Automated Emergency Suppression, Custom Matrix & PDF Export
- **3-Column Suppression Protocol Matrix:** Rapid HVAC fan isolation (`T+0s`), positive-pressure PBE donning (`T+15s`), and N₂-propelled Fine Water Mist (`< 50 μm`) or total flooding `CO2/N2` deployment (`T+60s`), strictly prohibiting high-velocity water streams that scatter molten polymers in `0g`.
- **Multi-Format Export Hub:** Downloadable multi-page pure-Python `%PDF-1.4` Mission Safety Dossiers alongside JSON/Markdown briefing exports and `NASA-STD-6001B` Test 1 / Test 2 calibration matrices.

---

## 🛠️ Installation & Quickstart

### Prerequisites
- Python 3.10+ (Python 3.12 recommended)
- Git
- *(Optional for native Rust rebuilds)* Rust toolchain (`rustc` / `cargo`) & `maturin`

### 1. Clone the Repository
```bash
git clone https://github.com/baonamv200/Bebo-ZeroG-X.git
cd Bebo-ZeroG-X
```

### 2. Set Up Virtual Environment

#### Option A: Using `uv` (Recommended - Ultra Fast)
```bash
uv venv .venv
# On Windows: .venv\Scripts\activate | On macOS/Linux: source .venv/bin/activate
uv pip install -r requirements.txt
```

#### Option B: Using standard Python `venv` and `pip`
```bash
python -m venv .venv
# On Windows: .venv\Scripts\activate | On macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
```

### 3. *(Optional)* Build Native Rust Extension & Run Automated Verification (406 Tests)
```bash
# Build native nasa_rust PyO3 extension (falls back cleanly to pure Python if skipped)
maturin develop --release

# Run Rust integration suite (15 tests) + full 5-tier Python pytest suite (391 tests)
cargo test
pytest tests/ -v --tb=short
```

### 4. Launch the Application
```bash
streamlit run app.py
```

The Mission Control dashboard will automatically open in your default browser at:
```text
http://localhost:8501
```

---

## 📚 NASA Scientific References & Flight Literature

- **NASA SoFIE Project:** Urban, D. L., Fernandez-Pello, C., et al., *"The Solid Fuel Ignition and Extinction (SoFIE) Project"*, Combustion and Flame, Vol. 245, 2022. `PSI-SOFIE-GEL-412`.
- **NASA Saffire Flight Investigation:** Ruff, G. A., Urban, D. L., T'ien, J. S., et al., *"Large-Scale Fire Safety Experiments in Space: Results from Saffire-I through Saffire-IV"*, Proceedings of the Combustion Institute, 2020. `PSI-SAFFIRE-I-IV`.
- **NASA BASS-II Project:** Olson, S. L., & Ferketič, P., *"Extinction Limits of Solid Fuel Combustion in Microgravity with Low-Speed Forced Flow"*, Combustion and Flame, Vol. 162, 2015. `PSI-BASS-II-P849`.
- **NASA FLEX Droplet Combustion:** Williams, F. A., Nayagam, V., Dietrich, D. L., et al., *"Spherical Cool Flames in Microgravity"*, Science, Vol. 338, Iss. 6114, pp. 1593-1596, 2012. `PSI-FLEX-ICE-102`.
- **NASA Flammability Standard:** NASA-STD-6001B (Revision B), *"Flammability, Odor, Offgassing, and Compatibility Requirements and Test Procedures for Materials in Environments that Support Combustion"*, NASA Technical Standards System, 2021.

---

## 👥 Project & Team Credits

- **Challenge Topic:** *Flames in Freefall: SI-Powered Fire Safety Insights from Microgravity Combustion Data*
- **Team:** Bebo ZeroG-X
- **Team Lead & Architect:** Vũ Bảo Nam (Vu Bao Nam)
- **Team Members:**
  - **Vũ Bảo Nam** — Team Lead, System Architecture & Full-stack Engineering
  - **Đỗ Duy Nam** — Microgravity Combustion Data & Physics Analytics
  - **Lương Đức Tùng** — Non-linear Flame Spread Kinetics & CFD Modeling
  - **Trịnh Đức Anh** — Aerospace UI/UX Design & Mission Documentation
- **School / Institution:** Trường THPT FPT (FPT High School, Hanoi, Vietnam)
- **Design System:** Aerospace Cyber-Glass Design System (`Plus Jakarta Sans`, `Inter`, `JetBrains Mono`, NASA Blue `#0B3D91`, Sky Cyan `#38BDF8`, NASA Red `#E03C31`, WCAG AA `#94A3B8` text contrast, and self-contained inline SVG Bebo Ignis-0G Mission Patch)
- **License:** Dual-Licensed under Apache License 2.0 / MIT License — see [LICENSE](LICENSE) (Apache License 2.0 applies as the default license per NASA Space Apps Challenge 2026 SEPA Rule 7).
