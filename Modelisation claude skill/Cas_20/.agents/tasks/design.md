# Technical Design: Cas 20 - Modelisation Design Audit

## Overview

Cas 20 implements a dynamic audit design modeling system that generates Word, Excel, PDF, and JSON documents with **grouped horizontal headers** (Level 1 headers spanning multiple Level 2/3/4 base columns). Unlike simple JSON-to-Word converters, this case handles complex hierarchical column structures with colspan/rowspan rendering and supports both predefined design patterns and LLM-driven "auto mode" for flexible design generation.

The implementation adapts the native Claude skill `render_design.py` into a standardized skill following the 9-phase TODO_IMPLEMENTATION_CAS_X.md workflow. The core challenge is preserving the native skill's sophisticated header matrix algorithm while integrating it into the project's established orchestration, automation, and n8n webhook patterns.

---

## 1. JSON Structure and Data Model

### 1.1 Input JSON Format (Formatage data Type 1)

The JSON follows a two-table structure with design modeling hierarchy:

```json
{
  "Etape mission - [Nom étape]": [
    {
      "table 1": {
        "Etape de mission": "Cartographie des risques",
        "Document": "Cartographie design avec regroupements",
        "Processus": "...",
        "Cycle d'activité": "...",
        "Méthodologie": "...",
        "Reference": "CR010",
        "Version": "...",
        "Etablissement": "...",
        "Date d'élaboration": "...",
        "Modélisation design": "[Cycle par sous processus], [Evaluation des risques par criticité]"
      }
    },
    {
      "table 2": [
        {
          "no": 1,
          "Cycle par sous processus": {
            "Cycle": "Cycle commercial",
            "Processus": "Ventes",
            "Tâche clé": "Facturation",
            "Opérationnel": "Émission facture",
            "Document": "Facture"
          },
          "Evaluation des risques par criticité": {
            "Probabilité": "Moyen (2)",
            "Impact": "Élevé (3)",
            "Criticité brute": "Élevé (6)"
          }
        }
      ]
    }
  ]
}
```

**Key characteristics:**
- **table 1**: vertical metadata dictionary (displayed as 2-column table)
- **table 2**: array of records where:
  - Scalar values = pivot columns (e.g., "no")
  - Object values = Level 1 grouped headers with nested columns
  - Nested objects = up to 3-4 levels of hierarchy
- Design names in table 1's `Modélisation design` field guide header rendering

### 1.2 Header Tree Structure

The native `render_design.py` builds a header tree from table 2 rows:

1. **Tree building** (`build_tree`): merge all row structures into a unified tree
2. **Leaf extraction** (`leaves`): identify all terminal columns (paths)
3. **Matrix generation** (`header_matrix`): produce (depth, cells, paths) where cells = [(row, col, rowspan, colspan, label)]
4. **Colspan calculation**: parent span = count of leaf descendants
5. **Rowspan calculation**: columns without parents span from their level to bottom

**Example tree:**
```
Root
├─ no (pivot, rowspan=2)
├─ Cycle par sous processus (Level 1, colspan=5)
│  ├─ Cycle
│  ├─ Processus
│  ├─ Tâche clé
│  ├─ Opérationnel
│  └─ Document
└─ Evaluation des risques par criticité (Level 1, colspan=3)
   ├─ Probabilité
   ├─ Impact
   └─ Criticité brute
```

### 1.3 Validation Rules

**Pre-conversion (input validation):**
- JSON parsable and UTF-8 encoded
- Top-level key matches `"Etape mission - .*"`
- table 1 is dict with required keys: `Etape de mission`, `Reference` (or generate)
- table 2 is non-empty array
- At least one row in table 2 contains nested objects (design groups)
- No duplicate column names across all paths

**Post-conversion (output validation):**
- Document opens without error
- Orientation = landscape (width > height)
- Header/footer present and correct
- Table count = JSON table count
- table 1: 2 columns, N+1 rows (header + N metadata)
- table 2: M columns (from paths), 1 header block (depth rows) + N data rows
- Header color = #800020 (Bordeaux)
- No data loss: all JSON values appear in document
- Filename matches format: `<ref>-<Etape_de_mission>- <Nom_logiciel>_<timestamp>.docx`

---

## 2. Core Script: json2word_modelisation.py

### 2.1 Adaptation Strategy from render_design.py

**Preserve from native script:**
- `build_tree`, `leaves`, `header_matrix` functions (lines ~30-60 in render_design.py)
- `get(row, path)` function for nested value extraction
- `col_weights` for proportional column width calculation
- `level_fill` for risk level color mapping (Élevé/Moyen/Faible)
- Bordeaux color constant `#800020`
- Header fusion logic (merge cells for rowspan > 1 or colspan > 1)
- Vertical fusion for repeated pivot column values (Cycle, Processus, Sous-processus)

**Adapt for standardization:**
- Replace argparse CLI with function signature matching orchestrator needs
- Add timestamp to filename generation
- Standardize error handling (log with level, return exit codes)
- Add `COLUMN_SPECS`-style metadata for non-design columns (though less critical here since columns are dynamic)
- Integrate with project's file naming convention: `{ref}-{etape}- {software}_{timestamp}.docx`

**New functionality:**
- Auto mode support: when `[Modélisation design]` absent or `= [Mode auto]`, analyze table 2 structure and propose design groupings
- Multiple format outputs: Word (primary), JSON (pass-through), Excel, PDF from same internal structure
- Webhook-friendly: accept JSON text with embedded `Data_integrale` wrapper (extract first)

### 2.2 Function Architecture

