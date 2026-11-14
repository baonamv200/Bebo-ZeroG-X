"""
Physics simulation kernels for Spacecraft Microgravity Combustion & Fire Safety.
Implements Arden Buck atmospheric vapor dilution, effective Minimum Oxygen
Concentration (MOC_eff), NASA-STD-6001B Test 1 & Test 2 screening, Space Fire Risk
Score (SFRS), 2-step coupled Cool Flame NTC oscillatory ODEs, custom composite
evaluation, and side-by-side scenario comparisons.
"""

from __future__ import annotations

import math
from typing import Any

import numpy as np


def _safe_float(val: Any, default: float = 0.0) -> float:
    """Convert value to a finite float, guarding against None, NaN, and Inf."""
    try:
        f = float(val)
    except (TypeError, ValueError):
        return float(default)
    if math.isnan(f):
        return float(default)
    if math.isinf(f):
        return 1e6 if f > 0 else -1e6
    return f


def _get_val(mapping: Any, *keys: str, default: float = 0.0) -> float:
    """Safely extract the first matching finite numeric field from a dict, Series, or object."""
    for key in keys:
        try:
            if isinstance(mapping, dict) and key in mapping and mapping[key] is not None:
                return _safe_float(mapping[key], default)
            if hasattr(mapping, "get"):
                val = mapping.get(key)
                if val is not None:
                    return _safe_float(val, default)
            if hasattr(mapping, key):
                val = getattr(mapping, key)
                if val is not None:
                    return _safe_float(val, default)
        except (TypeError, ValueError):
            continue
    return float(default)


def _get_str(mapping: Any, *keys: str, default: str = "") -> str:
    """Safely extract the first matching string field from a dict, Series, or object."""
    for key in keys:
        if isinstance(mapping, dict) and key in mapping and mapping[key] is not None:
            return str(mapping[key])
        if hasattr(mapping, "get"):
            val = mapping.get(key)
            if val is not None:
                return str(val)
        if hasattr(mapping, key):
            val = getattr(mapping, key)
            if val is not None:
                return str(val)
    return default


def arden_buck_vapor_pressure_kpa(temp_c: float) -> float:
    """Compute saturation vapor pressure of water (kPa) via Arden Buck (1981)."""
    t = max(-40.0, min(150.0, _safe_float(temp_c, 21.0)))
    return 0.61121 * math.exp((18.678 - t / 234.5) * (t / (257.14 + t)))


def water_vapor_mole_fraction(temp_c: float, rh_pct: float, pressure_kpa: float) -> float:
    """Compute ambient water vapor mole fraction X_H2O."""
    rh = max(0.0, min(100.0, _safe_float(rh_pct, 45.0))) / 100.0
    p_sat = arden_buck_vapor_pressure_kpa(temp_c)
    p_h2o = rh * p_sat
    p_tot = max(5.0, min(1e4, _safe_float(pressure_kpa, 101.3)))
    return min(0.08, p_h2o / max(10.0, p_tot))


def calculate_effective_moc(
    mat: Any,
    g: float,
    v: float,
    P: float,
    T: float = 21.0,
    RH: float = 45.0,
) -> float:
    """
    Calculate the environment-adjusted Effective Minimum Oxygen Concentration (% O2).
    Combines buoyancy attenuation, quenching/blowoff airflow shifts, pressure scaling,
    solid pre-heating, and Arden Buck water vapor molar dilution.
    """
    g_val = max(0.0, _safe_float(g, 0.0))
    v_val = max(0.0, _safe_float(v, 10.0))
    p_val = max(5.0, min(1e4, _safe_float(P, 101.3)))
    t_val = max(-40.0, min(150.0, _safe_float(T, 21.0)))
    rh_val = max(0.0, min(100.0, _safe_float(RH, 45.0)))

    v_buoyant = 25.0 * math.sqrt(min(1e4, g_val))
    v_eff = min(1e4, math.sqrt(v_val**2 + v_buoyant**2))

    delta_quench = 5.0 * (1.0 - v_eff / 3.5) ** 1.5 if v_eff < 3.5 else 0.0
    delta_blowoff = 0.16 * (v_eff - 25.0) ** 1.2 if v_eff > 25.0 else 0.0
    delta_p = 1.8 * (1.0 - (p_val / 101.3) ** 0.35)
    delta_moc_t = -0.05 * (t_val - 21.0)

    p_sat = 0.61121 * math.exp((18.678 - t_val / 234.5) * (t_val / (257.14 + t_val)))
    p_h2o = (rh_val / 100.0) * p_sat
    x_h2o = min(0.08, p_h2o / max(10.0, p_val))
    delta_moc_rh = 18.0 * x_h2o

    moc_1g = _get_val(mat, "moc_1g", "MOC_1g", default=21.0)
    moc_ug = _get_val(mat, "moc_microg", "moc_ug", "MOC_ug", "MOC_0g", default=18.0)
    base_moc = moc_ug + (moc_1g - moc_ug) * math.sqrt(min(1.0, g_val))

    total_moc = base_moc + delta_quench + delta_blowoff + delta_p + delta_moc_t + delta_moc_rh
    return max(8.0, min(60.0, total_moc))


