# -*- coding: utf-8 -*-
"""
json2word_cas10_automation.py - Cas 10
Convertit les donnees de "Programme de travail" avec Modelisation design
en document Word avec la charte graphique E-audit pro (bordeaux #7B1E3A)
"""

import json
import sys
import tempfile
from pathlib import Path
from datetime import datetime

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Pt, RGBColor, Twips

# Import du convertisseur generique avec charte E-audit pro
# Utilise directement le script de reference du Cas 2
CAS2_DIR = Path(__file__).parent.parent.parent / "Cas_2"
sys.path.insert(0, str(CAS2_DIR))

try:
    from json2word_audit import convert
except ImportError as e:
    print(f"[ERREUR] Import impossible: {e}", file=sys.stderr)
    print(f"   Chemin recherche: {CAS2_DIR}", file=sys.stderr)
    sys.exit(1)

# Dossier de sortie par defaut
OUTPUT_DIR = Path.home() / 'Downloads'

# Couleurs de la charte E-audit pro
BORDEAUX = "7B1E3A"
LIGHT_BORDEAUX = "C4A4B0"
LIGHT_GRAY = "F2F2F2"
WHITE = "FFFFFF"
GREY = "999999"


def parse_modelisation_design(data):
    """
    Extrait la section [Modelisation design] du JSON.
    
    Args:
        data: Donnees JSON (dict ou liste)
        
    Returns:
        dict: Dictionnaire des designs, ou {} si absent
    """
    # La structure est: {"Etape mission - ...": [{table 1}, {table 2}, {[Modelisation design]}]}
    if isinstance(data, dict):
        # Chercher la cle "Etape mission - ..."
        for key, value in data.items():
            if isinstance(value, list):
                # Parcourir la liste pour trouver l'item contenant [Modelisation design]
                for item in value:
                    if isinstance(item, dict) and "[Modélisation design]" in item:
                        return item["[Modélisation design]"]
    
    return {}


def _el(tag, **attrs):
    """Cree un element XML avec attributs."""
    e = OxmlElement(tag)
    for k, v in attrs.items():
        e.set(qn("w:" + k), str(v))
    return e


def _border(side, color, size=4):
    """Cree une bordure XML."""
    return _el(side, val="single", color=color, sz=size)


def style_cell_shading(cell, fill_color):
    """Applique une couleur de fond a une cellule."""
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = _el("w:shd", val="clear", color="auto", fill=fill_color)
    tc_pr.append(shd)


def style_design_table(table, widths):
    """Applique le style a une table de design."""
    tbl = table._tbl
    tbl_pr = tbl.tblPr
    
    # Nettoyer les proprietes existantes
    for child in list(tbl_pr):
        tbl_pr.remove(child)
    
    # Largeur de la table
    tbl_pr.append(_el("w:tblW", type="dxa", w=sum(widths)))
    
    # Bordures
    borders = _el("w:tblBorders")
    for side in ["top", "left", "bottom", "right", "insideH", "insideV"]:
        borders.append(_border("w:" + side, GREY))
    tbl_pr.append(borders)
    
    # Layout fixe
    tbl_pr.append(_el("w:tblLayout", type="fixed"))
    table.autofit = False
    
    # Largeurs des colonnes
    for i, w in enumerate(widths):
        table.columns[i].width = Twips(w)


def format_cell_text(cell, text, bold=False, italic=False, color=None):
    """Formate le texte dans une cellule."""
    cell.text = ""
    p = cell.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    run = p.add_run(str(text))
    run.font.name = "Calibri"
    run.font.size = Pt(9)
    run.font.bold = bold
    run.font.italic = italic
    if color:
        run.font.color.rgb = RGBColor.from_string(color)


