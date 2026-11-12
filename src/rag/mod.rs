//! NASA Flight Research RAG Vector Search & Retrieval Engine
//! Providing sub-microsecond in-memory TF-IDF search, domain reranking,
//! and deterministic NASA Directive answer generation.

pub mod corpus;
pub mod reranker;
pub mod synthesizer;
pub mod tfidf;

pub use corpus::*;
pub use reranker::*;
pub use synthesizer::*;
pub use tfidf::*;

use serde::{Deserialize, Serialize};

/// High-level search result item containing ranking score and document payload.
#[derive(Debug, Clone, Serialize, PartialEq)]
pub struct SearchResult {
    pub score: f32,
    pub document: PsiDocument,
}

/// JSON-friendly serializable ranked document structure matching SCOPE.md.
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq)]
pub struct RankedDocItem {
    pub score: f32,
    pub doc_id: String,
    pub title: String,
    pub report_id: String,
    pub authors: String,
    pub facility: String,
    pub section: String,
    pub page: u32,
    pub year: u32,
    pub tags: Vec<String>,
    pub text: String,
}

impl From<&SearchResult> for RankedDocItem {
    fn from(sr: &SearchResult) -> Self {
        Self {
            score: sr.score,
            doc_id: sr.document.doc_id.to_string(),
            title: sr.document.title.to_string(),
            report_id: sr.document.report_id.to_string(),
            authors: sr.document.authors.to_string(),
            facility: sr.document.facility.to_string(),
            section: sr.document.section.to_string(),
            page: sr.document.page,
            year: sr.document.year,
            tags: sr.document.tags.iter().map(|s| s.to_string()).collect(),
            text: sr.document.text.to_string(),
        }
    }
}

/// RAG query request matching API contract in SCOPE.md & PROJECT.md.
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct RagQueryRequest {
    pub query: String,
    pub lang: String, // "en" | "vi"
    pub top_k: usize,
}

/// RAG query response matching API contract in SCOPE.md & PROJECT.md.
#[derive(Debug, Clone, Serialize, PartialEq)]
pub struct RagQueryResponse {
    pub query: String,
    pub ranked_documents: Vec<RankedDocItem>,
    pub directive_answer: DirectiveAnswer,
}

/// Public database facade representing the in-memory NASA PSI Vector DB.
pub struct NasaPsiVectorDb {
    index: TfidfIndex,
}

impl Default for NasaPsiVectorDb {
    fn default() -> Self {
        Self::new()
    }
}

impl NasaPsiVectorDb {
    pub fn new() -> Self {
        Self {
            index: TfidfIndex::new(),
        }
    }

    /// Execute domain-reranked vector search.
    pub fn search(&self, query: &str, top_k: usize) -> Vec<SearchResult> {
        self.index.search(query, top_k)
    }

    /// Synthesize deterministic NASA Directive 3-block answer.
    pub fn synthesize_answer(
        &self,
        query: &str,
        results: &[SearchResult],
        lang: crate::i18n::Language,
    ) -> DirectiveAnswer {
        synthesizer::synthesize_directive_answer(query, results, lang)
    }
}

static GLOBAL_VECTOR_DB: std::sync::OnceLock<NasaPsiVectorDb> = std::sync::OnceLock::new();

/// Public entry point for querying the RAG vector engine.
pub fn query_rag(req: &RagQueryRequest) -> RagQueryResponse {
    let db = GLOBAL_VECTOR_DB.get_or_init(NasaPsiVectorDb::new);
    let lang = crate::i18n::Language::from_str_loose(&req.lang);
    let top_k = if req.top_k == 0 { 3 } else { req.top_k };
    let results = db.search(&req.query, top_k);
    let directive_answer = db.synthesize_answer(&req.query, &results, lang);
    let ranked_documents = results.iter().map(RankedDocItem::from).collect();

    RagQueryResponse {
        query: req.query.clone(),
        ranked_documents,
        directive_answer,
    }
}
