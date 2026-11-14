# Project: Microgravity Fire Safety Web Application Overhaul

## Architecture
Monolithic Streamlit application (`app.py`) modularized through `@st.fragment` rendering, companion Python engine modules for PDF export, semantic RAG, physics enhancements, and Three.js WebGL visualization.
Data flow:
1. Telemetry Controls (Sidebar & URL query parameters) -> In-memory session state & bidirectional query param sync.
2. Physics Core (Rust `nasa_rust` with pure Python mirror) -> MOC, spread rates, dynamic NTC cool flame oscillations, SFRS score.
3. Multi-Sensory Alerting -> Web Audio chime + pulsing emergency border when SFRS > 85.
4. Visualization Engines -> Three.js WebGL spherical flame component (`st.components.v1.html`), Plotly responsive charts, and pure-Python multi-page `%PDF-1.4` Mission Safety Dossier generator.
5. AI / RAG Engine -> Offline dense semantic vector space (LSI / SVD), document chunker for custom PDF/TXT uploads, multi-turn memory buffer, zero-key deterministic NASA directives.

## Code Layout
- `app.py`: Primary Streamlit application, sidebar controls, session state management, responsive styling, and isolated tab fragments.
- `.streamlit/config.toml`: Server configuration, theme settings, and telemetry opt-out (`gatherUsageStats = false`).
- `i18n.py`: Bilingual localization dictionary (220 `en`/`vi` keys), acronym definitions (7 ARIA tooltips), and emergency matrices.
- `pdf_dossier.py`: NASA Technical Memorandum styled multi-page pure-Python `%PDF-1.4` dossier generator (`generate_mission_safety_dossier_pdf`).
- `rag_engine.py`: Dense semantic vector search, dynamic PDF/text document chunker, and deterministic offline copilot.
- `physics_models.py`: Environmental temperature (T) and relative humidity (RH) physics, skeletal NTC cool flame ODE solver, and custom composite material evaluation.
- `threejs_flame.py`: Self-contained Three.js WebGL interactive 3D spherical flame generator with OrbitControls.
- `tests/`: Comprehensive test suites (Python pytest and Rust integration tests).

## Feature Inventory
| # | Feature | Description | Milestone | Source |
|---|---------|-------------|-----------|--------|
| 1 | Tab Fragment Rerun Optimization | Wrap tabs in `@st.fragment` and defer Plotly figure generation to eliminate full-page rerun lag | M1 | R1 |
| 2 | F5 Session State Persistence | Preserve simulation parameters across browser refresh via URL query string and localStorage | M1 | R1 |
| 3 | Deep-Linking URL Parameters | Read/write `tab`, `preset`, `g`, `o2`, `p`, `v`, `t`, `rh` to URL query parameters | M1 | R1 |
| 4 | Telemetry 404 Error Cleanup | Add `gatherUsageStats = false` to config.toml and use local/embedded favicon | M1 | R1 |
| 5 | Sub-1000px Responsive Layout | CSS media queries `@media (max-width: 1024px)` auto-stacking columns without clipping | M1 | R1 |
| 6 | Synchronized Direct Numeric Inputs | Pair every slider with an `st.number_input` supporting precise decimal keyboard entry | M1 | R2 |
| 7 | Acronym Tooltip Library | Plain-language hover tooltips for Da, Re, Pe, Ri, SFRS, MOC, and ΔO2% | M1 | R2 |
| 8 | Visual Hierarchy & Contrast | Tone down `#00F2FF` neon glow; apply WCAG AA compliant palette and deuteranopia dual-coding | M1 | R2 |
| 9 | Audible Alarm Chimes | Web Audio API synthesizer playing NASA warning chime via `st.components.v1.html` when SFRS > 85 | M2 | R2 |
| 10 | Pulsing Viewport Emergency Border | CSS screen border pulse and emergency banner activation when SFRS > 85 | M2 | R2 |
| 11 | 3D WebGL Spherical Flame | Interactive Three.js 360° rotatable isotropic spherical flame with heat dissipation particle waves | M2 | R5 |
| 12 | Environmental T & RH Parameters | Controls and physical formulations for ambient temperature and relative humidity | M3 | R4 |
| 13 | Dynamic Cool Flame Oscillations | Skeletal 2-step NTC chemical kinetics ODE generating live $T(t)$ and $[CO](t)$ curves | M3 | R4 |
| 14 | NASA-STD-6001B Calibration | Formal calibration matrix and documentation mapping SFRS to Test 1 and Test 2 | M3 | R4 |
| 15 | Dense Semantic Vector Retrieval | Offline dense semantic search using Scikit-Learn TruncatedSVD LSI + Cosine similarity | M4 | R3 |
| 16 | Custom Paper & PDF Ingestion | File uploader accepting PDF/TXT with sliding-window chunking and dynamic indexing | M4 | R3 |
| 17 | Multi-Turn Conversational Memory | Chat history retaining dialogue turns with context-aware query reformulation | M4 | R3 |
| 18 | Zero-Key Flight Safety Copilot | Structured 3-part NASA flight directives with verbatim citations without API key | M4 | R3 |
| 19 | Custom Composite Material Form | Thermophysical parameter inputs ($\rho, c_p, k, T_{ign}, MOC, HOC$) and immediate fire safety rating | M5 | R5 |
| 20 | Side-by-Side Scenario Comparison | Interactive dual-scenario selector with metric diff cards, 5-axis Radar chart, and bar breakdown | M5 | R5 |
| 21 | NASA-Style PDF Dossier Export | Pure-Python multi-page `%PDF-1.4` mission safety PDF dossier with parameters, scores, tables, and pagination | M5 | R5 |
| 22 | Comprehensive E2E Test Suite | Requirement-driven opaque-box test suite across Tiers 1-4 with runner and `TEST_READY.md` | E2E Track | E2E |
| 23 | Final E2E Test Pass | 100% pass of all E2E test cases across Tiers 1-4 | M6 (Final) | All |
| 24 | Adversarial Hardening (Tier 5) | Challenger-initiated adversarial coverage hardening and edge case stress testing | M6 (Final) | All |

