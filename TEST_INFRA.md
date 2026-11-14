# E2E Test Infra: Microgravity Fire Safety Web Application Overhaul

**Specification Version:** 1.0.0  
**Target Environment:** Python 3.12+ / Pytest / uv / Streamlit 1.66+  
**Target Root:** `e:\nasa`  
**Classification:** NASA Technical Memorandum Flight Safety Test Architecture (Opaque-Box E2E)

---

## Test Philosophy

### 1.1 Opaque-Box & Requirement-Driven Architecture
The End-to-End (E2E) testing framework for the Microgravity Fire Safety Web Application (*Flames in Freefall / Bebo Ignis-0G*) operates strictly on an **opaque-box, requirement-driven paradigm**. 
- **Decoupled from Internal Layout:** Tests assert against external behavioral contracts, user interface outputs, public API contracts, and physical/mathematical invariants defined in `PROJECT.md` and `ORIGINAL_REQUEST.md`.
- **Zero White-Box Coupling:** Tests never assume private implementation names, unexported helper functions, or ephemeral local variables. Whether a calculation is executed through compiled Rust PyO3 bindings (`nasa_rust`) or pure-Python analytical mirrors, the observable interface and mathematical tolerances remain identical.
- **Progressive Testability:** The suite is structured hierarchically so that tests for foundational components (M1 Architecture, State, and UI) can execute immediately, while downstream milestones (M2 Alerting/3D, M3 Physics/Cool Flames, M4 Vector RAG, M5 Custom Materials/PDF Dossier) are validated as their interface contracts land, concluding with holistic scenario validation.

### 1.2 Formal Test Design Methodologies
The suite combines four disciplined test engineering disciplines:

1. **Category-Partition Method (Ostrand & Balcer):**
   Functional inputs across all features are partitioned into disjoint equivalence classes (e.g., microgravity $0g$, lunar $0.16g$, Martian $0.38g$, terrestrial $1.0g$, and hypergravity $2.0g-5.0g$; normoxic $21\% \text{ O}_2$ vs. hypobaric-enriched $34\% \text{ O}_2$ vs. pure $100\% \text{ O}_2$; nominal vs. critical fire threat tiers). Each partition maps to dedicated assertions.

2. **Boundary Value Analysis (BVA):**
   Combustion physics, environmental variables, and widget inputs exhibit non-linear physical phase transitions (e.g., blowoff velocity at $V_{eff} > 25.0\text{ cm/s}$, radiative quenching at $V_{eff} < 3.5\text{ cm/s}$, cool flame trigger boundary at $g \le 0.08$ and $V \le 4.0\text{ cm/s}$, critical alarm trigger at $\text{SFRS} > 85.0$). BVA establishes test probes directly at:
   $$\{ \text{min}-\epsilon, \, \text{min}, \, \text{min}+\epsilon, \, \text{nominal}, \, \text{threshold}-\epsilon, \, \text{threshold}, \, \text{threshold}+\epsilon, \, \text{max}-\epsilon, \, \text{max}, \, \text{max}+\epsilon \}$$

3. **Pairwise Combinatorial Testing (All-Pairs):**
   Multi-dimensional inputs $(g \times \text{O}_2 \times P \times V \times T \times RH \times \text{Material} \times \text{Preset})$ create a combinatorial explosion. Tier 3 applies orthogonal pairwise coverage ensuring every 2-way parameter interaction is exercised across valid operational ranges.

4. **Workload & Stress Testing:**
   Validates continuous operational stability under rapid parameter sweeps, heavy document ingestion, multi-turn conversational context growth, and concurrent PDF generation without memory leaks or UI frame drops.

---

## Feature Inventory

The following master inventory maps all 24 features specified in `PROJECT.md` against their origin in `ORIGINAL_REQUEST.md`, their test allocation across Tiers 1–4, and coverage indices.