```python
# Constants
BORDEAUX = "800020"
BORDEAUX_RGB = (0x80, 0x00, 0x20)
DEFAULT_SOFTWARE = "Logiciel automatisé E-audit pro 2.0"
FOOTER = "Automatisez vos activités d'audit, risques et contrôles - Whatsapp : + 225 05 44 13 07 98"
LEVEL_COLORS = {
    "Élevé": "FF0000", "Eleve": "FF0000",
    "Moyen": "FFFF00",
    "Faible": "00B050"
}

# Tree building (from render_design.py)
def build_tree(rows: List[Dict]) -> Dict:
    """Merge all row structures into unified tree."""
    # Implementation: recursive merge

def leaves(tree: Dict, path: Tuple = ()) -> Iterator[Tuple]:
    """Extract all leaf paths from tree."""

def header_matrix(tree: Dict) -> Tuple[int, List[Tuple], List[Tuple]]:
    """Return (depth, cells, paths) for header rendering.
    cells = [(row, col, rowspan, colspan, label), ...]
    paths = [(level1, level2, ..., leaf), ...]
    """

def get(row: Dict, path: Tuple) -> Any:
    """Navigate nested dict by path tuple."""

def col_weights(rows: List[Dict], paths: List[Tuple]) -> List[int]:
    """Calculate proportional column widths based on content."""

# Value formatting
def flat(value: Any) -> str:
    """Flatten nested structures to display string."""
    if isinstance(value, list):
        return "\n".join(flat(x) for x in value)
    if isinstance(value, dict):
        return " ; ".join(f"{k} : {flat(v)}" for k, v in value.items())
    return "" if value is None else str(value)

def level_fill(value: str) -> Optional[str]:
    """Return hex color for risk level, or None."""
    s = str(value)
    for key, color in LEVEL_COLORS.items():
        if s.startswith(key):
            return color
    return None

# JSON extraction
def extract_json_from_text(text: str) -> Dict:
    """Extract JSON from text, handling Data_integrale wrapper."""
    data = json.loads(text)
    # If wrapped in Data_integrale, unwrap
    if isinstance(data, dict) and "Data_integrale" in data:
        items = data["Data_integrale"]
        if isinstance(items, list) and len(items) > 0:
            return items[0]  # Return first element
    return data

def load(json_path_or_text: str) -> Tuple[str, Optional[Tuple], Tuple, List]:
    """Load and parse JSON, return (title, meta, main, others).
    
    meta = (name, dict) or None
    main = (name, list) - the design-modeled table
    others = [(name, content), ...] - additional tables
    """
    if Path(json_path_or_text).is_file():
        data = json.loads(Path(json_path_or_text).read_text(encoding="utf8"))
    else:
        data = extract_json_from_text(json_path_or_text)
    
    title, tables = next(iter(data.items()))
    # Identify meta (table 1), main (table 2), others
    # meta = first dict, main = first list with nested objects
    # ...
    return title, meta, main, others

# Reference generation
def generate_reference() -> str:
    """Generate ref: 2 letters + 3 digits (e.g., CR010)."""
    letters = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=2))
    digits = ''.join(random.choices('0123456789', k=3))
    return f"{letters}{digits}"

def etape_name(meta: Optional[Tuple], title: str) -> str:
    """Extract Etape de mission from meta or title."""
    if meta and "Etape de mission" in meta[1]:
        return meta[1]["Etape de mission"]
    return title.replace("Etape mission - ", "")

def safe_filename(s: str) -> str:
    """Remove filesystem-forbidden characters."""
    return re.sub(r'[\\/:*?"<>|]', "", s).strip()

# Word generation with grouped headers
def to_docx(
    path: Path,
    title: str,
    meta: Optional[Tuple],
    main: Tuple,
    others: List[Tuple],
    software: str,
    etape: str
):
    """Generate Word document with design modeling.
    
    - Landscape A4
    - Header: "{software} - {etape}", bordeaux background
    - Footer: WhatsApp contact
    - table 1: vertical (2 columns)
    - Legend table: E/M/F colors
    - table 2: grouped headers with colspan/rowspan
    - Vertical merge for repeated pivot values
    - Risk level shading
    """
    from docx import Document
    from docx.enum.section import WD_ORIENT
    from docx.shared import Cm, Pt, RGBColor
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn
    # ... (full implementation as in render_design.py)

def to_xlsx(path: Path, title: str, meta, main, others, software: str, etape: str):
    """Generate Excel with design modeling.
    
    - Sheet "Informations": vertical table 1
    - Sheet "Données": table 2 with merged header cells, freeze panes, auto filter
    - Color fills for headers and risk levels
    """
    from openpyxl import Workbook
    from openpyxl.styles import PatternFill, Font, Alignment, Border, Side
    # ...

def to_pdf(path: Path, title: str, meta, main, others, software: str, etape: str):
    """Generate PDF with reportlab.
    
    - Landscape A4
    - Table with SPAN for colspan/rowspan
    - repeatRows for header
    """
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
    from reportlab.lib.pagesizes import A4, landscape
    # ...

def generate_document(
    json_input: str,
    output_dir: str,
    formats: List[str] = ["docx"],
    software: str = DEFAULT_SOFTWARE,
    reference: str = ""
) -> List[Path]:
    """Main entry point for orchestrator.
    
    Args:
        json_input: JSON string or file path
        output_dir: Output directory path
        formats: List of formats ["docx", "xlsx", "pdf", "json"]
        software: Software name for header
        reference: File reference (generated if empty)
    
    Returns:
        List of generated file paths
    
    Raises:
        ValueError: Invalid JSON or missing required fields
        IOError: File write errors
    """
    # Load and parse
    title, meta, main, others = load(json_input)
    etape = etape_name(meta, title)
    
    # Generate reference if needed
    if not reference and meta:
        reference = meta[1].get("Reference", "")
    if not reference or not re.fullmatch(r"[A-Za-z]{1,2}\d{2,3}", reference):
        reference = generate_reference()
    
    # Create output directory
    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    base = safe_filename(f"{reference}-{etape}- {software}_{timestamp}")
    
    generated = []
    for fmt in formats:
        if fmt == "docx":
            p = out_dir / f"{base}.docx"
            to_docx(p, title, meta, main, others, software, etape)
            generated.append(p)
        elif fmt == "xlsx":
            p = out_dir / f"{base}.xlsx"
            to_xlsx(p, title, meta, main, others, software, etape)
            generated.append(p)
        elif fmt == "pdf":
            p = out_dir / f"{base}.pdf"
            to_pdf(p, title, meta, main, others, software, etape)
            generated.append(p)
        elif fmt == "json":
            p = out_dir / f"{base}.json"
            # Pass-through or re-serialize
            p.write_text(json.dumps(load(json_input), ensure_ascii=False, indent=2), encoding="utf8")
            generated.append(p)
        else:
            raise ValueError(f"Unknown format: {fmt}")
    
    return generated

def main():
    """CLI entry point (for manual testing)."""
    parser = argparse.ArgumentParser(description="Cas 20: Modélisation Design Audit")
    parser.add_argument("--json", required=True, help="JSON file or string")
    parser.add_argument("--format", default="docx", help="Comma-separated formats")
    parser.add_argument("--software", default=DEFAULT_SOFTWARE)
    parser.add_argument("--ref", default="")
    parser.add_argument("--out-dir", default="./sortie_word_cas20")
    args = parser.parse_args()
    
    formats = [f.strip().lower() for f in args.format.split(",")]
    paths = generate_document(args.json, args.out_dir, formats, args.software, args.ref)
    for p in paths:
        print(p)

if __name__ == "__main__":
    main()
```

### 2.3 Auto Mode Implementation

When `[Modélisation design]` is absent or `= [Mode auto]`:

1. **Analyze table 2 structure**: iterate first row, identify all nested objects
2. **Propose designs**: each nested object becomes a Level 1 header
3. **Heuristics**:
   - Object key containing "cycle", "processus" → "Cycle par sous processus"
   - Object key containing "risque", "impact", "probabilité" → "Evaluation des risques par criticité"
   - Object key containing "contrôle" → "Dispositif de contrôle interne"
   - Object key containing "action", "recommandation" → "Plan d'action"
4. **Fallback**: use object key as-is if no pattern matches
5. **Document choice**: add to table 1's `Modélisation design` field for transparency

### 2.4 Error Handling

**Each operation that can fail:**

| Operation | Failure Condition | Recoverable? | Caller Receives | Logging |
|-----------|------------------|--------------|----------------|---------|
| JSON parse | Invalid JSON syntax | No | `ValueError` with line/col | ERROR |
| JSON structure validation | Missing table 1 or 2 | No | `ValueError` "Missing required table" | ERROR |
| Reference validation | Invalid format | Yes | Auto-generate valid ref | WARN |
| Tree building | Empty table 2 | No | `ValueError` "No data rows" | ERROR |
| File write | Disk full, permissions | No | `IOError` with path | ERROR |
| Excel merge | Invalid cell range | No | `ValueError` "Invalid merge range" | ERROR |
| PDF font loading | Font not found | Yes | Fallback to Helvetica | WARN |

