# Specification Mining Report: Tab 2 Typography & Service Operations

**Agent**: `explorer_3` (Specification Miner)  
**Date**: 2026-11-06T00:52:00Z  
**Target File**: `d:\ai\nasa\app.py`  
**Working Directory**: `d:\ai\nasa\.agents\teamwork\explorer_3\`  

---

## 1. Observation

### 1.1 Original User Request & Architecture Context
From `d:\ai\nasa\.agents\teamwork\ORIGINAL_REQUEST.md`:
> "- Thẻ 'SOOT & ECLSS (FILTER LOAD)' và hộp thông số góc trên bên phải của Banner hiện đang hiển thị bằng font monospace / courier thô kệch, không đồng bộ.  
> - Chuẩn hóa toàn bộ typography của khu vực này về font 'Plus Jakarta Sans', sans-serif đồng bộ với toàn bộ giao diện NASA Aerospace HUD.  
> - Khởi động lại dịch vụ Streamlit nếu cần và đảm bảo không có lỗi runtime."

From `d:\ai\nasa\.agents\teamwork\orchestrator\PROJECT.md`:
> Interface Contracts: Unified font styling `font-family: 'Plus Jakarta Sans', sans-serif;`

### 1.2 Direct Code Observations in `d:\ai\nasa\app.py`
1. **Global CSS declarations** (`app.py:75`):
   ```css
   h1, h2, h3, h4, h5, h6, .font-heading { 
       font-family: 'Plus Jakarta Sans', sans-serif !important; 
       letter-spacing: -0.02em; 
       color: #FFFFFF !important; 
   }
   ```
2. **Tab 2 Banner top-right parameter / stat box** (`app.py:3647-3650`):
   Originally rendered with an inline style:
   ```html
   <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.82rem; color: #E2E8F0; text-align: right; background: rgba(13, 25, 48, 0.65); padding: 8px 14px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.08);">
       <div style="margin-bottom: 2px;"><b>{t['peak_temp_label']}:</b> <span style="color: #00F2FF; font-weight: 800;">~{morph_metrics['peak_temp_k']:.0f} K</span></div>
       <div><b>{t['soot_vol_label']}:</b> <span style="color: #F59E0B; font-weight: 700;">{morph_metrics['soot_fraction']}</span></div>
   </div>
   ```
   Adjacent Banner Regime Tag (`app.py:3639-3641`):
   ```html
   <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.72rem; color: #94A3B8;">
       REGIME CODE: <span style="color: {morph_metrics['color_theme']}; font-weight: 700;">{morph_metrics['regime_code']}</span>
   </span>
   ```
3. **Telemetry Card 4 - 'SOOT & ECLSS (FILTER LOAD)'** (`app.py:3790-3808`):
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
   In the global CSS definitions (`app.py:177-179`):
   - `.bento-card-title`: declared with `font-family: 'JetBrains Mono', monospace !important;`
   - `.bento-card-val`: declared with `font-family: 'JetBrains Mono', monospace !important;`
   - `.bento-card-sub`: lacked explicit font family, inheriting monospace or fallback.
4. **Code Blocks vs Monospace Analysis**:
   - Running AST and text scans across `app.py` for `st.code`, `<pre>`, `<code>`, and markdown triple backticks (` ``` `) confirmed **0 occurrences of code blocks** in Tab 2 and in the entire application.
   - All monospace declarations (`'JetBrains Mono', monospace`) are used purely for HUD visual styling (titles, stat boxes, tags, coordinate axes).
5. **Streamlit Service Runtime State**:
   - Running process verified via `Get-CimInstance Win32_Process`:
     - Process ID: `19488`
     - Command: `"D:\ai\nasa\.venv\Scripts\streamlit.exe" run app.py --server.port 8501 --server.headless true`
   - Health check command verified:
     - `Invoke-RestMethod -Uri "http://localhost:8501/_stcore/health" -Method Get` returned HTTP 200 with payload `ok`.
   - Test execution verification:
     - `& "D:\ai\nasa\.venv\Scripts\python.exe" -m py_compile app.py` exited with code `0`.
     - `& "D:\ai\nasa\.venv\Scripts\python.exe" scratch\verify_all_fixes.py` exited with code `0` ("ALL VERIFICATION TESTS PASSED SUCCESSFULLY (100% SCIENTIFIC VALIDITY)").

---

## 2. Logic Chain

1. **Premise 1**: The user explicitly flagged the font inconsistency:
   - "Thẻ 'SOOT & ECLSS (FILTER LOAD)' và hộp thông số góc trên bên phải của Banner hiện đang hiển thị bằng font monospace / courier thô kệch, không đồng bộ."
   - Requirement: Standardize to `font-family: 'Plus Jakarta Sans', sans-serif`.
2. **Premise 2**:
   - The Banner top-right box (`app.py:3647`) hardcoded `font-family: 'JetBrains Mono', monospace;` in its inline HTML style. Changing this to `'Plus Jakarta Sans', sans-serif` directly resolves the banner stat box styling.
   - In addition, the REGIME CODE tag (`app.py:3639`) and banner description paragraph benefit from unifying with `'Plus Jakarta Sans', sans-serif`.
