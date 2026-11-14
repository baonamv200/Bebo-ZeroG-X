import math
import os
import pytest
from streamlit.testing.v1 import AppTest

from app import (
    TELEMETRY_CONFIG,
    PRESET_DEFAULTS,
    PRESET_PROFILES,
    VALID_TABS,
)

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
APP_PATH = os.path.join(ROOT_DIR, "app.py")


# ==============================================================================
# 1. STATE PERSISTENCE & DEEP LINKING ADVERSARIAL STRESS TESTS
# ==============================================================================

@pytest.mark.parametrize("param,bad_val,expected_bound", [
    ("g", "-5", 0.0),
    ("g", "-0.01", 0.0),
    ("g", "1.5", 1.0),
    ("g", "999", 1.0),
    ("g", "inf", 1.0),
    ("g", "-inf", 0.0),
    ("o2", "5", 14.0),
    ("o2", "13.9", 14.0),
    ("o2", "150", 100.0),
    ("o2", "9999", 100.0),
    ("o2", "inf", 100.0),
    ("p", "0", 25.0),
    ("p", "10", 25.0),
    ("p", "24.9", 25.0),
    ("p", "200", 105.0),
    ("p", "999", 105.0),
    ("p", "inf", 105.0),
    ("v", "-1", 0.0),
    ("v", "-50", 0.0),
    ("v", "9999", 50.0),
    ("v", "inf", 50.0),
])
def test_out_of_bounds_query_params_crash(param, bad_val, expected_bound):
    """
    Empirical adversarial test: verify whether app crashes when loaded with
    out-of-bounds query parameters (e.g. g=-5, o2=150, p=0, v=9999, inf).
    """
    at = AppTest.from_file(APP_PATH, default_timeout=30)
    at.query_params[param] = bad_val
    at.run()

    # If the app crashes with StreamlitValueBelowMinError or StreamlitValueAboveMaxError,
    # at.exception will contain the crash report.
    assert not at.exception, (
        f"App crashed on query param {param}={bad_val}! "
        f"Exception: {at.exception[0].message if at.exception else 'None'}"
    )


def test_combined_hostile_query_parameters():
    """
    Empirical test from prompt specification:
    ?g=-5&o2=150&p=0&v=9999&preset=FAKE&tab=nonexistent&lang=fr
    The app must gracefully clamp numeric bounds and sanitize invalid presets/tabs/languages.
    """
    at = AppTest.from_file(APP_PATH, default_timeout=30)
    at.query_params["g"] = "-5"
    at.query_params["o2"] = "150"
    at.query_params["p"] = "0"
    at.query_params["v"] = "9999"
    at.query_params["preset"] = "FAKE"
    at.query_params["tab"] = "nonexistent"
    at.query_params["lang"] = "fr"
    at.run()

    assert not at.exception, (
        f"App crashed on combined hostile query parameters! "
        f"Exception: {at.exception[0].message if at.exception else 'None'}"
    )

    # Sanity checks on sanitized values
    assert at.session_state.get("lang") in ("en", "vi"), "Invalid language was not sanitized"
    assert at.session_state.get("active_tab_id") in VALID_TABS, "Invalid tab was not sanitized"
    assert at.session_state.get("preset_selector") in PRESET_DEFAULTS or at.session_state.get("preset_selector") == "CUSTOM"
    assert 0.0 <= at.session_state.get("gravity_val") <= 1.0, "Gravity was not clamped"
    assert 14.0 <= at.session_state.get("o2_val") <= 100.0, "Oxygen was not clamped"
    assert 25.0 <= at.session_state.get("p_val") <= 105.0, "Pressure was not clamped"
    assert 0.0 <= at.session_state.get("v_val") <= 50.0, "Airflow was not clamped"


@pytest.mark.parametrize("param,nan_str", [
    ("g", "nan"),
    ("o2", "nan"),
    ("p", "nan"),
    ("v", "nan"),
])
def test_nan_query_parameters_sanitization(param, nan_str):
    """Verify that NaN query parameters do not propagate into numeric state."""
    at = AppTest.from_file(APP_PATH, default_timeout=30)
    at.query_params[param] = nan_str
    at.run()

    assert not at.exception
    val = at.session_state.get(f"{param}_val" if param != "g" else "gravity_val")
    assert not math.isnan(val), f"Parameter {param} became NaN in session state!"


@pytest.mark.parametrize("param,key,val", [
    ("g", "gravity_val", "0.00"),
    ("g", "gravity_val", "1.00"),
    ("o2", "o2_val", "14.0"),
    ("o2", "o2_val", "100.0"),
    ("p", "p_val", "25.0"),
    ("p", "p_val", "105.0"),
    ("v", "v_val", "0.0"),
    ("v", "v_val", "50.0"),
])
def test_exact_physical_boundaries(param, key, val):
    """Verify that exact boundary query parameters load cleanly without exceptions."""
    at = AppTest.from_file(APP_PATH, default_timeout=30)
    at.query_params[param] = val
    at.run()

    assert not at.exception
    assert math.isclose(at.session_state.get(key), float(val), abs_tol=1e-3)


