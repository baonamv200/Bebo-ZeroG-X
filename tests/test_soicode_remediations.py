"""
Regression test suite covering all /soicode remediation items:
1. Dynamic multi-block grounding in rag_engine.generate_grounded_directive.
2. Cabin T/RH propagation & continuous physics parity across app.py and physics_models.py.
3. NaN / +/-Inf guards in pdf_dossier.py, app.generate_3d_flame_figure, app.calculate_temperature_mesh, and Rust/PyO3 core.
4. LLM helper cache-key secret exclusion, valid Gemini flash model IDs, and empty-choices OpenAI 200 handling.
5. Custom material cm_name XSS escaping & uploaded RAG document merging / citation rendering.
6. SafeAlertProxy real app.py contract verification.
"""

from __future__ import annotations

import ast
import html
import inspect
import math
import os
import sys
from unittest.mock import MagicMock

import numpy as np
import pytest

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

import app
import pdf_dossier
import physics_models
import rag_engine


def _read_repo_file(rel_path: str) -> str:
    with open(os.path.join(REPO_ROOT, rel_path), "r", encoding="utf-8") as fh:
        return fh.read()


# ==============================================================================
# 1. Dynamic Grounding in rag_engine.generate_grounded_directive
# ==============================================================================
class TestDynamicRagGrounding:
    def test_directive_varies_with_query_docs_and_chat_history(self):
        doc_a = (
            0.91,
            {
                "report_id": "NASA/TM-2024-99001",
                "title": "Lunar Habitat Lithium-Polymer Thermal Runaway",
                "section": "Section 3.1: Pressure-Drop Suppression",
                "page": 17,
                "text": "Halving cabin pressure to 56.5 kPa lowers convective cooling on Nomex panels and demands immediate bus isolation.",
            },
        )
        doc_b = (
            0.88,
            {
                "report_id": "NASA/SP-2022-44110",
                "title": "ISS Columbus Wire Harness Overcurrent Study",
                "section": "Section 7.4: PTFE Insulation Charring",
                "page": 63,
                "text": "PTFE insulation emits toxic hydrogen fluoride vapors above 680 K when 12 cm/s ventilation fans remain active.",
            },
        )

        res_a = rag_engine.generate_grounded_directive(
            "How do we extinguish Nomex fire during Lunar depressurization?",
            [doc_a],
            chat_history=[{"role": "user", "content": "Cabin pressure is 56.5 kPa in Gateway airlock."}],
        )
        res_b = rag_engine.generate_grounded_directive(
            "Assess toxic gas risk from PTFE wire bundle charring in ISS Columbus.",
            [doc_b],
            chat_history=[{"role": "user", "content": "Crew detected acrid fumes near rack AV-02."}],
        )

        for res in (res_a, res_b):
            assert isinstance(res, dict)
            assert isinstance(res["directive"], str)
            assert isinstance(res["citations"], list)
            text = res["directive"]
            assert "BLOCK 1" in text
            assert "BLOCK 2" in text
            assert "BLOCK 3" in text
            assert "NASA-STD-6001B" in text
            assert "Test 1" in text
            assert "T+0s" in text and "T+15s" in text and "T+60s" in text

        assert res_a["directive"] != res_b["directive"]
        assert "NASA/TM-2024-99001" in res_a["directive"]
        assert "Nomex" in res_a["directive"]
        assert "Gateway airlock" in res_a["directive"] or "56.5 kPa" in res_a["directive"]
        assert "NASA/SP-2022-44110" in res_b["directive"]
        assert "PTFE" in res_b["directive"]
        assert "Columbus" in res_b["directive"]

    def test_directive_handles_empty_docs_and_non_tuple_dicts(self):
        res_empty = rag_engine.generate_grounded_directive("Emergency water mist suppression?", [])
        assert "BLOCK 1" in res_empty["directive"]
        assert "BLOCK 2" in res_empty["directive"]
        assert "BLOCK 3" in res_empty["directive"]
        assert res_empty["citations"] == []

        raw_doc = {
            "doc_id": "UPLOADED-TEST-01",
            "title": "Custom Cabin Silicone Seal Audit",
            "section": "Uploaded Chunk 1",
            "content": "Silicone seal outgasses cyclic siloxanes under elevated 36% O2.",
        }
        res_dict = rag_engine.generate_grounded_directive("Evaluate silicone seal in 36% O2", [raw_doc])
        assert "UPLOADED-TEST-01" in res_dict["directive"]
        assert "Custom Cabin Silicone Seal Audit" in res_dict["directive"]
        assert "siloxanes" in res_dict["directive"]
        assert any(
            isinstance(c, dict) and c.get("doc_id") == "UPLOADED-TEST-01"
            for c in res_dict["citations"]
        )

    def test_pmma_query_not_hijacked_by_secondary_cool_flame_doc(self):
        pmma_doc = (
            0.92,
            {
                "report_id": "NASA/TM-2023-0014829",
                "title": "SoFIE Microgravity PMMA Rod Kinetics",
                "section": "Section 4.3: Low-Flow Flammability",
                "page": 42,
                "text": "PMMA burning accelerates at 5 to 12 cm/s forced ventilation due to Damkohler transport.",
            },
        )
        cool_doc = (
            0.41,
            {
                "report_id": "SCI-FLEX-2012-1593",
                "title": "FLEX Cool Flame Droplet Extinction",
                "section": "Section 2.1: NTC Oxidation",
                "page": 369,
                "text": "Heptane droplets undergo two-stage cool flame combustion at 600-800 K.",
            },
        )
        res = rag_engine.generate_grounded_directive(
            "What is the PMMA low flow hazard?",
            [pmma_doc, cool_doc],
        )
        text = res["directive"]
        block1_part = text.split("#### BLOCK 2")[0]
        assert "What is the PMMA low flow hazard?" in block1_part
        assert "Negative Temperature Coefficient (NTC)" not in block1_part
        assert "Damköhler" in block1_part or "PMMA" in block1_part


