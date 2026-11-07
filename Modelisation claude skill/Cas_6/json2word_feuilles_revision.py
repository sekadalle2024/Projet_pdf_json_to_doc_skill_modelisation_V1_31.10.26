#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
json2word_feuilles_revision.py
==============================
Transforme un JSON de feuilles de révision d'audit (tests, pointages, conclusions)
en document Word (.docx) au style "E-procedure".

INSTALLATION ET UTILISATION
---------------------------
    pip install python-docx
    python json2word_feuilles_revision.py donnees.json --ref T001 -o ./sortie

Autres exemples :
    python json2word_feuilles_revision.py donnees.json
    python json2word_feuilles_revision.py donnees.json --software "Logiciel automatisé E-audit pro 2.0" --ref FDR001
    python json2word_feuilles_revision.py donnees.json --no-blank-rows

OPTIONS DISPONIBLES
-------------------
    --software          nom du logiciel, utilisé dans l'en-tête et le nom du fichier
    --footer            texte du pied de page
    --no-blank-rows     pas de ligne vide après chaque ligne renseignée
    --keep-test-prefix  conserve le terme « Test NN - » dans la colonne N° Test
    --ref               référence alphanumérique (ex. T001) ; générée si absente
    -o / --out-dir      dossier de sortie

CE QUE FAIT LE SCRIPT
---------------------
  * Lecture du JSON : accepte aussi un fichier texte qui contient du JSON, et
    repère les clés « table N » quel que soit leur nombre.
  * Table 1 : un dictionnaire devient une table VERTICALE « Rubrique /
    Description ». Les dictionnaires et listes imbriqués sont écrits en puces « - ».
  * Table 2 : une liste d'objets devient une table en colonnes (9 colonnes pour
    feuilles de révision), avec bordures de LIGNES invisibles, bordures de
    COLONNES visibles et une ligne vide après chaque ligne renseignée.
  * Mise en forme : en-têtes de tableau en rouge bordeaux (7B1E3A), page A4
    paysage, en-tête « [Logiciel] - [Étape de mission] », pied de page avec le
    numéro WhatsApp, uniquement des tables (aucun titre entre les tables).
  * Puces : « - » pour les dictionnaires/listes imbriqués, les textes
    multi-lignes (\\n) de la colonne Procédure de test.
  * Nom du fichier : <Etape_de_mission>―<Logiciel>_V1_HH-MM-SS_DD.MM.YY.docx

VALIDATION
----------
  Testé sur le JSON des feuilles de révision d'audit (9 colonnes de tests).
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
# CONFIGURATION DES COLONNES (9 COLONNES POUR FEUILLES DE RÉVISION)
# ──────────────────────────────────────────────────────────────────────────────
COLUMN_SPECS = {
    "N° Test":              ("N° Test",        800,  "bold"),
    "Objectif de contrôle": ("Objectif",       1800, "text"),
    "Nature du contrôle":   ("Nature",         1400, "text"),
    "Procédure de test":    ("Procédure",      2400, "nl"),
    "Taille échantillon":   ("Échantillon",    1200, "text"),
    "Résultat observé":     ("Résultat",       1600, "text"),
    "Écart identifié":      ("Écart",          1800, "text"),
    "Conclusion":           ("Conclusion",     1400, "text"),
    "Action recommandée":   ("Action",         1600, "text"),
}

BORDEAUX_RGB = RGBColor(0x7B, 0x1E, 0x3A)
PINK_RGB = RGBColor(0xF2, 0xE6, 0xEA)
GRAY_RGB = RGBColor(0x99, 0x99, 0x99)
WHITE_RGB = RGBColor(0xFF, 0xFF, 0xFF)

DEFAULT_SOFTWARE = "Logiciel automatisé E-audit pro 2.0"
DEFAULT_FOOTER = "Automatisez vos activités d'audit, risques et contrôles - Whatsapp : + 225 05 44 13 07 98"

# ──────────────────────────────────────────────────────────────────────────────
# FONCTIONS UTILITAIRES
# ──────────────────────────────────────────────────────────────────────────────

