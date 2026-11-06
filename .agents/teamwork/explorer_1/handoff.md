# Tab 2 (Dynamic Flame Morphology Visualizer) Typography Standardization Report

## 1. Observation

A systematic forensic examination of `d:\ai\nasa\app.py`, `.streamlit\config.toml`, and the active Streamlit instance (running on port 8501) was performed to identify typography implementations across Tab 2 (`with tab_morph:`, lines 3610 to 4470).

### 1.1 Font Definition & Loading Hierarchy in `app.py`
- **Google Fonts Import** (`app.py`, Line 72):
  ```css
  @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800;900&family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600;700;800&display=swap');
  ```
  `'Plus Jakarta Sans'` is loaded globally with font weights ranging from 400 (Regular) to 900 (Black).
- **Global Typography Directives** (`app.py`, Lines 74–75):
  ```css
  html, body, [class*="css"], .stMarkdown { font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
  h1, h2, h3, h4, h5, h6, .font-heading { font-family: 'Plus Jakarta Sans', sans-serif !important; letter-spacing: -0.02em; color: #FFFFFF !important; }
  ```
- **Streamlit Configuration** (`d:\ai\nasa\.streamlit\config.toml`):
  ```toml
  [theme]
  primaryColor = "#38BDF8"
  backgroundColor = "#060D1A"
  secondaryBackgroundColor = "#133a83ff"
  textColor = "#F8FAFC"
  font = "sans serif"
  ```

---

### 1.2 Monospace / Courier Stylings in Tab 2

Investigation revealed two root mechanisms causing monospace / courier appearances in Tab 2:

#### A. Global CSS Class Forcing Monospace (`app.py`, Lines 177–178, 187, 191)
In the `<style>` block, several CSS classes utilized in Tab 2 enforce `font-family: 'JetBrains Mono', monospace !important;`:
1. **`.bento-card-title`** (`app.py`, Line 177):
   ```css
   .bento-card-title { font-size: 0.71rem !important; font-weight: 800 !important; letter-spacing: 0.05em !important; color: #94A3B8 !important; text-transform: uppercase !important; font-family: 'JetBrains Mono', monospace !important; margin-bottom: 6px !important; display: flex !important; justify-content: space-between !important; align-items: center !important; }
   ```
   - **Direct impact**: Used across all four Bento Telemetry cards in Tab 2 (lines 3669, 3711, 3745, 3792). Specifically, in Card 4 (col_t4), `<span>🌫️ SOOT & ECLSS</span>` and `<span style="color: {eclss_col}; font-size: 0.65rem;">FILTER LOAD</span>` inherit this rule, forcing them into blocky Courier/monospace.
2. **`.bento-card-val`** (`app.py`, Line 178):
   ```css
   .bento-card-val { font-size: 1.55rem !important; font-weight: 900 !important; font-family: 'JetBrains Mono', monospace !important; color: #FFFFFF !important; line-height: 1.2 !important; }
   ```
   - **Direct impact**: In Card 4 (col_t4), `{soot_str}` (e.g., `"0.00% (Zero Soot)"` or text descriptions) inherits `JetBrains Mono` with `!important`.
3. **`.bento-env-badge` & `.bento-env-item-label`** (`app.py`, Lines 187, 191):
   ```css
   .bento-env-badge { font-family: 'JetBrains Mono', monospace !important; font-size: 0.76rem !important; font-weight: 800 !important; padding: 4px 10px !important; border-radius: 99px !important; white-space: nowrap !important; letter-spacing: 0.04em !important; }
   .bento-env-item-label { display: flex !important; align-items: center !important; gap: 6px !important; font-weight: 800 !important; font-size: 0.84rem !important; margin-bottom: 5px !important; text-transform: uppercase !important; letter-spacing: 0.04em !important; font-family: 'JetBrains Mono', monospace !important; }
   ```

#### B. Component 1: Tab 2 Active Regime Banner (`app.py`, Lines 3631–3656)
- **Top-Right Stats Box** (`app.py`, Line 3647):
  ```html
  <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.82rem; color: #E2E8F0; text-align: right; background: rgba(13, 25, 48, 0.65); padding: 8px 14px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.08);">
      <div style="margin-bottom: 2px;"><b>{t['peak_temp_label']}:</b> <span style="color: #00F2FF; font-weight: 800;">~{morph_metrics['peak_temp_k']:.0f} K</span></div>
      <div><b>{t['soot_vol_label']}:</b> <span style="color: #F59E0B; font-weight: 700;">{morph_metrics['soot_fraction']}</span></div>
  </div>
  ```
  This box directly hardcodes `font-family: 'JetBrains Mono', monospace;`, causing the labels and values to render in monospace font.
