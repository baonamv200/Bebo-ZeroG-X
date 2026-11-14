pub mod models;
pub mod physics;
pub mod mesh;
pub mod sweeps;
pub mod data_loader;
pub mod vector_db;

use pyo3::prelude::*;
use pyo3::types::{PyBool, PyDict, PyList, PyString, PyTuple};
use std::collections::HashMap;

use models::{
    extract_bool_field, extract_f64_field, extract_string_field, Material,
};
use physics::{
    calculate_effective_moc_core, calculate_flame_morphology_metrics_core,
    calculate_flame_spread_rate_core, calculate_space_fire_risk_score_core, detect_cool_flames_core,
    generate_extinction_curve_core,
};
use mesh::calculate_temperature_mesh_core;
use sweeps::{calculate_cached_boundary_sweep_core, calculate_cached_paradox_sweep_core};
use data_loader::load_nasa_psi_data_core;
use vector_db::{normalize_vn_text as rust_normalize_vn_text, NASAPsiVectorDB as RustVectorDB, DocRecord};

#[pyclass]
pub struct MicrogravityCombustionPhysics;

#[pymethods]
impl MicrogravityCombustionPhysics {
    #[staticmethod]
    pub fn calculate_effective_moc(
        material: &Bound<'_, PyAny>,
        gravity_g: f64,
        airflow_cm_s: f64,
        pressure_kpa: f64,
    ) -> PyResult<f64> {
        let moc_1g = extract_f64_field(material, "moc_1g", None)?;
        let moc_ug = extract_f64_field(material, "moc_microg", None)?;
        Ok(calculate_effective_moc_core(
            moc_1g,
            moc_ug,
            gravity_g,
            airflow_cm_s,
            pressure_kpa,
        ))
    }

    #[staticmethod]
    pub fn calculate_flame_spread_rate(
        material: &Bound<'_, PyAny>,
        gravity_g: f64,
        oxygen_pct: f64,
        pressure_kpa: f64,
        airflow_cm_s: f64,
        effective_moc: f64,
    ) -> PyResult<f64> {
        let base_spread = extract_f64_field(material, "base_spread_rate_mm_s", None)?;
        let moc_ug = extract_f64_field(material, "moc_microg", None)?;
        Ok(calculate_flame_spread_rate_core(
            base_spread,
            moc_ug,
            gravity_g,
            oxygen_pct,
            pressure_kpa,
            airflow_cm_s,
            effective_moc,
        ))
    }

    #[staticmethod]
    pub fn calculate_space_fire_risk_score(
        material: &Bound<'_, PyAny>,
        effective_moc: f64,
        spread_rate: f64,
        oxygen_pct: f64,
        pressure_kpa: f64,
        airflow_cm_s: f64,
    ) -> PyResult<(f64, String, String)> {
        let hoc = extract_f64_field(material, "heat_of_combustion_mj_kg", Some(20.0))?;
        Ok(calculate_space_fire_risk_score_core(
            effective_moc,
            spread_rate,
            oxygen_pct,
            pressure_kpa,
            airflow_cm_s,
            hoc,
        ))
    }

    #[staticmethod]
    #[pyo3(signature = (material, gravity_g, airflow_cm_s, oxygen_pct, pressure_kpa, lang="en", eff_moc=None))]
    pub fn detect_cool_flames(
        material: &Bound<'_, PyAny>,
        gravity_g: f64,
        airflow_cm_s: f64,
        oxygen_pct: f64,
        pressure_kpa: f64,
        lang: &str,
        eff_moc: Option<f64>,
    ) -> PyResult<(bool, String)> {
        let susceptible = extract_bool_field(material, "cool_flame_susceptible", Some(false))?;
        let eff = match eff_moc {
            Some(v) => v,
            None => {
                let moc_1g = extract_f64_field(material, "moc_1g", None)?;
                let moc_ug = extract_f64_field(material, "moc_microg", None)?;
                calculate_effective_moc_core(moc_1g, moc_ug, gravity_g, airflow_cm_s, pressure_kpa)
            }
        };
        Ok(detect_cool_flames_core(
            susceptible,
            eff,
            gravity_g,
            airflow_cm_s,
            oxygen_pct,
            pressure_kpa,
            lang,
        ))
    }

