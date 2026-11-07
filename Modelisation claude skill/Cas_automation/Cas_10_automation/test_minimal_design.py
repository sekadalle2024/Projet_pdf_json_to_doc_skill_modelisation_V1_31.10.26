# -*- coding: utf-8 -*-
"""
Test minimal de la structure hierarchique pour debug
"""
from docx import Document
from docx.shared import Pt, RGBColor, Twips
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

def _set_paragraph_shading(paragraph, fill_color):
    """Applique un fond coloré à un paragraphe via XML."""
    pPr = paragraph._p.get_or_add_pPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:fill"), fill_color)
    pPr.append(shd)

# Creer un document
doc = Document()

# Titre
p = doc.add_paragraph()
run = p.add_run("TEST - Modélisation Design Hiérarchique")
run.font.name = "Calibri"
run.font.size = Pt(16)
run.font.bold = True
run.font.color.rgb = RGBColor(123, 30, 58)  # Bordeaux

# Ligne vide
doc.add_paragraph()

# Design 1 - Structure linéaire
p = doc.add_paragraph()
run = p.add_run("Design 1 - Test Structure Linéaire")
run.font.name = "Calibri"
run.font.size = Pt(12)
run.font.bold = True

# Niveau 1: Bordeaux
p = doc.add_paragraph()
p.paragraph_format.left_indent = Twips(200)
_set_paragraph_shading(p, "7B1E3A")
run = p.add_run("|- Niveau 1: Cycle")
run.font.name = "Calibri"
run.font.size = Pt(11)
run.font.bold = True
run.font.color.rgb = RGBColor(255, 255, 255)

# Niveau 2: Light Bordeaux
p = doc.add_paragraph()
p.paragraph_format.left_indent = Twips(400)
_set_paragraph_shading(p, "C4A4B0")
run = p.add_run("|- Niveau 2: Processus")
run.font.name = "Calibri"
run.font.size = Pt(10)
run.font.bold = True
run.font.color.rgb = RGBColor(0, 0, 0)

# Niveau 3: Gray
p = doc.add_paragraph()
p.paragraph_format.left_indent = Twips(600)
_set_paragraph_shading(p, "F2F2F2")
run = p.add_run("|- Niveau 3: Tâches")
run.font.name = "Calibri"
run.font.size = Pt(10)
run.font.bold = False
run.font.color.rgb = RGBColor(0, 0, 0)

# Niveau 4: Italic
p = doc.add_paragraph()
p.paragraph_format.left_indent = Twips(800)
run = p.add_run("'- Niveau 4: Documents")
run.font.name = "Calibri"
run.font.size = Pt(9)
run.font.italic = True
run.font.color.rgb = RGBColor(153, 153, 153)

# Colonnes
p = doc.add_paragraph()
p.paragraph_format.left_indent = Twips(200)
_set_paragraph_shading(p, "F2F2F2")
run = p.add_run("Colonnes: Cycle, Processus, Tâches, Documents")
run.font.name = "Calibri"
run.font.size = Pt(9)
run.font.color.rgb = RGBColor(0, 0, 0)

# Ligne vide
doc.add_paragraph()

# Design 2 - Structure branchée
p = doc.add_paragraph()
run = p.add_run("Design 2 - Test Structure Branchée")
run.font.name = "Calibri"
run.font.size = Pt(12)
run.font.bold = True

# Niveau 1
p = doc.add_paragraph()
p.paragraph_format.left_indent = Twips(200)
_set_paragraph_shading(p, "7B1E3A")
run = p.add_run("|- Niveau 1: Preuve et responsabilité")
run.font.name = "Calibri"
run.font.size = Pt(11)
run.font.bold = True
run.font.color.rgb = RGBColor(255, 255, 255)

# Niveau 2 branches
p = doc.add_paragraph()
p.paragraph_format.left_indent = Twips(200)
_set_paragraph_shading(p, "C4A4B0")
run = p.add_run("|- Niveau 2 (branches):")
run.font.name = "Calibri"
run.font.size = Pt(10)
run.font.bold = True
run.font.color.rgb = RGBColor(0, 0, 0)

# Branches
p = doc.add_paragraph()
p.paragraph_format.left_indent = Twips(400)
_set_paragraph_shading(p, "C4A4B0")
run = p.add_run("     |- Preuve")
run.font.name = "Calibri"
run.font.size = Pt(10)
run.font.bold = True
run.font.color.rgb = RGBColor(0, 0, 0)

p = doc.add_paragraph()
p.paragraph_format.left_indent = Twips(400)
_set_paragraph_shading(p, "C4A4B0")
run = p.add_run("     |- Responsabilité et calendrier")
run.font.name = "Calibri"
run.font.size = Pt(10)
run.font.bold = True
run.font.color.rgb = RGBColor(0, 0, 0)

# Niveau 3 details
p = doc.add_paragraph()
p.paragraph_format.left_indent = Twips(200)
_set_paragraph_shading(p, "F2F2F2")
run = p.add_run("'- Niveau 3 (details par branche):")
run.font.name = "Calibri"
run.font.size = Pt(10)
run.font.color.rgb = RGBColor(0, 0, 0)

p = doc.add_paragraph()
p.paragraph_format.left_indent = Twips(600)
_set_paragraph_shading(p, "F2F2F2")
run = p.add_run("     |- Preuve -> Document, X-ref")
run.font.name = "Calibri"
run.font.size = Pt(10)
run.font.color.rgb = RGBColor(0, 0, 0)

p = doc.add_paragraph()
p.paragraph_format.left_indent = Twips(600)
_set_paragraph_shading(p, "F2F2F2")
run = p.add_run("     |- Responsabilité -> Propriétaire, Périodicité")
run.font.name = "Calibri"
run.font.size = Pt(10)
run.font.color.rgb = RGBColor(0, 0, 0)

# Sauvegarder
output_path = "C:\\Users\\LEADER\\Downloads\\Test_Hierarchie_Design.docx"
doc.save(output_path)
print(f"Document test créé: {output_path}")
