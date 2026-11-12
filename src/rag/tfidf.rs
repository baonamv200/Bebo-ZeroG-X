//! Pure Rust TF-IDF Vectorizer and Cosine Similarity Search Engine
//! Matching app.py:1913-1940 and 43-50.

use std::collections::{HashMap, HashSet};
use unicode_normalization::char::canonical_combining_class;
use unicode_normalization::UnicodeNormalization;
use regex::Regex;

use super::corpus::{PsiDocument, NASA_FLIGHT_CORPUS};
use super::SearchResult;

/// English and Vietnamese normalization: replaces đ/Đ, applies Unicode NFKD,
/// strips combining diacritical marks, and lowercases.
/// Exactly matches `normalize_vn_text` from `app.py:43-50`.
pub fn normalize_vn_text(text: &str) -> String {
    if text.is_empty() {
        return String::new();
    }
    let replaced = text.replace('đ', "d").replace('Đ', "D");
    let nfkd: String = replaced.nfkd().collect();
    nfkd.chars()
        .filter(|&c| canonical_combining_class(c) == 0)
        .collect::<String>()
        .to_lowercase()
}

/// Tokenizer regex matching `\b[a-z0-9_-]{2,}\b`.
pub fn tokenize(text: &str) -> Vec<String> {
    lazy_static_regex().find_iter(text)
        .map(|m| m.as_str().to_string())
        .collect()
}

fn lazy_static_regex() -> &'static Regex {
    use std::sync::OnceLock;
    static RE: OnceLock<Regex> = OnceLock::new();
    RE.get_or_init(|| Regex::new(r"\b[a-z0-9_-]{2,}\b").expect("Valid token regex"))
}

/// Standard 16 stopwords matching `app.py:1914`.
pub fn get_stopwords() -> HashSet<&'static str> {
    [
        "the", "a", "an", "in", "on", "at", "to", "for",
        "of", "and", "or", "is", "are", "with", "by", "that",
        "this", "it",
    ]
    .into_iter()
    .collect()
}

/// Pure Rust in-memory TF-IDF index over the 14 NASA flight research documents.
pub struct TfidfIndex {
    pub docs: &'static [PsiDocument],
    pub vocab: Vec<String>,
    pub vocab_idx: HashMap<String, usize>,
    pub idf: Vec<f32>,
    pub doc_vectors: Vec<Vec<f32>>,
    pub doc_norm_texts: Vec<String>,
}

impl Default for TfidfIndex {
    fn default() -> Self {
        Self::new()
    }
}

impl TfidfIndex {
    pub fn new() -> Self {
        let docs = NASA_FLIGHT_CORPUS;
        let stopwords = get_stopwords();
        let token_re = lazy_static_regex();

        // 1. Build document text representations
        let mut doc_tokens_list: Vec<Vec<String>> = Vec::with_capacity(docs.len());
        let mut vocab_seen: HashSet<String> = HashSet::new();
        let mut vocab: Vec<String> = Vec::with_capacity(750);

        for doc in docs {
            let full_text = format!("{} {} {} {}", doc.title, doc.section, doc.tags.join(" "), doc.text);
            let lower_text = full_text.to_lowercase();
            let tokens: Vec<String> = token_re
                .find_iter(&lower_text)
                .map(|m| m.as_str().to_string())
                .filter(|w| !stopwords.contains(w.as_str()))
                .collect();

            for tok in &tokens {
                if !vocab_seen.contains(tok) {
                    vocab_seen.insert(tok.clone());
                    vocab.push(tok.clone());
                }
            }
            doc_tokens_list.push(tokens);
        }

        let mut vocab_idx: HashMap<String, usize> = HashMap::with_capacity(vocab.len());
        for (i, w) in vocab.iter().enumerate() {
            vocab_idx.insert(w.clone(), i);
        }

        // 2. Compute IDF array: ln((14.0 + 1.0) / (df + 1.0)) + 1.0
        let n = docs.len() as f32;
        let mut idf = vec![0.0f32; vocab.len()];
        for (w, &idx) in &vocab_idx {
            let df = doc_tokens_list
                .iter()
                .filter(|tokens| tokens.contains(w))
                .count() as f32;
            idf[idx] = ((n + 1.0) / (df + 1.0)).ln() + 1.0;
        }

        // 3. Compute L2-normalized document vectors
        let mut doc_vectors: Vec<Vec<f32>> = Vec::with_capacity(docs.len());
        for tokens in &doc_tokens_list {
            let mut vec = vec![0.0f32; vocab.len()];
            for tok in tokens {
                if let Some(&idx) = vocab_idx.get(tok) {
                    vec[idx] += 1.0;
                }
            }
            // Multiply by IDF
            for i in 0..vec.len() {
                vec[i] *= idf[i];
            }
            // L2 normalize
            let sum_sq: f32 = vec.iter().map(|v| v * v).sum();
            let norm = sum_sq.sqrt();
            if norm > 0.0 {
                for v in &mut vec {
                    *v /= norm;
                }
            }
            doc_vectors.push(vec);
        }

        // 4. Precompute normalized document texts matching `app.py:1902`
        let doc_norm_texts = docs
            .iter()
            .map(|d| normalize_vn_text(&format!("{} {} {}", d.title, d.text, d.tags.join(" "))))
            .collect();

        Self {
            docs,
            vocab,
            vocab_idx,
            idf,
            doc_vectors,
            doc_norm_texts,
        }
    }

    /// Compute raw cosine similarity scores between query and all documents.
    pub fn compute_cosine_scores(&self, query_norm: &str) -> Vec<f32> {
        let tokens = tokenize(query_norm);
        let mut q_vec = vec![0.0f32; self.vocab.len()];
        for t in &tokens {
            if let Some(&idx) = self.vocab_idx.get(t) {
                q_vec[idx] += 1.0;
            }
        }
        for i in 0..q_vec.len() {
            q_vec[i] *= self.idf[i];
        }

        let sum_sq: f32 = q_vec.iter().map(|v| v * v).sum();
        let norm = sum_sq.sqrt();
        if norm <= 0.0 {
            return vec![0.0f32; self.docs.len()];
        }
        for v in &mut q_vec {
            *v /= norm;
        }

        self.doc_vectors
            .iter()
            .map(|d_vec| {
                d_vec
                    .iter()
                    .zip(&q_vec)
                    .map(|(a, b)| a * b)
                    .sum()
            })
            .collect()
    }

    /// Search and return top-k ranked documents using the hybrid domain reranker.
    pub fn search(&self, query: &str, top_k: usize) -> Vec<SearchResult> {
        super::reranker::rerank_and_filter(self, query, top_k)
    }
}
