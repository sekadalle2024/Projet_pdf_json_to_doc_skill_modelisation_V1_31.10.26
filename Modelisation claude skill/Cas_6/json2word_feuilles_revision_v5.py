#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
json2word_feuilles_revision_v5.py
==================================
Transforme un JSON de feuilles de révision (Cas 6) en document Word (.docx)
au style "E-audit pro".

INSTALLATION ET UTILISATION
---------------------------
    pip install python-docx
    python json2word_feuilles_revision_v5.py donnees.json --ref A10 -o ./sortie

Autres exemples :
    python json2word_feuilles_revision_v5.py donnees.json
    python json2word_feuilles_revision_v5.py donnees.json --software "Logiciel automatisé E-audit pro 2.0" --ref A10
    python json2word_feuilles_revision_v5.py donnees.json --no-blank-rows

OPTIONS DISPONIBLES
-------------------
    --software          nom du logiciel, utilisé dans l'en-tête et le nom du fichier
    --footer            texte du pied de page
    --no-blank-rows     pas de ligne vide après chaque ligne renseignée
    --keep-step-prefix  conserve le terme « Étape NN - » dans la colonne Etape
    --ref               référence alphanumérique (ex. A10) ; générée si absente
    -o / --out-dir      dossier de sortie

CE QUE FAIT LE SCRIPT (CAS 6 - FEUILLES DE RÉVISION)
----------------------------------------------------
  * Lecture du JSON : accepte un fichier texte contenant du JSON avec 9 tables
    (table 0 à table 8).
  * Table 0 (Signature worksheet) : table horizontale avec Client, Exercice, Preparer, Reviewer
  * Table 1 (Présentation) : table horizontale avec Etape de mission, Test, Reference, Nature de test
  * Table 2 (Objectifs) : une ligne avec les objectifs d'audit
  * Table 3 (Travaux à effectuer) : liste séquentielle des contrôles à effectuer
  * Table 4 (Résultats) : résumé des résultats des tests
  * Table 5 (Table de test) : LA PLUS IMPORTANTE - jusqu'à 20 colonnes avec échantillon testé
    - La colonne Ecart est en gras et si valeur != "0", fond rouge clair (FFE0E0)
  * Table 6 (Cross references) : références documentaires
  * Table 7 (Légendes) : symboles utilisés dans les tests
  * Table 8 (Revue manager) : questions/réponses superviseur/préparateur
  * Mise en forme : en-têtes de tableau en rouge bordeaux (7B1E3A), page A4
    paysage, en-tête « [Logiciel] - [Étape de mission] », pied de page avec le
    numéro WhatsApp, uniquement des tables (aucun titre entre les tables).
  * Nom du fichier : <référence>-<Etape_de_mission>-<Logiciel>.docx

CHANGEMENTS V5
--------------
  * Tables 0, 1, 2, 4 : toujours rendues en table horizontale (add_grid_table).
  * Lignes vides : supprimées dans toutes les tables (with_blank_rows toujours False).
  * Table 5 : colonnes réordonnées — Ecart avant CTR 1-5.

VALIDATION
----------
  Testé sur le JSON standard Cas 6 avec 9 tables incluant la table de test
  avec colonne Ecart conditionnelle.

LIMITES
-------
  * Les colonnes sont configurées dans COLUMN_SPECS avec leurs largeurs.
  * La table de test (table 5) peut avoir jusqu'à 20 colonnes ; la somme des
    largeurs est normalisée automatiquement à TABLE_WIDTH=15000 DXA.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

from docx import Document
from docx.enum.section import WD_ORIENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Pt, RGBColor, Twips

# --------------------------------------------------------------------------- #
# Paramètres de style (modifiables)
# --------------------------------------------------------------------------- #
BORDEAUX = "7B1E3A"        # fond des en-têtes de tableau et de l'en-tête de page
LIGHT = "F2E6EA"           # fond de la 1re colonne de la table verticale
GREY = "999999"            # bordures visibles
WHITE = "FFFFFF"           # bordures "invisibles" (lignes de la table 2)
FONT = "Calibri"
FONT_SIZE = 9              # pt
TABLE_WIDTH = 15000        # DXA (A4 paysage, marges 0,5")