| # | Feature Name | Description | Source | Tier 1 (Isolation) | Tier 2 (Boundary) | Tier 3 (Pairwise) | Tier 4 (Scenario) | Total Tests |
|---|---|---|---|:---:|:---:|:---:|:---:|:---:|
| 1 | **Tab Fragment Rerun Optimization** | Wrap tabs in `@st.fragment` & defer Plotly generation to eliminate full-page rerun lag | R1 | 5 | 5 | ✅ Pairwise | ✅ Scenario 1, 4 | 10+ |
| 2 | **F5 Session State Persistence** | Preserve telemetry & widget states across browser reload via query params & storage | R1 | 5 | 5 | ✅ Pairwise | ✅ Scenario 1, 2 | 10+ |
| 3 | **Deep-Linking URL Parameters** | Bidirectional read/write of `tab`, `preset`, `g`, `o2`, `p`, `v`, `t`, `rh` in URL | R1 | 5 | 5 | ✅ Pairwise | ✅ Scenario 2, 3 | 10+ |
| 4 | **Telemetry 404 Error Cleanup** | Opt-out of usage beaconing (`gatherUsageStats=false`) and local SVG/emoji favicon | R1 | 5 | 5 | ✅ Pairwise | ✅ Scenario 1 | 10+ |
| 5 | **Sub-1000px Responsive Layout** | CSS breakpoint `@media (max-width: 1024px)` auto-stacking columns without clipping | R1 | 5 | 5 | ✅ Pairwise | ✅ Scenario 3, 6 | 10+ |
| 6 | **Synchronized Direct Numeric Inputs** | Pair each slider with synchronized `st.number_input` supporting precise decimal typing | R2 | 5 | 5 | ✅ Pairwise | ✅ Scenario 2, 4 | 10+ |
| 7 | **Acronym Tooltip Library** | Hoverable plain-language tooltips for Da, Re, Pe, Ri, SFRS, MOC, and $\Delta\text{O}_2\%$ | R2 | 5 | 5 | ✅ Pairwise | ✅ Scenario 1, 5 | 10+ |
| 8 | **Visual Hierarchy & Contrast** | Soften cyan `#38BDF8`, ensure WCAG AA contrast $\ge 4.5:1$, deuteranopia dual-coding | R2 | 5 | 5 | ✅ Pairwise | ✅ Scenario 3, 6 | 10+ |
| 9 | **Audible Alarm Chimes** | Synthesize Web Audio NASA alarm warble (880Hz/1046Hz) when $\text{SFRS} > 85.0$ | R2 | 5 | 5 | ✅ Pairwise | ✅ Scenario 3, 6 | 10+ |
| 10 | **Pulsing Viewport Emergency Border** | Global CSS alert border pulse and emergency banner activation when $\text{SFRS} > 85.0$ | R2 | 5 | 5 | ✅ Pairwise | ✅ Scenario 3, 6 | 10+ |
| 11 | **3D WebGL Spherical Flame** | Three.js isotropic spherical flame with OrbitControls and heat dissipation particles | R5 | 5 | 5 | ✅ Pairwise | ✅ Scenario 1, 5 | 10+ |
| 12 | **Environmental T & RH Parameters** | Controls & physics for ambient temperature ($10\text{--}50^\circ\text{C}$) & humidity ($10\text{--}90\%$) | R4 | 5 | 5 | ✅ Pairwise | ✅ Scenario 4, 5 | 10+ |
| 13 | **Dynamic Cool Flame Oscillations** | 2-step NTC chemical kinetics ODE generating live $T(t)$ and $[\text{CO}](t)$ time-series | R4 | 5 | 5 | ✅ Pairwise | ✅ Scenario 5 | 10+ |
| 14 | **NASA-STD-6001B Calibration** | Formal calibration table & criteria mapping SFRS tiers to Test 1 & 2 standards | R4 | 5 | 5 | ✅ Pairwise | ✅ Scenario 2, 4 | 10+ |
| 15 | **Dense Semantic Vector Retrieval** | LSI TruncatedSVD dense semantic vector space with cosine relevance scoring | R3 | 5 | 5 | ✅ Pairwise | ✅ Scenario 4, 5 | 10+ |
| 16 | **Custom Paper & PDF Ingestion** | In-memory PDF/TXT parser with sliding-window chunking (350w/50w overlap) & indexing | R3 | 5 | 5 | ✅ Pairwise | ✅ Scenario 5, 6 | 10+ |
| 17 | **Multi-Turn Conversational Memory** | Context memory buffer retaining turns with conversational query reformulation | R3 | 5 | 5 | ✅ Pairwise | ✅ Scenario 1, 6 | 10+ |
| 18 | **Zero-Key Flight Safety Copilot** | Deterministic 3-part NASA flight safety directives (Kinetics, Standards, Protocol) | R3 | 5 | 5 | ✅ Pairwise | ✅ Scenario 1, 3 | 10+ |
| 19 | **Custom Composite Material Form** | Thermophysical inputs ($\rho, c_p, k, T_{ign}, MOC, HOC$) evaluating custom composites | R5 | 5 | 5 | ✅ Pairwise | ✅ Scenario 2, 4 | 10+ |
| 20 | **Side-by-Side Scenario Comparison** | Dual preset selector with metric diff cards, 5-axis polar Radar, and bar breakdown | R5 | 5 | 5 | ✅ Pairwise | ✅ Scenario 2, 3 | 10+ |
| 21 | **NASA-Style PDF Dossier Export** | ReportLab styled mission safety PDF dossier with parameters, scores, and tables | R5 | 5 | 5 | ✅ Pairwise | ✅ Scenario 6 | 10+ |
| 22 | **Comprehensive E2E Test Suite** | Master test orchestration suite across Tiers 1–4 with automated discovery | E2E | 5 | 5 | ✅ Pairwise | ✅ All | 10+ |
| 23 | **Final E2E Test Pass** | Verification harness asserting 100% test pass status across all tiers | Final | 5 | 5 | ✅ Pairwise | ✅ All | 10+ |
| 24 | **Adversarial Hardening (Tier 5)** | Extreme stress: NaN/Inf injection, XSS payloads, zero-division, malformed inputs | Final | 5 | 5 | ✅ Pairwise | ✅ All | 10+ |
| **Total** | **All 24 Features** | **Full Project Scope** | — | **120** | **120** | **24+** | **12+** | **≥ 276** |

---

## Test Architecture

### 3.1 Test Runner & Invocation Semantics
The testing framework uses standard `pytest` managed via the `uv` toolchain.
- **Master Test Command:**
  ```powershell
  uv run pytest tests/test_e2e_requirements.py -v --tb=short
  ```
- **Exit Code Semantics:**
  - `0`: All test cases passed successfully. Flawless requirement compliance.
  - `1`: One or more assertion tests failed. Execution completed without crashing.
  - `2`: Pytest test execution was interrupted by the user or system signal.
  - `3`: Internal pytest error during test execution.
  - `4`: Command-line usage or configuration syntax error.
  - `5`: No tests were collected matching the criteria.
- **Continuous Integration Reporting:**
  - Standard JUnit XML generation: `--junitxml=reports/e2e_results.xml`
  - Execution timeout enforcement: Individual unit tests timeout at 10.0 seconds; full suite must complete in $< 120$ seconds.

### 3.2 Directory and File Layout
```
e:\nasa\
├── tests\
│   ├── __init__.py
│   ├── conftest.py                       # Global test fixtures, session mocks, seeds, and test data
│   ├── test_e2e_requirements.py          # Master Suite Entry Point (Aggregator & Health Runner)
│   ├── test_e2e_tier1_features.py        # Tier 1: Isolated Feature Contract Tests (≥5 per feature, 120 tests)
│   ├── test_e2e_tier2_boundaries.py      # Tier 2: Boundary Value & Edge Limit Tests (≥5 per feature, 120 tests)
│   ├── test_e2e_tier3_pairwise.py        # Tier 3: Pairwise Combinatorial Interaction Tests (≥24 tests)
│   ├── test_e2e_tier4_scenarios.py       # Tier 4: Realistic End-to-End Mission Scenarios (≥6 major scenarios)
│   └── test_adversarial_physics_security.py # Legacy physics & security stress baseline
├── app.py                                # Primary Streamlit application
├── physics_models.py                     # Environmental physics, cool flame ODE, composite evaluation
├── rag_engine.py                         # Dense semantic vector search, PDF chunker, zero-key copilot
├── pdf_dossier.py                        # NASA Technical Memorandum PDF generator
├── threejs_flame.py                      # Interactive Three.js WebGL spherical flame generator
├── i18n.py                               # Bilingual dictionary, acronym tooltips, suppression matrix
├── .streamlit\
│   └── config.toml                       # Telemetry opt-out & server configuration
└── TEST_INFRA.md                         # This Master E2E Architecture Specification
```