## Milestones
| # | Name | Scope | Dependencies | Status |
|---|------|-------|-------------|--------|
| M1 | Architecture, Performance & Responsive State Engine | Features 1-8: `@st.fragment` on 5 tabs + flame visualizer, F5 persistence (`st.query_params` + `localStorage`, unified `rh:.1f`), URL deep-linking, `gatherUsageStats = false` & emoji favicon, <1024px layout reflow, paired numeric inputs, 7 ARIA acronym tooltips, `#38BDF8` palette | none | COMPLETED (`6/6` `test_m1_features`, `48/48` `test_m1_adversarial`, `4/4` `test_challenger_m1_telemetry_favicon` live `:8503` pass, `16/16` `test_challenger_m1_*` [`0` skipped], `6/6` `test_telemetry_sync`, `6/6` `test_acronym_tooltips`; Tier 1-2 F1-F8 pass; `/soicode` audit notes resolved in `sentinel/handoff.md`) |
| M2 | Multi-Sensory Alerting & 3D WebGL Spherical Flame | Features 9-11: Web Audio `880/1046 Hz` alarm chime & pulsing `#EF4444` emergency border (`nasaCriticalBorderPulse` + `screenBorderEmergencyPulse`, `SFRS > 85.0`) in `app.py`, interactive Three.js 3D WebGL spherical (`is0g ? 1.0 : ...`) / buoyant flame (`OrbitControls`, `450` particles) in `threejs_flame.py` | M1 | COMPLETED (Tier 1-2 F9-F11 pass + `SafeAlertProxy` contract wired directly to `app.py`; `ruff` `0` errors) |
| M3 | Combustion Physics, Environmental Parameters & Standards Alignment | Features 12-14: T & RH Arden Buck flammability integration (`calculate_effective_moc`, `calculate_flame_spread_rate`) propagated across `app.py` sweeps, figures, `evaluate_all_materials`, and `AICoPilotEngine` (Rust STP-gated); closed-form NTC cool flame kinetics `solve_cool_flame_ntc_kinetics` ($T(t)$ & $[\text{CO}](t)$), `NASA-STD-6001B` Test 1/2 calibration matrix; Rust `NaN`/`!is_finite()` & portable `resolve_data_dir` | M1 | COMPLETED (Tier 1-2 F12-F14 pass + `T`/`RH` sweep/parity tests + `15/15` `cargo test` Rust checks pass; `ruff` `0` errors) |
| M4 | Offline Semantic Vector RAG & Conversational Assistant | Features 15-18: Dense semantic TF-IDF + `TruncatedSVD` retrieval (`DenseSemanticVectorIndex`), 300w/50-overlap PDF/TXT/MD uploader (`ingest_user_document`) merged into `app.py`, multi-turn `reformulate_query_with_history`, dynamic query/doc/history-grounded 3-block NASA directive (`generate_grounded_directive`), regex `BLOCK 1/2/3` parser, `_api_key` cache isolation & Gemini 2.5 Flash / OpenAI hardening | M1 | COMPLETED (Tier 1-2 F15-F18 pass + `3/3` `test_vector_search_rag.rs` + `AppTest` uploaded-RAG & dynamic grounding tests pass; `ruff` `0` errors) |
| M5 | Custom Materials, Scenario Comparison & NASA PDF Dossier | Features 19-21: Custom composite evaluation (`evaluate_custom_composite`) with single-escaped `cm_name` / normalized `raw_mat`, dual-scenario diff & 5-axis radar (`calculate_scenario_diff`), pure-Python multi-page `%PDF-1.4` NASA dossier generator (`generate_mission_safety_dossier_pdf`, `_safe_float` hardened, `18,239 bytes` single-page / multi-page pagination verified) | M1, M3 | COMPLETED (Tier 1-2 F19-F21 pass + §7.1 PDF check + multi-page PDF & `AppTest` XSS tests pass; `ruff` `0` errors) |
| M6 | Final Verification: 100% E2E Pass & Adversarial Hardening | Features 23-24: Full pytest suite (`391 passed, 0 skipped, 0 failed` / `391` collected with live `:8503` server, JUnit XML `reports/e2e_results.xml`), `15/15` `test_adversarial_physics_security.py`, `18/18` `test_soicode_remediations.py`, `15/15` `cargo test`, `ruff` clean, `py_compile app.py` exit `0`, all `/soicode` findings resolved | M1-M5, E2E Track | COMPLETED (`391/391` pytest passed [`0` skipped], `15/15` Rust `cargo test` passed [`406` automated tests total], `ruff` All checks passed; all `/soicode` findings resolved in `sentinel/handoff.md`) |
| E2E | E2E Testing Track | Feature 22: 4-Tier opaque-box E2E suite + Tier 5 adversarial hardening (`test_e2e_requirements.py`, `tier1`–`tier4`), JUnit XML `reports/e2e_results.xml`, `TEST_READY.md`, and `sentinel/handoff.md` | none (parallel) | COMPLETED (`275/275` E2E Tiers 1-4 + Master passed [`0` failed, `0` skipped]: Master 5, Tier 1 120, Tier 2 120, Tier 3 24, Tier 4 6; `reports/e2e_results.xml` & `TEST_READY.md` verified) |

