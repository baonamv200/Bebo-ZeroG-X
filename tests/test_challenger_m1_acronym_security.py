"""
Empirical Edge Case & Security Fuzzing for Feature 7: Acronym Tooltips.
Tests:
1. XSS injection via display_text
2. XSS injection via acronym_key (missing key fallback)
3. HTML attribute injection via quotes in display_text or acronym_key
4. NoneType handling (crash on .strip())
5. Empty and whitespace string handling
6. Extremely long payloads (ReDoS / memory / buffer)
7. Non-ASCII, unicode, RTL and emoji keys
8. Unsupported language tags
"""

import html
import pytest
import i18n
from i18n import ACRONYM_DICTIONARY, render_acronym_tooltip


def test_tooltip_none_key_raises_attribute_error():
    """Verify passing None as acronym_key degrades gracefully without AttributeError."""
    assert render_acronym_tooltip(None) == ""
    assert render_acronym_tooltip(None, display_text="Fallback") == "Fallback"


def test_tooltip_xss_in_display_text():
    """Verify raw HTML/JS script injection in display_text is properly escaped."""
    xss_payload = '<script>alert("XSS")</script>'
    rendered = render_acronym_tooltip("Da", display_text=xss_payload)

    assert "<script>" not in rendered
    assert "&lt;script&gt;" in rendered
    assert html.escape(xss_payload, quote=True) in rendered


def test_tooltip_xss_in_missing_key():
    """Verify unknown acronym_key with XSS payload is returned HTML-escaped."""
    xss_key = '<img src=x onerror=alert("XSS")>'
    rendered = render_acronym_tooltip(xss_key)

    assert "<img" not in rendered
    assert "&lt;img" in rendered
    assert html.escape(xss_key, quote=True) in rendered


def test_tooltip_attribute_breakout():
    """Verify attribute breakout payloads with quotes are safely escaped."""
    payload = '"><svg onload=alert(1)>'
    rendered = render_acronym_tooltip("MOC", display_text=payload)

    assert "<svg" not in rendered
    assert "&quot;&gt;&lt;svg" in rendered
    assert '<span class="nasa-acronym-text">&quot;&gt;&lt;svg onload=alert(1)&gt;</span>' in rendered


def test_tooltip_empty_and_whitespace():
    """Tests edge cases with empty string and pure whitespace."""
    assert render_acronym_tooltip("") == ""
    assert render_acronym_tooltip("   ") == "   "
    assert render_acronym_tooltip("", display_text="Fallback") == "Fallback"


def test_tooltip_long_string_stress():
    """Stress test with 100,000 character string."""
    long_key = "A" * 100_000
    res = render_acronym_tooltip(long_key)
    assert len(res) == 100_000


def test_tooltip_unicode_and_special_keys():
    """Test unicode, emojis, and special chars."""
    for special in ["🔥", "ΔO2%", "Ω_flame", "日本語", "مرحبا"]:
        res = render_acronym_tooltip(special)
        assert isinstance(res, str)


def test_tooltip_unsupported_language_fallback():
    """Verify fallback when an unknown language code is supplied."""
    res_fr = render_acronym_tooltip("Da", lang="fr")
    # Should fall back gracefully to English
    assert "Damköhler Number" in res_fr
