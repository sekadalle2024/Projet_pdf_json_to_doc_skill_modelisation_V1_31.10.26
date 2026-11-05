# Implementation Plan: Cas 14 FRAP/Recommandations - Phase 2 Python Scripts

## Context Summary

**Project**: Audit document automation (PDF/Excel project)  
**Task**: Implement Phase 2 of Cas 14 (FRAP/Recommandations) - Create 2 Python scripts  
**Environment**: conda env `pdf_excel_env`, Python >= 3.9  
**Location**: `h:\Projet_pdf_excel\Modelisation claude skill\Cas_14/`  
**Phase 1 Status**: ✅ Complete (Documentation created)  

**Key Specifications for Cas 14**:
- **Unique feature**: Table 1 column 1 has bordeaux background #8B0000 (RGB 139, 0, 0) - NOT #7B1E3A like Cas 2/3/6
- **6 tables structure**: 1 metadata table (vertical) + 5 content tables (horizontal, 1 column each)
- **Table 1**: Vertical format (2 columns), column 1 has bordeaux background with white text
- **Tables 2-6**: Horizontal format (1 column each), content with bullet points
- **Orientation**: Landscape A4
- **Header**: Bordeaux background (#8B0000) with white text "Logiciel automatisé E-audit pro - Frap"
- **Footer**: WhatsApp contact centered, bordeaux color
- **Filename format**: `<Reference>-<Etape_de_mission>- Logiciel automatisé E-audit pro_<timestamp>.docx`

**Reference Implementations**:
- Cas 12: `json2word_cartographie_risques.py` - Similar table generation patterns
- Cas 2: `json2word_audit.py` - Column specs and rendering patterns
- Cas 2: `execute_cas2_production.py` - Orchestrator workflow pattern

**JSON Structure** (from `exemple_frap_minimal.json`):
```json
{
  "Data_integrale": [{
    "Etape mission - Frap": [
      {"table 1": {"Etape de mission": "...", "Norme": "...", "Méthode": "...", "Reference": "..."}},
      {"table 2": {"Intitule": "..."}},
      {"table 3": {"Observation": "..."}},
      {"table 4": {"Constat": "..."}},
      {"table 5": {"Risque": "..."}},
      {"table 6": {"Recommendation": "..."}}
    ]
  }]
}
```

---

## Implementation Plan

- [ ] 1. **Create `json2word_frap.py` - Main converter script (Phase 2.1)**
      
      Create the main conversion script at `h:\Projet_pdf_excel\Modelisation claude skill\Cas_14\json2word_frap.py` following the full specification in `audit-frap-recos-json2word.skill.md`.
      
      **Implementation approach**:
      
      **Import section**:
      - Import standard libs: `argparse`, `json`, `random`, `re`, `string`, `sys`, `datetime`, `pathlib.Path`
      - Import python-docx: `Document`, `Inches`, `Pt`, `RGBColor`, `Twips`
      - Import enums: `WD_ORIENT`, `WD_ALIGN_PARAGRAPH`, `WD_ALIGN_VERTICAL`, `WD_LINE_SPACING`
      - Import XML: `qn`, `OxmlElement`
      
      **Constants section**:
      - `BORDEAUX_RGB = (139, 0, 0)` - #8B0000 (UNIQUE TO CAS 14 - different from Cas 2/3/6)
      - `WHITE_RGB = (255, 255, 255)`
      - `FONT_NAME = "Arial"`
      - `FONT_SIZE = 8.5` (pt)
      - `DEFAULT_SOFTWARE = "Logiciel automatisé E-audit pro"`
      - `DEFAULT_FOOTER = "Automatisez vos activités d'audit, risques et contrôles - Whatsapp : + 225 05 44 13 07 98"`
      - Margins: Top=1200, Bottom=1100, Left/Right=900 (twips)
      
      **Function: `extract_json_from_text(text: str) -> dict`**:
      - Parse JSON from text that may contain surrounding content
      - Find first `{` character, use `json.JSONDecoder().raw_decode()`
      - Handle UTF-8 with BOM (`utf-8-sig`)
      - Return parsed dict or raise ValueError
      
      **Function: `generate_reference() -> str`**:
      - Generate reference like "AUTO-<timestamp>" if not provided
      - Use `datetime.now().strftime("%Y%m%d_%H%M%S")`
      - Return string reference
      
      **Function: `set_cell_background(cell, color_rgb: tuple)`**:
      - Get or add `tcPr` element from `cell._tc`
      - Create `w:shd` OxmlElement with attributes `val="clear"`, `color="auto"`
      - Set `fill` attribute to hex color: `f"{color_rgb[0]:02X}{color_rgb[1]:02X}{color_rgb[2]:02X}"`
      - Append shading element to tcPr
      
      **Function: `set_cell_border(cell, **kwargs)`**:
      - Accept kwargs: `top`, `bottom`, `left`, `right` (color hex strings)
      - Get or add `tcPr`, create `w:tcBorders` element
      - For each border side provided, create `w:<side>` element with `val="single"`, `sz="4"`, `color=<value>`
      - Append borders to tcPr
      
      **Function: `format_value_as_text(value) -> str`**:
      - Handle None → ""
      - Handle int/float → str(value)
      - Handle list → join with " | "
      - Handle dict → join values with " | "
      - Handle str → strip and normalize newlines
      - Return cleaned string
      
      **Function: `add_bulleted_lines(paragraph, text: str)`**:
      - Split text by newlines
      - For each non-empty line:
        - If line starts with "- " or "• ", strip prefix
        - Add run with "• " + line text
        - Set font: Arial 8.5pt
      - This creates bullet point rendering for multi-line text
      
      **Function: `create_vertical_table(doc, data_dict: dict, title: str) -> Table`**:
      - Create table with len(data_dict) rows, 2 columns
      - Set column widths: [4000 twips, 11038 twips] (total 15038 for landscape)
      - For each key-value pair:
        - Row cell 0 (label): Set background to BORDEAUX_RGB, text white bold, centered
        - Row cell 1 (value): Format as text with bullets if multi-line, left-aligned
        - Set all borders visible (gray)
      - Return table object
      
      **Function: `create_horizontal_table(doc, data_list: list, title: str) -> Table`**:
      - IMPORTANT: Tables 2-6 are NOT lists - they are single-key dicts like `{"Intitule": "text"}`
      - This function handles the single-column format for tables 2-6
      - Create table with 2 rows (header + content), 1 column
      - Set column width: 15038 twips (full landscape width)
      - Header row: Background BORDEAUX_RGB, white bold text with the key name (e.g., "Intitule")
      - Content row: Parse value text for bullet points (lines starting with "- " or containing "\n")
      - Use `add_bulleted_lines()` for multi-line content
      - Set borders visible
      - Return table object
      
      **Function: `generate_word_document(json_data: dict, output_path: Path, software: str, footer: str)`**:
      - Create Document() object
      - Configure page:
        - Landscape orientation: `section.orientation = WD_ORIENT.LANDSCAPE`
        - Page width/height: Swap for landscape (11906 x 16838 twips)
        - Set margins: top=1200, bottom=1100, left=900, right=900
      - Setup header:
        - Add paragraph to section.header
        - Text: f"{software} - Frap" (or use Etape de mission from table 1)
        - Font: Arial bold, color BORDEAUX_RGB, centered
        - Add bottom border (bordeaux line)
      - Setup footer:
        - Add paragraph to section.footer
        - Text: footer text (WhatsApp contact)
        - Font: Arial, color BORDEAUX_RGB, centered
        - Add top border (bordeaux line)
      - Extract tables from JSON:
        - Find key containing "Etape mission -" (e.g., "Etape mission - Frap")
        - Get list of table dictionaries
        - Validate: must have "table 1" through at least "table 2"
      - Process table 1 (metadata):
        - Call `create_vertical_table(doc, table1_data, "Métadonnées")`
        - Add spacing paragraph (6pt)
      - Process tables 2-6 (content):
        - For each table N (N=2 to 6):
          - Extract single key-value pair (e.g., {"Intitule": "text"})
          - Call `create_horizontal_table(doc, table_data, key_name)`
          - Add spacing paragraph (6pt) between tables
      - Save document to output_path
      
      **Function: `main()`**:
      - Setup argparse:
        - Positional: `json_file` (required)
        - Optional: `-o/--output-dir` (default: "./sortie_word_cas14")
        - Optional: `--software` (default: DEFAULT_SOFTWARE)
        - Optional: `--footer` (default: DEFAULT_FOOTER)
      - Read JSON file with UTF-8 encoding
      - Parse with `extract_json_from_text()`
      - Extract reference from table 1 or generate with `generate_reference()`
      - Extract "Etape de mission" from table 1
      - Generate timestamp: `datetime.now().strftime("%Y%m%d_%H%M%S")`
      - Build filename: f"{reference}-{etape_de_mission}- {software}_{timestamp}.docx"
      - Sanitize filename (remove invalid chars: `/:*?"<>|`)
      - Create output directory if not exists
      - Call `generate_word_document()`
      - Print success message with filename and path
      - Handle exceptions: JSONDecodeError, KeyError, IOError, python-docx errors
      
      **Files**: `h:\Projet_pdf_excel\Modelisation claude skill\Cas_14\json2word_frap.py`
      
      **Verify**: Run `python json2word_frap.py exemple_frap_minimal.json` and confirm:
      - Document generated successfully
      - Opens in Word without errors
      - Orientation is landscape
      - 6 tables present (1 vertical + 5 horizontal single-column)
      - Table 1 column 1 has bordeaux background (#8B0000)
      - Header shows "Logiciel automatisé E-audit pro - Frap" in bordeaux
      - Footer shows WhatsApp contact centered in bordeaux
      - Filename matches format with timestamp

---

- [ ] 2. **Create `execute_cas14_production.py` - Orchestrator script (Phase 2.2)**
      
      Create the orchestrator script at `h:\Projet_pdf_excel\Modelisation claude skill\Cas_14\execute_cas14_production.py` following the pattern from Cas 2's `execute_cas2_production.py`.
      
      **Implementation approach**:
      
      **Import section**:
      - `requests`, `json`, `subprocess`, `sys`
      - `pathlib.Path`, `datetime`
      
      **Configuration constants**:
      - `WEBHOOK_URL = "http://localhost:5678/webhook/skill_frap_cas14"`
      - `OUTPUT_DIR = Path("./sortie_word_cas14")`
      - `TEMP_DIR = Path("./temp_frap_cas14")`
      - `DATA_DIR = Path("./data_json_from_n8n_cas14")`
      - `TIMEOUT = 30` (seconds)
      
      **Function: `log(message: str, level: str = "INFO")`**:
      - Print formatted log with timestamp: `[YYYY-MM-DD HH:MM:SS] [LEVEL] message`
      - Levels: INFO, SUCCESS, WARNING, ERROR
      - Use different prefixes: ✅ for SUCCESS, ❌ for ERROR, ⚠️ for WARNING
      
      **Function: `call_n8n_api(url: str, method: str = "POST", timeout: int = 30) -> dict | None`**:
      - Log the API call (URL, method)
      - Make HTTP request with `requests.post(url, json={}, timeout=timeout)` or `requests.get()`
      - Handle exceptions:
        - `requests.exceptions.Timeout` → log timeout error, return None
        - `requests.exceptions.ConnectionError` → log connection error with hint to start N8N, return None
        - `requests.exceptions.HTTPError` → log HTTP error, return None
        - `json.JSONDecodeError` → log JSON parsing error, return None
      - On success: log status code, return response.json()
      
      **Function: `extract_data_integrale(response) -> list | None`**:
      - Handle two cases:
        1. Response is list: `response[0]["Data_integrale"]`
        2. Response is dict: `response["Data_integrale"]`
      - Check for nested structure: if `data[0]["Data_integrale"]` exists, extract that level
      - Log number of FRAP elements found
      - Return list of FRAP objects or None
      
      **Function: `save_full_response(data, data_dir: Path) -> Path | None`**:
      - Create data_dir if not exists
      - Generate timestamp: `YYYYMMDD_HHMMSS`
      - Filename: `reponse_api_{timestamp}.json`
      - Write JSON with `json.dump(data, f, ensure_ascii=False, indent=2)`
      - Use UTF-8 encoding
      - Log saved filepath
      - Return filepath or None on error
      
      **Function: `process_frap(data_integrale: list, output_dir: Path, temp_dir: Path, ref_prefix: str = "FRAP", software: str = DEFAULT_SOFTWARE) -> int`**:
      - Create output_dir and temp_dir if not exist
      - Initialize success counter
      - Get path to json2word_frap.py script (same directory as this script)
      - Verify script exists
      - Loop through each FRAP in data_integrale with enumerate (idx starting at 1):
        - Log progress: "FRAP {idx}/{total}"
        - Save FRAP to temp file: `temp_dir / f"frap_{idx}.json"`
        - Write with UTF-8 encoding, indent=2
        - Generate timestamp for reference: `datetime.now().strftime("%Y%m%d_%H%M%S")`
        - Build reference: f"{ref_prefix}-{idx:02d}" (no timestamp in reference, only in filename)
        - Build command: `["python", script_path, temp_file, "-o", output_dir, "--software", software]`
        - Note: Reference is embedded in table 1 of JSON, not passed as CLI arg
        - Execute with `subprocess.run(cmd, capture_output=True, text=True, timeout=120, encoding='utf-8')`
        - Check returncode: 0 = success (increment counter, log success), else log error with stderr
        - Handle TimeoutExpired exception
      - Return success count
      
      **Function: `main() -> int`**:
      - Force UTF-8 encoding for Windows console: `sys.stdout.reconfigure(encoding='utf-8')`
      - Print banner:
        ```
        ═══════════════════════════════════════════════════════
           🎯 EXECUTION SKILL CAS 14 : FRAP / RECOS (PRODUCTION)
        ═══════════════════════════════════════════════════════
        ```
      - Record start time
      - **STEP 1**: Call N8N API
        - Print section header
        - Call `call_n8n_api(WEBHOOK_URL, "POST", TIMEOUT)`
        - If None, log error and exit with code 1
        - Save full response with `save_full_response()`
        - Extract data_integrale with `extract_data_integrale()`
        - If None or empty, log error and exit with code 1
      - **STEP 2**: Execute skill
        - Print section header
        - Call `process_frap(data_integrale, OUTPUT_DIR, TEMP_DIR, "FRAP", DEFAULT_SOFTWARE)`
      - **SUMMARY**:
        - Calculate duration
        - Print summary:
          ```
          ═══════════════════════════════════════════════════════
             📊 RÉSUMÉ FINAL
          ═══════════════════════════════════════════════════════
          Total traités : N
          Succès : N
          Échecs : N
          Taux de succès : X%
          Dossier de sortie : <path>
          Durée totale : X.X secondes
          ```
        - List generated Word files from OUTPUT_DIR
        - Return 0 if all succeeded, 1 if some/all failed
      
      **Entry point**:
      - `if __name__ == "__main__": sys.exit(main())`
      - Handle KeyboardInterrupt: print "Workflow interrompu", exit 130
      - Handle generic Exception: print traceback, exit 1
      
      **Files**: `h:\Projet_pdf_excel\Modelisation claude skill\Cas_14\execute_cas14_production.py`
      
      **Verify**: 
      - Prerequisites: N8N must be running with webhook configured at `http://localhost:5678/webhook/skill_frap_cas14`
      - Run `python execute_cas14_production.py`
      - Confirm:
        - API called successfully (200 OK)
        - Data_integrale extracted
        - Each FRAP processed
        - Word documents generated in `sortie_word_cas14/`
        - Full response saved to `data_json_from_n8n_cas14/reponse_api_<timestamp>.json`
        - Summary shows success count and list of files

---

- [ ] 3. **Test with minimal JSON example**
      
      Verify the complete workflow with the minimal example to ensure all components work together.
      
      **Test steps**:
      - Activate conda environment: `conda activate pdf_excel_env`
      - Navigate to: `cd "h:\Projet_pdf_excel\Modelisation claude skill\Cas_14"`
      - Run converter directly: `python json2word_frap.py exemple_frap_minimal.json`
      - Expected output:
        - Success message printed
        - File created: `sortie_word_cas14/FRAP-TEST-01-Frap- Logiciel automatisé E-audit pro_<timestamp>.docx`
      - Open generated document in Word
      - Manual validation checklist:
        - ✅ Opens without errors
        - ✅ Orientation is landscape
        - ✅ Header: "Logiciel automatisé E-audit pro - Frap" in bordeaux (#8B0000)
        - ✅ Footer: WhatsApp contact centered in bordeaux
        - ✅ Table 1: 2 columns, vertical format, column 1 bordeaux background with white text
        - ✅ Table 1: Contains "Etape de mission", "Norme", "Méthode", "Reference"
        - ✅ Tables 2-6: Single column each with bullet points
        - ✅ Table 2: "Intitule" header
        - ✅ Table 3: "Observation" header
        - ✅ Table 4: "Constat" header with bullet points
        - ✅ Table 5: "Risque" header with bullet points
        - ✅ Table 6: "Recommendation" header with bullet points
        - ✅ All text is readable (Arial 8.5pt)
        - ✅ Filename format correct with timestamp
      
      **Files**: Validation log (can be manual notes)
      
      **Verify**: All checklist items pass; document is production-ready

---

- [ ] 4. **Test with complete JSON example**
      
      Verify handling of multiple FRAP entries with the complete example (3 FRAP entries).
      
      **Test steps**:
      - Navigate to: `cd "h:\Projet_pdf_excel\Modelisation claude skill\Cas_14"`
      - Run converter: `python json2word_frap.py exemple_frap_complet.json`
      - Expected: Should generate 1 document with the first FRAP (script processes one JSON file = one FRAP structure)
      - Note: The orchestrator (`execute_cas14_production.py`) handles multiple FRAPs from N8N response
      - For testing multiple FRAPs locally, would need to split `exemple_frap_complet.json` or use the orchestrator
      - Validate generated document has same quality as minimal test
      - Check that longer text content (in Observation, Constat, Risque, Recommendation) renders correctly with:
        - Proper line wrapping
        - Bullet points preserved
        - No text truncation
        - Tables fit on landscape page
      
      **Files**: Generated Word document(s)
      
      **Verify**: Document quality maintained with longer/more complex content; no layout issues

---

- [ ] 5. **Code quality and documentation review**
      
      Ensure both scripts meet professional standards before finalization.
      
      **Review checklist**:
      
      **For `json2word_frap.py`**:
      - ✅ Module-level docstring with description, usage, dependencies
      - ✅ All functions have docstrings with Args/Returns
      - ✅ Consistent code formatting (4-space indentation)
      - ✅ Meaningful variable names (no single letters except loop counters)
      - ✅ Error handling: try-except blocks for file I/O, JSON parsing, docx operations
      - ✅ UTF-8 encoding specified for all file operations
      - ✅ Constants in UPPER_CASE at module level
      - ✅ Type hints for function parameters and returns
      - ✅ Comments explaining complex logic (especially XML manipulation for borders/colors)
      
      **For `execute_cas14_production.py`**:
      - ✅ Module-level docstring with workflow description
      - ✅ All functions have docstrings
      - ✅ Comprehensive error handling for API calls
      - ✅ UTF-8 encoding for Windows console output
      - ✅ Informative log messages at each step
      - ✅ Progress indicators (e.g., "FRAP 1/3")
      - ✅ Final summary with statistics
      - ✅ Proper exit codes (0=success, 1=failure, 130=interrupt)
      
      **Common**:
      - ✅ No hardcoded absolute paths (use Path and relative paths)
      - ✅ No commented-out debug code
      - ✅ No `print()` for debugging (use proper logging or remove)
      - ✅ Consistent string quotes (prefer double quotes for user-facing strings)
      
      **Files**: Both Python scripts
      
      **Verify**: Code passes manual review; ready for production use

---

## Key Decisions and Rationale

### Decision 1: Bordeaux Color #8B0000 vs #7B1E3A
**Context**: Cas 2/3/6 use #7B1E3A for headers; spec for Cas 14 specifies #8B0000.  
**Decision**: Use #8B0000 (RGB 139, 0, 0) exclusively for Cas 14.  
**Rationale**: The skill.md specification explicitly states "Couleur en-têtes de tableau: (139, 0, 0) #8B0000" and "Colonne 1 Table 1: (139, 0, 0) #8B0000". This is documented as the unique color for Cas 14 in the FRAP context. Following spec exactly ensures consistency with user expectations and documentation.

### Decision 2: Tables 2-6 as Single-Column Format
**Context**: Tables 2-6 in JSON are dicts like `{"Intitule": "text"}`, not lists of objects.  
**Decision**: Render tables 2-6 as single-column tables (header row + content row).  
**Rationale**: The JSON structure shows single key-value pairs, and the spec says "Format 1: Dictionnaire à clé unique (rendu: tableau 1 colonne)". Unlike Cas 2/3/6 which have multi-column grids, Cas 14's content tables are simpler single-column layouts with bullet-point content.

### Decision 3: Reference in Filename but Not CLI Arg
**Context**: Filename format requires `<Reference>-<Etape_de_mission>-...`.  
**Decision**: Extract reference from table 1 in JSON; don't pass as separate CLI argument.  
**Rationale**: The orchestrator saves each FRAP's complete JSON to a temp file. The reference is already embedded in table 1 of that JSON. Passing it separately would create redundancy and risk of mismatch. The converter extracts it from table 1, generates "AUTO" if missing.

### Decision 4: Bullet Point Rendering
**Context**: Tables 4-6 contain multi-line text with "- " prefixes or "\n" separators.  
**Decision**: Implement `add_bulleted_lines()` function to parse and render as "• " bullets.  
**Rationale**: The spec states "Tables 2+: Format adapté au contenu" and shows examples with bullet points. Text containing "\n" or starting with "- " should be rendered as visual bullets for better readability. This matches the pattern in other Cas implementations.

### Decision 5: Timestamp in Filename Only
**Context**: Need unique filenames for multiple FRAP documents.  
**Decision**: Add timestamp suffix to filename: `<Reference>-<Etape>- <Software>_YYYYMMDD_HHMMSS.docx`.  
**Rationale**: The spec shows "Exemples: FRAP-BK-A10-01-Frap- Logiciel automatisé E-audit pro_20261031_143022.docx". Timestamp ensures uniqueness when processing multiple FRAPs with same reference, and allows chronological sorting. Format matches the pattern from the spec examples.

### Decision 6: Landscape Orientation Enforced
**Context**: Constraint: "Orientation: Paysage (A4)".  
**Decision**: Set `section.orientation = WD_ORIENT.LANDSCAPE` and swap page dimensions.  
**Rationale**: Landscape provides sufficient width for readable tables, especially table 1 with two columns. This is mandatory per spec. All other Cas also use landscape for tabular audit documents.

---

## Dependencies and Prerequisites

**Python version**: >= 3.9  
**Conda environment**: `pdf_excel_env` (must be activated)  
**Python packages** (from environment.yml):
- `python-docx >= 1.1.0` - Document generation
- `requests >= 2.28.0` - API calls (for orchestrator)

**External services** (for orchestrator only):
- N8N running on `http://localhost:5678`
- Webhook configured at `/webhook/skill_frap_cas14`
- Webhook must return JSON with `Data_integrale` array

**Files required**:
- `audit-frap-recos-json2word.skill.md` - Full specification
- `exemple_frap_minimal.json` - Test data
- `exemple_frap_complet.json` - Extended test data

---

## Success Criteria

1. ✅ `json2word_frap.py` executes without errors on minimal JSON
2. ✅ Generated document opens in Word without errors or warnings
3. ✅ Document orientation is landscape (validated by opening in Word)
4. ✅ Table 1 has 2 columns; column 1 has bordeaux background (#8B0000)
5. ✅ Tables 2-6 present with single-column format and bullet points
6. ✅ Header shows "Logiciel automatisé E-audit pro - Frap" in bordeaux
7. ✅ Footer shows WhatsApp contact centered in bordeaux
8. ✅ Filename follows format: `<Reference>-<Etape>- <Software>_<timestamp>.docx`
9. ✅ `execute_cas14_production.py` successfully calls N8N webhook
10. ✅ Orchestrator processes multiple FRAPs and generates separate documents
11. ✅ All generated files listed in summary output
12. ✅ Code is clean, documented, and follows Python best practices

---

## Notes

- **Unique to Cas 14**: The bordeaux color #8B0000 (RGB 139, 0, 0) is specific to FRAP documents; other Cas use #7B1E3A. This is not a mistake—it's documented in the spec as the FRAP brand color.
  
- **Table structure difference**: Unlike Cas 2/3/6 which have multi-column data grids in table 2, Cas 14 uses a simpler structure: table 1 is metadata (vertical 2-column), and tables 2-6 are single-column content tables. This reflects the nature of FRAP documents (narrative analysis vs. structured procedures).

- **Filename format**: The spec shows a space before "Logiciel" in the filename pattern: `<Reference>-<Etape>- Logiciel...` (note the space after the dash). This quirk should be preserved to match the documented format exactly.

- **Bullet point handling**: The JSON examples show text with "- " prefixes and "\n" separators. The converter should intelligently detect these patterns and render them as proper bullets ("• ") in Word for visual consistency.

- **Error resilience**: The orchestrator should continue processing remaining FRAPs even if one fails, providing a complete summary at the end. This ensures maximum throughput in production scenarios.

- **UTF-8 encoding**: Windows console output requires explicit UTF-8 reconfiguration. All file I/O must specify `encoding='utf-8'` to handle French accented characters correctly.

---

**Plan created**: 2026-11-01  
**Target completion**: After implementation by coding agent  
**Phase 1 artifacts**: Documentation in `Cas_14/` directory  
**Phase 2 artifacts**: `json2word_frap.py` and `execute_cas14_production.py` in `Cas_14/` directory