# ==============================================================================
# 2. SLIDER & DIRECT NUMERIC INPUT SYNCHRONIZATION AND PRECISION TESTS
# ==============================================================================

@pytest.mark.parametrize("preset_name,expected_vals", [
    ("ISS", {"gravity_val": 0.0, "o2_val": 21.0, "p_val": 101.3, "v_val": 10.0}),
    ("LUNAR_ROVER", {"gravity_val": 0.16, "o2_val": 30.0, "p_val": 70.3, "v_val": 12.0}),
    ("ARTEMIS", {"gravity_val": 0.16, "o2_val": 34.0, "p_val": 56.5, "v_val": 15.0}),
    ("SPACESUIT", {"gravity_val": 0.16, "o2_val": 100.0, "p_val": 29.6, "v_val": 6.0}),
    ("MARS", {"gravity_val": 0.38, "o2_val": 26.0, "p_val": 70.0, "v_val": 8.0}),
    ("EARTH", {"gravity_val": 1.0, "o2_val": 21.0, "p_val": 101.3, "v_val": 0.0}),
])
def test_preset_auto_detection_from_query_params(preset_name, expected_vals):
    """Verify that matching exact telemetry sets detects the named preset."""
    at = AppTest.from_file(APP_PATH, default_timeout=30)
    at.query_params["g"] = str(expected_vals["gravity_val"])
    at.query_params["o2"] = str(expected_vals["o2_val"])
    at.query_params["p"] = str(expected_vals["p_val"])
    at.query_params["v"] = str(expected_vals["v_val"])
    at.run()

    assert not at.exception
    assert at.session_state.get("preset_selector") == preset_name


def test_custom_preset_detection_on_deviating_parameter():
    """Verify that altering any single parameter away from a preset results in CUSTOM."""
    at = AppTest.from_file(APP_PATH, default_timeout=30)
    # Artemis with slight oxygen deviation (34.1 instead of 34.0)
    at.query_params["g"] = "0.16"
    at.query_params["o2"] = "34.1"
    at.query_params["p"] = "56.5"
    at.query_params["v"] = "15.0"
    at.run()

    assert not at.exception
    assert at.session_state.get("preset_selector") == "CUSTOM"


def test_numeric_input_substep_precision():
    """Verify behavior of high-precision decimal values and rounding to defined precision."""
    at = AppTest.from_file(APP_PATH, default_timeout=30)
    # g has 2 decimals, o2 has 1 decimal
    at.query_params["g"] = "0.1649"
    at.query_params["o2"] = "34.04"
    at.run()

    assert not at.exception
    # g=0.1649 should round to 0.16
    assert math.isclose(round(at.session_state.get("gravity_val"), 2), 0.16, abs_tol=1e-3)


# ==============================================================================
# 3. FRAGMENT RERUN ISOLATION & DEFERRED RENDERING VERIFICATION
# ==============================================================================

@pytest.mark.parametrize("target_tab,tab_index", [
    ("sim", 0),
    ("morph", 1),
    ("rag", 2),
    ("matrix", 3),
    ("research", 4),
])
def test_tab_fragment_deferred_rendering_isolation(target_tab, tab_index):
    """
    Verify that deep linking to a specific tab ONLY renders that active tab's fragment,
    and all 4 inactive tabs remain unrendered (0 children).
    """
    at = AppTest.from_file(APP_PATH, default_timeout=30)
    at.query_params["tab"] = target_tab
    at.run()

    assert not at.exception
    assert at.session_state.get("active_tab_id") == target_tab

    # Assert active tab has content and inactive tabs have 0 children
    for idx, tab in enumerate(at.tabs):
        if idx == tab_index:
            assert len(tab.children) > 0, f"Active tab {target_tab} (index {idx}) has no children!"
        else:
            assert len(tab.children) == 0, f"Inactive tab index {idx} was unexpectedly rendered!"


def test_specimen_selector_interaction_inside_tab_sim():
    """Verify that changing specimen in tab_sim updates target material without full page rerun crash."""
    at = AppTest.from_file(APP_PATH, default_timeout=30)
    at.query_params["tab"] = "sim"
    at.run()

    assert not at.exception
    specimen_sb = [s for s in at.selectbox if s.key == "cfd_target_specimen_selector"]
    assert len(specimen_sb) == 1
    sb = specimen_sb[0]
    initial_val = sb.value

    # Pick another specimen
    other_options = [o for o in sb.options if o != initial_val]
    assert len(other_options) > 0
    sb.select(other_options[0])
    at.run()

    assert not at.exception
    assert at.session_state.get("global_target_mat_id") != initial_val