# ==============================================================================
# 2. Cabin T/RH Propagation & Continuous Physics Parity
# ==============================================================================
class TestTempRhPropagationAndParity:
    @staticmethod
    def _sample_material() -> dict:
        return dict(app.materials_df.iloc[0].to_dict())

    def test_extinction_curve_and_sweeps_respond_to_temp_and_rh(self):
        sample_mat = self._sample_material()
        mat_tuple = tuple(sorted(sample_mat.items()))

        _, moc_cold_humid = app.MicrogravityCombustionPhysics.generate_extinction_curve(
            sample_mat, 0.0, 101.3, temp_c=15.0, rh_pct=85.0
        )
        _, moc_hot_dry = app.MicrogravityCombustionPhysics.generate_extinction_curve(
            sample_mat, 0.0, 101.3, temp_c=40.0, rh_pct=10.0
        )
        assert float(np.mean(moc_cold_humid)) > float(np.mean(moc_hot_dry)) + 1.0

        sweep_a = app.calculate_cached_paradox_sweep(mat_tuple, 21.0, 101.3, 0.0, temp_c=15.0, rh_pct=85.0)
        sweep_b = app.calculate_cached_paradox_sweep(mat_tuple, 21.0, 101.3, 0.0, temp_c=40.0, rh_pct=10.0)
        assert not np.allclose(sweep_a[1], sweep_b[1])

        bnd_a = app.calculate_cached_boundary_sweep(mat_tuple, 0.0, 101.3, temp_c=15.0, rh_pct=85.0)
        bnd_b = app.calculate_cached_boundary_sweep(mat_tuple, 0.0, 101.3, temp_c=40.0, rh_pct=10.0)
        assert not np.allclose(bnd_a[1], bnd_b[1])

    def test_figures_and_evaluate_all_materials_propagate_temp_rh(self):
        sample_mat = self._sample_material()
        mat_tuple = tuple(sorted(sample_mat.items()))

        fig_sfrs_1 = app.generate_sfrs_figure(0.0, 21.0, 101.3, 10.0, lang="en", temp_c=15.0, rh_pct=85.0)
        fig_sfrs_2 = app.generate_sfrs_figure(0.0, 21.0, 101.3, 10.0, lang="en", temp_c=40.0, rh_pct=10.0)
        assert not np.allclose(
            np.asarray(fig_sfrs_1.data[0].y, dtype=float),
            np.asarray(fig_sfrs_2.data[0].y, dtype=float),
        )

        fig_par_1 = app.generate_paradox_figure(mat_tuple, 21.0, 101.3, 0.0, 10.0, 0.5, lang="en", temp_c=15.0, rh_pct=85.0)
        fig_par_2 = app.generate_paradox_figure(mat_tuple, 21.0, 101.3, 0.0, 10.0, 0.5, lang="en", temp_c=40.0, rh_pct=10.0)
        assert not np.allclose(np.asarray(fig_par_1.data[0].y, dtype=float), np.asarray(fig_par_2.data[0].y, dtype=float))

        fig_bnd_1 = app.generate_boundary_figure(mat_tuple, 0.0, 101.3, 10.0, 21.0, lang="en", temp_c=15.0, rh_pct=85.0)
        fig_bnd_2 = app.generate_boundary_figure(mat_tuple, 0.0, 101.3, 10.0, 21.0, lang="en", temp_c=40.0, rh_pct=10.0)
        assert not np.allclose(np.asarray(fig_bnd_1.data[0].y, dtype=float), np.asarray(fig_bnd_2.data[0].y, dtype=float))

        df_cold_humid, _ = app.evaluate_all_materials(0.0, 21.0, 101.3, 10.0, "en", temp_c=15.0, rh_pct=85.0)
        df_hot_dry, _ = app.evaluate_all_materials(0.0, 21.0, 101.3, 10.0, "en", temp_c=40.0, rh_pct=10.0)
        assert float(df_cold_humid["effective_moc"].mean()) > float(df_hot_dry["effective_moc"].mean())

    def test_pressure_continuity_and_physics_models_parity(self):
        sample_mat = self._sample_material()
        moc_below = app.MicrogravityCombustionPhysics.calculate_effective_moc(
            sample_mat, 0.0, 10.0, 101.29, temp_c=21.0, rh_pct=45.0
        )
        moc_stp = app.MicrogravityCombustionPhysics.calculate_effective_moc(
            sample_mat, 0.0, 10.0, 101.3, temp_c=21.0, rh_pct=45.0
        )
        moc_above = app.MicrogravityCombustionPhysics.calculate_effective_moc(
            sample_mat, 0.0, 10.0, 101.31, temp_c=21.0, rh_pct=45.0
        )
        assert abs(moc_stp - moc_below) < 0.05
        assert abs(moc_above - moc_stp) < 0.05

        app_base = app.MicrogravityCombustionPhysics.calculate_effective_moc(
            sample_mat, 0.0, 10.0, 101.3, temp_c=21.0, rh_pct=45.0
        )
        app_env = app.MicrogravityCombustionPhysics.calculate_effective_moc(
            sample_mat, 0.0, 10.0, 80.0, temp_c=30.0, rh_pct=25.0
        )
        pm_base = physics_models.calculate_effective_moc(
            sample_mat, 0.0, 10.0, 101.3, T=21.0, RH=45.0
        )
        pm_env = physics_models.calculate_effective_moc(
            sample_mat, 0.0, 10.0, 80.0, T=30.0, RH=25.0
        )
        assert (app_env - app_base) == pytest.approx(pm_env - pm_base, rel=1e-6, abs=1e-6)

        spread_app_cold = app.MicrogravityCombustionPhysics.calculate_flame_spread_rate(
            sample_mat, 0.0, 24.0, 80.0, 10.0, app_base, temp_c=15.0, rh_pct=85.0
        )
        spread_app_hot = app.MicrogravityCombustionPhysics.calculate_flame_spread_rate(
            sample_mat, 0.0, 24.0, 80.0, 10.0, app_env, temp_c=40.0, rh_pct=10.0
        )
        spread_pm_hot = physics_models.calculate_flame_spread_rate(
            sample_mat, 0.0, 10.0, 80.0, T=40.0, RH=10.0, o2=24.0, moc_eff=pm_env
        )
        assert math.isfinite(spread_app_cold) and math.isfinite(spread_app_hot) and math.isfinite(spread_pm_hot)
        assert spread_app_hot > spread_app_cold


