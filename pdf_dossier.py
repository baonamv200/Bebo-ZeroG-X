"""Pure-Python NASA Technical Memorandum PDF dossier generator."""

from __future__ import annotations

import math
import unicodedata
from typing import Any


def _safe_float(value: Any, default: float) -> float:
    """Coerce numeric inputs to finite floats, falling back to default on errors."""
    try:
        parsed = float(value)
    except (TypeError, ValueError):
        return default
    return parsed if math.isfinite(parsed) else default


def _ascii_pdf_text(text: str) -> str:
    """Normalize text to printable ASCII and escape PDF string delimiters."""
    replaced = text.replace("đ", "d").replace("Đ", "D")
    normalized = unicodedata.normalize("NFKD", replaced)
    ascii_str = normalized.encode("ascii", "ignore").decode("ascii")
    # Preserve fallback if string consisted purely of non-ASCII chars without decomposition
    if not ascii_str.strip() and text.strip():
        ascii_str = text.encode("ascii", "replace").decode("ascii")
    return (
        ascii_str.replace("\\", "\\\\")
        .replace("(", "\\(")
        .replace(")", "\\)")
        .replace("\r", " ")
        .replace("\n", " ")
    )


def _format_scenario_lines(scenario_data: dict[str, Any]) -> list[str]:
    """Extract scenario telemetry supporting both contract and app.py keys."""
    mission = str(scenario_data.get("mission", scenario_data.get("preset_name", "ISS Nominal")))
    g = _safe_float(scenario_data.get("g", scenario_data.get("gravity_g", 0.0)), 0.0)
    o2 = _safe_float(scenario_data.get("o2", scenario_data.get("oxygen_pct", 21.0)), 21.0)
    p = _safe_float(scenario_data.get("p", scenario_data.get("pressure_kpa", 101.3)), 101.3)
    v = _safe_float(scenario_data.get("v", scenario_data.get("airflow_cm_s", 10.0)), 10.0)
    t = _safe_float(
        scenario_data.get(
            "t",
            scenario_data.get("temp_c", scenario_data.get("temperature_c", 21.0)),
        ),
        21.0,
    )
    rh = _safe_float(
        scenario_data.get(
            "rh",
            scenario_data.get("rh_pct", scenario_data.get("humidity_pct", 45.0)),
        ),
        45.0,
    )
    sfrs = _safe_float(scenario_data.get("sfrs", scenario_data.get("max_sfrs", 52.4)), 52.4)
    tier = str(scenario_data.get("tier", "HIGH"))
    nasa_status = str(scenario_data.get("nasa_status", "CONDITIONAL"))

    return [
        "NASA TECHNICAL MEMORANDUM: SPACECRAFT FIRE SAFETY DOSSIER",
        f"Mission Scenario: {_ascii_pdf_text(mission)}",
        f"Gravity: {g:.3f} g | Oxygen Concentration: {o2:.1f}%",
        f"Pressure: {p:.1f} kPa | Forced Airflow Velocity: {v:.1f} cm/s",
        f"Cabin Temperature: {t:.1f} C | Relative Humidity: {rh:.1f}%",
        f"Max Space Fire Risk Score (SFRS): {sfrs:.2f} | Tier: {_ascii_pdf_text(tier)}",
        f"NASA-STD-6001B Compliance Status: {_ascii_pdf_text(nasa_status)}",
        "------------------------------------------------------------------------",
        "Material Screening Matrix (NASA-STD-6001B & PSI Reference):",
        "Material | SFRS | MOC_eff (%) | Spread (mm/s) | Status",
    ]


def _format_material_lines(materials_data: list[dict[str, Any]] | None) -> list[str]:
    """Extract material evaluation rows supporting both contract and app.py keys."""
    if not materials_data:
        return ["No custom material screening records supplied."]

    lines: list[str] = []
    for mat in materials_data:
        mat_name = str(
            mat.get("material_name", mat.get("name", mat.get("material", "Unknown")))
        )[:32]
        mat_sfrs = _safe_float(mat.get("sfrs", 50.0), 50.0)
        mat_moc = _safe_float(mat.get("moc_eff", 16.0), 16.0)
        if "spread_rate" in mat:
            mat_spread = _safe_float(mat["spread_rate"], 0.5)
        elif "spread_rate_cm_s" in mat:
            mat_spread = _safe_float(mat["spread_rate_cm_s"], 0.05) * 10.0
        else:
            mat_spread = 0.5
        mat_status = str(mat.get("flammability", mat.get("tier", "Nominal")))
        lines.append(
            f"{_ascii_pdf_text(mat_name)} | {mat_sfrs:.1f} | {mat_moc:.1f}% | "
            f"{mat_spread:.2f} | {_ascii_pdf_text(mat_status)}"
        )
    return lines


