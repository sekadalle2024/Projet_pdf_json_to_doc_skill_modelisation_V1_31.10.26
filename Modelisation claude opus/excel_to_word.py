#!/usr/bin/env python3
"""
excel_to_word.py - Convertit le contenu d'un classeur Excel en tableaux Word (.docx)
avec la charte du modèle "Matrice de surveillance permanente" (bordeaux 7B1E3A, Calibri,
A4 paysage, en-tête / pied de page, ligne d'en-tête répétée, lignes non coupées).

Deux modes (détection automatique) :
  1. "cartographie" : classeur de cartographie des risques issu d'une conversion PDF
     (en-têtes "PROCESSUS / SOUS PROCESSUS", colonnes décalées, cellules fusionnées,
     lignes de suite sans libellé). Un tableau par processus.
  2. "generic" : tout autre classeur. Chaque onglet est lu, les lignes/colonnes vides sont
     supprimées et chaque bloc de données séparé par une ligne vide devient un tableau
     (dimensions variables d'un onglet à l'autre).

Usage :
    python excel_to_word.py entree.xlsx sortie.docx [--titre "..."] [--mode auto|cartographie|generic]
Dépendances : openpyxl, python-docx
"""
import argparse
import datetime as dt
import re
from collections import OrderedDict

from docx import Document
from docx.enum.section import WD_ORIENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Pt, RGBColor, Twips
from openpyxl import load_workbook
from openpyxl.utils import column_index_from_string as CI

# ----------------------------------------------------------------- charte graphique
BORDEAUX, ROSE, ROSE_MID, ROSE_PALE = "7B1E3A", "F2E6EA", "E3C4CE", "FAF3F5"
GRIS, FONT = "999999", "Calibri"
PAGE_W, PAGE_H = 16838, 11906            # A4 paysage (DXA)
MARGIN_LR, USABLE_W = 720, 16838 - 2 * 720


# ----------------------------------------------------------------- utilitaires texte
def clean(v):
    """Valeur de cellule -> texte propre (nbsp, .0, espaces)."""
    if v is None:
        return ""
    if isinstance(v, float) and v.is_integer():
        v = int(v)
    if isinstance(v, (dt.datetime, dt.date)):
        return v.strftime("%d/%m/%Y")
    s = str(v).replace("\xa0", " ").replace("\r", "")
    s = "\n".join(line.strip() for line in s.split("\n"))
    return re.sub(r"\n{3,}", "\n\n", s).strip()


def norm(s):
    return re.sub(r"\s+", " ", clean(s)).strip().upper()


# ----------------------------------------------------------------- briques XML Word
def _el(tag, **attrs):
    e = OxmlElement(tag)
    for k, v in attrs.items():
        e.set(qn(k.replace("_", ":", 1)), str(v))
    return e


def style_run(run, size=9, bold=False, italic=False, color=None):
    run.font.name = FONT
    rpr = run._r.get_or_add_rPr()
    rf = rpr.find(qn("w:rFonts"))
    for a in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
        rf.set(qn(a), FONT)
    run.font.size = Pt(size)
    run.font.bold, run.font.italic = bold, italic
    if color:
        run.font.color.rgb = RGBColor.from_string(color)