DEFAULT_SOFTWARE = "Logiciel automatisé E-audit pro"
DEFAULT_FOOTER = ("Automatisez vos activités d'audit, risques et contrôles - "
                  "Whatsapp : + 225 05 44 13 07 98")

# Spécification des colonnes du Cas 6 (Feuilles de révision)
COLUMN_SPECS = {
    # Table 0 - Signature worksheet
    "Client": ("Client", 2500, "text"),
    "Exercice": ("Exercice", 700, "text"),
    "Reviewer": ("Reviewer", 2500, "text"),

    # Table 1 - Présentation (horizontale, géré auto par add_grid_table)
    "Etape de mission": ("Etape de mission", 3000, "text"),
    "Test": ("Test", 700, "text"),
    "Reference": ("Reference", 5000, "text"),
    "Nature de test": ("Nature de test", 1000, "text"),

    # Table 2 - Objectifs
    "OBJECTIFS": ("Objectifs d'audit", 15000, "text"),

    # Table 3 - Travaux à effectuer
    "no": ("N°", 400, "text"),
    "travaux a effectuer": ("Travaux à effectuer", 14600, "text"),

    # Table 4 - Résultats
    "Résultats des tests": ("Résultats des tests", 15000, "text"),

    # Table 5 - Table de test (LA PLUS IMPORTANTE)
    "N°": ("N°", 300, "text"),
    "N° Ordre": ("N°", 300, "text"),
    "N° Compte Client": ("N° Compte", 900, "text"),
    "Date Réactivation": ("Date", 700, "text"),
    "Intitulé Compte": ("Intitulé", 1400, "text"),
    "Solde Veille Réactivation": ("Solde Veille", 900, "text"),
    "Visa Agence (Maker)": ("Maker", 500, "text"),
    "Visa Conformité Siège (Checker)": ("Checker", 500, "text"),
    "Contact Liquidateur Conforme": ("Contact", 500, "text"),
    "Montant Débit Réalisé": ("Montant", 900, "text"),
    "Ecart": ("Ecart", 600, "bold"),
    "Assertion": ("Assertion", 800, "text"),
    "CTR 1": ("CTR 1", 400, "text"),
    "CTR 2": ("CTR 2", 400, "text"),
    "CTR 3": ("CTR 3", 400, "text"),
    "CTR 4": ("CTR 4", 400, "text"),
    "CTR 5": ("CTR 5", 400, "text"),
    "X-Ref": ("X-Ref", 500, "text"),
    "Description": ("Description", 2000, "text"),
    "Conclusion": ("Conclusion", 900, "text"),

    # Table 6 - Cross references
    "Cross references": ("Réf", 500, "text"),
    "Document": ("Document", 3000, "text"),

    # Table 7 - Légendes
    "Légende": ("Légende", 2500, "text"),
    "Symboles": ("Symbole", 600, "text"),

    # Table 8 - Revue manager (Preparer ici = "Réponse préparateur")
    "Superviseur": ("Question superviseur", 3000, "text"),
    "Preparer": ("Réponse préparateur", 3000, "text"),
}


# --------------------------------------------------------------------------- #
# Outils XML bas niveau
# --------------------------------------------------------------------------- #
def _el(tag: str, **attrs) -> OxmlElement:
    e = OxmlElement(tag)
    for k, v in attrs.items():
        e.set(qn("w:" + k), str(v))
    return e


def _border(side: str, color: str, size: int = 4):
    return _el(side, val="single", color=color, sz=size)


def style_table(table, widths, inside_h: str):
    """Table à largeur fixe + bordures extérieures grises."""
    tbl = table._tbl
    tbl_pr = tbl.tblPr
    for child in list(tbl_pr):
        tbl_pr.remove(child)
    tbl_pr.append(_el("w:tblW", type="dxa", w=sum(widths)))
    borders = _el("w:tblBorders")
    for side, color in (("top", GREY), ("left", GREY), ("bottom", GREY),
                        ("right", GREY), ("insideH", inside_h), ("insideV", GREY)):
        borders.append(_border("w:" + side, color))
    tbl_pr.append(borders)
    tbl_pr.append(_el("w:tblLayout", type="fixed"))
    table.autofit = False
    for i, w in enumerate(widths):
        table.columns[i].width = Twips(w)