# ==============================================================================
# 3. NaN & +/-Inf Immunity (PDF Dossier, 3D Flame Figure, Mesh, Rust PyO3)
# ==============================================================================
class TestNonFiniteGuards:
    def test_pdf_dossier_handles_nan_and_inf_gracefully(self):
        scenario = {
            "gravity_g": float("nan"),
            "oxygen_pct": float("inf"),
            "pressure_kpa": float("-inf"),
            "airflow_cm_s": "corrupt-float",
            "temp_c": None,
            "rh_pct": float("nan"),
            "sfrs": float("nan"),
            "tier": "Critical",
            "mission_profile": "Gateway Edge <Test>",
        }
        materials = [
            {
                "material_name": "Nomex IIIA",
                "moc": float("nan"),
                "spread_rate": float("inf"),
                "sfrs": float("-inf"),
                "tier": "Safe",
            }
        ]
        pdf_bytes = pdf_dossier.generate_mission_safety_dossier_pdf(scenario, materials)
        assert isinstance(pdf_bytes, bytes)
        assert pdf_bytes.startswith(b"%PDF-")
        assert len(pdf_bytes) > 500
        pdf_empty_mats = pdf_dossier.generate_mission_safety_dossier_pdf(scenario, [])
        assert pdf_empty_mats.startswith(b"%PDF-")

    def test_pdf_dossier_multipage_no_truncation(self):
        scenario = {
            "mission": "ISS",
            "g": 0.0,
            "o2": 21.0,
            "p": 101.3,
            "v": 10.0,
            "t": 21.0,
            "rh": 45.0,
            "sfrs": 52.4,
            "tier": "HIGH",
        }
        materials = [
            {
                "material_name": f"MAT-ROW-{idx:03d}",
                "sfrs": 40.0 + (idx % 40),
                "moc_eff": 18.5,
                "spread_rate": 0.42,
                "flammability": "Flammable",
            }
            for idx in range(1, 61)
        ]
        pdf_bytes = pdf_dossier.generate_mission_safety_dossier_pdf(scenario, materials)
        assert pdf_bytes.startswith(b"%PDF-1.")
        assert b"xref" in pdf_bytes
        assert pdf_bytes.endswith(b"%%EOF\n")
        assert b"/Count 2" in pdf_bytes
        assert b"MAT-ROW-001" in pdf_bytes
        assert b"MAT-ROW-060" in pdf_bytes

    def test_3d_flame_figure_and_temperature_mesh_handle_nan_inf(self):
        for g_val in (float("nan"), float("inf"), float("-inf")):
            for v_val in (float("nan"), float("inf")):
                fig = app.generate_3d_flame_figure(g_val, v_val, float("nan"), is_extinguished=False, lang="en")
                assert len(fig.data) >= 1
                for trace in fig.data:
                    for attr in ("x", "y", "z", "value", "intensity"):
                        val = getattr(trace, attr, None)
                        if val is not None:
                            arr = np.asarray(val, dtype=float)
                            assert np.all(np.isfinite(arr))
                x_vals, y_vals, temp_grid, cscale = app.calculate_temperature_mesh(g_val, v_val, float("inf"))
                for num_arr in (x_vals, y_vals, temp_grid):
                    np_arr = np.asarray(num_arr, dtype=float)
                    assert np_arr.size > 0
                    assert np.all(np.isfinite(np_arr))
                assert isinstance(cscale, list) and len(cscale) >= 2

    def test_rust_pyo3_nan_immunity_if_available(self):
        if not app.RUST_BACKEND_AVAILABLE:
            pytest.skip("nasa_rust native module not compiled in environment")
        mat = TestTempRhPropagationAndParity._sample_material()
        moc_nan = app.rust_core.MicrogravityCombustionPhysics.calculate_effective_moc(
            mat, float("nan"), float("nan"), float("nan")
        )
        assert math.isfinite(moc_nan)
        moc_inf = app.rust_core.MicrogravityCombustionPhysics.calculate_effective_moc(
            mat, float("inf"), 10.0, 101.3
        )
        assert moc_inf == 60.0
        sfrs_nan = app.rust_core.MicrogravityCombustionPhysics.calculate_space_fire_risk_score(
            mat, float("nan"), float("nan"), float("nan"), float("nan"), float("nan")
        )
        assert math.isfinite(sfrs_nan[0])


