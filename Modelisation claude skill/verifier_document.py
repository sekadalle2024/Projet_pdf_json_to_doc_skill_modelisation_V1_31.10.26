#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Script de vérification du document Word généré"""

from docx import Document
from docx.shared import Pt

# Ouvrir le document
doc_path = 'sortie_word/A210-Manuel_audit_interne_-_Phase_de_préparation- Logiciel automatisé E-procedure.docx'
doc = Document(doc_path)

print("=" * 80)
print("VÉRIFICATION DU DOCUMENT WORD GÉNÉRÉ")
print("=" * 80)

# 1. Informations générales
print("\n📄 INFORMATIONS GÉNÉRALES")
print(f"Nombre de tables: {len(doc.tables)}")

# 2. Orientation de la page
section = doc.sections[0]
orientation = "Paysage" if section.page_width > section.page_height else "Portrait"
print(f"Orientation: {orientation}")
print(f"Largeur page: {section.page_width.cm:.2f} cm")
print(f"Hauteur page: {section.page_height.cm:.2f} cm")

# 3. En-tête et pied de page
print(f"\n📋 EN-TÊTE ET PIED DE PAGE")
print(f"En-tête: {section.header.paragraphs[0].text}")
print(f"Pied de page: {section.footer.paragraphs[0].text}")

# 4. Table 1 (métadonnées)
print(f"\n📊 TABLE 1 (MÉTADONNÉES)")
table1 = doc.tables[0]
print(f"Nombre de lignes: {len(table1.rows)}")
print(f"Nombre de colonnes: {len(table1.columns)}")
print(f"En-tête ligne 1: {table1.rows[0].cells[0].text} | {table1.rows[0].cells[1].text}")

# Afficher les 5 premières lignes
print("\nPremières lignes de la table 1:")
for i, row in enumerate(table1.rows[:6]):
    if i == 0:
        print(f"  [{i}] EN-TÊTE: {row.cells[0].text} | {row.cells[1].text}")
    else:
        rubrique = row.cells[0].text[:40] + "..." if len(row.cells[0].text) > 40 else row.cells[0].text
        description = row.cells[1].text[:60] + "..." if len(row.cells[1].text) > 60 else row.cells[1].text
        print(f"  [{i}] {rubrique} | {description}")

# 5. Table 2 (étapes méthodologiques)
print(f"\n📊 TABLE 2 (ÉTAPES MÉTHODOLOGIQUES)")
table2 = doc.tables[1]
print(f"Nombre de lignes: {len(table2.rows)}")
print(f"Nombre de colonnes: {len(table2.columns)}")

# En-têtes de colonnes
print("\nEn-têtes de colonnes:")
header_row = table2.rows[0]
for i, cell in enumerate(header_row.cells):
    print(f"  Colonne {i+1}: {cell.text}")

# Compter les lignes renseignées vs vides
filled_rows = 0
empty_rows = 0
for i, row in enumerate(table2.rows[1:], start=1):
    is_empty = all(not cell.text.strip() for cell in row.cells)
    if is_empty:
        empty_rows += 1
    else:
        filled_rows += 1

print(f"\nLignes renseignées: {filled_rows}")
print(f"Lignes vides (séparateurs): {empty_rows}")

# Afficher les 3 premières étapes
print("\nPremières étapes méthodologiques:")
count = 0
for i, row in enumerate(table2.rows[1:], start=1):
    is_empty = all(not cell.text.strip() for cell in row.cells)
    if not is_empty and count < 3:
        etape = row.cells[0].text[:50] + "..." if len(row.cells[0].text) > 50 else row.cells[0].text
        acteur = row.cells[1].text[:30] + "..." if len(row.cells[1].text) > 30 else row.cells[1].text
        print(f"  [{i}] Étape: {etape}")
        print(f"       Acteur: {acteur}")
        count += 1

# 6. Validation
print(f"\n✅ VALIDATION")
checks = [
    ("Orientation paysage", orientation == "Paysage"),
    ("2 tables présentes", len(doc.tables) == 2),
    ("Table 1 : 2 colonnes", len(table1.columns) == 2),
    ("Table 1 : au moins 10 lignes", len(table1.rows) >= 10),
    ("Table 2 : 6 colonnes", len(table2.columns) == 6),
    ("Table 2 : lignes vides insérées", empty_rows > 0),
    ("En-tête présent", bool(section.header.paragraphs[0].text)),
    ("Pied de page présent", bool(section.footer.paragraphs[0].text)),
]

all_passed = True
for check_name, check_result in checks:
    status = "✅ OK" if check_result else "❌ ÉCHEC"
    print(f"{status} - {check_name}")
    if not check_result:
        all_passed = False

print("\n" + "=" * 80)
if all_passed:
    print("✅ TOUS LES CONTRÔLES SONT PASSÉS - Document valide")
else:
    print("⚠️ CERTAINS CONTRÔLES ONT ÉCHOUÉ - Vérifier le document")
print("=" * 80)
