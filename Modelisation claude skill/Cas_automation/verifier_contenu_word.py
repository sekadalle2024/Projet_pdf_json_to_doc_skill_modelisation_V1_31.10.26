#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de vérification du contenu des fichiers Word.
Compte les paragraphes et tableaux pour détecter les fichiers vides.
"""

from pathlib import Path
from docx import Document
import sys

def analyser_word(filepath):
    """Analyse un fichier Word et affiche son contenu."""
    try:
        doc = Document(filepath)
        
        print(f"\n{'='*70}")
        print(f"📄 Fichier: {Path(filepath).name}")
        print(f"{'='*70}")
        
        # Compter les paragraphes non vides
        paragraphes = [p for p in doc.paragraphs if p.text.strip()]
        print(f"📝 Paragraphes: {len(paragraphes)}")
        
        # Compter les tableaux
        tableaux = doc.tables
        print(f"📊 Tableaux: {len(tableaux)}")
        
        # Afficher les premiers paragraphes
        if paragraphes:
            print(f"\n✅ Premiers paragraphes:")
            for i, p in enumerate(paragraphes[:5]):
                text = p.text[:100]
                print(f"   {i+1}. {text}...")
        else:
            print(f"\n❌ Aucun paragraphe trouvé")
        
        # Afficher les tableaux
        if tableaux:
            print(f"\n✅ Tableaux trouvés:")
            for i, table in enumerate(tableaux[:3]):
                rows = len(table.rows)
                cols = len(table.columns)
                print(f"   {i+1}. Tableau {rows}x{cols}")
                
                # Première cellule
                if table.rows:
                    first_cell = table.rows[0].cells[0].text[:50]
                    print(f"      Première cellule: {first_cell}...")
        else:
            print(f"\n❌ Aucun tableau trouvé")
        
        # Verdict
        print(f"\n{'='*70}")
        if len(paragraphes) > 5 or len(tableaux) > 0:
            print(f"✅ VERDICT: Document contient des données")
        else:
            print(f"❌ VERDICT: Document probablement vide")
        print(f"{'='*70}\n")
        
        return len(tableaux) > 0
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python verifier_contenu_word.py <fichier.docx>")
        sys.exit(1)
    
    filepath = sys.argv[1]
    has_content = analyser_word(filepath)
    sys.exit(0 if has_content else 1)
