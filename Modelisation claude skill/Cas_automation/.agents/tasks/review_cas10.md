# Cas 10 automation implementation with hierarchical design modeling

Implementation adds Cas 10 automation endpoint to the Flask server, wrapping the existing Cas 2 converter with new logic to parse, extract, and render hierarchical design specifications from the JSON input. The design section gets its own styled tables appended to the generated Word document. File naming follows the Cas10_YYYYMMDD_HHMMSS pattern, endpoints are wired into the server, and test infrastructure verifies document generation.

**Watch for:** No blocking concerns. The implementation is clean, follows established patterns, and avoids emojis. Design table styling matches the E-audit pro charter (bordeaux/white/gray hierarchy). The modelisation design extraction happens before the generic converter runs, preventing it from being treated as a mission table.

**Verdict**: APPROVED

## High-level view

The core script imports the Cas 2 generic converter, extracts the `[Modélisation design]` section from the JSON payload, strips it from the mission data, generates the base document via `convert()`, then reopens the document to append styled design tables. Each design table presents a 2-column layout (Niveau | Colonnes/Sous-groupes) with color-coded rows: bordeaux for Niveau 1, light bordeaux for Niveau 2, light gray for Niveau 3, white for Niveau 4. Branching structures (Design 5 with list-valued Niveau 2) receive special handling that renders branches and their associated columns.

The server wiring follows the established pattern: POST endpoint at `/automation/cas_10`, GET test endpoint at `/automation/test/10`, with both routes delegating to `run_python_script` using `use_dash_o=False` and `cas_number=10`. File renaming to `Cas10_YYYYMMDD_HHMMSS.docx` happens in the subprocess runner after document generation completes.

The test script mirrors Cas 8 test structure, checking for the presence of a `Cas10_*.docx` file in Downloads and validating minimum file size (40 KB threshold, more permissive than Cas 6/8 due to variable design content).

<details>
<summary>Issues (0)</summary>

No blocking issues identified.

</details>

<details>
<summary>Details</summary>

## Design extraction and data flow

The `parse_modelisation_design()` function walks the JSON structure to locate the `[Modélisation design]` item, which sits in the mission data list alongside the actual tables. It searches for the top-level "Etape mission - ..." key, iterates through the list value, and returns the design dictionary when found. After extraction, the main function filters out the design item from the mission data before passing it to `convert()`, ensuring the generic converter only sees mission tables.

This two-phase approach (extract design, filter it out, convert, reopen and append) avoids polluting the Cas 2 converter with Cas 10-specific logic. The converter remains generic; design rendering is entirely localized to Cas 10.

## Hierarchical table rendering with color coding

`build_design_section_tables()` iterates through each table cible and design specification, constructing a 2-column table for each design. The color hierarchy matches the E-audit pro charter:

- **Niveau 1**: bordeaux background (#7B1E3A), white text, bold
- **Niveau 2**: light bordeaux (#C4A4B0), black text, bold
- **Niveau 3**: light gray (#F2F2F2), black text, normal weight
- **Niveau 4**: white background, black text, italic

The function distinguishes between linear designs (Niveau 2 is a string) and branching designs (Niveau 2 is a list). For branching designs (Design 5), Niveau 2 cells render the branch names separated by pipes, and subsequent rows render each branch's columns under Niveau 3. For linear designs, each nivel occupies a single row with the nivel label in column 1 and the column names or grouping label in column 2.

A "Colonnes couvertes" row appears at the bottom of each design table, listing all columns that participate in the design. This row uses light gray shading.

## Server endpoint wiring and test route inclusion

The server adds `/automation/cas_10` as a POST endpoint that follows the established pattern: extract JSON from request body, write to temporary file, invoke `run_python_script()` with `use_dash_o=False` and `cas_number=10`, clean up temp file, return JSON response with filename and path. The test route `/automation/test/<int:cas>` now accepts 10 in its validation list and delegates to the POST endpoint via `app.test_client()`.

The health endpoint reports `cas_10: CAS_10_AVAILABLE` in the capabilities object, and the root endpoint lists `cas_10` in the endpoints dictionary. The script path check at module level ensures `CAS_10_AVAILABLE` is set based on file existence, which gates the endpoint and prevents 503 errors when the script is missing.

## File naming and subprocess management

The `run_python_script()` function receives `cas_number=10` and delegates renaming to `rename_to_short_name()`, which generates `Cas10_YYYYMMDD_HHMMSS.docx` via `generate_short_filename()`. The renaming happens after the subprocess completes and after a 0.5-second sleep to allow Word to release the file handle. If renaming fails, the function returns the original path rather than raising an exception.

The subprocess invocation uses `sys.executable` to ensure the correct Python interpreter runs, sets `PYTHONIOENCODING=utf-8` in the environment to suppress emoji-related encoding errors on Windows, and applies a 120-second timeout. The `encoding='utf-8', errors='replace'` arguments to `subprocess.run()` prevent crashes when the subprocess outputs non-ASCII characters.

## Test script validation strategy

The test script counts `Cas10_*.docx` files in Downloads before and after subprocess execution, identifies the newest file by modification time, and validates that its size exceeds 40 KB. The 40 KB threshold is lower than the Cas 6/8 threshold (50 KB) to accommodate variable design content: a minimal JSON with few designs produces a smaller document than a full mission with multiple designs.

The script uses `encoding='utf-8', errors='replace'` when invoking the subprocess to match the server's strategy, ensuring test output doesn't crash on emoji or non-ASCII characters even though the script itself produces none.

## No emoji in output

All print statements and comments use plain ASCII. The success message in `json2word_cas10_automation.py` reads "Document cree : {filename}" without checkmarks or other emoji. Docstrings and error messages in the server and test scripts are emoji-free. The only emoji risk was in the success print, which the implementation replaced with plain text.

</details>

---

<details>
<summary>File map</summary>

**Modified:**

- `server_automation.py` — Added `/automation/cas_10` POST endpoint, extended `/automation/test/<cas>` to accept 10, updated health and root endpoints to advertise cas_10 availability
- `test_cas10_automation.py` — Test script that validates Cas10_*.docx generation using the standard JSON, checking filename pattern and minimum 40 KB size

**Added:**

- `Cas_10_automation/__init__.py` — Package marker with module-level docstring
- `Cas_10_automation/json2word_cas10_automation.py` — Main script that extracts `[Modélisation design]`, invokes Cas 2 converter, reopens document, appends color-coded design tables, saves as Cas10_YYYYMMDD_HHMMSS.docx

</details>