### 3.3 Interface Contracts & Assertion Strategies
Tests perform verification through five explicit public contracts:

#### Contract 1: Telemetry State & URL Synchronization
- **Session State Contract:**
  The application maintains `st.session_state` keys with enforced types:
  - `gravity_val`: `float` $\in [0.0, 5.0]$
  - `o2_val`: `float` $\in [14.0, 100.0]$
  - `p_val`: `float` $\in [20.0, 150.0]$
  - `v_val`: `float` $\in [0.0, 50.0]$
  - `temp_val`: `float` $\in [10.0, 50.0]$
  - `rh_val`: `float` $\in [10.0, 90.0]$
  - `preset_selector`: `str` $\in \{\text{"ISS"}, \text{"LUNAR_ROVER"}, \text{"ARTEMIS"}, \text{"SPACESUIT"}, \text{"MARS"}, \text{"EARTH"}, \text{"CUSTOM"}\}$
  - `active_tab_id`: `str` $\in \{\text{"sim"}, \text{"morph"}, \text{"rag"}, \text{"matrix"}, \text{"research"}, \text{"compare"}\}$
  - `lang`: `str` $\in \{\text{"en"}, \text{"vi"}\}$
- **URL Query Parameters Contract:**
  Query parameters mirror state bidirectionally:
  `?tab=<str>&preset=<str>&g=<float>&o2=<float>&p=<float>&v=<float>&t=<float>&rh=<float>`
- **Assertion Strategy:** Mock `st.query_params` dictionary; verify that modifying `st.session_state` reflects immediately in query params, and injecting query params parses into valid numeric floats with fallback on invalid values.

#### Contract 2: Combustion Physics Core & Dynamic Models
- **Functions:**
  - `calculate_effective_moc(mat: dict, g: float, v: float, P: float, T: float = 21.0, RH: float = 45.0) -> float`
  - `calculate_flame_spread_rate(mat: dict, g: float, v: float, P: float, T: float, RH: float, o2: float, moc_eff: float) -> float`
  - `calculate_space_fire_risk_score(o2: float, moc_eff: float, spread_rate: float, hoc: float) -> float`
  - `solve_cool_flame_ntc_kinetics(T0: float, o2: float, P: float, t_max: float = 40.0, steps: int = 400) -> dict`
- **Assertion Strategy:**
  - Invariants: $\text{MOC}_{eff} \in [8.0, 60.0]$, $\text{SFRS} \in [5.0, 100.0]$, $\text{spread\_rate} \ge 0.0$.
  - Physical monotonicity: $\frac{\partial \text{MOC}}{\partial T} < 0$, $\frac{\partial \text{MOC}}{\partial RH} > 0$, $\frac{\partial \text{spread}}{\partial \text{O}_2} \ge 0$.
  - Cool flame output contract: Dictionary containing equal-length arrays `time` ($[0, t_{max}]$), `temperature` ($500\text{K} \le T \le 1600\text{K}$), and `co_ppm` (monotonically non-decreasing).

#### Contract 3: Dense Semantic Vector RAG & Offline Flight Copilot
- **Functions:**
  - `search_semantic(query: str, top_k: int = 3, threshold: float = 0.05) -> list[dict]`
  - `ingest_user_document(file_bytes: bytes, filename: str) -> int` (returns chunk count $> 0$)
  - `generate_grounded_directive(query: str, retrieved_docs: list[dict], chat_history: list[dict]) -> dict`
- **Assertion Strategy:**
  - Semantic synonym test: Assert queries without literal keywords ("second stage low temperature combustion") rank appropriate documents (`SCI-FLEX-2012-1593`) in top 3.
  - Chunking contract: Chunks must not exceed 400 words, must overlap by $\ge 30$ words, and must retain metadata (`doc_id`, `filename`, `page`).
  - Directive schema: Dictionary with keys `directive` (string containing 3 distinct sections: Combustion Kinetics, NASA-STD-6001B Compliance, Emergency Protocol) and `citations` (list of matching doc metadata).

#### Contract 4: Custom Composite Materials & Scenario Diff
- **Functions:**
  - `evaluate_custom_composite(props: dict, env: dict) -> dict`
  - `calculate_scenario_diff(env_a: dict, env_b: dict, material: dict) -> dict`
- **Assertion Strategy:**
  - Thermal inertia calculation: $I_{th} = k \cdot \rho \cdot c_p$.
  - Diff dictionary schema: Contains keys `delta_sfrs`, `delta_moc`, `delta_spread`, `hazard_transition`, and `radar_metrics` with 5 normalized axes.

#### Contract 5: NASA Technical Memorandum PDF Dossier Export
- **Function:**
  - `generate_mission_safety_dossier_pdf(scenario_data: dict, materials_data: list[dict]) -> bytes`
- **Assertion Strategy:**
  - Header check: Output bytes begin with standard PDF magic number `b"%PDF-1."`.
  - Non-empty buffer: Size $\ge 15,000$ bytes.
  - Structural integrity: Contains valid cross-reference table (`xref`) and trailer terminating with `b"%%EOF"`.

---

## Real-World Application Scenarios (Tier 4)

Tier 4 tests execute complete, realistic operational mission profiles. Each scenario simulates a distinct flight deck condition, evaluating the full pipeline from telemetry ingestion to risk assessment, alerting, and reporting.

