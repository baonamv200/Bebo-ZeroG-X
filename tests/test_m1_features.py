import os
import tomllib
import pytest
from streamlit.testing.v1 import AppTest

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
APP_PATH = os.path.join(ROOT_DIR, "app.py")
CONFIG_PATH = os.path.join(ROOT_DIR, ".streamlit", "config.toml")


def test_app_loads_without_exceptions():
    """Verify that app.py initializes cleanly with default ISS parameters."""
    at = AppTest.from_file(APP_PATH, default_timeout=30)
    at.run()
    assert not at.exception
    # Verify default state
    assert at.session_state.get("preset_selector") == "ISS"
    assert at.session_state.get("gravity_val") == 0.0
    assert at.session_state.get("o2_val") == 21.0
    assert at.session_state.get("p_val") == 101.3
    assert at.session_state.get("v_val") == 10.0


def test_app_bootstraps_from_query_params():
    """Verify F5 persistence and deep-linking by restoring state from URL query parameters."""
    at = AppTest.from_file(APP_PATH, default_timeout=30)
    # Deep-link to Artemis scenario in Vietnamese on morphology tab
    at.query_params["preset"] = "ARTEMIS"
    at.query_params["tab"] = "morph"
    at.query_params["lang"] = "vi"
    at.query_params["g"] = "0.16"
    at.query_params["o2"] = "34.0"
    at.query_params["p"] = "56.5"
    at.query_params["v"] = "15.0"
    at.run()

    assert not at.exception
    assert at.session_state["preset_selector"] == "ARTEMIS"
    assert at.session_state["active_tab_id"] == "morph"
    assert at.session_state["lang"] == "vi"
    assert at.session_state["gravity_val"] == 0.16
    assert at.session_state["o2_val"] == 34.0
    assert at.session_state["p_val"] == 56.5
    assert at.session_state["v_val"] == 15.0


def test_custom_telemetry_detects_custom_preset():
    """Verify that setting non-preset parameter values automatically marks preset as CUSTOM."""
    at = AppTest.from_file(APP_PATH, default_timeout=30)
    at.query_params["g"] = "0.75"
    at.query_params["o2"] = "45.0"
    at.run()

    assert not at.exception
    assert at.session_state["preset_selector"] == "CUSTOM"
    assert at.session_state["gravity_val"] == 0.75
    assert at.session_state["o2_val"] == 45.0


def test_paired_widgets_initialization():
    """Verify that paired slider and number_input state keys are pre-initialized."""
    at = AppTest.from_file(APP_PATH, default_timeout=30)
    at.run()
    assert not at.exception
    for key in ["gravity_val", "o2_val", "p_val", "v_val"]:
        assert f"{key}_slider" in at.session_state
        assert f"{key}_num" in at.session_state
        assert at.session_state[f"{key}_slider"] == at.session_state[key]
        assert at.session_state[f"{key}_num"] == at.session_state[key]


def test_telemetry_cleanup_in_config_toml():
    """Verify that .streamlit/config.toml disables browser usage stats telemetry to eliminate 404s."""
    assert os.path.exists(CONFIG_PATH)
    with open(CONFIG_PATH, "rb") as f:
        cfg = tomllib.load(f)
    assert "browser" in cfg
    assert cfg["browser"].get("gatherUsageStats") is False


def test_favicon_is_local_emoji():
    """Verify that app.py uses inline emoji favicon '🔥' instead of remote CDN URL."""
    with open(APP_PATH, "r", encoding="utf-8") as f:
        content = f.read()
    assert 'page_icon="🔥"' in content
    assert "https://www.nasa.gov/wp-content/plugins/nasa-hds-core-setup/assets/favicons" not in content
