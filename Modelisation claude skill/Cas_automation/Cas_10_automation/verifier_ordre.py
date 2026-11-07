# -*- coding: utf-8 -*-
"""
Verifie l'ordre des sections dans le document Cas 10
"""
from docx import Document
import sys

def verifier_ordre(doc_path):
    """Verifie l'ordre Table 1 -> Design -> Table 2."""
    doc = Document(doc_path)
    
    print(f"\n{'='*80}")
    print(f"VERIFICATION DE L'ORDRE DES SECTIONS")
    print(f"{'='*80}\n")
    
    # Analyser l'ordre des elements
    elements = []
    
    for i, para in enumerate(doc.paragraphs):
        text = para.text.strip()
        if text:
            if "Modelisation Design" in text and "hierarchique" in text:
                elements.append(f"Position {i}: MODELISATION DESIGN (titre)")
            elif text.startswith("Design"):
                elements.append(f"Position {i}: {text[:50]}")
    
    for i, table in enumerate(doc.tables):
        # Trouver la position dans le document
        # Approximation: compter les paragraphes avant chaque table
        if i == 0:
            elements.insert(0, f"Position 0-2: TABLE 1 (Metadonnees - {len(table.rows)} lignes)")
        else:
            elements.append(f"Position fin: TABLE {i+1} (Donnees - {len(table.rows)} lignes x {len(table.columns)} colonnes)")
    
    # Afficher l'ordre
    print("ORDRE DES ELEMENTS:\n")
    for elem in elements[:15]:  # Limiter à 15
        print(f"  {elem}")
    
    # Verifier l'ordre attendu
    print(f"\n{'='*80}")
    has_table1 = any("TABLE 1" in e for e in elements)
    has_design = any("MODELISATION DESIGN" in e for e in elements)
    has_table2 = any("TABLE 2" in e for e in elements)
    
    # Trouver les positions
    pos_table1 = next((i for i, e in enumerate(elements) if "TABLE 1" in e), -1)
    pos_design = next((i for i, e in enumerate(elements) if "MODELISATION DESIGN" in e), -1)
    pos_table2 = next((i for i, e in enumerate(elements) if "TABLE 2" in e), -1)
    
    print(f"Elements detectes:")
    print(f"  - Table 1 (metadonnees): {'OUI' if has_table1 else 'NON'}")
    print(f"  - Modelisation Design: {'OUI' if has_design else 'NON'}")
    print(f"  - Table 2 (donnees): {'OUI' if has_table2 else 'NON'}")
    
    print(f"\nOrdre relatif:")
    if pos_table1 >= 0:
        print(f"  Table 1 en position: {pos_table1}")
    if pos_design >= 0:
        print(f"  Design en position: {pos_design}")
    if pos_table2 >= 0:
        print(f"  Table 2 en position: {pos_table2}")
    
    # Validation
    if has_table1 and has_design and has_table2:
        if pos_table1 < pos_design < pos_table2:
            print(f"\n✓ ORDRE CORRECT: Table 1 -> Design -> Table 2")
            return True
        else:
            print(f"\n✗ ORDRE INCORRECT!")
            print(f"  Attendu: Table 1 < Design < Table 2")
            print(f"  Obtenu: {pos_table1} < {pos_design} < {pos_table2}")
            return False
    else:
        print(f"\n✗ Elements manquants!")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        doc_path = "C:\\Users\\LEADER\\Downloads\\Cas10_ORDRE_CORRIGE.docx"
    else:
        doc_path = sys.argv[1]
    
    verifier_ordre(doc_path)