def set_cell(cell, text, width, fill=None, bold=False, italic=False, color=None,
             size=8, align="left", valign="top", span=None, vm=None):
    tcPr = cell._tc.get_or_add_tcPr()
    for child in list(tcPr):
        tcPr.remove(child)
    tcPr.append(_el("w:tcW", w_type="dxa", w_w=width))
    if span:
        tcPr.append(_el("w:gridSpan", w_val=span))
    if vm:
        tcPr.append(_el("w:vMerge", **({"w_val": "restart"} if vm == "restart" else {})))
    b = _el("w:tcBorders")
    for side in ("top", "left", "bottom", "right"):
        b.append(_el(f"w:{side}", w_val="single", w_color=GRIS, w_sz=4))
    tcPr.append(b)
    if fill:
        tcPr.append(_el("w:shd", w_fill=fill, w_color="auto", w_val="clear"))
    m = _el("w:tcMar")
    for side, w in (("top", 50), ("left", 80), ("bottom", 50), ("right", 80)):
        m.append(_el(f"w:{side}", w_type="dxa", w_w=w))
    tcPr.append(m)
    tcPr.append(_el("w:vAlign", w_val=valign))

    lines = (text or "").split("\n") or [""]
    for i, line in enumerate(lines):
        p = cell.paragraphs[0] if i == 0 else cell.add_paragraph()
        pf = p.paragraph_format
        pf.space_before = pf.space_after = Pt(0)
        p.alignment = {"left": 0, "center": 1, "right": 2}[align]
        style_run(p.add_run(line), size, bold, italic, color)


def new_table(doc, widths):
    t = doc.add_table(rows=0, cols=len(widths))
    t.autofit = False
    tblPr = t._tbl.tblPr
    for child in list(tblPr):
        if child.tag in (qn("w:tblStyle"), qn("w:tblW"), qn("w:tblLayout")):
            tblPr.remove(child)
    look = tblPr.find(qn("w:tblLook"))
    borders = _el("w:tblBorders")
    for side in ("top", "left", "bottom", "right", "insideH", "insideV"):
        borders.append(_el(f"w:{side}", w_val="single", w_color="auto", w_sz=4))
    for el in (_el("w:tblW", w_type="dxa", w_w=sum(widths)), borders, _el("w:tblLayout", w_type="fixed")):
        look.addprevious(el)          # respecte l'ordre imposé par le schéma
    grid = t._tbl.tblGrid
    for gc, w in zip(grid.findall(qn("w:gridCol")), widths):
        gc.set(qn("w:w"), str(w))
    return t


def add_row(table, header=False):
    row = table.add_row()
    trPr = row._tr.get_or_add_trPr()
    trPr.append(_el("w:cantSplit"))
    if header:
        trPr.append(_el("w:tblHeader"))
    return row


def merge_cells(cells, start, end):
    """Fusion horizontale (gridSpan) : retire du XML les cellules absorbées."""
    for c in cells[start + 1:end + 1]:
        c._tc.getparent().remove(c._tc)
    return cells[start]


def heading(doc, text, size=13, space_before=14):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.keep_with_next = True
    style_run(p.add_run(text), size, True, color=BORDEAUX)
    return p


def spacer(doc):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(6)


def setup_document(header_text, footer_text):
    doc = Document()
    st = doc.styles["Normal"]
    st.font.name, st.font.size = FONT, Pt(9)
    zoom = doc.settings.element.find(qn("w:zoom"))
    if zoom is not None and zoom.get(qn("w:percent")) is None:
        zoom.set(qn("w:percent"), "100")
    sec = doc.sections[0]
    sec.orientation = WD_ORIENT.LANDSCAPE
    sec.page_width, sec.page_height = Twips(PAGE_W), Twips(PAGE_H)
    sec.left_margin = sec.right_margin = Twips(MARGIN_LR)
    sec.top_margin, sec.bottom_margin = Twips(1300), Twips(1200)
    sec.header_distance = sec.footer_distance = Twips(708)

    def band(par, text, size, bold, color, border, align=0):
        pPr = par._p.get_or_add_pPr()
        bd = _el("w:pBdr")
        bd.append(_el(f"w:{border}", w_val="single", w_color=BORDEAUX, w_sz=8, w_space=4))
        pPr.append(bd)                # pBdr avant jc (ordre du schéma)
        par.alignment = align
        style_run(par.add_run(text), size, bold, color=color)

    band(sec.header.paragraphs[0], header_text, 10, True, BORDEAUX, "bottom")
    band(sec.footer.paragraphs[0], footer_text, 8, False, "444444", "top", align=1)
    # pagination "Page X / Y"
    fp = sec.footer.add_paragraph()
    fp.alignment = 1
    for kind, txt in (("Page ", None), ("PAGE", "instr"), (" / ", None), ("NUMPAGES", "instr")):
        r = fp.add_run("" if txt else kind)
        style_run(r, 8, color="444444")
        if txt:
            for t, extra in (("begin", None), (None, kind), ("end", None)):
                if t:
                    r._r.append(_el("w:fldChar", w_fldCharType=t))
                else:
                    it = OxmlElement("w:instrText")
                    it.set(qn("xml:space"), "preserve")
                    it.text = f" {extra} "
                    r._r.append(it)
    return doc


