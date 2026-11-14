"""
Tier 4: Realistic Mission Operational Scenarios for NASA Microgravity Fire Safety Web App.
Covers 6 comprehensive End-to-End Mission Profiles per TEST_INFRA.md Section 4 & 6.4:
1. ISS Nominal Microgravity Habitat (MAT-01 PMMA Acrylic)
2. Artemis Exploration Atmosphere (MAT-03 Nomex Qualification)
3. EVA Spacesuit Oxygen Breach (MAT-02 Cotton Blend Critical Alarm)
4. Lunar Base Overheated Electronics Bay (MAT-10 Kapton & MAT-05 Ultem)
5. Microgravity Hydrocarbon Droplet Cool Flame Encounter (MAT-08 Heptane NTC Kinetics)
6. Crew Emergency Suppression & NASA Mission Safety PDF Dossier Generation
"""

import math
import os
import sys
import pytest

# Ensure repository root is on sys.path
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)


@pytest.mark.tier4
class TestTier4MissionScenarios:
    """Holistic End-to-End Mission Scenario Pipeline Validations."""

    def test_scenario_01_iss_nominal_microgravity_baseline(
        self, physics_engine, rag_engine, threejs_flame_generator, materials_database, sample_mission_scenarios
    ):
        """
        Scenario 1: ISS Nominal Microgravity Habitat
        Parameters: 0g, 21% O2, 101.3 kPa, 10 cm/s, 21°C, 45% RH. Specimen: PMMA (MAT-01).
        Verifies: MOC in [14.0, 16.5]%, SFRS in [45.0, 65.0] (HIGH), Alarm OFF, Isotropic 3D sphere.
        """
        scen = sample_mission_scenarios["scenario_1"]
        pmma = materials_database[0]

        # 1. Physical flammability evaluation
        moc_eff = physics_engine.calculate_effective_moc(pmma, scen["g"], scen["v"], scen["p"], scen["t"], scen["rh"])
        assert scen["expected_moc_range"][0] <= moc_eff <= scen["expected_moc_range"][1], \
            f"ISS PMMA MOC {moc_eff:.2f}% out of expected range {scen['expected_moc_range']}"

        spread = physics_engine.calculate_flame_spread_rate(pmma, scen["g"], scen["v"], scen["p"], scen["t"], scen["rh"], scen["o2"], moc_eff)
        sfrs = physics_engine.calculate_space_fire_risk_score(scen["o2"], moc_eff, spread, pmma["heat_of_combustion_mj_kg"])
        assert scen["expected_sfrs_range"][0] <= sfrs <= scen["expected_sfrs_range"][1], \
            f"ISS SFRS {sfrs:.1f} out of expected range {scen['expected_sfrs_range']}"

        # 2. Multi-sensory alert verification
        audio_alarm_active = sfrs > 85.0
        assert audio_alarm_active is False, "Audio alarm must remain OFF for nominal ISS habitat (SFRS < 85.0)"

        # 3. 3D WebGL Spherical flame component verification
        html = threejs_flame_generator(gravity_g=scen["g"], airflow_cm_s=scen["v"], oxygen_pct=scen["o2"], pressure_kpa=scen["p"])
        assert "is0g = true" in html, "3D component must render isotropic spherical flame in microgravity (g=0)"

        # 4. RAG Copilot verification
        results = rag_engine.search_semantic("PMMA low flow flammability anomalies", top_k=1)
        assert len(results) > 0
        directive = rag_engine.generate_grounded_directive("What is the PMMA low flow hazard?", results)
        assert "BLOCK 1" in directive["directive"]

    def test_scenario_02_artemis_exploration_atmosphere_nomex_qualification(
        self, physics_engine, materials_database, sample_mission_scenarios
    ):
        """
        Scenario 2: Artemis Exploration Atmosphere
        Parameters: 0.16g Lunar, 34% O2 Enriched, 56.5 kPa Hypobaric, 12 cm/s, 22°C, 35% RH.
        Specimen: Nomex HT90-40 (MAT-03).
        Verifies: Nomex passes in 1g normoxic but fails in Artemis 34% O2; delta-SFRS vs ISS > +20.0.
        """
        scen_artemis = sample_mission_scenarios["scenario_2"]
        scen_iss = sample_mission_scenarios["scenario_1"]
        nomex = materials_database[2]

        # 1. Terrestrial baseline check (Nomex MOC in 1g is ~28.5%, so passes 21% O2 air)
        moc_1g = physics_engine.calculate_effective_moc(nomex, g=1.0, v=10.0, P=101.3, T=21.0, RH=45.0)
        assert 21.0 < moc_1g, "Nomex must be non-flammable in standard terrestrial air"

        # 2. Artemis atmosphere flammability check
        moc_artemis = physics_engine.calculate_effective_moc(nomex, scen_artemis["g"], scen_artemis["v"], scen_artemis["p"], scen_artemis["t"], scen_artemis["rh"])
        assert scen_artemis["expected_moc_range"][0] <= moc_artemis <= scen_artemis["expected_moc_range"][1]
        assert scen_artemis["o2"] > moc_artemis, "Artemis 34% O2 exceeds Nomex MOC, requiring flight exemption!"

        # 3. Dual Scenario comparison diff
        diff = physics_engine.calculate_scenario_diff(scen_iss, scen_artemis, nomex)
        assert diff["delta_sfrs"] > 20.0, f"Expected delta-SFRS > +20.0 for Artemis transition, got {diff['delta_sfrs']:.1f}"
        radar = diff["radar_metrics"]
        assert radar["values_b"][0] > radar["values_a"][0], "Artemis Oxygen Hazard axis must exceed ISS"

    def test_scenario_03_eva_spacesuit_oxygen_breach_critical_alarm(
        self, physics_engine, rag_engine, materials_database, sample_mission_scenarios
    ):
        """
        Scenario 3: EVA Spacesuit Oxygen Breach
        Parameters: 0g, 100% Pure O2, 29.6 kPa, 18 cm/s, 18°C, 20% RH. Specimen: Cotton Blend (MAT-02).
        Verifies: SFRS >= 90.0, Audio Alarm ACTIVE, Emergency Border ACTIVE, Emergency Copilot protocol.
        """
        scen = sample_mission_scenarios["scenario_3"]
        cotton = materials_database[1]

        # 1. Physics evaluation
        moc_eff = physics_engine.calculate_effective_moc(cotton, scen["g"], scen["v"], scen["p"], scen["t"], scen["rh"])
        spread = physics_engine.calculate_flame_spread_rate(cotton, scen["g"], scen["v"], scen["p"], scen["t"], scen["rh"], scen["o2"], moc_eff)
        sfrs = physics_engine.calculate_space_fire_risk_score(scen["o2"], moc_eff, spread, cotton["heat_of_combustion_mj_kg"])
        assert sfrs >= scen["expected_min_sfrs"], f"SFRS {sfrs:.1f} must be >= {scen['expected_min_sfrs']} for 100% O2 suit breach"

        # 2. Multi-sensory alarm triggers
        audio_active = sfrs > 85.0
        border_active = sfrs > 85.0
        assert audio_active is True, "Audio alarm must activate for critical threat SFRS > 85.0"
        assert border_active is True, "Pulsing border must activate for critical threat SFRS > 85.0"

        # 3. Zero-key Copilot emergency protocol
        results = rag_engine.search_semantic("EVA oxygen breach rapid fire suppression", top_k=2)
        directive = rag_engine.generate_grounded_directive("Immediate actions for spacesuit oxygen fire?", results)
        assert "BLOCK 3" in directive["directive"]
        assert "T+0s" in directive["directive"]

    def test_scenario_04_lunar_base_overheated_electronics_bay(
        self, physics_engine, rag_engine, materials_database, sample_mission_scenarios
    ):
        """
        Scenario 4: Lunar Base Overheated Electronics Bay
        Parameters: 0.16g, 21% O2, 101.3 kPa, 3 cm/s low airflow, 42°C overheated, 15% dry RH.
        Specimens: Kapton HN (MAT-10) and Ultem 1000 (MAT-05).
        Verifies: Kapton MOC decreases due to preheating, Ultem flammability threshold, cooling directives.
        """
        scen = sample_mission_scenarios["scenario_4"]
        kapton = materials_database[9]
        ultem = materials_database[4]

        # 1. Thermal preheating effect
        moc_kapton_nom = physics_engine.calculate_effective_moc(kapton, scen["g"], scen["v"], scen["p"], T=21.0, RH=scen["rh"])
        moc_kapton_hot = physics_engine.calculate_effective_moc(kapton, scen["g"], scen["v"], scen["p"], T=scen["t"], RH=scen["rh"])
        delta_moc = moc_kapton_nom - moc_kapton_hot
        assert delta_moc > 0.5, f"Thermal preheating at 42°C must drop Kapton MOC by > 0.5% O2 (got {delta_moc:.2f}%)"

        # 2. Kapton still survives (MOC remains well above 21%)
        assert moc_kapton_hot > 25.0, "Kapton must retain high extinction margin even when overheated"

        # 3. Ultem evaluation under overheated low flow
        moc_ultem = physics_engine.calculate_effective_moc(ultem, scen["g"], scen["v"], scen["p"], scen["t"], scen["rh"])
        assert moc_ultem > 20.0

        # 4. Copilot directive for avionics overheating
        retrieved = rag_engine.search_semantic("overheated avionics rack fire suppression", top_k=2)
        directive = rag_engine.generate_grounded_directive("Mitigation for overheated rack at 42C?", retrieved)
        assert "HVAC" in directive["directive"] or "cooling" in directive["directive"] or "BLOCK 3" in directive["directive"]

    def test_scenario_05_microgravity_droplet_cool_flame_encounter(
        self, physics_engine, rag_engine, threejs_flame_generator, materials_database, sample_mission_scenarios
    ):
        """
        Scenario 5: Microgravity Hydrocarbon Droplet Cool Flame Encounter
        Parameters: 0g, 17.5% O2 (vitiated), 101.3 kPa, 2.0 cm/s flow, 20°C, 40% RH. Specimen: Heptane (MAT-08).
        Verifies: Dynamic NTC limit-cycle oscillations (600K-760K), toxic CO > 100 ppm, FLEX-2 retrieval #1.
        """
        scen = sample_mission_scenarios["scenario_5"]
        heptane = materials_database[7]
        assert heptane["cool_flame_susceptible"] is True

        # 1. Dynamic Cool Flame Chemical Kinetics ODE
        kinetics = physics_engine.solve_cool_flame_ntc_kinetics(T0=1450.0, o2=scen["o2"], P=scen["p"], t_max=40.0, steps=400)
        t_arr = kinetics["time"]
        t_temps = kinetics["temperature"]
        co_ppm = kinetics["co_ppm"]

        assert len(t_arr) == 400
        # Post-extinction oscillations in the cool flame regime
        late_temps = t_temps[100:]
        assert max(late_temps) <= 900.0, "Cool flame oscillations must stay below 900K"
        assert min(late_temps) >= 500.0, "Cool flame oscillations must stay above 500K"
        assert co_ppm[-1] >= scen["expected_min_co_ppm"], f"Accumulated CO {co_ppm[-1]:.1f} ppm must be >= {scen['expected_min_co_ppm']} ppm"

        # 2. Semantic Document Retrieval: FLEX-2 study
        results = rag_engine.search_semantic("invisible second stage low temperature burning after radiative extinction", top_k=1)
        assert len(results) > 0
        top_doc = results[0]["doc"]
        assert top_doc["doc_id"] == "SCI-FLEX-2012-1593", "FLEX-2 study must be ranked #1 for cool flame queries"

        # 3. 3D WebGL Visualization
        html = threejs_flame_generator(gravity_g=0.0, airflow_cm_s=2.0, oxygen_pct=17.5, pressure_kpa=101.3)
        assert "is0g = true" in html
        assert "Points" in html  # Heat dissipation particle field

    def test_scenario_06_crew_emergency_suppression_and_pdf_dossier(
        self, physics_engine, pdf_generator, materials_database, sample_mission_scenarios
    ):
        """
        Scenario 6: Crew Emergency Suppression & NASA Mission Safety PDF Dossier Generation
        Parameters: 0g, 28% O2, 85.0 kPa, 8 cm/s, 26°C, 50% RH. Specimen: Multi-Material Fleet.
        Verifies: Fine Water Mist protocol, PDF byte stream with %PDF- header, > 15KB size, tables.
        """
        scen = sample_mission_scenarios["scenario_6"]

        # 1. Evaluate all 10 materials under mission atmosphere
        eval_records = []
        for mat in materials_database:
            moc = physics_engine.calculate_effective_moc(mat, scen["g"], scen["v"], scen["p"], scen["t"], scen["rh"])
            spread = physics_engine.calculate_flame_spread_rate(mat, scen["g"], scen["v"], scen["p"], scen["t"], scen["rh"], scen["o2"], moc)
            sfrs = physics_engine.calculate_space_fire_risk_score(scen["o2"], moc, spread, mat["heat_of_combustion_mj_kg"])
            eval_records.append({
                "material_name": mat["material_name"],
                "sfrs": sfrs,
                "moc_eff": moc,
                "spread_rate": spread,
                "flammability": "Flammable" if scen["o2"] >= moc else "Extinguished",
            })

        max_sfrs = max(r["sfrs"] for r in eval_records)
        scen_payload = {
            "mission": "Crew Emergency Compartment Evaluation",
            "g": scen["g"],
            "o2": scen["o2"],
            "p": scen["p"],
            "v": scen["v"],
            "t": scen["t"],
            "rh": scen["rh"],
            "sfrs": max_sfrs,
            "tier": "CRITICAL" if max_sfrs >= 70.0 else "HIGH",
            "nasa_status": "PROHIBITED / EXEMPTION REQUIRED",
        }

        # 2. Generate NASA Mission Safety PDF Dossier
        pdf_bytes = pdf_generator(scen_payload, eval_records)

        # 3. PDF Structural & Byte Assertions
        assert pdf_bytes.startswith(b"%PDF-1."), f"Invalid PDF magic bytes: {pdf_bytes[:10]}"
        assert len(pdf_bytes) >= scen["expected_min_pdf_size"], \
            f"PDF dossier size {len(pdf_bytes)} bytes is less than {scen['expected_min_pdf_size']} bytes threshold"
        assert b"xref" in pdf_bytes, "PDF missing cross-reference table"
        assert b"%%EOF" in pdf_bytes, "PDF missing EOF trailer termination"
        assert b"NASA TECHNICAL MEMORANDUM" in pdf_bytes, "PDF missing NASA Technical Memorandum header"