def extract_json_from_text(text: str):
    """Extrait le premier objet JSON trouvé dans une chaîne de caractères."""
    pattern = r'\{(?:[^{}]|(?:\{(?:[^{}]|(?:\{[^{}]*\}))*\}))*\}'
    match = re.search(pattern, text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(0))
        except json.JSONDecodeError:
            pass
    return None


def generate_reference():
    """Génère une référence aléatoire (format: 2 lettres + 3 chiffres, ex: FX251)."""
    letters = ''.join(random.choices(string.ascii_uppercase, k=2))
    numbers = ''.join(random.choices(string.digits, k=3))
    return letters + numbers


def set_cell_background(cell, color_rgb):
    """Définit la couleur de fond d'une cellule."""
    shading_elm = OxmlElement('w:shd')
    # RGBColor est un tuple (r, g, b) ou un objet RGBColor
    if isinstance(color_rgb, tuple):
        r, g, b = color_rgb
    else:
        # C'est un objet RGBColor de python-docx
        r, g, b = color_rgb
    shading_elm.set(qn('w:fill'), f"{r:02X}{g:02X}{b:02X}")
    cell._element.get_or_add_tcPr().append(shading_elm)


def set_cell_border(cell, **kwargs):
    """
    Définit les bordures d'une cellule.
    kwargs peut contenir: top, bottom, left, right
    Chaque valeur est un tuple (size, color) ou None
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
            color = border_val[1]
            # Gérer RGBColor comme tuple
            if isinstance(color, tuple):
                r, g, b = color
            else:
                r, g, b = color
            border_elm.set(qn('w:color'), f"{r:02X}{g:02X}{b:02X}")
            tcBorders.append(border_elm)

    tcPr.append(tcBorders)


def format_value_as_text(value):
    """
    Convertit une valeur (dict, list, str, etc.) en texte avec puces si nécessaire.
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
    """Ajoute des lignes avec puces dans un paragraphe."""
    lines = text.split('\n')
    for i, line in enumerate(lines):
        if i > 0:
            paragraph.add_run('\n')
        paragraph.add_run(line.strip())


# ──────────────────────────────────────────────────────────────────────────────
# CRÉATION DES TABLES
# ──────────────────────────────────────────────────────────────────────────────

def create_vertical_table(doc, data_dict, software_name, etape_mission):
    """
    Crée une table verticale (2 colonnes: Rubrique | Description).
    """
    table = doc.add_table(rows=len(data_dict) + 1, cols=2)
    table.style = 'Table Grid'

    # En-tête
    header_cells = table.rows[0].cells
    header_cells[0].text = "Rubrique"
    header_cells[1].text = "Description"

    for cell in header_cells:
        set_cell_background(cell, BORDEAUX_RGB)
        for paragraph in cell.paragraphs:
            for run in paragraph.runs:
                run.font.bold = True
                run.font.color.rgb = RGBColor(255, 255, 255)
            paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER

    # Données
    for idx, (key, value) in enumerate(data_dict.items(), start=1):
        row_cells = table.rows[idx].cells
        
        # Colonne Rubrique
        row_cells[0].text = key
        set_cell_background(row_cells[0], PINK_RGB)
        for paragraph in row_cells[0].paragraphs:
            for run in paragraph.runs:
                run.font.bold = True

        # Colonne Description
        formatted_value = format_value_as_text(value)
        row_cells[1].text = ""
        paragraph = row_cells[1].paragraphs[0]
        add_bulleted_lines(paragraph, formatted_value)

    return table