def info_table(doc, pairs):
    """Tableau 'Rubrique / Description' identique au modèle."""
    widths = [4200, 10800]
    t = new_table(doc, widths)
    r = add_row(t, header=True)
    for c, txt, w in zip(r.cells, ("Rubrique", "Description"), widths):
        set_cell(c, txt, w, BORDEAUX, True, color="FFFFFF", size=9, align="center", valign="center")
    for k, v in pairs:
        r = add_row(t)
        set_cell(r.cells[0], k, widths[0], ROSE, True, size=9, valign="center")
        set_cell(r.cells[1], v, widths[1], size=9, valign="center")
    spacer(doc)


# ================================================================ MODE 1 : cartographie
# rôle -> colonne Excel, pour une ligne "libellé" (col. A renseignée) et une ligne "suite"
COLS_A = dict(prob="F", imp="G", amp="H", fact="I", c1="K", c2="M",
              rprob="R", rimp="S", ramp="T", plan="U")
COLS_B = dict(prob="B", imp="C", amp="D", fact="E", c1="J", c2="L",
              rprob="N", rimp="O", ramp="P", plan="Q")
ROLES = ["prob", "imp", "amp", "fact", "c1", "c2", "rprob", "rimp", "ramp", "plan"]
FILL_LEVEL = {"D9D9D9": 0, "C5DFB4": 1, "B4C5E7": 2, "FFFF00": 3}
CARTO_W = [1750, 620, 620, 620, 2600, 2400, 2400, 620, 620, 620, 2130]   # = 15 000


def is_carto(ws):
    return any(norm(ws.cell(r, 1).value).startswith("PROCESSUS /") for r in range(1, min(ws.max_row, 400) + 1))


def parse_cartographie(ws):
    rows = {}
    for row in ws.iter_rows():
        vals = {c.column_letter: clean(c.value) for c in row if clean(c.value)}
        if vals:
            rows[row[0].row] = vals

    hdr = [r for r, v in rows.items() if norm(v.get("A", "")).startswith("PROCESSUS /")]
    # ligne titre d'un processus = dernière ligne "A seule" non CARTOGRAPHIE avant l'en-tête
    titles = []
    for h in hdr:
        t = max(r for r, v in rows.items()
                if r < h and set(v) == {"A"} and not norm(v["A"]).startswith("CARTOGRAPHIE"))
        titles.append(t)

    sections = OrderedDict()
    for i, (h, t) in enumerate(zip(hdr, titles)):
        end = (titles[i + 1] if i + 1 < len(titles) else ws.max_row + 1) - 1
        r0 = h + 1
        while r0 in rows and set(rows[r0]) <= {"K", "M"} or norm(rows.get(r0, {}).get("A", "")) == "SOUS PROCESSUS":
            r0 += 1
        title = rows[t]["A"]
        items, label, skipped = [], "", 0
        for r in range(r0, end + 1):
            v = rows.get(r)
            if not v or norm(v.get("A", "")).startswith("CARTOGRAPHIE"):
                continue
            if "A" in v:
                has_risk = any(k in v for k in "FGHKMRSTU") or (len(v.get("I", "")) > 4)
                header_like = set(v) <= {"A", "K", "M"} and all("CONTR" in norm(v[k]) for k in "KM" if k in v)
                if has_risk and not header_like:                       # activité + 1er risque
                    label = v["A"]
                    items.append(dict(kind="row", label=label, cont=False,
                                      **{k: v.get(COLS_A[k], "") for k in ROLES}))
                elif norm(v["A"]) != norm(title):                      # bandeau hiérarchique
                    rgb = (ws.cell(r, 1).fill.fgColor.rgb or "")[-6:]
                    items.append(dict(kind="head", text=v["A"], level=FILL_LEVEL.get(rgb, 2)))
                    label = v["A"]
            else:                                                       # ligne de suite
                data = {k: v.get(COLS_B[k], "") for k in ROLES}
                if any(data.values()):
                    items.append(dict(kind="row", label=label, cont=True, **data))
        sections[title] = items
    return sections


