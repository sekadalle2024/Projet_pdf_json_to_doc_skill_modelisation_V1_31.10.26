#!/usr/bin/env python3
"""
json_to_word.py - Convertit des données JSON en documents Word (.docx) avec la même charte
que excel_to_word.py (A4 paysage, Calibri, en-têtes bordeaux 7B1E3A, première colonne rose
F2E6EA, bordures grises, ligne d'en-tête répétée, lignes non coupées, pagination).

STRUCTURE JSON ACCEPTÉE (souple)
  {
    "Nom de la feuille": [                      <- 1 clé racine = 1 feuille (section)
        { "table 0 - Titre": [ {..}, {..} ] },  <- 1 tableau = 1 liste d'enregistrements
        { "table 1": [ {..} ] },                   (le préfixe "table N - " est retiré du titre)
        ...
    ]
  }
  - Un fichier peut contenir PLUSIEURS objets JSON à la suite (comme dans l'exemple
    "Feuille couverture" x2) : chaque objet racine devient un document Word.
  - Variantes tolérées : {"feuille": {"tableau": [..]}}, {"feuille": [ {..}, {..} ]},
    une liste d'enregistrements seule, valeurs imbriquées (listes / objets) aplaties en texte.

MISE EN FORME AUTOMATIQUE SELON LA FORME DU TABLEAU
  - 1 enregistrement, 1 seul champ ............ bloc de texte (ex. OBJECTIFS)
  - 1 enregistrement, <=6 champs courts ........ tableau compact horizontal (ex. signatures)
  - 1 enregistrement, champs longs ............. fiche "Rubrique / Description"
  - plusieurs enregistrements ................. tableau à colonnes (largeurs calculées
                                                 selon le contenu, police réduite si large)
  - Coloration facultative : "Non-satisfaisant" / "-" en rouge pâle, "Satisfaisant" / "+" en vert pâle.

USAGE
    python json_to_word.py entree.json [sortie] [--fusion] [--titre "..."] [--pied "..."]
                           [--sans-couleurs] [--ecraser]
  entree : un fichier .json ou un dossier (tous les *.json)
  sortie : dossier de sortie (défaut : ./sorties_word), ou nom de fichier .docx avec --fusion
Dépendance : python-docx
"""
import argparse
import datetime as dt
import json
import re
from pathlib import Path
from statistics import mean

from docx import Document
from docx.enum.section import WD_ORIENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Pt, RGBColor, Twips

# ----------------------------------------------------------------- charte graphique
BORDEAUX, ROSE, GRIS, FONT = "7B1E3A", "F2E6EA", "999999", "Calibri"
PAGE_W, PAGE_H, MARGIN_LR = 16838, 11906, 720      # A4 paysage (DXA)
TOTAL_W = 15000                                    # largeur des tableaux (comme le modèle)
DEFAULT_FOOTER = "Automatisez vos activités d'audit, risques et contrôles - Whatsapp : + 225 05 44 13 07 98"
VERT, ROUGE = "DDEFD9", "F8D7DA"
COULEURS = {"satisfaisant": VERT, "+": VERT, "non-satisfaisant": ROUGE,
            "non satisfaisant": ROUGE, "-": ROUGE}


# ----------------------------------------------------------------- lecture / normalisation JSON
def load_json_objects(path):
    """Lit un fichier contenant 1..n objets JSON concaténés."""
    text = Path(path).read_text(encoding="utf-8-sig")
    dec, i, n, objs = json.JSONDecoder(), 0, len(text), []
    while True:
        while i < n and text[i] in " \t\r\n,":
            i += 1
        if i >= n:
            break
        try:
            obj, i = dec.raw_decode(text, i)
        except json.JSONDecodeError as e:
            raise SystemExit(f"JSON invalide dans {path} (ligne {e.lineno}, colonne {e.colno}) : {e.msg}")
        objs.append(obj)
    return objs


def clean(s):
    s = str(s).replace("\xa0", " ").replace("\r", "")
    s = "\n".join(re.sub(r"[ \t]+", " ", line).strip() for line in s.split("\n"))
    return re.sub(r"\n{3,}", "\n\n", s).strip()


def txt(v):
    """Valeur JSON -> texte (listes / objets imbriqués aplatis)."""
    if v is None:
        return ""
    if isinstance(v, bool):
        return "Oui" if v else "Non"
    if isinstance(v, float) and v.is_integer():
        return str(int(v))
    if isinstance(v, list):
        return clean("\n".join(txt(x) for x in v))
    if isinstance(v, dict):
        return clean("\n".join(f"{k} : {txt(x)}" for k, x in v.items()))
    return clean(v)


def nice_title(name):
    t = re.sub(r"^\s*table\s*\d*\s*[-–:]?\s*", "", str(name), flags=re.I).strip()
    return t[:1].upper() + t[1:] if t else ""