| Scenario # | Mission Name | Environmental Parameters | Test Specimen | Key Physical & Operational Phenomenon | Expected Observable Outputs & Assertions |
|---|---|---|---|---|---|
| **1** | **ISS Nominal Microgravity Habitat** | $g = 0.0\text{g}$<br>$\text{O}_2 = 21.0\%$<br>$P = 101.3\text{ kPa}$<br>$V = 10.0\text{ cm/s}$<br>$T = 21.0^\circ\text{C}$<br>$RH = 45\%$ | PMMA Acrylic Rod (MAT-01) | Baseline microgravity forced convection; laminar boundary layer ($Re \approx 140$); ventilation keeps fuel above extinction; moderate flammability. | - $\text{MOC}_{eff} \in [14.0\%, 16.5\%]$<br>- $\text{SFRS} \in [45.0, 65.0]$ (HIGH risk)<br>- Audio Alarm: **OFF** ($\text{SFRS} < 85$)<br>- Screen Border: **Normal**<br>- Three.js: Isotropic sphere ($L/W = 1.0$) |
| **2** | **Artemis Exploration Atmosphere** | $g = 0.16\text{g}$ (Lunar)<br>$\text{O}_2 = 34.0\%$ (Enriched)<br>$P = 56.5\text{ kPa}$ (Hypobaric)<br>$V = 12.0\text{ cm/s}$<br>$T = 22.0^\circ\text{C}$<br>$RH = 35\%$ | Nomex HT90-40 (MAT-03) | Hypobaric oxygen-enriched habitat. Nomex passes in 1g normoxic air ($\text{MOC}_{1g} \approx 28.5\%$) but is tested under enriched atmosphere exceeding its threshold. | - $\text{MOC}_{eff} \in [24.0\%, 27.0\%]$<br>- Oxygen overage $\Delta\text{O}_2\% > 0$<br>- NASA-STD-6001B status: **FAIL / EXEMPTION REQUIRED**<br>- Scenario Diff vs ISS: $\Delta\text{SFRS} > +20.0$<br>- Radar polar axes reflect elevated oxygen hazard |
| **3** | **EVA Spacesuit Oxygen Breach** | $g = 0.0\text{g}$<br>$\text{O}_2 = 100.0\%$ (Pure $\text{O}_2$)<br>$P = 29.6\text{ kPa}$<br>$V = 18.0\text{ cm/s}$<br>$T = 18.0^\circ\text{C}$<br>$RH = 20\%$ | Cotton-Fiberglass Blend (MAT-02) | Catastrophic pure oxygen suit breach. Flame spread accelerates exponentially; heat release reaches maximum danger rating. | - $\text{SFRS} \ge 90.0$ (CRITICAL THREAT)<br>- Audio Alarm: **ACTIVE** (880/1046Hz chime component rendered)<br>- Screen Border: **ACTIVE** (`screenBorderEmergencyPulse` CSS rendered)<br>- Zero-Key Copilot: Immediate EVA Depress & Nitrogen Purge protocol |
| **4** | **Lunar Base Overheated Electronics Bay** | $g = 0.16\text{g}$<br>$\text{O}_2 = 21.0\%$<br>$P = 101.3\text{ kPa}$<br>$V = 3.0\text{ cm/s}$ (Low Flow)<br>$T = 42.0^\circ\text{C}$ (Overheated)<br>$RH = 15\%$ (Dry) | Kapton HN (MAT-10) & Ultem 1000 (MAT-05) | Elevated ambient temperature preheats polymers, decreasing MOC; low airflow nears ventilation paradox; dry air minimizes moisture heat sink. | - Kapton $\text{MOC}_{eff}$ shifts down by $\sim 1.05\%\text{ O}_2$<br>- Thermal preheating factor $> 1.05\times$<br>- Custom Material Evaluation confirms Kapton survival while unrated plastics ignite<br>- Vector search retrieves ECLSS thermal cooling directives |
| **5** | **Hydrocarbon Droplet Cool Flame Encounter** | $g = 0.0\text{g}$<br>$\text{O}_2 = 17.5\%$ (Vitiated)<br>$P = 101.3\text{ kPa}$<br>$V = 2.0\text{ cm/s}$<br>$T = 20.0^\circ\text{C}$<br>$RH = 40\%$ | Heptane Fuel Droplet (MAT-08) | Hot flame quenches radiatively at $t \sim 2\text{s}$; low-temperature alkylperoxy kinetics initiate invisible cool flame with NTC limit-cycle oscillations. | - `solve_cool_flame_ntc_kinetics` generates oscillations ($620\text{K} \leftrightarrow 760\text{K}$)<br>- Accumulated $[\text{CO}](t) > 250\text{ ppm}$ at $t=40\text{s}$<br>- Semantic RAG ranks FLEX-2 study (`SCI-FLEX-2012-1593`) #1<br>- Three.js component shows translucent pulsating shell |
| **6** | **Crew Emergency Suppression & PDF Dossier** | $g = 0.0\text{g}$<br>$\text{O}_2 = 28.0\%$<br>$P = 85.0\text{ kPa}$<br>$V = 8.0\text{ cm/s}$<br>$T = 26.0^\circ\text{C}$<br>$RH = 50\%$ | Multi-Material Flight Compartment (All 10 Materials) | Critical cabin fire incident requiring emergency water mist deployment, followed by generation of a NASA Mission Safety Technical Memorandum. | - Emergency matrix triggers Fine Water Mist protocol ($100\mu\text{m}$ droplets)<br>- `generate_mission_safety_dossier_pdf` returns $> 20\text{ KB}$ valid PDF<br>- PDF contains NASA Meatball header, all 10 ranked materials, SFRS callout box, and author signature |

---

## Coverage Thresholds

### 5.1 Test Tier Distribution
To guarantee comprehensive verification, the test suite enforces quantitative coverage thresholds across all 24 features:

```
================================================================================
                         E2E TEST SUITE PYRAMID
================================================================================
     ▲
    / \     Tier 4: Mission Scenarios (≥ 6 comprehensive workflows)
   /   \    Tier 3: Pairwise Interactions (≥ 24 combinatorial tests)
  /     \   Tier 2: Boundary Value Analysis (≥ 120 tests; 5 per feature)
 /       \  Tier 1: Feature Isolation Unit Tests (≥ 120 tests; 5 per feature)
/_________\ Tier 5: Adversarial Stress Hardening (Embedded across tiers)
================================================================================
```

### 5.2 Minimum Test Case Counts
- **Tier 1 (Feature Isolation):**
  - Minimum 5 distinct test cases for each of the 24 features:
  $$24 \times 5 = 120 \text{ tests minimum}$$
- **Tier 2 (Boundary Value Analysis):**
  - Minimum 5 distinct edge case and boundary limit tests for each feature:
  $$24 \times 5 = 120 \text{ tests minimum}$$