def build_design_section_tables(doc, modelisation_design):
    """
    Ajoute les tables de Modelisation design au document.
    
    Args:
        doc: Document python-docx
        modelisation_design: Dictionnaire des designs
    """
    if not modelisation_design:
        return
    
    # Ajouter un titre pour la section
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run("Modelisation Design - Synthese des structures hierarchiques")
    run.font.name = "Calibri"
    run.font.size = Pt(14)
    run.font.bold = True
    run.font.color.rgb = RGBColor.from_string(BORDEAUX)
    
    # Parcourir chaque table cible
    for table_cible, designs in modelisation_design.items():
        if not isinstance(designs, dict):
            continue
        
        # Titre de la table cible
        p = doc.add_paragraph()
        run = p.add_run(str(table_cible))
        run.font.name = "Calibri"
        run.font.size = Pt(12)
        run.font.bold = True
        run.font.color.rgb = RGBColor.from_string(BORDEAUX)
        
        # Parcourir chaque design
        for design_name, design_spec in designs.items():
            if not isinstance(design_spec, dict):
                continue
            
            # Titre du design
            p = doc.add_paragraph()
            run = p.add_run(str(design_name))
            run.font.name = "Calibri"
            run.font.size = Pt(11)
            run.font.bold = True
            
            # Creer le tableau du design (2 colonnes: Niveau | Colonnes / Sous-groupes)
            widths = [3000, 12000]
            table = doc.add_table(rows=1, cols=2)
            style_design_table(table, widths)
            
            # En-tete du tableau
            hdr_row = table.rows[0]
            style_cell_shading(hdr_row.cells[0], BORDEAUX)
            style_cell_shading(hdr_row.cells[1], BORDEAUX)
            format_cell_text(hdr_row.cells[0], "Niveau", bold=True, color=WHITE)
            format_cell_text(hdr_row.cells[1], "Colonnes / Sous-groupes", bold=True, color=WHITE)
            
            # Extraire les niveaux
            niveau1 = design_spec.get("[Niveau 1]", "")
            niveau2 = design_spec.get("[Niveau 2]", "")
            niveau3 = design_spec.get("[Niveau 3]", "")
            niveau4 = design_spec.get("[Niveau 4]", "")
            colonnes = design_spec.get("Colonnes couvertes", [])
            
            # Gerer Design 5 avec branchement au Niveau 2
            is_branching = isinstance(niveau2, list)
            
            if is_branching:
                # Design 5: structure branchee
                # Niveau 1
                row = table.add_row()
                style_cell_shading(row.cells[0], BORDEAUX)
                style_cell_shading(row.cells[1], BORDEAUX)
                format_cell_text(row.cells[0], "Niveau 1", bold=True, color=WHITE)
                format_cell_text(row.cells[1], niveau1, bold=True, color=WHITE)
                
                # Niveau 2: branches
                row = table.add_row()
                style_cell_shading(row.cells[0], LIGHT_BORDEAUX)
                style_cell_shading(row.cells[1], LIGHT_BORDEAUX)
                format_cell_text(row.cells[0], "Niveau 2 (branches)", bold=True, color="000000")
                branches_text = " | ".join(niveau2)
                format_cell_text(row.cells[1], branches_text, bold=True, color="000000")
                
                # Niveau 3: details des branches
                if isinstance(niveau3, dict):
                    for branch_name, branch_cols in niveau3.items():
                        row = table.add_row()
                        style_cell_shading(row.cells[0], LIGHT_GRAY)
                        style_cell_shading(row.cells[1], LIGHT_GRAY)
                        format_cell_text(row.cells[0], f"  {branch_name}", bold=False, color="000000")
                        if isinstance(branch_cols, list):
                            cols_text = ", ".join(branch_cols)
                        else:
                            cols_text = str(branch_cols)
                        format_cell_text(row.cells[1], cols_text, bold=False, color="000000")
            else:
                # Designs normaux (1-4): structure lineaire
                # Niveau 1
                if niveau1:
                    row = table.add_row()
                    style_cell_shading(row.cells[0], BORDEAUX)
                    style_cell_shading(row.cells[1], BORDEAUX)
                    format_cell_text(row.cells[0], "Niveau 1", bold=True, color=WHITE)
                    format_cell_text(row.cells[1], niveau1, bold=True, color=WHITE)
                
                # Niveau 2
                if niveau2:
                    row = table.add_row()
                    style_cell_shading(row.cells[0], LIGHT_BORDEAUX)
                    style_cell_shading(row.cells[1], LIGHT_BORDEAUX)
                    format_cell_text(row.cells[0], "Niveau 2", bold=True, color="000000")
                    format_cell_text(row.cells[1], niveau2, bold=True, color="000000")
                
                # Niveau 3
                if niveau3:
                    row = table.add_row()
                    style_cell_shading(row.cells[0], LIGHT_GRAY)
                    style_cell_shading(row.cells[1], LIGHT_GRAY)
                    format_cell_text(row.cells[0], "Niveau 3", bold=False, color="000000")
                    format_cell_text(row.cells[1], niveau3, bold=False, color="000000")
                
                # Niveau 4
                if niveau4:
                    row = table.add_row()
                    style_cell_shading(row.cells[0], WHITE)
                    style_cell_shading(row.cells[1], WHITE)
                    format_cell_text(row.cells[0], "Niveau 4", italic=True, color="000000")
                    format_cell_text(row.cells[1], niveau4, italic=True, color="000000")
            
            # Colonnes couvertes
            if colonnes:
                row = table.add_row()
                style_cell_shading(row.cells[0], LIGHT_GRAY)
                style_cell_shading(row.cells[1], LIGHT_GRAY)
                format_cell_text(row.cells[0], "Colonnes couvertes", bold=True, color="000000")
                if isinstance(colonnes, list):
                    colonnes_text = ", ".join(colonnes)
                else:
                    colonnes_text = str(colonnes)
                format_cell_text(row.cells[1], colonnes_text, bold=False, color="000000")
            
            # Espace apres le tableau
            doc.add_paragraph()