- **Banner Tags & Pills** (`app.py`, Lines 3636–3641):
  ```html
  <span class="nasa-pill" style="background: {morph_metrics['color_theme']}; color: #000000; font-weight: 800; font-size: 0.72rem; letter-spacing: 0.04em;">
      {t['active_regime_badge']}
  </span>
  <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.72rem; color: #94A3B8;">
      REGIME CODE: <span style="color: {morph_metrics['color_theme']}; font-weight: 700;">{morph_metrics['regime_code']}</span>
  </span>
  ```
  `.nasa-pill` has `font-family: 'JetBrains Mono', monospace;` defined in global CSS line 106, and `REGIME CODE:` explicitly injects `font-family: 'JetBrains Mono', monospace;`.

#### C. Component 2: Card 4 'SOOT & ECLSS (FILTER LOAD)' Telemetry Card (`app.py`, Lines 3790–3808)
```html
<div class="bento-telemetry-card" style="border-top-color: {eclss_col};">
    <div class="bento-card-title">
        <span>🌫️ {'BỒ HÓNG & ECLSS' if lang == 'vi' else 'SOOT & ECLSS'}</span>
        <span style="color: {eclss_col}; font-size: 0.65rem;">FILTER LOAD</span>
    </div>
    <div class="bento-card-val" style="color: {eclss_col}; font-size: 1.25rem;">
        {soot_str}
    </div>
    <div style="margin: 8px 0 6px 0;">
        <span style="background: {eclss_bg}; color: {eclss_col}; border: 1px solid {eclss_col}66; border-radius: 99px; padding: 2px 8px; font-size: 0.68rem; font-weight: 800; display: inline-block;">
            {eclss_tag}
        </span>
    </div>
    <div class="bento-card-sub" style="color: #94A3B8; font-size: 0.70rem;">
        {eclss_sub}
    </div>
</div>
```
- Title header `SOOT & ECLSS` and `FILTER LOAD` are rendered in `JetBrains Mono` due to `.bento-card-title`.
- Value `{soot_str}` is rendered in `JetBrains Mono` due to `.bento-card-val`.
- Badge `{eclss_tag}` (`🛡️ ECLSS TỐI ƯU` / `🚨 BÁO ĐỘNG HEPA`) lacks explicit font-family specification, resulting in font inconsistency.

#### D. Component 3: Adjacent Headers & Metric Badges in Tab 2
1. **Chamber Left Cockpit Panel** (`app.py`, Lines 3818–3855):
   - Line 3818, 3823: `flame_status_beacon` (`QUENCHED / COLD` or `CIR-FLEX OPTICAL RIG`) has `font-family: 'JetBrains Mono', monospace;`.
   - Line 3834: `<span style="font-family: 'JetBrains Mono', monospace; font-size: 0.65rem; color: #64748B;">Z-AXIS 1:1 CALIBRATED</span>`.
   - Line 3843: Top-right AR badge has `font-family: 'JetBrains Mono', monospace;`.
   - Line 3848: Optical sensing strip has `font-family: 'JetBrains Mono', monospace;`.
2. **Chamber Right Cockpit Panel** (`app.py`, Lines 4130–4146):
   - Line 4130: `THERMAL & 3D RIG` badge has `font-family: 'JetBrains Mono', monospace;`.
   - Line 4134: `KELVIN FIELD` has `font-family: 'JetBrains Mono', monospace;`.
   - Line 4143: Top-right `T_max` box has `font-family: 'JetBrains Mono', monospace;`.
3. **Telemetry Footer Strips** (`app.py`, Lines 4097–4120 & Lines 4253–4278):
   - Uppercase labels (`Regime`, `Aspect Ratio`, `Transport`, `Peak Temp`, `Soot Level`, `Spectral`) use `font-family: 'JetBrains Mono', monospace;`.