def create_horizontal_table(doc, data_list, blank_rows=True, keep_prefix=False):
    """
    Crée une table horizontale pour les tests de révision (9 colonnes).
    """
    if not data_list:
        return None

    # Déterminer les colonnes présentes
    all_keys = set()
    for item in data_list:
        all_keys.update(item.keys())

    # Filtrer les colonnes reconnues
    recognized_cols = [k for k in COLUMN_SPECS.keys() if k in all_keys]
    if not recognized_cols:
        return None

    # Nombre de lignes : en-tête + (lignes * 2 si blank_rows, sinon lignes)
    num_data_rows = len(data_list)
    num_rows = 1 + (num_data_rows * 2 if blank_rows else num_data_rows)

    table = doc.add_table(rows=num_rows, cols=len(recognized_cols))
    table.style = 'Table Grid'

    # En-tête
    header_cells = table.rows[0].cells
    for col_idx, key in enumerate(recognized_cols):
        short_name, width_twips, _ = COLUMN_SPECS[key]
        cell = header_cells[col_idx]
        cell.text = short_name
        cell.width = Inches(width_twips / 1440)
        
        set_cell_background(cell, BORDEAUX_RGB)
        for paragraph in cell.paragraphs:
            for run in paragraph.runs:
                run.font.bold = True
                run.font.color.rgb = RGBColor(255, 255, 255)
            paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER

    # Données
    row_idx = 1
    for item in data_list:
        row_cells = table.rows[row_idx].cells
        
        for col_idx, key in enumerate(recognized_cols):
            value = item.get(key, "")
            _, _, render_type = COLUMN_SPECS[key]
            cell = row_cells[col_idx]
            
            # Bordures : colonnes visibles, lignes invisibles
            set_cell_border(
                cell,
                left=(6, GRAY_RGB),
                right=(6, GRAY_RGB),
                top=(6, WHITE_RGB),
                bottom=(6, WHITE_RGB)
            )
            
            cell.text = ""
            paragraph = cell.paragraphs[0]
            
            if render_type == "bold":
                # Retirer préfixe "Test NN -" si nécessaire
                if not keep_prefix and isinstance(value, str):
                    value = re.sub(r'^Test\s+\d+\s*-\s*', '', value, flags=re.IGNORECASE)
                
                run = paragraph.add_run(str(value))
                run.font.bold = True
            
            elif render_type == "nl":
                # Multiligne avec puces
                if isinstance(value, str) and '\n' in value:
                    add_bulleted_lines(paragraph, value)
                else:
                    paragraph.add_run(str(value))
            
            elif render_type == "csv":
                # Valeurs CSV en puces
                if isinstance(value, str) and ',' in value:
                    items = [item.strip() for item in value.split(',')]
                    text_with_bullets = "\n".join([f"- {item}" for item in items if item])
                    add_bulleted_lines(paragraph, text_with_bullets)
                else:
                    paragraph.add_run(str(value))
            
            else:  # "text"
                paragraph.add_run(str(value))
        
        row_idx += 1
        
        # Ligne vide
        if blank_rows:
            blank_cells = table.rows[row_idx].cells
            for cell in blank_cells:
                set_cell_border(
                    cell,
                    left=(6, GRAY_RGB),
                    right=(6, GRAY_RGB),
                    top=(6, WHITE_RGB),
                    bottom=(6, WHITE_RGB)
                )
            row_idx += 1

    return table


# ──────────────────────────────────────────────────────────────────────────────
# GÉNÉRATION DU DOCUMENT
# ──────────────────────────────────────────────────────────────────────────────

