"""
Empirical Verification for Feature 4: Telemetry & Favicon.
Verifies:
1. gatherUsageStats is strictly false in .streamlit/config.toml
2. app.py set_page_config uses local/emoji favicon (no external CDN)
3. Live HTML response from Streamlit server contains no external CDN favicon requests
4. Static scan of app.py and i18n.py for external favicon assets
"""

import os
import re
import urllib.request
import pytest

try:
    import tomllib
except ImportError:
    import tomli as tomllib


def test_telemetry_gather_usage_stats_is_false():
    """Verify gatherUsageStats is explicitly false in config.toml."""
    config_path = os.path.join(os.path.dirname(__file__), "..", ".streamlit", "config.toml")
    assert os.path.exists(config_path), "config.toml not found"
    
    with open(config_path, "rb") as f:
        config = tomllib.load(f)
    
    assert "browser" in config, "[browser] section missing in config.toml"
    assert config["browser"].get("gatherUsageStats") is False, (
        f"Expected gatherUsageStats = false, got {config['browser'].get('gatherUsageStats')}"
    )


def test_set_page_config_favicon_in_app():
    """Verify st.set_page_config uses an emoji or local asset, not a remote CDN URL."""
    app_path = os.path.join(os.path.dirname(__file__), "..", "app.py")
    with open(app_path, "r", encoding="utf-8") as f:
        code = f.read()
    
    # Locate set_page_config call by finding opening and matching closing parenthesis
    idx = code.find("st.set_page_config(")
    assert idx != -1, "st.set_page_config not found in app.py"
    start = idx + len("st.set_page_config(")
    depth = 1
    end = start
    while end < len(code) and depth > 0:
        if code[end] == "(":
            depth += 1
        elif code[end] == ")":
            depth -= 1
        end += 1
    
    config_args = code[start:end-1]
    assert "page_icon" in config_args, "page_icon not specified in st.set_page_config"
    
    # Assert page_icon is NOT an external URL (http:// or https://)
    assert "http://" not in config_args and "https://" not in config_args, (
        "st.set_page_config contains external URL for page_icon"
    )
    # Should be emoji "🔥"
    assert '"🔥"' in config_args or "'🔥'" in config_args, f"Expected emoji '🔥', found: {config_args}"


def test_no_external_favicon_in_codebase():
    """Verify no external favicon CDNs exist in the codebase."""
    for filename in ["app.py", "i18n.py"]:
        path = os.path.join(os.path.dirname(__file__), "..", filename)
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Check for remote favicon links
        bad_patterns = [
            r'https?://[^"\']*(?:favicon\.ico|favicon\.png)',
            r'https?://[^"\']*nasa\.gov/[^"\']*favicon',
            r'<link[^>]*rel=["\'](?:shortcut )?icon["\'][^>]*href=["\']https?://'
        ]
        for pattern in bad_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            assert len(matches) == 0, f"Found remote favicon pattern '{pattern}' in {filename}: {matches}"


def test_live_server_favicon_and_telemetry_isolation():
    """Query live Streamlit server to inspect served HTML and headers."""
    try:
        req = urllib.request.urlopen("http://localhost:8503", timeout=3)
        html_body = req.read().decode("utf-8", errors="replace")
    except Exception as e:
        pytest.skip(f"Live server not available: {e}")
    
    # Check that there are no external CDN favicon tags injected into <head>
    head_favicons = re.findall(r'<link[^>]+(?:icon|favicon)[^>]*>', html_body, re.IGNORECASE)
    for tag in head_favicons:
        assert "http://" not in tag and "https://" not in tag, (
            f"External CDN favicon link found in live HTML: {tag}"
        )
