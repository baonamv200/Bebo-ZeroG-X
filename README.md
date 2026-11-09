# Flames in Freefall: SI-Powered Spacecraft Fire Safety Dashboard
### NASA Space Apps Challenge 2026 - Aerospace Microgravity Combustion Intelligence
**Team Lead & Architect:** Vũ Bảo Nam (Vu Bao Nam) | **Team Members:** Đỗ Duy Nam, Lương Đức Tùng, Trịnh Đức Anh  
**Team:** Bebo ZeroG-X (THPT FPT) | **Core Combustion Engine:** `Bebo Ignis-0G` Microgravity Combustion Physics & RAG Engine

   ---

   An expert-grade interactive Mission Control safety platform built with **Streamlit** and **Plotly** to evaluate, rank, and simulate fire behavior in extreme spaceflight environments (ISS, Lunar Artemis Habitat, Mars Transit) using real NASA Physical Sciences Informatics (PSI) research datasets (SoFIE, Saffire, BASS-II, FLEX-2).

   ---

   ## 👨‍🚀 Team & Author Attribution

- **Project Lead & System Architect:** Vũ Bảo Nam (Vu Bao Nam)
- **Team Members:**
  - **Vũ Bảo Nam** — Team Lead, System Architecture & Full-stack Engineering
  - **Đỗ Duy Nam** — Microgravity Combustion Data & Physics Analytics
  - **Lương Đức Tùng** — Non-linear Flame Spread Kinetics & CFD Modeling
  - **Trịnh Đức Anh** — Aerospace UI/UX Design & Mission Documentation