4. **Environment Comparison Bento Grid** (`app.py`, Lines 4288–4468):
   - Subtitle tags (`BASELINE TERRESTRIAL`, `MICROGRAVITY SHELL`, `0.16g / 0.38g PARTIAL`) use `font-family: 'JetBrains Mono', monospace;`.

---

## 2. Logic Chain

1. **Premise**: In Tab 1 (`with tab_sim:`), NASA HUD design standards set card labels and metric headers using `.nasa-card-label` (`app.py`, Line 112: `font-family: 'Plus Jakarta Sans', sans-serif; color: #BAE6FD !important; font-weight: 800;`).
2. **Discrepancy in Tab 2**: In Tab 2, `.bento-card-title` was defined with `font-family: 'JetBrains Mono', monospace !important;` (`app.py`, Line 177). Because of CSS specificity with `!important`, this rule overrides any outer container styling and forces all card titles in Tab 2 into a typewriter monospace font.
3. **Banner Stats Box Discrepancy**: Unlike the main title `morph_metrics['regime_name']` which correctly uses `'Plus Jakarta Sans'` (`app.py`, Line 3643), the adjacent stats box (`app.py`, Line 3647) had an explicit inline declaration `font-family: 'JetBrains Mono', monospace;`.
4. **Soot & ECLSS Badge Discrepancy**: In Card 4 (col_t4), `FILTER LOAD` is a child of `.bento-card-title`, and the `{eclss_tag}` badge relies on default browser/container inheritance rather than an explicit HUD pill style. Furthermore, `{soot_str}` is textual information rendered under `.bento-card-val` (which forces `JetBrains Mono !important`).
5. **Resolution Path**:
   - Updating `.bento-card-title` in CSS from `JetBrains Mono, monospace` to `'Plus Jakarta Sans', sans-serif` automatically fixes all card titles across Tab 2, including `SOOT & ECLSS (FILTER LOAD)` and `DIMENSIONLESS TRANSPORT (FLUID / RXN)`.
   - Modifying the Banner top-right stats box inline style from `JetBrains Mono` to `'Plus Jakarta Sans', sans-serif` unifies the banner header typography.
   - Explicitly adding `'Plus Jakarta Sans', sans-serif` to `{eclss_tag}`, `{soot_str}`, and Banner pill tags provides complete typographic coherence without breaking layout or causing text wrapping issues.

---

## 3. Caveats

- **SVG Flame Visualizer Scale Bars & Rulers**: In lines 4017–4082, engineering coordinate numbers (`-140`, `0 mm`, `+120`, `50 mm`) use `JetBrains Mono`. This is standard aerospace CAD/instrumentation practice (numbers on measuring axes are tabular). The callout annotations on the flame (`Radical Shell`, `Expanding Dome`) already use or can use `'Plus Jakarta Sans'`.
- **Plotly Heatmap Tick Coordinates**: In lines 4173–4200, contour numerical ticks use `family='JetBrains Mono'`, while the overall chart layout font is already `'Plus Jakarta Sans', sans-serif` (line 4187). Numerical axes ticks do not look out of place and preserve tabular alignment.
- **Read-Only Scope**: In compliance with subagent constraints, no source code was directly edited. All proposed changes below are complete, exact, drop-in replacements.

---

## 4. Conclusion & Recommended Code Replacements

To eliminate the crude monospace font and achieve 100% typography consistency with the NASA Aerospace HUD design system, the implementer should apply the following targeted updates in `d:\ai\nasa\app.py`:

### Change 1: Global CSS Definition for `.bento-card-title`
**Target File**: `d:\ai\nasa\app.py`  
**Location**: Line 177  

```css
/* BEFORE (Line 177) */
.bento-card-title { font-size: 0.71rem !important; font-weight: 800 !important; letter-spacing: 0.05em !important; color: #94A3B8 !important; text-transform: uppercase !important; font-family: 'JetBrains Mono', monospace !important; margin-bottom: 6px !important; display: flex !important; justify-content: space-between !important; align-items: center !important; }

/* AFTER (Standardized to Plus Jakarta Sans) */
.bento-card-title { font-size: 0.71rem !important; font-weight: 800 !important; letter-spacing: 0.05em !important; color: #BAE6FD !important; text-transform: uppercase !important; font-family: 'Plus Jakarta Sans', sans-serif !important; margin-bottom: 6px !important; display: flex !important; justify-content: space-between !important; align-items: center !important; }
```