def render_cartographie(doc, sections):
    groups = [("Processus / Sous-processus", None, 0), ("RISQUE INHÉRENT", 3, 1),
              ("Facteurs de risques", None, 4), ("DISPOSITIF DE CONTRÔLE INTERNE", 2, 5),
              ("RISQUE RÉSIDUEL", 3, 7), ("Plan d'actions", None, 10)]
    sub = {1: "Prob.", 2: "Imp.", 3: "Amp.", 5: "1er échelon\nAuto-contrôle / contrôle hiérarchique",
           6: "2e échelon\nContrôle permanent / audit interne", 7: "Prob.", 8: "Imp.", 9: "Amp."}
    W = CARTO_W
    for n, (title, items) in enumerate(sections.items(), 1):
        heading(doc, f"{n}. {title}")
        t = new_table(doc, W)
        r1, r2 = add_row(t, True), add_row(t, True)
        c1, c2 = list(r1.cells), list(r2.cells)          # capturées avant toute fusion
        for txt, span, idx in groups:
            if span:
                c = merge_cells(c1, idx, idx + span - 1)
                set_cell(c, txt, sum(W[idx:idx + span]), BORDEAUX, True, color="FFFFFF", size=8,
                         align="center", valign="center", span=span)
            else:
                set_cell(c1[idx], txt, W[idx], BORDEAUX, True, color="FFFFFF", size=8,
                         align="center", valign="center", vm="restart")
                set_cell(c2[idx], "", W[idx], BORDEAUX, vm="cont")
        for idx, txt in sub.items():
            set_cell(c2[idx], txt, W[idx], BORDEAUX, True, color="FFFFFF", size=7,
                     align="center", valign="center")
        for it in items:
            row = add_row(t)
            if it["kind"] == "head":
                c = merge_cells(list(row.cells), 0, len(W) - 1)
                fill = [ROSE_MID, ROSE, ROSE_PALE, "FFFFFF"][min(it["level"], 3)]
                set_cell(c, it["text"], sum(W), fill, True, size=8.5, span=len(W), valign="center")
                continue
            lab = it["label"]
            if it["cont"]:
                set_cell(row.cells[0], f"↳ {lab}", W[0], ROSE, False, True, color="555555", size=7.5)
            else:
                set_cell(row.cells[0], lab, W[0], ROSE, True, size=8)
            for i, k in enumerate(ROLES, 1):
                num = k in ("prob", "imp", "amp", "rprob", "rimp", "ramp")
                set_cell(row.cells[i], it[k], W[i], size=8, align="center" if num else "left",
                         valign="center" if num else "top")
        spacer(doc)


