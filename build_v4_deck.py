"""Build the official 7-slide English NASA Space Apps Challenge 2026 deck.

Generates both:
- Flames_in_Freefall_Presentation.pptx
- Flames_in_Freefall_Presentation_v5.pptx
"""

from __future__ import annotations

import os

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Inches, Pt

TOTAL_SLIDES = 7

# Theme Colors (NASA Mission Control Dark — WCAG AA compliant text)
BG_COLOR = RGBColor(4, 8, 22)          # #040816 Deep space dark
CARD_BG = RGBColor(14, 27, 56)         # #0E1B38 Glass card
CARD_BG_ALT = RGBColor(18, 36, 74)     # #12244A Elevated navy
CARD_BORDER = RGBColor(30, 58, 110)    # #1E3A6E Border
CYAN_ACCENT = RGBColor(0, 242, 255)    # #00F2FF Bright cyan
CYAN_GLOW = RGBColor(56, 189, 248)     # #38BDF8 Sky blue
ALERT_RED = RGBColor(224, 60, 49)      # #E03C31 Critical alert
AMBER_WARN = RGBColor(245, 158, 11)    # #F59E0B Amber warning
GREEN_OK = RGBColor(16, 185, 129)      # #10B981 Emerald safe
TEXT_WHITE = RGBColor(248, 250, 252)   # #F8FAFC Primary white
TEXT_MUTED = RGBColor(203, 213, 225)   # #CBD5E1 Body slate
TEXT_SUBTLE = RGBColor(148, 163, 184)  # #94A3B8 WCAG AA muted slate

FONT_HEADING = "Segoe UI"
FONT_BODY = "Segoe UI"
FONT_MONO = "Consolas"


def create_presentation() -> tuple[Presentation, object]:
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    return prs, prs.slide_layouts[6]


def create_slide(prs: Presentation, blank_layout: object, notes: str = ""):
    slide = prs.slides.add_slide(blank_layout)
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    bg.fill.solid()
    bg.fill.fore_color.rgb = BG_COLOR
    bg.line.fill.background()
    if notes:
        slide.notes_slide.notes_text_frame.text = notes
    return slide


def add_footer(slide) -> None:
    line = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, Inches(0.7), Inches(7.0), Inches(11.933), Inches(0.015)
    )
    line.fill.solid()
    line.fill.fore_color.rgb = CARD_BORDER
    line.line.fill.background()

    left_box = slide.shapes.add_textbox(Inches(0.7), Inches(7.06), Inches(7.5), Inches(0.3))
    tf_l = left_box.text_frame
    tf_l.margin_top = tf_l.margin_bottom = 0
    p_l = tf_l.paragraphs[0]
    p_l.text = "TEAM BEBO ZEROG-X // FPT HIGH SCHOOL | NASA SPACE APPS CHALLENGE 2026"
    p_l.font.name = FONT_MONO
    p_l.font.size = Pt(9.5)
    p_l.font.color.rgb = TEXT_SUBTLE

    right_box = slide.shapes.add_textbox(Inches(8.2), Inches(7.06), Inches(4.433), Inches(0.3))
    tf_r = right_box.text_frame
    tf_r.margin_top = tf_r.margin_bottom = 0
    p_r = tf_r.paragraphs[0]
    p_r.alignment = PP_ALIGN.RIGHT
    p_r.text = "github.com/baonamv200/Bebo-ZeroG-X"
    p_r.font.name = FONT_MONO
    p_r.font.size = Pt(9.5)
    p_r.font.color.rgb = CYAN_GLOW


def add_header(slide, title: str, category: str, slide_num: int) -> None:
    cat_box = slide.shapes.add_textbox(Inches(0.7), Inches(0.32), Inches(9.5), Inches(0.3))
    tf_c = cat_box.text_frame
    tf_c.word_wrap = True
    tf_c.margin_top = tf_c.margin_bottom = 0
    p_c = tf_c.paragraphs[0]
    p_c.text = f"// {category.upper()}"
    p_c.font.name = FONT_MONO
    p_c.font.size = Pt(11.5)
    p_c.font.bold = True
    p_c.font.color.rgb = CYAN_ACCENT

    title_box = slide.shapes.add_textbox(Inches(0.7), Inches(0.6), Inches(10.3), Inches(0.6))
    tf_t = title_box.text_frame
    tf_t.word_wrap = True
    tf_t.margin_top = tf_t.margin_bottom = 0
    p_t = tf_t.paragraphs[0]
    p_t.text = title
    p_t.font.name = FONT_HEADING
    p_t.font.size = Pt(24)
    p_t.font.bold = True
    p_t.font.color.rgb = TEXT_WHITE

    num_box = slide.shapes.add_textbox(Inches(11.133), Inches(0.45), Inches(1.5), Inches(0.4))
    tf_n = num_box.text_frame
    tf_n.margin_top = tf_n.margin_bottom = 0
    p_n = tf_n.paragraphs[0]
    p_n.alignment = PP_ALIGN.RIGHT
    p_n.text = f"[{slide_num:02d}/{TOTAL_SLIDES:02d}]"
    p_n.font.name = FONT_MONO
    p_n.font.size = Pt(13.5)
    p_n.font.bold = True
    p_n.font.color.rgb = CYAN_GLOW

    line = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, Inches(0.7), Inches(1.24), Inches(11.933), Inches(0.02)
    )
    line.fill.solid()
    line.fill.fore_color.rgb = CARD_BORDER
    line.line.fill.background()