    #[staticmethod]
    pub fn generate_extinction_curve(
        material: &Bound<'_, PyAny>,
        gravity_g: f64,
        pressure_kpa: f64,
    ) -> PyResult<(Vec<f64>, Vec<f64>)> {
        let moc_1g = extract_f64_field(material, "moc_1g", None)?;
        let moc_ug = extract_f64_field(material, "moc_microg", None)?;
        Ok(generate_extinction_curve_core(
            moc_1g,
            moc_ug,
            gravity_g,
            pressure_kpa,
        ))
    }

    #[staticmethod]
    #[pyo3(signature = (gravity_g, airflow_cm_s, oxygen_pct, pressure_kpa=101.325, lang="vi", is_extinguished=false, material_row=None))]
    pub fn calculate_flame_morphology_metrics<'py>(
        py: Python<'py>,
        gravity_g: f64,
        airflow_cm_s: f64,
        oxygen_pct: f64,
        pressure_kpa: f64,
        lang: &str,
        is_extinguished: bool,
        material_row: Option<&Bound<'_, PyAny>>,
    ) -> PyResult<Bound<'py, PyDict>> {
        let hoc = match material_row {
            Some(m) => Some(extract_f64_field(m, "heat_of_combustion_mj_kg", Some(25.0))?),
            None => None,
        };

        let metrics = calculate_flame_morphology_metrics_core(
            gravity_g,
            airflow_cm_s,
            oxygen_pct,
            pressure_kpa,
            lang,
            is_extinguished,
            hoc,
        );

        metrics.to_py_dict(py)
    }
}

#[pyfunction]
#[pyo3(signature = (gravity_g, airflow_cm_s, peak_temp_k, is_extinguished=false))]
pub fn calculate_temperature_mesh(
    gravity_g: f64,
    airflow_cm_s: f64,
    peak_temp_k: f64,
    is_extinguished: bool,
) -> (Vec<f64>, Vec<f64>, Vec<Vec<f64>>, Vec<(f64, String)>) {
    calculate_temperature_mesh_core(gravity_g, airflow_cm_s, peak_temp_k, is_extinguished)
}

#[pyfunction]
pub fn calculate_cached_paradox_sweep(
    material: &Bound<'_, PyAny>,
    oxygen_pct: f64,
    pressure_kpa: f64,
    gravity_g: f64,
) -> PyResult<(Vec<f64>, Vec<f64>, Vec<f64>, Vec<f64>)> {
    let moc_1g = extract_f64_field(material, "moc_1g", None)?;
    let moc_ug = extract_f64_field(material, "moc_microg", None)?;
    let base_spread = extract_f64_field(material, "base_spread_rate_mm_s", None)?;
    Ok(calculate_cached_paradox_sweep_core(
        moc_1g,
        moc_ug,
        base_spread,
        oxygen_pct,
        pressure_kpa,
        gravity_g,
    ))
}

#[pyfunction]
pub fn calculate_cached_boundary_sweep(
    material: &Bound<'_, PyAny>,
    gravity_g: f64,
    pressure_kpa: f64,
) -> PyResult<(Vec<f64>, Vec<f64>)> {
    let moc_1g = extract_f64_field(material, "moc_1g", None)?;
    let moc_ug = extract_f64_field(material, "moc_microg", None)?;
    Ok(calculate_cached_boundary_sweep_core(
        moc_1g,
        moc_ug,
        gravity_g,
        pressure_kpa,
    ))
}