- **Tier 3 (Pairwise Combinatorial):**
  - Cross-feature multi-variable interaction tests covering all critical subsystem pairings:
  $$\ge 24 \text{ tests minimum}$$
- **Tier 4 (Realistic End-to-End Scenarios):**
  - Multi-step realistic mission operations covering all operational regimes:
  $$\ge 6 \text{ comprehensive scenarios (each containing multiple sub-assertions)}$$
- **Total Suite Minimum Count:**
  $$\text{Total} = 120 + 120 + 24 + 12 = \mathbf{276 \text{ test cases minimum}}$$

---

## 6. Detailed Tier-by-Tier Specification

### 6.1 Tier 1: Feature Isolation Tests (`tests/test_e2e_tier1_features.py`)
Each of the 24 features has at least 5 independent, isolated test methods:

#### Features 1–4: Architecture & Session Management
- `test_f01_tab_fragment_isolation`: Asserts tab renderers are decorated with `@st.fragment` and execute independently.
- `test_f01_deferred_figure_generation`: Asserts Plotly figure generation is deferred when a tab is inactive.
- `test_f01_rerun_execution_budget`: Asserts non-active tab execution completes in $< 5\text{ ms}$.
- `test_f01_state_preservation_across_fragments`: Asserts fragment execution does not mutate global sidebar state.
- `test_f01_fragment_error_containment`: Asserts an exception inside one fragment does not crash adjacent tabs.

- `test_f02_session_state_initialization`: Asserts all default telemetry keys exist in session state upon startup.
- `test_f02_f5_reload_state_recovery`: Asserts simulated reload restores custom values from storage/query dictionary.
- `test_f02_preset_selection_state_mutation`: Asserts selecting a preset updates all related telemetry variables.
- `test_f02_custom_override_flips_preset_to_custom`: Asserts manually editing a variable flips `preset_selector` to "CUSTOM".
- `test_f02_session_isolation_between_clients`: Asserts distinct session states do not leak between isolated mock instances.

- `test_f03_url_param_parsing`: Asserts query string `?g=0.16&o2=34.0` parses into matching float session values.
- `test_f03_url_param_serialization`: Asserts changing state values correctly produces serialized query parameters.
- `test_f03_tab_deep_link_navigation`: Asserts `?tab=matrix` activates the Emergency Matrix tab on initial render.
- `test_f03_invalid_query_param_fallback`: Asserts invalid query parameters (e.g. `?g=invalid`) fall back to default $0.0$.
- `test_f03_bidirectional_param_sync`: Asserts round-trip sync maintains numeric fidelity to 2 decimal places.

- `test_f04_telemetry_beacon_disabled`: Asserts `.streamlit/config.toml` contains `gatherUsageStats = false`.
- `test_f04_no_external_favicon_network_call`: Asserts `app.py` does not reference external HTTP WordPress favicons.
- `test_f04_local_favicon_asset_exists`: Asserts favicon uses local SVG data URI or standard Unicode emoji.
- `test_f04_headless_server_config_valid`: Asserts server runs in headless mode with CORS/XSRF protection appropriately set.
- `test_f04_console_error_free_mock_run`: Asserts running initialization generates zero HTTP 404 network warnings.

#### Features 5–8: UI/UX, Mobile Responsiveness & Accessibility
- `test_f05_responsive_breakpoint_1024px`: Asserts CSS includes `@media (max-width: 1024px)` responsive queries.
- `test_f05_column_autostack_rule`: Asserts `[data-testid="stHorizontalBlock"]` reflows to `flex-direction: column`.
- `test_f05_sidebar_responsive_width`: Asserts sidebar uses flexible `min(340px, 85vw)` on compact viewports.
- `test_f05_table_horizontal_scroll_wrapper`: Asserts data tables are wrapped in `.table-responsive` overflow containers.
- `test_f05_metric_cards_no_text_clipping`: Asserts metric cards retain readable min-widths without overflow clipping.

- `test_f06_numeric_input_slider_pairing`: Asserts each slider has an accompanying `st.number_input` widget.
- `test_f06_slider_to_number_synchronization`: Asserts changing slider updates the numeric input value.
- `test_f06_number_to_slider_synchronization`: Asserts typing into numeric input updates the slider value.
- `test_f06_decimal_precision_keyboard_entry`: Asserts entering decimal value `21.4` is preserved without rounding.
- `test_f06_numeric_input_bounds_clamping`: Asserts typing values out of range clamps safely to min/max boundaries.

- `test_f07_acronym_dictionary_completeness`: Asserts dictionary contains Da, Re, Pe, Ri, SFRS, MOC, and $\Delta\text{O}_2\%$.
- `test_f07_tooltip_plain_language_clarity`: Asserts tooltip text does not simply repeat the acronym and is $> 20$ chars.
- `test_f07_tooltip_html_wrapper`: Asserts helper renders valid HTML `<span>` with `data-tooltip` or title attribute.
- `test_f07_bilingual_tooltip_lookup`: Asserts acronym explanations are fully localized in English and Vietnamese.
- `test_f07_tooltip_accessibility_aria`: Asserts acronym elements include `aria-label` or accessible role tags.

- `test_f08_neon_contrast_toning`: Asserts primary accent is toned to `#38BDF8` and avoids high-glare `#00F2FF` text.
- `test_f08_wcag_contrast_ratio_text`: Asserts text-to-background contrast ratio meets or exceeds 4.5:1.
- `test_f08_deuteranopia_dual_coding_icons`: Asserts all risk badges include both icon and text, not color alone.
- `test_f08_colorblind_palette_separation`: Asserts safe (teal) and critical (crimson) maintain $\ge 30\%$ lightness delta.
- `test_f08_focus_visible_outline_contrast`: Asserts keyboard interactive elements have visible focus outlines.

