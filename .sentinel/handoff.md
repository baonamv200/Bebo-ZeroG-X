# Sentinel Handoff Dossier — Flames in Freefall (Microgravity Fire Safety Web Application)

**Workspace:** `e:\nasa`  
**Verification Timestamp:** `2026-11-14T09:32:09+07:00` (JUnit XML run started `2026-11-14T09:29:54.843700+07:00` with live `:8503` Streamlit server active; **`406` automated tests total: `391` pytest + `15` Rust**)  
**Scope:** Milestones M1–M6, E2E Track & NASA Space Apps / SEPA Compliance Remediation (All 24 Features, Interface Contracts 1–5, 4-Tier + Tier 5 + `/soicode` Pytest Suite, Rust `cargo test`, `ruff` lint, `py_compile app.py`, 7-slide English PPTX/HTML deck, 30s English-subtitled demo script, inline SVG patch, WCAG AA `#94A3B8` contrast, `?tab=compare` deep-link, Dual-License Apache 2.0 / MIT sync, & `.gitignore` hygiene)

---

## 1. Executive Summary & Workspace Status

The **Flames in Freefall** (`Bebo Ignis-0G`) microgravity fire safety platform in `e:\nasa` has completed its M1–M6 verification cycle, `/soicode` remediations, NASA Space Apps / SEPA compliance fixes, live `:8503` verification, and documentation/license synchronization across [app.py](file:///e:/nasa/app.py), companion Python engines ([physics_models.py](file:///e:/nasa/physics_models.py), [rag_engine.py](file:///e:/nasa/rag_engine.py), [pdf_dossier.py](file:///e:/nasa/pdf_dossier.py), [threejs_flame.py](file:///e:/nasa/threejs_flame.py), [i18n.py](file:///e:/nasa/i18n.py)), compiled Rust `PyO3` backend ([src/lib.rs](file:///e:/nasa/src/lib.rs)), presentation/demo assets ([build_v4_deck.py](file:///e:/nasa/build_v4_deck.py), [Flames_in_Freefall_Presentation.pptx](file:///e:/nasa/Flames_in_Freefall_Presentation.pptx), [Flames_in_Freefall_Presentation_v5.pptx](file:///e:/nasa/Flames_in_Freefall_Presentation_v5.pptx), [designs/flames-in-freefall/project/deck.json](file:///e:/nasa/designs/flames-in-freefall/project/deck.json), [VIDEO_PITCH_SCRIPT_2MIN.md](file:///e:/nasa/VIDEO_PITCH_SCRIPT_2MIN.md)), license & submission docs ([LICENSE](file:///e:/nasa/LICENSE), [PROJECT.md](file:///e:/nasa/PROJECT.md), [README.md](file:///e:/nasa/README.md), [NASA_SPACE_APPS_SUBMISSION.md](file:///e:/nasa/NASA_SPACE_APPS_SUBMISSION.md), [NASA_SUBMISSION_CHECKLIST.md](file:///e:/nasa/NASA_SUBMISSION_CHECKLIST.md), [HUONG_DAN_NOP_BAI_VA_THUYET_TRINH.md](file:///e:/nasa/HUONG_DAN_NOP_BAI_VA_THUYET_TRINH.md), [.gitignore](file:///e:/nasa/.gitignore)), and test harness ([tests/conftest.py](file:///e:/nasa/tests/conftest.py), [tests/test_soicode_remediations.py](file:///e:/nasa/tests/test_soicode_remediations.py)).

- **Automated Test & Lint Gates:**
  - **Ruff Lint:** `All checks passed!` on `physics_models.py rag_engine.py pdf_dossier.py threejs_flame.py i18n.py tests/test_soicode_remediations.py` (`ruff 0.17.3`, exit code `0`).
  - **Python Syntax Compile (`app.py`):** `.\.venv\Scripts\python.exe -m py_compile app.py` exited with code `0`.
  - **Pytest Full Suite:** **`391 passed, 0 skipped, 0 failed`** (`391` collected in `99.73s` / `0:01:39`, exit code `0`; JUnit XML written to [reports/e2e_results.xml](file:///e:/nasa/reports/e2e_results.xml), `55,999 bytes`). Live `:8503` server was active so `test_live_server_favicon_and_telemetry_isolation` in [test_challenger_m1_telemetry_favicon.py](file:///e:/nasa/tests/test_challenger_m1_telemetry_favicon.py) executed and passed (`4/4` in module).
  - **E2E Master + Tiers 1–4:** **`275 / 275 passed`**, `0 skipped`, `0 failed` (`test_e2e_requirements.py`: 5, `tier1`: 120, `tier2`: 120, `tier3`: 24, `tier4`: 6).
  - **`/soicode` Targeted Remediation Suite:** **`18 / 18 passed`**, `0 skipped`, `0 failed` in [tests/test_soicode_remediations.py](file:///e:/nasa/tests/test_soicode_remediations.py).
  - **Rust Backend (`cargo test`):** **`15 passed, 0 failed, 0 ignored`** across 7 integration test suites (exit code `0`).
  - **PDF Dossier & `?tab=compare` AppTest Verification:** `pdf_dossier.generate_mission_safety_dossier_pdf` returns `18,239 bytes` (`%PDF-1.4` header, `%%EOF`) on nominal single-page inputs; `AppTest` verified default `expand_compare_on_load is False` and `?tab=compare` mapping `active_tab_id == "sim"` with `expand_compare_on_load is True`.
- **NASA Space Apps / SEPA Compliance Remediation Status:**
  - **7-Slide English Presentation & Demo Video (`@deck`):** Refactored `build_v4_deck.py` and regenerated both `Flames_in_Freefall_Presentation.pptx` and `Flames_in_Freefall_Presentation_v5.pptx` (`58,625 bytes` each), verified via `zipfile`/XML to contain strictly 7 English slides (`ppt/slides/slide1.xml`..`slide7.xml`, `[01/07]`..`[07/07]`) with zero non-English diacritics and zero restricted NASA insignia; synchronized `designs/flames-in-freefall/project/deck.json` (`order` length 7) and `slides/*.html` (removed `tech-stack.html` and `rubric.html`); restructured `VIDEO_PITCH_SCRIPT_2MIN.md` so Section 1 is the official 30-second (`00:00 - 00:30`) English-subtitled live-demo script citing `SoFIE`, `Saffire`, `BASS-II`, and `NASA-STD-6001B`.
  - **App Branding, WCAG AA Contrast, `?tab=compare` & `.gitignore` (`@app_compliance`):** Added `render_mission_patch_svg` (`app.py:105-140`) replacing all 3 Wikimedia `NASA_logo.svg` `<img>` tags (`3371`, `4320`, `7104`, verified `0` matches for `wikimedia` and `NASA_logo.svg`); upgraded foreground CSS text `#64748B` declarations (`0` foreground `color:\s*#64748B` remaining) to WCAG AA `#94A3B8`/`#FFFFFF` while preserving `color_theme = "#64748B"` (`1858`); preserved `VALID_TABS` (`248`) while supporting `?tab=compare` via `expand_compare_on_load` (`342-347`, `5185`); added `target/`, `.cargo/`, and `.agents/` to `.gitignore`.
  - **Dual-License & Submission Doc Sync (`@docs_license`):** Updated `LICENSE` (`SPDX-License-Identifier: Apache-2.0 OR MIT`) and synchronized `NASA_SPACE_APPS_SUBMISSION.md`, `NASA_SUBMISSION_CHECKLIST.md`, `HUONG_DAN_NOP_BAI_VA_THUYET_TRINH.md`, and `README.md` on Dual-License `Apache License 2.0 / MIT License`, 7-slide English deck, 30-second English-subtitled demo video, and verified `406` test counts.
- **Static `/soicode` Audit Status:** All actionable wave-1, wave-2, and adversarial-review `/soicode` findings are resolved and covered by regression tests; companion modules pass AST/RCE checks (zero `eval`/`exec`/`compile`/`__import__`/`pickle`/`subprocess`/`yaml.load`/`os.system` in production Python files).
  - **Remediations Applied:**
    - `rag_engine.py`: Dynamic query-, retrieved-doc-, and chat-history-grounded 3-block synthesis (`BLOCK 1/2/3`, `NASA-STD-6001B`, `Test 1`, `T+0s/T+15s/T+60s`) prioritizing query & top-doc upload signals and placing query/history focus inside `BLOCK 1`.
    - `app.py` (RAG Upload Merge, Directive Rendering & XSS): Unpacks both `dict` (`{"score", "doc"}`) and `(score, doc)` hits from `rag_engine.search_semantic`, prioritizes uploaded documents cleanly, handles `"⚠️"` online warnings via `st.warning` + local directive fallback, removes stale canned `elif` topic overrides so uploaded papers & multi-turn context drive `BLOCK 1/2/3`, stores raw `cm_name` while single-escaping in `_custom_rows` (`&lt;` without `&amp;lt;`), normalizes custom `raw_mat` keys for CoPilot & Scenario Comparison, and escapes `directive_code`, `badge_rag`, chat history, and Tab 3 CoPilot fields via `html.escape(..., quote=True)`.
    - `app.py` (`T`/`RH` & continuous physics + Python `NaN` safety): Propagated `temp_c` & `rh_pct` into `calculate_effective_moc`, `calculate_flame_spread_rate`, `detect_cool_flames`, `generate_extinction_curve`, `calculate_cached_paradox_sweep`, `calculate_cached_boundary_sweep`, `generate_sfrs_figure`, `generate_paradox_figure`, `generate_boundary_figure`, `evaluate_all_materials`, `render_tab_sim`, `AICoPilotEngine.generate_expert_insights`, and `AICoPilotEngine.call_online_ai`; gated Rust fast-path strictly to STP (`T≈21°C, RH≈45%, P≈101.3 kPa`); guarded pure-Python fallbacks (`calculate_space_fire_risk_score`, `detect_cool_flames`, `calculate_flame_morphology_metrics`) against `NaN`/`Inf`.
    - `app.py` (LLM hardening): Excluded raw `_api_key` from `@st.cache_data` cache keys in `_query_online_llm_rag_cached` and `AICoPilotEngine._call_online_ai_cached` (keyed via SHA-256 prefix), replaced `"gemini-3.8-flash"` with valid Gemini Flash identifiers (`"gemini-2.5-flash"`, `"gemini-2.0-flash"`, etc.), re-raised `requests.exceptions.Timeout` out of Gemini retry loops, guarded Gemini `content: None` + `finishReason: "SAFETY"`, and handled OpenAI HTTP 200 empty/`content: None`/malformed `choices` cleanly with `api_error_notice` and `"fallback"` mode.
    - `src/mesh.rs`, `src/physics.rs`, `src/data_loader.rs`, `tests/test_adversarial_inputs.rs`: Guarded float boundaries against `f64::NAN`/`!is_finite()`, replaced hardcoded `"e:/nasa/data"` fallback with portable `resolve_data_dir` (`custom_dir` / `NASA_DATA_DIR` / `"data"` / ancestor search), and added `test_nan_mesh_and_physics_immunity`.
    - `tests/conftest.py` & `tests/test_soicode_remediations.py`: Wired `SafeAlertProxy` to AST/regex-validate and extract real alert CSS (`@keyframes nasaCriticalBorderPulse`, `@keyframes screenBorderEmergencyPulse`, `#EF4444`, `[data-testid="stAppViewContainer"]`) and audio `<script>` (`880`, `1046`, `ctx.resume()`) directly from `app.py`; added 18 regression tests covering dynamic & query-first RAG grounding, `T`/`RH` sweeps & CoPilot propagation, `NaN`/`Inf` immunity across Python fallback & Rust/PyO3, Gemini timeout/`SAFETY` & OpenAI `content: None` handling, `AppTest` XSS `cm_name` single-escaping, real uploaded `dict` RAG merging + XSS escaping, and `SafeAlertProxy`.

---

## 2. Architecture Overview & M1–M6 Completion Matrix

### 2.1 System Architecture & Data Flow
1. **Frontend & State Synchronization ([app.py](file:///e:/nasa/app.py), [i18n.py](file:///e:/nasa/i18n.py), [.streamlit/config.toml](file:///e:/nasa/.streamlit/config.toml)):**
   - Sidebar telemetry controls (`TELEMETRY_CONFIG`, `PRESET_PROFILES`) synchronize bidirectionally with `st.session_state`, `st.query_params` (`sync_telemetry_to_query_params`, `sync_state_to_query_params` with unified `rh:.1f`), and browser `localStorage` (`nasa_flames_session_state_v1`).
   - Five isolated tab renderers (`render_tab_sim`, `render_tab_morph`, `render_tab_rag`, `render_matrix_tab_fragment`, `render_tab_research`) plus `render_flame_visualizer_fragment` are wrapped in `@st.fragment` with deferred open-state rendering.
   - Telemetry stats collection is disabled (`gatherUsageStats = false` in `.streamlit/config.toml`), and the page uses an inline emoji favicon (`"🔥"`).
2. **Dual Physics & Cool Flame Layer ([physics_models.py](file:///e:/nasa/physics_models.py), [src/lib.rs](file:///e:/nasa/src/lib.rs)):**
   - Compiled `nasa_rust` crate (`PyO3 0.24`, `maturin`) exposes `MicrogravityCombustionPhysics`, `evaluate_all_materials`, `calculate_temperature_mesh`, `calculate_cached_paradox_sweep`, `calculate_cached_boundary_sweep`, `load_nasa_psi_data`, `normalize_vn_text`, and `rust_health_check`.
   - `physics_models.py` provides Contract 2 & 4 models including Arden Buck vapor dilution (`arden_buck_vapor_pressure_kpa`, `water_vapor_mole_fraction`), `T`/`RH`-aware `calculate_effective_moc` and `calculate_flame_spread_rate`, `calculate_space_fire_risk_score`, `solve_cool_flame_ntc_kinetics`, `NASA-STD-6001B` Test 1/Test 2 calibration (`get_nasa_std_6001b_calibration_table`), `evaluate_custom_composite`, and `calculate_scenario_diff`.
   - `app.generate_3d_flame_figure` enforces `math.isfinite` coercion for `gravity_g`, `airflow_cm_s`, and `peak_temp_k`.
3. **Multi-Sensory Alerting & 3D WebGL ([app.py](file:///e:/nasa/app.py), [threejs_flame.py](file:///e:/nasa/threejs_flame.py)):**
   - At `max_sfrs > 85.0`, `app.py` injects pulsing CSS border animations (defining both `@keyframes nasaCriticalBorderPulse` and `@keyframes screenBorderEmergencyPulse`) and a Web Audio API dual-tone (`880 Hz` / `1046 Hz`) oscillator alert when unmuted.
   - `threejs_flame.py` (`generate_threejs_flame_html`) renders an interactive Three.js 3D flame (`OrbitControls`, `450` heat dissipation particles, strict isotropic `0g` spherical scaling `is0g ? 1.0 : 1.0 + driftX * 0.25`, buoyant plume, extinguished states, and offline fallback if `THREE` CDN is unavailable).
4. **Offline Semantic Vector RAG & PDF Dossier ([rag_engine.py](file:///e:/nasa/rag_engine.py), [pdf_dossier.py](file:///e:/nasa/pdf_dossier.py)):**
   - `DenseSemanticVectorIndex` builds a TF-IDF + `TruncatedSVD` (`n_components <= 8`) hybrid semantic index over `NASA_PSI_CORPUS`, supports 300-word/50-word-overlap PDF/TXT/MD ingestion (`ingest_user_document`), multi-turn history expansion (`reformulate_query_with_history`), and 3-block safety directives (`generate_grounded_directive`).
   - `app.py` merges uploaded document hits (and fallback hits when `not matched_results`) from `rag_engine.search_semantic` into `matched_results` (deduped by `(report_id, title)`, capped at 3), escapes rendered card/LLM HTML via `html.escape(..., quote=True)`, and parses `BLOCK 1/2/3` via heading-agnostic regex (`1 -> b_kin`, `2 -> b_std`, `3 -> b_emg`).
   - `pdf_dossier.py` emits pure-Python multi-page `%PDF-1.4` binary payloads (`generate_mission_safety_dossier_pdf`, `_build_page_content_bytes`) guarded by `_safe_float` against `NaN`/`±Inf`/malformed inputs, with 46 lines/page automatic pagination, exact byte-offset `xref` tables, and `%%EOF` trailers.

### 2.2 Milestones M1–M6 & E2E Matrix

| # | Milestone | Scope | Status | Verified Metrics & Audit Summary |
|---|---|---|---|---|
| **M1** | Architecture, Performance & Responsive State Engine | Features 1–8 | **COMPLETED** | `6/6` `test_m1_features`, `48/48` `test_m1_adversarial`, `17/17` `test_challenger_m1_*` (`0` skipped with live `:8503` server), `6/6` `test_telemetry_sync`, `6/6` `test_acronym_tooltips`, `10/10` F1–F8 Tier 1/2 each; **SEPA Fixes:** inline SVG `render_mission_patch_svg` replaces all 3 Wikimedia `NASA_logo.svg` tags, foreground CSS `#64748B` upgraded to WCAG AA `#94A3B8`/`#FFFFFF`, `?tab=compare` `expand_compare_on_load` deep-link supported, `rh:.1f` query-param parity resolved. |
| **M2** | Multi-Sensory Alerting & 3D WebGL Spherical Flame | Features 9–11 | **COMPLETED** | Tier 1–2 F9–F11 (`30/30` tests) + `SafeAlertProxy` contract wiring pass; `ruff` clean. **Resolved:** `screenBorderEmergencyPulse` `@keyframes` alias + `#EF4444` border rule in `app.py`, `threejs_flame.py` `0g` X-axis scaling locked to `1.0`, and `SafeAlertProxy` (`tests/conftest.py`) wired to verify & extract real `app.py` CSS/audio script contracts. |
| **M3** | Combustion Physics, Environmental Parameters & Standards | Features 12–14 | **COMPLETED** | Tier 1–2 F12–F14 (`30/30` tests) + `15/15` `cargo test` + `T`/`RH` sweep tests pass; `ruff` clean. **Resolved:** `T`/`RH` propagated through `app.py` curves, sweeps, figures, and `evaluate_all_materials`; Rust STP fast-path gated to `T≈21, RH≈45, P≈101.3`; continuous environmental coefficients match `physics_models.py` deltas. |
| **M4** | Offline Semantic Vector RAG & Conversational Assistant | Features 15–18 | **COMPLETED** | Tier 1–2 F15–F18 (`40/40` tests) + `3/3` `test_vector_search_rag.rs` + `3/3` dynamic RAG tests pass; `ruff` clean. **Resolved:** `app.py` unpacks both `dict` & tuple `semantic_hits` uploads safely with `.get(...)` defaults, falls back cleanly on `"⚠️"` online errors, escapes rendered RAG HTML/dockets, extracts `BLOCK 1/2/3`, and `rag_engine.generate_grounded_directive` prioritizes query/top-doc upload signals. |
| **M5** | Custom Materials, Scenario Comparison & PDF Dossier | Features 19–21 | **COMPLETED** | Tier 1–2 F19–F21 (`30/30` tests) + §7.1 PDF check (`18,239 bytes`) + multi-page pagination (`MAT-ROW-060`, `/Count 2`) pass; `ruff` clean. **Resolved:** single-escaped `_custom_rows`, normalized custom `raw_mat`, and `ai_insight_text`/CoPilot XSS escaping in `app.py` (verified via `AppTest`); `_safe_float` hardening and multi-page pagination in `pdf_dossier.py`. |
| **M6** | Final Verification & Adversarial Hardening | Features 23–24 | **COMPLETED** | Full pytest `391 passed, 0 skipped` (`391` collected, `99.73s`, exit `0`), `15/15` `test_adversarial_physics_security.py`, `18/18` `test_soicode_remediations.py`, `15/15` `cargo test`, `ruff` exit `0`, `py_compile app.py` exit `0`, JUnit XML `reports/e2e_results.xml` (`55,999 B`); Rust/Python `NaN`/`Inf` & LLM secret-cache/Gemini/OpenAI hardening + SEPA deck/app/license compliance verified. |
| **E2E** | E2E Testing Track | Feature 22 | **COMPLETED** | `275/275 passed` (`0` skipped, `0` failed) across `test_e2e_requirements.py` (5), `tier1` (120), `tier2` (120), `tier3` (24), and `tier4` (6); `reports/e2e_results.xml` & [TEST_READY.md](file:///e:/nasa/TEST_READY.md) updated. |

### 2.3 All 24 Features Completion Matrix

| # | Feature | Milestone | Source | Implementation Location | Tier 1/2/3/4 Verification | Audit Status |
|---:|---|---|---|---|---|---|
| 1 | Tab Fragment Rerun Optimization | M1 | R1 | `app.py` (`@st.fragment` tab/viewer renderers) | Tier 1 (5/5), Tier 2 (5/5), Tier 3, Tier 4 | PASS |
| 2 | F5 Session State Persistence | M1 | R1 | `app.py` (`localStorage` + `sync_state_to_query_params`) | Tier 1 (5/5), Tier 2 (5/5), Tier 3, Tier 4 | PASS |
| 3 | Deep-Linking URL Parameters | M1 | R1 | `app.py` (`VALID_TABS`, `expand_compare_on_load`, `sync_telemetry_to_query_params`, `sync_state_to_query_params`) | Tier 1 (5/5), Tier 2 (5/5), Tier 3, Tier 4, `AppTest` `?tab=compare` | PASS (`rh:.1f` unified; `?tab=compare` maps to `sim` + `expand_compare_on_load=True` while preserving `VALID_TABS`) |
| 4 | Telemetry 404 Error Cleanup | M1 | R1 | `.streamlit/config.toml`, `app.py` (`page_icon="🔥"`, `render_mission_patch_svg`) | Tier 1 (5/5), Tier 2 (5/5), Tier 3, Tier 4 | PASS (all 3 Wikimedia `NASA_logo.svg` tags replaced by inline SVG patch; external Google Fonts & Three.js CDNs w/ offline fallback remain) |
| 5 | Sub-1000px Responsive Layout | M1 | R1 | `app.py` (responsive CSS breakpoints) | Tier 1 (5/5), Tier 2 (5/5), CDP `1/1` | PASS |
| 6 | Synchronized Direct Numeric Inputs | M1 | R2 | `app.py` (`TELEMETRY_CONFIG`, `render_telemetry_control`) | Tier 1 (5/5), Tier 2 (5/5), `test_m1_adversarial` | PASS w/ Audit Note (`gravity_val` `[0,1]`, `p_val` `[25,105]` preserved) |
| 7 | Acronym Tooltip Library | M1 | R2 | `i18n.py` (`ACRONYM_DICTIONARY`, `render_acronym_tooltip`) | Tier 1 (5/5), Tier 2 (5/5), `6/6` tooltip, `8/8` security | PASS |
| 8 | Visual Hierarchy & Contrast | M1 | R2 | `app.py`, `.streamlit/config.toml` | Tier 1 (5/5), Tier 2 (5/5), `4/4` WCAG | PASS (foreground `#64748B` CSS upgraded to WCAG AA `#94A3B8`/`#FFFFFF`; `color_theme="#64748B"` & audit test constants preserved) |
| 9 | Audible Alarm Chimes | M2 | R2 | `app.py` (Web Audio API chime at `max_sfrs > 85.0`) | Tier 1 (5/5), Tier 2 (5/5), Tier 3, Tier 4, `test_soicode_remediations` | PASS (`SafeAlertProxy` wired to validate & extract real `app.py` alert contract) |
| 10 | Pulsing Viewport Emergency Border | M2 | R2 | `app.py` (`nasaCriticalBorderPulse` + `screenBorderEmergencyPulse`) | Tier 1 (5/5), Tier 2 (5/5), Tier 3, Tier 4 | PASS (`@keyframes screenBorderEmergencyPulse` + `#EF4444` border rule active) |
| 11 | 3D WebGL Spherical Flame | M2 | R5 | `threejs_flame.py` (`generate_threejs_flame_html`), `app.py` | Tier 1 (5/5), Tier 2 (5/5), Tier 3, Tier 4 | PASS (`is0g ? 1.0 : ...` strict isotropic scale applied) |
| 12 | Environmental T & RH Parameters | M3 | R4 | `app.py`, `physics_models.py` | Tier 1 (5/5), Tier 2 (5/5), Tier 3, Tier 4, `test_soicode_remediations` | PASS (`T`/`RH` propagated through `app.py` sweeps, figures & `evaluate_all_materials`; Rust STP-gated) |
| 13 | Dynamic Cool Flame Oscillations | M3 | R4 | `physics_models.py` (`solve_cool_flame_ntc_kinetics`), `app.py` | Tier 1 (5/5), Tier 2 (5/5), Tier 3, Tier 4 | PASS w/ Audit Note (closed-form damped sinusoid vs ODE integration; `[295,1600]` K clamp) |
| 14 | NASA-STD-6001B Calibration | M3 | R4 | `physics_models.py`, `app.py` | Tier 1 (5/5), Tier 2 (5/5), Tier 3, Tier 4 | PASS |
| 15 | Dense Semantic Vector Retrieval | M4 | R3 | `rag_engine.py`, `app.py` | Tier 1 (5/5), Tier 2 (5/5), Tier 3, Tier 4 | PASS (`semantic_hits` fallback & XSS escaping wired in `app.py`) |
| 16 | Custom Paper & PDF Ingestion | M4 | R3 | `rag_engine.py` (`ingest_user_document`), `app.py` | Tier 1 (5/5), Tier 2 (5/5), Tier 3, Tier 4 | PASS (uploaded `semantic_hits` merged w/ safe `.get(...)` defaults in `app.py`) |
| 17 | Multi-Turn Conversational Memory | M4 | R3 | `rag_engine.py` (`reformulate_query_with_history`), `app.py` | Tier 1 (5/5), Tier 2 (5/5), Tier 3, Tier 4 | PASS |
| 18 | Zero-Key Flight Safety Copilot | M4 | R3 | `rag_engine.py` (`generate_grounded_directive`), `app.py` | Tier 1 (5/5), Tier 2 (5/5), Tier 3, Tier 4, `test_soicode_remediations` | PASS (dynamic query/doc/history 3-block synthesis in `rag_engine.py`; regex parser in `app.py`) |
| 19 | Custom Composite Material Form | M5 | R5 | `physics_models.py`, `app.py` | Tier 1 (5/5), Tier 2 (5/5), Tier 3, Tier 4, `AppTest` XSS | PASS (`cm_name` & `_custom_rows` `html.escape(..., quote=True)` verified via `AppTest`) |
| 20 | Side-by-Side Scenario Comparison | M5 | R5 | `physics_models.py` (`calculate_scenario_diff`), `app.py` | Tier 1 (5/5), Tier 2 (5/5), Tier 3, Tier 4, `AppTest` `?tab=compare` | PASS (rendered inside `sim` expander with `?tab=compare` `expand_compare_on_load=True` auto-expansion) |
| 21 | NASA-Style PDF Dossier Export | M5 | R5 | `pdf_dossier.py` (`_safe_float`, `_build_page_content_bytes`, `generate_mission_safety_dossier_pdf`) | Tier 1 (5/5), Tier 2 (5/5), §7.1 check (`18,239 B`), multi-page `/Count 2` | PASS w/ Note (`_safe_float` NaN/Inf hardened & automatic 46-line/page multi-page pagination; pure-Python ASCII PDF-1.4) |
| 22 | Comprehensive E2E Test Suite | E2E | E2E | `tests/test_e2e_requirements.py`, `tier1`–`tier4`, `TEST_READY.md` | Tier 1 (5/5), Tier 2 (5/5), Master (5/5) | PASS |
| 23 | Final E2E Test Pass | M6 | All | `tests/` (`391/391` pytest), `cargo test` (`15/15`), `reports/e2e_results.xml` | Tier 1 (5/5), Tier 2 (5/5), Full Run Exit `0` | PASS (`0` skipped w/ live `:8503` server) |
| 24 | Adversarial Hardening (Tier 5) | M6 | All | `tests/test_adversarial_physics_security.py`, `test_soicode_remediations.py`, `test_m1_adversarial.py`, `tests/*.rs` | Tier 1 (5/5), Tier 2 (5/5), `15/15` adversarial, `18/18` remediation, `48/48` M1 adv | PASS (Rust/Python `NaN`/`Inf` guards, multi-page PDF & LLM hardening verified) |

---

## 3. Interface Contracts 1–5 Verification Summary

| Contract | Module(s) & Verified Public Symbols | Verification Verdict | Notes & Deviations Observed |
|---|---|---|---|
| **Contract 1:** Telemetry State & URL Synchronization | [app.py](file:///e:/nasa/app.py): `TELEMETRY_CONFIG`, `PRESET_PROFILES`, `VALID_TABS`, `detect_preset_from_telemetry`, `sync_telemetry_to_query_params`, `on_slider_change`, `on_num_change`, `apply_preset`, `render_telemetry_control`, `sync_state_to_query_params` | **Pass w/ Config Preservation Notes** | `sync_state_to_query_params` `rh` aligned to `:.1f`; `?tab=compare` maps `active_tab_id="sim"` with `expand_compare_on_load=True` while preserving `VALID_TABS` (`["sim", "morph", "rag", "matrix", "research"]`), `gravity_val` `[0.00, 1.00]`, and `p_val` `[25.0, 105.0]`. |
| **Contract 2:** Combustion Physics Core & Dynamic Models | [physics_models.py](file:///e:/nasa/physics_models.py): `arden_buck_vapor_pressure_kpa`, `water_vapor_mole_fraction`, `calculate_effective_moc`, `calculate_flame_spread_rate`, `calculate_space_fire_risk_score`, `is_cool_flame_envelope`, `map_sfrs_to_nasa_tier`, `evaluate_nasa_std_6001b_test1`, `evaluate_nasa_std_6001b_test2`, `solve_cool_flame_ntc_kinetics`, `get_nasa_std_6001b_calibration_table`. [src/lib.rs](file:///e:/nasa/src/lib.rs): `MicrogravityCombustionPhysics`, `evaluate_all_materials`, `calculate_temperature_mesh`, `calculate_cached_paradox_sweep`, `calculate_cached_boundary_sweep` | **Pass w/ Edge & Parity Notes** | `app.py` propagates `T`/`RH` through curves, sweeps, figures, and `evaluate_all_materials`, gates Rust fast-path strictly to STP (`T≈21, RH≈45, P≈101.3`), and matches `physics_models.py` environmental delta coefficients continuously (preserving the intentional `v=10` `moc_microg` baseline). `src/mesh.rs` & `src/physics.rs` enforce `!is_finite()` / `is_nan()` guards; `src/data_loader.rs` uses portable `resolve_data_dir`. |
| **Contract 3:** Dense Semantic Vector RAG & Copilot | [rag_engine.py](file:///e:/nasa/rag_engine.py): `NASA_PSI_CORPUS`, `_extract_pdf_text`, `DenseSemanticVectorIndex`, `search_semantic`, `ingest_user_document`, `clear_custom_documents`, `reset_custom_documents`, `generate_grounded_directive`, `reformulate_query_with_history`, `get_default_rag_index`. [src/lib.rs](file:///e:/nasa/src/lib.rs): `NASAPsiVectorDB` | **Pass** | `app.py` merges `semantic_hits` uploads (and fallback hits when `not matched_results`), dedupes by `(report_id, title)` capped at 3, uses `.get(...)` defaults (`"Uploaded Document"`, `1`), escapes rendered HTML, and parses `BLOCK 1/2/3` via regex (`1->b_kin`, `2->b_std`, `3->b_emg`). `rag_engine.generate_grounded_directive` dynamically grounds `BLOCK 1/2/3` in `query`, `retrieved_docs`, and `chat_history`. |
| **Contract 4:** Custom Composite Materials & Scenario Diff | [physics_models.py](file:///e:/nasa/physics_models.py): `evaluate_custom_composite`, `_extract_env_tuple`, `calculate_scenario_diff` | **Pass** | Computes `thermal_inertia = k * rho * cp`, `nasa_6001b_test1`, `nasa_6001b_test2`, `delta_sfrs`, `delta_moc`, `delta_spread`, `hazard_transition`, and 5-axis `radar_metrics` plus UI aliases; `cm_name` & `_custom_rows` are HTML-escaped in `app.py`. |
| **Contract 5:** NASA Technical Memorandum PDF Dossier | [pdf_dossier.py](file:///e:/nasa/pdf_dossier.py): `_safe_float`, `_ascii_pdf_text`, `_format_scenario_lines`, `_format_material_lines`, `_build_page_content_bytes`, `generate_mission_safety_dossier_pdf` | **Hardened / Multi-Page Pure-Python PDF-1.4** | Returns valid `%PDF-1.4` bytes (`18,239 bytes >= 15,000` single-page), paginates automatically across N pages (46 lines/page, `/Count N` + `/Kids` verified on 60 rows), exact byte-offset `xref`, and `%%EOF` even under `NaN`/`±Inf`/malformed inputs via `_safe_float`. |
| **Supporting UI Modules** | [i18n.py](file:///e:/nasa/i18n.py): `ACRONYM_DICTIONARY`, `_sanitize_tooltip_text`, `render_acronym_tooltip`, `get_i18n`, `get_protocol`, `get_morphology_regime_info`. [threejs_flame.py](file:///e:/nasa/threejs_flame.py): `_finite_or_default`, `generate_threejs_flame_html` | **Pass** | All 7 acronyms (`Da`, `Re`, `Pe`, `Ri`, `SFRS`, `MOC`, `ΔO2%`) are HTML-escaped and ARIA-labeled in `en`/`vi`; Three.js renderer enforces strict isotropic `0g` scaling (`is0g ? 1.0 : 1.0 + driftX * 0.25`) alongside `OrbitControls`, particle emitter, extinguished shell, and offline fallback. |

---

## 4. 4-Tier + Tier 5 E2E Pytest & Rust Cargo Test Verification Results

All commands below were executed on `2026-11-14` (`2026-11-14T09:29:54+07:00` – `2026-11-14T09:32:09+07:00`) after applying `/soicode` remediations and NASA Space Apps / SEPA compliance fixes.

### 4.1 Command Summary

| Verification Gate | Command | Tooling / Version | Exit Code | Result |
|---|---|---|---|---|
| **Ruff Lint** | `ruff check physics_models.py rag_engine.py pdf_dossier.py threejs_flame.py i18n.py tests/test_soicode_remediations.py` | `ruff 0.17.3` (`C:\Users\baonam\.local\bin\ruff.exe`; `.venv\Scripts\ruff.exe` absent) | `0` | `All checks passed!` |
| **Python Compile (`app.py`)** | `.\.venv\Scripts\python.exe -m py_compile app.py` | Python `3.12.14` | `0` | Clean syntax compile |
| **Pytest Full Suite + JUnit XML** | `.\.venv\Scripts\pytest.exe tests/ -v --tb=short --junitxml=reports/e2e_results.xml` | Python `3.12.14`, pytest `9.2.0` | `0` | **`391 passed, 0 skipped in 99.73s (0:01:39)`** (`391` collected; `0` failed, `0` errors) |
| **Rust Integration Suite** | `cargo test` | Rust `cargo` | `0` | **`15 passed, 0 failed, 0 ignored`** across 7 integration test binaries |
| **SEPA & PDF Verification Checks** | Inline Python verification (`zipfile`/XML on both `.pptx`, `deck.json`/HTML slides, `VIDEO_PITCH_SCRIPT_2MIN.md`, `app.py`/`.gitignore` regex, 5 docs/license checks, `AppTest` `?tab=compare`, `pdf_dossier`, `nasa_rust.rust_health_check`) | Python `3.12.14` | `0` | `nasa_rust: ok`, `PDF_BYTES: 18239`, `APPTEST_COMPARE_OK`, both `.pptx` 7 English slides (`58,625 B`), `DECK_HTML_OK`, `ALL_DOCS_AND_VIDEO_SCRIPT_VERIFIED` |

**JUnit XML Artifact:** [e:\nasa\reports\e2e_results.xml](file:///e:/nasa/reports/e2e_results.xml) (`55,999 bytes`, root `<testsuite name="pytest" errors="0" failures="0" skipped="0" tests="391" time="99.739" timestamp="2026-11-14T09:29:54.843700+07:00" hostname="DESKTOP-ADMIN">`).

### 4.2 Pytest Breakdown by Category & Module (from JUnit XML)

| Category | Test Module | Passed | Skipped | Failed | Duration | Notes |
|---|---|---:|---:|---:|---:|---|
| **E2E Master & Tiers 1–4** | [test_e2e_requirements.py](file:///e:/nasa/tests/test_e2e_requirements.py) | 5 | 0 | 0 | 0.13s | Master discovery & count threshold checks (`>= 270`) |
| **E2E Tier 1 (Isolation)** | [test_e2e_tier1_features.py](file:///e:/nasa/tests/test_e2e_tier1_features.py) | 120 | 0 | 0 | 5.74s | 5 tests per feature across Features 1–24 |
| **E2E Tier 2 (Boundary)** | [test_e2e_tier2_boundaries.py](file:///e:/nasa/tests/test_e2e_tier2_boundaries.py) | 120 | 0 | 0 | 1.94s | 5 BVA tests per feature across Features 1–24 |
| **E2E Tier 3 (Pairwise)** | [test_e2e_tier3_pairwise.py](file:///e:/nasa/tests/test_e2e_tier3_pairwise.py) | 24 | 0 | 0 | 0.08s | 24 orthogonal multi-factor interaction probes |
| **E2E Tier 4 (Scenarios)** | [test_e2e_tier4_scenarios.py](file:///e:/nasa/tests/test_e2e_tier4_scenarios.py) | 6 | 0 | 0 | 0.05s | 6 mission profiles (ISS, Artemis, EVA, Lunar Bay, Cool Flame, Emergency PDF) |
| *Subtotal (E2E Tiers 1–4 + Master)* | *5 files* | **275** | **0** | **0** | **7.94s** | *100% pass rate* |
| **M1 Feature Suite** | [test_m1_features.py](file:///e:/nasa/tests/test_m1_features.py) | 6 | 0 | 0 | 3.13s | App load, query bootstrap, paired widgets, config, favicon |
| **M1 Adversarial Suite** | [test_m1_adversarial.py](file:///e:/nasa/tests/test_m1_adversarial.py) | 48 | 0 | 0 | 32.51s | Hostile query params, NaN/Inf, boundaries, presets, fragments |
| **M1 Challenger (CDP)** | [test_challenger_m1_cdp_responsive.py](file:///e:/nasa/tests/test_challenger_m1_cdp_responsive.py) | 1 | 0 | 0 | 35.70s | Empirical viewport responsive layout sweep |
| **M1 Challenger (Tooltips)** | [test_challenger_m1_acronym_security.py](file:///e:/nasa/tests/test_challenger_m1_acronym_security.py) | 8 | 0 | 0 | 0.01s | XSS payloads, attribute breakout, Unicode, missing keys |
| **M1 Challenger (WCAG)** | [test_challenger_m1_contrast_wcag.py](file:///e:/nasa/tests/test_challenger_m1_contrast_wcag.py) | 4 | 0 | 0 | 0.01s | Palette WCAG AA/AAA & `#64748B` contrast audit |
| **M1 Challenger (Telemetry)** | [test_challenger_m1_telemetry_favicon.py](file:///e:/nasa/tests/test_challenger_m1_telemetry_favicon.py) | 4 | 0 | 0 | 0.08s | `test_live_server_favicon_and_telemetry_isolation` passed against live `:8503` server |
| *Subtotal (M1 & Challenger)* | *6 files* | **71** | **0** | **0** | **71.44s** | *100% pass rate (live `:8503` check executed)* |
| **Tier 5 / Adversarial** | [test_adversarial_physics_security.py](file:///e:/nasa/tests/test_adversarial_physics_security.py) | 15 | 0 | 0 | 9.66s | Physics stress, AST RCE check, online LLM timeout, memory stability |
| **`/soicode` Remediations** | [test_soicode_remediations.py](file:///e:/nasa/tests/test_soicode_remediations.py) | 18 | 0 | 0 | 4.99s | Dynamic RAG grounding, `T`/`RH` sweeps & CoPilot, `NaN`/`Inf` (Rust & Python fallback), multi-page PDF, LLM hardening, `AppTest` XSS/uploads, `SafeAlertProxy` |
| **Telemetry Sync Unit** | [test_telemetry_sync.py](file:///e:/nasa/tests/test_telemetry_sync.py) | 6 | 0 | 0 | 0.01s | `TELEMETRY_CONFIG`, `PRESET_PROFILES`, `VALID_TABS`, clamping |
| **Tooltip Contract** | [test_acronym_tooltips.py](file:///e:/nasa/tests/test_acronym_tooltips.py) | 6 | 0 | 0 | 0.01s | Required keys, `en`/`vi` HTML output, aliases |
| *Subtotal (Adversarial / Remediations / Unit)* | *4 files* | **45** | **0** | **0** | **14.67s** | *100% pass rate* |
| **Total Pytest Suite** | **15 files** | **391** | **0** | **0** | **94.05s** | *Wall clock `99.73s`; collected `391` items (`reports/e2e_results.xml`)* |

### 4.3 Rust `cargo test` Breakdown

`src/lib.rs` unit tests: `0` | Doc-tests: `0` | Integration targets (`tests/*.rs`): `15 passed, 0 failed, 0 ignored`:
- [test_adversarial_inputs.rs](file:///e:/nasa/tests/test_adversarial_inputs.rs): `3 passed` (including `test_nan_mesh_and_physics_immunity`)
- [test_extinction_curves.rs](file:///e:/nasa/tests/test_extinction_curves.rs): `1 passed`
- [test_materials_evaluation.rs](file:///e:/nasa/tests/test_materials_evaluation.rs): `2 passed`
- [test_performance_stress.rs](file:///e:/nasa/tests/test_performance_stress.rs): `1 passed`
- [test_physics_boundaries.rs](file:///e:/nasa/tests/test_physics_boundaries.rs): `4 passed`
- [test_temperature_mesh.rs](file:///e:/nasa/tests/test_temperature_mesh.rs): `1 passed`
- [test_vector_search_rag.rs](file:///e:/nasa/tests/test_vector_search_rag.rs): `3 passed`

---

## 5. `/soicode` Code Review, Security & Performance Audit Findings

Static read-only review performed across `app.py`, `i18n.py`, `physics_models.py`, `rag_engine.py`, `pdf_dossier.py`, `threejs_flame.py`, and `src/*.rs`, followed by wave-1 P0/P1 remediations and wave-2 structural/hygiene remediations on `2026-11-14`.

### 5.1 Positive Security & Performance Controls
- **AST / Arbitrary Code Execution Check (PASS):** Zero occurrences of `eval`, `exec`, `compile`, `__import__`, `pickle`, `subprocess`, `yaml.load`, or `os.system` across production `.py` files.
- **Tooltip XSS Sanitization (PASS):** `i18n.render_acronym_tooltip` escapes attribute/HTML metacharacters via `html.escape(..., quote=True)`.
- **Fragment Isolation (PASS):** `@st.fragment` wraps all 5 main tabs plus the flame visualizer with deferred open-state rendering.

### 5.2 Findings Ledger (All Actionable Findings Resolved)

1. **[CRITICAL -> RESOLVED] Stored / Reflected XSS via `render_html` (`app.py`)**
   - **Resolution Applied:** Added `import html` in `app.py`; stored unescaped `cm_name.strip()` while single-escaping `_ev["name"]` in `_custom_rows` (eliminating `&amp;lt;` double-escaping), normalized custom `raw_mat` keys for CoPilot & Scenario Comparison, escaped text inside `_fmt_online_block` prior to Markdown `<b>`/heading formatting, escaped `directive_code`, `badge_rag`, `doc_rep_id`/`top_doc` header fields, chat history markdown, all citation card fields (`title`, `report_id`, `section`, `page`, `authors`, `facility`, `text`), and Tab 3 CoPilot fields (`cp_name`, `cp_psi`, `cp_mission`, `cp_cat`, `cp_geom`, `cp_chem`, `cp_morph`, `llm_provider`, `ai_insight_text`). Covered by Streamlit `AppTest` XSS assertions across custom forms, Tab 3 uploads, and custom CoPilot selection in `tests/test_soicode_remediations.py`.

2. **[HIGH -> RESOLVED] Uploaded RAG Documents & Dynamic Directive Synthesis (`app.py` & `rag_engine.py`)**
   - **Resolution Applied in `app.py`:** `app.py` unpacks both `dict` (`{"score", "doc"}`) and `(score, doc)` tuples from `rag_engine.search_semantic` (`top_k=6`), prioritizes uploaded documents in `matched_results` (deduped by `(report_id, title)`, capped at 3), handles `"⚠️"` online error notices with `st.warning` + local directive fallback, removes stale canned `elif` topic overrides so uploaded chunks & `chat_history` drive `BLOCK 1/2/3`, and applies `.get(...)` defaults (`"Uploaded Document"`, page `1`, `"Mission Operator"`, `"User Upload"`).
   - **Resolution Applied in `rag_engine.py`:** Replaced static 3-block boilerplate in `DenseSemanticVectorIndex.generate_grounded_directive` with dynamic synthesis grounded in `query`, retrieved document IDs/titles/sections/pages/excerpts, and `chat_history` — prioritizing query & top-doc upload signals over secondary doc #2/#3 text and embedding query/history context inside `BLOCK 1` while preserving `BLOCK 1/2/3`, `NASA-STD-6001B`, `Test 1`, `T+0s/T+15s/T+60s`, and `{"directive", "citations"}`.

3. **[HIGH -> RESOLVED] `T`/`RH` Propagation & Continuous Physics Parity (`app.py` & `physics_models.py`)**
   - **Resolution Applied:** Propagated `temp_c` & `rh_pct` into `app.MicrogravityCombustionPhysics` (`calculate_effective_moc`, `calculate_flame_spread_rate`, `detect_cool_flames`, `generate_extinction_curve`), `calculate_cached_paradox_sweep`, `calculate_cached_boundary_sweep`, `generate_sfrs_figure`, `generate_paradox_figure`, `generate_boundary_figure`, `evaluate_all_materials`, `render_tab_sim`, `AICoPilotEngine.generate_expert_insights`, and `AICoPilotEngine.call_online_ai` / `copilot_cache_key`. Gated `app.py` calls to the compiled Rust STP backend (`T≈21°C, RH≈45%, P≈101.3 kPa`) so non-STP queries evaluate continuously using environmental coefficients matching `physics_models.py` deltas while preserving the `v=10` `moc_microg` baseline required by existing Tier 1–4 & Rust contracts.

4. **[HIGH -> RESOLVED] RAG Fallback Split `IndexError` & `rh` Query-Param Churn (`app.py`)**
   - **Resolution Applied:** Replaced `.split("**BLOCK 1:")` indexing with a heading-agnostic `re.finditer` extractor matching `**BLOCK N:...**`, `#{1,4} BLOCK N:...`, and bare `BLOCK N:...` (`1 -> b_kin`, `2 -> b_std`, `3 -> b_emg`) without `IndexError`. Standardized `rh` in `sync_state_to_query_params` from `:.0f` to `:.1f` matching `sync_telemetry_to_query_params`.

5. **[HIGH — Test Hygiene -> RESOLVED] `SafeAlertProxy` Real Contract Wiring & Regression Coverage (`tests/conftest.py`, `tests/test_soicode_remediations.py`)**
   - **Resolution Applied:** Wired `SafeAlertProxy` in `tests/conftest.py` (`_load_app_alert_contract`) to AST- and regex-verify `if max_sfrs > 85.0:`, `audio_muted` gate, `#EF4444`, `@keyframes nasaCriticalBorderPulse`, `@keyframes screenBorderEmergencyPulse`, `[data-testid="stAppViewContainer"]`, `ctx.resume()`, `[880, 1046]`, and SFRS threat thresholds directly from `app.py` while returning genuine extracted CSS/audio payloads and preserving Tier 1–4 interfaces. Added 18 targeted tests in `tests/test_soicode_remediations.py` (including real `AppTest` custom-form & Tab 3 uploaded-`dict` XSS rendering, query-first RAG routing, `T`/`RH` sweeps & CoPilot, `NaN`/`Inf` across PDF/3D/Mesh/Python fallback/Rust, multi-page PDF `/Count 2` pagination, LLM timeout/safety/`content: None` hardening, and `SafeAlertProxy`). *(Legacy Tier 1–4 structural test count requirements in `test_e2e_requirements.py` remain preserved untouched.)*

6. **[MEDIUM -> RESOLVED] `NaN`/`Inf` Leakage, LLM Key Caching & Rust Portability (`src/*.rs`, `app.py`, `pdf_dossier.py`)**
   - **Resolution Applied:**
     - `app.generate_3d_flame_figure`, `app.calculate_temperature_mesh`, and pure-Python fallbacks (`calculate_space_fire_risk_score`, `detect_cool_flames`, `calculate_flame_morphology_metrics`) coerce non-finite inputs cleanly via `math.isfinite` / `_safe_float`.
     - `pdf_dossier.py` uses `_safe_float` in `_format_scenario_lines` and `_format_material_lines`, safely handling `NaN`, `±Inf`, `None`, and malformed numeric strings without `ValueError`.
     - `src/mesh.rs` & `src/physics.rs` guard float parameters with `is_nan()` / `!is_finite()` prior to `< 0.0` / `<= 0.0` checks, covered by `test_nan_mesh_and_physics_immunity` in `tests/test_adversarial_inputs.rs` and `maturin develop --release`.
     - `src/data_loader.rs` replaces the hardcoded `"e:/nasa/data"` fallback with portable `resolve_data_dir` checking `custom_dir`, `NASA_DATA_DIR`, `"data"`, `current_dir` ancestors, and `current_exe` ancestors.
     - `app.py` splits `_query_online_llm_rag_cached` and `AICoPilotEngine._call_online_ai_cached` with `_api_key` excluded from `@st.cache_data` keys (keyed via SHA-256 `api_key_hash`), replaces nonexistent `"gemini-3.8-flash"` with valid Gemini Flash models (`"gemini-2.5-flash"`, `"gemini-2.0-flash"`, `"gemini-flash-latest"`, `"gemini-1.5-flash"`), re-raises `requests.exceptions.Timeout` out of Gemini loops, guards Gemini `content: None` + `finishReason: "SAFETY"`, and handles HTTP 200 empty/`content: None`/malformed OpenAI `choices` cleanly with `api_error_notice` before falling back.

7. **[MINOR / Spec & SEPA Compliance Observations — RESOLVED / PRESERVED]**
   - **Resolved (`/soicode`):** Defined `@keyframes screenBorderEmergencyPulse` alongside `@keyframes nasaCriticalBorderPulse` + `border-color: #EF4444` in `app.py`, enforced strict `0g` isotropic core scaling `is0g ? 1.0 : 1.0 + driftX * 0.25` in `threejs_flame.py`, and upgraded `pdf_dossier.py` from a 45-line single-page cap to automatic multi-page pagination (46 lines/page) while preserving nominal `18,239 bytes` single-page output.
   - **Resolved (SEPA Compliance):** Replaced all 3 external Wikimedia `NASA_logo.svg` `<img>` tags with `render_mission_patch_svg` inline SVG (`app.py`), upgraded foreground CSS `#64748B` to WCAG AA `#94A3B8`/`#FFFFFF`, wired `?tab=compare` `expand_compare_on_load`, added `target/`, `.cargo/`, `.agents/` to `.gitignore`, refactored `build_v4_deck.py` / both `.pptx` / HTML slides to strictly 7 English slides (`[01/07]`..`[07/07]`), made `VIDEO_PITCH_SCRIPT_2MIN.md` Section 1 the 30s English-subtitled live demo script, and dual-licensed `LICENSE` + submission docs under `Apache License 2.0 / MIT License`.
   - **Intentionally Preserved Spec Constraints:** External Google Fonts & Three.js CDNs (with offline fallback); legacy `#00F2FF` accents and WCAG `#64748B` contrast audit constant; `color_theme = "#64748B"` extinguished regime badge; closed-form NTC kinetics; pure-Python ASCII PDF-1.4 with archive comment padding; preserved `TELEMETRY_CONFIG` `g` `[0,1]` / `p` `[25,105]` and `VALID_TABS` (`["sim", "morph", "rag", "matrix", "research"]`).

---

## 6. Operational Runbook & Submission Readiness Checklist

### 6.1 Operational Runbook (Windows PowerShell, `e:\nasa`)

```powershell
# 1. Verify Rust PyO3 native extension inside .venv
.\.venv\Scripts\python.exe -c "import nasa_rust; print('nasa_rust:', nasa_rust.rust_health_check())"

# 2. Launch Streamlit Mission Control Dashboard (default http://localhost:8501)
.\.venv\Scripts\streamlit.exe run app.py

# 3. Run Ruff style/lint checks & Python compile check
ruff check physics_models.py rag_engine.py pdf_dossier.py threejs_flame.py i18n.py tests/test_soicode_remediations.py
.\.venv\Scripts\python.exe -m py_compile app.py

# 4. Run full Pytest suite (Tiers 1-4, M1, Challenger, Adversarial, Remediations) + JUnit XML
.\.venv\Scripts\pytest.exe tests/ -v --tb=short --junitxml=reports/e2e_results.xml

# 5. Run Master E2E Tiers 1-4 Aggregator only
.\.venv\Scripts\pytest.exe tests/test_e2e_requirements.py -v --tb=short

# 6. Run Rust integration test suite
cargo test

# 7. Run PDF Dossier verification check (TEST_INFRA.md §7.1)
.\.venv\Scripts\python.exe -c "import pdf_dossier; b = pdf_dossier.generate_mission_safety_dossier_pdf({'mission':'ISS','g':0.0,'o2':21.0,'p':101.3,'v':10.0,'t':21.0,'rh':45.0,'sfrs':52.4,'tier':'HIGH'}, [{'material_name':'PMMA','sfrs':52.4,'moc_eff':15.2,'spread_rate':0.85,'flammability':'Flammable'}]); assert b.startswith(b'%PDF-1.') and len(b) > 15000 and b'%%EOF' in b; print(f'PDF Dossier verification PASSED: {len(b)} bytes')"
```

*Optional live-server check:* Starting Streamlit on port `8503` (`.\.venv\Scripts\streamlit.exe run app.py --server.port 8503`) allows `test_live_server_favicon_and_telemetry_isolation` in [test_challenger_m1_telemetry_favicon.py](file:///e:/nasa/tests/test_challenger_m1_telemetry_favicon.py) to run instead of skipping.

### 6.2 Submission Readiness Checklist

#### Verified Passing Gates & Resolved `/soicode` Items
- [x] **M1–M6, E2E & SEPA Compliance Documentation Updated:** [LICENSE](file:///e:/nasa/LICENSE) (`Apache-2.0 OR MIT`), [PROJECT.md](file:///e:/nasa/PROJECT.md), [README.md](file:///e:/nasa/README.md), [NASA_SPACE_APPS_SUBMISSION.md](file:///e:/nasa/NASA_SPACE_APPS_SUBMISSION.md), [NASA_SUBMISSION_CHECKLIST.md](file:///e:/nasa/NASA_SUBMISSION_CHECKLIST.md), [HUONG_DAN_NOP_BAI_VA_THUYET_TRINH.md](file:///e:/nasa/HUONG_DAN_NOP_BAI_VA_THUYET_TRINH.md), [VIDEO_PITCH_SCRIPT_2MIN.md](file:///e:/nasa/VIDEO_PITCH_SCRIPT_2MIN.md), [TEST_READY.md](file:///e:/nasa/TEST_READY.md), [sentinel/handoff.md](file:///e:/nasa/sentinel/handoff.md), and [.sentinel/handoff.md](file:///e:/nasa/.sentinel/handoff.md) synchronized.
- [x] **E2E Tiers 1–4 + Master Suite:** `275 / 275` passed (`0` failed, `0` skipped) in `7.94s`.
- [x] **Full Pytest Suite & JUnit XML:** `391 passed, 0 skipped` (`391` collected, `99.73s`, exit `0`) -> [reports/e2e_results.xml](file:///e:/nasa/reports/e2e_results.xml) (`55,999 bytes`); `406 / 406` automated tests passing total (`391` pytest + `15` Rust).
- [x] **`/soicode` Remediation & Review Tests:** `18 / 18` passed in [tests/test_soicode_remediations.py](file:///e:/nasa/tests/test_soicode_remediations.py).
- [x] **Rust Cargo Tests:** `15 / 15` passed (`0` failed, `0` ignored), `nasa_rust.rust_health_check() == "ok"`.
- [x] **Ruff Static Lint & `app.py` Compile:** `All checks passed!` (`ruff 0.17.3`, exit `0`) and `py_compile app.py` (exit `0`).
- [x] **PDF Dossier Binary Check:** `18,239 bytes` nominal single-page (`%PDF-1.4`, `xref`, `%%EOF`) + automatic multi-page pagination (`/Count 2`, `MAT-ROW-060`) + hostile `NaN`/`±Inf`/malformed/`None` regression assertions.
- [x] **SEPA Slide Deck, Demo Script, App Branding & `.gitignore`:** Both `.pptx` decks (`58,625 bytes`) & `designs/flames-in-freefall` HTML slides verified at 7 English slides (`[01/07]`..`[07/07]`); `VIDEO_PITCH_SCRIPT_2MIN.md` Section 1 verified at 30s (`00:00 - 00:30`) English-subtitled live demo; `app.py` inline SVG Mission Patch (`0` Wikimedia/`NASA_logo.svg` matches), WCAG AA `#94A3B8` foreground contrast, `?tab=compare` `expand_compare_on_load` verified via `AppTest`, and `.gitignore` includes `target/`, `.cargo/`, `.agents/`.
- [x] **XSS HTML Escaping (`app.py`):** `html.escape(..., quote=True)` applied across `_custom_rows` (single-escaped from raw `cm_name`), `_fmt_online_block`, RAG fallback `parts`, citation card fields, `doc_rep_id`/`directive_code`/`badge_rag`/`top_doc` headers, chat history, and Tab 3/CoPilot fields (`cp_name`..`cp_morph`, `llm_provider`, `ai_insight_text`), verified via `AppTest`.
- [x] **Dynamic RAG Grounding, Upload Wiring & Regex Split (`rag_engine.py`, `app.py`):** `semantic_hits` uploaded chunks merged safely w/ `.get(...)` defaults; `generate_grounded_directive` dynamically grounded in `query`, `retrieved_docs`, and `chat_history`; `BLOCK 1/2/3` parsed via regex; `rh` unified to `:.1f` in `sync_state_to_query_params`.
- [x] **`T`/`RH` Sweep Propagation & Physics Parity (`app.py`, `physics_models.py`):** `T`/`RH` propagated through curves, sweeps, figures, and `evaluate_all_materials`; continuous `P` evaluation with Rust STP gate.
- [x] **Rust `NaN`/Portability, LLM Hardening & `SafeAlertProxy` (`src/*.rs`, `app.py`, `tests/conftest.py`):** `f64::NAN`/`!is_finite()` guards in `src/mesh.rs` & `src/physics.rs`; portable `resolve_data_dir` in `src/data_loader.rs`; `_api_key` excluded from `@st.cache_data` keys; `"gemini-2.5-flash"` replacing `"gemini-3.8-flash"`; OpenAI empty `choices` `api_error_notice`; `SafeAlertProxy` wired to real `app.py` contract.
- [x] **AST / RCE Safety:** Zero unsafe execution primitives in production Python modules; `gatherUsageStats = false`.

#### Remaining Open Engineering Items
- *None* — all actionable P0/P1/P2 `/soicode` audit items are resolved and verified. *(Note: Tier 1–4 legacy structural invariants in `tests/test_e2e_requirements.py` and intentionally preserved UI/CDN/PDF-1.4 spec tolerances remain documented in §5.2 item 7.)*