fn material_to_pydict<'py>(py: Python<'py>, mat: &Material) -> PyResult<Bound<'py, PyDict>> {
    let dict = PyDict::new(py);
    dict.set_item("material_id", &mat.material_id)?;
    dict.set_item("material_name", &mat.material_name)?;
    dict.set_item("material_name_vi", &mat.material_name_vi)?;
    dict.set_item("psi_id", &mat.psi_id)?;
    dict.set_item("mission", &mat.mission)?;
    dict.set_item("category", &mat.category)?;
    dict.set_item("category_vi", &mat.category_vi)?;
    dict.set_item("geometry", &mat.geometry)?;
    dict.set_item("geometry_vi", &mat.geometry_vi)?;
    dict.set_item("moc_1g", mat.moc_1g)?;
    dict.set_item("moc_microg", mat.moc_microg)?;
    dict.set_item("base_spread_rate_mm_s", mat.base_spread_rate_mm_s)?;
    dict.set_item("chemical_formula", &mat.chemical_formula)?;
    dict.set_item("heat_of_combustion_mj_kg", mat.heat_of_combustion_mj_kg)?;
    dict.set_item("cool_flame_susceptible", mat.cool_flame_susceptible)?;
    dict.set_item("flame_morphology", &mat.flame_morphology)?;
    dict.set_item("flame_morphology_vi", &mat.flame_morphology_vi)?;
    dict.set_item("quenching_mode", &mat.quenching_mode)?;
    dict.set_item("quenching_mode_vi", &mat.quenching_mode_vi)?;
    dict.set_item("summary_notes", &mat.summary_notes)?;
    Ok(dict)
}