#### Features 9–11: Multi-Sensory Alerting & 3D WebGL Visualization
- `test_f09_audio_alarm_trigger_condition`: Asserts audio synthesizer HTML is generated when $\text{SFRS} > 85.0$.
- `test_f09_audio_alarm_silent_when_nominal`: Asserts audio component is suppressed when $\text{SFRS} \le 85.0$.
- `test_f09_audio_alarm_frequencies_warble`: Asserts Web Audio script schedules NASA 880Hz and 1046Hz tones.
- `test_f09_audio_alarm_mute_toggle`: Asserts user mute toggle prevents audio synthesis injection.
- `test_f09_audio_context_resume_handling`: Asserts script checks `ctx.state === 'suspended'` and calls `resume()`.

- `test_f10_emergency_border_css_injection`: Asserts pulsing border CSS is injected when $\text{SFRS} > 85.0$.
- `test_f10_emergency_border_absent_when_safe`: Asserts pulsing border CSS is omitted when $\text{SFRS} \le 85.0$.
- `test_f10_emergency_banner_text_and_icon`: Asserts top warning banner displays critical warning and SFRS score.
- `test_f10_emergency_keyframe_animation`: Asserts CSS animation `screenBorderEmergencyPulse` is defined.
- `test_f10_emergency_deuteranopia_border`: Asserts border pulse combines high-luminance glow and distinct border stroke.

- `test_f11_threejs_component_html_generation`: Asserts Three.js HTML string contains canvas and script initialization.
- `test_f11_threejs_orbitcontrols_included`: Asserts Three.js script instantiates `OrbitControls` for 360° rotation.
- `test_f11_threejs_spherical_geometry_0g`: Asserts flame geometry creates isotropic sphere when $g \le 0.08$.
- `test_f11_threejs_particle_system_radiation`: Asserts particle system is instantiated for heat dissipation waves.
- `test_f11_threejs_extinguished_state`: Asserts component renders cooled contracted shell when $\text{O}_2 < \text{MOC}$.

#### Features 12–14: Combustion Physics & Standards Alignment
- `test_f12_temperature_input_controls`: Asserts temperature slider and numeric input exist ($10\text{--}50^\circ\text{C}$).
- `test_f12_humidity_input_controls`: Asserts humidity slider and numeric input exist ($10\text{--}90\%$).
- `test_f12_temperature_moc_reduction`: Asserts elevating temperature from $21^\circ\text{C}$ to $40^\circ\text{C}$ reduces MOC.
- `test_f12_humidity_moc_elevation`: Asserts elevating RH from $20\%$ to $80\%$ increases MOC due to vapor heat capacity.
- `test_f12_humidity_spread_retardation`: Asserts high humidity reduces flame spread rate.

- `test_f13_cool_flame_ode_solver_convergence`: Asserts `solve_cool_flame_ntc_kinetics` converges without NaN/Inf.
- `test_f13_cool_flame_ntc_temperature_bounds`: Asserts simulated cool flame oscillates in the $500\text{K}\text{--}900\text{K}$ regime.
- `test_f13_cool_flame_co_accumulation`: Asserts toxic $[\text{CO}]$ increases monotonically over time.
- `test_f13_cool_flame_trigger_envelope`: Asserts kinetics trigger only within low-g, low-flow cool flame envelope.
- `test_f13_cool_flame_output_time_series_length`: Asserts time series returns consistent step dimensions (400 points).

- `test_f14_nasa_std_6001b_table_structure`: Asserts calibration table includes Test 1, Test 2, and Flight Status columns.
- `test_f14_nasa_std_6001b_tier_mapping`: Asserts $\text{SFRS} < 20$ maps to Pass (Class A) and $\ge 70$ maps to Prohibited.
- `test_f14_nasa_std_6001b_test1_burn_length`: Asserts Test 1 criteria enforces 15 cm burn length threshold.
- `test_f14_nasa_std_6001b_test2_heat_release`: Asserts Test 2 criteria references peak heat release $< 100\text{ kW/m}^2$.
- `test_f14_nasa_std_6001b_waiver_conditions`: Asserts materials in High risk tier ($45\text{--}70$) specify waiver requirements.

#### Features 15–18: AI Assistant & Semantic Document Retrieval
- `test_f15_dense_lsi_vector_projection`: Asserts TruncatedSVD projects document vocabulary to dense latent space.
- `test_f15_semantic_synonym_retrieval`: Asserts non-literal query matches relevant documents above threshold.
- `test_f15_cosine_similarity_ranking`: Asserts retrieved documents are sorted in descending order of similarity score.
- `test_f15_retrieval_threshold_filtering`: Asserts documents with score $< 0.05$ are excluded from results.
- `test_f15_offline_retrieval_speed`: Asserts dense vector search completes in $< 15\text{ ms}$.

- `test_f16_pdf_file_ingestion`: Asserts uploading PDF extracts text and generates valid document chunks.
- `test_f16_text_file_ingestion`: Asserts uploading TXT/MD files parses cleanly without encoding errors.
- `test_f16_sliding_window_chunking`: Asserts chunks are 250–350 words with $\ge 30$-word contextual overlap.
- `test_f16_dynamic_index_updating`: Asserts uploaded chunks are immediately queryable via semantic search.
- `test_f16_uploaded_chunk_provenance_badge`: Asserts retrieved upload chunks include User Upload badge and metadata.

- `test_f17_chat_history_state_structure`: Asserts `rag_chat_history` stores turns with role, query, content, citations.
- `test_f17_conversational_query_reformulation`: Asserts follow-up query augments search with antecedent keywords.
- `test_f17_chat_dialogue_reset_button`: Asserts reset action clears conversation history without resetting chamber state.
- `test_f17_multi_turn_turn_limit`: Asserts memory safely manages at least 10 consecutive dialogue turns.
- `test_f17_chat_rendering_alternating_bubbles`: Asserts user questions and copilot answers render in distinct styling.

- `test_f18_zero_key_directive_structure`: Asserts offline answer contains all 3 NASA directive blocks.
- `test_f18_zero_key_kinetics_block`: Asserts Block 1 details combustion kinetics and dimensionless numbers.
- `test_f18_zero_key_standards_block`: Asserts Block 2 cites NASA-STD-6001B Test 1/2 flammability certification.
- `test_f18_zero_key_tactical_protocol`: Asserts Block 3 specifies tactical emergency steps ($T+0\text{s}, T+15\text{s}, T+60\text{s}$).
- `test_f18_verbatim_document_citations`: Asserts response includes docket IDs and document report numbers.