def main(json_file, output_dir=None):
    """
    Convertit un fichier JSON Programme de travail avec Modelisation design
    en document Word.
    
    Args:
        json_file: Chemin vers le fichier JSON
        output_dir: Dossier de sortie (optionnel, par defaut Downloads)
    
    Returns:
        bool: True si succes, False sinon
    """
    json_path = Path(json_file)
    
    if not json_path.exists():
        print(f"[ERREUR] Fichier introuvable : {json_path}", file=sys.stderr)
        return False
    
    # Charger le JSON
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            raw_data = json.load(f)
    except Exception as e:
        print(f"[ERREUR] Lecture JSON : {e}", file=sys.stderr)
        return False
    
    # Extraire les donnees reelles depuis la structure du webhook
    data = raw_data
    if isinstance(raw_data, dict) and "data" in raw_data:
        data = raw_data["data"]
    
    # Extraire la section Modelisation design AVANT de passer a convert()
    modelisation_design = parse_modelisation_design(data)
    
    # Retirer l'item [Modelisation design] des donnees pour convert()
    # (pour eviter qu'il soit traite comme une table)
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, list):
                # Filtrer l'item contenant [Modelisation design]
                data[key] = [item for item in value 
                            if not (isinstance(item, dict) and "[Modélisation design]" in item)]
    
    # Determiner le dossier de sortie
    if output_dir:
        out_path = Path(output_dir)
    else:
        out_path = OUTPUT_DIR
    
    out_path.mkdir(parents=True, exist_ok=True)
    
    # Creer un fichier temporaire avec juste les donnees mission (format Cas 2)
    temp_json = None
    try:
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8') as tmp:
            json.dump(data, tmp, ensure_ascii=False, indent=2)
            temp_json = Path(tmp.name)
        
        # Generer un nom de fichier avec timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        reference = f"Cas10_{timestamp}"
        
        # Appeler le convertisseur avec la charte E-audit pro
        # blank_rows=False pour Cas 10 (comme Cas 8)
        # strip_steps=False pour garder les prefixes "Etape"
        temp_output = convert(
            json_path=temp_json,
            out_dir=out_path,
            software="Logiciel automatise E-audit pro",
            reference=reference,
            footer="Automatisez vos activites d'audit, risques et controles - Whatsapp : + 225 05 44 13 07 98",
            blank_rows=False,
            strip_steps=False
        )
        
        # Rouvrir le document pour ajouter la section Modelisation design
        if modelisation_design:
            doc = Document(str(temp_output))
            
            # Ajouter un saut de section (nouveau paragraphe)
            doc.add_paragraph()
            
            # Ajouter les tables de Modelisation design
            build_design_section_tables(doc, modelisation_design)
            
            # Sauvegarder le document mis a jour
            doc.save(str(temp_output))
        
        # Affichage du resultat sans emoji pour compatibilite Windows
        print(f"Document cree : {temp_output.name}")
        print(f"Dossier : {temp_output.parent}")
        return True
        
    except Exception as e:
        print(f"[ERREUR] Conversion : {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return False
    
    finally:
        # Nettoyer le fichier temporaire
        if temp_json and temp_json.exists():
            try:
                temp_json.unlink()
            except:
                pass


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python json2word_cas10_automation.py <fichier.json> [dossier_sortie]")
        sys.exit(1)
    
    json_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else None
    
    success = main(json_path, output_dir)
    sys.exit(0 if success else 1)