#[pyfunction]
pub fn evaluate_all_materials<'py>(
    py: Python<'py>,
    materials: &Bound<'_, PyAny>,
    gravity_g: f64,
    oxygen_pct: f64,
    pressure_kpa: f64,
    airflow_cm_s: f64,
    lang: &str,
) -> PyResult<(Bound<'py, PyList>, usize)> {
    let mut rows: Vec<(f64, Bound<'py, PyDict>)> = Vec::new();
    let mut cf_count = 0;

    for item in materials.try_iter()? {
        let mat = item?;
        let moc_1g = extract_f64_field(&mat, "moc_1g", None)?;
        let moc_ug = extract_f64_field(&mat, "moc_microg", None)?;
        let base_spread = extract_f64_field(&mat, "base_spread_rate_mm_s", None)?;
        let hoc = extract_f64_field(&mat, "heat_of_combustion_mj_kg", Some(20.0))?;
        let cool_flame_susc = extract_bool_field(&mat, "cool_flame_susceptible", Some(false))?;

        let eff_moc = calculate_effective_moc_core(moc_1g, moc_ug, gravity_g, airflow_cm_s, pressure_kpa);
        let spread = calculate_flame_spread_rate_core(base_spread, moc_ug, gravity_g, oxygen_pct, pressure_kpa, airflow_cm_s, eff_moc);
        let (sfrs, tier, color) = calculate_space_fire_risk_score_core(eff_moc, spread, oxygen_pct, pressure_kpa, airflow_cm_s, hoc);
        let (cf_active, cf_msg) = detect_cool_flames_core(cool_flame_susc, eff_moc, gravity_g, airflow_cm_s, oxygen_pct, pressure_kpa, lang);

        if cf_active {
            cf_count += 1;
        }

        let material_id = extract_string_field(&mat, "material_id", Some("".to_string()))?;
        let mat_name_en = extract_string_field(&mat, "material_name", Some("".to_string()))?;
        let mat_name_vi = extract_string_field(&mat, "material_name_vi", Some(mat_name_en.clone()))?;
        let material_name = if lang == "vi" { mat_name_vi } else { mat_name_en };

        let cat_en = extract_string_field(&mat, "category", Some("".to_string()))?;
        let cat_vi = extract_string_field(&mat, "category_vi", Some(cat_en.clone()))?;
        let category = if lang == "vi" { cat_vi } else { cat_en };

        let psi_id = extract_string_field(&mat, "psi_id", Some("".to_string()))?;
        let mission = extract_string_field(&mat, "mission", Some("".to_string()))?;

        let row_dict = PyDict::new(py);
        row_dict.set_item("material_id", material_id)?;
        row_dict.set_item("material_name", material_name)?;
        row_dict.set_item("category", category)?;
        row_dict.set_item("psi_id", psi_id)?;
        row_dict.set_item("mission", mission)?;
        row_dict.set_item("effective_moc", (eff_moc * 100.0).round() / 100.0)?;
        row_dict.set_item("flame_spread_rate_mm_s", (spread * 1000.0).round() / 1000.0)?;
        row_dict.set_item("spread_rate", (spread * 1000.0).round() / 1000.0)?;
        row_dict.set_item("sfrs", (sfrs * 10.0).round() / 10.0)?;
        row_dict.set_item("tier", tier)?;
        row_dict.set_item("color", color)?;

        let cf_bool = PyBool::new(py, cf_active);
        let cf_str = PyString::new(py, &cf_msg);
        let cf_tuple = PyTuple::new(py, &[cf_bool.as_any(), cf_str.as_any()])?;
        row_dict.set_item("cool_flame", cf_tuple)?;
        row_dict.set_item("raw_mat", &mat)?;

        rows.push((sfrs, row_dict));
    }

    rows.sort_by(|a, b| b.0.partial_cmp(&a.0).unwrap_or(std::cmp::Ordering::Equal));

    let py_list = PyList::empty(py);
    for (_, r) in rows {
        py_list.append(r)?;
    }

    Ok((py_list, cf_count))
}

#[pyfunction]
pub fn normalize_vn_text(text: &str) -> String {
    rust_normalize_vn_text(text)
}

#[pyfunction]
#[pyo3(signature = (data_dir=None))]
pub fn load_nasa_psi_data<'py>(
    py: Python<'py>,
    data_dir: Option<&str>,
) -> PyResult<Bound<'py, PyDict>> {
    let (embedded, sofie, saffire, bass, status) = load_nasa_psi_data_core(data_dir);

    let result = PyDict::new(py);

    let mat_list = PyList::empty(py);
    for m in &embedded {
        mat_list.append(material_to_pydict(py, m)?)?;
    }
    result.set_item("embedded_materials", mat_list)?;

    let records_to_pylist = |recs_opt: Option<Vec<HashMap<String, String>>>| -> PyResult<Option<Bound<'py, PyList>>> {
        if let Some(recs) = recs_opt {
            let list = PyList::empty(py);
            for rec in recs {
                let d = PyDict::new(py);
                for (k, v) in rec {
                    d.set_item(k, v)?;
                }
                list.append(d)?;
            }
            Ok(Some(list))
        } else {
            Ok(None)
        }
    };

    result.set_item("sofie_records", records_to_pylist(sofie)?)?;
    result.set_item("saffire_records", records_to_pylist(saffire)?)?;
    result.set_item("bass_records", records_to_pylist(bass)?)?;
    result.set_item("source_status", status)?;

    Ok(result)
}

#[pyclass]
pub struct NASAPsiVectorDB {
    inner: RustVectorDB,
}

#[pymethods]
impl NASAPsiVectorDB {
    #[new]
    pub fn new() -> Self {
        Self {
            inner: RustVectorDB::new(),
        }
    }