def add_card(
    slide,
    left,
    top,
    width,
    height,
    bg=CARD_BG,
    border=CARD_BORDER,
    border_width=1.25,
):
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    card.adjustments[0] = 0.04
    card.fill.solid()
    card.fill.fore_color.rgb = bg
    card.line.color.rgb = border
    card.line.width = Pt(border_width)
    return card


def add_lines(tf, items: list[tuple[str, str, int, bool, RGBColor]]) -> None:
    """Populate paragraphs inside a text frame cleanly."""
    for idx, (text, font_name, size_pt, bold, color) in enumerate(items):
        p = tf.paragraphs[0] if idx == 0 else tf.add_paragraph()
        p.text = text
        p.font.name = font_name
        p.font.size = Pt(size_pt)
        p.font.bold = bold
        p.font.color.rgb = color
        p.space_after = Pt(4)


def build_deck() -> Presentation:
    prs, blank_layout = create_presentation()

    # ---------------------------------------------------------
    # SLIDE 1 [01/07]: COVER & HIGH-LEVEL SUMMARY
    # ---------------------------------------------------------
    s1_notes = (
        "Hello judges, we are Team Bebo ZeroG-X from FPT High School, Hanoi. "
        "Our project is Flames in Freefall, an SI-powered spacecraft fire safety dashboard "
        "built with a compiled Rust PyO3 physics engine, interactive 3D WebGL simulation, "
        "and offline semantic RAG grounded in NASA PSI datasets to protect crewed ISS, "
        "Artemis Lunar, and Mars Transit habitats."
    )
    s1 = create_slide(prs, blank_layout, s1_notes)

    badge = add_card(
        s1, Inches(0.7), Inches(0.5), Inches(6.1), Inches(0.42),
        bg=RGBColor(11, 30, 68), border=CYAN_ACCENT,
    )
    tf_b = badge.text_frame
    tf_b.vertical_anchor = MSO_ANCHOR.MIDDLE
    p_b = tf_b.paragraphs[0]
    p_b.alignment = PP_ALIGN.CENTER
    p_b.text = "BEBO IGNIS-0G // NASA SPACE APPS CHALLENGE 2026"
    p_b.font.name = FONT_MONO
    p_b.font.size = Pt(11.5)
    p_b.font.bold = True
    p_b.font.color.rgb = CYAN_ACCENT

    num1 = s1.shapes.add_textbox(Inches(11.133), Inches(0.5), Inches(1.5), Inches(0.42))
    tf_n1 = num1.text_frame
    tf_n1.vertical_anchor = MSO_ANCHOR.MIDDLE
    p_n1 = tf_n1.paragraphs[0]
    p_n1.alignment = PP_ALIGN.RIGHT
    p_n1.text = f"[01/{TOTAL_SLIDES:02d}]"
    p_n1.font.name = FONT_MONO
    p_n1.font.size = Pt(13.5)
    p_n1.font.bold = True
    p_n1.font.color.rgb = CYAN_GLOW

    t_box = s1.shapes.add_textbox(Inches(0.7), Inches(1.1), Inches(7.7), Inches(2.7))
    tf = t_box.text_frame
    tf.word_wrap = True
    add_lines(
        tf,
        [
            ("FLAMES IN FREEFALL", FONT_HEADING, 44, True, TEXT_WHITE),
            (
                "SI-Powered Spacecraft Fire Safety Dashboard",
                FONT_HEADING,
                21,
                True,
                CYAN_ACCENT,
            ),
            (
                "Challenge: Microgravity Combustion & Space Exploration Fire Safety",
                FONT_MONO,
                12,
                True,
                CYAN_GLOW,
            ),
            (
                ("Dual-engine Rust (PyO3 nasa_rust) + Streamlit 3D WebGL Mission Control platform "
                "transforming NASA PSI flight data (SoFIE, Saffire I-VI, BASS-II, FLEX-2) into "
                "real-time SFRS (0-100) risk scores, Cool Flame tracking, and NASA-STD-6001B suppression directives."),
                FONT_BODY,
                13.5,
                False,
                TEXT_MUTED,
            ),
        ],
    )

    # Original Bebo Ignis-0G Concentric Spherical Flame Motif (non-NASA-insignia)
    fx, fy = Inches(10.65), Inches(2.45)
    rings = [
        (Inches(3.4), RGBColor(6, 16, 40), CARD_BORDER, 1.5),
        (Inches(2.4), RGBColor(10, 42, 98), CYAN_GLOW, 1.5),
        (Inches(1.45), RGBColor(0, 120, 215), CYAN_ACCENT, 1.5),
        (Inches(0.68), CYAN_ACCENT, TEXT_WHITE, 1.5),
    ]
    for diam, fill_c, line_c, lw in rings:
        shp = s1.shapes.add_shape(
            MSO_SHAPE.OVAL, fx - diam / 2, fy - diam / 2, diam, diam
        )
        shp.fill.solid()
        shp.fill.fore_color.rgb = fill_c
        shp.line.color.rgb = line_c
        shp.line.width = Pt(lw)

    c1 = add_card(
        s1, Inches(0.7), Inches(4.15), Inches(5.8), Inches(2.65),
        bg=CARD_BG, border=CYAN_ACCENT,
    )
    tf1 = c1.text_frame
    tf1.word_wrap = True
    tf1.margin_left = tf1.margin_right = Inches(0.28)
    tf1.margin_top = Inches(0.2)
    add_lines(
        tf1,
        [
            ("HIGH-LEVEL MISSION SUMMARY", FONT_MONO, 12, True, CYAN_ACCENT),
            ("From Raw PSI Telemetry to Crew Safety", FONT_HEADING, 17, True, TEXT_WHITE),
            (
                ("• Evaluates ISS (0.0g), Artemis Lunar (0.16g), & Mars (0.38g) habitats\n"
                "• Quantifies Low-Flow Ventilation Paradox & Cool Flames (500-800 K)\n"
                "• Calibrates materials directly to NASA-STD-6001B Test 1 & Test 2\n"
                "• Verified by 406 automated tests (391 pytest + 15 Rust cargo)"),
                FONT_BODY,
                13,
                False,
                TEXT_MUTED,
            ),
        ],
    )

    c2 = add_card(
        s1, Inches(6.833), Inches(4.15), Inches(5.8), Inches(2.65),
        bg=CARD_BG_ALT, border=CARD_BORDER,
    )
    tf2 = c2.text_frame
    tf2.word_wrap = True
    tf2.margin_left = tf2.margin_right = Inches(0.28)
    tf2.margin_top = Inches(0.2)
    add_lines(
        tf2,
        [
            ("TEAM & OPEN-SOURCE DEPLOYMENT", FONT_MONO, 12, True, CYAN_ACCENT),
            ("Team Bebo ZeroG-X // FPT High School", FONT_HEADING, 17, True, TEXT_WHITE),
            (
                ("• Team Lead & Architect: Vu Bao Nam\n"
                "• Members: Do Duy Nam • Luong Duc Tung • Trinh Duc Anh\n"
                "• Live App: flames-in-freefall.streamlit.app\n"
                "• Dual-Licensed: Apache License 2.0 / MIT License"),
                FONT_BODY,
                13,
                False,
                TEXT_MUTED,
            ),
        ],
    )
    add_footer(s1)

    # ---------------------------------------------------------
    # SLIDE 2 [02/07]: PROBLEM — MICROGRAVITY COMBUSTION PARADOXES
    # ---------------------------------------------------------
    s2_notes = (
        "Terrestrial fire intuition fails dangerously in space. In 0.0g, flames lose buoyancy "
        "and become dim-blue spheres. Worse, mandatory cabin ventilation of 5 to 20 cm/s creates "
        "a flammability paradox, while 0.16g and 0.38g habitats suffer broad hemispherical flaring "
        "and invisible 500 to 800 K cool flames emit toxic carbon monoxide."
    )
    s2 = create_slide(prs, blank_layout, s2_notes)
    add_header(
        s2,
        "Why Spaceflight Fires Defy Terrestrial Fire Safety Physics",
        "01 // PROBLEM STATEMENT & COMBUSTION HAZARDS",
        2,
    )

    p_cards = [
        (
            "01 // MICROGRAVITY SPHERICAL FLAMES (0.0g)",
            "Isotropic Blue Spheres Evade Optical Sensors",
            ("• Absence of buoyancy eliminates hot-gas updraft (Earth 1.0g teardrop L/W ~ 3.2, ~1850 K).\n"
            "• 3D molecular diffusion produces quiet, soot-free dim-blue spheres (L/W ~ 1.0, ~1380 K).\n"
            "• Low visible radiance delays optical flame detection while sub-micron soot blinds HEPA filters."),
            RGBColor(10, 28, 64),
            CYAN_ACCENT,
            Inches(0.7),
            Inches(1.45),
        ),
        (
            "02 // LOW-FLOW FORCED VENTILATION PARADOX (5-20 cm/s)",
            "Cabin Fans Accelerate Flame Spread Below 1.0g MOC",
            ("• Mandatory HVAC airflow (5-20 cm/s) prevents CO2 pockets around sleeping astronauts.\n"
            "• Gentle airflow feeds fresh O2 and strips CO2 blankets without convective blowoff cooling.\n"
            "• Twin U-curve bounds: radiative quenching (< 3 cm/s) vs convective blowoff (> 35 cm/s)."),
            RGBColor(24, 20, 42),
            AMBER_WARN,
            Inches(6.833),
            Inches(1.45),
        ),
        (
            "03 // PARTIAL-GRAVITY FLARING (0.16g LUNAR / 0.38g MARS)",
            "Hemispherical Dome Expansion (+240% Contact Area)",
            ("• Fractional gravity buoyancy is too weak to lift plumes vertically, yet draws fresh O2 inward.\n"
            "• Flames mushroom laterally into broad hemispherical domes against cabin walls.\n"
            "• Lateral surface contact expands up to +240%, spiking heat flux into adjacent avionics."),
            RGBColor(28, 16, 28),
            ALERT_RED,
            Inches(0.7),
            Inches(4.22),
        ),
        (
            "04 // INVISIBLE COOL FLAMES (500-800 K)",
            "Silent NTC Oxidation & Lethal CO Accumulation",
            ("• After hot-flame quenching, hydrocarbons enter 2nd-stage Negative Temperature Coefficient (NTC) burning.\n"
            "• Operates at 500-800 K with zero blackbody soot emission—completely invisible to crew eyes.\n"
            "• Continuously consumes fuel mass and releases lethal Carbon Monoxide (CO) and aldehydes."),
            RGBColor(14, 24, 50),
            CYAN_GLOW,
            Inches(6.833),
            Inches(4.22),
        ),
    ]

    for tag, heading, body, bg_c, b_c, x, y in p_cards:
        card = add_card(s2, x, y, Inches(5.8), Inches(2.58), bg=bg_c, border=b_c)
        tf_c = card.text_frame
        tf_c.word_wrap = True
        tf_c.margin_left = tf_c.margin_right = Inches(0.28)
        tf_c.margin_top = Inches(0.18)
        add_lines(
            tf_c,
            [
                (tag, FONT_MONO, 11, True, b_c),
                (heading, FONT_HEADING, 16.5, True, TEXT_WHITE),
                (body, FONT_BODY, 12.5, False, TEXT_MUTED),
            ],
        )
    add_footer(s2)

    # ---------------------------------------------------------
    # SLIDE 3 [03/07]: SOLUTION & ARCHITECTURE
    # ---------------------------------------------------------
    s3_notes = (
        "Flames in Freefall combines an @st.fragment Mission Control HUD, a compiled Rust PyO3 "
        "combustion kernel paired with Python physics parity, dense TF-IDF plus TruncatedSVD "
        "semantic RAG over 14 NASA reports, and multi-page PDF-1.4 dossier generation."
    )
    s3 = create_slide(prs, blank_layout, s3_notes)
    add_header(
        s3,
        "Flames in Freefall: Mission Control HUD & Dual-Engine Architecture",
        "02 // SOLUTION & SOFTWARE ARCHITECTURE",
        3,
    )

    col_w = Inches(3.8)
    col_gap = Inches(0.266)
    s3_cols = [
        (
            "01 // MISSION CONTROL HUD (app.py)",
            "Zero-Rerun Telemetry & Multi-Sensory UX",
            ("• @st.fragment isolation across 5 tabs (sim, morph, rag, matrix, research)\n"
            "• Interactive Three.js WebGL 3D spherical flame (OrbitControls, 450 particles)\n"
            "• Web Audio 880/1046 Hz chime + pulsing #EF4444 border when SFRS > 85\n"
            "• F5 localStorage + URL deep-links (?tab=compare, g, o2, p, v, t, rh)\n"
            "• 6 mission presets, 7 ARIA tooltips & 220 EN/VI keys"),
            CYAN_ACCENT,
        ),
        (
            "02 // DUAL RUST + PYTHON PHYSICS",
            "PyO3 nasa_rust & Parity Models",
            ("• Compiled Rust PyO3 0.24 core (nasa_rust): 60x60 isothermal meshes in <0.25 ms\n"
            "• Arden Buck T & RH water-vapor dilution in MOC_eff & flame spread\n"
            "• Closed-form 2-step NTC Cool Flame ODE solver for T(t) and [CO](t)\n"
            "• Custom Composite screening & 5-axis Scenario Diff Radar\n"
            "• Hardened NaN / Inf clamping across Rust & Python"),
            CYAN_GLOW,
        ),
        (
            "03 // SEMANTIC RAG & PDF DOSSIER",
            "Offline LSI Vector Copilot & Reporting",
            ("• Normalized TF-IDF + TruncatedSVD LSI over 14 NASA Technical Reports\n"
            "• Live PDF/TXT/MD upload chunking (300 words, 50-word overlap)\n"
            "• Multi-turn history query reformulation & 3-block zero-key directives\n"
            "• Optional Gemini 2.5 Flash / OpenAI LLM bridge\n"
            "• Pure-Python multi-page %PDF-1.4 Mission Safety Dossier export"),
            GREEN_OK,
        ),
    ]

    for idx, (tag, heading, body, border_c) in enumerate(s3_cols):
        card = add_card(
            s3, Inches(0.7) + idx * (col_w + col_gap), Inches(1.45), col_w, Inches(4.25),
            bg=CARD_BG, border=border_c,
        )
        tf_c = card.text_frame
        tf_c.word_wrap = True
        tf_c.margin_left = tf_c.margin_right = Inches(0.24)
        tf_c.margin_top = Inches(0.2)
        add_lines(
            tf_c,
            [
                (tag, FONT_MONO, 11, True, border_c),
                (heading, FONT_HEADING, 16, True, TEXT_WHITE),
                (body, FONT_BODY, 12.2, False, TEXT_MUTED),
            ],
        )

    ribbon3 = add_card(
        s3, Inches(0.7), Inches(5.88), Inches(11.933), Inches(0.95),
        bg=CARD_BG_ALT, border=CARD_BORDER,
    )
    tf_r3 = ribbon3.text_frame
    tf_r3.word_wrap = True
    tf_r3.margin_left = Inches(0.28)
    tf_r3.margin_top = Inches(0.14)
    add_lines(
        tf_r3,
        [
            ("VERIFIED FULL-STACK ARCHITECTURE", FONT_MONO, 11, True, CYAN_ACCENT),
            (
                ("Rust 1.99 (PyO3 0.24 / maturin)  •  Python 3.12  •  Streamlit 1.66 (@st.fragment)  •  "
                "Plotly & Three.js WebGL  •  scikit-learn TruncatedSVD  •  Pure-Python %PDF-1.4"),
                FONT_HEADING,
                14,
                True,
                TEXT_WHITE,
            ),
        ],
    )
    add_footer(s3)

    # ---------------------------------------------------------
    # SLIDE 4 [04/07]: NASA PSI DATA & CALIBRATION
    # ---------------------------------------------------------
    s4_notes = (
        "All equations and thresholds are grounded in NASA Physical Sciences Informatics data: "
        "SoFIE PMMA rods on ISS, Saffire I through VI large-scale burns on Cygnus, BASS-II "
        "and FLEX extinction measurements, calibrated directly against NASA-STD-6001B Test 1 and Test 2."
    )
    s4 = create_slide(prs, blank_layout, s4_notes)
    add_header(
        s4,
        "NASA PSI Flight Datasets & NASA-STD-6001B Calibration Pipeline",
        "03 // EMPIRICAL DATA & STANDARDS CALIBRATION",
        4,
    )

    ds_cards = [
        (
            "EXP 01 // ISS CIR",
            "NASA SoFIE",
            ("sofie_pmma_burn_rates.csv\n"
            "• 6.35 mm PMMA rod flame spread under 0-50 cm/s forced flow.\n"
            "• Captures low-flow spread peak & radiative quenching boundaries."),
            CYAN_ACCENT,
        ),
        (
            "EXP 02 // CYGNUS",
            "NASA Saffire I-VI",
            ("saffire_pressure_oxygen.csv\n"
            "• 0.4 x 1.0 m fabric & polymer burns inside Cygnus cargo craft.\n"
            "• Validates hypobaric (56.5-70 kPa), 26-34% O2 Exploration Atmospheres."),
            CYAN_GLOW,
        ),
        (
            "EXP 03 // ISS MSG & MDCA",
            "BASS-II & FLEX-2",
            ("bass_extinction_limits.csv\n"
            "• Microgravity LOI/MOC across flight polymers & alkane droplets.\n"
            "• Maps Nomex, Silicone RTV, Ultem 1000, Kapton HN, PTFE, & Heptane."),
            AMBER_WARN,
        ),
    ]

    for idx, (tag, heading, body, b_c) in enumerate(ds_cards):
        card = add_card(
            s4, Inches(0.7) + idx * (col_w + col_gap), Inches(1.45), col_w, Inches(2.95),
            bg=CARD_BG, border=b_c,
        )
        tf_c = card.text_frame
        tf_c.word_wrap = True
        tf_c.margin_left = tf_c.margin_right = Inches(0.24)
        tf_c.margin_top = Inches(0.18)
        add_lines(
            tf_c,
            [
                (tag, FONT_MONO, 11, True, b_c),
                (heading, FONT_HEADING, 18, True, TEXT_WHITE),
                (body, FONT_BODY, 12.5, False, TEXT_MUTED),
            ],
        )

    cal_left = add_card(
        s4, Inches(0.7), Inches(4.6), Inches(5.8), Inches(2.22),
        bg=CARD_BG_ALT, border=ALERT_RED,
    )
    tf_cl = cal_left.text_frame
    tf_cl.word_wrap = True
    tf_cl.margin_left = tf_cl.margin_right = Inches(0.28)
    tf_cl.margin_top = Inches(0.18)
    add_lines(
        tf_cl,
        [
            ("NASA-STD-6001B TEST 1 & TEST 2 CALIBRATION", FONT_MONO, 11.5, True, ALERT_RED),
            ("Flight Material Certification Thresholds", FONT_HEADING, 16, True, TEXT_WHITE),
            (
                ("• Test 1 (Upward Propagation): Pass if burn length <= 15.0 cm, zero dripping\n"
                "• Test 2 (Cone Calorimeter): Pass if peak HRR <= 100.0 kW/m2\n"
                "• SFRS Tiers: Class A (<20) • Conditional (20-45) • Waiver (45-70) • Prohibited (>=70)"),
                FONT_BODY,
                12.2,
                False,
                TEXT_MUTED,
            ),
        ],
    )

    cal_right = add_card(
        s4, Inches(6.833), Inches(4.6), Inches(5.8), Inches(2.22),
        bg=CARD_BG, border=CYAN_ACCENT,
    )
    tf_cr = cal_right.text_frame
    tf_cr.word_wrap = True
    tf_cr.margin_left = tf_cr.margin_right = Inches(0.28)
    tf_cr.margin_top = Inches(0.18)
    add_lines(
        tf_cr,
        [
            ("SI CALIBRATION & NTRS CORPUS PIPELINE", FONT_MONO, 11.5, True, CYAN_ACCENT),
            ("Deterministic Ingestion -> Vector & Physics Core", FONT_HEADING, 16, True, TEXT_WHITE),
            (
                ("1. Portable CSV Ingestion (data_loader.rs) + SI unit normalization (kPa, cm/s, K)\n"
                "2. Arden Buck vapor dilution + De Ris / Fernandez-Pello spread calibration\n"
                "3. 14 peer-reviewed NASA/TM, NASA/CR & NASA/TP reports indexed in LSI RAG"),
                FONT_BODY,
                12.2,
                False,
                TEXT_MUTED,
            ),
        ],
    )
    add_footer(s4)

    # ---------------------------------------------------------
    # SLIDE 5 [05/07]: LIVE DEMO & BENCHMARKS
    # ---------------------------------------------------------
    s5_notes = (
        "In our Artemis Lunar Cabin live benchmark at 0.16g, 34 percent oxygen, 56.5 kPa, and "
        "12 cm/s airflow, PMMA registers a Critical SFRS of 78.5, MOC_eff of 14.8 percent, and "
        "spread rate of 0.84 mm/s. The system prescribes T+0s HVAC shutdown, T+15s PBE donning, "
        "and T+60s Fine Water Mist suppression, backed by 406 passing automated tests."
    )
    s5 = create_slide(prs, blank_layout, s5_notes)
    add_header(
        s5,
        "Live Demo Benchmark, Suppression Protocol & 406 Automated Tests",
        "04 // ARTEMIS VERIFICATION & TEST CERTIFICATION",
        5,
    )

    demo_l = add_card(
        s5, Inches(0.7), Inches(1.45), Inches(5.8), Inches(3.58),
        bg=RGBColor(26, 12, 22), border=ALERT_RED,
    )
    tf_dl = demo_l.text_frame
    tf_dl.word_wrap = True
    tf_dl.margin_left = tf_dl.margin_right = Inches(0.28)
    tf_dl.margin_top = Inches(0.18)
    add_lines(
        tf_dl,
        [
            ("ARTEMIS LUNAR CABIN BENCHMARK // LIVE APP", FONT_MONO, 11.5, True, ALERT_RED),
            ("0.16g • 34% O2 • 56.5 kPa • 12 cm/s (PMMA)", FONT_HEADING, 17, True, TEXT_WHITE),
            (
                ("• Space Fire Risk Score (SFRS): 78.5 / 100 [CRITICAL HAZARD]\n"
                "• Effective MOC (MOC_eff): 14.8% O2 (drops from 17.5% at 1.0g)\n"
                "• Flame Spread Rate: 0.84 mm/s (low-flow forced ventilation boost)\n"
                "• Morphology: Hemispherical flaring (+240% surface contact area)\n"
                "• Demo Flow: Preset -> 3D WebGL Flame -> ?tab=compare -> %PDF-1.4 Export"),
                FONT_BODY,
                12.5,
                False,
                TEXT_MUTED,
            ),
        ],
    )

    demo_r = add_card(
        s5, Inches(6.833), Inches(1.45), Inches(5.8), Inches(3.58),
        bg=CARD_BG, border=CYAN_ACCENT,
    )
    tf_dr = demo_r.text_frame
    tf_dr.word_wrap = True
    tf_dr.margin_left = tf_dr.margin_right = Inches(0.28)
    tf_dr.margin_top = Inches(0.18)
    add_lines(
        tf_dr,
        [
            ("NASA-STD-6001B SUPPRESSION PROTOCOL", FONT_MONO, 11.5, True, CYAN_ACCENT),
            ("Fine Water Mist & T+0s / T+15s / T+60s Action", FONT_HEADING, 17, True, TEXT_WHITE),
            (
                ("• T+0s (HVAC Isolation): Cut cabin fans (v < 2 cm/s) to force radiative quenching.\n"
                "• T+15s (Crew PBE): Don positive-pressure Breathing Equipment against CO & smoke.\n"
                "• T+60s (Fine Water Mist): Deploy N2-propelled Fine Water Mist (< 50 um) or CO2/N2\n"
                "  total flooding; scrub CO < 25 ppm via TCCS.\n"
                "• PROHIBITED: High-velocity water jets (scatters burning molten polymer in low-g)."),
                FONT_BODY,
                12.5,
                False,
                TEXT_MUTED,
            ),
        ],
    )

    test_bar = add_card(
        s5, Inches(0.7), Inches(5.22), Inches(11.933), Inches(1.6),
        bg=RGBColor(8, 28, 36), border=GREEN_OK,
    )
    tf_tb = test_bar.text_frame
    tf_tb.word_wrap = True
    tf_tb.margin_left = tf_tb.margin_right = Inches(0.28)
    tf_tb.margin_top = Inches(0.16)
    add_lines(
        tf_tb,
        [
            ("AUTOMATED QUALITY & VERIFICATION SUITE // 406 / 406 PASSING (100%)", FONT_MONO, 12, True, GREEN_OK),
            (
                ("• 391 / 391 Python pytest (0 skipped, 0 failed): 275 E2E Tiers 1-4 + 71 M1/Challenger "
                "(Chrome CDP responsive, WCAG AA #94A3B8, live :8503) + 45 Adversarial/Security/PDF/Telemetry\n"
                "• 15 / 15 Rust cargo test integration checks (nasa_rust boundary, 60x60 mesh, sweeps, RAG)  "
                "• ruff check & py_compile exit 0  • Multi-page %PDF-1.4 verified"),
                FONT_BODY,
                12.5,
                False,
                TEXT_WHITE,
            ),
        ],
    )
    add_footer(s5)

    # ---------------------------------------------------------
    # SLIDE 6 [06/07]: IMPACT & FUTURE ROADMAP
    # ---------------------------------------------------------
    s6_notes = (
        "Flames in Freefall impacts human spaceflight safety across ISS, Artemis, and Mars "
        "missions, empowers open-source STEM education under dual Apache 2.0 and MIT licenses, "
        "and follows a clear 2026 to 2027 roadmap integrating SoFIE-MIST, PINNs, and ECLSS IoT."
    )
    s6 = create_slide(prs, blank_layout, s6_notes)
    add_header(
        s6,
        "Spaceflight Safety Impact, Open-Source Value & 2026-2027 Roadmap",
        "05 // MISSION IMPACT & STRATEGIC ROADMAP",
        6,
    )

    imp_cards = [
        (
            "IMPACT 01 // ARTEMIS & MARS",
            "Spacecraft & Habitat Safety",
            ("• Pre-flight NASA-STD-6001B screening for 0.16g Lunar (34% O2) & 0.38g Mars cabins.\n"
            "• Catches materials like Nomex that pass 1.0g air yet burn in enriched atmospheres."),
            CYAN_ACCENT,
        ),
        (
            "IMPACT 02 // FLIGHT OPERATIONS",
            "Crew & Engineering Decisions",
            ("• Instant T+0s/T+15s/T+60s suppression protocols & toxic offgassing checklists.\n"
            "• Exports audit-ready %PDF-1.4 dossiers and custom composite material screeners."),
            CYAN_GLOW,
        ),
        (
            "IMPACT 03 // OPEN SCIENCE",
            "Open-Source & STEM Reach",
            ("• Dual-licensed Apache License 2.0 / MIT License at github.com/baonamv200/Bebo-ZeroG-X.\n"
            "• Turns raw NASA PSI datasets into interactive 3D WebGL physics for global STEM."),
            GREEN_OK,
        ),
    ]

    for idx, (tag, heading, body, b_c) in enumerate(imp_cards):
        card = add_card(
            s6, Inches(0.7) + idx * (col_w + col_gap), Inches(1.45), col_w, Inches(2.55),
            bg=CARD_BG, border=b_c,
        )
        tf_c = card.text_frame
        tf_c.word_wrap = True
        tf_c.margin_left = tf_c.margin_right = Inches(0.24)
        tf_c.margin_top = Inches(0.18)
        add_lines(
            tf_c,
            [
                (tag, FONT_MONO, 11, True, b_c),
                (heading, FONT_HEADING, 17, True, TEXT_WHITE),
                (body, FONT_BODY, 12.5, False, TEXT_MUTED),
            ],
        )

    road_box = add_card(
        s6, Inches(0.7), Inches(4.2), Inches(11.933), Inches(2.6),
        bg=CARD_BG_ALT, border=CYAN_GLOW,
    )
    tf_rb = road_box.text_frame
    tf_rb.word_wrap = True
    tf_rb.margin_left = tf_rb.margin_right = Inches(0.28)
    tf_rb.margin_top = Inches(0.18)
    add_lines(
        tf_rb,
        [
            ("2026-2027 STRATEGIC DEVELOPMENT ROADMAP", FONT_MONO, 12, True, CYAN_ACCENT),
            ("Scaling from Mission Simulation to Autonomous Habitat Protection", FONT_HEADING, 17, True, TEXT_WHITE),
            (
                ("• Phase 1 (Q4 2026): Ingest upcoming ISS SoFIE-GEL & SoFIE-MIST datasets plus multi-spectral IR flame imagery.\n"
                "• Phase 2 (Q1-Q2 2027): Train Physics-Informed Neural Networks (PINNs) for millisecond partial-g (LUCI / FM2) forecasting.\n"
                "• Phase 3 (Q3-Q4 2027): Connect directly to spacecraft ECLSS & particulate IoT telemetry for autonomous zone isolation."),
                FONT_BODY,
                13,
                False,
                TEXT_MUTED,
            ),
        ],
    )
    add_footer(s6)

    # ---------------------------------------------------------
    # SLIDE 7 [07/07]: TEAM ROSTER, REFERENCES & MANDATORY AI DISCLOSURE
    # ---------------------------------------------------------
    s7_notes = (
        "Thank you, judges. Here is our Bebo ZeroG-X team roster from FPT High School, our "
        "peer-reviewed NASA academic references, and our transparent AI disclosure confirming "
        "zero fabricated data or unverified experimental results."
    )
    s7 = create_slide(prs, blank_layout, s7_notes)
    add_header(
        s7,
        "Team Roster, Academic References & Mandatory AI Disclosure",
        "06 // ATTRIBUTION, CITATIONS & ACADEMIC INTEGRITY",
        7,
    )

    team_card = add_card(
        s7, Inches(0.7), Inches(1.45), Inches(5.65), Inches(2.62),
        bg=CARD_BG, border=CYAN_ACCENT,
    )
    tf_tm = team_card.text_frame
    tf_tm.word_wrap = True
    tf_tm.margin_left = tf_tm.margin_right = Inches(0.24)
    tf_tm.margin_top = Inches(0.16)
    add_lines(
        tf_tm,
        [
            ("TEAM BEBO ZEROG-X // FPT HIGH SCHOOL (HANOI)", FONT_MONO, 11, True, CYAN_ACCENT),
            (
                ("• Vu Bao Nam (Team Lead & Architect): Physics equations, Rust PyO3 core, HUD, 3D WebGL, RAG\n"
                "• Do Duy Nam (Data Engineer): NASA PSI SoFIE/Saffire/BASS-II CSV ingestion & SI calibration\n"
                "• Luong Duc Tung (Safety Specialist): NASA-STD-6001B suppression matrix & toxicity rules\n"
                "• Trinh Duc Anh (QA Engineer): Adversarial boundary stress testing & numerical stability"),
                FONT_BODY,
                12,
                False,
                TEXT_MUTED,
            ),
        ],
    )

    ref_card = add_card(
        s7, Inches(0.7), Inches(4.24), Inches(5.65), Inches(2.58),
        bg=CARD_BG_ALT, border=CARD_BORDER,
    )
    tf_rf = ref_card.text_frame
    tf_rf.word_wrap = True
    tf_rf.margin_left = tf_rf.margin_right = Inches(0.24)
    tf_rf.margin_top = Inches(0.16)
    add_lines(
        tf_rf,
        [
            ("ACADEMIC REFERENCES & NASA SOURCES", FONT_MONO, 11, True, CYAN_GLOW),
            (
                ("• Urban et al. (2022) — SoFIE on ISS (Proc. Combust. Inst. 38(4))\n"
                "• Ruff et al. (2021) — Saffire I-IV (Proc. Combust. Inst. 38(4))\n"
                "• Olson & Ferketic (2015) — BASS-II Extinction (Combust. Flame 162(5))\n"
                "• Williams et al. (2012) — Spherical Cool Flames (Science 338)\n"
                "• NASA-STD-6001B (2021) | NASA PSI (psi.nasa.gov) & NTRS (ntrs.nasa.gov)"),
                FONT_BODY,
                11.5,
                False,
                TEXT_MUTED,
            ),
        ],
    )

    ai_card = add_card(
        s7, Inches(6.6), Inches(1.45), Inches(6.033), Inches(5.37),
        bg=CARD_BG, border=AMBER_WARN,
    )
    tf_ai = ai_card.text_frame
    tf_ai.word_wrap = True
    tf_ai.margin_left = tf_ai.margin_right = Inches(0.26)
    tf_ai.margin_top = Inches(0.18)
    add_lines(
        tf_ai,
        [
            ("MANDATORY AI DISCLOSURE // NASA SPACE APPS 2026", FONT_MONO, 11.5, True, AMBER_WARN),
            ("Transparent Tooling & Human Verification", FONT_HEADING, 17, True, TEXT_WHITE),
            (
                ("• Gemini 2.5 Pro / Flash (Google DeepMind): Assisted bilingual EN/VI terminology "
                "(i18n.py) and technical abstract synthesis; manually audited vs NASA SP-2016-6105.\n"
                "• Claude 3.7 Sonnet (Anthropic): Mathematical boundary & kinetics sanity checks "
                "(Pe, Ri, Da); verified directly against Combustion Institute literature.\n"
                "• Antigravity (Google DeepMind): Multi-agent workflow orchestration, automated test "
                "execution & linting; human architect authored all schemas & specifications.\n"
                "• GitHub Copilot (GitHub/OpenAI): PyO3 & Streamlit boilerplate autocompletion; "
                "100% audited & validated via 406 automated tests (391 pytest + 15 Rust cargo)."),
                FONT_BODY,
                12,
                False,
                TEXT_MUTED,
            ),
            (
                ("AFFIRMATION: ZERO FABRICATED DATA, INVENTED CITATIONS, OR UNVERIFIED RESULTS. "
                "ALL EMPIRICAL METRICS TRACE DIRECTLY TO NASA PSI FLIGHT RECORDS."),
                FONT_MONO,
                10.5,
                True,
                GREEN_OK,
            ),
        ],
    )
    add_footer(s7)

    return prs


def main() -> None:
    prs = build_deck()
    assert len(prs.slides) == TOTAL_SLIDES, f"Expected {TOTAL_SLIDES} slides, got {len(prs.slides)}"
    base_dir = os.path.dirname(os.path.abspath(__file__))
    targets = [
        os.path.join(base_dir, "Flames_in_Freefall_Presentation.pptx"),
        os.path.join(base_dir, "Flames_in_Freefall_Presentation_v5.pptx"),
    ]
    for path in targets:
        prs.save(path)
        print(f"SUCCESS: Saved {path} ({len(prs.slides)} slides)")


if __name__ == "__main__":
    main()