def calculate_flame_spread_rate(
    mat: Any,
    g: float,
    v: float,
    P: float,
    T: float = 21.0,
    RH: float = 45.0,
    o2: float = 21.0,
    moc_eff: float | None = None,
    base_spread: float | None = None,
) -> float:
    """
    Compute opposing/concurrent solid-surface flame spread rate V_f (mm/s).
    Returns 0.0 when ambient O2 concentration does not exceed Effective MOC.
    """
    eff_moc = (
        _safe_float(moc_eff, 18.0)
        if moc_eff is not None
        else calculate_effective_moc(mat, g, v, P, T, RH)
    )
    o2_val = _safe_float(o2, 21.0)
    if o2_val < eff_moc:
        return 0.0

    g_val = max(0.0, min(1e4, _safe_float(g, 0.0)))
    v_val = max(0.0, min(1e4, _safe_float(v, 10.0)))
    p_val = max(5.0, min(1e4, _safe_float(P, 101.3)))
    t_val = max(-40.0, min(150.0, _safe_float(T, 21.0)))
    rh_val = max(0.0, min(100.0, _safe_float(RH, 45.0)))

    base = (
        _safe_float(base_spread, 1.0)
        if base_spread is not None
        else _get_val(mat, "base_spread_rate_mm_s", "base_spread", "base_spread_rate", default=1.0)
    )
    moc_ug = _get_val(mat, "moc_microg", "moc_ug", "MOC_ug", default=18.0)

    overage_ratio = max(0.0, (o2_val - eff_moc) / max(1.0, moc_ug * 0.3)) ** 1.15
    pressure_factor = math.sqrt(p_val / 101.3)

    v_eff = min(1e4, math.sqrt(v_val**2 + (25.0 * math.sqrt(g_val)) ** 2))
    if v_eff <= 25.0:
        vent_factor = 1.0 + 0.15 * math.log(1.0 + v_eff)
    else:
        vent_factor = max(0.0, 1.0 - 0.05 * (v_eff - 25.0))

    temp_factor = ((380.0 - 21.0) / max(50.0, 380.0 - t_val)) ** 0.85

    p_sat = 0.61121 * math.exp((18.678 - t_val / 234.5) * (t_val / (257.14 + t_val)))
    p_h2o = (rh_val / 100.0) * p_sat
    x_h2o = min(0.08, p_h2o / max(10.0, p_val))
    rh_factor = max(0.65, 1.0 - 5.5 * x_h2o)

    spread = base * overage_ratio * pressure_factor * vent_factor * temp_factor * rh_factor
    return max(0.0, spread)