def to_table(records):
    """Liste d'enregistrements -> (en-têtes, lignes) ; colonnes = union des clés (ordre d'apparition)."""
    if isinstance(records, dict):
        records = [records]
    if not isinstance(records, list):
        records = [records]
    recs = [r if isinstance(r, dict) else {"Valeur": r} for r in records]
    headers = []
    for r in recs:
        for k in r:
            if k not in headers:
                headers.append(k)
    return [clean(h) for h in headers], [[txt(r.get(h)) for h in headers] for r in recs]


def is_wrapper(item):
    return isinstance(item, dict) and len(item) == 1 and isinstance(next(iter(item.values())), (list, dict))


def tables_of(content):
    """Contenu d'une feuille -> liste de (titre, en-têtes, lignes)."""
    out = []
    if isinstance(content, list) and content and all(is_wrapper(x) for x in content):
        for item in content:
            (name, recs), = item.items()
            out.append((nice_title(name), *to_table(recs)))
    elif isinstance(content, dict) and content and all(isinstance(v, (list, dict)) for v in content.values()):
        for name, recs in content.items():
            out.append((nice_title(name), *to_table(recs)))
    else:
        out.append(("", *to_table(content)))
    return [t for t in out if t[2]]          # ignore les tableaux sans ligne


def document_model(root):
    """Objet racine -> liste de (nom de feuille, [tableaux])."""
    if isinstance(root, dict):
        return [(str(k), tables_of(v)) for k, v in root.items()]
    return [("Données", tables_of(root))]


# ----------------------------------------------------------------- briques XML Word
def _el(tag, **attrs):
    e = OxmlElement(tag)
    for k, v in attrs.items():
        e.set(qn(k.replace("_", ":", 1)), str(v))
    return e


def style_run(run, size=9, bold=False, italic=False, color=None):
    run.font.name = FONT
    rf = run._r.get_or_add_rPr().find(qn("w:rFonts"))
    for a in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
        rf.set(qn(a), FONT)
    run.font.size = Pt(size)
    run.font.bold, run.font.italic = bold, italic
    if color:
        run.font.color.rgb = RGBColor.from_string(color)


def set_cell(cell, text, width, fill=None, bold=False, color=None, size=8,
             align="left", valign="top", mar=80):
    tcPr = cell._tc.get_or_add_tcPr()
    for child in list(tcPr):
        tcPr.remove(child)
    tcPr.append(_el("w:tcW", w_type="dxa", w_w=width))
    b = _el("w:tcBorders")
    for side in ("top", "left", "bottom", "right"):
        b.append(_el(f"w:{side}", w_val="single", w_color=GRIS, w_sz=4))
    tcPr.append(b)
    if fill:
        tcPr.append(_el("w:shd", w_fill=fill, w_color="auto", w_val="clear"))
    m = _el("w:tcMar")
    for side, w in (("top", 50), ("left", mar), ("bottom", 50), ("right", mar)):
        m.append(_el(f"w:{side}", w_type="dxa", w_w=w))
    tcPr.append(m)
    tcPr.append(_el("w:vAlign", w_val=valign))
    for i, line in enumerate((text or "").split("\n")):
        p = cell.paragraphs[0] if i == 0 else cell.add_paragraph()
        p.paragraph_format.space_before = p.paragraph_format.space_after = Pt(0)
        p.alignment = {"left": 0, "center": 1, "right": 2}[align]
        style_run(p.add_run(line), size, bold, color=color)


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
        look.addprevious(el)                      # ordre imposé par le schéma
    for gc, w in zip(t._tbl.tblGrid.findall(qn("w:gridCol")), widths):
        gc.set(qn("w:w"), str(w))
    return t


def add_row(table, header=False):
    row = table.add_row()
    trPr = row._tr.get_or_add_trPr()
    trPr.append(_el("w:cantSplit"))
    if header:
        trPr.append(_el("w:tblHeader"))
    return row


def add_field(par, code, size, color):
    """Champ Word (PAGE / NUMPAGES) en 5 runs : begin, instr, separate, résultat, end."""
    def run_with(el):
        r = par.add_run()
        style_run(r, size, color=color)
        r._r.append(el)
    run_with(_el("w:fldChar", w_fldCharType="begin"))
    it = OxmlElement("w:instrText")
    it.set(qn("xml:space"), "preserve")
    it.text = f" {code} "
    run_with(it)
    run_with(_el("w:fldChar", w_fldCharType="separate"))
    style_run(par.add_run("1"), size, color=color)
    run_with(_el("w:fldChar", w_fldCharType="end"))


def heading(doc, text, size=12, before=12, page_break=False):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(before)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.keep_with_next = True
    p.paragraph_format.page_break_before = page_break
    style_run(p.add_run(text), size, True, color=BORDEAUX)


