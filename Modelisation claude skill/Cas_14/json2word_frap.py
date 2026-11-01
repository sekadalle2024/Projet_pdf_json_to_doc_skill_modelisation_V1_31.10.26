#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
json2word_frap.py
=================
Transforme un JSON de FRAP (Fiche de Révélation et d'Analyse de Problème) et
Recommandations en document Word (.docx) au style E-audit pro.

INSTALLATION ET UTILISATION
---------------------------
    pip install python-docx
    python json2word_frap.py donnees.json -o ./sortie_word_cas14

Autres exemples :
    python json2word_frap.py exemple_frap_minimal.json
    python json2word_frap.py exemple_frap_complet.json --software "Logiciel automatisé E-audit pro"

OPTIONS DISPONIBLES
-------------------
    --software          nom du logiciel (en-tête et nom fichier)
    --footer            texte du pied de page
    -o / --out-dir      dossier de sortie

CE QUE FAIT LE SCRIPT
---------------------
  * Lecture du JSON avec support de structures imbriquées Data_integrale
  * Table 1 : format VERTICAL (2 colonnes : Rubrique | Description)
    - Colonne 1 : fond bordeaux #8B0000 (UNIQUE à Cas 14), texte blanc gras
    - Colonne 2 : texte noir
  * Tables 2-6 : format HORIZONTAL (1 colonne par table)
    - En-tête : fond bordeaux #8B0000, texte blanc gras
    - Contenu : puces automatiques pour textes multiligne
  * Orientation : A4 Paysage
  * En-tête : fond bordeaux avec texte blanc
  * Pied de page : contact WhatsApp centré
  * Nom du fichier : <Reference>-<Etape_de_mission>- Logiciel automatisé E-audit pro_<timestamp>.docx

VALIDATION
----------
  Testé avec exemple_frap_minimal.json et exemple_frap_complet.json
  Vérifie : 6 tables, orientation paysage, fond bordeaux colonne 1 table 1
"""

import argparse
import json
import random
import re
import string
import sys
from datetime import datetime
from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor

# ──────────────────────────────────────────────────────────────────────────────
# CONFIGURATION
# ──────────────────────────────────────────────────────────────────────────────

# Couleur bordeaux #8B0000 (UNIQUE à Cas 14)
BORDEAUX_RGB = RGBColor(0x8B, 0x00, 0x00)
WHITE_RGB = RGBColor(0xFF, 0xFF, 0xFF)
BLACK_RGB = RGBColor(0x00, 0x00, 0x00)

DEFAULT_SOFTWARE = "Logiciel automatisé E-audit pro"
DEFAULT_FOOTER = "Automatisez vos activités d'audit, risques et contrôles - Whatsapp : + 225 05 44 13 07 98"

# ──────────────────────────────────────────────────────────────────────────────
# FONCTIONS UTILITAIRES
# ──────────────────────────────────────────────────────────────────────────────

def extract_json_from_text(text: str):
    """
    Extrait le premier objet JSON trouvé dans une chaîne de caractères.
    
    Args:
        text: Texte contenant du JSON
        
    Returns:
        dict: Objet JSON parsé ou None
    """
    pattern = r'\{(?:[^{}]|(?:\{(?:[^{}]|(?:\{[^{}]*\}))*\}))*\}'
    match = re.search(pattern, text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(0))
        except json.JSONDecodeError:
            pass
    return None


def generate_reference():
    """
    Génère une référence aléatoire (format: AUTO-HHMMSS).
    
    Returns:
        str: Référence générée
    """
    now = datetime.now()
    return f"AUTO-{now.strftime('%H%M%S')}"


def set_cell_background(cell, color_hex):
    """
    Définit la couleur de fond d'une cellule.
    
    Args:
        cell: Cellule de tableau
        color_hex: Couleur en format hexadécimal (ex: '8B0000')
    """
    shading_elm = OxmlElement('w:shd')
    shading_elm.set(qn('w:fill'), color_hex)
    cell._element.get_or_add_tcPr().append(shading_elm)


def set_cell_border(cell, **kwargs):
    """
    Définit les bordures d'une cellule.
    
    Args:
        cell: Cellule de tableau
        **kwargs: top, bottom, left, right (tuples (size, color_hex) ou None)
    """
    tc = cell._element
    tcPr = tc.get_or_add_tcPr()
    tcBorders = OxmlElement('w:tcBorders')

    for border_name in ['top', 'bottom', 'left', 'right']:
        if border_name in kwargs:
            border_val = kwargs[border_name]
            if border_val is None:
                continue
            border_elm = OxmlElement(f'w:{border_name}')
            border_elm.set(qn('w:val'), 'single')
            border_elm.set(qn('w:sz'), str(border_val[0]))
            color_hex = border_val[1]
            border_elm.set(qn('w:color'), color_hex)
            tcBorders.append(border_elm)

    tcPr.append(tcBorders)


def format_value_as_text(value):
    """
    Convertit une valeur (dict, list, str) en texte avec puces si nécessaire.
    
    Args:
        value: Valeur à formater
        
    Returns:
        str: Texte formaté
    """
    if isinstance(value, dict):
        lines = []
        for k, v in value.items():
            lines.append(f"- {k}: {format_value_as_text(v)}")
        return "\n".join(lines)
    elif isinstance(value, list):
        return "\n".join([f"- {format_value_as_text(item)}" for item in value])
    else:
        return str(value)


def add_bulleted_lines(paragraph, text):
    """
    Ajoute des lignes avec puces dans un paragraphe.
    
    Args:
        paragraph: Paragraphe docx
        text: Texte avec retours à la ligne
    """
    lines = text.split('\n')
    for i, line in enumerate(lines):
        if i > 0:
            paragraph.add_run('\n')
        # Ajouter puce si la ligne commence par "-"
        line_stripped = line.strip()
        if line_stripped.startswith('-'):
            # Utiliser un bullet point Unicode
            paragraph.add_run('• ' + line_stripped[1:].strip())
        else:
            paragraph.add_run(line_stripped)


# ──────────────────────────────────────────────────────────────────────────────
# CRÉATION DES TABLES
# ──────────────────────────────────────────────────────────────────────────────

def create_vertical_table(doc, data_dict, software_name, etape_mission):
    """
    Crée la Table 1 en format VERTICAL (2 colonnes: Rubrique | Description).
    
    SPÉCIFICITÉ CAS 14: Colonne 1 avec fond BORDEAUX #8B0000.
    
    Args:
        doc: Document Word
        data_dict: Dictionnaire des données
        software_name: Nom du logiciel
        etape_mission: Étape de mission
        
    Returns:
        Table: Table créée
    """
    table = doc.add_table(rows=len(data_dict), cols=2)
    table.style = 'Table Grid'
    
    # Largeurs des colonnes (en twips)
    # Colonne 1 : 4000 twips, Colonne 2 : 11038 twips
    col_widths = [4000, 11038]
    
    for row_idx, (key, value) in enumerate(data_dict.items()):
        row_cells = table.rows[row_idx].cells
        
        # Colonne 1 : Rubrique (fond bordeaux #8B0000, texte blanc gras)
        cell_rubrique = row_cells[0]
        cell_rubrique.width = Inches(col_widths[0] / 1440)
        cell_rubrique.text = key
        
        set_cell_background(cell_rubrique, '8B0000')
        for paragraph in cell_rubrique.paragraphs:
            for run in paragraph.runs:
                run.font.bold = True
                run.font.color.rgb = WHITE_RGB
                run.font.name = 'Arial'
                run.font.size = Pt(8.5)
        
        # Colonne 2 : Description (fond blanc, texte noir)
        cell_description = row_cells[1]
        cell_description.width = Inches(col_widths[1] / 1440)
        cell_description.text = ""
        
        formatted_value = format_value_as_text(value)
        paragraph = cell_description.paragraphs[0]
        add_bulleted_lines(paragraph, formatted_value)
        
        for run in paragraph.runs:
            run.font.name = 'Arial'
            run.font.size = Pt(8.5)
            run.font.color.rgb = BLACK_RGB
    
    return table


def create_horizontal_table(doc, data_list_or_dict, table_name):
    """
    Crée une table horizontale (Tables 2-6) en format 1 colonne.
    
    Args:
        doc: Document Word
        data_list_or_dict: Données (dict ou list)
        table_name: Nom de la table (ex: "table 2")
        
    Returns:
        Table: Table créée
    """
    # Gérer les dictionnaires à clé unique (format: {"Intitule": "Texte..."})
    if isinstance(data_list_or_dict, dict):
        # Extraire la clé et la valeur
        if len(data_list_or_dict) == 1:
            header_key = list(data_list_or_dict.keys())[0]
            content_value = list(data_list_or_dict.values())[0]
            
            # Créer une table 2 lignes x 1 colonne
            table = doc.add_table(rows=2, cols=1)
            table.style = 'Table Grid'
            
            # En-tête
            header_cell = table.rows[0].cells[0]
            header_cell.text = header_key
            set_cell_background(header_cell, '8B0000')
            for paragraph in header_cell.paragraphs:
                for run in paragraph.runs:
                    run.font.bold = True
                    run.font.color.rgb = WHITE_RGB
                    run.font.name = 'Arial'
                    run.font.size = Pt(8.5)
                paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
            
            # Contenu
            content_cell = table.rows[1].cells[0]
            content_cell.text = ""
            paragraph = content_cell.paragraphs[0]
            
            # Formater le contenu avec puces si multiligne
            content_text = format_value_as_text(content_value)
            add_bulleted_lines(paragraph, content_text)
            
            for run in paragraph.runs:
                run.font.name = 'Arial'
                run.font.size = Pt(8.5)
                run.font.color.rgb = BLACK_RGB
            
            return table
        
        else:
            # Dictionnaire multi-clés : format vertical
            table = doc.add_table(rows=len(data_list_or_dict), cols=2)
            table.style = 'Table Grid'
            
            for row_idx, (key, value) in enumerate(data_list_or_dict.items()):
                row_cells = table.rows[row_idx].cells
                
                # En-tête (clé)
                header_cell = row_cells[0]
                header_cell.text = key
                set_cell_background(header_cell, '8B0000')
                for paragraph in header_cell.paragraphs:
                    for run in paragraph.runs:
                        run.font.bold = True
                        run.font.color.rgb = WHITE_RGB
                        run.font.name = 'Arial'
                        run.font.size = Pt(8.5)
                
                # Contenu (valeur)
                content_cell = row_cells[1]
                content_cell.text = ""
                paragraph = content_cell.paragraphs[0]
                
                content_text = format_value_as_text(value)
                add_bulleted_lines(paragraph, content_text)
                
                for run in paragraph.runs:
                    run.font.name = 'Arial'
                    run.font.size = Pt(8.5)
                    run.font.color.rgb = BLACK_RGB
            
            return table
    
    elif isinstance(data_list_or_dict, list):
        # Liste d'objets : format horizontal multi-colonnes
        if not data_list_or_dict:
            return None
        
        # Déterminer les colonnes
        all_keys = set()
        for item in data_list_or_dict:
            if isinstance(item, dict):
                all_keys.update(item.keys())
        
        if not all_keys:
            return None
        
        columns = sorted(list(all_keys))
        
        # Créer table (en-tête + lignes)
        table = doc.add_table(rows=1 + len(data_list_or_dict), cols=len(columns))
        table.style = 'Table Grid'
        
        # En-têtes
        header_cells = table.rows[0].cells
        for col_idx, col_name in enumerate(columns):
            cell = header_cells[col_idx]
            cell.text = col_name
            set_cell_background(cell, BORDEAUX_RGB)
            for paragraph in cell.paragraphs:
                for run in paragraph.runs:
                    run.font.bold = True
                    run.font.color.rgb = WHITE_RGB
                    run.font.name = 'Arial'
                    run.font.size = Pt(8.5)
                paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
        
        # Contenu
        for row_idx, item in enumerate(data_list_or_dict, start=1):
            row_cells = table.rows[row_idx].cells
            for col_idx, col_name in enumerate(columns):
                cell = row_cells[col_idx]
                value = item.get(col_name, "")
                
                cell.text = ""
                paragraph = cell.paragraphs[0]
                
                value_text = format_value_as_text(value)
                add_bulleted_lines(paragraph, value_text)
                
                for run in paragraph.runs:
                    run.font.name = 'Arial'
                    run.font.size = Pt(8.5)
                    run.font.color.rgb = BLACK_RGB
        
        return table
    
    return None


# ──────────────────────────────────────────────────────────────────────────────
# GÉNÉRATION DU DOCUMENT
# ──────────────────────────────────────────────────────────────────────────────

def generate_word_document(
    json_data,
    output_path,
    software_name=DEFAULT_SOFTWARE,
    footer_text=DEFAULT_FOOTER
):
    """
    Génère le document Word complet à partir du JSON.
    
    Args:
        json_data: Données JSON
        output_path: Chemin du fichier de sortie
        software_name: Nom du logiciel
        footer_text: Texte du pied de page
    """
    doc = Document()
    
    # Configuration page PAYSAGE A4
    section = doc.sections[0]
    section.page_width = Inches(11.69)  # A4 paysage
    section.page_height = Inches(8.27)
    section.left_margin = Inches(0.38)
    section.right_margin = Inches(0.38)
    section.top_margin = Inches(0.5)
    section.bottom_margin = Inches(0.46)

    # Extraire Data_integrale (gérer les niveaux imbriqués)
    data_to_process = json_data
    
    if "Data_integrale" in json_data:
        data_to_process = json_data["Data_integrale"]
        
        # Vérifier si c'est une liste avec un niveau supplémentaire
        if isinstance(data_to_process, list) and len(data_to_process) > 0:
            if isinstance(data_to_process[0], dict) and "Data_integrale" in data_to_process[0]:
                data_to_process = data_to_process[0]["Data_integrale"]
    
    # Convertir en liste si c'est un dict unique
    if isinstance(data_to_process, dict):
        data_to_process = [data_to_process]
    
    # Trouver l'étape de mission et la référence depuis le premier FRAP
    etape_mission = "Frap"
    reference = generate_reference()
    
    for frap_item in data_to_process:
        if isinstance(frap_item, dict):
            for main_key, main_value in frap_item.items():
                if "Etape mission" in main_key and isinstance(main_value, list) and len(main_value) > 0:
                    # Extraire table 1
                    for item in main_value:
                        if isinstance(item, dict) and "table 1" in item:
                            table1 = item["table 1"]
                            if "Etape de mission" in table1:
                                etape_mission = table1["Etape de mission"]
                            if "Reference" in table1:
                                reference = table1["Reference"]
                            break
                    break
            break
    
    # En-tête
    header = section.header
    header_para = header.paragraphs[0]
    header_para.text = f"{software_name} - {etape_mission}"
    header_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = header_para.runs[0]
    run.font.bold = True
    run.font.size = Pt(12)
    run.font.color.rgb = WHITE_RGB
    run.font.name = 'Arial'
    
    # Fond bordeaux pour l'en-tête
    shading_elm = OxmlElement('w:shd')
    shading_elm.set(qn('w:fill'), '8B0000')
    header_para._element.get_or_add_pPr().append(shading_elm)

    # Pied de page
    footer = section.footer
    footer_para = footer.paragraphs[0]
    footer_para.text = footer_text
    footer_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    footer_run = footer_para.runs[0]
    footer_run.font.color.rgb = BORDEAUX_RGB
    footer_run.font.name = 'Arial'
    footer_run.font.size = Pt(9)

    # Traiter uniquement le premier FRAP du JSON
    first_frap = None
    for frap_item in data_to_process:
        if isinstance(frap_item, dict):
            for main_key, main_value in frap_item.items():
                if "Etape mission" in main_key:
                    first_frap = main_value
                    break
            if first_frap:
                break
    
    if not first_frap:
        print("❌ Erreur : Aucune clé 'Etape mission - ...' trouvée dans le JSON")
        return
    
    # Traitement des tables
    for item in first_frap:
        if not isinstance(item, dict):
            continue
        
        for sub_key, sub_value in item.items():
            # Table 1 : format vertical avec colonne 1 bordeaux
            if sub_key.lower() == "table 1" and isinstance(sub_value, dict):
                create_vertical_table(doc, sub_value, software_name, etape_mission)
                doc.add_paragraph()  # Espacement
            
            # Tables 2+ : format horizontal
            elif sub_key.lower().startswith("table ") and sub_key.lower() != "table 1":
                create_horizontal_table(doc, sub_value, sub_key)
                doc.add_paragraph()  # Espacement
    
    # Sauvegarder
    doc.save(str(output_path))
    print(f"✅ Document Word généré avec succès")
    print(f"📄 Fichier : {output_path.name}")
    print(f"📍 Emplacement : {output_path.parent.resolve()}")


# ──────────────────────────────────────────────────────────────────────────────
# MAIN
# ──────────────────────────────────────────────────────────────────────────────

def main():
    """Point d'entrée CLI"""
    parser = argparse.ArgumentParser(
        description="Convertit un JSON de FRAP/Recommandations en document Word (.docx)"
    )
    parser.add_argument("json_file", help="Chemin vers le fichier JSON d'entrée")
    parser.add_argument("--software", default=DEFAULT_SOFTWARE, help="Nom du logiciel")
    parser.add_argument("--footer", default=DEFAULT_FOOTER, help="Texte du pied de page")
    parser.add_argument("-o", "--out-dir", default=".", help="Dossier de sortie")

    args = parser.parse_args()

    # Lecture du JSON
    json_path = Path(args.json_file)
    if not json_path.exists():
        print(f"❌ Erreur : Le fichier {json_path} n'existe pas.")
        sys.exit(1)

    with open(json_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Extraire le JSON
    try:
        json_data = json.loads(content)
    except json.JSONDecodeError:
        json_data = extract_json_from_text(content)
        if json_data is None:
            print("❌ Erreur : Aucun objet JSON valide trouvé dans le fichier.")
            sys.exit(1)

    # Extraire métadonnées pour le nom de fichier
    etape_mission = "Frap"
    reference = generate_reference()
    
    # Parcourir pour trouver table 1
    data_to_scan = json_data
    if "Data_integrale" in json_data:
        data_to_scan = json_data["Data_integrale"]
        if isinstance(data_to_scan, list) and len(data_to_scan) > 0:
            if isinstance(data_to_scan[0], dict) and "Data_integrale" in data_to_scan[0]:
                data_to_scan = data_to_scan[0]["Data_integrale"]
    
    if isinstance(data_to_scan, dict):
        data_to_scan = [data_to_scan]
    
    for frap_item in data_to_scan:
        if isinstance(frap_item, dict):
            for main_key, main_value in frap_item.items():
                if "Etape mission" in main_key and isinstance(main_value, list):
                    for item in main_value:
                        if isinstance(item, dict) and "table 1" in item:
                            table1 = item["table 1"]
                            if "Etape de mission" in table1:
                                etape_mission = table1["Etape de mission"]
                            if "Reference" in table1:
                                reference = table1["Reference"]
                            break
                    break
            break

    # Horodatage
    now = datetime.now()
    timestamp = now.strftime("%Y%m%d_%H%M%S")

    # Nom du fichier selon le format requis
    output_filename = f"{reference}-{etape_mission}- {args.software}_{timestamp}.docx"
    output_path = Path(args.out_dir) / output_filename

    # Créer le dossier de sortie
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Générer le document
    generate_word_document(
        json_data,
        output_path,
        args.software,
        args.footer
    )


if __name__ == "__main__":
    main()
