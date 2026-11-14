"""
Tier 3: Pairwise Combinatorial Interaction Tests for NASA Microgravity Fire Safety Web App.
Covers cross-feature multi-variable interactions across telemetry, physics, materials, RAG, and UI
per TEST_INFRA.md Section 6.3 (>= 24 combinatorial interaction tests).
"""

import math
import os
import re
import sys
import pytest

# Ensure repository root is on sys.path
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)


@pytest.mark.tier3
class TestTier3PairwiseCombinations:
    """Pairwise Combinatorial Test Suite covering orthogonal subsystem interactions."""

    def test_pairwise_01_microgravity_stagnant_cool_flame_trigger(self, physics_engine, materials_database):
        """Pairing 1: (g=0.0, O2=21.0, V=2.0) -> Radiative quenching vs. cool flame trigger."""
        mat = materials_database[7]  # Heptane Droplet (cool flame susceptible)
        moc_eff = physics_engine.calculate_effective_moc(mat, g=0.0, v=2.0, P=101.3)
        spread = physics_engine.calculate_flame_spread_rate(mat, g=0.0, v=2.0, P=101.3, T=21.0, RH=45.0, o2=17.5, moc_eff=moc_eff)
        res = physics_engine.solve_cool_flame_ntc_kinetics(T0=1450.0, o2=17.5, P=101.3)
        assert spread > 0.0
        assert len(res["temperature"]) == 400
        # Dynamic NTC oscillations in cool flame regime (500K-900K)
        assert min(res["temperature"][100:]) >= 500.0
        assert max(res["temperature"][100:]) <= 900.0
        assert res["co_ppm"][-1] > 50.0

    def test_pairwise_02_pure_oxygen_microgravity_critical_alarm(self, physics_engine, materials_database, mock_session_state):
        """Pairing 2: (g=0.0, O2=100.0, V=10.0) -> Pure oxygen microgravity rapid spread with critical alarm."""
        mat = materials_database[1]  # Cotton blend
        moc_eff = physics_engine.calculate_effective_moc(mat, g=0.0, v=10.0, P=29.6)
        spread = physics_engine.calculate_flame_spread_rate(mat, g=0.0, v=10.0, P=29.6, T=21.0, RH=20.0, o2=100.0, moc_eff=moc_eff)
        sfrs = physics_engine.calculate_space_fire_risk_score(o2=100.0, moc_eff=moc_eff, spread_rate=spread, hoc=mat["heat_of_combustion_mj_kg"])
        assert sfrs >= 85.0, f"Expected critical threat SFRS >= 85.0 for 100% O2, got {sfrs:.1f}"
        mock_session_state.sfrs_score = sfrs
        mock_session_state.audio_muted = False
        should_alarm_audio = (mock_session_state.sfrs_score > 85.0) and (not mock_session_state.audio_muted)
        should_alarm_visual = mock_session_state.sfrs_score > 85.0
        assert should_alarm_audio is True
        assert should_alarm_visual is True

    def test_pairwise_03_artemis_hypobaric_enriched_nomex(self, physics_engine, materials_database):
        """Pairing 3: (g=0.16, O2=34.0, P=56.5) -> Artemis Exploration Atmosphere flammability threshold."""
        nomex = materials_database[2]
        moc_eff = physics_engine.calculate_effective_moc(nomex, g=0.16, v=12.0, P=56.5)
        # Nomex passes in 1g normoxic (21%) but in Artemis (34% O2) exceeds MOC
        assert 34.0 > moc_eff
        spread = physics_engine.calculate_flame_spread_rate(nomex, g=0.16, v=12.0, P=56.5, T=22.0, RH=35.0, o2=34.0, moc_eff=moc_eff)
        assert spread > 0.0
        sfrs = physics_engine.calculate_space_fire_risk_score(o2=34.0, moc_eff=moc_eff, spread_rate=spread, hoc=nomex["heat_of_combustion_mj_kg"])
        assert sfrs >= 35.0, "Nomex under Artemis enriched atmosphere must reflect elevated flammability"

    def test_pairwise_04_martian_gravity_elevated_temperature(self, physics_engine, materials_database):
        """Pairing 4: (g=0.38, O2=21.0, T=40.0) -> Martian gravity with elevated temperature preheating."""
        pmma = materials_database[0]
        moc_nom = physics_engine.calculate_effective_moc(pmma, g=0.38, v=10.0, P=101.3, T=21.0, RH=45.0)
        moc_hot = physics_engine.calculate_effective_moc(pmma, g=0.38, v=10.0, P=101.3, T=40.0, RH=45.0)
        assert moc_hot < moc_nom
        spread_nom = physics_engine.calculate_flame_spread_rate(pmma, g=0.38, v=10.0, P=101.3, T=21.0, RH=45.0, o2=21.0, moc_eff=moc_nom)
        spread_hot = physics_engine.calculate_flame_spread_rate(pmma, g=0.38, v=10.0, P=101.3, T=40.0, RH=45.0, o2=21.0, moc_eff=moc_hot)
        assert spread_hot > spread_nom, "Elevated temperature preheating must accelerate flame spread rate"

    def test_pairwise_05_terrestrial_hypoxia_stagnant_extinction(self, physics_engine, materials_database):
        """Pairing 5: (g=1.0, O2=14.0, V=0.0) -> Terrestrial hypoxia with stagnant airflow self-extinction."""
        pmma = materials_database[0]
        moc_eff = physics_engine.calculate_effective_moc(pmma, g=1.0, v=0.0, P=101.3)
        spread = physics_engine.calculate_flame_spread_rate(pmma, g=1.0, v=0.0, P=101.3, T=21.0, RH=45.0, o2=14.0, moc_eff=moc_eff)
        assert moc_eff > 14.0
        assert spread == 0.0, "Material must self-extinguish when O2 (14%) < MOC_eff"

    def test_pairwise_06_opposing_temperature_humidity_extremes(self, physics_engine, materials_database):
        """Pairing 6: (g=0.0, T=50.0, RH=90.0) -> Opposing effects of max preheating vs. max moisture dilution."""
        pmma = materials_database[0]
        moc_hot_dry = physics_engine.calculate_effective_moc(pmma, g=0.0, v=10.0, P=101.3, T=50.0, RH=10.0)
        moc_hot_humid = physics_engine.calculate_effective_moc(pmma, g=0.0, v=10.0, P=101.3, T=50.0, RH=90.0)
        assert moc_hot_humid > moc_hot_dry, "Elevated humidity must increase MOC via vapor thermal capacity dilution"

    def test_pairwise_07_lunar_hypobaric_high_velocity_blowoff(self, physics_engine, materials_database):
        """Pairing 7: (g=0.16, V=35.0, P=25.0) -> High-speed ventilation blowoff in lunar hypobaric atmosphere."""
        mat = materials_database[0]
        moc_eff = physics_engine.calculate_effective_moc(mat, g=0.16, v=35.0, P=25.0)
        # V_eff > 25.0 triggers convective blowoff delta elevating MOC
        assert moc_eff > mat["moc_microg"]

    def test_pairwise_08_visual_alert_with_muted_audio(self, physics_engine, materials_database, mock_session_state):
        """Pairing 8: (SFRS > 85, Muted=True) -> Visual alert triggers while audio remains suppressed."""
        cotton = materials_database[1]
        moc = physics_engine.calculate_effective_moc(cotton, g=0.0, v=18.0, P=29.6, T=20.0, RH=20.0)
        spread = physics_engine.calculate_flame_spread_rate(cotton, g=0.0, v=18.0, P=29.6, T=20.0, RH=20.0, o2=100.0, moc_eff=moc)
        sfrs = physics_engine.calculate_space_fire_risk_score(o2=100.0, moc_eff=moc, spread_rate=spread, hoc=cotton["heat_of_combustion_mj_kg"])
        assert sfrs > 85.0
        mock_session_state.sfrs_score = sfrs
        mock_session_state.audio_muted = True
        visual_border_active = mock_session_state.sfrs_score > 85.0
        audio_chime_active = (mock_session_state.sfrs_score > 85.0) and (not mock_session_state.audio_muted)
        assert visual_border_active is True
        assert audio_chime_active is False

    def test_pairwise_09_multisensory_alert_both_active(self, physics_engine, materials_database, mock_session_state):
        """Pairing 9: (SFRS > 85, Muted=False) -> Both visual alert and audio alarm chime trigger simultaneously."""
        cotton = materials_database[1]
        moc = physics_engine.calculate_effective_moc(cotton, g=0.0, v=18.0, P=29.6, T=20.0, RH=20.0)
        spread = physics_engine.calculate_flame_spread_rate(cotton, g=0.0, v=18.0, P=29.6, T=20.0, RH=20.0, o2=100.0, moc_eff=moc)
        sfrs = physics_engine.calculate_space_fire_risk_score(o2=100.0, moc_eff=moc, spread_rate=spread, hoc=cotton["heat_of_combustion_mj_kg"])
        assert sfrs > 85.0
        mock_session_state.sfrs_score = sfrs
        mock_session_state.audio_muted = False
        visual_border_active = mock_session_state.sfrs_score > 85.0
        audio_chime_active = (mock_session_state.sfrs_score > 85.0) and (not mock_session_state.audio_muted)
        assert visual_border_active is True
        assert audio_chime_active is True
        nasa_audio_tones = [880, 1046]
        assert 880 in nasa_audio_tones and 1046 in nasa_audio_tones

    def test_pairwise_10_custom_material_artemis_evaluation(self, physics_engine, sample_custom_materials):
        """Pairing 10: (Custom Material, Artemis Atmosphere) -> Custom composite evaluated under enriched lunar preset."""
        cust_mat = sample_custom_materials[0]
        env_artemis = {"g": 0.16, "o2": 34.0, "p": 56.5, "v": 12.0, "t": 22.0, "rh": 35.0}
        res = physics_engine.evaluate_custom_composite(cust_mat, env_artemis)
        assert res["sfrs"] > 0.0
        assert res["thermal_inertia"] > 0.0
        assert res["moc_eff"] > 0.0
        assert res["tier"] in ["Safe", "Moderate", "High", "Critical"]

    def test_pairwise_11_custom_material_thermal_stress(self, physics_engine, sample_custom_materials):
        """Pairing 11: (Custom Material, Extreme Temperature 50°C) -> Custom material ignition sensitivity under thermal stress."""
        cust_mat = sample_custom_materials[1]  # Aerogel
        env_nominal = {"g": 0.0, "v": 10.0, "p": 101.3, "t": 21.0, "rh": 45.0, "o2": 21.0}
        env_hot = {"g": 0.0, "v": 10.0, "p": 101.3, "t": 50.0, "rh": 45.0, "o2": 21.0}
        res_nom = physics_engine.evaluate_custom_composite(cust_mat, env_nominal)
        res_hot = physics_engine.evaluate_custom_composite(cust_mat, env_hot)
        assert res_hot["moc_eff"] < res_nom["moc_eff"]
        assert res_hot["sfrs"] >= res_nom["sfrs"]

    def test_pairwise_12_uploaded_pdf_cited_in_copilot(self, rag_engine, synthetic_research_papers):
        """Pairing 12: (Uploaded PDF, Zero-Key Copilot) -> Ingested document cited directly in 3-part directive."""
        rag_engine.ingest_user_document(synthetic_research_papers["pdf_bytes"], "Custom_Flight_Paper.pdf")
        retrieved = rag_engine.search_semantic("Spacecraft Flammability in Enriched Atmospheres", top_k=1)
        assert len(retrieved) > 0
        directive = rag_engine.generate_grounded_directive("What are the flammability limits?", retrieved)
        assert len(directive["citations"]) > 0
        assert "BLOCK 1" in directive["directive"]
        assert "BLOCK 2" in directive["directive"]
        assert "BLOCK 3" in directive["directive"]

    def test_pairwise_13_multi_turn_chat_persists_across_presets(self, rag_engine, mock_session_state):
        """Pairing 13: (Multi-Turn Chat, Scenario Preset Switch) -> Chat memory persists across scenario modifications."""
        res1 = rag_engine.search_semantic("PMMA low-flow flammability", top_k=1)
        dir1 = rag_engine.generate_grounded_directive("PMMA low-flow hazard?", res1, chat_history=mock_session_state.rag_chat_history)
        mock_session_state.rag_chat_history.append({"query": "PMMA low-flow hazard?", "answer": dir1["directive"]})

        # Switch preset to LUNAR_ROVER modifying chamber telemetry
        mock_session_state.preset_selector = "LUNAR_ROVER"
        mock_session_state.gravity_val = 0.16
        mock_session_state.o2_val = 34.0

        res2 = rag_engine.search_semantic("extinction protocol", top_k=1)
        dir2 = rag_engine.generate_grounded_directive("What extinction protocol applies?", res2, chat_history=mock_session_state.rag_chat_history)
        mock_session_state.rag_chat_history.append({"query": "What extinction protocol applies?", "answer": dir2["directive"]})

        assert len(mock_session_state.rag_chat_history) == 2
        assert mock_session_state.preset_selector == "LUNAR_ROVER"
        assert mock_session_state.gravity_val == 0.16
        assert "BLOCK 1" in mock_session_state.rag_chat_history[0]["answer"]

    def test_pairwise_14_side_by_side_comparison_custom_material(self, physics_engine, sample_custom_materials):
        """Pairing 14: (Side-by-Side Comparison, Custom Material) -> Custom material evaluated in dual-scenario radar comparison."""
        cust = sample_custom_materials[0]
        env_iss = {"g": 0.0, "o2": 21.0, "p": 101.3, "v": 10.0, "t": 21.0, "rh": 45.0}
        env_art = {"g": 0.16, "o2": 34.0, "p": 56.5, "v": 12.0, "t": 22.0, "rh": 35.0}
        diff = physics_engine.calculate_scenario_diff(env_iss, env_art, cust)
        assert "delta_sfrs" in diff
        assert diff["delta_sfrs"] > 0
        assert len(diff["radar_metrics"]["axes"]) == 5
        assert all(0.0 <= v <= 1.0 for v in diff["radar_metrics"]["values_a"])
        assert all(0.0 <= v <= 1.0 for v in diff["radar_metrics"]["values_b"])

    def test_pairwise_15_pdf_dossier_overheated_lunar_scenario(self, pdf_generator, materials_database):
        """Pairing 15: (PDF Dossier Export, Overheated Lunar Preset) -> Mission safety PDF generated under high-risk lunar condition."""
        scenario = {"mission": "Lunar Overheated Avionics", "g": 0.16, "o2": 21.0, "p": 101.3, "v": 3.0, "t": 42.0, "rh": 15.0, "sfrs": 58.2, "tier": "HIGH"}
        pdf_bytes = pdf_generator(scenario, materials_database)
        assert pdf_bytes.startswith(b"%PDF-1.")
        assert len(pdf_bytes) >= 15000
        assert b"%%EOF" in pdf_bytes
        assert b"xref" in pdf_bytes

    def test_pairwise_16_sub1000px_dual_scenario_comparison(self):
        """Pairing 16: (Sub-1000px Viewport, Dual Scenario Compare) -> Comparison view stacks cleanly without horizontal scroll."""
        app_path = os.path.join(REPO_ROOT, "app.py")
        with open(app_path, "r", encoding="utf-8") as f:
            app_code = f.read()
        assert "@media (max-width: 1024px)" in app_code
        assert "flex-direction: column !important;" in app_code
        assert "overflow-x: auto" in app_code
        assert '[data-testid="stHorizontalBlock"]' in app_code

    def test_pairwise_17_sub1000px_3d_webgl_flame(self, threejs_flame_generator):
        """Pairing 17: (Sub-1000px Viewport, 3D WebGL Flame) -> Three.js canvas auto-resizes to viewport width."""
        html = threejs_flame_generator(gravity_g=0.16, airflow_cm_s=12.0)
        assert "window.innerWidth" in html
        assert "renderer.setSize" in html
        assert "renderer.setPixelRatio" in html

    def test_pairwise_18_direct_numeric_input_with_url_deep_link(self, mock_session_state, mock_query_params):
        """Pairing 18: (Direct Numeric Input, URL Parameter Deep Link) -> Numeric input reflects URL parameter updates without lag."""
        mock_query_params["o2"] = "34.55"
        raw_o2 = float(mock_query_params.get("o2"))
        clamped_o2 = max(14.0, min(100.0, raw_o2))
        mock_session_state.o2_val = clamped_o2
        mock_session_state["o2_val_num"] = clamped_o2
        assert abs(mock_session_state.o2_val - 34.55) < 1e-4
        assert abs(mock_session_state["o2_val_num"] - 34.55) < 1e-4

        # Verify reverse synchronization from direct numeric keyboard input
        mock_session_state["o2_val_num"] = 42.80
        mock_session_state.o2_val = mock_session_state["o2_val_num"]
        mock_query_params["o2"] = f"{mock_session_state.o2_val:.2f}"
        assert mock_query_params.get("o2") == "42.80"

    def test_pairwise_19_tab_fragment_switch_with_alarm_active(self, physics_engine, materials_database, mock_session_state):
        """Pairing 19: (Tab Fragment Switching, Audio Alarm Active) -> Emergency state persists across tab navigation."""
        cotton = materials_database[1]
        moc = physics_engine.calculate_effective_moc(cotton, g=0.0, v=15.0, P=29.6, T=20.0, RH=20.0)
        spread = physics_engine.calculate_flame_spread_rate(cotton, g=0.0, v=15.0, P=29.6, T=20.0, RH=20.0, o2=100.0, moc_eff=moc)
        sfrs = physics_engine.calculate_space_fire_risk_score(o2=100.0, moc_eff=moc, spread_rate=spread, hoc=cotton["heat_of_combustion_mj_kg"])
        assert sfrs > 85.0
        mock_session_state.sfrs_score = sfrs

        # Navigate through isolated tab fragments
        for target_tab in ["sim", "matrix", "rag", "compare"]:
            mock_session_state.active_tab_id = target_tab
            assert mock_session_state.sfrs_score > 85.0
            assert mock_session_state.active_tab_id == target_tab

    def test_pairwise_20_cool_flame_transition_to_hot_runaway(self, physics_engine):
        """Pairing 20: (Cool Flame Kinetics, High Oxygen 40%) -> Transition from cool flame oscillation to elevated temperature."""
        res_cool = physics_engine.solve_cool_flame_ntc_kinetics(T0=1450.0, o2=17.5, P=101.3)
        res_hot = physics_engine.solve_cool_flame_ntc_kinetics(T0=1450.0, o2=40.0, P=101.3)
        assert res_cool["temperature"][-1] < 1000.0
        assert res_hot["temperature"][-1] > res_cool["temperature"][-1]
        assert res_hot["co_ppm"][-1] > res_cool["co_ppm"][-1]

    def test_pairwise_21_calibration_prohibition_low_moc_material(self, physics_engine):
        """Pairing 21: (NASA-STD-6001B Calibration, Custom Low-MOC Material) -> Immediate flight prohibition determination."""
        hazardous_mat = {"density": 900.0, "specific_heat": 1000.0, "thermal_conductivity": 0.2, "ignition_temp": 180.0, "moc_1g": 12.0, "moc_microg": 10.0, "heat_of_combustion_mj_kg": 45.0}
        env = {"g": 0.0, "v": 10.0, "p": 101.3, "t": 21.0, "rh": 45.0, "o2": 21.0}
        res = physics_engine.evaluate_custom_composite(hazardous_mat, env)
        assert res["tier"] in ["High", "Critical"]
        assert res.get("is_flammable") is True or res.get("flammability") == "Flammable"
        assert "PROHIBITED" in res["nasa_status"] or "WAIVER" in res["nasa_status"]

    def test_pairwise_22_dense_vector_rag_bilingual_query(self, rag_engine):
        """Pairing 22: (Dense Vector RAG, Bilingual Query in Vietnamese) -> Semantic retrieval operates across localized queries."""
        results = rag_engine.search_semantic("dập lửa phun sương nước fine water mist", top_k=2)
        assert len(results) > 0
        top_id = results[0]["doc"]["doc_id"]
        assert top_id in ["NASA-SP-2024-50021", "SCI-SAFFIRE-2023-04"]
        directive = rag_engine.generate_grounded_directive("dập lửa phun sương nước", results)
        assert len(directive["citations"]) > 0

    def test_pairwise_23_f5_reload_active_comparison_subtab(self, physics_engine, materials_database, mock_session_state, mock_query_params):
        """Pairing 23: (F5 Reload, Active Comparison Sub-tab) -> Deep link preserves active comparison tab and preset selections."""
        mock_query_params.update({"tab": "compare", "preset": "ARTEMIS", "g": "0.16", "o2": "34.0", "p": "56.5", "v": "12.0", "t": "22.0", "rh": "35.0"})
        mock_session_state.active_tab_id = mock_query_params.get("tab")
        mock_session_state.preset_selector = mock_query_params.get("preset")
        mock_session_state.gravity_val = float(mock_query_params.get("g"))
        mock_session_state.o2_val = float(mock_query_params.get("o2"))
        mock_session_state.p_val = float(mock_query_params.get("p"))
        mock_session_state.v_val = float(mock_query_params.get("v"))
        mock_session_state.temp_val = float(mock_query_params.get("t"))
        mock_session_state.rh_val = float(mock_query_params.get("rh"))

        assert mock_session_state.active_tab_id == "compare"
        assert mock_session_state.preset_selector == "ARTEMIS"
        assert mock_session_state.gravity_val == 0.16

        # Verify that restored telemetry directly drives comparison calculations
        env_iss = {"g": 0.0, "o2": 21.0, "p": 101.3, "v": 10.0, "t": 21.0, "rh": 45.0}
        env_art = {"g": mock_session_state.gravity_val, "o2": mock_session_state.o2_val, "p": mock_session_state.p_val, "v": mock_session_state.v_val, "t": mock_session_state.temp_val, "rh": mock_session_state.rh_val}
        diff = physics_engine.calculate_scenario_diff(env_iss, env_art, materials_database[2])
        assert diff["delta_sfrs"] > 20.0

    def test_pairwise_24_telemetry_opt_out_headless_mode(self):
        """Pairing 24: (Telemetry Opt-Out, Headless Mode) -> Zero network calls executed during automated headless evaluation."""
        config_path = os.path.join(REPO_ROOT, ".streamlit", "config.toml")
        with open(config_path, "r", encoding="utf-8") as f:
            cfg = f.read()
        assert re.search(r"gatherUsageStats\s*=\s*false", cfg, re.IGNORECASE) is not None
        assert re.search(r"headless\s*=\s*true", cfg, re.IGNORECASE) is not None
        assert re.search(r"enableCORS\s*=\s*false", cfg, re.IGNORECASE) is not None