# ==============================================================================
# 4. LLM Helper Hardening (Cache Keys, Valid Gemini IDs, Empty OpenAI Choices)
# ==============================================================================
class TestLlmHelperHardening:
    def test_cache_decorators_exclude_raw_api_key_and_remove_gemini_38(self):
        app_src = _read_repo_file("app.py")
        assert "gemini-3.8-flash" not in app_src
        assert "gemini-2.5-flash" in app_src

        sig_rag = inspect.signature(app._query_online_llm_rag_cached)
        assert "_api_key" in sig_rag.parameters
        assert "api_key" not in sig_rag.parameters

        sig_copilot = inspect.signature(app.AICoPilotEngine._call_online_ai_cached)
        assert "_api_key" in sig_copilot.parameters
        assert "api_key" not in sig_copilot.parameters

    def test_openai_200_empty_choices_returns_clean_notice(self, monkeypatch):
        fake_resp = MagicMock()
        fake_resp.status_code = 200
        fake_resp.json.return_value = {"choices": []}
        monkeypatch.setattr(app.requests, "post", lambda *args, **kwargs: fake_resp)

        app._query_online_llm_rag_cached.clear()
        app.AICoPilotEngine._call_online_ai_cached.clear()

        rag_out = app.query_online_llm_rag(
            "Explain PMMA microgravity paradox",
            "NASA/TM-2023-0014829 excerpt",
            "OpenAI",
            "sk-unit-test-secret-0001",
            lang="en",
        )
        assert "Empty or malformed response from OpenAI" in rag_out
        assert "sk-unit-test-secret-0001" not in rag_out

        copilot_text, mode = app.AICoPilotEngine.call_online_ai(
            "sk-unit-test-secret-0001",
            "OpenAI",
            "Nomex IIIA",
            "PSI-02",
            "ISS",
            "Aramid",
            22.0,
            24.0,
            0.0,
            21.0,
            101.3,
            10.0,
            42.0,
            "Moderate",
            22.0,
            0.25,
            False,
            lang="en",
        )
        assert mode == "fallback"
        assert "empty" in copilot_text.lower()
        assert "sk-unit-test-secret-0001" not in copilot_text


