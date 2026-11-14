"""Unit tests for Feature 7: Acronym Tooltip Library in i18n.py"""
import pytest
from i18n import ACRONYM_DICTIONARY, render_acronym_tooltip

def test_all_required_acronyms_present():
    required = ["Da", "Re", "Pe", "Ri", "SFRS", "MOC", "ΔO2%"]
    for acr in required:
        assert acr in ACRONYM_DICTIONARY, f"Missing acronym: {acr}"
        entry = ACRONYM_DICTIONARY[acr]
        assert "en" in entry["term"] and "vi" in entry["term"]
        assert "en" in entry["description"] and "vi" in entry["description"]
        assert len(entry["description"]["en"]) > 20
        assert len(entry["description"]["vi"]) > 20
        assert "full_abbr" in entry
        assert "formula" in entry

def test_render_acronym_tooltip_html_en():
    html_en = render_acronym_tooltip("Da", lang="en")
    assert '<abbr class="nasa-acronym-abbr"' in html_en
    assert 'tabindex="0"' in html_en
    assert 'Damköhler Number' in html_en
    assert 'role="tooltip"' in html_en
    assert 'class="nasa-tt-card"' in html_en
    assert 'class="nasa-tt-formula"' in html_en

def test_render_acronym_tooltip_html_vi():
    html_vi = render_acronym_tooltip("SFRS", lang="vi")
    assert '<abbr class="nasa-acronym-abbr"' in html_vi
    assert 'tabindex="0"' in html_vi
    assert 'Điểm Nguy cơ Cháy Tàu Vũ trụ' in html_vi
    assert 'role="tooltip"' in html_vi

def test_render_acronym_tooltip_custom_display_text():
    html = render_acronym_tooltip("MOC", lang="en", display_text="<b>MOC_eff:</b>")
    assert '<span class="nasa-acronym-text"><b>MOC_eff:</b></span>' in html
    assert 'Maximum Oxygen Concentration' in html

def test_render_acronym_tooltip_aliases():
    for alias in ["Delta_O2", "dO2", "delta_o2", "ΔO2", "ΔO2%"]:
        html = render_acronym_tooltip(alias, lang="en")
        assert "Oxygen Safety Margin" in html
        assert 'class="nasa-tt-badge">ΔO2%' in html

def test_render_acronym_tooltip_unknown_key():
    fallback = render_acronym_tooltip("UNKNOWN_ACRONYM", lang="en", display_text="Custom Text")
    assert fallback == "Custom Text"
    fallback_default = render_acronym_tooltip("UNKNOWN_ACRONYM", lang="en")
    assert fallback_default == "UNKNOWN_ACRONYM"