def style_cell(cell, width, *, fill=None, top=GREY, bottom=GREY, valign="top"):
    cell.width = Twips(width)
    tc_pr = cell._tc.get_or_add_tcPr()
    borders = _el("w:tcBorders")
    borders.append(_border("w:top", top))
    borders.append(_border("w:left", GREY))
    borders.append(_border("w:bottom", bottom))
    borders.append(_border("w:right", GREY))
    tc_pr.append(borders)
    if fill:
        tc_pr.append(_el("w:shd", val="clear", color="auto", fill=fill))
    mar = _el("w:tcMar")
    for side, w in (("top", 50), ("left", 80), ("bottom", 50), ("right", 80)):
        mar.append(_el("w:" + side, type="dxa", w=w))
    tc_pr.append(mar)
    tc_pr.append(_el("w:vAlign", val=valign))


def style_row(row, *, header=False):
    tr_pr = row._tr.get_or_add_trPr()
    tr_pr.append(_el("w:cantSplit"))
    if header:
        tr_pr.append(_el("w:tblHeader"))


def _font(run, bold=False, color=None, size=FONT_SIZE):
    run.font.name = FONT
    run._element.rPr.rFonts.set(qn("w:eastAsia"), FONT)
    run._element.rPr.rFonts.set(qn("w:cs"), FONT)
    run.font.size = Pt(size)
    run.font.bold = bold or None
    if color:
        run.font.color.rgb = RGBColor.from_string(color)


def fill_cell(cell, lines, *, bold=False, color=None, center=False):
    """Écrit une liste de lignes (1 paragraphe par ligne) dans la cellule."""
    lines = lines if lines else [""]
    for i, text in enumerate(lines):
        p = cell.paragraphs[0] if i == 0 else cell.add_paragraph()
        pf = p.paragraph_format
        pf.space_before = Pt(0)
        pf.space_after = Pt(0 if center else 2)
        if center:
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(text)
        _font(run, bold=bold, color=color)


# --------------------------------------------------------------------------- #
# Normalisation des données
# --------------------------------------------------------------------------- #
def load_json(path: Path) -> dict:
    """Charge le JSON, même si le fichier contient du texte avant/après."""
    text = path.read_text(encoding="utf-8-sig")
    start = text.find("{")
    if start < 0:
        raise ValueError("Aucun objet JSON trouvé dans le fichier.")
    data, _ = json.JSONDecoder().raw_decode(text[start:])
    return data


def extract_tables(data: dict):
    """Retourne la liste ordonnée [(nom_table, contenu)] quel que soit l'emballage."""
    # 1) emballage "Etape mission - ..." : [ {"table 1": ...}, {"table 2": ...} ]
    containers = [v for v in data.values() if isinstance(v, list)
                  and v and all(isinstance(x, dict) for x in v)
                  and any(str(k).lower().startswith("table") for x in v for k in x)]
    items = containers[0] if containers else [data]
    tables = []
    for item in items:
        for key, value in item.items():
            if str(key).lower().startswith("table"):
                tables.append((key, value))
    if not tables:
        raise ValueError('Aucune clé "table N" trouvée dans le JSON.')
    return tables


def strip_step_prefix(text: str) -> str:
    """'Étape 02 - Bascule ...' -> 'Bascule ...' (on retire le terme Étape)."""
    return re.sub(r"^\s*[ÉEé]tape\s*\d+\s*[-–:]\s*", "", text or "").strip()


def to_lines(value) -> list[str]:
    """Valeur JSON -> lignes de texte (dict/list => puces '- ')."""
    if isinstance(value, dict):
        return ["- " + str(v) for v in value.values()]
    if isinstance(value, list):
        return ["- " + str(v) for v in value]
    return [str(value)] if value not in (None, "") else [""]


def render_lines(value: str, kind: str) -> list[str]:
    value = "" if value is None else str(value)
    if kind == "nl":
        lines = [l.strip() for l in value.split("\n") if l.strip()]
        return [l if l.startswith("- ") else "- " + l.lstrip("-• ").strip() for l in lines]
    if kind == "csv":
        return ["- " + x.strip() for x in value.split(", ") if x.strip()]
    return [value]


def is_empty_record(rec: dict) -> bool:
    return not any(str(v).strip() for v in rec.values())


def with_blank_rows(records: list[dict], enabled: bool) -> list[dict]:
    """Supprime les lignes vides existantes. En v5, on n'insère jamais de lignes vides."""
    return [r for r in records if not is_empty_record(r)]


