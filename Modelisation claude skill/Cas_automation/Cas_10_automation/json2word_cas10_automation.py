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


def _set_paragraph_shading(paragraph, fill_color):
    """Applique un fond coloré à un paragraphe via XML."""
    pPr = paragraph._p.get_or_add_pPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), fill_color)
    pPr.append(shd)


def build_hierarchical_design(doc, design_name, design_spec):
    """
    Rend un design avec une structure hiérarchique visuelle (paragraphes indentés).
    
    Args:
        doc: Document python-docx
        design_name: Nom du design (ex: "Design 1 - Cycle par sous-processus")
        design_spec: Dictionnaire de spécification du design
    """
    # Titre du design (bordeaux, gras, taille 11pt, 0 indent)
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Twips(0)
    run = p.add_run(str(design_name))
    run.font.name = "Calibri"
    run.font.size = Pt(11)
    run.font.bold = True
    run.font.color.rgb = RGBColor.from_string(BORDEAUX)
    
    # Extraire les niveaux
    niveau1 = design_spec.get("[Niveau 1]", "")
    niveau2 = design_spec.get("[Niveau 2]", "")
    niveau3 = design_spec.get("[Niveau 3]", "")
    niveau4 = design_spec.get("[Niveau 4]", "")
    colonnes = design_spec.get("Colonnes couvertes", [])
    
    # Déterminer si c'est une structure branchée (niveau2 = liste)
    is_branching = isinstance(niveau2, list)
    
    if is_branching:
        # Structure branchée (Design 5)
        
        # Niveau 1: fond bordeaux, texte blanc, gras, indent 200
        if niveau1:
            p = doc.add_paragraph()
            p.paragraph_format.left_indent = Twips(200)
            _set_paragraph_shading(p, BORDEAUX)
            run = p.add_run(f"|- Niveau 1: {niveau1}")
            run.font.name = "Calibri"
            run.font.size = Pt(11)
            run.font.bold = True
            run.font.color.rgb = RGBColor(255, 255, 255)  # Blanc
        
        # Niveau 2 (branches): fond light bordeaux, texte noir, gras, indent 200
        if niveau2:
            p = doc.add_paragraph()
            p.paragraph_format.left_indent = Twips(200)
            _set_paragraph_shading(p, LIGHT_BORDEAUX)
            run = p.add_run("|- Niveau 2 (branches):")
            run.font.name = "Calibri"
            run.font.size = Pt(10)
            run.font.bold = True
            run.font.color.rgb = RGBColor(0, 0, 0)
            
            # Lister chaque branche avec indent 400
            for branch in niveau2:
                p = doc.add_paragraph()
                p.paragraph_format.left_indent = Twips(400)
                _set_paragraph_shading(p, LIGHT_BORDEAUX)
                run = p.add_run(f"|    |- {branch}")
                run.font.name = "Calibri"
                run.font.size = Pt(10)
                run.font.bold = True
                run.font.color.rgb = RGBColor(0, 0, 0)
        
        # Niveau 3 (détails par branche): fond gris clair, indent 200 puis 600 pour les détails
        if isinstance(niveau3, dict):
            p = doc.add_paragraph()
            p.paragraph_format.left_indent = Twips(200)
            _set_paragraph_shading(p, LIGHT_GRAY)
            run = p.add_run("'- Niveau 3 (details par branche):")
            run.font.name = "Calibri"
            run.font.size = Pt(10)
            run.font.bold = False
            run.font.color.rgb = RGBColor(0, 0, 0)
            
            # Détails de chaque branche
            for branch_name, branch_cols in niveau3.items():
                p = doc.add_paragraph()
                p.paragraph_format.left_indent = Twips(600)
                _set_paragraph_shading(p, LIGHT_GRAY)
                if isinstance(branch_cols, list):
                    cols_text = ", ".join(branch_cols)
                else:
                    cols_text = str(branch_cols)
                run = p.add_run(f"     |- {branch_name} -> {cols_text}")
                run.font.name = "Calibri"
                run.font.size = Pt(10)
                run.font.bold = False
                run.font.color.rgb = RGBColor(0, 0, 0)
    
    else:
        # Structure linéaire (Designs 1-4)
        
        # Niveau 1: fond bordeaux, texte blanc, gras, indent 200
        if niveau1:
            p = doc.add_paragraph()
            p.paragraph_format.left_indent = Twips(200)
            _set_paragraph_shading(p, BORDEAUX)
            run = p.add_run(f"|- Niveau 1: {niveau1}")
            run.font.name = "Calibri"
            run.font.size = Pt(11)
            run.font.bold = True
            run.font.color.rgb = RGBColor(255, 255, 255)  # Blanc
        
        # Niveau 2: fond light bordeaux, texte noir, gras, indent 400
        if niveau2:
            p = doc.add_paragraph()
            p.paragraph_format.left_indent = Twips(400)
            _set_paragraph_shading(p, LIGHT_BORDEAUX)
            run = p.add_run(f"|- Niveau 2: {niveau2}")
            run.font.name = "Calibri"
            run.font.size = Pt(10)
            run.font.bold = True
            run.font.color.rgb = RGBColor(0, 0, 0)
        
        # Niveau 3: fond gris clair, texte noir, normal, indent 600
        if niveau3:
            p = doc.add_paragraph()
            p.paragraph_format.left_indent = Twips(600)
            _set_paragraph_shading(p, LIGHT_GRAY)
            run = p.add_run(f"|- Niveau 3: {niveau3}")
            run.font.name = "Calibri"
            run.font.size = Pt(10)
            run.font.bold = False
            run.font.color.rgb = RGBColor(0, 0, 0)
        
        # Niveau 4: fond blanc, texte gris, italique, indent 800
        if niveau4:
            p = doc.add_paragraph()
            p.paragraph_format.left_indent = Twips(800)
            run = p.add_run(f"'- Niveau 4: {niveau4}")
            run.font.name = "Calibri"
            run.font.size = Pt(9)
            run.font.bold = False
            run.font.italic = True
            run.font.color.rgb = RGBColor.from_string(GREY)
    
    # Colonnes couvertes: fond gris clair, indent 200
    if colonnes:
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Twips(200)
        _set_paragraph_shading(p, LIGHT_GRAY)
        if isinstance(colonnes, list):
            colonnes_text = ", ".join(colonnes)
        else:
            colonnes_text = str(colonnes)
        run = p.add_run(f"Colonnes: {colonnes_text}")
        run.font.name = "Calibri"
        run.font.size = Pt(9)
        run.font.bold = False
        run.font.color.rgb = RGBColor(0, 0, 0)
    
    # Espace après le design
    doc.add_paragraph()


