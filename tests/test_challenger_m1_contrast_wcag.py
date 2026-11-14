"""
Empirical WCAG 2.1 SC 1.4.3 (Contrast Minimum - AA) and SC 1.4.6 (Contrast Enhanced - AAA)
Auditing text, badges, and borders against dark space backgrounds (#060D1A and #0D1930).
"""

import pytest

DARK_BG_DEEP = "#060D1A"
DARK_BG_SECONDARY = "#0D1930"


def srgb_to_lin(c):
    c = c / 255.0
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def relative_luminance(hex_code):
    hex_code = hex_code.lstrip('#')
    r, g, b = [int(hex_code[i:i+2], 16) for i in (0, 2, 4)]
    return 0.2126 * srgb_to_lin(r) + 0.7152 * srgb_to_lin(g) + 0.0722 * srgb_to_lin(b)


def contrast_ratio(hex1, hex2):
    l1 = relative_luminance(hex1)
    l2 = relative_luminance(hex2)
    lighter = max(l1, l2)
    darker = min(l1, l2)
    return (lighter + 0.05) / (darker + 0.05)


# Palette used in NASA Fire Safety UI
CORE_TEXT_PALETTE = {
    "White": "#FFFFFF",
    "Slate 50 (Body)": "#F8FAFC",
    "Gray 100": "#F3F4F6",
    "Slate 200 (Subheadings)": "#E2E8F0",
    "Slate 300 (Citations/Tables)": "#CBD5E1",
    "Sky 200 (Card Labels)": "#BAE6FD",
    "Sky 300 (Moderate text)": "#7DD3FC",
    "NASA Cyan (Accent)": "#38BDF8",
    "Slate 400 (Muted/Units)": "#94A3B8",
}

STATUS_BADGES = {
    "Critical Text": "#FCA5A5",
    "Critical Border": "#EF4444",
    "High Text": "#FDE68A",
    "High Border": "#F59E0B",
    "Moderate Text": "#7DD3FC",
    "Moderate Border": "#38BDF8",
    "Safe Text": "#6EE7B7",
    "Safe Border": "#10B981",
}


def test_core_text_palette_wcag_aa():
    """Verify all primary body, heading, and label text exceeds WCAG AA (4.5:1)."""
    for name, hex_code in CORE_TEXT_PALETTE.items():
        cr_deep = contrast_ratio(hex_code, DARK_BG_DEEP)
        cr_sec = contrast_ratio(hex_code, DARK_BG_SECONDARY)
        assert cr_deep >= 4.5, f"{name} ({hex_code}) failed AA vs {DARK_BG_DEEP}: {cr_deep:.2f}:1"
        assert cr_sec >= 4.5, f"{name} ({hex_code}) failed AA vs {DARK_BG_SECONDARY}: {cr_sec:.2f}:1"


def test_status_badges_contrast():
    """Verify status badge text passes WCAG AA (4.5:1) and borders pass graphical UI (3.0:1)."""
    for name, hex_code in STATUS_BADGES.items():
        cr_deep = contrast_ratio(hex_code, DARK_BG_DEEP)
        cr_sec = contrast_ratio(hex_code, DARK_BG_SECONDARY)
        
        if "Text" in name:
            assert cr_deep >= 4.5, f"Badge text {name} ({hex_code}) fails AA vs {DARK_BG_DEEP}: {cr_deep:.2f}:1"
            assert cr_sec >= 4.5, f"Badge text {name} ({hex_code}) fails AA vs {DARK_BG_SECONDARY}: {cr_sec:.2f}:1"
        elif "Border" in name:
            # SC 1.4.11 Non-text Contrast requires 3.0:1 for graphical objects and UI components
            assert cr_deep >= 3.0, f"Badge border {name} ({hex_code}) fails UI vs {DARK_BG_DEEP}: {cr_deep:.2f}:1"
            assert cr_sec >= 3.0, f"Badge border {name} ({hex_code}) fails UI vs {DARK_BG_SECONDARY}: {cr_sec:.2f}:1"


def test_audit_slate_500_contrast_deficiency():
    """
    CRITIC FINDING: Slate 500 (#64748B) is used for text in team credits, Z-axis labels,
    and KELVIN FIELD tags, but fails WCAG AA (4.5:1) against both dark space backgrounds.
    """
    hex_code = "#64748B"
    cr_deep = contrast_ratio(hex_code, DARK_BG_DEEP)
    cr_sec = contrast_ratio(hex_code, DARK_BG_SECONDARY)
    
    # Empirically document the contrast deficit
    assert cr_deep < 4.5, f"Expected deficiency, but got {cr_deep:.2f}:1"
    assert cr_sec < 4.5, f"Expected deficiency, but got {cr_sec:.2f}:1"
    print(f"\nEmpirically reproduced contrast deficiency for #64748B: {cr_deep:.2f}:1 vs #060D1A, {cr_sec:.2f}:1 vs #0D1930 (Requires >= 4.5:1)")


def test_audit_wcag_aaa_contrast():
    """
    Audit text against WCAG AAA (7.0:1).
    Identify colors that achieve AA (4.5:1) but fall below AAA (7.0:1).
    """
    aaa_passes = []
    aaa_fails = []
    
    for name, hex_code in CORE_TEXT_PALETTE.items():
        cr_deep = contrast_ratio(hex_code, DARK_BG_DEEP)
        cr_sec = contrast_ratio(hex_code, DARK_BG_SECONDARY)
        if cr_deep >= 7.0 and cr_sec >= 7.0:
            aaa_passes.append((name, hex_code, min(cr_deep, cr_sec)))
        else:
            aaa_fails.append((name, hex_code, min(cr_deep, cr_sec)))
            
    print(f"\nWCAG AAA (7.0:1) Passed: {len(aaa_passes)}, Failed: {len(aaa_fails)}")
    for name, hex_code, cr in aaa_fails:
        print(f"  Fails AAA (< 7:1): {name} ({hex_code}) with min contrast {cr:.2f}:1")
    
    # Document that Slate 400 (#94A3B8) achieves 6.83:1 vs #0D1930, just below 7.0:1 AAA threshold
    assert any(hex_code == "#94A3B8" for _, hex_code, _ in aaa_fails)