- **Team:** Bebo ZeroG-X
- **Institution:** Trường THPT FPT (FPT High School)
- **Project Topic:** *Flames in Freefall: SI-Powered Fire Safety Insights from Microgravity Combustion Data*
- **Competition:** Official Entry for **NASA Space Apps Challenge 2026**
- **Core Engine:** **Bebo Ignis-0G** Microgravity Combustion Physics & RAG Vector Space Engine

   ---

   ## 🖥️ Live Demo & Preview

   - 🌐 **Live Web Application:** [Launch Flames in Freefall Dashboard](https://beboignis-0g.streamlit.app/) *(Official Deployment on Streamlit Community Cloud)*
   - 🎬 **2-Minute Video Pitch & Walkthrough:** [Watch Official Video Pitch](https://github.com/baonam-fpt/flames-in-freefall#readme) • *Bebo ZeroG-X Team*
   - 🛰️ **NASA Space Apps Challenge Entry:** [Official Project Submission Page](https://www.spaceappschallenge.org/2026/find-a-team/flames-in-freefall/) *(Placeholder)*

   ---

   ## 📂 Project Architecture

   ```text
   flames-in-freefall/
   │
   ├── app.py                             # Core Streamlit application (NASA.gov WDS design, Bebo Ignis-0G Engine, RAG, Visualizers)
   ├── i18n.py                            # Bilingual internationalization dictionary (vi/en) & emergency suppression database
   ├── requirements.txt                   # Production Python package dependencies
   ├── README.md                          # Engineering documentation & quickstart guide
   │
   └── data/                              # NASA Physical Sciences Informatics (PSI) experimental datasets
      ├── sofie_pmma_burn_rates.csv      # NASA SoFIE microgravity PMMA rod burn rate & airflow data
      ├── saffire_pressure_oxygen.csv    # NASA Saffire large-scale fabric burns in Cygnus resupply craft
      └── bass_extinction_limits.csv     # NASA BASS-II & FLEX extinction boundaries & LOI measurements
   ```

   ---

   ## 🚀 Key Highlights & Physics Features

1. **Space Fire Risk Score (SFRS, 0-100)**:
   - Evaluates non-linear microgravity combustion behavior where low-velocity ventilation ($5-20\text{ cm/s}$) eliminates natural buoyant heat loss while continuously feeding fresh oxidizer, making materials ignite at **lower oxygen concentrations (MOC)** than on Earth ($1.0g$).
2. **Cool Flames & Radiative Extinction Modeling**:
   - Accurately captures the twin branches of microgravity extinction: **Radiative Quenching** at quiescent flow ($< 3\text{ cm/s}$) and **Convective Blowoff** at high flow ($> 35\text{ cm/s}$).
   - Emits alerts when conditions transition into the **Cool Flames Region** (low-temperature $500-800\text{ K}$ smoldering producing dangerous CO gas without visible light).
3. **NASA PSI Data Pipeline**:
   - Ingests raw experimental datasets from `data/sofie_pmma_burn_rates.csv`, `data/saffire_pressure_oxygen.csv`, and `data/bass_extinction_limits.csv`.
   - Seamless fallback to embedded aerospace cache if external files are unavailable.
4. **Mission Environment Simulator (Bebo Ignis-0G)**:
   - 6 flight-certified mission presets including **ISS Standard** ($0.0g, 21\%\text{ O}_2, 101.3\text{ kPa}$), **Moon Base / Pressurized Rover** ($0.16g, 30\%\text{ O}_2, 70.3\text{ kPa}$), **Artemis Lunar Cabin** ($0.16g, 34\%\text{ O}_2, 56.5\text{ kPa}$), **EVA Spacesuit Pre-breathe** ($0.16g, 100\%\text{ O}_2, 29.6\text{ kPa}$), **Mars Transit** ($0.38g, 26\%\text{ O}_2, 70.0\text{ kPa}$), and **Earth Baseline** ($1.0g$).
   - Real-time parameter sweeps for Gravity ($0.00 - 1.00g$), Oxygen ($14.0 - 100.0\%$), Cabin Pressure ($25.0 - 105.0\text{ kPa}$), and Airflow ($0 - 50\text{ cm/s}$).
5. **Dual-Engine AI Co-Pilot (Summarize, Rank & Interpret)**:
   - **Offline Deterministic Expert System**: Instantaneous aerospace combustion physics reasoning answering why a material is hazardous, design alternatives (NASA-STD-6001B), and emergency HVAC/suppression actions.
   - **Online LLM Bridge**: Supports Gemini API (upgraded to `gemini-2.5-flash`) or OpenAI API key for extended live mission briefings.
6. **Mission Safety Briefing & Digital Attribution Export**:
   - One-click generation of print-ready technical briefing sheets, downloadable Markdown dossiers, and `.json` telemetry exports signed with author attribution (`Vu Bao Nam & Team | Bebo ZeroG-X`).
7. **Academic Literature & PSI Citations**:
   - Cross-linked with original peer-reviewed papers, Experiment IDs, and Principal Investigators (Urban, Olson, Ferketič, T'ien, Williams).

   ---

   ## 🌟 Advanced Aerospace Modules

   ### 🤖 1. Battle-Tested RAG & Semantic Vector Search ("Ask NASA PSI Docs")
   - **High-Dimensional Vector Search Engine:** Hybrid TF-IDF and normalized cosine similarity search indexing 14 official NASA technical reports (NASA/TM, NASA/CR, NASA-STD-6001B) with sub-4ms retrieval latency.
   - **Precision Evidence Extraction:** Freeform semantic queries in Vietnamese and English (e.g., *"Điều gì xảy ra với tốc độ cháy của nhựa PMMA dưới luồng gió thông gió thấp trong vi trọng lực?"*) return exact excerpts, match confidence scores (%), official report numbers, sections, page citations, and PIs.
   - **Synthesized Flight Safety Advisory:** Generates grounded answers formulating technical safety guidance based directly on flight-proven data.

   ### 🔥 2. Dynamic Flame Morphology Visualizer
   - **Morphological Geometry Transition:**
   - **Earth ($1.0g$):** Elongated buoyant teardrop plume ($L/W \approx 3.2$, $T \approx 1850\text{ K}$) radiating bright yellow-orange soot.
   - **Space Station ($0.0g$):** Perfectly symmetric pure blue spherical diffusion shell ($L/W \approx 1.0$, $T \approx 1380\text{ K}$) driven entirely by 3D molecular diffusion with zero soot.
   - **Moon/Mars ($0.16g - 0.38g$):** **Hazardous expanding hemispherical dome** ($L/W \approx 0.65 - 0.85$, $T \approx 1600\text{ K}$) flaring laterally into a 240% broader contact area with surrounding spacecraft structures.
   - **Telemetry & Contours:** Live calculation of Grashof ($Gr$), Richardson ($Ri$), Peclet ($Pe$) numbers, coupled with interactive SVG cross-sections and Plotly 2D thermal field maps.

   ### 🚨 3. Automated Emergency Suppression & Mitigation Matrix
   - **3-Column Technical Recommendation Table** dynamically generated for all Critical & High-risk flight materials:
   1. **Immediate Emergency Action (T+0s to T+3s):** Rapid HVAC fan isolation to starve forced convection and induce radiative quenching.
   2. **Optimal Suppression Agent:** Fine Water Mist ($< 50\ \mu\text{m}$) propelled by $N_2$ or Total Flooding $CO_2$; **STRICTLY PROHIBITS single high-velocity water jets** to prevent hydrodynamic shattering of burning molten polymers.
   3. **Secondary Life-Support Hazards & Toxicity:** Off-gassing analysis ($CO$, $HF$, siloxanes, aerosolized glass fibers) and mandatory astronaut positive-pressure breathing equipment (PBE/SCBA) duration.
   - **Dual-Pane Export Hub:** Left pane provides machine-readable JSON & Markdown exports with author digital signature; right pane renders print-ready `.briefing-sheet` dossier.

   ---

   ## 🛠️ Installation & Quickstart

   ### Prerequisites
   - Python 3.10+ (Python 3.11 or 3.12 recommended)
   - Git

   ### 1. Clone the Repository
   ```bash
   git clone https://github.com/baonam-fpt/flames-in-freefall.git
   cd flames-in-freefall
   ```

   ### 2. Set Up Virtual Environment

   #### Option A: Using `uv` (Recommended - Ultra Fast)
   ```bash
   # Create virtual environment
   uv venv .venv

   # Activate environment
   # On Windows:
   .venv\Scripts\activate
   # On macOS / Linux:
   source .venv/bin/activate

   # Install dependencies
   uv pip install -r requirements.txt
   ```

   #### Option B: Using standard Python `venv` and `pip`
   ```bash
   # Create virtual environment
   python -m venv .venv

   # Activate environment
   # On Windows:
   .venv\Scripts\activate
   # On macOS / Linux:
   source .venv/bin/activate

   # Install dependencies
   pip install -r requirements.txt
   ```

   ### 3. Launch the Application
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
- **Project Lead & System Architect:** Vũ Bảo Nam (Vu Bao Nam)
- **Team Members:**
  - **Vũ Bảo Nam** — Team Lead, System Architecture & Full-stack Engineering
  - **Đỗ Duy Nam** — Microgravity Combustion Data & Physics Analytics
  - **Lương Đức Tùng** — Non-linear Flame Spread Kinetics & CFD Modeling
  - **Trịnh Đức Anh** — Aerospace UI/UX Design & Mission Documentation
- **School / Institution:** THPT FPT (FPT High School)
- **Design System:** Official NASA.gov Digital Design System with Modern Cyber-Glass Aesthetic (`Plus Jakarta Sans`, `Inter`, `JetBrains Mono`, NASA Blue `#0B3D91`, Cyan `#00F2FF`, NASA Red `#E03C31`)
- **License:** Open Source under the MIT License.