# ==============================================================================
# 5. XSS Sanitization & Uploaded RAG Document Merging
# ==============================================================================
class TestXssAndUploadedRagUi:
    def test_custom_material_xss_payload_is_escaped_and_rag_merges_uploads(self):
        app_src = _read_repo_file("app.py")
        tree = ast.parse(app_src)

        render_rag_fn = next(
            (n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef) and n.name == "render_tab_rag"),
            None,
        )
        assert render_rag_fn is not None
        render_rag_src = ast.unparse(render_rag_fn)
        assert "matched_results" in render_rag_src
        assert "generate_grounded_directive(effective_rag_query, matched_results" in render_rag_src
        assert "html.escape" in render_rag_src

        assert 'html.escape(str(_ev[\'name\'])' in app_src or 'html.escape(str(_ev["name"])' in app_src

        # Validate AppTest end-to-end with malicious cm_name XSS payload in session_state
        from streamlit.testing.v1 import AppTest

        payload = '<script>alert("xss")</script><img src=x onerror=alert(1)>'
        escaped_payload = html.escape(payload, quote=True)
        at = AppTest.from_file(os.path.join(REPO_ROOT, "app.py"), default_timeout=30)
        at.session_state["custom_materials"] = [
            {
                "name": payload,
                "density_kg_m3": 1600.0,
                "specific_heat_j_kgk": 1350.0,
                "thermal_conductivity": 0.25,
                "ignition_temp_c": 420.0,
                "moc_1g": 28.0,
                "moc_ug": 24.5,
                "hoc_mj_kg": 24.0,
            }
        ]
        at.run()
        assert not at.exception

        all_rendered_html = "\n".join(el.value for el in at.markdown)
        assert payload not in all_rendered_html
        # If custom material name appears in any markdown table/card, it must be HTML-escaped
        if "CUSTOM" in all_rendered_html and "script" in all_rendered_html:
            assert escaped_payload in all_rendered_html