def spacer(doc):
    doc.add_paragraph().paragraph_format.space_after = Pt(4)


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
        pPr.append(bd)                            # pBdr avant jc (ordre du schéma)
        par.alignment = align
        style_run(par.add_run(text), size, bold, color=color)

    band(sec.header.paragraphs[0], header_text, 10, True, BORDEAUX, "bottom")
    band(sec.footer.paragraphs[0], footer_text, 8, False, "444444", "top", align=1)
    fp = sec.footer.add_paragraph()
    fp.alignment = 1
    style_run(fp.add_run("Page "), 8, color="444444")
    add_field(fp, "PAGE", 8, "444444")
    style_run(fp.add_run(" / "), 8, color="444444")
    add_field(fp, "NUMPAGES", 8, "444444")
    return doc


# ----------------------------------------------------------------- largeurs et alignements
def compute_widths(headers, rows, total, size, pad=200):
    """Largeurs de colonnes selon le contenu : jamais plus étroit que le mot le plus long,
    le reste réparti en priorité aux colonnes de texte long."""
    cdx = size * 10.5                              # DXA par caractère (gras)
    words = lambda t: [w for w in re.split(r"[ \n]", t) if w]
    minw, want, boost = [], [], []
    for j, h in enumerate(headers):
        vals = [r[j] for r in rows if r[j]]
        lw = max(max((len(w) for w in words(h)), default=1),
                 min(max((len(w) for v in vals for w in words(v)), default=1), 16))
        avg = mean(max(len(l) for l in v.split("\n")) for v in vals) if vals else 1
        boost.append(3 if avg > 40 else 1)         # le texte long passe avant les colonnes courtes
        minw.append(max(520, int(lw * cdx + pad)))
        want.append(max(520, int(max(lw, min(avg, 60)) * cdx + pad)))
    smin = sum(minw)
    if smin > total:
        ws = [max(400, m * total / smin) for m in minw]
    else:
        extra, rem = [w - m for w, m in zip(want, minw)], total - smin
        se = sum(extra)
        if se <= rem:
            weights = extra if se else want
            left = total - sum(want)
            ws = [w + left * e / sum(weights) for w, e in zip(want, weights)]
        else:
            be = [e * b for e, b in zip(extra, boost)]
            ws = [m + rem * x / sum(be) for m, x in zip(minw, be)]
    ints = [int(x) for x in ws]
    ints[-1] += total - sum(ints)
    return ints


def col_align(vals):
    v = [x for x in vals if x]
    if not v or all(len(x) <= 6 for x in v) or all(re.fullmatch(r"\d{2}/\d{2}/\d{4}", x) for x in v):
        return "center"
    if all(re.fullmatch(r"-?[\d\s.,]+", x) for x in v):
        return "right"
    return "left"


def font_size(ncol):
    return 9 if ncol <= 6 else 8 if ncol <= 10 else 7.5 if ncol <= 14 else 7