---

### Change 2: Tab 2 Active Regime Banner Top-Right Stats Box & Tags
**Target File**: `d:\ai\nasa\app.py`  
**Location**: Lines 3636–3650  

```python
# BEFORE (Lines 3636-3650)
                        <span class="nasa-pill" style="background: {morph_metrics['color_theme']}; color: #000000; font-weight: 800; font-size: 0.72rem; letter-spacing: 0.04em;">
                            {t['active_regime_badge']}
                        </span>
                        <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.72rem; color: #94A3B8;">
                            REGIME CODE: <span style="color: {morph_metrics['color_theme']}; font-weight: 700;">{morph_metrics['regime_code']}</span>
                        </span>
                    </div>
                    <h3 style="color: #FFFFFF; margin: 4px 0; font-family: 'Plus Jakarta Sans', sans-serif; font-size: 1.28rem;">
                        {morph_metrics['regime_name']}
                    </h3>
                </div>
                <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.82rem; color: #E2E8F0; text-align: right; background: rgba(13, 25, 48, 0.65); padding: 8px 14px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.08);">
                    <div style="margin-bottom: 2px;"><b>{t['peak_temp_label']}:</b> <span style="color: #00F2FF; font-weight: 800;">~{morph_metrics['peak_temp_k']:.0f} K</span></div>
                    <div><b>{t['soot_vol_label']}:</b> <span style="color: #F59E0B; font-weight: 700;">{morph_metrics['soot_fraction']}</span></div>
                </div>

# AFTER (Unified to Plus Jakarta Sans)
                        <span class="nasa-pill" style="background: {morph_metrics['color_theme']}; color: #000000; font-weight: 800; font-size: 0.72rem; letter-spacing: 0.04em; font-family: 'Plus Jakarta Sans', sans-serif;">
                            {t['active_regime_badge']}
                        </span>
                        <span style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 0.72rem; font-weight: 600; color: #94A3B8;">
                            REGIME CODE: <span style="color: {morph_metrics['color_theme']}; font-weight: 800; font-family: 'Plus Jakarta Sans', sans-serif;">{morph_metrics['regime_code']}</span>
                        </span>
                    </div>
                    <h3 style="color: #FFFFFF; margin: 4px 0; font-family: 'Plus Jakarta Sans', sans-serif; font-size: 1.28rem;">
                        {morph_metrics['regime_name']}
                    </h3>
                </div>
                <div style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 0.82rem; color: #E2E8F0; text-align: right; background: rgba(13, 25, 48, 0.65); padding: 8px 14px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.08);">
                    <div style="margin-bottom: 2px;"><b>{t['peak_temp_label']}:</b> <span style="color: #00F2FF; font-weight: 800; font-family: 'Plus Jakarta Sans', sans-serif;">~{morph_metrics['peak_temp_k']:.0f} K</span></div>
                    <div><b>{t['soot_vol_label']}:</b> <span style="color: #F59E0B; font-weight: 700; font-family: 'Plus Jakarta Sans', sans-serif;">{morph_metrics['soot_fraction']}</span></div>
                </div>
```

---

### Change 3: Card 4 'SOOT & ECLSS (FILTER LOAD)' Telemetry Card
**Target File**: `d:\ai\nasa\app.py`  
**Location**: Lines 3790–3808  

