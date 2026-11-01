#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
verify_document_structure.py
============================
Vérifie la structure d'un document Word généré pour Cas 14.

Usage:
    python verify_document_structure.py <fichier.docx>
"""

import sys
from pathlib import Path
from docx import Document

def verify_document(docx_path):
    """Vérifie la structure d'un document Word"""
    
    print(f"\n{'='*70}")
    print(f"  VÉRIFICATION STRUCTURE DOCUMENT CAS 14")
    print(f"{'='*70}\n")
    print(f"Fichier : {docx_path.name}")
    print(f"Taille : {docx_path.stat().st_size / 1024:.2f} KB\n")
    
    try:
        doc = Document(str(docx_path))
        
        # Vérifier orientation
        section = doc.sections[0]
        width_inches = section.page_width.inches
        height_inches = section.page_height.inches
        is_landscape = width_inches > height_inches
        
        print(f"✅ Document ouvert avec succès\n")
        print(f"{'─'*70}")
        print(f"ORIENTATION")
        print(f"{'─'*70}")
        print(f"  Largeur  : {width_inches:.2f} pouces")
        print(f"  Hauteur  : {height_inches:.2f} pouces")
        print(f"  Format   : {'✅ Paysage' if is_landscape else '❌ Portrait'}\n")
        
        # Compter les tables
        num_tables = len(doc.tables)
        print(f"{'─'*70}")
        print(f"TABLES")
        print(f"{'─'*70}")
        print(f"  Nombre total : {num_tables}")
        
        if num_tables >= 6:
            print(f"  ✅ Au moins 6 tables présentes\n")
        else:
            print(f"  ❌ Nombre de tables insuffisant (attendu : 6)\n")
        
        # Analyser chaque table
        for idx, table in enumerate(doc.tables, start=1):
            num_rows = len(table.rows)
            num_cols = len(table.columns)
            print(f"\n  Table {idx}:")
            print(f"    Lignes   : {num_rows}")
            print(f"    Colonnes : {num_cols}")
            
            if idx == 1:
                # Table 1 doit être verticale (2 colonnes)
                if num_cols == 2:
                    print(f"    ✅ Format vertical (2 colonnes)")
                    
                    # Vérifier la couleur de fond (approximatif)
                    # Note: python-docx ne permet pas facilement de lire les couleurs
                    print(f"    ⚠️  Couleur bordeaux à vérifier manuellement dans Word")
                else:
                    print(f"    ❌ Format incorrect (attendu : 2 colonnes)")
            
            elif idx <= 6:
                # Tables 2-6 : format horizontal (1 ou plusieurs colonnes)
                print(f"    ✅ Table de contenu")
        
        # Vérifier en-tête et pied de page
        print(f"\n{'─'*70}")
        print(f"EN-TÊTE ET PIED DE PAGE")
        print(f"{'─'*70}")
        
        if section.header:
            header_text = section.header.paragraphs[0].text if section.header.paragraphs else ""
            print(f"  En-tête : {header_text[:60]}...")
            if "E-audit pro" in header_text or "Logiciel automatisé" in header_text:
                print(f"  ✅ En-tête conforme")
            else:
                print(f"  ❌ En-tête non conforme")
        
        if section.footer:
            footer_text = section.footer.paragraphs[0].text if section.footer.paragraphs else ""
            print(f"  Pied de page : {footer_text[:60]}...")
            if "WhatsApp" in footer_text or "Whatsapp" in footer_text:
                print(f"  ✅ Pied de page conforme")
            else:
                print(f"  ❌ Pied de page non conforme")
        
        # Résumé
        print(f"\n{'='*70}")
        print(f"RÉSUMÉ DE LA VÉRIFICATION")
        print(f"{'='*70}\n")
        
        checks = [
            ("Document ouvrable", True),
            ("Orientation paysage", is_landscape),
            ("6 tables présentes", num_tables >= 6),
            ("Table 1 : 2 colonnes", doc.tables[0] and len(doc.tables[0].columns) == 2 if doc.tables else False),
            ("En-tête présent", bool(section.header and section.header.paragraphs)),
            ("Pied de page présent", bool(section.footer and section.footer.paragraphs)),
        ]
        
        passed = sum(1 for _, check in checks if check)
        total = len(checks)
        
        for name, check in checks:
            status = "✅" if check else "❌"
            print(f"  {status} {name}")
        
        print(f"\n  Score : {passed}/{total} ({passed/total*100:.0f}%)")
        
        if passed == total:
            print(f"\n  🎉 TOUTES LES VÉRIFICATIONS RÉUSSIES !\n")
            return 0
        else:
            print(f"\n  ⚠️  Certaines vérifications ont échoué\n")
            return 1
        
    except Exception as e:
        print(f"\n❌ ERREUR : {e}\n")
        import traceback
        traceback.print_exc()
        return 1


def main():
    if len(sys.argv) < 2:
        print("Usage: python verify_document_structure.py <fichier.docx>")
        return 1
    
    docx_path = Path(sys.argv[1])
    
    if not docx_path.exists():
        print(f"❌ Erreur : Le fichier {docx_path} n'existe pas.")
        return 1
    
    return verify_document(docx_path)


if __name__ == "__main__":
    sys.exit(main())