# ================================================================ MODE 2 : générique
def blocks_of_sheet(ws):
    """Découpe un onglet en blocs de lignes séparés par >=1 ligne vide ; retire les colonnes vides.
    Détecte automatiquement la dernière colonne utile pour éviter les MemoryError."""
    
    # Détecter la dernière colonne réellement utilisée (non vide)
    max_col_used = 1
    for row in ws.iter_rows(min_row=1, max_row=min(ws.max_row, 1000), values_only=False):
        for cell in row:
            if cell.value is not None and clean(cell.value):
                max_col_used = max(max_col_used, cell.column)
    
    # Limiter à 200 colonnes max (sécurité supplémentaire)
    max_col_used = min(max_col_used, 200)
    
    # Charger uniquement les colonnes utiles
    rows = []
    for r in ws.iter_rows(min_col=1, max_col=max_col_used):
        rows.append([clean(c.value) for c in r])
    blocks, cur = [], []
    for r in rows:
        if any(r):
            cur.append(r)
        elif cur:
            blocks.append(cur)
            cur = []
    if cur:
        blocks.append(cur)
    out = []
    for b in blocks:
        keep = [j for j in range(max(len(r) for r in b)) if any(len(r) > j and r[j] for r in b)]
        out.append([[r[j] if j < len(r) else "" for j in keep] for r in b])
    return out


def render_generic(doc, wb):
    for ws in wb.worksheets:
        blocks = blocks_of_sheet(ws)
        if not blocks:
            continue
        heading(doc, ws.title)
        for k, b in enumerate(blocks, 1):
            ncol = len(b[0])
            if len(blocks) > 1:
                p = doc.add_paragraph()
                p.paragraph_format.keep_with_next = True
                style_run(p.add_run(f"Tableau {k}"), 9, True, color="444444")
            # largeur proportionnelle au contenu (bornée), somme = largeur utile
            lens = [min(60, max(6, max(len(x) for x in (r[j] for r in b)) if b else 6)) for j in range(ncol)]
            tot = sum(lens)
            W = [max(500, int(USABLE_W * l / tot)) for l in lens]
            W[-1] += USABLE_W - sum(W)
            size = 9 if ncol <= 6 else 8 if ncol <= 10 else 7
            t = new_table(doc, W)
            h = add_row(t, True)
            for j, txt in enumerate(b[0]):
                set_cell(h.cells[j], txt, W[j], BORDEAUX, True, color="FFFFFF", size=size,
                         align="center", valign="center")
            for r in b[1:]:
                row = add_row(t)
                for j, txt in enumerate(r):
                    first = j == 0
                    set_cell(row.cells[j], txt, W[j], ROSE if first else None, first, size=size)
            spacer(doc)


# ================================================================ main
def convert(src, dst, titre=None, mode="auto"):
    wb = load_workbook(src, data_only=True)
    carto = [ws for ws in wb.worksheets if is_carto(ws)]
    use_carto = mode == "cartographie" or (mode == "auto" and carto)
    titre = titre or "Cartographie des risques" if use_carto else (titre or "Export Excel")
    doc = setup_document(titre, "Document généré automatiquement à partir du fichier Excel source")

    if use_carto:
        sections = OrderedDict()
        for ws in carto:
            sections.update(parse_cartographie(ws))
        n_risk = sum(1 for items in sections.values() for i in items if i["kind"] == "row")
        info_table(doc, [
            ("Fichier source", src.replace("\\", "/").split("/")[-1]),
            ("Onglet(s) traité(s)", ", ".join(ws.title for ws in carto)),
            ("Processus couverts", " ; ".join(sections)),
            ("Nombre de lignes de risque / contrôle", str(n_risk)),
            ("Date de génération", dt.date.today().strftime("%d/%m/%Y")),
        ])
        render_cartographie(doc, sections)
    else:
        info_table(doc, [
            ("Fichier source", src.replace("\\", "/").split("/")[-1]),
            ("Onglet(s) traité(s)", ", ".join(ws.title for ws in wb.worksheets)),
            ("Date de génération", dt.date.today().strftime("%d/%m/%Y")),
        ])
        render_generic(doc, wb)
    doc.save(dst)
    return dst


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("src")
    ap.add_argument("dst")
    ap.add_argument("--titre")
    ap.add_argument("--mode", choices=["auto", "cartographie", "generic"], default="auto")
    a = ap.parse_args()
    print("OK ->", convert(a.src, a.dst, a.titre, a.mode))