# ==============================================================================
# 6. SafeAlertProxy Real app.py Contract Verification
# ==============================================================================
class TestSafeAlertProxyRealContract:
    def test_alert_proxy_verifies_real_app_css_audio_and_non_finite(self, alert_system):
        assert alert_system.should_trigger_alarm(85.0) is False
        assert alert_system.should_trigger_alarm(85.1) is True
        assert alert_system.should_trigger_alarm(95.0, muted=True) is False
        assert alert_system.should_trigger_alarm(float("nan")) is False
        assert alert_system.should_trigger_alarm(float("inf")) is False

        css = alert_system.generate_emergency_border_css(90.0)
        assert "@keyframes nasaCriticalBorderPulse" in css
        assert "@keyframes screenBorderEmergencyPulse" in css
        assert "#EF4444" in css
        assert "stAppViewContainer" in css
        assert alert_system.generate_emergency_border_css(85.0) == ""

        html_alarm = alert_system.generate_alarm_html(90.0)
        assert "880" in html_alarm and "1046" in html_alarm
        assert "ctx.resume()" in html_alarm
        assert alert_system.get_fire_threat_tier(float("nan")) == "Safe"


# ==============================================================================
# 7. Wave-2 Adversarial Review Regression Tests (RAG UI Merge, XSS, LLM, T/RH, Python NaN)
# ==============================================================================
class TestAdversarialReviewRegressions:
    def test_copilot_propagates_temp_and_rh(self):
        mat = dict(app.materials_df.iloc[0].to_dict())
        cabin_cool = {"gravity_g": 0.0, "oxygen_pct": 24.0, "pressure_kpa": 101.3, "airflow_cm_s": 10.0, "temp_c": 15.0, "rh_pct": 20.0}
        cabin_hot = {"gravity_g": 0.0, "oxygen_pct": 24.0, "pressure_kpa": 101.3, "airflow_cm_s": 10.0, "temp_c": 42.0, "rh_pct": 85.0}
        risk_data = {"sfrs": 65.0, "tier": "High", "effective_moc": 18.0, "flame_spread_rate_mm_s": 0.55, "cool_flame": (False, "Nominal")}

        out_cool = app.AICoPilotEngine.generate_expert_insights(mat, cabin_cool, risk_data, lang="en")
        out_hot = app.AICoPilotEngine.generate_expert_insights(mat, cabin_hot, risk_data, lang="en")
        assert "15.0" in out_cool["physics_explanation"] and "20%" in out_cool["physics_explanation"]
        assert "42.0" in out_hot["physics_explanation"] and "85%" in out_hot["physics_explanation"]
        assert out_cool["physics_explanation"] != out_hot["physics_explanation"]

    def test_python_fallback_nan_immunity_when_rust_disabled(self, monkeypatch):
        monkeypatch.setattr(app, "RUST_BACKEND_AVAILABLE", False)
        mat = dict(app.materials_df.iloc[0].to_dict())

        score, tier, _ = app.MicrogravityCombustionPhysics.calculate_space_fire_risk_score(
            mat, float("nan"), float("nan"), float("nan"), float("nan"), float("nan")
        )
        assert math.isfinite(score)
        assert tier == "Safe"

        active, _ = app.MicrogravityCombustionPhysics.detect_cool_flames(
            {"cool_flame_susceptible": True, "moc_1g": 21.0, "moc_microg": 18.0},
            float("nan"), float("nan"), float("nan"), float("nan"), lang="en",
        )
        assert active is False

        morph = app.MicrogravityCombustionPhysics.calculate_flame_morphology_metrics(
            float("nan"), float("nan"), float("nan"), float("nan"), lang="en", material_row=mat
        )
        for metric_key in ("grashof", "reynolds", "richardson", "peclet", "damkohler", "aspect_ratio", "peak_temp_k"):
            assert math.isfinite(morph[metric_key]), f"Non-finite {metric_key}: {morph[metric_key]}"

    def test_llm_gemini_timeout_and_null_content_and_openai_null_content(self, monkeypatch):
        import requests

        call_count = {"n": 0}

        def _raise_timeout(*args, **kwargs):
            call_count["n"] += 1
            raise requests.exceptions.Timeout("simulated 15s hang")

        monkeypatch.setattr(app.requests, "post", _raise_timeout)
        app._query_online_llm_rag_cached.clear()
        app.AICoPilotEngine._call_online_ai_cached.clear()

        rag_timeout = app.query_online_llm_rag("test", "ctx", "Google Gemini", "AIzaTestKeyTimeout", lang="en")
        assert call_count["n"] == 1
        assert "timed out" in rag_timeout.lower()

        call_count["n"] = 0
        cp_timeout_txt, cp_timeout_mode = app.AICoPilotEngine.call_online_ai(
            "AIzaTestKeyTimeout", "Google Gemini", "PMMA", "PSI-1", "ISS", "Chem",
            18.0, 21.0, 0.0, 21.0, 101.3, 10.0, 40.0, "Moderate", 18.0, 0.3, False, lang="en"
        )
        assert call_count["n"] == 1
        assert cp_timeout_mode == "fallback"
        assert "[Timeout]" in cp_timeout_txt

        fake_safety = MagicMock()
        fake_safety.status_code = 200
        fake_safety.json.return_value = {"candidates": [{"content": None, "finishReason": "SAFETY"}]}
        monkeypatch.setattr(app.requests, "post", lambda *args, **kwargs: fake_safety)
        app._query_online_llm_rag_cached.clear()
        app.AICoPilotEngine._call_online_ai_cached.clear()

        rag_safety = app.query_online_llm_rag("test", "ctx", "Google Gemini", "AIzaTestKeySafety", lang="en")
        assert "safety filter" in rag_safety.lower()
        cp_safety_txt, cp_safety_mode = app.AICoPilotEngine.call_online_ai(
            "AIzaTestKeySafety", "Google Gemini", "PMMA", "PSI-1", "ISS", "Chem",
            18.0, 21.0, 0.0, 21.0, 101.3, 10.0, 40.0, "Moderate", 18.0, 0.3, False, lang="en"
        )
        assert cp_safety_mode == "fallback"
        assert "safety filter" in cp_safety_txt.lower()
        assert "[HTTP 200]" not in cp_safety_txt

        fake_null_openai = MagicMock()
        fake_null_openai.status_code = 200
        fake_null_openai.json.return_value = {"choices": [{"message": {"content": None}}]}
        monkeypatch.setattr(app.requests, "post", lambda *args, **kwargs: fake_null_openai)
        app._query_online_llm_rag_cached.clear()
        app.AICoPilotEngine._call_online_ai_cached.clear()

        rag_null = app.query_online_llm_rag("test", "ctx", "OpenAI", "sk-null-key", lang="en")
        assert "empty or malformed" in rag_null.lower()
        cp_null_txt, cp_null_mode = app.AICoPilotEngine.call_online_ai(
            "sk-null-key", "OpenAI", "PMMA", "PSI-1", "ISS", "Chem",
            18.0, 21.0, 0.0, 21.0, 101.3, 10.0, 40.0, "Moderate", 18.0, 0.3, False, lang="en"
        )
        assert cp_null_mode == "fallback"
        assert cp_null_txt is not None and "empty or malformed" in cp_null_txt.lower()

    def test_apptest_custom_form_single_escape_and_uploaded_rag_merge_xss(self):
        from streamlit.testing.v1 import AppTest

        at = AppTest.from_file(os.path.join(REPO_ROOT, "app.py"), default_timeout=30)
        at.run()
        assert not at.exception

        raw_name = '<script>alert(1)</script> & Carbon'
        cm_inputs = [ti for ti in at.text_input if "Specimen" in str(ti.label) or "CF-PEEK" in str(ti.value)]
        assert cm_inputs
        cm_inputs[0].set_value(raw_name)
        submit_btns = [b for b in at.button if "custom_material_eval_form" in str(b.key) or "Evaluate" in str(b.label)]
        assert submit_btns
        submit_btns[0].click()
        at.run()
        assert not at.exception
        assert any(m.get("name") == raw_name for m in at.session_state["custom_materials"])

        xss_filename = 'audit_<img src=x onerror=alert(1)>.txt'
        rag_engine.clear_custom_documents()
        try:
            chunks = rag_engine.ingest_user_document(
                b"UniqueZebra777 cool flame helium diluent suppresses PMMA pyrolysis in microgravity chambers.",
                xss_filename,
            )
            assert chunks == 1

            at_rag = AppTest.from_file(os.path.join(REPO_ROOT, "app.py"), default_timeout=30)
            at_rag.query_params["tab"] = "rag"
            at_rag.run()
            assert not at_rag.exception

            rag_inputs = [ti for ti in at_rag.text_input if ti.key == "rag_input"]
            assert rag_inputs
            rag_inputs[0].set_value("UniqueZebra777 cool flame")
            at_rag.run()
            assert not at_rag.exception

            md_all = "\n".join(el.value for el in at_rag.markdown)
            assert "UniqueZebra777" in md_all
            assert "USER-UPLOAD" in md_all
            assert "<img src=x onerror=alert(1)>" not in md_all
            assert html.escape(xss_filename, quote=True) in md_all
            assert "&amp;lt;" not in md_all

            # Also verify selecting CUSTOM-1 in Tab 3 Deep-Dive CoPilot never KeyErrors
            at_rag.session_state["custom_materials"] = list(at.session_state["custom_materials"])
            at_rag.run()
            assert not at_rag.exception
            cp_sel = [sb for sb in at_rag.selectbox if sb.key == "copilot_material_select"]
            assert cp_sel
            custom_opts = [opt for opt in cp_sel[0].options if "Carbon" in opt]
            assert custom_opts
            cp_sel[0].select(custom_opts[0])
            at_rag.run()
            assert not at_rag.exception
            md_cp = "\n".join(el.value for el in at_rag.markdown)
            assert "<script>alert(1)</script>" not in md_cp
            assert "&amp;lt;script&amp;gt;" not in md_cp
        finally:
            rag_engine.clear_custom_documents()
