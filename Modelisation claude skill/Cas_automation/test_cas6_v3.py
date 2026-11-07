#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test rapide du script Cas 6 v3
"""

import subprocess
import sys
from pathlib import Path
from datetime import datetime

# Chemins
CAS6_V3_SCRIPT = Path(__file__).parent.parent / "Cas_6" / "json2word_feuilles_revision_v3.py"
JSON_FILE = Path(__file__).parent / "json standard" / "Json_standard_[Cas 6].txt"
OUTPUT_DIR = Path.home() / "Downloads"

print("="*70)
print("TEST Cas 6 v3")
print("="*70)
print(f"Script: {CAS6_V3_SCRIPT}")
print(f"JSON: {JSON_FILE}")
print(f"Output: {OUTPUT_DIR}")
print()

if not CAS6_V3_SCRIPT.exists():
    print(f"❌ Script v3 non trouvé: {CAS6_V3_SCRIPT}")
    sys.exit(1)

if not JSON_FILE.exists():
    print(f"❌ JSON non trouvé: {JSON_FILE}")
    sys.exit(1)

# Compter les fichiers avant
files_before = list(OUTPUT_DIR.glob("Cas6_*.docx"))
print(f"📁 Fichiers Cas6 existants: {len(files_before)}")

# Exécuter le script
print("\n🚀 Exécution du script v3...")
cmd = [sys.executable, str(CAS6_V3_SCRIPT), str(JSON_FILE), "-o", str(OUTPUT_DIR)]

try:
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        encoding='cp1252',  # Windows default encoding
        errors='replace',
        timeout=30
    )
    
    print("\n📤 STDOUT:")
    print(result.stdout)
    
    if result.stderr:
        print("\n📤 STDERR:")
        print(result.stderr)
    
    print(f"\n📊 Exit code: {result.returncode}")
    
    if result.returncode == 0:
        # Trouver le nouveau fichier
        files_after = list(OUTPUT_DIR.glob("Cas6_*.docx"))
        new_files = set(files_after) - set(files_before)
        
        if new_files:
            new_file = sorted(new_files)[-1]  # Plus récent
            file_size = new_file.stat().st_size
            
            print("\n✅ SUCCESS")
            print(f"📄 Fichier généré: {new_file.name}")
            print(f"📊 Taille: {file_size:,} octets ({file_size/1024:.2f} KB)")
            
            # Vérifier le contenu avec python-docx
            try:
                from docx import Document
                doc = Document(str(new_file))
                num_paragraphs = len(doc.paragraphs)
                num_tables = len(doc.tables)
                
                print(f"\n📋 Contenu du document:")
                print(f"   Paragraphes: {num_paragraphs}")
                print(f"   Tables: {num_tables}")
                
                if num_tables > 0:
                    for idx, table in enumerate(doc.tables, 1):
                        print(f"   Table {idx}: {len(table.rows)}x{len(table.columns)}")
                        if table.rows:
                            first_cell_text = table.rows[0].cells[0].text[:30]
                            print(f"      Première cellule: {first_cell_text}...")
                
            except ImportError:
                print("⚠️ python-docx non disponible pour vérification détaillée")
            except Exception as e:
                print(f"⚠️ Erreur vérification: {e}")
        else:
            print("\n⚠️ Aucun nouveau fichier détecté")
    else:
        print("\n❌ FAILED")
        
except subprocess.TimeoutExpired:
    print("\n❌ TIMEOUT (>30s)")
except Exception as e:
    print(f"\n❌ ERROR: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*70)