```python
# BEFORE (Lines 3790-3808)
        render_html(f"""
            <div class="bento-telemetry-card" style="border-top-color: {eclss_col};">
                <div class="bento-card-title">
                    <span>🌫️ {'BỒ HÓNG & ECLSS' if lang == 'vi' else 'SOOT & ECLSS'}</span>
                    <span style="color: {eclss_col}; font-size: 0.65rem;">FILTER LOAD</span>
                </div>
                <div class="bento-card-val" style="color: {eclss_col}; font-size: 1.25rem;">
                    {soot_str}
                </div>
                <div style="margin: 8px 0 6px 0;">
                    <span style="background: {eclss_bg}; color: {eclss_col}; border: 1px solid {eclss_col}66; border-radius: 99px; padding: 2px 8px; font-size: 0.68rem; font-weight: 800; display: inline-block;">
                        {eclss_tag}
                    </span>
                </div>
                <div class="bento-card-sub" style="color: #94A3B8; font-size: 0.70rem;">
                    {eclss_sub}
                </div>
            </div>
        """)

# AFTER (Harmonized with Plus Jakarta Sans & Enhanced Pill Badge)
        render_html(f"""
            <div class="bento-telemetry-card" style="border-top-color: {eclss_col}; font-family: 'Plus Jakarta Sans', sans-serif;">
                <div class="bento-card-title">
                    <span style="font-family: 'Plus Jakarta Sans', sans-serif; font-weight: 800;">🌫️ {'BỒ HÓNG & ECLSS' if lang == 'vi' else 'SOOT & ECLSS'}</span>
                    <span style="color: {eclss_col}; font-size: 0.65rem; font-family: 'Plus Jakarta Sans', sans-serif; font-weight: 800; letter-spacing: 0.06em;">FILTER LOAD</span>
                </div>
                <div class="bento-card-val" style="color: {eclss_col}; font-size: 1.25rem; font-family: 'Plus Jakarta Sans', sans-serif !important; font-weight: 800;">
                    {soot_str}
                </div>
                <div style="margin: 8px 0 6px 0;">
                    <span style="background: {eclss_bg}; color: {eclss_col}; border: 1px solid {eclss_col}66; border-radius: 99px; padding: 3px 9px; font-size: 0.68rem; font-weight: 800; font-family: 'Plus Jakarta Sans', sans-serif; letter-spacing: 0.03em; display: inline-block;">
                        {eclss_tag}
                    </span>
                </div>
                <div class="bento-card-sub" style="color: #94A3B8; font-size: 0.70rem; font-family: 'Plus Jakarta Sans', sans-serif;">
                    {eclss_sub}
                </div>
            </div>
        """)
```

---

### Change 4: Adjacent Cockpit Header Badges (Left & Right Flame Bays)
**Target File**: `d:\ai\nasa\app.py`  
**Location**: Lines 3818–3855 & Lines 4130–4147  

1. **Flame Status Beacon & Calibrated Tag** (Lines 3818, 3823, 3834):
   - Replace `font-family: 'JetBrains Mono', monospace;` with `font-family: 'Plus Jakarta Sans', sans-serif;` for `flame_status_beacon`.
   - Update `Z-AXIS 1:1 CALIBRATED` span: `font-family: 'Plus Jakarta Sans', sans-serif; font-weight: 700;`.
   - Update `AR:` top badge (line 3843): `font-family: 'Plus Jakarta Sans', sans-serif; font-weight: 800;`.
2. **Right Panel Badges** (Lines 4130, 4134, 4143):
   - Update `THERMAL & 3D RIG` and `KELVIN FIELD` tags to `font-family: 'Plus Jakarta Sans', sans-serif; font-weight: 700;`.
   - Update `T_max` top badge (line 4143) to `font-family: 'Plus Jakarta Sans', sans-serif; font-weight: 800;`.

---

## 5. Verification Method

To verify these changes independently:

1. **Python Syntax & Bytecode Compilation**:
   ```powershell
   d:\ai\nasa\.venv\Scripts\python.exe -m py_compile d:\ai\nasa\app.py
   ```
   *Expected outcome*: Exit code 0, zero syntax errors.

2. **Full Regression Test Suite**:
   ```powershell
   d:\ai\nasa\.venv\Scripts\python.exe d:\ai\nasa\scratch\test_full_suite.py
   ```
   *Expected outcome*: `All physical engine & vector tests passed with flying colors!`, Exit code 0.

3. **Streamlit App Live Verification**:
   Inspect the running Streamlit server (PID 12036 on `http://localhost:8501`).
   - Navigate to **Tab 2 (Dynamic Flame Morphology Visualizer)**.
   - Verify that the Active Regime Banner top-right box displays in modern, clean sans-serif ('Plus Jakarta Sans').
   - Verify that Card 4 `SOOT & ECLSS` and `FILTER LOAD` are rendered in bold 'Plus Jakarta Sans' rather than typewriter monospace.
   - Verify that the `{eclss_tag}` badge (`🛡️ ECLSS TỐI ƯU` / `🚨 BÁO ĐỘNG HEPA`) has matching rounded pill styling and font.
   - Confirm responsive behavior across viewports and bilingual toggling (`EN` and `VI`).
