#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
json2word_feuilles_revision_v3.py - Cas 6 (version 3)
Convertit les données de "Feuille de révision" en document Word
avec génération correcte de toutes les tables

Version 3: Reconstruction complète pour générer les 9 tables séparément
"""

import json
import sys
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any

from docx import Document
from docx.shared import Pt, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn


# Couleurs de la charte E-audit pro
BORDEAUX_RGB = RGBColor(123, 30, 58)  # #7B1E3A
LIGHT_RGB = RGBColor(242, 230, 234)    # #F2E6EA
GREY_RGB = RGBColor(153, 153, 153)     # #999999
WHITE_RGB = RGBColor(255, 255, 255)    # #FFFFFF


def set_cell_color(cell, color_rgb):
    """Définit la couleur de fond d'une cellule."""
    shading_elm = OxmlElement('w:shd')
    # RGBColor est un tuple (r, g, b), pas un objet avec des attributs
    r, g, b = color_rgb[0], color_rgb[1], color_rgb[2]
    shading_elm.set(qn('w:fill'), f'{r:02x}{g:02x}{b:02x}')
    cell._element.get_or_add_tcPr().append(shading_elm)


def set_cell_borders(cell, color='CCCCCC', sz='4'):
    """Définit les bordures d'une cellule."""
    tc = cell._element
    tcPr = tc.get_or_add_tcPr()
    
    for border_name in ['top', 'left', 'bottom', 'right']:
        border = OxmlElement(f'w:{border_name}')
        border.set(qn('w:val'), 'single')
        border.set(qn('w:sz'), sz)
        border.set(qn('w:color'), color)
        tcPr.append(border)


def create_table_from_list(doc, data: List[Dict[str, Any]], table_name: str):
    """Crée une table Word à partir d'une liste de dictionnaires."""
    if not data:
        return
    
    # Extraire toutes les colonnes uniques
    columns = []
    for row_data in data:
        for key in row_data.keys():
            if key not in columns:
                columns.append(key)
    
    # Créer la table
    num_rows = len(data) + 1  # +1 pour l'en-tête
    num_cols = len(columns)
    table = doc.add_table(rows=num_rows, cols=num_cols)
    table.style = 'Table Grid'
    
    # Remplir l'en-tête
    header_cells = table.rows[0].cells
    for idx, col_name in enumerate(columns):
        cell = header_cells[idx]
        cell.text = str(col_name)
        set_cell_color(cell, BORDEAUX_RGB)
        # Texte en blanc et gras
        for paragraph in cell.paragraphs:
            for run in paragraph.runs:
                run.font.color.rgb = WHITE_RGB
                run.font.bold = True
                run.font.size = Pt(9)
            paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    # Remplir les données
    for row_idx, row_data in enumerate(data, start=1):
        cells = table.rows[row_idx].cells
        for col_idx, col_name in enumerate(columns):
            value = row_data.get(col_name, '')
            cells[col_idx].text = str(value) if value is not None else ''
            # Format des cellules de données
            for paragraph in cells[col_idx].paragraphs:
                for run in paragraph.runs:
                    run.font.size = Pt(9)
    
    # Ajuster la largeur des colonnes selon le contenu
    for col_idx in range(num_cols):
        # Calculer la largeur max nécessaire
        max_width = max(len(str(data[row_idx].get(columns[col_idx], ''))) 
                       for row_idx in range(len(data)))
        max_width = max(max_width, len(columns[col_idx]))
        # Limiter entre 0.5 et 3 pouces
        width = min(max(0.5, max_width * 0.1), 3.0)
        for row in table.rows:
            row.cells[col_idx].width = Inches(width)
    
    doc.add_paragraph()  # Espacement après la table


def create_table_from_dict(doc, data: Dict[str, Any], table_name: str):
    """Crée une table Word verticale à partir d'un dictionnaire."""
    if not data:
        return
    
    # Créer une table 2 colonnes (clé | valeur)
    table = doc.add_table(rows=len(data), cols=2)
    table.style = 'Table Grid'
    
    for row_idx, (key, value) in enumerate(data.items()):
        # Cellule de clé
        key_cell = table.rows[row_idx].cells[0]
        key_cell.text = str(key)
        set_cell_color(key_cell, LIGHT_RGB)
        for paragraph in key_cell.paragraphs:
            for run in paragraph.runs:
                run.font.bold = True
                run.font.size = Pt(9)
        
        # Cellule de valeur
        value_cell = table.rows[row_idx].cells[1]
        value_cell.text = str(value) if value is not None else ''
        for paragraph in value_cell.paragraphs:
            for run in paragraph.runs:
                run.font.size = Pt(9)
    
    doc.add_paragraph()  # Espacement après la table


def generate_word_document(data: List[Dict], output_file: Path):
    """Génère le document Word avec toutes les tables."""
    doc = Document()
    
    # Configuration de la page
    section = doc.sections[0]
    section.page_height = Inches(11.69)  # A4
    section.page_width = Inches(8.27)
    section.left_margin = Inches(0.5)
    section.right_margin = Inches(0.5)
    section.top_margin = Inches(0.75)
    section.bottom_margin = Inches(0.75)
    
    # Parcourir tous les éléments du JSON
    for item in data:
        for table_key, table_data in item.items():
            # Ajouter un titre pour la table
            title = doc.add_heading(table_key, level=2)
            title_run = title.runs[0]
            title_run.font.color.rgb = BORDEAUX_RGB
            title_run.font.size = Pt(12)
            
            # Générer la table selon son type
            if isinstance(table_data, list):
                if table_data and isinstance(table_data[0], dict):
                    # Liste de dictionnaires -> table horizontale
                    create_table_from_list(doc, table_data, table_key)
                else:
                    # Liste simple -> à ignorer ou traiter différemment
                    pass
            elif isinstance(table_data, dict):
                # Dictionnaire -> table verticale
                create_table_from_dict(doc, table_data, table_key)
    
    # Sauvegarder
    doc.save(str(output_file))
    return output_file


def main():
    """Point d'entrée principal."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Convertit un JSON de feuilles de révision en document Word (.docx)"
    )
    parser.add_argument("json_file", help="Chemin vers le fichier JSON d'entrée")
    parser.add_argument("-o", "--out-dir", default=".", help="Dossier de sortie")
    
    args = parser.parse_args()
    
    json_path = Path(args.json_file)
    if not json_path.exists():
        print(f"[ERREUR] : Le fichier {json_path} n'existe pas.")
        return False
    
    # Charger le JSON
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            raw_data = json.load(f)
    except Exception as e:
        print(f"[ERREUR] Lecture JSON : {e}", file=sys.stderr)
        return False
    
    # Extraire les données réelles
    data = raw_data
    if isinstance(raw_data, dict):
        for key in raw_data.keys():
            if "Etape mission" in key or "Feuille revision" in key:
                data = raw_data[key]
                break
    
    if not isinstance(data, list):
        print(f"[ERREUR] Format de donnees inattendu : {type(data)}")
        return False
    
    # Déterminer le dossier de sortie
    out_path = Path(args.out_dir)
    out_path.mkdir(parents=True, exist_ok=True)
    
    # Générer un nom de fichier
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = out_path / f"Cas6_{timestamp}.docx"
    
    try:
        generate_word_document(data, output_file)
        print(f"[OK] Document genere : {output_file}")
        return True
    except Exception as e:
        print(f"[ERREUR] Conversion : {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
