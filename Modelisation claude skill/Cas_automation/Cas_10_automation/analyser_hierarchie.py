# -*- coding: utf-8 -*-
"""
Analyse detaillee de la structure hierarchique des designs dans Cas 10
"""
from docx import Document
import sys

def analyser_hierarchie(doc_path):
    """Analyse la structure hierarchique des paragraphes."""
    doc = Document(doc_path)
    
    print(f"\n{'='*80}")
    print(f"ANALYSE HIERARCHIQUE - MODELISATION DESIGN")
    print(f"{'='*80}\n")
    
    in_design_section = False
    current_design = None
    
    for i, para in enumerate(doc.paragraphs):
        text = para.text.strip()
        
        # Detecter le debut de la section Modelisation Design
        if "Modelisation Design" in text and "hierarchique" in text:
            in_design_section = True
            print(f"\n{text}")
            print("-" * 80)
            continue
        
        if in_design_section and text:
            # Detecter les designs
            if text.startswith("Design"):
                current_design = text
                print(f"\n{text}")
                print("~" * 60)
                continue
            
            # Afficher les paragraphes avec leur indentation et style
            if current_design:
                # Recuperer le style du paragraphe
                runs = para.runs
                if runs:
                    run = runs[0]
                    bold = run.bold
                    italic = run.italic
                    color = None
                    if run.font.color and run.font.color.rgb:
                        r = run.font.color.rgb[0]
                        g = run.font.color.rgb[1]
                        b = run.font.color.rgb[2]
                        color = f"#{r:02x}{g:02x}{b:02x}"
                    
                    # Afficher avec formatage
                    prefix = ""
                    if bold and color and "7b1e3a" in color.lower():
                        prefix = "[N1-BORDEAUX] "
                    elif bold and color and "c4a4b0" in color.lower():
                        prefix = "[N2-LIGHT] "
                    elif color and "f2f2f2" in color.lower():
                        prefix = "[N3-GRAY] "
                    elif italic:
                        prefix = "[N4-ITALIC] "
                    
                    # Compter l'indentation
                    indent_count = text.count("  ") if text.startswith("  ") else 0
                    indent = "  " * min(indent_count, 4)
                    
                    print(f"{indent}{prefix}{text[:80]}")
    
    print(f"\n{'='*80}")
    print(f"FIN DE L'ANALYSE")
    print(f"{'='*80}\n")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python analyser_hierarchie.py <fichier.docx>")
        sys.exit(1)
    
    analyser_hierarchie(sys.argv[1])
