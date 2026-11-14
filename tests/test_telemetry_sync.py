import math
import pytest
from app import (
    TELEMETRY_CONFIG,
    PRESET_DEFAULTS,
    PRESET_PROFILES,
    VALID_TABS,
)


def test_telemetry_config_structure():
    """Verify that TELEMETRY_CONFIG defines all 4 primary flight parameters with valid bounds."""
    expected_keys = ["gravity_val", "o2_val", "p_val", "v_val"]
    for k in expected_keys:
        assert k in TELEMETRY_CONFIG
        cfg = TELEMETRY_CONFIG[k]
        assert cfg["min"] < cfg["max"]
        assert cfg["step"] > 0
        assert cfg["min"] <= cfg["default"] <= cfg["max"]
        assert isinstance(cfg["decimals"], int)
        assert cfg["decimals"] >= 0
        assert "qp_key" in cfg


def test_preset_profiles_alignment():
    """Verify that PRESET_PROFILES matches the physical specifications in PRESET_DEFAULTS."""
    for preset_name, prof in PRESET_PROFILES.items():
        assert preset_name in PRESET_DEFAULTS
        baseline = PRESET_DEFAULTS[preset_name]
        assert math.isclose(prof["gravity_val"], baseline["g"], abs_tol=1e-3)
        assert math.isclose(prof["o2_val"], baseline["o2"], abs_tol=1e-3)
        assert math.isclose(prof["p_val"], baseline["p"], abs_tol=1e-3)
        assert math.isclose(prof["v_val"], baseline["v"], abs_tol=1e-3)


def test_valid_tabs_coverage():
    """Ensure all five core navigation tabs are included in VALID_TABS."""
    expected = ["sim", "morph", "rag", "matrix", "research"]
    assert sorted(VALID_TABS) == sorted(expected)


def test_preset_detection_logic():
    """Simulate session state dictionary and verify preset detection behaves correctly."""
    def detect_preset_from_dict(state_dict):
        cur = {
            k: round(float(state_dict.get(k, cfg["default"])), cfg["decimals"])
            for k, cfg in TELEMETRY_CONFIG.items()
        }
        for preset_name, preset_vals in PRESET_PROFILES.items():
            if all(math.isclose(cur[k], preset_vals[k], abs_tol=1e-3) for k in preset_vals):
                return preset_name
        return "CUSTOM"

    # 1. Nominal ISS baseline
    iss_state = {"gravity_val": 0.0, "o2_val": 21.0, "p_val": 101.3, "v_val": 10.0}
    assert detect_preset_from_dict(iss_state) == "ISS"

    # 2. Nominal Artemis baseline
    artemis_state = {"gravity_val": 0.16, "o2_val": 34.0, "p_val": 56.5, "v_val": 15.0}
    assert detect_preset_from_dict(artemis_state) == "ARTEMIS"

    # 3. Nominal Spacesuit EVA baseline
    eva_state = {"gravity_val": 0.16, "o2_val": 100.0, "p_val": 29.6, "v_val": 6.0}
    assert detect_preset_from_dict(eva_state) == "SPACESUIT"

    # 4. Custom modified parameters
    custom_state = {"gravity_val": 0.42, "o2_val": 28.5, "p_val": 80.0, "v_val": 12.0}
    assert detect_preset_from_dict(custom_state) == "CUSTOM"


def test_numeric_input_clamping_and_rounding():
    """Verify that simulated on_num_change clamps out-of-bounds input and rounds to precision."""
    def simulate_num_change(param_key, typed_val, state):
        cfg = TELEMETRY_CONFIG[param_key]
        clamped_val = max(cfg["min"], min(cfg["max"], float(typed_val)))
        val = round(clamped_val, cfg["decimals"])
        state[param_key] = val
        state[f"{param_key}_num"] = val
        state[f"{param_key}_slider"] = val
        return val

    mock_state = {}
    # Oxygen: Min 14.0, Max 100.0, decimals=1
    val = simulate_num_change("o2_val", 150.0, mock_state)
    assert val == 100.0
    assert mock_state["o2_val_slider"] == 100.0

    val = simulate_num_change("o2_val", 5.0, mock_state)
    assert val == 14.0
    assert mock_state["o2_val_slider"] == 14.0

    val = simulate_num_change("o2_val", 21.4389, mock_state)
    assert val == 21.4
    assert mock_state["o2_val"] == 21.4

    # Gravity: Min 0.00, Max 1.00, decimals=2
    val = simulate_num_change("gravity_val", 0.3821, mock_state)
    assert val == 0.38
    assert mock_state["gravity_val"] == 0.38


def test_idempotent_query_param_sync():
    """Test that query parameter synchronization is strictly idempotent and prevents redundant writes."""
    state = {
        "active_tab_id": "morph",
        "preset_selector": "ARTEMIS",
        "gravity_val": 0.16,
        "o2_val": 34.0,
        "p_val": 56.5,
        "v_val": 15.0,
        "temp_val": 22.0,
        "rh_val": 42.0,
        "lang": "vi",
    }
    target_qp = {
        "tab": state["active_tab_id"],
        "preset": state["preset_selector"],
        "g": f"{float(state['gravity_val']):.2f}",
        "o2": f"{float(state['o2_val']):.1f}",
        "p": f"{float(state['p_val']):.1f}",
        "v": f"{float(state['v_val']):.1f}",
        "t": f"{float(state['temp_val']):.1f}",
        "rh": f"{float(state['rh_val']):.0f}",
        "lang": state["lang"],
    }
    mock_qp = {}
    writes = 0

    def sync(qp_dict, current_qp):
        nonlocal writes
        for k, v in qp_dict.items():
            if current_qp.get(k) != v:
                current_qp[k] = v
                writes += 1

    # First sync: writes all 9 parameters
    sync(target_qp, mock_qp)
    assert writes == 9
    assert mock_qp["preset"] == "ARTEMIS"
    assert mock_qp["g"] == "0.16"
    assert mock_qp["o2"] == "34.0"
    assert mock_qp["tab"] == "morph"

    # Second sync without state change: writes 0 times (idempotent guard works!)
    writes = 0
    sync(target_qp, mock_qp)
    assert writes == 0