# ----------------------------------------------------------------- rendu des tableaux
def render_table(doc, title, headers, rows, colors=True):
    rows = [[c.replace(" ", "\u00a0") if re.fullmatch(r"-?\d[\d ]*", c) else c for c in r] for r in rows]
    if title:
        heading(doc, title, size=11, before=10)
    ncol = len(headers)
    if len(rows) == 1 and ncol == 1:                                   # bloc de texte
        t = new_table(doc, [TOTAL_W])
        set_cell(add_row(t, True).cells[0], headers[0], TOTAL_W, BORDEAUX, True, "FFFFFF", 9, "center", "center")
        set_cell(add_row(t).cells[0], rows[0][0], TOTAL_W, size=9)
    elif len(rows) == 1 and ncol <= 6 and all(len(c) <= 40 and "\n" not in c for c in rows[0]):
        W = [TOTAL_W // ncol] * ncol                                   # tableau compact
        W[-1] += TOTAL_W - sum(W)
        t = new_table(doc, W)
        h, r = add_row(t, True), add_row(t)
        for j in range(ncol):
            set_cell(h.cells[j], headers[j], W[j], BORDEAUX, True, "FFFFFF", 9, "center", "center")
            set_cell(r.cells[j], rows[0][j], W[j], size=9, align="center", valign="center")
    elif len(rows) == 1:                                               # fiche Rubrique / Description
        W = [4200, 10800]
        t = new_table(doc, W)
        h = add_row(t, True)
        for c, s, w in zip(h.cells, ("Rubrique", "Description"), W):
            set_cell(c, s, w, BORDEAUX, True, "FFFFFF", 9, "center", "center")
        for k, v in zip(headers, rows[0]):
            r = add_row(t)
            set_cell(r.cells[0], k, W[0], ROSE, True, size=9, valign="center")
            set_cell(r.cells[1], v, W[1], size=9, valign="center")
    else:                                                              # tableau à colonnes
        size = font_size(ncol)
        dense = ncol > 12                          # tableau très large : marges réduites, pleine largeur utile
        mar, total = (45, 15350) if dense else (80, TOTAL_W)
        W = compute_widths(headers, rows, total, size, pad=2 * mar + 40)
        aligns = [col_align([r[j] for r in rows]) for j in range(ncol)]
        t = new_table(doc, W)
        h = add_row(t, True)
        for j in range(ncol):
            set_cell(h.cells[j], headers[j], W[j], BORDEAUX, True, "FFFFFF", size, "center", "center", mar)
        for data in rows:
            r = add_row(t)
            for j in range(ncol):
                fill, bold, color = (ROSE, True, None) if j == 0 else (None, False, None)
                key = data[j].strip().lower()
                if colors and j > 0 and key in COULEURS:
                    fill = COULEURS[key]
                    if key.startswith("non"):
                        bold, color = True, "9C1C1C"
                set_cell(r.cells[j], data[j], W[j], fill, bold, color, size, aligns[j],
                         "top" if aligns[j] == "left" else "center", mar)
    spacer(doc)


def render_document(doc, model, first=True, colors=True, show_title=True):
    for n, (sheet, tables) in enumerate(model):
        start = first and n == 0
        if show_title or not start:               # l'en-tête de page porte déjà le nom de la feuille
            heading(doc, sheet, size=14, before=0 if start else 12, page_break=not start)
        for title, headers, rows in tables:
            render_table(doc, title, headers, rows, colors)


# ----------------------------------------------------------------- nommage et exécution
def slug(s):
    return re.sub(r"[^\w\-.]+", "_", s, flags=re.UNICODE).strip("_") or "document"


def doc_code(model, fallback):
    """Code de référence (ex. FC-BK-A10) lu dans une colonne 'Reference', sinon repli."""
    for _, tables in model:
        for _, headers, rows in tables:
            for j, h in enumerate(headers):
                if re.fullmatch(r"r[ée]f[ée]rence", h.strip(), flags=re.I) and rows and rows[0][j]:
                    return slug(rows[0][j].split(" - ")[0])
    return slug(fallback)


def free_path(path, overwrite):
    if overwrite or not path.exists():
        return path
    return path.with_name(f"{path.stem}_{dt.datetime.now():%Y%m%d_%H%M%S}{path.suffix}")


def convert(src, out, fusion=False, titre=None, pied=DEFAULT_FOOTER, colors=True, overwrite=False):
    src = Path(src)
    files = sorted(src.glob("*.json")) if src.is_dir() else [src]
    if not files:
        raise SystemExit(f"Aucun fichier .json dans {src}")
    jobs = []                                      # (fichier, index, modèle)
    for f in files:
        for i, obj in enumerate(load_json_objects(f), 1):
            jobs.append((f, i, document_model(obj)))
    results = []
    if fusion:
        out = Path(out) if out and str(out).lower().endswith(".docx") else Path(out or "sorties_word") / "fusion.docx"
        out.parent.mkdir(parents=True, exist_ok=True)
        doc = setup_document(titre or jobs[0][2][0][0], pied)
        for k, (_, _, model) in enumerate(jobs):
            render_document(doc, model, first=(k == 0), colors=colors, show_title=True)
        out = free_path(out, overwrite)
        doc.save(out)
        results.append((out, sum(len(t) for _, _, m in jobs for _, t in m)))
    else:
        outdir = Path(out or "sorties_word")
        outdir.mkdir(parents=True, exist_ok=True)
        for f, i, model in jobs:
            doc = setup_document(titre or model[0][0], pied)
            render_document(doc, model, colors=colors, show_title=bool(titre) or len(model) > 1)
            path = free_path(outdir / f"{doc_code(model, f'{f.stem}_{i}')}.docx", overwrite)
            doc.save(path)
            results.append((path, sum(len(t) for _, t in model)))
    return results


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("src", help="fichier .json ou dossier")
    ap.add_argument("out", nargs="?", help="dossier de sortie (ou .docx avec --fusion)")
    ap.add_argument("--fusion", action="store_true", help="un seul .docx pour tous les objets JSON")
    ap.add_argument("--titre", help="texte de l'en-tête de page (défaut : nom de la feuille)")
    ap.add_argument("--pied", default=DEFAULT_FOOTER, help="texte du pied de page")
    ap.add_argument("--sans-couleurs", action="store_true", help="désactive la coloration +/-/Satisfaisant")
    ap.add_argument("--ecraser", action="store_true", help="écrase un .docx existant (sinon suffixe horodaté)")
    a = ap.parse_args()
    for path, n in convert(a.src, a.out, a.fusion, a.titre, a.pied, not a.sans_couleurs, a.ecraser):
        print(f"OK -> {path}  ({n} tableaux)")