def generate_word_document(
    json_data,
    output_path,
    software_name=DEFAULT_SOFTWARE,
    footer_text=DEFAULT_FOOTER,
    blank_rows=True,
    keep_prefix=False
):
    """
    Génère le document Word complet à partir du JSON.
    """
    doc = Document()
    
    # Configuration page paysage
    section = doc.sections[0]
    section.page_width = Inches(11)
    section.page_height = Inches(8.5)
    section.left_margin = Inches(0.5)
    section.right_margin = Inches(0.5)
    section.top_margin = Inches(0.5)
    section.bottom_margin = Inches(0.5)

    # Trouver l'étape de mission
    etape_mission = "Feuille de révision"
    for main_key, main_value in json_data.items():
        if isinstance(main_value, list) and len(main_value) > 0:
            for item in main_value:
                if isinstance(item, dict):
                    table1 = item.get("table 1")
                    if table1 and isinstance(table1, (dict, list)):
                        table1_dict = table1[0] if isinstance(table1, list) else table1
                        if isinstance(table1_dict, dict) and "Etape de mission" in table1_dict:
                            etape_mission = table1_dict["Etape de mission"]
                            break

    # En-tête
    header = section.header
    header_para = header.paragraphs[0]
    header_para.text = f"{software_name} - {etape_mission}"
    header_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = header_para.runs[0]
    run.font.bold = True
    run.font.size = Pt(12)
    run.font.color.rgb = RGBColor(255, 255, 255)
    
    # Fond bordeaux pour l'en-tête
    shading_elm = OxmlElement('w:shd')
    shading_elm.set(qn('w:fill'), '7B1E3A')
    header_para._element.get_or_add_pPr().append(shading_elm)

    # Pied de page
    footer = section.footer
    footer_para = footer.paragraphs[0]
    footer_para.text = footer_text
    footer_para.alignment = WD_ALIGN_PARAGRAPH.CENTER

    # Traitement de TOUS les tableaux (pas seulement table 1 et 2)
    for main_key, main_value in json_data.items():
        if not isinstance(main_value, list):
            continue

        for item in main_value:
            if not isinstance(item, dict):
                continue

            # Traiter TOUS les tableaux trouvés
            for sub_key, sub_value in item.items():
                # Vérifier si c'est une clé de type "table X" ou "table X - description"
                if re.match(r'table\s+\d+', sub_key, re.IGNORECASE):
                    # Déterminer le type de tableau (vertical ou horizontal)
                    if isinstance(sub_value, dict):
                        # Tableau vertical (une seule ligne de métadonnées)
                        create_vertical_table(doc, sub_value, software_name, etape_mission)
                    elif isinstance(sub_value, list):
                        # Tableau horizontal (plusieurs lignes de données)
                        create_horizontal_table(doc, sub_value, blank_rows, keep_prefix)
                    
                    doc.add_paragraph()  # Espacement après chaque tableau

    # Sauvegarder
    doc.save(output_path)
    print(f"✅ Document généré : {output_path}")


# ──────────────────────────────────────────────────────────────────────────────
# MAIN
# ──────────────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Convertit un JSON de feuilles de révision d'audit en document Word (.docx)"
    )
    parser.add_argument("json_file", help="Chemin vers le fichier JSON d'entrée")
    parser.add_argument("--software", default=DEFAULT_SOFTWARE, help="Nom du logiciel")
    parser.add_argument("--footer", default=DEFAULT_FOOTER, help="Texte du pied de page")
    parser.add_argument("--no-blank-rows", action="store_true", help="Ne pas ajouter de lignes vides")
    parser.add_argument("--keep-test-prefix", action="store_true", help="Conserver le préfixe 'Test NN -'")
    parser.add_argument("--ref", default=None, help="Référence (ex: T001)")
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

    # Vérifier la présence de tables
    has_tables = False
    for main_value in json_data.values():
        if isinstance(main_value, list):
            for item in main_value:
                if isinstance(item, dict):
                    for key in item.keys():
                        if re.match(r'table\s+\d+', key, re.IGNORECASE):
                            has_tables = True
                            break

    if not has_tables:
        print("❌ Erreur : Aucune clé 'table N' trouvée dans le JSON.")
        sys.exit(1)

    # Extraire l'étape de mission pour le nom de fichier
    etape_mission = "Feuille_revision"
    for main_value in json_data.values():
        if isinstance(main_value, list) and len(main_value) > 0:
            table1 = main_value[0].get("table 1", {})
            if "Etape de mission" in table1:
                etape_mission = table1["Etape de mission"]
                etape_mission = etape_mission.replace(" ", "_").replace("-", "_")
                break

    # Référence
    reference = args.ref if args.ref else generate_reference()

    # Horodatage
    now = datetime.now()
    timestamp = now.strftime("V1_%H-%M-%S_%d.%m.%y")

    # Nom du logiciel simplifié
    software_short = args.software.replace("Logiciel automatisé ", "").replace(" 2.0", "")

    # Nom du fichier
    output_filename = f"{etape_mission} ― {software_short}_{timestamp}.docx"
    output_path = Path(args.out_dir) / output_filename

    # Créer le dossier de sortie
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Générer le document
    generate_word_document(
        json_data,
        output_path,
        args.software,
        args.footer,
        not args.no_blank_rows,
        args.keep_test_prefix
    )


if __name__ == "__main__":
    main()
