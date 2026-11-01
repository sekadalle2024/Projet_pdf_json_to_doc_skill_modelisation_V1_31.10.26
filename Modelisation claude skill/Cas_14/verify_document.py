#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de vérification du document Word généré.
Vérifie : orientation, nombre de tables, couleurs, structure.
"""

import sys
from pathlib import Path
from docx import Document
from docx.enum.section import WD_ORIENT
from docx.oxml.ns import qn

def verify_document(docx_path):
    """Vérifie la structure du document Word généré."""
    
    print(f"\n{'='*70}")
    print(f"  VÉRIFICATION DU DOCUMENT : {Path(docx_path).name}")
    print(f"{'='*70}\n")
    
    try:
        doc = Document(docx_path)
    except Exception as e:
        print(f"❌ Erreur d'ouverture du document : {e}")
        return False
    
    success = True
    
    # 1. Vérifier l'orientation
    section = doc.sections[0]
    print(f"1. ORIENTATION")
    print(f"   Largeur : {section.page_width.inches:.2f} inches")
    print(f"   Hauteur : {section.page_height.inches:.2f} inches")
    
    if section.page_width > section.page_height:
        print(f"   ✅ Orientation : LANDSCAPE (correct)")
    else:
        print(f"   ❌ Orientation : PORTRAIT (incorrect)")
        success = False
    
    # Vérifier l'orientation explicite
    try:
        orientation = section.orientation
        if orientation == WD_ORIENT.LANDSCAPE:
            print(f"   ✅ Orientation explicite : LANDSCAPE")
        else:
            print(f"   ⚠️  Orientation explicite : {orientation}")
    except:
        print(f"   ⚠️  Orientation explicite non définie")
    
    # 2. Vérifier le nombre de tables
    table_count = len(doc.tables)
    print(f"\n2. NOMBRE DE TABLES")
    print(f"   Nombre total : {table_count}")
    
    if table_count == 6:
        print(f"   ✅ 6 tables détectées (correct)")
    else:
        print(f"   ❌ {table_count} tables au lieu de 6")
        success = False
    
    # 3. Vérifier Table 1 (structure verticale 2 colonnes)
    if table_count >= 1:
        table1 = doc.tables[0]
        row_count = len(table1.rows)
        col_count = len(table1.columns)
        
        print(f"\n3. TABLE 1 (Métadonnées)")
        print(f"   Lignes : {row_count}")
        print(f"   Colonnes : {col_count}")
        
        if col_count == 2:
            print(f"   ✅ Structure 2 colonnes (correct)")
        else:
            print(f"   ❌ {col_count} colonnes au lieu de 2")
            success = False
        
        # Vérifier la couleur de fond de la première cellule
        first_cell = table1.rows[0].cells[0]
        shading_elm = first_cell._element.xpath('.//w:shd')
        
        if shading_elm:
            fill_color = shading_elm[0].get(qn('w:fill'))
            print(f"   Couleur fond colonne 1 : #{fill_color}")
            
            if fill_color and fill_color.upper() == '8B0000':
                print(f"   ✅ Couleur bordeaux #8B0000 (correct)")
            else:
                print(f"   ❌ Couleur incorrecte (attendu #8B0000)")
                success = False
        else:
            print(f"   ❌ Pas de couleur de fond détectée")
            success = False
        
        # Vérifier les largeurs de colonnes
        col1_width = table1.columns[0].width
        col2_width = table1.columns[1].width
        
        print(f"   Largeur colonne 1 : {col1_width} EMUs (~{col1_width/914400:.2f} inches)")
        print(f"   Largeur colonne 2 : {col2_width} EMUs (~{col2_width/914400:.2f} inches)")
        
        # 4000 twips * 635 = 2,540,000 EMUs (~2.78 inches)
        expected_col1 = 4000 * 635
        tolerance = 100000  # Tolérance de 100k EMUs
        
        if abs(col1_width - expected_col1) < tolerance:
            print(f"   ✅ Largeur colonne 1 correcte (~4000 twips)")
        else:
            print(f"   ⚠️  Largeur colonne 1 : {col1_width} EMUs (attendu ~{expected_col1})")
    
    # 4. Vérifier Tables 2-6 (format horizontal)
    print(f"\n4. TABLES 2-6 (Contenu)")
    for i in range(1, min(6, table_count)):
        table = doc.tables[i]
        row_count = len(table.rows)
        col_count = len(table.columns)
        
        print(f"   Table {i+1} : {row_count} lignes × {col_count} colonnes")
        
        # Vérifier la couleur de l'en-tête
        if row_count > 0:
            header_cell = table.rows[0].cells[0]
            shading_elm = header_cell._element.xpath('.//w:shd')
            
            if shading_elm:
                fill_color = shading_elm[0].get(qn('w:fill'))
                if fill_color and fill_color.upper() == '8B0000':
                    print(f"             ✅ En-tête bordeaux")
                else:
                    print(f"             ⚠️  En-tête : #{fill_color}")
    
    # 5. Vérifier l'en-tête du document
    print(f"\n5. EN-TÊTE ET PIED DE PAGE")
    if doc.sections[0].header.paragraphs:
        header_text = doc.sections[0].header.paragraphs[0].text
        print(f"   En-tête : {header_text[:50]}...")
        
        # Vérifier la couleur de fond de l'en-tête
        header_para = doc.sections[0].header.paragraphs[0]
        shading_elm = header_para._element.xpath('.//w:shd')
        
        if shading_elm:
            fill_color = shading_elm[0].get(qn('w:fill'))
            if fill_color and fill_color.upper() == '8B0000':
                print(f"   ✅ En-tête avec fond bordeaux")
            else:
                print(f"   ⚠️  En-tête fond : #{fill_color}")
    
    if doc.sections[0].footer.paragraphs:
        footer_text = doc.sections[0].footer.paragraphs[0].text
        print(f"   Pied de page : {footer_text[:50]}...")
        print(f"   ✅ Pied de page présent")
    
    # Résumé
    print(f"\n{'='*70}")
    if success:
        print(f"  ✅ VÉRIFICATION RÉUSSIE : Document conforme aux spécifications")
    else:
        print(f"  ⚠️  VÉRIFICATION PARTIELLE : Quelques différences détectées")
    print(f"{'='*70}\n")
    
    return success

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python verify_document.py <chemin_vers_fichier.docx>")
        sys.exit(1)
    
    docx_path = sys.argv[1]
    
    if not Path(docx_path).exists():
        print(f"❌ Fichier introuvable : {docx_path}")
        sys.exit(1)
    
    result = verify_document(docx_path)
    sys.exit(0 if result else 1)