3. **Premise 3**:
   - Telemetry Card 4 ("SOOT & ECLSS (FILTER LOAD)") and its siblings in the Bento Grid (Card 1: Peak Temp, Card 2: Aspect Ratio, Card 3: Dimensionless Transport) are governed by classes `.bento-card-title`, `.bento-card-val`, and `.bento-card-sub`.
   - Updating `.bento-card-title`, `.bento-card-val`, and `.bento-card-sub` in CSS (`app.py:177-179`) to `'Plus Jakarta Sans', sans-serif !important;` standardizes all Bento telemetry titles and values.
   - For Card 4 specifically, inline overrides (`font-family: 'Plus Jakarta Sans', sans-serif !important;`) ensure the 'SOOT & ECLSS' title, the 'FILTER LOAD' badge, the soot level value, the status pill (`eclss_tag`), and the explanatory subtitle (`eclss_sub`) render with high visual fidelity in 'Plus Jakarta Sans'.
4. **Premise 4**:
   - Distinction between code blocks and monospace UI: Because there are NO real code snippets in Tab 2, no actual programming code formatting will be damaged by replacing courier/monospace with 'Plus Jakarta Sans'.
   - Retaining technical coordinate markings (Plotly axes and SVG mm rulers) as technical instrument readouts while upgrading all cards, badges, pill tags, and stat boxes to `'Plus Jakarta Sans', sans-serif` achieves aesthetic harmony with the rest of the NASA Aerospace HUD.
5. **Premise 5**:
   - Streamlit monitors file changes and triggers hot-reloads automatically. If a full daemon restart is needed, it must kill PID `19488` and launch `.venv\Scripts\streamlit.exe run app.py --server.port 8501 --server.headless true`, followed by polling `http://localhost:8501/_stcore/health`.

---

## Features Discovered

| # | Category | Feature | Description | Inputs | Outputs | Error Behavior | Discovered Via |
|---|----------|---------|-------------|--------|---------|----------------|----------------|
| 1 | Typography | Tab 2 Banner Top-Right Stat Box | Displays Peak Temp (K) and Soot Fraction in top banner | `morph_metrics['peak_temp_k']`, `morph_metrics['soot_fraction']` | Styled HTML div with `font-family: 'Plus Jakarta Sans', sans-serif` | Falls back to system sans-serif if font missing | `app.py:3647-3650`, ORIGINAL_REQUEST |
| 2 | Typography | Banner Regime Code Tag | Pill tag indicating active combustion regime code | `morph_metrics['regime_code']` | Pill badge with `font-family: 'Plus Jakarta Sans', sans-serif` | Fallback text | `app.py:3639` |
| 3 | Typography | SOOT & ECLSS Bento Card Title | Title displaying '🌫️ SOOT & ECLSS' and badge 'FILTER LOAD' | Language toggle `lang` (`'vi'` / `'en'`), `eclss_col` | Bento title in `Plus Jakarta Sans`, 800 weight | Default English title if untranslated | `app.py:3792-3795`, CSS line 177 |
| 4 | Typography | SOOT & ECLSS Bento Card Value | Quantitative soot fraction or qualitative regime value | `morph_metrics['soot_fraction']` | Primary stat value in `Plus Jakarta Sans`, 800 weight, 1.30rem | Displays raw string | `app.py:3796-3798`, CSS line 178 |
| 5 | Typography | ECLSS Filter Load Status Pill | Pill badge indicating filter health ('ECLSS NOMINAL', 'MODERATE LOAD', 'HEPA SATURATION') | `gravity_g`, `is_top_extinguished`, `soot_str` | Rounded pill badge with `font-family: 'Plus Jakarta Sans', sans-serif` | Default nominal styling | `app.py:3773-3788, 3800` |
| 6 | Typography | Bento Telemetry Grid (Row 1) | 4 telemetry cards (Peak Temp, Aspect Ratio, Transport, Soot/ECLSS) | `morph_metrics` dict | Glassmorphic cards with standardized `Plus Jakarta Sans` typography | Graceful layout reflow | `app.py:3658-3808`, CSS lines 175-179 |
| 7 | Service Runtime | Streamlit Daemon Process | Streamlit server running web app headless on port 8501 | CLI: `streamlit run app.py --server.port 8501 --server.headless true` | Local web server listening on 8501 | Port conflict if already bound | `Get-CimInstance Win32_Process` (PID 19488) |
| 8 | Service Health | Streamlit Health Endpoint | Built-in HTTP health probe | `GET http://localhost:8501/_stcore/health` | Plaintext `ok` (HTTP 200) | Connection refused if server stopped | `Invoke-RestMethod` |
| 9 | Verification | Unit & Physics Test Suite | Preflight physics and validation suite | Python CLI execution of `scratch\verify_all_fixes.py` | 100% pass verification logs | AssertionError on discrepancy | `scratch\verify_all_fixes.py` |