## Interface Contracts
### Telemetry State ↔ Tab Fragments
- `st.session_state`: Keys `gravity_val` (float), `o2_val` (float), `p_val` (float), `v_val` (float), `temp_val` (float), `rh_val` (float), `preset_selector` (str), `lang` (str), `active_tab_id` (str).
- `st.query_params`: Mirrored bidirectional query params `?tab=&preset=&g=&o2=&p=&v=&t=&rh=`.

### Physics Engine ↔ Custom Materials & Comparison
- `calculate_effective_moc(g, v, P, T, RH)` -> float
- `calculate_flame_spread_rate(g, v, P, T, RH, o2, moc_eff, base_spread)` -> float
- `calculate_space_fire_risk_score(o2, moc_eff, spread_rate, hoc)` -> float
- `solve_cool_flame_ntc_kinetics(T0, o2, P, t_max)` -> dict: `{"time": [...], "temperature": [...], "co_ppm": [...]}`

### RAG Engine ↔ Chat Interface
- `search_semantic(query: str, top_k: int = 3)` -> list[dict]
- `ingest_user_document(file_bytes: bytes, filename: str)` -> int (chunk count)
- `generate_grounded_directive(query: str, retrieved_docs: list[dict], chat_history: list[dict])` -> dict: `{"directive": str, "citations": list[dict]}`

### PDF Dossier Generator
- `generate_mission_safety_dossier_pdf(scenario_data: dict, materials_data: list[dict])` -> bytes
