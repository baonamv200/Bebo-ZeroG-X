//! Domain Keyword Reranker with 17 Aerospace Combustion Terminology Groups
//! Matching app.py:1879-1976.

use super::corpus::PsiDocument;
use super::tfidf::{normalize_vn_text, TfidfIndex};
use super::SearchResult;

/// 17 domain synonym categories matching `app.py:1879-1897`.
pub const DOMAIN_KEYWORD_GROUPS: &[(&str, &[&str])] = &[
    (
        "pmma",
        &["pmma", "acrylic", "polymethyl", "nhua pmma", "lucite", "plexiglas"],
    ),
    (
        "airflow",
        &[
            "airflow", "ventilation", "flow", "velocity", "gio", "thong gio",
            "van toc", "luong gio", "gio thap", "thong gio thap", "low flow", "paradox",
        ],
    ),
    (
        "microgravity",
        &[
            "microgravity", "0g", "zero gravity", "zero-g", "vi trong luc",
            "khong trong luc", "trong luc", "freefall",
        ],
    ),
    (
        "cool flame",
        &[
            "cool flame", "cool flames", "droplet", "flex", "ngon lua lanh",
            "lua lanh", "lanh", "chay lanh", "heptane", "second stage",
        ],
    ),
    (
        "water",
        &[
            "water", "mist", "extinguisher", "suppression", "jet", "nuoc",
            "suong nuoc", "dap lua", "chua chay", "tia nuoc", "dap hoa hoan",
            "nghiem cam", "co2", "n2",
        ],
    ),
    (
        "nomex",
        &["nomex", "fabric", "cloth", "vai", "aramid", "chong chay", "ht90", "spacesuit"],
    ),
    (
        "saffire",
        &[
            "saffire", "cygnus", "large-scale", "kho lon", "quy mo lon",
            "saffire-v", "saffire-vi", "hypobaric",
        ],
    ),
    (
        "moon",
        &[
            "moon", "lunar", "0.16g", "hemispherical", "mat trang", "ban cau",
            "0.16", "vom ban cau", "flaring",
        ],
    ),
    (
        "mars",
        &[
            "mars", "0.38g", "partial gravity", "sao hoa", "trong luc mot phan",
            "trong luc ban phan", "0.38",
        ],
    ),
    (
        "teflon",
        &[
            "teflon", "ptfe", "hf", "wire", "day dien", "boc day", "fluorinated",
            "hydrofluoric",
        ],
    ),
    (
        "silicone",
        &[
            "silicone", "rtv", "gasket", "ash", "gioang", "tro", "silica",
            "depressurization",
        ],
    ),
    (
        "same_daft",
        &[
            "same", "same-r", "daft", "daft-2", "smoke detection", "dust",
            "bao khoi", "do bui", "cam bien khoi",
        ],
    ),
    (
        "acme_sub",
        &[
            "acme", "bre", "cfi-g", "e-field", "slice", "spice", "85%",
            "inside-out", "dien truong", "luci", "fm2",
        ],
    ),
    (
        "earth_spinoff",
        &[
            "earth", "terrestrial", "firefighter", "spin-off", "trai dat",
            "linh cuu hoa", "ung dung",
        ],
    ),
    (
        "kapton",
        &[
            "kapton", "polyimide", "mli", "insulation", "tam cach nhiet",
            "mang cach nhiet",
        ],
    ),
    (
        "ultem",
        &["ultem", "pei", "polyetherimide", "cau truc", "structural polymer"],
    ),
    (
        "eclss",
        &[
            "eclss", "decontamination", "scrubbing", "loc khi", "khu nhiem",
            "than hoat tinh", "toxic offgassing",
        ],
    ),
];

/// Hybrid reranker adjusting base TF-IDF cosine scores with domain-specific keyword bonuses.
pub fn rerank_and_filter(index: &TfidfIndex, query: &str, top_k: usize) -> Vec<SearchResult> {
    let clean_query = query.trim();
    if clean_query.is_empty() {
        return Vec::new();
    }

    let q_norm = normalize_vn_text(clean_query);
    let base_scores = index.compute_cosine_scores(&q_norm);

    // Identify active synonym groups
    let mut active_groups: Vec<Vec<String>> = Vec::new();
    for (_grp_name, syns) in DOMAIN_KEYWORD_GROUPS {
        let norm_syns: Vec<String> = syns.iter().map(|s| normalize_vn_text(s)).collect();
        if norm_syns.iter().any(|s| q_norm.contains(s.as_str())) {
            active_groups.push(norm_syns);
        }
    }

    let mut adjusted_scores: Vec<SearchResult> = Vec::with_capacity(index.docs.len());

    for (i, &base_score) in base_scores.iter().enumerate() {
        let doc: &PsiDocument = &index.docs[i];
        let doc_all_text = &index.doc_norm_texts[i];
        let title_norm = normalize_vn_text(doc.title);
        let tags_norm = normalize_vn_text(&doc.tags.join(" "));

        let mut match_count: usize = 0;
        let mut title_tag_hit: f32 = 0.0;

        for syns in &active_groups {
            for s in syns {
                if s.len() > 2 {
                    match_count += doc_all_text.matches(s.as_str()).count();
                }
            }
            if syns.iter().any(|s| title_norm.contains(s.as_str()) || tags_norm.contains(s.as_str())) {
                title_tag_hit += 0.28;
            }
        }

        let freq_bonus = (match_count as f32 * 0.06).min(0.40);
        let total_score = base_score + title_tag_hit + freq_bonus;
        let final_score = total_score.min(0.99);

        adjusted_scores.push(SearchResult {
            score: final_score,
            document: doc.clone(),
        });
    }

    // Sort descending by score
    adjusted_scores.sort_by(|a, b| b.score.partial_cmp(&a.score).unwrap_or(std::cmp::Ordering::Equal));

    // Threshold cutoff < 0.05
    if adjusted_scores.is_empty() || adjusted_scores[0].score < 0.05 {
        return Vec::new();
    }

    adjusted_scores.into_iter().take(top_k).collect()
}