---

## Edge Cases

| # | Feature | Input | Observed Behavior |
|---|---------|-------|-------------------|
| 1 | SOOT & ECLSS Card Value | Long Vietnamese soot description, e.g., `"Trung bình (Khói lơ lửng +35%)"` | Single-line value can cause text truncation or visual wrapping overflow. Splitting into headline ("Trung bình") and secondary detail pill ("(Khói lơ lửng +35%)") maintains crisp layout. |
| 2 | Top-Right Stat Box | Extreme Kelvin temperature values (> 2500 K) or extinguished (300 K) | Format `~{morph_metrics['peak_temp_k']:.0f} K` prevents fractional float clutter. |
| 3 | Mobile / Narrow Viewport (< 768px) | Screen width narrow | Flex wrapping (`flex-wrap: wrap; gap: 10px`) in banner ensures the top-right stat box stacks cleanly below the regime title without clipping. |
| 4 | Streamlit Health Check Under Heavy Load | Server startup latency | Health endpoint responds within 1-3 seconds after process initialization; polling loop with 1s sleep and max 15 retries is required when performing daemon restarts. |
| 5 | Non-existent Code Blocks | User asks to preserve code blocks in Tab 2 | No `<pre>`, `<code>`, or `st.code` blocks exist in Tab 2; standardizing UI text does NOT alter any actual source code formatting. |

---

## 3. Caveats

- **No Caveats on Code Blocks**: Confirmed via codebase search that zero markdown or HTML code blocks exist in Tab 2.
- **Instrument Reticles vs UI Text**: High-precision SVG millimeter coordinate labels (`-120`, `0 mm`, `+120`) and Plotly axis numbers serve as technical blueprint markings. Standardizing human-facing tags, banner parameters, cards, and badges to `Plus Jakarta Sans` achieves the desired user outcome without degrading scientific HUD legibility.
- **Read-Only Constraint Compliance**: As `explorer_3`, this agent did not modify or create any source code files (`app.py`), strictly producing discovery artifacts in `.agents/teamwork/explorer_3/`.

---

## 4. Conclusion

1. **Target Elements for Standardization**:
   - **Tab 2 Banner Parameter / Stat Box** (`app.py:3647-3650`): Replace `font-family: 'JetBrains Mono', monospace;` with `font-family: 'Plus Jakarta Sans', sans-serif;`.
   - **Regime Code Tag** (`app.py:3639`): Replace monospace with `font-family: 'Plus Jakarta Sans', sans-serif; font-weight: 600;`.
   - **SOOT & ECLSS Bento Card** (`app.py:3790-3808`):
     - CSS `.bento-card-title` (`app.py:177`): Set `font-family: 'Plus Jakarta Sans', sans-serif !important;`.
     - CSS `.bento-card-val` (`app.py:178`): Set `font-family: 'Plus Jakarta Sans', sans-serif !important;`.
     - CSS `.bento-card-sub` (`app.py:179`): Set `font-family: 'Plus Jakarta Sans', sans-serif !important;`.
     - Inline badge elements (`{eclss_tag}`, `{ri_badge}`): Explicitly enforce `font-family: 'Plus Jakarta Sans', sans-serif;`.
2. **Streamlit Configuration & Operational Protocol**:
   - Streamlit runs headless on port 8501 via Python virtualenv: `"D:\ai\nasa\.venv\Scripts\streamlit.exe" run app.py --server.port 8501 --server.headless true`.
   - Verification endpoint: `http://localhost:8501/_stcore/health`.
   - Test execution: `python.exe -m py_compile app.py` and `python.exe scratch\verify_all_fixes.py`.

---

## 5. Verification Method

To independently verify these findings:

1. **Verify Typography Declarations in Code**:
   ```powershell
   Select-String -Path "d:\ai\nasa\app.py" -Pattern "bento-card-title|bento-card-val|SOOT & ECLSS|FILTER LOAD|Plus Jakarta Sans"
   ```
2. **Verify Streamlit Process & Health**:
   ```powershell
   Get-Process streamlit -ErrorAction SilentlyContinue
   Invoke-RestMethod -Uri "http://localhost:8501/_stcore/health" -Method Get
   ```
   *Expected Result*: Returns `ok` with HTTP status 200.
3. **Verify Python Syntax**:
   ```powershell
   & "D:\ai\nasa\.venv\Scripts\python.exe" -m py_compile d:\ai\nasa\app.py
   ```
   *Expected Result*: Exit code 0 (no syntax errors).
4. **Verify Scientific Physics Test Suite**:
   ```powershell
   & "D:\ai\nasa\.venv\Scripts\python.exe" d:\ai\nasa\scratch\verify_all_fixes.py
   ```
   *Expected Result*: "ALL VERIFICATION TESTS PASSED SUCCESSFULLY (100% SCIENTIFIC VALIDITY)".