def build_design_section_tables(doc, modelisation_design):
    """
    Ajoute les sections de Modélisation design au document avec une structure hiérarchique visuelle.
    
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
        
        # Parcourir chaque design et appeler build_hierarchical_design
        for design_name, design_spec in designs.items():
            if not isinstance(design_spec, dict):
                continue
            
            build_hierarchical_design(doc, design_name, design_spec)
            
            # Séparateur visuel entre designs (ligne vide)
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
            
            # Récupérer l'élément XML de Table 2 (index 1)
            # Table 2 est la deuxième table du document
            if len(doc.tables) >= 2:
                table2_el = doc.tables[1]._tbl
                parent = table2_el.getparent()
                table2_index = list(parent).index(table2_el)
                
                # Créer les éléments de la section design dans un doc temporaire
                tmp_doc = Document()
                
                # Ajouter un paragraphe vide de séparation
                tmp_doc.add_paragraph()
                
                # Construire la section design dans le doc temporaire
                build_design_section_tables(tmp_doc, modelisation_design)
                
                # Insérer les éléments du doc temporaire AVANT table2_el
                # Les éléments à insérer sont les paragraphes du body du doc temporaire
                # (en excluant le dernier paragraphe vide obligatoire de tout doc Word)
                tmp_body = tmp_doc.element.body
                elements_to_insert = list(tmp_body)[:-1]  # Exclure le dernier para vide final
                
                # Insérer en ordre inverse pour maintenir l'ordre (insertion avant)
                insert_pos = table2_index
                for elem in elements_to_insert:
                    # Détacher l'élément de son parent temporaire
                    tmp_body.remove(elem)
                    parent.insert(insert_pos, elem)
                    insert_pos += 1
            else:
                # Fallback : ajouter à la fin si moins de 2 tables
                doc.add_paragraph()
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
