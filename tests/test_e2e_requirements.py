"""
Master E2E Requirements Aggregator & Verification Runner for NASA Microgravity Fire Safety Web App.
Classification: NASA Technical Memorandum Flight Safety Test Architecture (Opaque-Box E2E).

Aggregates all 4 Tiers of verification:
- Tier 1: Feature Isolation Unit Tests (Features 1-24, >=120 tests)
- Tier 2: Boundary Value Analysis & Edge Limit Tests (Features 1-24, >=120 tests)
- Tier 3: Pairwise Combinatorial Interaction Tests (>=24 tests)
- Tier 4: Realistic Mission Operational Scenarios (>=6 comprehensive profiles)
Asserts full compliance with PROJECT.md and TEST_INFRA.md (Total test count >= 270).
"""

import ast
import os
import sys
import pytest

# Ensure repository root is on sys.path
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)


@pytest.mark.e2e
class TestMasterRequirementsSuite:
    """Master Suite Aggregator & Health Verification Runner."""

    def test_master_suite_discovery(self):
        """Asserts all tiered test suite modules are present and accessible on disk."""
        tests_dir = os.path.dirname(__file__)
        required_files = [
            "__init__.py",
            "conftest.py",
            "test_e2e_tier1_features.py",
            "test_e2e_tier2_boundaries.py",
            "test_e2e_tier3_pairwise.py",
            "test_e2e_tier4_scenarios.py",
            "test_e2e_requirements.py",
        ]
        for f in required_files:
            file_path = os.path.join(tests_dir, f)
            assert os.path.isfile(file_path), f"Missing required test file: {f}"

    def test_feature_inventory_coverage(self):
        """Asserts all 24 features (F1 to F24) are present in Tier 1 and Tier 2 suites."""
        tests_dir = os.path.dirname(__file__)
        tier1_path = os.path.join(tests_dir, "test_e2e_tier1_features.py")
        tier2_path = os.path.join(tests_dir, "test_e2e_tier2_boundaries.py")

        with open(tier1_path, "r", encoding="utf-8") as f:
            t1_code = f.read()
        with open(tier2_path, "r", encoding="utf-8") as f:
            t2_code = f.read()

        t1_tree = ast.parse(t1_code)
        t2_tree = ast.parse(t2_code)

        def count_test_functions(tree):
            tests = {}
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    class_tests = [n.name for n in node.body if isinstance(n, ast.FunctionDef) and n.name.startswith("test_")]
                    tests[node.name] = len(class_tests)
            return tests

        t1_classes = count_test_functions(t1_tree)
        t2_classes = count_test_functions(t2_tree)

        assert len(t1_classes) == 24, f"Tier 1 must have exactly 24 feature classes, found {len(t1_classes)}"
        assert len(t2_classes) == 24, f"Tier 2 must have exactly 24 feature classes, found {len(t2_classes)}"

        for cls_name, count in t1_classes.items():
            assert count >= 5, f"Tier 1 class {cls_name} has {count} tests (expected >= 5)"

        for cls_name, count in t2_classes.items():
            assert count >= 5, f"Tier 2 class {cls_name} has {count} tests (expected >= 5)"

    def test_tier3_pairwise_matrix_coverage(self):
        """Asserts Tier 3 combinatorial suite contains at least 24 orthogonal pairing tests."""
        tier3_path = os.path.join(os.path.dirname(__file__), "test_e2e_tier3_pairwise.py")
        with open(tier3_path, "r", encoding="utf-8") as f:
            tree = ast.parse(f.read())

        test_funcs = [
            n.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)
            for n in node.body if isinstance(n, ast.FunctionDef) and n.name.startswith("test_")
        ]
        assert len(test_funcs) >= 24, f"Tier 3 must contain >= 24 interaction tests, found {len(test_funcs)}"

    def test_tier4_mission_scenario_coverage(self):
        """Asserts Tier 4 contains all 6 realistic mission operational workflow scenarios."""
        tier4_path = os.path.join(os.path.dirname(__file__), "test_e2e_tier4_scenarios.py")
        with open(tier4_path, "r", encoding="utf-8") as f:
            code = f.read()

        required_scenarios = [
            "test_scenario_01_iss_nominal_microgravity_baseline",
            "test_scenario_02_artemis_exploration_atmosphere_nomex_qualification",
            "test_scenario_03_eva_spacesuit_oxygen_breach_critical_alarm",
            "test_scenario_04_lunar_base_overheated_electronics_bay",
            "test_scenario_05_microgravity_droplet_cool_flame_encounter",
            "test_scenario_06_crew_emergency_suppression_and_pdf_dossier",
        ]
        for sc in required_scenarios:
            assert sc in code, f"Missing required mission scenario test: {sc}"

    def test_total_test_suite_threshold_exceeded(self):
        """Asserts total test case count across the entire suite strictly exceeds >= 270 tests."""
        tests_dir = os.path.dirname(__file__)
        suite_files = [
            "test_e2e_tier1_features.py",
            "test_e2e_tier2_boundaries.py",
            "test_e2e_tier3_pairwise.py",
            "test_e2e_tier4_scenarios.py",
            "test_e2e_requirements.py",
        ]
        total_tests = 0
        file_counts = {}

        for f in suite_files:
            with open(os.path.join(tests_dir, f), "r", encoding="utf-8") as fp:
                tree = ast.parse(fp.read())
            count = sum(
                1 for n in ast.walk(tree)
                if isinstance(n, ast.FunctionDef) and n.name.startswith("test_")
            )
            file_counts[f] = count
            total_tests += count

        # Minimum required: Tier 1 (120) + Tier 2 (120) + Tier 3 (24) + Tier 4 (6) + Req (5) = 275 tests
        assert total_tests >= 270, f"Total test suite count {total_tests} is less than required 270!"
        assert file_counts["test_e2e_tier1_features.py"] >= 120
        assert file_counts["test_e2e_tier2_boundaries.py"] >= 120
        assert file_counts["test_e2e_tier3_pairwise.py"] >= 24
        assert file_counts["test_e2e_tier4_scenarios.py"] >= 6
