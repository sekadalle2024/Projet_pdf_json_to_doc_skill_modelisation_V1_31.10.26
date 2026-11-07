# -*- coding: utf-8 -*-
"""
Extrait SEULEMENT la section Modelisation Design vers un nouveau document
"""
from docx import Document
import sys

def extraire_design_section(source_path, target_path):
    """Extrait la section design vers un nouveau document."""
    source_doc = Document(source_path)
    target_doc = Document()
    
    # Trouver le debut de la section design
    start_index = None
    for i, para in enumerate(source_doc.paragraphs):
        if "Modelisation Design" in para.text and "hierarchique" in para.text:
            start_index = i
            break
    
    if start_index is None:
        print("Section Modelisation Design introuvable !")
        return False
    
    print(f"Section trouvee au paragraphe {start_index}")
    print(f"Total paragraphes: {len(source_doc.paragraphs)}")
    print(f"Paragraphes a copier: {len(source_doc.paragraphs) - start_index}")
    
    # Copier tous les paragraphes depuis start_index
    copied = 0
    for para in source_doc.paragraphs[start_index:]:
        # Copier le paragraphe
        new_para = target_doc.add_paragraph()
        
        # Copier l'alignement
        new_para.alignment = para.alignment
        
        # Copier l'indentation
        new_para.paragraph_format.left_indent = para.paragraph_format.left_indent
        
        # Copier le fond (shading) - skip si erreur
        try:
            if para._p.pPr is not None:
                pPr = para._p.pPr
                for child in pPr:
                    if 'shd' in child.tag:
                        # Copier l'element shading
                        new_para._p.get_or_add_pPr().append(child)
                        break
        except:
            pass
        
        # Copier les runs avec leur formatage
        for run in para.runs:
            new_run = new_para.add_run(run.text)
            new_run.font.name = run.font.name
            new_run.font.size = run.font.size
            new_run.font.bold = run.bold
            new_run.font.italic = run.italic
            if run.font.color and run.font.color.rgb:
                new_run.font.color.rgb = run.font.color.rgb
        
        copied += 1
    
    # Sauvegarder
    target_doc.save(target_path)
    print(f"\nDocument extrait sauvegarde: {target_path}")
    print(f"Paragraphes copies: {copied}")
    return True

if __name__ == "__main__":
    source = "C:\\Users\\LEADER\\Downloads\\Cas10_20261107_212015.docx"
    target = "C:\\Users\\LEADER\\Downloads\\DESIGN_SECTION_ONLY.docx"
    
    extraire_design_section(source, target)
