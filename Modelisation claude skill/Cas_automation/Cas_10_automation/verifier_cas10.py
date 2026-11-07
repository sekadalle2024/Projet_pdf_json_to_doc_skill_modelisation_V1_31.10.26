# -*- coding: utf-8 -*-
"""
Verification rapide du contenu du document Cas 10
"""
from docx import Document
import sys

def verifier_document(doc_path):
    """Verifie le contenu d'un document Word."""
    doc = Document(doc_path)
    
    print(f"\n{'='*80}")
    print(f"ANALYSE DU DOCUMENT: {doc_path}")
    print(f"{'='*80}\n")
    
    # Compter les paragraphes
    print(f"Nombre de paragraphes: {len(doc.paragraphs)}")
    
    # Compter les tables
    print(f"Nombre de tables: {len(doc.tables)}")
    
    # Analyser chaque table
    for i, table in enumerate(doc.tables):
        print(f"\n--- Table {i} ---")
        print(f"  Lignes: {len(table.rows)}")
        print(f"  Colonnes: {len(table.columns)}")
        
        # Premiere ligne (en-tete)
        if table.rows:
            first_row = table.rows[0]
            headers = [cell.text.strip() for cell in first_row.cells]
            print(f"  En-tetes: {headers}")
        
        # Afficher les 2 premieres lignes de donnees
        if len(table.rows) > 1:
            print(f"  Premiere ligne de donnees:")
            for j, cell in enumerate(table.rows[1].cells):
                text = cell.text.strip()[:50]  # Limiter a 50 caracteres
                print(f"    Col {j}: {text}")
    
    # Chercher les sections Modelisation design
    print(f"\n{'='*80}")
    print(f"SECTIONS MODELISATION DESIGN")
    print(f"{'='*80}\n")
    
    found_modelisation = False
    for para in doc.paragraphs:
        text = para.text.strip()
        if "Modelisation" in text or "Design" in text or "hierarchique" in text:
            found_modelisation = True
            print(f"  - {text}")
    
    if not found_modelisation:
        print("  Aucune section Modelisation design trouvee dans les paragraphes.")
        print("  Cela peut etre normal si les designs sont dans les tables.")
    
    print(f"\n{'='*80}")
    print(f"FIN DE L'ANALYSE")
    print(f"{'='*80}\n")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python verifier_cas10.py <fichier.docx>")
        sys.exit(1)
    
    verifier_document(sys.argv[1])