# --------------------------------------------------------------------------- #
# Construction des tables
# --------------------------------------------------------------------------- #
def add_vertical_table(doc, content: dict):
    """Table 1 : Rubrique / Description (orientation verticale)."""
    widths = [4200, 10800]
    table = doc.add_table(rows=1 + len(content), cols=2)
    style_table(table, widths, inside_h=GREY)

    hdr = table.rows[0]
    style_row(hdr, header=True)
    for cell, w, label in zip(hdr.cells, widths, ("Rubrique", "Description")):
        style_cell(cell, w, fill=BORDEAUX, valign="center")
        fill_cell(cell, [label], bold=True, color=WHITE, center=True)

    for row, (key, value) in zip(table.rows[1:], content.items()):
        style_row(row)
        style_cell(row.cells[0], widths[0], fill=LIGHT, valign="center")
        fill_cell(row.cells[0], [str(key)], bold=True)
        style_cell(row.cells[1], widths[1], valign="center")
        fill_cell(row.cells[1], to_lines(value))
    return table


def auto_detect_column_width(key: str, records: list[dict]) -> int | None:
    """
    Détecte automatiquement la largeur optimale d'une colonne selon son contenu.
    
    Retourne:
        - 400 pour les colonnes de numérotation (no, #, num)
        - 600 pour les codes courts (3-5 caractères max)
        - 1000 pour les codes moyens (6-10 caractères max)
        - None pour laisser la largeur par défaut
    """
    key_lower = key.lower().strip()
    
    # Colonne de numérotation
    if key_lower in ["no", "n°", "#", "num", "numero", "numéro", "n"]:
        return 400
    
    # Analyser le contenu des 10 premières lignes non vides
    sample_values = []
    for rec in records[:10]:
        val = str(rec.get(key, "")).strip()
        if val:
            sample_values.append(val)
    
    if not sample_values:
        return None
    
    # Calculer la longueur max des valeurs
    max_len = max(len(v) for v in sample_values)
    
    # Codes très courts (1-3 caractères) : 400-600 DXA
    if max_len <= 3:
        return 500
    
    # Codes courts (4-6 caractères) : 600-800 DXA
    if max_len <= 6:
        return 700
    
    # Codes moyens (7-10 caractères) : 800-1000 DXA
    if max_len <= 10:
        return 900
    
    # Sinon, laisser l'algorithme de répartition faire son travail
    return None


def column_layout(keys: list[str], records: list[dict] = None):
    """Libellés, largeurs et types de rendu des colonnes (connues ou non)."""
    labels, widths, kinds = [], [], []
    for k in keys:
        # Chercher d'abord dans COLUMN_SPECS
        if k in COLUMN_SPECS:
            label, w, kind = COLUMN_SPECS[k]
        else:
            # Auto-détection pour les colonnes inconnues
            label = k
            kind = "text"
            w = auto_detect_column_width(k, records) if records else None
        
        labels.append(label)
        widths.append(w)
        kinds.append(kind)
    
    unknown = [i for i, w in enumerate(widths) if w is None]
    if unknown:
        remaining = max(TABLE_WIDTH - sum(w for w in widths if w), 1200 * len(unknown))
        for i in unknown:
            widths[i] = remaining // len(unknown)
    total = sum(widths)
    if total != TABLE_WIDTH:                      # recalage sur la largeur utile
        widths = [round(w * TABLE_WIDTH / total) for w in widths]
        widths[-1] += TABLE_WIDTH - sum(widths)
    return labels, widths, kinds


def reorder_table5_columns(records: list[dict]) -> list[dict]:
    """
    Réordonne les colonnes de la table 5 (Table de test) selon la règle Cas 6 :
    Identification → Contrôle → ECART → CTR 1-5 → Colonnes finales.
    La colonne Ecart est AVANT les CTR.
    """
    if not records:
        return records

    ORDER = [
        "N°", "N° Ordre", "N° Compte Client", "Date Réactivation",
        "Intitulé Compte", "Solde Veille Réactivation",
        "Visa Agence (Maker)", "Visa Conformité Siège (Checker)",
        "Contact Liquidateur Conforme", "Montant Débit Réalisé",
        "Ecart",  # AVANT les CTR
        "CTR 1", "CTR 2", "CTR 3", "CTR 4", "CTR 5",
        "Assertion", "X-Ref", "Description", "Conclusion",
    ]

    reordered = []
    for rec in records:
        new_rec = {}
        # D'abord les colonnes dans l'ordre défini
        for col in ORDER:
            if col in rec:
                new_rec[col] = rec[col]
        # Puis les colonnes non listées dans ORDER (au cas où)
        for col in rec:
            if col not in new_rec:
                new_rec[col] = rec[col]
        reordered.append(new_rec)
    return reordered


