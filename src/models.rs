use pyo3::prelude::*;
use pyo3::types::{PyDict, PyTuple, PyList};
use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Material {
    pub material_id: String,
    pub material_name: String,
    pub material_name_vi: String,
    pub psi_id: String,
    pub mission: String,
    pub category: String,
    pub category_vi: String,
    pub geometry: String,
    pub geometry_vi: String,
    pub moc_1g: f64,
    pub moc_microg: f64,
    pub base_spread_rate_mm_s: f64,
    pub chemical_formula: String,
    pub heat_of_combustion_mj_kg: f64,
    pub cool_flame_susceptible: bool,
    pub flame_morphology: String,
    pub flame_morphology_vi: String,
    pub quenching_mode: String,
    pub quenching_mode_vi: String,
    pub summary_notes: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct FlameMorphologyMetrics {
    pub grashof: f64,
    pub reynolds: f64,
    pub richardson: f64,
    pub peclet: f64,
    pub damkohler: f64,
    pub aspect_ratio: f64,
    pub regime_code: String,
    pub regime_name: String,
    pub color_theme: String,
    pub peak_temp_k: f64,
    pub soot_fraction: String,
    pub morph_desc: String,
}

impl FlameMorphologyMetrics {
    pub fn to_py_dict<'py>(&self, py: Python<'py>) -> PyResult<Bound<'py, PyDict>> {
        let dict = PyDict::new(py);
        dict.set_item("grashof", self.grashof)?;
        dict.set_item("reynolds", self.reynolds)?;
        dict.set_item("richardson", self.richardson)?;
        dict.set_item("peclet", self.peclet)?;
        dict.set_item("damkohler", self.damkohler)?;
        dict.set_item("aspect_ratio", self.aspect_ratio)?;
        dict.set_item("regime_code", &self.regime_code)?;
        dict.set_item("regime_name", &self.regime_name)?;
        dict.set_item("color_theme", &self.color_theme)?;
        dict.set_item("peak_temp_k", self.peak_temp_k)?;
        dict.set_item("soot_fraction", &self.soot_fraction)?;
        dict.set_item("morph_desc", &self.morph_desc)?;
        Ok(dict)
    }
}

/// Helper function to safely extract an f64 field from any Python object (dict, series, tuple pairs, etc.)
pub fn extract_f64_field(obj: &Bound<'_, PyAny>, key: &str, default: Option<f64>) -> PyResult<f64> {
    if let Ok(dict) = obj.downcast::<PyDict>() {
        if let Some(val) = dict.get_item(key)? {
            if let Ok(f) = val.extract::<f64>() {
                return Ok(f);
            }
            if let Ok(s) = val.extract::<String>() {
                if let Ok(parsed) = s.trim().parse::<f64>() {
                    return Ok(parsed);
                }
            }
        }
    } else if let Ok(tuple) = obj.downcast::<PyTuple>() {
        // Cached sweeps pass tuple(sorted(self.pmma.items()))
        for item in tuple.iter() {
            if let Ok(pair) = item.downcast::<PyTuple>() {
                if pair.len() == 2 {
                    if let Ok(k) = pair.get_item(0)?.extract::<String>() {
                        if k == key {
                            let val = pair.get_item(1)?;
                            if let Ok(f) = val.extract::<f64>() {
                                return Ok(f);
                            }
                            if let Ok(s) = val.extract::<String>() {
                                if let Ok(parsed) = s.trim().parse::<f64>() {
                                    return Ok(parsed);
                                }
                            }
                        }
                    }
                }
            }
        }
    } else if let Ok(list) = obj.downcast::<PyList>() {
        for item in list.iter() {
            if let Ok(pair) = item.downcast::<PyTuple>() {
                if pair.len() == 2 {
                    if let Ok(k) = pair.get_item(0)?.extract::<String>() {
                        if k == key {
                            let val = pair.get_item(1)?;
                            if let Ok(f) = val.extract::<f64>() {
                                return Ok(f);
                            }
                        }
                    }
                }
            }
        }
    }

    // Try general get_item
    if let Ok(val) = obj.get_item(key) {
        if let Ok(f) = val.extract::<f64>() {
            return Ok(f);
        }
        if let Ok(s) = val.extract::<String>() {
            if let Ok(parsed) = s.trim().parse::<f64>() {
                return Ok(parsed);
            }
        }
    }

    // Try general getattr
    if let Ok(val) = obj.getattr(key) {
        if let Ok(f) = val.extract::<f64>() {
            return Ok(f);
        }
    }

    if let Some(d) = default {
        Ok(d)
    } else {
        Err(pyo3::exceptions::PyKeyError::new_err(format!(
            "Missing required numeric field '{}'",
            key
        )))
    }
}

/// Helper function to safely extract a bool field from any Python object
pub fn extract_bool_field(obj: &Bound<'_, PyAny>, key: &str, default: Option<bool>) -> PyResult<bool> {
    if let Ok(dict) = obj.downcast::<PyDict>() {
        if let Some(val) = dict.get_item(key)? {
            if let Ok(b) = val.extract::<bool>() {
                return Ok(b);
            }
        }
    } else if let Ok(tuple) = obj.downcast::<PyTuple>() {
        for item in tuple.iter() {
            if let Ok(pair) = item.downcast::<PyTuple>() {
                if pair.len() == 2 {
                    if let Ok(k) = pair.get_item(0)?.extract::<String>() {
                        if k == key {
                            let val = pair.get_item(1)?;
                            if let Ok(b) = val.extract::<bool>() {
                                return Ok(b);
                            }
                        }
                    }
                }
            }
        }
    }

    if let Ok(val) = obj.get_item(key) {
        if let Ok(b) = val.extract::<bool>() {
            return Ok(b);
        }
    }

    if let Ok(val) = obj.getattr(key) {
        if let Ok(b) = val.extract::<bool>() {
            return Ok(b);
        }
    }

    if let Some(d) = default {
        Ok(d)
    } else {
        Err(pyo3::exceptions::PyKeyError::new_err(format!(
            "Missing required boolean field '{}'",
            key
        )))
    }
}

/// Helper function to safely extract a string field from any Python object
pub fn extract_string_field(obj: &Bound<'_, PyAny>, key: &str, default: Option<String>) -> PyResult<String> {
    if let Ok(dict) = obj.downcast::<PyDict>() {
        if let Some(val) = dict.get_item(key)? {
            if let Ok(s) = val.extract::<String>() {
                return Ok(s);
            }
        }
    } else if let Ok(tuple) = obj.downcast::<PyTuple>() {
        for item in tuple.iter() {
            if let Ok(pair) = item.downcast::<PyTuple>() {
                if pair.len() == 2 {
                    if let Ok(k) = pair.get_item(0)?.extract::<String>() {
                        if k == key {
                            let val = pair.get_item(1)?;
                            if let Ok(s) = val.extract::<String>() {
                                return Ok(s);
                            }
                        }
                    }
                }
            }
        }
    }

    if let Ok(val) = obj.get_item(key) {
        if let Ok(s) = val.extract::<String>() {
            return Ok(s);
        }
    }

    if let Some(d) = default {
        Ok(d)
    } else {
        Err(pyo3::exceptions::PyKeyError::new_err(format!(
            "Missing required string field '{}'",
            key
        )))
    }
}
