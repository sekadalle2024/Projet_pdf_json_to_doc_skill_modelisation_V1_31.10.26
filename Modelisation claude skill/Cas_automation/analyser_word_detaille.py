#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Analyse détaillée d'un document Word pour voir EXACTEMENT ce qu'il contient
"""

import sys
from pathlib import Path
from docx import Document

def analyser_document(fichier_path):
    """Analyse détaillée du contenu d'un document Word."""
    print("="*70)
    print(f"ANALYSE DÉTAILLÉE: {Path(fichier_path).name}")
    print("="*70)
    
    try:
        doc = Document(str(fichier_path))
        
        # Statistiques générales
        print(f"\n[STATISTIQUES]")
        print(f"Sections: {len(doc.sections)}")
        print(f"Paragraphes: {len(doc.paragraphs)}")
        print(f"Tables: {len(doc.tables)}")
        
        # Analyser chaque section
        print(f"\n[SECTIONS]")
        for idx, section in enumerate(doc.sections, 1):
            print(f"  Section {idx}:")
            print(f"    Orientation: {section.orientation}")
            print(f"    Largeur: {section.page_width.inches:.2f} pouces")
            print(f"    Hauteur: {section.page_height.inches:.2f} pouces")
            
            # En-tête
            if section.header.paragraphs:
                header_text = " ".join([p.text for p in section.header.paragraphs if p.text.strip()])
                if header_text:
                    print(f"    En-tête: {header_text[:60]}...")
            
            # Pied de page
            if section.footer.paragraphs:
                footer_text = " ".join([p.text for p in section.footer.paragraphs if p.text.strip()])
                if footer_text:
                    print(f"    Pied de page: {footer_text[:60]}...")
        
        # Analyser les paragraphes
        if doc.paragraphs:
            print(f"\n[PARAGRAPHES]")
            for idx, para in enumerate(doc.paragraphs[:10], 1):  # Max 10 premiers
                if para.text.strip():
                    print(f"  {idx}. {para.text[:60]}...")
        
        # Analyser TOUTES les tables en détail
        print(f"\n[TABLES - DÉTAIL COMPLET]")
        for idx, table in enumerate(doc.tables, 1):
            print(f"\n  TABLE {idx}:")
            print(f"    Dimensions: {len(table.rows)} lignes x {len(table.columns)} colonnes")
            
            # Première ligne (en-têtes)
            if table.rows:
                print(f"    En-têtes (ligne 1):")
                for col_idx, cell in enumerate(table.rows[0].cells):
                    text = cell.text.strip()
                    if text:
                        print(f"      Col {col_idx+1}: {text[:40]}")
                
                # Première ligne de données
                if len(table.rows) > 1:
                    print(f"    Données (ligne 2):")
                    for col_idx, cell in enumerate(table.rows[1].cells):
                        text = cell.text.strip()
                        if text:
                            print(f"      Col {col_idx+1}: {text[:40]}")
                
                # Compter les lignes avec données
                data_rows = sum(1 for row in table.rows[1:] 
                               if any(cell.text.strip() for cell in row.cells))
                print(f"    Lignes avec données: {data_rows}")
        
        # Vérifier si le document semble vide
        has_content = False
        
        # Vérifier les tables
        for table in doc.tables:
            for row in table.rows:
                for cell in row.cells:
                    if cell.text.strip():
                        has_content = True
                        break
                if has_content:
                    break
            if has_content:
                break
        
        # Vérifier les paragraphes
        if not has_content:
            for para in doc.paragraphs:
                if para.text.strip():
                    has_content = True
                    break
        
        print("\n" + "="*70)
        if has_content:
            print("[VERDICT] Document contient du contenu visible")
        else:
            print("[VERDICT] Document semble VIDE (pas de texte détecté)")
        print("="*70)
        
    except Exception as e:
        print(f"\n[ERREUR] {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python analyser_word_detaille.py <fichier.docx>")
        sys.exit(1)
    
    analyser_document(sys.argv[1])