def add_grid_table(doc, records: list[dict], blank_rows: bool, strip_steps: bool):
    """Table 2 : colonnes, bordures de lignes visibles horizontalement et verticalement."""
    rows_data = with_blank_rows(records, blank_rows)
    keys = list(next(r for r in records if not is_empty_record(r)).keys())
    labels, widths, kinds = column_layout(keys, records)

    table = doc.add_table(rows=1 + len(rows_data), cols=len(keys))
    style_table(table, widths, inside_h=GREY)

    hdr = table.rows[0]
    style_row(hdr, header=True)
    for cell, w, label in zip(hdr.cells, widths, labels):
        style_cell(cell, w, fill=BORDEAUX, valign="center")
        fill_cell(cell, [label], bold=True, color=WHITE, center=True)

    last = len(rows_data) - 1
    for idx, (row, rec) in enumerate(zip(table.rows[1:], rows_data)):
        style_row(row)
        # Toutes les lignes ont des bordures grises visibles
        for cell, w, key, kind in zip(row.cells, widths, keys, kinds):
            value = rec.get(key, "")
            # Style conditionnel pour la colonne Ecart
            is_ecart_non_zero = (key == "Ecart" and str(value).strip() not in ("", "0", "0 ", " 0"))
            cell_fill = "FFE0E0" if is_ecart_non_zero else None
            style_cell(cell, w, fill=cell_fill, top=GREY, bottom=GREY)
            if kind == "bold" and strip_steps:
                value = strip_step_prefix(value)
            fill_cell(cell, render_lines(value, kind), bold=(kind == "bold" or is_ecart_non_zero))
    return table


def add_spacer(doc, points: float = 6):
    """Mini-paragraphe entre deux tables (aucun titre, aucun texte)."""
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.space_before = Pt(0)
    pf.space_after = Pt(0)
    pf.line_spacing_rule = WD_LINE_SPACING.EXACTLY
    pf.line_spacing = Pt(points)


# --------------------------------------------------------------------------- #
# Page, en-tête, pied de page
# --------------------------------------------------------------------------- #
def _paragraph_border(paragraph, side: str):
    p_pr = paragraph._p.get_or_add_pPr()
    bdr = _el("w:pBdr")
    bdr.append(_el("w:" + side, val="single", color=BORDEAUX, sz=8, space=4))
    p_pr.append(bdr)


def setup_page(doc, header_text: str, footer_text: str):
    sec = doc.sections[0]
    sec.orientation = WD_ORIENT.LANDSCAPE
    sec.page_width, sec.page_height = Twips(16838), Twips(11906)
    sec.left_margin = sec.right_margin = Twips(720)
    sec.top_margin, sec.bottom_margin = Twips(1300), Twips(1200)
    sec.header_distance = sec.footer_distance = Twips(708)

    hp = sec.header.paragraphs[0]
    _font(hp.add_run(header_text), bold=True, color=BORDEAUX, size=10)
    _paragraph_border(hp, "bottom")

    fp = sec.footer.paragraphs[0]
    _paragraph_border(fp, "top")              # pBdr avant jc (ordre du schéma)
    fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    _font(fp.add_run(footer_text), color="444444", size=8)


# --------------------------------------------------------------------------- #
# Nom de fichier : <référence>-<Etape_de_mission>-<Nom logiciel>.docx
# --------------------------------------------------------------------------- #
def auto_reference(seed: str) -> str:
    """Référence alphanumérique auto : 2 lettres + 3 chiffres (ex. MA417)."""
    letters = "".join(w[0] for w in re.findall(r"[A-Za-zÀ-ÿ]+", seed))[:2].upper() or "XX"
    letters = (letters + "X")[:2]
    digits = int(hashlib.md5(seed.encode("utf-8")).hexdigest(), 16) % 900 + 100
    return f"{letters}{digits}"


