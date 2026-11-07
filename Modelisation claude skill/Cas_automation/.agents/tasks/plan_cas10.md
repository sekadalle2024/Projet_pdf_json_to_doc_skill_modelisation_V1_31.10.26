# Implementation Plan - Cas 10 Automation Endpoint

## Context
Based on exploration of the codebase:
- **Base framework**: Cas 10 extends Cas 8 (Programme de travail) which uses the generic converter from Cas_2/json2word_audit.py
- **New feature**: Hierarchical [Modélisation design] section with 5 designs for table 2
- **Server structure**: Flask server in server_automation.py handles endpoints for Cas 6, 7, 8
- **Output location**: C:\Users\LEADER\Downloads (DOWNLOADS_DIR)
- **Encoding constraint**: No emojis - Windows cp1252 encoding
- **Testing pattern**: test_cas6_v3.py shows the standard test structure

## Key Design Decisions

**Decision 1: Modélisation design rendering strategy**
The [Modélisation design] section will be rendered as a visual summary at the end of the Word document, after the main table 2. Each design will be displayed as a separate Word table showing the hierarchical structure with color-coded levels (bordeaux #7B1E3A for level 1, lighter shades for deeper levels). This provides a clear visual representation of how columns are organized without modifying the main table.

**Decision 2: Script architecture**
Follow the Cas 8 pattern: create json2word_cas10_automation.py that imports and extends json2word_audit.py's convert() function. Add a post-processing step to append the Modélisation design section before the final paragraph. This minimizes code duplication and leverages the proven Cas 2 base.

**Decision 3: Hierarchical formatting approach**
Design 5 has a branching structure (Niveau 2 splits into "Preuve" and "Responsabilité et calendrier"). We'll detect this by checking if [Niveau 2] is a list. If so, create sub-columns under each branch name. Use nested tables or merged cells to show the hierarchy visually.

**Decision 4: Module organization**
Create Cas_10_automation/ subdirectory to mirror the pattern implied by the requirement to "copy specific skill versions into sub-folders by case". This keeps the automation-specific version isolated from any agent-manipulated version.

## Implementation Steps

- [ ] 1. Create the Cas_10_automation directory structure
      Create the subdirectory and __init__.py file to establish the module.
      Files: h:\Projet_pdf_excel\Modelisation claude skill\Cas_automation\Cas_10_automation\__init__.py
      Verify: `python -c "import sys; sys.path.append(r'h:\Projet_pdf_excel\Modelisation claude skill\Cas_automation'); from Cas_10_automation import json2word_cas10_automation; print('Import OK')"` - no import errors

- [ ] 2. Create json2word_cas10_automation.py with Modélisation design parsing
      Copy Cas_8/json2word_programme_travail.py as base. Add parse_modelisation_design(json_data) function that extracts the [Modélisation design] dictionary from the third item in the mission list. Add create_design_table(doc, design_name, design_spec) function that creates a Word table for one design with hierarchical formatting (4 levels max: Niveau 1 = bordeaux #7B1E3A white text bold, Niveau 2 = light bordeaux #C4A4B0 black text bold, Niveau 3 = light gray #F2F2F2 black text, Niveau 4 = white background italic). Handle Design 5's branching by checking if [Niveau 2] is a list - if so, create two sub-groups. Accept arguments: <json_file> [output_dir]. Output to C:\Users\LEADER\Downloads by default. Filename format: Cas10_YYYYMMDD_HHMMSS.docx.
      Files: h:\Projet_pdf_excel\Modelisation claude skill\Cas_automation\Cas_10_automation\json2word_cas10_automation.py
      Verify: `python h:\Projet_pdf_excel\Modelisation claude skill\Cas_automation\Cas_10_automation\json2word_cas10_automation.py "h:\Projet_pdf_excel\Modelisation claude skill\Cas_automation\json standard\Json_standard_[Cas 10].txt"` - creates Cas10_*.docx in Downloads, file size > 50KB, contains 3+ tables (table 1, table 2, design tables)

- [ ] 3. Add Cas 10 endpoint to server_automation.py
      Add CAS_10_SCRIPT constant pointing to Cas_10_automation/json2word_cas10_automation.py. Add CAS_10_AVAILABLE boolean check. Add route @app.route('/automation/cas_10', methods=['POST']) following the cas_8 pattern (use_dash_o=False, cas_number=10). Update test_cas() route to accept cas=10. Update health_check() to include 'cas_10' in capabilities. Update index() to list cas_10 endpoint.
      Files: h:\Projet_pdf_excel\Modelisation claude skill\Cas_automation\server_automation.py
      Verify: `python h:\Projet_pdf_excel\Modelisation claude skill\Cas_automation\server_automation.py` starts without errors, then `curl http://localhost:5000/health` shows "cas_10": true in capabilities

- [ ] 4. Test the Cas 10 endpoint via HTTP
      Start server_automation.py in background. Send POST request to /automation/cas_10 with Json_standard_[Cas 10].txt content. Verify response contains success: true, filename, and path. Open the generated .docx file and verify: A4 landscape, bordeaux header, table 1 (vertical), table 2 (40 rows × 15 columns), Modélisation design section with 5 separate tables showing hierarchies. Stop server.
      Files: (no new files, verification only)
      Verify: `Start-Process python -ArgumentList "h:\Projet_pdf_excel\Modelisation claude skill\Cas_automation\server_automation.py" -NoNewWindow` then `Invoke-WebRequest -Uri http://localhost:5000/automation/test/10 -Method GET` returns 200 OK, check Downloads folder for new Cas10_*.docx file

- [ ] 5. Create test_cas10_automation.py
      Create standalone test script following test_cas6_v3.py pattern. Test direct script execution (not HTTP). Count files before execution. Run json2word_cas10_automation.py with Json_standard_[Cas 10].txt. Verify new file created, size > 50KB. Use python-docx to count tables (expect 7+: 1 table 1 + 1 table 2 + 5 design tables). Print first cell of each table for verification. Handle Windows cp1252 encoding. No emojis in output.
      Files: h:\Projet_pdf_excel\Modelisation claude skill\Cas_automation\test_cas10_automation.py
      Verify: `python h:\Projet_pdf_excel\Modelisation claude skill\Cas_automation\test_cas10_automation.py` - exits with code 0, prints "SUCCESS", shows 7+ tables detected, new Cas10_*.docx file appears in Downloads

## Verification Commands

All verification uses the actual Python environment and project structure discovered during exploration:
- **Import test**: `python -c "import sys; sys.path.append(r'h:\Projet_pdf_excel\Modelisation claude skill\Cas_automation'); from Cas_10_automation import json2word_cas10_automation"`
- **Direct script test**: `python h:\Projet_pdf_excel\Modelisation claude skill\Cas_automation\Cas_10_automation\json2word_cas10_automation.py "h:\Projet_pdf_excel\Modelisation claude skill\Cas_automation\json standard\Json_standard_[Cas 10].txt"`
- **Server health check**: `Invoke-WebRequest -Uri http://localhost:5000/health | ConvertFrom-Json`
- **HTTP endpoint test**: `Invoke-WebRequest -Uri http://localhost:5000/automation/test/10 -Method GET`
- **Standalone test**: `python h:\Projet_pdf_excel\Modelisation claude skill\Cas_automation\test_cas10_automation.py`

## Design Structure Reference

The JSON contains 5 designs for table 2:

1. **Design 1 - Cycle par sous-processus**: 4 levels (Cycle par sous-processus > Cycle > Processus > Sous-processus)
2. **Design 2 - Risque et assertion**: 3 levels (Risque et assertion à couvrir > Risque > Assertion)
3. **Design 3 - Evaluation des risques**: 4 levels (Evaluation des risques par criticité > Probabilité > Impact > Criticité brute)
4. **Design 4 - Contrôle et objectif**: 4 levels (Contrôle et objectif d'audit > Point de contrôle > Contrôle audit > Objectif de contrôle)
5. **Design 5 - Preuve et responsabilité**: Branching structure with Niveau 2 split into "Preuve" (Document, X-ref) and "Responsabilité et calendrier" (Propriétaire du contrôle, Périodicité)

## Notes

- The Modélisation design section is informational/documentary - it describes how columns in table 2 are logically organized into hierarchies
- Each design table should be self-contained with its own headers and hierarchy visualization
- Color scheme: Niveau 1 = #7B1E3A (white text), Niveau 2 = #C4A4B0 (black text), Niveau 3 = #F2F2F2 (black text), Niveau 4 = white (italic black text)
- Design 5 requires special handling for the branching at Niveau 2 - the structure is: Niveau 1 > [Preuve, Responsabilité et calendrier] > {Preuve: [Document, X-ref], Responsabilité et calendrier: [Propriétaire du contrôle, Périodicité]}
- Windows encoding cp1252 means no emojis anywhere in Python source or output
- Output files always go to C:\Users\LEADER\Downloads with timestamp-based naming
