#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Script de contrôle qualité pour vérifier la complétude des conversions Excel → Word"""

import re
import openpyxl
from docx import Document
import warnings
warnings.filterwarnings('ignore')

def normaliser(texte):
    """Normalise un texte : espaces insécables, espaces multiples, majuscules"""
    if not texte:
        return ""
    s = str(texte).replace('\xa0', ' ').replace('\r', '')
    s = re.sub(r'\s+', ' ', s).strip()
    return s.upper()

def extraire_texte_excel(fichier_xlsx):
    """Extrait toutes les cellules de texte significatives (≥4 caractères) du fichier Excel"""
    wb = openpyxl.load_workbook(fichier_xlsx, data_only=True)
    cellules = []
    
    for ws in wb.worksheets:
        # Limiter le scan aux 50 premières colonnes
        max_col = min(ws.max_column, 50)
        for row_idx in range(1, ws.max_row + 1):
            for col_idx in range(1, max_col + 1):
                cell = ws.cell(row_idx, col_idx)
                val = cell.value
                if val and isinstance(val, str) and len(val.strip()) >= 4:
                    cellules.append({
                        'onglet': ws.title,
                        'coord': f"{cell.coordinate}",
                        'texte': val.strip(),
                        'texte_norm': normaliser(val)
                    })
    
    wb.close()
    return cellules

def extraire_texte_word(fichier_docx):
    """Extrait tout le texte des tableaux du document Word"""
    doc = Document(fichier_docx)
    texte_complet = []
    
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                texte = cell.text.strip()
                if texte:
                    texte_complet.append(texte)
    
    # Concaténer et normaliser
    texte_word = ' '.join(texte_complet)
    return normaliser(texte_word)

def verifier_completude(fichier_xlsx, fichier_docx):
    """Vérifie que toutes les cellules Excel sont présentes dans le Word"""
    print("⏳ Extraction du contenu Excel...")
    cellules_excel = extraire_texte_excel(fichier_xlsx)
    print(f"   ✓ {len(cellules_excel)} cellules extraites\n")
    
    print("⏳ Extraction du contenu Word...")
    texte_word = extraire_texte_word(fichier_docx)
    print(f"   ✓ {len(texte_word)} caractères extraits\n")
    
    print("⏳ Vérification de la complétude...")
    manquantes = []
    
    for cell in cellules_excel:
        if cell['texte_norm'] not in texte_word:
            manquantes.append(cell)
    
    # Résultats
    print(f"\n{'='*80}")
    print(f"📊 RÉSULTATS DU CONTRÔLE DE COMPLÉTUDE")
    print(f"{'='*80}")
    print(f"Cellules testées    : {len(cellules_excel)}")
    print(f"Cellules retrouvées : {len(cellules_excel) - len(manquantes)}")
    print(f"Cellules manquantes : {len(manquantes)}")
    print(f"Taux de complétude  : {(len(cellules_excel) - len(manquantes)) / len(cellules_excel) * 100:.1f}%")
    
    if manquantes:
        print(f"\n❌ CELLULES NON RETROUVÉES (20 premières) :")
        print(f"{'-'*80}")
        for cell in manquantes[:20]:
            texte_court = cell['texte'][:60] + '...' if len(cell['texte']) > 60 else cell['texte']
            print(f"  [{cell['onglet']}] {cell['coord']:8} → {texte_court}")
    else:
        print(f"\n✅ Toutes les cellules ont été retrouvées dans le document Word !")
    
    return len(cellules_excel), len(manquantes)

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 3:
        print("Usage: python controle_qualite.py <fichier.xlsx> <fichier.docx>")
        sys.exit(1)
    
    verifier_completude(sys.argv[1], sys.argv[2])