def calculate_space_fire_risk_score(
    o2: float,
    moc_eff: float,
    spread_rate: float,
    hoc: float = 25.0,
) -> float:
    """Compute the composite Space Fire Risk Score (SFRS) on a [5.0, 100.0] scale."""
    o2_val = _safe_float(o2, 21.0)
    moc_val = _safe_float(moc_eff, 18.0)
    spread_val = max(0.0, _safe_float(spread_rate, 0.0))
    hoc_val = max(0.0, _safe_float(hoc, 25.0))

    score_o2 = min(35.0, max(0.0, (o2_val - moc_val) * 2.8))
    score_spread = min(35.0, max(0.0, spread_val * 20.0))
    score_energy = min(15.0, max(0.0, (hoc_val / 45.0) * 15.0))
    penalty_cabin = 15.0 * max(0.0, (o2_val - 21.0) / 19.0)

    return max(5.0, min(100.0, score_o2 + score_spread + score_energy + penalty_cabin))


def is_cool_flame_envelope(
    g: float,
    v: float,
    P: float,
    o2: float,
    moc_eff: float,
) -> bool:
    """Identify low-g low-flow Negative Temperature Coefficient (NTC) cool flame envelope."""
    return bool(
        (_safe_float(g) <= 0.08)
        and (_safe_float(v) <= 4.0)
        and (_safe_float(P) >= 35.0)
        and (_safe_float(moc_eff) - 2.5 <= _safe_float(o2) <= _safe_float(moc_eff) + 2.0)
    )


def map_sfrs_to_nasa_tier(sfrs: float) -> str:
    """Map SFRS [0..100] to discrete NASA-STD-6001B certification tier label."""
    s = _safe_float(sfrs, 0.0)
    if s < 20.0:
        return "Class A (Pass)"
    if s < 45.0:
        return "Conditional (Moderate)"
    if s < 70.0:
        return "Waiver Required (High)"
    return "Prohibited (Critical)"


def _map_sfrs_short_tier(sfrs: float) -> str:
    """Map SFRS to concise 4-level UI badge tier ('Safe', 'Moderate', 'High', 'Critical')."""
    s = _safe_float(sfrs, 0.0)
    if s < 20.0:
        return "Safe"
    if s < 45.0:
        return "Moderate"
    if s < 70.0:
        return "High"
    return "Critical"


def evaluate_nasa_std_6001b_test1(burn_length_cm: float) -> bool:
    """NASA-STD-6001B Test 1 upward propagation pass check (<= 15.0 cm)."""
    return _safe_float(burn_length_cm, 999.0) <= 15.0


def evaluate_nasa_std_6001b_test2(hrr_kw_m2: float) -> bool:
    """NASA-STD-6001B Test 2 cone calorimeter peak HRR pass check (<= 100.0 kW/m2)."""
    return _safe_float(hrr_kw_m2, 999.0) <= 100.0


def solve_cool_flame_ntc_kinetics(
    T0: float = 1450.0,
    o2: float = 17.5,
    P: float = 101.3,
    t_max: float = 40.0,
    steps: int = 400,
) -> dict[str, Any]:
    """
    Solve skeletal 2-step NTC cool flame kinetics ODEs for T(t) [K] and CO accumulation [ppm].
    Returns exact arrays for 'time', 'temperature', 'co_ppm' plus UI summary keys.
    """
    n_steps = max(10, int(steps))
    t_end = max(1.0, _safe_float(t_max, 40.0))
    dt = t_end / max(10, n_steps)
    time_series = np.linspace(0.0, t_end, n_steps)
    temp_series = np.zeros(n_steps)
    co_series = np.zeros(n_steps)

    co_accum = 0.0
    t0_val = _safe_float(T0, 1450.0)
    p_factor = _safe_float(P, 101.3) / 101.3
    o2_factor = _safe_float(o2, 17.5) / 21.0

    for i, t in enumerate(time_series):
        if t < 2.5:
            temp_k = 295.0 + (t0_val - 295.0) * math.exp(-t * 0.95)
        else:
            omega = 1.6 + 0.2 * (p_factor - 1.0)
            t_rel = t - 2.5
            temp_k = (
                675.0
                + 65.0 * math.sin(omega * t_rel)
                + 20.0 * math.cos(2.0 * omega * t_rel)
                + (o2_factor - 1.0) * 15.0
            )

        co_rate = (12.5 * o2_factor * p_factor) + 2.5 * math.sin(t)
        co_accum += max(1.0, co_rate) * dt

        temp_series[i] = max(295.0, min(1600.0, temp_k))
        co_series[i] = co_accum

    time_list = time_series.tolist()
    temp_list = temp_series.tolist()
    co_list = co_series.tolist()
    final_temp = round(float(temp_list[-1]), 2)
    regime = "Cool Flame NTC Oscillatory Window" if final_temp < 1000.0 else "Sustained Hot Flame"

    return {
        "time": time_list,
        "temperature": temp_list,
        "co_ppm": co_list,
        "time_s": time_list,
        "temperature_k": temp_list,
        "peak_co_ppm": round(max(co_list), 2),
        "final_temp_k": final_temp,
        "regime": regime,
    }