**Logging:**
- Use `logging` module with level-based output
- Format: `[LEVEL] [timestamp] [function] message`
- Log to stderr for errors, stdout for info
- Orchestrator captures logs and surfaces to user

---

## 3. Orchestrator: execute_cas20_production.py

### 3.1 Architecture

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Orchestrateur Cas 20 : Modélisation Design Audit
Appelle N8N webhook, extrait Data_integrale, génère documents Word/Excel/PDF.
"""

import sys
import json
import requests
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any

# Configuration
WEBHOOK_URL = "http://localhost:5678/webhook/skill_modelisation_cas20"
OUTPUT_DIR = Path("./sortie_word_cas20")
TEMP_DIR = Path("./temp_modelisation_cas20")
DATA_DIR = Path("./data_json_from_n8n_cas20")
TIMEOUT = 30

# Import skill
from json2word_modelisation import generate_document, DEFAULT_SOFTWARE

def log(message: str, level: str = "INFO"):
    """Log with timestamp and level."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{level}] [{timestamp}] {message}", file=sys.stderr if level == "ERROR" else sys.stdout)

def call_n8n_api(url: str, method: str = "POST", timeout: int = 30) -> Dict:
    """Call N8N webhook and return JSON response.
    
    Raises:
        requests.ConnectionError: N8N not reachable
        requests.Timeout: Request exceeded timeout
        requests.HTTPError: HTTP error status
        ValueError: Response not JSON
    """
    log(f"Calling N8N: {method} {url}")
    try:
        if method == "POST":
            response = requests.post(url, timeout=timeout)
        else:
            response = requests.get(url, timeout=timeout)
        
        response.raise_for_status()
        data = response.json()
        log(f"✓ N8N response received: {len(json.dumps(data))} bytes")
        return data
    
    except requests.ConnectionError as e:
        log(f"✗ Connection error: {e}", "ERROR")
        raise
    except requests.Timeout as e:
        log(f"✗ Timeout after {timeout}s", "ERROR")
        raise
    except requests.HTTPError as e:
        log(f"✗ HTTP {response.status_code}: {e}", "ERROR")
        raise
    except ValueError as e:
        log(f"✗ Invalid JSON response: {e}", "ERROR")
        raise

def extract_data_integrale(response: Dict) -> List[Dict]:
    """Extract Data_integrale from N8N response.
    
    Handles:
    - Direct: {"Data_integrale": [...]}
    - Nested: [{"Data_integrale": [...]}]
    - Double: {"Data_integrale": [{"Data_integrale": [...]}]}
    
    Returns:
        List of data records (each is a full JSON for one document)
    """
    if isinstance(response, list):
        response = response[0] if response else {}
    
    if "Data_integrale" not in response:
        log("✗ No Data_integrale in response", "ERROR")
        raise ValueError("Missing Data_integrale field")
    
    data = response["Data_integrale"]
    
    # Handle double nesting
    if isinstance(data, list) and len(data) > 0:
        if isinstance(data[0], dict) and "Data_integrale" in data[0]:
            data = data[0]["Data_integrale"]
    
    if not isinstance(data, list):
        data = [data]
    
    log(f"✓ Extracted {len(data)} records from Data_integrale")
    return data

def save_full_response(data: Dict, data_dir: Path) -> Path:
    """Save full N8N response for audit trail."""
    data_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = data_dir / f"n8n_response_{timestamp}.json"
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf8")
    log(f"✓ Saved response to {path}")
    return path