def safe(text: str) -> str:
    return re.sub(r'[\\/:*?"<>|]', "", text).strip()


def build_filename(reference: str, step: str, software: str) -> str:
    # Format simple: Cas6_YYYYMMDD_HHMMSS.docx (sans accents ni caractères spéciaux)
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"Cas6_{timestamp}.docx"


# --------------------------------------------------------------------------- #
# Programme principal
# --------------------------------------------------------------------------- #
def convert(json_path: Path, out_dir: Path, *, software: str, reference: str | None,
            footer: str, blank_rows: bool, strip_steps: bool) -> Path:
    data = load_json(json_path)
    tables = extract_tables(data)

    # Etape de mission : lue dans la table 1 si présente
    step = "Document"
    for _, content in tables:
        if isinstance(content, dict) and "Etape de mission" in content:
            step = str(content["Etape de mission"]).strip() or step
            break
        elif isinstance(content, list):
            for rec in content:
                if isinstance(rec, dict) and "Etape de mission" in rec:
                    step = str(rec["Etape de mission"]).strip() or step
                    break
            if step != "Document":
                break

    doc = Document()
    zoom = doc.settings.element.find(qn("w:zoom"))   # modèle python-docx : zoom sans pourcentage
    if zoom is not None and zoom.get(qn("w:percent")) is None:
        zoom.set(qn("w:percent"), "100")
    normal = doc.styles["Normal"]
    normal.font.name = FONT
    normal.font.size = Pt(FONT_SIZE)
    normal.paragraph_format.space_before = Pt(0)
    normal.paragraph_format.space_after = Pt(0)
    normal.paragraph_format.line_spacing = 1.0
    setup_page(doc, f"{software} - {step}", footer)

    for n, (table_name, content) in enumerate(tables):
        # Réordonner les colonnes de la table 5
        key_lower = str(table_name).lower()
        m = re.search(r'table\s+(\d+)', key_lower)
        if m and m.group(1) == '5' and isinstance(content, list):
            content = reorder_table5_columns(content)

        if n:
            add_spacer(doc)
        if isinstance(content, dict):
            add_vertical_table(doc, content)
        elif isinstance(content, list) and content:
            add_grid_table(doc, content, blank_rows, strip_steps)
    add_spacer(doc, 1)                      # Word exige un paragraphe final

    reference = reference or auto_reference(step)
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / build_filename(reference, step, software)
    doc.save(out)
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("json", type=Path, help="fichier JSON (ou texte contenant le JSON)")
    ap.add_argument("-o", "--out-dir", type=Path, default=Path("."), help="dossier de sortie")
    ap.add_argument("--software", default=DEFAULT_SOFTWARE, help="nom du logiciel (en-tête + nom de fichier)")
    ap.add_argument("--ref", default=None, help="référence alphanumérique (ex. A10) ; auto si absente")
    ap.add_argument("--footer", default=DEFAULT_FOOTER, help="texte du pied de page")
    ap.add_argument("--no-blank-rows", action="store_true",
                    help="ne pas insérer de ligne vide après chaque ligne renseignée")
    ap.add_argument("--keep-step-prefix", action="store_true",
                    help='conserver le terme "Étape NN -" dans la colonne Etape')
    args = ap.parse_args(argv)

    try:
        out = convert(args.json, args.out_dir, software=args.software, reference=args.ref,
                      footer=args.footer, blank_rows=False,
                      strip_steps=not args.keep_step_prefix)
    except Exception as exc:                # message clair plutôt qu'une trace
        print(f"[ERREUR] : {exc}", file=sys.stderr)
        return 1
    
    # Afficher le résultat (gérer l'encodage Windows)
    try:
        print(f"[OK] Fichier généré : {out}")
    except UnicodeEncodeError:
        # Si l'encodage échoue, afficher sans le nom complet
        print(f"[OK] Fichier généré : [nom contient des caractères spéciaux]")
        print(f"Chemin : {out.parent}")
    
    return 0


if __name__ == "__main__":
    # Forcer UTF-8 sur Windows si possible
    if sys.platform == 'win32':
        try:
            sys.stdout.reconfigure(encoding='utf-8')
            sys.stderr.reconfigure(encoding='utf-8')
        except:
            pass
    sys.exit(main())