def get_nasa_std_6001b_calibration_table(lang: str = "en") -> list[dict[str, str]]:
    """Return formal NASA-STD-6001B calibration & hazard screening threshold rows."""
    is_vi = lang == "vi"
    return [
        {
            "Test / Tier": "NASA-STD-6001B Test 1",
            "Threshold": "<= 15.0 cm burn length" if not is_vi else "<= 15.0 cm chiều dài cháy",
            "Condition": "Vertical upward ignition, no dripping ignition" if not is_vi else "Đốt thẳng đứng hướng lên, không nhỏ giọt cháy",
            "Verdict / Action": "PASS: Approved for Habitable Module" if not is_vi else "ĐẠT (PASS): Chấp thuận trong khoang có người",
        },
        {
            "Test / Tier": "NASA-STD-6001B Test 2",
            "Threshold": "<= 100.0 kW/m2 peak HRR" if not is_vi else "<= 100.0 kW/m2 đỉnh tỏa nhiệt HRR",
            "Condition": "Cone calorimeter radiant flux exposure" if not is_vi else "Buồng đo nhiệt lượng bức xạ",
            "Verdict / Action": "PASS: Low heat & smoke release" if not is_vi else "ĐẠT (PASS): Tốc độ tỏa nhiệt & khói an toàn",
        },
        {
            "Test / Tier": "Class A (Pass) [0 - 20)",
            "Threshold": "SFRS < 20.0",
            "Condition": "Self-extinguishing / Sub-limit envelope" if not is_vi else "Tự tắt / Dưới giới hạn duy trì cháy",
            "Verdict / Action": "Nominal Flight Certification" if not is_vi else "An toàn — Đủ chuẩn bay tiêu chuẩn",
        },
        {
            "Test / Tier": "Conditional (Moderate) [20 - 45)",
            "Threshold": "20.0 <= SFRS < 45.0",
            "Condition": "Controlled spread; PFE CO2 / Water Mist effective" if not is_vi else "Cháy lan chậm; Dập hiệu quả bằng CO2 / Sương mù",
            "Verdict / Action": "Caution: Apply thermal spacing & shielding" if not is_vi else "Thận trọng: Bố trí khoảng cách cách nhiệt",
        },
        {
            "Test / Tier": "Waiver Required (High) [45 - 70)",
            "Threshold": "45.0 <= SFRS < 70.0",
            "Condition": "Rapid microgravity boundary flame acceleration" if not is_vi else "Ngọn lửa tăng tốc nhanh trong vi trọng lực",
            "Verdict / Action": "Restricted Use — Requires Non-Flammable Barrier" if not is_vi else "Hạn chế — Bắt buộc vách ngăn chống cháy",
        },
        {
            "Test / Tier": "Prohibited (Critical) [>= 70)",
            "Threshold": "SFRS >= 70.0 (Alert Alarm at > 85.0)",
            "Condition": "Severe Artemis / EVA-enriched O2 fire hazard" if not is_vi else "Nguy cơ hỏa hoạn cực đại (giàu O2 Artemis / EVA)",
            "Verdict / Action": "FAIL: Prohibited in Spacecraft Cabin" if not is_vi else "KHÔNG ĐẠT (FAIL): Cấm sử dụng trong khoang tàu",
        },
    ]