#### Features 19–21: Custom Materials, Comparison & PDF Export
- `test_f19_custom_material_input_schema`: Asserts form accepts $\rho, c_p, k, T_{ign}, MOC, HOC$.
- `test_f19_thermal_inertia_calculation`: Asserts thermal inertia $I_{th} = k \cdot \rho \cdot c_p$ is computed correctly.
- `test_f19_de_ris_spread_rate_estimation`: Asserts base spread rate derives accurately from thermal properties.
- `test_f19_custom_material_dynamic_evaluation`: Asserts custom material evaluates against active chamber atmosphere.
- `test_f19_custom_material_injection`: Asserts new material appends to active DataFrame and specimen dropdowns.

- `test_f20_dual_scenario_selection`: Asserts baseline and challenger presets can be selected simultaneously.
- `test_f20_metric_diff_calculation`: Asserts $\Delta\text{SFRS}, \Delta\text{MOC}, \Delta\text{spread}$ compute correctly.
- `test_f20_radar_chart_data_structure`: Asserts polar radar chart includes 5 distinct normalized hazard axes.
- `test_f20_hazard_tier_transition_card`: Asserts diff view highlights transitions between safety tiers.
- `test_f20_waterfall_bar_breakdown`: Asserts score component differences render in bar breakdown.

- `test_f21_pdf_magic_bytes_header`: Asserts PDF generator output begins with `%PDF-1.`.
- `test_f21_pdf_buffer_size`: Asserts generated PDF dossier exceeds 15 KB in size.
- `test_f21_pdf_structure_and_trailer`: Asserts document contains valid cross-reference table and `%%EOF`.
- `test_f21_pdf_contains_scenario_parameters`: Asserts PDF binary embeds text for $g, \text{O}_2, P, V, T, RH$.
- `test_f21_pdf_contains_materials_table`: Asserts PDF includes tabular records for evaluated materials.

#### Features 22–24: Test Harness, Verification Pass & Adversarial Hardening
- `test_f22_master_runner_discovery`: Asserts `test_e2e_requirements.py` discovers all sub-tier test files.
- `test_f22_fixture_isolation_setup`: Asserts fixtures in `conftest.py` instantiate cleanly without side effects.
- `test_f22_test_metadata_annotations`: Asserts all tests carry tier markers (`@pytest.mark.tier1`, etc.).
- `test_f22_xml_report_generation`: Asserts test execution can generate valid JUnit XML results.
- `test_f22_execution_time_tracking`: Asserts test runner tracks execution durations across test modules.

- `test_f23_suite_pass_threshold_100_pct`: Asserts zero test failures across all registered test items.
- `test_f23_no_skipped_or_ignored_tests`: Asserts no core requirement tests are marked skipped without justification.
- `test_f23_exit_code_zero_on_completion`: Asserts pytest process terminates with exit code 0.
- `test_f23_deterministic_reproducibility`: Asserts two consecutive runs produce identical pass/fail outputs.
- `test_f23_no_facade_or_dummy_assertions`: Asserts test logic exercises real calculations and rejects invalid mocks.

- `test_f24_adversarial_nan_inf_immunity`: Asserts physics functions reject or clamp `NaN`, `+Inf`, and `-Inf`.
- `test_f24_adversarial_extreme_hypergravity`: Asserts gravity $g = 100.0$ does not cause numeric overflow.
- `test_f24_adversarial_xss_injection`: Asserts document titles and custom material names escape `<script>` tags.
- `test_f24_adversarial_empty_corpus_search`: Asserts vector search handles empty document corpus gracefully.
- `test_f24_adversarial_zero_division_pressure`: Asserts chamber pressure $P = 0.0\text{ kPa}$ does not trigger zero division.

---

### 6.2 Tier 2: Boundary Value Analysis Tests (`tests/test_e2e_tier2_boundaries.py`)
Each of the 24 features is subjected to 5 extreme boundary conditions:
- **Gravity Boundaries:** $g \in \{0.0, 10^{-6}, 0.08, 0.16, 0.38, 1.0, 5.0\}$. Tests exact transitions at microgravity cutoff ($0.08g$), lunar ($0.16g$), and Martian ($0.38g$).
- **Oxygen Boundaries:** $\text{O}_2 \in \{14.0\%, 20.9\%, 21.0\%, 34.0\%, 99.9\%, 100.0\%\}$. Tests hypoxia cutoff, normoxic air, Artemis exploration enrichment, and pure oxygen.
- **Pressure Boundaries:** $P \in \{20.0, 25.0, 29.6, 56.5, 101.3, 105.0, 150.0\}\text{ kPa}$. Tests extreme hypobaric suit atmosphere up to hyperbaric chamber limits.
- **Ventilation Boundaries:** $V \in \{0.0, 0.5, 3.49, 3.51, 24.9, 25.1, 50.0\}\text{ cm/s}$. Probes exact inflection points for radiative quenching ($3.5\text{ cm/s}$) and convective blowoff ($25.0\text{ cm/s}$).
- **Temperature Boundaries:** $T \in \{10.0, 10.1, 21.0, 41.9, 42.1, 50.0\}^\circ\text{C}$. Probes chilling limit, nominal ECLSS, overheated electronics, and thermal stress ceiling.
- **Humidity Boundaries:** $RH \in \{10.0, 10.1, 45.0, 89.9, 90.0\}\%$. Probes dry static discharge risk up to high condensation quenching.
- **Threat Score Alert Boundary:** $\text{SFRS} \in \{84.9, 85.0, 85.1\}$. Tests exact transition where alarm chime and pulsing emergency border switch from dormant to active.
- **Document Chunking Boundary:** Files with 0 bytes, 1 word, exactly 350 words, 351 words, and $10^6$ words.
- **Conversational Memory Turn Boundary:** 0 turns, 1 turn, 10 turns, and 50 turns.

---