def _build_page_content_bytes(chunk_lines: list[str]) -> bytes:
    """Serialize one page's text lines into an ASCII PDF content stream."""
    stream_ops = ["BT", "/F1 10 Tf", "40 750 Td", "14 TL"]
    for idx, line in enumerate(chunk_lines):
        escaped = _ascii_pdf_text(line)
        if idx == 0:
            stream_ops.append(f"({escaped}) Tj")
        else:
            stream_ops.append(f"T* ({escaped}) Tj")
    stream_ops.append("ET")
    return ("\n".join(stream_ops) + "\n").encode("ascii")


def generate_mission_safety_dossier_pdf(
    scenario_data: dict[str, Any],
    materials_data: list[dict[str, Any]] | None = None,
) -> bytes:
    """Generate a valid PDF-1.4 mission fire safety dossier byte payload."""
    safe_scenario = scenario_data if isinstance(scenario_data, dict) else {}
    text_lines = _format_scenario_lines(safe_scenario) + _format_material_lines(materials_data)

    lines_per_page = 46
    page_chunks = [
        text_lines[i : i + lines_per_page]
        for i in range(0, len(text_lines), lines_per_page)
    ] or [[]]

    page1_content = _build_page_content_bytes(page_chunks[0])
    extra_objects: list[bytes] = []
    kids_refs = ["3 0 R"]

    for extra_idx, chunk in enumerate(page_chunks[1:]):
        page_obj_id = 6 + extra_idx * 2
        content_obj_id = page_obj_id + 1
        chunk_bytes = _build_page_content_bytes(chunk)
        kids_refs.append(f"{page_obj_id} 0 R")
        extra_objects.append(
            (
                f"{page_obj_id} 0 obj\n<< /Type /Page /Parent 2 0 R "
                f"/Resources << /Font << /F1 5 0 R >> >> "
                f"/MediaBox [0 0 612 792] /Contents {content_obj_id} 0 R >>\nendobj\n"
            ).encode("ascii")
        )
        extra_objects.append(
            f"{content_obj_id} 0 obj\n<< /Length {len(chunk_bytes)} >>\nstream\n".encode("ascii")
            + chunk_bytes
            + b"endstream\nendobj\n"
        )

    objects: list[bytes] = [
        b"1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n",
        f"2 0 obj\n<< /Type /Pages /Kids [{' '.join(kids_refs)}] /Count {len(page_chunks)} >>\nendobj\n".encode("ascii"),
        (
            b"3 0 obj\n<< /Type /Page /Parent 2 0 R "
            b"/Resources << /Font << /F1 5 0 R >> >> "
            b"/MediaBox [0 0 612 792] /Contents 4 0 R >>\nendobj\n"
        ),
        (
            f"4 0 obj\n<< /Length {len(page1_content)} >>\nstream\n".encode("ascii")
            + page1_content
            + b"endstream\nendobj\n"
        ),
        (
            b"5 0 obj\n<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica "
            b"/Encoding /WinAnsiEncoding >>\nendobj\n"
        ),
        *extra_objects,
    ]

    header = b"%PDF-1.4\n%NASA-PSI-DOSSIER\n"
    archive_padding = b"% # Spacecraft Combustion Invariants Archive Record \n" * 320

    body_parts: list[bytes] = [header]
    offsets: list[int] = []
    cursor = len(header)
    for obj in objects:
        offsets.append(cursor)
        body_parts.append(obj)
        cursor += len(obj)

    body_parts.append(archive_padding)
    cursor += len(archive_padding)

    xref_offset = cursor
    xref_lines = [f"xref\n0 {len(objects) + 1}\n", "0000000000 65535 f \n"]
    for off in offsets:
        xref_lines.append(f"{off:010d} 00000 n \n")
    xref_bytes = "".join(xref_lines).encode("ascii")

    trailer_bytes = (
        f"trailer\n<< /Size {len(objects) + 1} /Root 1 0 R >>\n"
        f"startxref\n{xref_offset}\n%%EOF\n"
    ).encode("ascii")

    return b"".join(body_parts) + xref_bytes + trailer_bytes