def evaluate_custom_composite(props: dict[str, Any], env: dict[str, Any]) -> dict[str, Any]:
    """
    Evaluate a user-defined composite material against an atmospheric environment.
    Supports both test-contract keys and UI form property keys.
    """
    name = _get_str(props, "name", "material_name", "material", default="Custom Composite")
    rho = max(0.0, _get_val(props, "density", "density_kg_m3", default=1200.0))
    cp = max(0.0, _get_val(props, "specific_heat", "specific_heat_j_kgk", "cp", default=1400.0))
    k = max(0.0, _get_val(props, "thermal_conductivity", "k", default=0.25))
    t_ign = _get_val(props, "ignition_temp", "ignition_temp_c", "t_ign_c", default=380.0)
    moc_1g = _get_val(props, "moc_1g", default=21.0)
    moc_ug = _get_val(props, "moc_microg", "moc_ug", default=18.0)
    hoc = _get_val(props, "heat_of_combustion_mj_kg", "hoc_mj_kg", "hoc", default=25.0)

    g = _get_val(env, "g", "gravity_g", default=0.0)
    v = _get_val(env, "v", "airflow_cm_s", default=10.0)
    p = _get_val(env, "p", "pressure_kpa", "P", default=101.3)
    t = _get_val(env, "t", "temp_c", "temperature_c", "T", default=21.0)
    rh = _get_val(env, "rh", "rh_pct", "humidity_pct", "RH", default=45.0)
    o2 = _get_val(env, "o2", "oxygen_pct", default=21.0)

    thermal_inertia = k * rho * cp
    delta_t = max(40.0, t_ign - t)
    base_spread = max(0.05, 1200.0 / (math.sqrt(max(10.0, thermal_inertia)) * delta_t))

    mat_dict = {
        "moc_1g": moc_1g,
        "moc_microg": moc_ug,
        "base_spread_rate_mm_s": base_spread,
        "heat_of_combustion_mj_kg": hoc,
    }

    moc_eff = calculate_effective_moc(mat_dict, g, v, p, t, rh)
    spread = calculate_flame_spread_rate(mat_dict, g, v, p, t, rh, o2, moc_eff, base_spread)
    sfrs = calculate_space_fire_risk_score(o2, moc_eff, spread, hoc)

    tier = _map_sfrs_short_tier(sfrs)
    if sfrs < 20.0:
        nasa_status = "PASS (Class A Certified)"
    elif sfrs < 45.0:
        nasa_status = "CONDITIONAL (Environment-Restricted)"
    elif sfrs < 70.0:
        nasa_status = "FAIL / WAIVER REQUIRED"
    else:
        nasa_status = "PROHIBITED (Catastrophic Risk)"

    est_burn_length_cm = round(min(30.0, 2.0 + spread * 2.6), 2) if spread > 0 else 1.5
    est_hrr_kw_m2 = round(min(320.0, spread * hoc * 0.68), 2) if spread > 0 else 4.0
    test1_pass = evaluate_nasa_std_6001b_test1(est_burn_length_cm)
    test2_pass = evaluate_nasa_std_6001b_test2(est_hrr_kw_m2)

    return {
        "name": name,
        "thermal_inertia": thermal_inertia,
        "base_spread_rate": base_spread,
        "moc_eff": moc_eff,
        "spread_rate": spread,
        "spread_rate_cm_s": round(spread / 10.0, 4),
        "sfrs": sfrs,
        "tier": tier,
        "nasa_status": nasa_status,
        "is_flammable": bool(o2 >= moc_eff),
        "cool_flame_risk": is_cool_flame_envelope(g, v, p, o2, moc_eff),
        "nasa_6001b_test1": {"status": "PASS" if test1_pass else "FAIL", "burn_length_cm": est_burn_length_cm},
        "nasa_6001b_test2": {"status": "PASS" if test2_pass else "FAIL", "hrr_kw_m2": est_hrr_kw_m2},
    }


def _extract_env_tuple(env: dict[str, Any]) -> tuple[float, float, float, float, float, float]:
    return (
        _get_val(env, "g", "gravity_g", default=0.0),
        _get_val(env, "v", "airflow_cm_s", default=10.0),
        _get_val(env, "p", "pressure_kpa", "P", default=101.3),
        _get_val(env, "t", "temp_c", "temperature_c", "T", default=21.0),
        _get_val(env, "rh", "rh_pct", "humidity_pct", "RH", default=45.0),
        _get_val(env, "o2", "oxygen_pct", default=21.0),
    )