    #[pyo3(signature = (query_text, top_k=3))]
    pub fn search<'py>(
        &self,
        py: Python<'py>,
        query_text: &str,
        top_k: usize,
    ) -> PyResult<Bound<'py, PyList>> {
        let results = self.inner.search(query_text, top_k);
        let py_list = PyList::empty(py);

        for (score, doc) in results {
            let doc_dict = PyDict::new(py);
            doc_dict.set_item("doc_id", &doc.doc_id)?;
            doc_dict.set_item("title", &doc.title)?;
            doc_dict.set_item("report_id", &doc.report_id)?;
            doc_dict.set_item("authors", &doc.authors)?;
            doc_dict.set_item("facility", &doc.facility)?;
            doc_dict.set_item("section", &doc.section)?;
            doc_dict.set_item("page", doc.page)?;
            doc_dict.set_item("year", doc.year)?;

            let tags_list = PyList::empty(py);
            for t in &doc.tags {
                tags_list.append(t)?;
            }
            doc_dict.set_item("tags", tags_list)?;
            doc_dict.set_item("text", &doc.text)?;

            let py_score = score.into_pyobject(py)?;
            let tuple = PyTuple::new(py, &[py_score.as_any(), doc_dict.as_any()])?;
            py_list.append(tuple)?;
        }

        Ok(py_list)
    }

    #[pyo3(signature = (query_text, ranked_results, lang="en"))]
    pub fn synthesize_answer(
        &self,
        query_text: &str,
        ranked_results: &Bound<'_, PyAny>,
        lang: &str,
    ) -> PyResult<String> {
        let mut rust_ranked = Vec::new();

        if let Ok(iter) = ranked_results.try_iter() {
            for item in iter {
                let pair = item?;
                if let Ok(tuple) = pair.downcast::<PyTuple>() {
                    if tuple.len() >= 2 {
                        let score = tuple.get_item(0)?.extract::<f64>().unwrap_or(0.0);
                        let doc_obj = tuple.get_item(1)?;

                        let doc_id = extract_string_field(&doc_obj, "doc_id", Some("".to_string()))?;
                        let title = extract_string_field(&doc_obj, "title", Some("".to_string()))?;
                        let report_id = extract_string_field(&doc_obj, "report_id", Some("".to_string()))?;
                        let authors = extract_string_field(&doc_obj, "authors", Some("".to_string()))?;
                        let facility = extract_string_field(&doc_obj, "facility", Some("".to_string()))?;
                        let section = extract_string_field(&doc_obj, "section", Some("".to_string()))?;
                        let page = extract_f64_field(&doc_obj, "page", Some(0.0))? as i64;
                        let year = extract_f64_field(&doc_obj, "year", Some(2023.0))? as i64;
                        let text = extract_string_field(&doc_obj, "text", Some("".to_string()))?;

                        let tags = if let Ok(t_list) = doc_obj.get_item("tags") {
                            if let Ok(list_iter) = t_list.try_iter() {
                                list_iter
                                    .filter_map(|x| x.ok().and_then(|val| val.extract::<String>().ok()))
                                    .collect()
                            } else {
                                Vec::new()
                            }
                        } else {
                            Vec::new()
                        };

                        rust_ranked.push((
                            score,
                            DocRecord {
                                doc_id,
                                title,
                                report_id,
                                authors,
                                facility,
                                section,
                                page,
                                year,
                                tags,
                                text,
                            },
                        ));
                    }
                }
            }
        }

        Ok(self.inner.synthesize_answer(query_text, &rust_ranked, lang))
    }
}

#[pyfunction]
fn rust_health_check() -> &'static str {
    "ok"
}

#[pymodule]
fn nasa_rust(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<MicrogravityCombustionPhysics>()?;
    m.add_class::<NASAPsiVectorDB>()?;
    m.add_function(wrap_pyfunction!(calculate_temperature_mesh, m)?)?;
    m.add_function(wrap_pyfunction!(calculate_cached_paradox_sweep, m)?)?;
    m.add_function(wrap_pyfunction!(calculate_cached_boundary_sweep, m)?)?;
    m.add_function(wrap_pyfunction!(evaluate_all_materials, m)?)?;
    m.add_function(wrap_pyfunction!(normalize_vn_text, m)?)?;
    m.add_function(wrap_pyfunction!(load_nasa_psi_data, m)?)?;
    m.add_function(wrap_pyfunction!(rust_health_check, m)?)?;
    Ok(())
}