### 6.3 Tier 3: Pairwise Combinatorial Tests (`tests/test_e2e_tier3_pairwise.py`)
Tier 3 tests exercise multi-factor interactions across the 24 features using an orthogonal array covering:
1. `(g=0.0, O2=21.0, V=2.0)` $\rightarrow$ Radiative quenching vs. cool flame trigger.
2. `(g=0.0, O2=100.0, V=10.0)` $\rightarrow$ Pure oxygen microgravity rapid spread with critical alarm.
3. `(g=0.16, O2=34.0, P=56.5)` $\rightarrow$ Artemis Exploration Atmosphere flammability threshold.
4. `(g=0.38, O2=21.0, T=40.0)` $\rightarrow$ Martian gravity with elevated temperature preheating.
5. `(g=1.0, O2=14.0, V=0.0)` $\rightarrow$ Terrestrial hypoxia with stagnant airflow self-extinction.
6. `(g=0.0, T=50.0, RH=90.0)` $\rightarrow$ Opposing effects of maximum thermal preheating vs. maximum moisture dilution.
7. `(g=0.16, V=35.0, P=25.0)` $\rightarrow$ High-speed ventilation blowoff in lunar hypobaric atmosphere.
8. `(SFRS > 85, Muted=True)` $\rightarrow$ Visual alert triggers while audio remains suppressed.
9. `(SFRS > 85, Muted=False)` $\rightarrow$ Both visual alert and audio alarm chime trigger simultaneously.
10. `(Custom Material, Artemis Atmosphere)` $\rightarrow$ Custom composite evaluated under enriched lunar preset.
11. `(Custom Material, Extreme Temperature 50°C)` $\rightarrow$ Custom material ignition sensitivity under thermal stress.
12. `(Uploaded PDF, Zero-Key Copilot)` $\rightarrow$ Ingested document cited directly in deterministic 3-part directive.
13. `(Multi-Turn Chat, Scenario Preset Switch)` $\rightarrow$ Chat memory persists across scenario preset modifications.
14. `(Side-by-Side Comparison, Custom Material)` $\rightarrow$ Custom material evaluated in dual-scenario radar comparison.
15. `(PDF Dossier Export, Overheated Lunar Preset)` $\rightarrow$ Mission safety PDF generated under high-risk lunar condition.
16. `(Sub-1000px Viewport, Dual Scenario Compare)` $\rightarrow$ Comparison view stacks cleanly without horizontal scroll.
17. `(Sub-1000px Viewport, 3D WebGL Flame)` $\rightarrow$ Three.js canvas auto-resizes to viewport width.
18. `(Direct Numeric Input, URL Parameter Deep Link)` $\rightarrow$ Numeric input reflects URL parameter updates without lag.
19. `(Tab Fragment Switching, Audio Alarm Active)` $\rightarrow$ Emergency state persists across tab navigation.
20. `(Cool Flame Kinetics, High Oxygen 40%)` $\rightarrow$ Transition from cool flame oscillation to hot runaway flame.
21. `(NASA-STD-6001B Calibration, Custom Low-MOC Material)` $\rightarrow$ Immediate flight prohibition determination.
22. `(Dense Vector RAG, Bilingual Query in Vietnamese)` $\rightarrow$ Semantic retrieval operates across localized queries.
23. `(F5 Reload, Active Comparison Sub-tab)` $\rightarrow$ Deep link preserves active comparison tab and preset selections.
24. `(Telemetry Opt-Out, Headless Mode)` $\rightarrow$ Zero network calls executed during automated headless evaluation.

---

### 6.4 Tier 4: Realistic Mission Scenarios (`tests/test_e2e_tier4_scenarios.py`)
Each of the 6 detailed scenarios in Section 4 is implemented as an end-to-end mission pipeline test:
1. `test_scenario_01_iss_nominal_microgravity_baseline()`
2. `test_scenario_02_artemis_exploration_atmosphere_nomex_qualification()`
3. `test_scenario_03_eva_spacesuit_oxygen_breach_critical_alarm()`
4. `test_scenario_04_lunar_base_overheated_electronics_bay()`
5. `test_scenario_05_microgravity_droplet_cool_flame_encounter()`
6. `test_scenario_06_crew_emergency_suppression_and_pdf_dossier()`

---

## 7. Verification and Audit Matrix

### 7.1 Independent Auditor Verification Commands
An independent auditor or evaluator can verify the entire test infrastructure specification and its corresponding implementations using the following verification protocol:

```powershell
# 1. Verify environment dependencies and toolchain
uv --version
uv run python --version

# 2. Execute legacy physics & adversarial security suite
uv run pytest tests/test_adversarial_physics_security.py -v -k "not test_live_streamlit_server_http_health"

# 3. Execute master E2E test suite (Tiers 1-4)
uv run pytest tests/test_e2e_requirements.py -v --tb=short

# 4. Verify Rust backend test invariants (if cargo available)
cargo test -- --nocapture

# 5. Verify PDF generation and header compliance
uv run python -c "
import pdf_dossier
pdf_bytes = pdf_dossier.generate_mission_safety_dossier_pdf(
    {'mission': 'ISS', 'g': 0.0, 'o2': 21.0, 'p': 101.3, 'v': 10.0, 't': 21.0, 'rh': 45.0, 'sfrs': 52.4, 'tier': 'HIGH'},
    [{'material_name': 'PMMA', 'sfrs': 52.4, 'moc_eff': 15.2, 'spread_rate': 0.85, 'flammability': 'Flammable'}]
)
assert pdf_bytes.startswith(b'%PDF-1.'), 'Invalid PDF header'
assert len(pdf_bytes) > 15000, 'PDF buffer too small'
print(f'PDF Dossier verification PASSED: {len(pdf_bytes)} bytes')
"
```

### 7.2 Strict Integrity & Anti-Cheating Invariants
- **No Facade Tests:** Every test must execute the underlying mathematical or logical functions. Assertions such as `assert True` or mock functions returning hardcoded results without computing the state are classified as integrity violations.
- **Authoritative Oracles:** Expected physical values are derived directly from NASA technical reports (NASA-STD-6001B, NASA TP-2015-218570, NASA TM-2020-5008246).
- **Slide Deck Protection:** No test or script shall touch, alter, or rename `Flames_in_Freefall_Presentation.pptx`, `Flames_in_Freefall_Presentation_v5.pptx`, `build_v2_deck.py`, `build_v4_deck.py`, or `generate_deck.py`.

---
*End of Test Infrastructure Architecture Specification (`TEST_INFRA.md`).*