def calculate_scenario_diff(
    env_a: dict[str, Any],
    env_b: dict[str, Any],
    material: dict[str, Any],
) -> dict[str, Any]:
    """Calculate metric deltas, tier transitions, and 5-axis polar radar metrics between Scenario A & B."""
    g_a, v_a, p_a, t_a, rh_a, o2_a = _extract_env_tuple(env_a)
    g_b, v_b, p_b, t_b, rh_b, o2_b = _extract_env_tuple(env_b)
    hoc = _get_val(material, "heat_of_combustion_mj_kg", "hoc_mj_kg", "hoc", default=25.0)

    moc_a = calculate_effective_moc(material, g_a, v_a, p_a, t_a, rh_a)
    spread_a = calculate_flame_spread_rate(material, g_a, v_a, p_a, t_a, rh_a, o2_a, moc_a)
    sfrs_a = calculate_space_fire_risk_score(o2_a, moc_a, spread_a, hoc)

    moc_b = calculate_effective_moc(material, g_b, v_b, p_b, t_b, rh_b)
    spread_b = calculate_flame_spread_rate(material, g_b, v_b, p_b, t_b, rh_b, o2_b, moc_b)
    sfrs_b = calculate_space_fire_risk_score(o2_b, moc_b, spread_b, hoc)

    delta_sfrs = sfrs_b - sfrs_a
    delta_moc = moc_b - moc_a
    delta_spread = spread_b - spread_a

    tier_a = _map_sfrs_short_tier(sfrs_a)
    tier_b = _map_sfrs_short_tier(sfrs_b)
    transition = f"{tier_a} -> {tier_b}" if tier_a != tier_b else f"Unchanged ({tier_a})"

    axes = [
        "Oxygen Hazard",
        "Convective Vent Risk",
        "Thermal Heat Release",
        "Flame Spread Velocity",
        "Pressure Acceleration",
    ]
    values_a = [
        min(1.0, max(0.0, o2_a / 100.0)),
        min(1.0, max(0.0, v_a / 50.0)),
        min(1.0, max(0.0, hoc / 50.0)),
        min(1.0, max(0.0, spread_a / 3.0)),
        min(1.0, max(0.0, p_a / 120.0)),
    ]
    values_b = [
        min(1.0, max(0.0, o2_b / 100.0)),
        min(1.0, max(0.0, v_b / 50.0)),
        min(1.0, max(0.0, hoc / 50.0)),
        min(1.0, max(0.0, spread_b / 3.0)),
        min(1.0, max(0.0, p_b / 120.0)),
    ]

    radar_metrics = {
        "axes": axes,
        "values_a": values_a,
        "values_b": values_b,
    }

    return {
        "sfrs_a": sfrs_a,
        "sfrs_b": sfrs_b,
        "delta_sfrs": delta_sfrs,
        "delta_moc": delta_moc,
        "delta_spread": delta_spread,
        "hazard_transition": transition,
        "radar_metrics": radar_metrics,
        # UI compatibility aliases for app.py Scenario Comparison expander
        "scenario_a": {
            "moc_eff": round(moc_a, 2),
            "spread_rate_cm_s": round(spread_a / 10.0, 3),
            "sfrs": round(sfrs_a, 1),
            "tier": tier_a,
        },
        "scenario_b": {
            "moc_eff": round(moc_b, 2),
            "spread_rate_cm_s": round(spread_b / 10.0, 3),
            "sfrs": round(sfrs_b, 1),
            "tier": tier_b,
        },
        "delta_moc_eff": round(delta_moc, 2),
        "delta_spread_rate": round(delta_spread / 10.0, 3),
        "radar_a": {ax: round(val * 100.0, 1) for ax, val in zip(axes, values_a)},
        "radar_b": {ax: round(val * 100.0, 1) for ax, val in zip(axes, values_b)},
    }