def process_modelisation(
    data_integrale: List[Dict],
    output_dir: Path,
    temp_dir: Path,
    formats: List[str] = ["docx"],
    software: str = DEFAULT_SOFTWARE
) -> Dict[str, int]:
    """Process all modelisation records and generate documents.
    
    Returns:
        {"success": count, "failed": count}
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    temp_dir.mkdir(parents=True, exist_ok=True)
    
    stats = {"success": 0, "failed": 0}
    
    for idx, record in enumerate(data_integrale, 1):
        log(f"Processing record {idx}/{len(data_integrale)}...")
        
        try:
            # Save temp JSON
            temp_json = temp_dir / f"record_{idx}.json"
            temp_json.write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding="utf8")
            
            # Generate documents
            paths = generate_document(
                json_input=str(temp_json),
                output_dir=str(output_dir),
                formats=formats,
                software=software,
                reference=""  # Auto-generate
            )
            
            for path in paths:
                log(f"  ✓ Generated: {path.name}")
            
            stats["success"] += 1
        
        except Exception as e:
            log(f"  ✗ Failed record {idx}: {e}", "ERROR")
            stats["failed"] += 1
    
    return stats

def main():
    """Main orchestration flow."""
    log("=" * 80)
    log("ORCHESTRATEUR CAS 20 : MODÉLISATION DESIGN AUDIT")
    log("=" * 80)
    
    try:
        # Step 1: Call N8N
        log("\n[ÉTAPE 1] Appel API N8N...")
        response = call_n8n_api(WEBHOOK_URL, method="POST", timeout=TIMEOUT)
        save_full_response(response, DATA_DIR)
        
        # Step 2: Extract and process
        log("\n[ÉTAPE 2] Extraction et conversion...")
        data_integrale = extract_data_integrale(response)
        
        stats = process_modelisation(
            data_integrale=data_integrale,
            output_dir=OUTPUT_DIR,
            temp_dir=TEMP_DIR,
            formats=["docx"],  # Add "xlsx", "pdf" as needed
            software=DEFAULT_SOFTWARE
        )
        
        # Step 3: Summary
        log("\n" + "=" * 80)
        log("RÉSUMÉ")
        log("=" * 80)
        log(f"✓ Documents générés : {stats['success']}")
        log(f"✗ Échecs : {stats['failed']}")
        log(f"Dossier de sortie : {OUTPUT_DIR.absolute()}")
        log("=" * 80)
        
        sys.exit(0 if stats["failed"] == 0 else 1)
    
    except KeyboardInterrupt:
        log("\n✗ Interrupted by user", "ERROR")
        sys.exit(130)
    except Exception as e:
        log(f"\n✗ Fatal error: {e}", "ERROR")
        sys.exit(1)

if __name__ == "__main__":
    main()
```

### 3.2 Configuration

- **WEBHOOK_URL**: `http://localhost:5678/webhook/skill_modelisation_cas20`
- **OUTPUT_DIR**: `./sortie_word_cas20` (created if missing)
- **TEMP_DIR**: `./temp_modelisation_cas20` (intermediate JSON files)
- **DATA_DIR**: `./data_json_from_n8n_cas20` (audit trail of N8N responses)
- **TIMEOUT**: 30 seconds
- **DEFAULT_SOFTWARE**: `"Logiciel automatisé E-audit pro 2.0"`

All paths are relative to Cas_20 directory when executed from there.

---

## 4. Automation Scripts

### 4.1 execute_cas20.bat (Windows Batch)

```batch
@echo off
chcp 65001 >nul
echo ================================================================================
echo EXÉCUTION CAS 20 : MODÉLISATION DESIGN AUDIT
echo ================================================================================
echo.

REM Verify Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERREUR] Python non installé
    echo Installez Python 3.8+ depuis https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Execute
echo [INFO] Lancement de l'orchestrateur...
python execute_cas20_production.py

echo.
echo ================================================================================
echo Code de sortie : %ERRORLEVEL%
echo ================================================================================
pause
```

**Features:**
- UTF-8 console encoding (chcp 65001)
- Python presence check
- Error code display
- Pause for user review

### 4.2 test_workflow_cas20.ps1 (PowerShell Tests)

```powershell
# -*- coding: utf-8 -*-
# Test Suite Cas 20 : Modélisation Design Audit

$ErrorActionPreference = "Continue"
$TestsPassed = 0
$TestsFailed = 0

Write-Host "=" * 80
Write-Host "TESTS CAS 20 : MODÉLISATION DESIGN AUDIT" -ForegroundColor Cyan
Write-Host "=" * 80

# TEST 1: Python installation
Write-Host "`n[TEST 1] Vérification de Python..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "  ✓ Python trouvé : $pythonVersion" -ForegroundColor Green
    $TestsPassed++
} catch {
    Write-Host "  ✗ Python non installé" -ForegroundColor Red
    $TestsFailed++
}

# TEST 2: Python dependencies
Write-Host "`n[TEST 2] Vérification des dépendances Python..." -ForegroundColor Yellow
$deps = @("docx", "requests", "openpyxl", "reportlab")
$allDepsOk = $true
foreach ($dep in $deps) {
    $check = python -c "import $dep" 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  ✓ $dep installé" -ForegroundColor Green
    } else {
        Write-Host "  ✗ $dep manquant" -ForegroundColor Red
        $allDepsOk = $false
    }
}
if ($allDepsOk) {
    Write-Host "  ✓ Toutes les dépendances présentes" -ForegroundColor Green
    $TestsPassed++
} else {
    Write-Host "  ✗ Installez : pip install python-docx requests openpyxl reportlab" -ForegroundColor Red
    $TestsFailed++
}

# TEST 3: Skill files
Write-Host "`n[TEST 3] Vérification des fichiers du skill..." -ForegroundColor Yellow
$files = @(
    "json2word_modelisation.py",
    "execute_cas20_production.py",
    "audit-modelisation-design-json2word.skill.md",
    "GUIDE_CONFIGURATION_N8N.md"
)
$allFilesOk = $true
foreach ($file in $files) {
    if (Test-Path $file) {
        Write-Host "  ✓ $file trouvé" -ForegroundColor Green
    } else {
        Write-Host "  ✗ $file manquant" -ForegroundColor Red
        $allFilesOk = $false
    }
}
if ($allFilesOk) {
    $TestsPassed++
} else {
    $TestsFailed++
}

# TEST 4: N8N reachability
Write-Host "`n[TEST 4] Vérification de N8N..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost:5678" -TimeoutSec 3 -UseBasicParsing
    Write-Host "  ✓ N8N accessible" -ForegroundColor Green
    $TestsPassed++
} catch {
    Write-Host "  ✗ N8N non accessible (http://localhost:5678)" -ForegroundColor Red
    Write-Host "    Lancez : n8n start" -ForegroundColor Yellow
    $TestsFailed++
}

# TEST 5: Webhook test
Write-Host "`n[TEST 5] Test du webhook Cas 20..." -ForegroundColor Yellow
try {
    $body = @{
        Data_integrale = @(
            @{
                "Etape mission - Test" = @(
                    @{ "table 1" = @{ "Etape de mission" = "Test"; "Reference" = "T001" } },
                    @{ "table 2" = @(
                        @{ "no" = 1; "Test groupe" = @{ "Col1" = "Val1"; "Col2" = "Val2" } }
                    )}
                )
            }
        )
    } | ConvertTo-Json -Depth 10
    
    $response = Invoke-RestMethod -Uri "http://localhost:5678/webhook/skill_modelisation_cas20" -Method POST -Body $body -ContentType "application/json" -TimeoutSec 5
    
    if ($response.Data_integrale) {
        $count = $response.Data_integrale.Count
        Write-Host "  ✓ Webhook répond : $count élément(s)" -ForegroundColor Green
        $TestsPassed++
    } else {
        Write-Host "  ✗ Webhook ne retourne pas Data_integrale" -ForegroundColor Red
        $TestsFailed++
    }
} catch {
    Write-Host "  ✗ Webhook non accessible" -ForegroundColor Red
    Write-Host "    Configurez le workflow N8N (voir GUIDE_CONFIGURATION_N8N.md)" -ForegroundColor Yellow
    $TestsFailed++
}

# TEST 6: Output directories
Write-Host "`n[TEST 6] Création des dossiers de sortie..." -ForegroundColor Yellow
$dirs = @("sortie_word_cas20", "temp_modelisation_cas20", "data_json_from_n8n_cas20")
foreach ($dir in $dirs) {
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
    }
    if (Test-Path $dir) {
        Write-Host "  ✓ $dir créé/vérifié" -ForegroundColor Green
    } else {
        Write-Host "  ✗ $dir impossible à créer" -ForegroundColor Red
        $allDirsOk = $false
    }
}
$TestsPassed++

# TEST 7: Conversion script test
Write-Host "`n[TEST 7] Test du script de conversion..." -ForegroundColor Yellow
try {
    # Create minimal JSON
    $testJson = @{
        "Etape mission - Test Design" = @(
            @{ "table 1" = @{ "Etape de mission" = "Test"; "Reference" = "T002" } },
            @{ "table 2" = @(
                @{ "no" = 1; "Design Test" = @{ "Col A" = "A1"; "Col B" = "B1" } }
            )}
        )
    } | ConvertTo-Json -Depth 10
    
    $testFile = "test_minimal_cas20.json"
    $testJson | Out-File -FilePath $testFile -Encoding UTF8
    
    # Run conversion
    $output = python json2word_modelisation.py --json $testFile --out-dir ./sortie_word_cas20 2>&1
    
    if ($LASTEXITCODE -eq 0) {
        $docxFiles = Get-ChildItem ./sortie_word_cas20 -Filter "*.docx" | Where-Object { $_.LastWriteTime -gt (Get-Date).AddMinutes(-1) }
        if ($docxFiles.Count -gt 0) {
            Write-Host "  ✓ Document généré : $($docxFiles[0].Name)" -ForegroundColor Green
            $TestsPassed++
            # Cleanup
            Remove-Item $docxFiles[0].FullName -Force
        } else {
            Write-Host "  ✗ Aucun document généré" -ForegroundColor Red
            $TestsFailed++
        }
    } else {
        Write-Host "  ✗ Script de conversion échoué" -ForegroundColor Red
        Write-Host "    $output" -ForegroundColor Yellow
        $TestsFailed++
    }
    
    Remove-Item $testFile -Force -ErrorAction SilentlyContinue
} catch {
    Write-Host "  ✗ Erreur lors du test : $_" -ForegroundColor Red
    $TestsFailed++
}

# Summary
Write-Host "`n" + ("=" * 80)
Write-Host "RÉSUMÉ DES TESTS" -ForegroundColor Cyan
Write-Host ("=" * 80)
Write-Host "✓ Tests réussis : $TestsPassed" -ForegroundColor Green
Write-Host "✗ Tests échoués : $TestsFailed" -ForegroundColor Red
$total = $TestsPassed + $TestsFailed
$rate = [math]::Round(($TestsPassed / $total) * 100, 1)
Write-Host "Taux de succès : $rate%" -ForegroundColor $(if ($rate -ge 85) { "Green" } else { "Yellow" })
Write-Host ("=" * 80)

exit $(if ($TestsFailed -eq 0) { 0 } else { 1 })
```

**Test coverage:**
1. Python installation and version
2. Dependencies (python-docx, requests, openpyxl, reportlab)
3. Skill files present
4. N8N running (localhost:5678)
5. Webhook responds correctly
6. Output directories created
7. End-to-end conversion (JSON → Word)

---

## 5. N8N Webhook Configuration

### 5.1 Workflow Structure

```
[Webhook] → [Edit Fields (Set)] → [Respond to Webhook]
```

**Node 1: Webhook**
- **Node Name**: `Webhook Cas 20`
- **HTTP Method**: POST
- **Path**: `skill_modelisation_cas20`
- **Response Mode**: When Last Node Finishes
- **Full URL**: `http://localhost:5678/webhook/skill_modelisation_cas20`

**Node 2: Edit Fields (Set)**
- **Node Name**: `Prepare Data_integrale`
- **Mode**: Manual Mapping
- **Fields to Set**:
  - **Name**: `Data_integrale`
  - **Type**: Array
  - **Value**: (Example structure)
    ```json
    [
      {
        "Etape mission - Cartographie des risques": [
          {
            "table 1": {
              "Etape de mission": "Cartographie des risques",
              "Document": "Cartographie design",
              "Processus": "Gestion des risques",
              "Cycle d'activité": "Management des Risques",
              "Méthodologie": "ISO 31000:2018, COSO ERM 2017",
              "Reference": "CR010",
              "Version": "V1.0",
              "Etablissement": "Banque Test",
              "Date d'élaboration": "2026-11-01",
              "Modélisation design": "[Cycle par sous processus], [Evaluation des risques par criticité]"
            }
          },
          {
            "table 2": [
              {
                "no": 1,
                "Cycle par sous processus": {
                  "Cycle": "Cycle commercial",
                  "Processus": "Ventes",
                  "Tâche clé": "Facturation"
                },
                "Evaluation des risques par criticité": {
                  "Probabilité": "Moyen (2)",
                  "Impact": "Élevé (3)",
                  "Criticité brute": "Élevé (6)"
                }
              }
            ]
          }
        ]
      }
    ]
    ```

**Node 3: Respond to Webhook**
- **Node Name**: `Send Response`
- **Response Body**: `{{ $json }}`

### 5.2 Database Integration (Optional)

To connect to a real data source (PostgreSQL example):

**Insert between Webhook and Edit Fields:**

```
[Webhook] → [PostgreSQL] → [Code (Transform)] → [Edit Fields] → [Respond]
```

**PostgreSQL Node:**
- **Operation**: Execute Query
- **Query**:
  ```sql
  SELECT
    id,
    etape_mission,
    processus,
    json_data,
    created_at
  FROM audit_modelisations
  WHERE statut = 'pending'
  ORDER BY created_at DESC
  LIMIT 10;
  ```

**Code Node (Transform to Data_integrale format):**
```javascript
// Transform DB rows to Data_integrale structure
const items = $input.all();
const data_integrale = items.map(item => {
  const jsonData = JSON.parse(item.json.json_data);
  return jsonData;
});

return [{ json: { Data_integrale: data_integrale } }];
```

---

## 6. Example Data Shapes

### 6.1 Minimal Example (exemple_modelisation_minimal.json)

```json
{
  "Etape mission - Programme de travail": [
    {
      "table 1": {
        "Etape de mission": "Programme de travail",
        "Document": "Programme de travail - Audit des ventes",
        "Processus": "Cycle commercial - Ventes",
        "Reference": "PT001",
        "Date d'élaboration": "2026-11-01"
      }
    },
    {
      "table 2": [
        {
          "no": 1,
          "Plan d'action": {
            "Niveau 1": "Contrôles généraux",
            "Niveau 2": "Séparation des tâches",
            "Point de contrôle": "Vérifier ségrégation vente/encaissement"
          },
          "Contrôle": {
            "Contrôle audit": "Inspection des matrices de droits",
            "Assertion": "Séparation des fonctions incompatibles",
            "Document": "Matrice des droits SAP"
          }
        }
      ]
    }
  ]
}
```

### 6.2 Complete Example (exemple_modelisation_complet.json)

```json
{
  "Etape mission - Cartographie des risques": [
    {
      "table 1": {
        "Etape de mission": "Cartographie des risques",
        "Document": "Cartographie des risques opérationnels - Cycle commercial",
        "Processus": "Gestion des ventes et créances clients",
        "Cycle d'activité": "Cycle commercial",
        "Secteur d'activité": "Banque UMOA",
        "Méthodologie": "ISO 31000:2018, COSO ERM 2017, Référentiel BCEAO",
        "Reference": "CR015",
        "Version": "V2.0 - Cartographie avec design",
        "Etablissement": "Banque Commerciale de l'Ouest",
        "Périmètre": "Processus crédit commercial",
        "Date d'élaboration": "31 octobre 2026",
        "Approbation": "Comité des Risques",
        "Responsable": "Directeur des Risques",
        "Modélisation design": "[Cycle par sous processus], [Evaluation des risques par criticité], [Dispositif de contrôle interne par échelon]"
      }
    },
    {
      "table 2": [
        {
          "no": 1,
          "Cycle par sous processus": {
            "Cycle": "Cycle commercial",
            "Processus": "Ventes",
            "Sous-processus": "Commandes clients",
            "Tâche clé": "Enregistrement commande",
            "Document": "Bon de commande"
          },
          "Evaluation des risques par criticité": {
            "Probabilité": "Moyen (2)",
            "Impact": "Élevé (3)",
            "Criticité brute": "Élevé (6)",
            "Cause racine": "Absence de validation formelle"
          },
          "Dispositif de contrôle interne par échelon": {
            "1er échelon": "Auto-contrôle commercial",
            "2e échelon": "Validation manager",
            "Efficacité": "Partiellement efficace",
            "Criticité nette": "Moyen (4)"
          }
        },
        {
          "no": 2,
          "Cycle par sous processus": {
            "Cycle": "Cycle commercial",
            "Processus": "Ventes",
            "Sous-processus": "Facturation",
            "Tâche clé": "Émission facture",
            "Document": "Facture"
          },
          "Evaluation des risques par criticité": {
            "Probabilité": "Faible (1)",
            "Impact": "Moyen (2)",
            "Criticité brute": "Faible (2)",
            "Cause racine": "Automatisation complète"
          },
          "Dispositif de contrôle interne par échelon": {
            "1er échelon": "Contrôle automatique ERP",
            "2e échelon": "Rapprochement mensuel",
            "Efficacité": "Efficace",
            "Criticité nette": "Faible (1)"
          }
        }
      ]
    }
  ]
}
```

---

## 7. Documentation Outline

### 7.1 audit-modelisation-design-json2word.skill.md (15000+ words)

**Structure (mandatory sections per TODO):**

1. **Dependencies** (Installation Base + Complète)
2. **Metadata** (Name, Version, Author, Description, Tags, Dependencies)
3. **Purpose** (Description claire, distinction avec autres cas)
4. **Use Cases** (Workflow Automatisé avec API N8N)
5. **Input Format** (Structure JSON détaillée, designs, auto mode)
6. **Contraintes Obligatoires** (5 sous-sections):
   - Format du Document (paysage, marges)
   - En-tête et Pied de Page (bordeaux, WhatsApp)
   - Orientation des Tables (table 1 verticale, table 2 horizontale avec designs)
   - Couleurs et Mise en Forme (bordeaux #800020, risk colors)
   - Règles de Nommage des Fichiers (`<ref>-<Etape>- <Software>_<timestamp>.docx`)
7. **Output Format** (Word avec grouped headers, Excel, PDF, JSON)
8. **Technical Implementation** (Architecture, tree building, colspan/rowspan logic)
9. **Validation Rules** (9 contrôles pré/post conversion)
10. **Usage Examples** (Exemple 1 : Workflow Production minimal et complet)
11. **Error Handling** (Tableau des erreurs communes avec solutions)
12. **Best Practices** (3+ sous-sections: design conception, performance, maintenance)
13. **Extending the Skill** (Comment ajouter designs, formats)
14. **Limitations** (5 limitations: max columns, nested depth, font availability, etc.)
15. **Testing** (Test connexion N8N + workflow complet 7/7 tests)
16. **License & Attribution**
17. **Changelog** (Version 1.0.0 avec date)

**Key content priorities:**
- Detailed explanation of header tree algorithm (build_tree → leaves → header_matrix)
- Colspan/rowspan calculation with examples
- Auto mode decision heuristics
- Design catalog from mode-auto.md
- Variable reference from variables.md
- Render constraints from contraintes-rendu.md
- Complete error code reference
- Performance considerations (large tables, many designs)

### 7.2 README.md

**Sections:**
- **Description** 📋: Cas 20 purpose and scope
- **Statut** ✅: OPÉRATIONNEL (after phase 6 tests pass)
- **Objectif** 🎯: Generate audit design documents with grouped headers
- **Fichiers Disponibles** 📦:
  - Scripts Principaux: json2word_modelisation.py, execute_cas20_production.py
  - Documentation: skill.md, GUIDE_CONFIGURATION_N8N.md, README, CHANGELOG
- **Démarrage Rapide** 🚀:
  - Installation: `pip install python-docx requests openpyxl reportlab`
  - Configuration N8N: see guide
  - Exécution: `python execute_cas20_production.py` or `execute_cas20.bat`
- **Workflow Complet** 📊: ASCII diagram N8N → Orchestrator → Skill → Word/Excel/PDF
- **Format de Sortie** 📝:
  - Nom: `<ref>-<Etape>- <Software>_<timestamp>.docx`
  - Caractéristiques: paysage, grouped headers, bordeaux #800020
- **Configuration** 🔧:
  - URL webhook: /webhook/skill_modelisation_cas20
  - Dossiers: sortie_word_cas20, temp_modelisation_cas20, data_json_from_n8n_cas20
  - Timeout: 30s
- **Tests** 🧪: `.\test_workflow_cas20.ps1` (7 tests)
- **Fonctionnalités** 📈:
  - ✅ Implémenté: grouped headers, auto mode, multi-format, risk colors
  - 🔜 Futures: templates personnalisés, API REST, interface web
- **Dépannage** 🐛: common errors and solutions
- **Documentation** 📚: links to skill.md and n8n guide
- **Contact** 📞: WhatsApp
- **Version** 📅: 1.0.0

### 7.3 CHANGELOG.md

```markdown
# Changelog - Cas 20 : Modélisation Design Audit

## [1.0.0] - 2026-11-01

### ✨ Ajouté
- Skill de modélisation design avec en-têtes regroupés
- Support des designs: Cycle par sous processus, Evaluation risques, Dispositif contrôle, Plan d'action
- Mode auto pour génération intelligente des designs
- Algorithme de construction d'arbre d'en-têtes (build_tree, header_matrix)
- Rendu colspan/rowspan dans Word, Excel, PDF
- Fusion verticale des colonnes pivot (Cycle, Processus)
- Coloration des niveaux de risque (Élevé/Moyen/Faible)
- Orchestrateur avec webhook N8N /webhook/skill_modelisation_cas20
- Scripts d'automatisation (execute_cas20.bat, test_workflow_cas20.ps1)
- 7 tests automatisés (Python, dépendances, N8N, webhook, conversion)

### 📋 Documenté
- audit-modelisation-design-json2word.skill.md (15000+ mots)
- GUIDE_CONFIGURATION_N8N.md avec workflow complet
- README.md avec démarrage rapide
- Exemples JSON (minimal et complet)

### 🔧 Spécifié
- Couleur bordeaux #800020 (distincte des autres cas)
- Format de fichier: `<ref>-<Etape>- <Software>_<timestamp>.docx`
- Structure JSON: designs imbriqués avec groupes niveau 1
- Validation: 9 contrôles pré/post conversion

### 📚 Aligné
- TODO_IMPLEMENTATION_CAS_X.md: phases 1-9 complètes
- Conventions du projet (Cas_2, Cas_6, Cas_12)
- Native skill render_design.py adapté

## [Unreleased] - À venir

### ⏳ À Implémenter
- Templates Word personnalisés ([Template source])
- Support Jinja2 pour templates dynamiques
- API REST standalone (Flask/FastAPI)
- Interface web (upload JSON → download Word)
- Batch processing (folder monitoring)

### 🔜 Améliorations Futures
- Validation JSON schema (JSONSchema)
- Support de plus de 4 niveaux de hiérarchie
- Export Power BI / Tableau
- Intégration SharePoint
- Versioning des documents
```

### 7.4 GUIDE_CONFIGURATION_N8N.md

**Sections:**
- **Pré-requis** 📋: N8N, Python, dépendances
- **Installation de N8N** 🚀: npm global, npx, Docker
- **Configuration du Workflow** 🔧:
  - Étape 1: Créer workflow
  - Étape 2: Nœud Webhook (config détaillée)
  - Étape 3: Nœud Edit Fields (structure Data_integrale)
  - Étape 4: Nœud Respond
  - Étape 5: Activer
- **Vérification** ✅: 4 tests (curl, Python, script complet, PowerShell)
- **Structure des Données** 📊: Format Data_integrale, designs imbriqués
- **Connexion Base de Données** 🔗: PostgreSQL/MySQL example
- **Dépannage** 🐛: Connection refused, webhook not found, timeout
- **Conseils d'Optimisation** 💡: Pinned data, pagination, filtrage
- **Support** 📞
- **Ressources** 📚
- **Vue d'Ensemble** 🎯: Diagramme ASCII du flux complet

---

## 8. Testability

### 8.1 Unit Testing Strategy

**json2word_modelisation.py:**
- `test_build_tree()`: various input structures → verify tree shape
- `test_leaves()`: tree → verify all paths extracted
- `test_header_matrix()`: tree → verify cells with correct rowspan/colspan
- `test_get()`: nested dict + path → verify value extraction
- `test_level_fill()`: risk strings → verify color mapping
- `test_flat()`: nested structures → verify string representation
- `test_generate_reference()`: no input → verify format `[A-Z]{2}\d{3}`
- `test_extract_json_from_text()`: wrapped JSON → verify unwrapping
- `test_load()`: JSON file → verify (title, meta, main, others) extraction

**execute_cas20_production.py:**
- `test_call_n8n_api_success()`: mock requests → verify JSON returned
- `test_call_n8n_api_timeout()`: mock timeout → verify exception raised
- `test_extract_data_integrale()`: various response shapes → verify extraction
- `test_process_modelisation()`: mock data → verify stats correct

**Framework:** pytest with fixtures for sample JSON structures

### 8.2 Integration Testing

**Test 1: Minimal design (1 group)**
- Input: 1 design with 3 columns
- Expected: Word with 2-row header (Level 1 + leaves), 3 data columns

**Test 2: Multiple designs (3 groups)**
- Input: 3 designs, 10 columns total
- Expected: Word with 2-row header, 10 columns, correct groupings

**Test 3: Nested designs (3 levels)**
- Input: Cycle > Processus > Sous-processus
- Expected: 3-row header, vertical merges for repeated Cycle/Processus

**Test 4: Risk level coloring**
- Input: Columns with "Élevé", "Moyen", "Faible" values
- Expected: Cells shaded red, yellow, green

**Test 5: Auto mode**
- Input: JSON without explicit designs (nested objects in table 2)
- Expected: Designs auto-detected, Word generated

**Test 6: Multi-format**
- Input: formats=["docx", "xlsx", "pdf"]
- Expected: 3 files generated, all readable

**Test 7: Large dataset**
- Input: 100 rows, 20 columns
- Expected: Document generated in < 10s, no truncation

### 8.3 What Can Be Unit Tested vs. Integration Tested

**Unit testable:**
- Tree building algorithm (pure functions)
- Path extraction and navigation
- Column width calculation
- Reference generation
- JSON extraction and validation
- Color mapping logic

**Integration required:**
- Word document rendering (python-docx interaction)
- Excel rendering (openpyxl interaction)
- PDF rendering (reportlab interaction)
- N8N webhook communication
- File I/O and directory creation
- End-to-end: JSON → Word → verify content

**Hard to test (manual validation):**
- Visual layout (column widths appropriate)
- Print preview (headers repeat on pages)
- Document compatibility (opens in MS Word, LibreOffice)
- Font rendering on different systems

---

## 9. Edge Cases and Invariants

### 9.1 Edge Cases

**Edge Case 1: No designs (all scalar columns)**
- Behavior: Render as flat table with 1-row header
- Rationale: Degrade gracefully, still usable

**Edge Case 2: Empty table 2**
- Behavior: Fatal error, ValueError("No data rows")
- Rationale: Cannot build tree from empty set

**Edge Case 3: Single column design**
- Behavior: Accept but warn (design with colspan=1)
- Rationale: Technically valid, but user may have intended grouping

**Edge Case 4: Very deep nesting (5+ levels)**
- Behavior: Render all levels, but warn if depth > 4
- Rationale: Readability concern, not technical limit

**Edge Case 5: Extremely long column names**
- Behavior: Wrap text in header cell, adjust column width
- Rationale: Preserve all data, may require wider columns

**Edge Case 6: Missing Reference**
- Behavior: Auto-generate valid reference
- Rationale: Required for filename, better to auto-fill than fail

**Edge Case 7: Duplicate column names across groups**
- Behavior: Fatal error, ValueError("Duplicate column")
- Rationale: Ambiguous structure, cannot merge correctly

**Edge Case 8: Unicode characters in filenames**
- Behavior: Preserve accents, remove only forbidden chars
- Rationale: French language support required

**Edge Case 9: Nested objects with mixed types (scalar + object)**
- Behavior: Accept, scalar = rowspan column, object = grouping
- Rationale: Common in real data

**Edge Case 10: N8N returns empty Data_integrale**
- Behavior: Error, log "No data returned", exit code 1
- Rationale: Cannot proceed without data

### 9.2 Invariants and Ownership

**Invariant 1: All leaf paths are unique**
- **Owner**: `build_tree` function
- **Enforcement**: Check during tree merge, raise if duplicate detected
- **Reason**: Prevents ambiguous column references

**Invariant 2: Colspan of parent = sum of child colspans**
- **Owner**: `header_matrix` function
- **Enforcement**: Recursive count during matrix generation
- **Reason**: Ensures correct cell merging in Word/Excel

**Invariant 3: Total columns in header = total data columns**
- **Owner**: `to_docx` / `to_xlsx` / `to_pdf` functions
- **Enforcement**: Verify len(paths) == table column count before rendering
- **Reason**: Prevents misaligned data

**Invariant 4: Filename matches format `<ref>-<etape>- <software>_<timestamp>.<ext>`**
- **Owner**: `generate_document` function
- **Enforcement**: Construct filename from validated components, apply safe_filename
- **Reason**: Consistency across all cases, filesystem compatibility

**Invariant 5: Bordeaux color = #800020 in all headers**
- **Owner**: `to_docx` / `to_xlsx` / `to_pdf` functions
- **Enforcement**: Use constant BORDEAUX, verify in post-conversion tests
- **Reason**: Brand consistency, distinguishes from other cases

**Invariant 6: table 1 is always vertical (2 columns)**
- **Owner**: `to_docx` / `to_xlsx` functions
- **Enforcement**: Force 2-column layout regardless of metadata count
- **Reason**: Contrainte obligatoire from contraintes-rendu.md

**Invariant 7: Header rows repeat on every page**
- **Owner**: `to_docx` function
- **Enforcement**: Apply `w:tblHeader` XML element to header rows
- **Reason**: Readability for multi-page documents

**Invariant 8: No data loss (all JSON values appear in output)**
- **Owner**: Integration tests
- **Enforcement**: Compare JSON values with extracted Word table cells
- **Reason**: Data integrity requirement

---

## 10. Technology Stack (Locked Post-Approval)

**Programming Language:** Python 3.11

**Core Libraries:**
- **python-docx** 0.8.11+: Word document generation, cell merging, styling
- **openpyxl** 3.0+: Excel generation with merged cells, filters, conditional formatting
- **reportlab** 3.6+: PDF generation with table spans
- **requests** 2.28+: N8N webhook communication
- **Pillow** 9.0+ (optional): Image handling in documents

**Standard Library:**
- argparse: CLI parsing
- json: JSON serialization/deserialization
- pathlib: Path manipulation
- datetime: Timestamps
- re: Regex for validation and cleaning
- random/string: Reference generation
- logging: Structured logging

**Environment:**
- **Conda environment**: `pdf_excel_env` (Python 3.11, Windows)
- **Activation**: `conda activate pdf_excel_env`

**External Services:**
- **N8N** (workflow automation): webhook endpoint, Data_integrale structure
- **Webhook URL**: `http://localhost:5678/webhook/skill_modelisation_cas20`

**File Formats:**
- Input: JSON (UTF-8)
- Output: DOCX (Office Open XML), XLSX (Office Open XML), PDF (reportlab), JSON (pass-through)

**Automation:**
- **Windows Batch** (.bat): Windows CLI execution
- **PowerShell** (.ps1): Cross-platform testing (7 tests)

**Documentation:**
- **Markdown**: skill.md, README, CHANGELOG, GUIDE_CONFIGURATION_N8N

**Why these choices:**
- python-docx: de facto standard for Word generation in Python, rich API for merging/styling
- openpyxl: complete Excel support, actively maintained
- reportlab: mature PDF library, handles complex tables
- requests: simplest HTTP client for N8N integration
- Conda: project standard, isolates dependencies
- N8N: already in use across other cases, webhook pattern established

---

## 11. Performance Considerations

**Expected load:**
- Typical: 5-20 records per batch, 10-30 columns per record
- Large: 100 records, 50 columns (cartographie complète)

**Performance targets:**
- Small (5 records, 15 columns): < 3 seconds total
- Medium (20 records, 25 columns): < 8 seconds
- Large (100 records, 50 columns): < 30 seconds

**Bottlenecks:**
1. **Tree building**: O(rows × columns × depth) - acceptable for typical sizes
2. **Word cell merging**: Each merge is an XML operation - batch when possible
3. **Column width calculation**: O(rows × columns) - cache if rows reused
4. **N8N roundtrip**: Network latency - use 30s timeout

**Optimizations:**
- **Reuse tree structure**: If multiple formats requested, build tree once
- **Lazy font loading**: Load fonts only when first needed (PDF)
- **Stream large tables**: For future 1000+ row support, consider chunked rendering
- **Parallel format generation**: Spawn threads for docx/xlsx/pdf concurrently (future)

**Memory:**
- Estimated: 5-10 MB per document in memory
- Peak: During Word/Excel generation (python-docx holds full document in RAM)
- Acceptable: < 100 MB for typical batches

---

## 12. Maintenance and Extensibility

### 12.1 Adding a New Design Pattern

1. Add to design catalog in `mode-auto.md`
2. Update auto-detection heuristics in `json2word_modelisation.py` (if auto mode should recognize it)
3. Add example to `exemple_modelisation_complet.json`
4. Document in skill.md section "Design Catalog"
5. Add test case in integration tests

**No code change required if:** design follows existing nesting structure (Level 1 → leaves)

### 12.2 Adding a New Output Format

1. Implement `to_<format>()` function in `json2word_modelisation.py`
2. Accept same signature: `(path, title, meta, main, others, software, etape)`
3. Use `header_matrix` output for rendering
4. Add to `generate_document` format switch
5. Update skill.md and README
6. Add validation test in `test_workflow_cas20.ps1`

**Example:** CSV format
```python
def to_csv(path: Path, title: str, meta, main, others, software: str, etape: str):
    import csv
    rows = main[1]
    tree = build_tree(rows)
    depth, cells, paths = header_matrix(tree)
    
    with open(path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        # Write flattened headers
        writer.writerow([".".join(p) for p in paths])
        # Write data
        for row in rows:
            writer.writerow([get(row, p) for p in paths])
```

### 12.3 Modifying Column Specifications

For cases where certain columns have special rendering (e.g., monetary values, dates):

1. Add `COLUMN_SPECS` dict mapping column names to render types
2. In `to_docx`, check column name against specs before rendering
3. Apply special formatting (e.g., currency symbol, date format)

**Example:**
```python
COLUMN_SPECS = {
    "Coût traitement": ("currency", "FCFA"),
    "Échéance": ("date", "%d/%m/%Y"),
    "Criticité brute": ("risk_level", True),  # Apply color
}
```

### 12.4 Backward Compatibility

- JSON structure: Locked post-approval, changes require new major version
- API signature: `generate_document()` is public interface, maintain signature
- Output format: Minor layout changes OK, major changes (e.g., color scheme) require user notification
- N8N webhook: URL and Data_integrale structure must remain stable

---

## 13. Open Questions and Decisions Made

### 13.1 Design Decisions Made

**Q: Should auto mode generate designs even when none are present?**
- **A:** Yes, if table 2 contains nested objects, propose groupings. If all scalar, render flat table.

**Q: How many levels of hierarchy to support?**
- **A:** 2-4 levels. 2 is standard (Level 1 group + leaves), 3-4 for complex cases (Cycle > Processus > Sous-processus). Warn if > 4.

**Q: What to do when Reference is missing?**
- **A:** Auto-generate format `[A-Z]{2}\d{3}`, log warning. Never fail on missing reference.

**Q: Should timestamp be in filename?**
- **A:** Yes, format `YYYYMMDD_HHMMSS`, prevents overwrites in rapid batch processing.

**Q: Where to log errors?**
- **A:** Orchestrator logs to stderr (ERROR) and stdout (INFO). Skill script returns error messages in exceptions, caught by orchestrator.

**Q: Should skill validate JSON schema?**
- **A:** Phase 1: basic validation (keys present, types correct). Phase 2 (future): JSONSchema for strict validation.

**Q: How to handle very wide tables (> 20 columns)?**
- **A:** Adjust column widths proportionally, allow horizontal scroll in Excel, landscape orientation mandatory.

### 13.2 Deferred to Future Versions

- **Templates personnalisés**: [Template source] support (Phase 2 enhancement)
- **API REST standalone**: Skill as microservice (not urgent, N8N sufficient)
- **Batch folder monitoring**: Auto-process JSON files dropped in folder (nice-to-have)
- **Real-time preview**: Web interface with live preview (low priority)
- **Multi-language**: English/French toggle (currently French-only)

### 13.3 Risks and Mitigations

**Risk 1: python-docx cell merge fails with complex structures**
- **Mitigation:** Extensive testing in Phase 6, fallback to non-merged headers if merge fails

**Risk 2: Very large datasets (1000+ rows) exceed memory**
- **Mitigation:** Document limit (100 rows recommended), future streaming support

**Risk 3: Font availability varies across systems (PDF rendering)**
- **Mitigation:** Font detection with fallback to Helvetica (cross-platform)

**Risk 4: N8N webhook timeout for slow data sources**
- **Mitigation:** 30s timeout configurable, recommend database query optimization

**Risk 5: Filename collision in rapid batch**
- **Mitigation:** Timestamp with seconds, extremely unlikely collision

---

## Conclusion

This design provides a complete blueprint for implementing Cas 20's design modeling skill. The core technical challenge—rendering hierarchical grouped headers with accurate colspan/rowspan—is solved by preserving the native skill's tree-building algorithm while adapting it to the project's standardized orchestration and automation patterns.

All major architectural decisions are concrete:
- JSON structure follows Type 1 with nested design groups
- Header tree algorithm uses build_tree → header_matrix → render pipeline
- Multi-format support (Word/Excel/PDF/JSON) from unified internal structure
- N8N webhook /webhook/skill_modelisation_cas20 with Data_integrale wrapper
- Orchestrator follows Cas_2/Cas_6 pattern with logging and stats
- Automation via batch + PowerShell with 7 comprehensive tests
- Documentation exceeds 15000 words across skill.md, README, CHANGELOG, n8n guide
- Technology stack locked: Python 3.11, python-docx, openpyxl, reportlab, requests

Error handling is explicit for each operation, validation rules are testable, and the design is maintainable with clear extension points for new formats and design patterns.

The implementation is ready to proceed to coding phase (Phase 2 of TODO_IMPLEMENTATION_CAS_X.md).
