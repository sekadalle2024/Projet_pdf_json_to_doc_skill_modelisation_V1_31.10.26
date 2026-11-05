#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
json2word_audit.py
==================
Transforme un JSON de modélisation (manuel d'audit interne, FRAP, cartographie
des risques, etc.) en document Word (.docx) au style "E-procedure".

INSTALLATION ET UTILISATION
---------------------------
    pip install python-docx
    python json2word_audit.py donnees.json --ref A210 -o ./sortie

Autres exemples :
    python json2word_audit.py donnees.json
    python json2word_audit.py donnees.json --software "Logiciel automatisé E-audit pro 2.0" --ref BB040
    python json2word_audit.py donnees.json --no-blank-rows

OPTIONS DISPONIBLES
-------------------
    --software          nom du logiciel, utilisé dans l'en-tête et le nom du fichier
    --footer            texte du pied de page
    --no-blank-rows     pas de ligne vide après chaque ligne renseignée
    --keep-step-prefix  conserve le terme « Étape NN - » dans la colonne Etape
    --ref               référence alphanumérique (ex. A210) ; générée si absente
    -o / --out-dir      dossier de sortie

CE QUE FAIT LE SCRIPT
---------------------
  * Lecture du JSON : accepte aussi un fichier texte qui contient du JSON, et
    repère les clés « table N » quel que soit leur nombre.
  * Table 1 : un dictionnaire devient une table VERTICALE « Rubrique /
    Description ». Les dictionnaires et listes imbriqués sont écrits en puces « - ».
  * Table 2 : une liste d'objets devient une table en colonnes, avec bordures de
    LIGNES invisibles, bordures de COLONNES visibles et une ligne vide après
    chaque ligne renseignée. Les lignes vides déjà présentes sont retirées avant
    d'être réinsérées proprement.
  * Mise en forme : en-têtes de tableau en rouge bordeaux (7B1E3A), page A4
    paysage, en-tête « [Logiciel] - [Étape de mission] », pied de page avec le
    numéro WhatsApp, uniquement des tables (aucun titre entre les tables).
  * Puces : « - » pour les dictionnaires/listes imbriqués, les textes
    multi-lignes (\\n) de la colonne Traitement et la colonne Document
    (valeurs séparées par des virgules).
  * Nom du fichier : <référence>-<Etape_de_mission>- <Logiciel>.docx
    Sans --ref, une référence est générée (2 lettres + 3 chiffres, ex. FX251).

VALIDATION
----------
  Testé sur le JSON du manuel d'audit (texte identique au manuel précédent,
  fichier valide pour Word) et sur un petit JSON de structure différente
  (type FRAP).

LIMITES
-------
  * Les colonnes du manuel d'audit (Étape, Acteur, Traitement, Document,
    Normes, Extrait) sont déjà configurées avec leurs largeurs et leur rendu.
    Pour une autre structure (FRAP, cartographie des risques), ajoutez une
    ligne dans le dictionnaire COLUMN_SPECS en haut du script. Sinon les
    colonnes sont créées avec des largeurs égales et le texte simple.
  * La règle propre aux feuilles de couverture (schéma de calcul entre les
    tables 5 et 4) n'est pas intégrée.
  * La conversion des actions au présent n'est pas automatique : elle doit
    déjà figurer dans le JSON.

FORMAT JSON ATTENDU (clés « table N » et noms de colonnes libres)
-----------------------------------------------------------------
    {
      "Etape mission - ...": [
        {"table 1": {"Etape de mission": "...", "Document": "...", "Norme": {"Norme 1": "..."}}},
        {"table 2": [ {"col A": "...", "col B": "..."}, ... ]}
      ]
    }
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

# Spécification des colonnes connues de la table 2 :
#   clé JSON -> (libellé d'en-tête, largeur DXA, type de rendu)
# type : "bold" (gras), "nl" (puces, 1 par ligne \n), "csv" (puces, séparées par
# des virgules), "text" (texte simple)
# Note : les colonnes non listées sont auto-détectées (largeur selon contenu)
COLUMN_SPECS = {
    "Étape méthodologique":            ("Etape",           1900, "bold"),
    "Acteur audit":                    ("Acteur",          1500, "text"),
    "Traitement et diligences d'audit": ("Traitement",     5100, "nl"),
    "Document probant":                ("Document",        2300, "csv"),
    "Norme IIA / CRIPP":               ("Normes",          1700, "text"),
    "Extrait de la norme":             ("Extrait de norme",2500, "text"),
}
# Renseignez ici d'autres colonnes (FRAP, cartographie...) si besoin, ex. :
# COLUMN_SPECS["Risque"] = ("Risque", 3000, "text")


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
    """Supprime les lignes vides existantes puis en insère une après chaque ligne renseignée."""
    filled = [r for r in records if not is_empty_record(r)]
    if not enabled or not filled:
        return filled
    blank = {k: "" for k in filled[0]}
    out = []
    for r in filled:
        out.extend([r, dict(blank)])
    return out


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
            style_cell(cell, w, top=GREY, bottom=GREY)
            value = rec.get(key, "")
            if kind == "bold" and strip_steps:
                value = strip_step_prefix(value)
            fill_cell(cell, render_lines(value, kind), bold=(kind == "bold"))
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
# Nom de fichier : <référence>-<Etape_de_mission>- <Nom logiciel>.docx
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
    step_part = re.sub(r"\s+", "_", safe(step))
    
    # Extraire le timestamp de la référence si présent (format: PROD001_V1_14-54-04_31.10.26)
    timestamp_match = re.search(r"_(V\d+_[\d-]+_[\d.]+)$", reference)
    if timestamp_match:
        # Le timestamp devient le nom complet (sans préfixe de référence)
        timestamp = timestamp_match.group(1)
        # Format: [Etape] - [Logiciel]_[timestamp].docx (tiret simple pour compatibilité)
        return f"{step_part} - {safe(software)}_{timestamp}.docx"
    else:
        # Pas de timestamp, format normal avec référence
        return f"{reference} - {step_part} - {safe(software)}.docx"


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

    for n, (_, content) in enumerate(tables):
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
    ap.add_argument("--ref", default=None, help="référence alphanumérique (ex. A210) ; auto si absente")
    ap.add_argument("--footer", default=DEFAULT_FOOTER, help="texte du pied de page")
    ap.add_argument("--no-blank-rows", action="store_true",
                    help="ne pas insérer de ligne vide après chaque ligne renseignée")
    ap.add_argument("--keep-step-prefix", action="store_true",
                    help='conserver le terme "Étape NN -" dans la colonne Etape')
    args = ap.parse_args(argv)

    try:
        out = convert(args.json, args.out_dir, software=args.software, reference=args.ref,
                      footer=args.footer, blank_rows=not args.no_blank_rows,
                      strip_steps=not args.keep_step_prefix)
    except Exception as exc:                # message clair plutôt qu'une trace
        print(f"Erreur : {exc}", file=sys.stderr)
        return 1
    
    # Afficher le résultat (gérer l'encodage Windows)
    try:
        print(f"Fichier généré : {out}")
    except UnicodeEncodeError:
        # Si l'encodage échoue, afficher sans le nom complet
        print(f"Fichier généré : [nom contient des caractères spéciaux]")
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
