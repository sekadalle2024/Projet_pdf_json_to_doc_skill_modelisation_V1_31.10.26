#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
json2word_frap.py - Convertit un JSON d'audit (cles "table 1", "table 2"...) en .docx
au format du modele "Recos contrôle des comptes - Logiciel E-révision" (Modelisation_template).

Usage :
  python json2word_frap.py <fichier.json|.txt> -o <dossier_sortie> [--ref A210]
        [--software "Logiciel automatisé E-audit pro"] [--footer "..."] [--color 8B0000]
        [--step "Frap"] [--overwrite]

Regles de rendu (issues du modele et des contraintes) :
 - A4 paysage, marges haut 1200 / bas 1100 / gauche-droite 900 dxa, Arial 8,5 pt.
 - Entete : "<Logiciel> - <Etape de mission>" ; pied : "Automatisez vos activités d'audit, ... 98".
 - Corps = uniquement des TABLEAUX (separes par un paragraphe vide, jamais de titre).
 - En-tete de tableau : fond bordeaux (8B0000 par defaut), texte blanc gras, repete sur chaque page.
 - table 1 (dictionnaire)                    -> tableau VERTICAL "Rubrique | Description" (4000 | 11038),
                                                1re colonne : fond bordeaux + texte blanc gras.
 - table N = {"Titre": "texte"}              -> tableau 1 colonne : en-tete = Titre, corps = texte.
 - table N = {"k1": "...", "k2": "..."}      -> tableau vertical Rubrique | Description.
 - table N = [ {...}, {...} ]                -> tableau en colonnes (en-tetes = cles).
 - Texte multi-lignes : une ligne = un paragraphe ; lignes "- " conservees en puces a retrait ;
   ligne vide = respiration entre paragraphes. Aucun texte n'est reformule.
 - Etape "Feuille couverture"/"Couverture" : mention "Schéma de calcul : ..." retiree ; tableau de schema
   insere entre table 4 et table 5 si le JSON contient une cle "Schéma de calcul" (voir references/couverture.md).
"""
import argparse, json, os, random, re, string, sys
from docx import Document
from docx.shared import Pt, Emu
from docx.enum.section import WD_ORIENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

DEFAULT_SOFTWARE = "Logiciel automatisé E-audit pro"
DEFAULT_FOOTER = "Automatisez vos activités d'audit, risques et contrôles - Whatsapp : + 225 05 44 13 07 98"
DEFAULT_REF = "A210"
DEFAULT_COLOR = "8B0000"
PAGE_W, PAGE_H = 16838, 11906
MARG = dict(top=1200, right=900, bottom=1100, left=900)
TBL_W = 15038
COL_VERT = (4000, 11038)
FONT, SZ = "Arial", 17  # demi-points => 8,5 pt
BORDER = "BFBFBF"
DXA = 635  # 1 dxa = 635 EMU


# ---------------------------------------------------------------- utilitaires XML
def _fonts(rpr):
    f = OxmlElement("w:rFonts")
    for a in ("ascii", "hAnsi", "eastAsia", "cs"):
        f.set(qn("w:" + a), FONT)
    rpr.append(f)


def make_run(text, bold=False, color=None, size=SZ):
    r = OxmlElement("w:r")
    rpr = OxmlElement("w:rPr")
    _fonts(rpr)
    if bold:
        rpr.append(OxmlElement("w:b"))
        rpr.append(OxmlElement("w:bCs"))
    if color:
        c = OxmlElement("w:color")
        c.set(qn("w:val"), color)
        rpr.append(c)
    for tag in ("w:sz", "w:szCs"):
        s = OxmlElement(tag)
        s.set(qn("w:val"), str(size))
        rpr.append(s)
    r.append(rpr)
    t = OxmlElement("w:t")
    t.set(qn("xml:space"), "preserve")
    t.text = text
    r.append(t)
    return r


def make_par(text, bold=False, color=None, after=0, bullet=False):
    p = OxmlElement("w:p")
    ppr = OxmlElement("w:pPr")
    sp = OxmlElement("w:spacing")
    sp.set(qn("w:after"), str(after))
    ppr.append(sp)
    if bullet:
        ind = OxmlElement("w:ind")
        ind.set(qn("w:left"), "170")
        ind.set(qn("w:hanging"), "170")
        ppr.append(ind)
    p.append(ppr)
    if text != "":
        p.append(make_run(text, bold, color))
    return p


def make_cell(width, paras, fill=None):
    tc = OxmlElement("w:tc")
    pr = OxmlElement("w:tcPr")
    w = OxmlElement("w:tcW")
    w.set(qn("w:type"), "dxa")
    w.set(qn("w:w"), str(width))
    pr.append(w)
    b = OxmlElement("w:tcBorders")
    for side in ("top", "left", "bottom", "right"):
        e = OxmlElement("w:" + side)
        e.set(qn("w:val"), "single")
        e.set(qn("w:color"), BORDER)
        e.set(qn("w:sz"), "4")
        b.append(e)
    pr.append(b)
    if fill:
        sh = OxmlElement("w:shd")
        sh.set(qn("w:fill"), fill)
        sh.set(qn("w:color"), "auto")
        sh.set(qn("w:val"), "clear")
        pr.append(sh)
    m = OxmlElement("w:tcMar")
    for side, v in (("top", 80), ("left", 100), ("bottom", 80), ("right", 100)):
        e = OxmlElement("w:" + side)
        e.set(qn("w:type"), "dxa")
        e.set(qn("w:w"), str(v))
        m.append(e)
    pr.append(m)
    va = OxmlElement("w:vAlign")
    va.set(qn("w:val"), "center")
    pr.append(va)
    tc.append(pr)
    for p in paras:
        tc.append(p)
    return tc


def make_table(widths):
    tbl = OxmlElement("w:tbl")
    pr = OxmlElement("w:tblPr")
    w = OxmlElement("w:tblW")
    w.set(qn("w:type"), "dxa")
    w.set(qn("w:w"), str(sum(widths)))
    pr.append(w)
    bd = OxmlElement("w:tblBorders")
    for side in ("top", "left", "bottom", "right", "insideH", "insideV"):
        e = OxmlElement("w:" + side)
        e.set(qn("w:val"), "single")
        e.set(qn("w:color"), "auto")
        e.set(qn("w:sz"), "4")
        bd.append(e)
    pr.append(bd)
    lay = OxmlElement("w:tblLayout")
    lay.set(qn("w:type"), "fixed")
    pr.append(lay)
    tbl.append(pr)
    g = OxmlElement("w:tblGrid")
    for x in widths:
        c = OxmlElement("w:gridCol")
        c.set(qn("w:w"), str(x))
        g.append(c)
    tbl.append(g)
    return tbl


def make_row(cells, header=False):
    tr = OxmlElement("w:tr")
    if header:
        pr = OxmlElement("w:trPr")
        pr.append(OxmlElement("w:tblHeader"))
        tr.append(pr)
    for c in cells:
        tr.append(c)
    return tr


# ---------------------------------------------------------------- rendu du texte
def to_text(v):
    if v is None:
        return ""
    if isinstance(v, bool):
        return "Oui" if v else "Non"
    if isinstance(v, (int, float)):
        return str(v)
    if isinstance(v, list):
        return "\n".join(("- " + to_text(i)) if not isinstance(i, (dict, list)) else to_text(i) for i in v)
    if isinstance(v, dict):
        return "\n".join("- %s : %s" % (k, to_text(x).replace("\n", " ")) for k, x in v.items())
    return str(v)


def text_paras(text):
    """Une ligne = un paragraphe ; ligne vide => espace supplementaire apres le paragraphe precedent."""
    items = []
    for ln in text.replace("\r\n", "\n").replace("\r", "\n").split("\n"):
        if ln.strip() == "":
            if items:
                items[-1][2] = True
            continue
        items.append([ln.rstrip(), ln.lstrip().startswith("- "), False])
    if not items:
        return [make_par("", after=0)]
    out = []
    for i, (ln, bul, big) in enumerate(items):
        last = i == len(items) - 1
        after = 0 if last else (160 if big else 80)
        out.append(make_par(ln, bullet=bul, after=after))
    return out


# ---------------------------------------------------------------- tableaux
def tbl_single(title, text, fill):
    t = make_table([TBL_W])
    t.append(make_row([make_cell(TBL_W, [make_par(title, True, "FFFFFF")], fill)], header=True))
    t.append(make_row([make_cell(TBL_W, text_paras(text))]))
    return t


def tbl_vertical(d, fill, first_col_filled=False):
    t = make_table(list(COL_VERT))
    t.append(make_row([make_cell(COL_VERT[0], [make_par("Rubrique", True, "FFFFFF")], fill),
                       make_cell(COL_VERT[1], [make_par("Description", True, "FFFFFF")], fill)], header=True))
    for k, v in d.items():
        if first_col_filled:  # 1re colonne de la table 1 : fond bordeaux, texte blanc gras
            c0 = make_cell(COL_VERT[0], [make_par(str(k), True, "FFFFFF")], fill)
        else:
            c0 = make_cell(COL_VERT[0], [make_par(str(k))])
        t.append(make_row([c0, make_cell(COL_VERT[1], text_paras(to_text(v)))]))
    return t


def tbl_columns(rows, fill, widths=None):
    cols = []
    for r in rows:
        for k in r:
            if k not in cols:
                cols.append(k)
    n = len(cols)
    if widths is None:
        widths = [TBL_W // n] * n
        widths[-1] += TBL_W - sum(widths)
    t = make_table(widths)
    t.append(make_row([make_cell(w, [make_par(str(c), True, "FFFFFF")], fill) for w, c in zip(widths, cols)], header=True))
    for r in rows:
        t.append(make_row([make_cell(w, text_paras(to_text(r.get(c, "")))) for w, c in zip(widths, cols)]))
    return t


def schema_widths(rows, cols):
    """Largeur par colonne : le contenu tient sur UNE ligne (~115 dxa/caractere a 8,5 pt + marges)."""
    ws = []
    for c in cols:
        m = max([len(str(c))] + [len(to_text(r.get(c, ""))) for r in rows])
        ws.append(max(900, int(m * 115) + 260))
    tot = sum(ws)
    if tot < TBL_W:
        extra = TBL_W - tot
        ws = [w + int(extra * w / tot) for w in ws]
        ws[-1] += TBL_W - sum(ws)
    return ws


# ---------------------------------------------------------------- JSON
def load_json(path):
    raw = open(path, "rb").read().decode("utf-8-sig", errors="replace")
    if "Ã" in raw or "Â" in raw:
        print("ATTENTION : caracteres illisibles (Ã©...) - encodage a verifier, non repare.", file=sys.stderr)
    s = raw.find("{")
    if s < 0:
        raise ValueError("aucun objet JSON trouve")
    obj, _ = json.JSONDecoder().raw_decode(raw[s:])
    return obj


def extract_tables(obj):
    """-> (cle_racine, [(num, nom, valeur)])"""
    if not isinstance(obj, dict) or len(obj) < 1:
        raise ValueError("racine JSON invalide")
    root = next(iter(obj))
    items = obj[root]
    if isinstance(items, dict):
        items = [{k: v} for k, v in items.items()]
    out = []
    for it in items:
        for k, v in it.items():
            m = re.match(r"\s*table\s*(\d+)", k, re.I)
            out.append((int(m.group(1)) if m else len(out) + 1, k, v))
    if not out:
        raise ValueError("aucune cle 'table N'")
    return root, out


def get_step(root, tables):
    for n, k, v in tables:
        if isinstance(v, dict) and "Etape de mission" in v:
            return str(v["Etape de mission"]).strip()
    return re.sub(r"^\s*Etape\s+mission\s*-\s*", "", root, flags=re.I).strip() or "Etape"


def gen_ref():
    return "".join(random.choice(string.ascii_uppercase) for _ in range(random.choice((1, 2)))) + \
           "".join(random.choice(string.digits) for _ in range(random.choice((2, 3))))


def safe_name(ref, step, software):
    s = re.sub(r'[\\/:*?"<>|]', "", step).strip().replace(" ", "_")
    return re.sub(r'[\\/:*?"<>|]', "", "%s-%s- %s" % (ref, s, software)).strip() + ".docx"


SCHEMA_RE = re.compile(r"\s*Sch[ée]ma de calcul\s*:\s*C\s*=\s*A\s*\+\s*B\s*;\s*[ÉEé]cart\s*=\s*C\s*[−\-–]\s*D\.?", re.I)


def strip_schema_mention(v):
    if isinstance(v, str):
        return SCHEMA_RE.sub("", v).strip()
    if isinstance(v, list):
        return [strip_schema_mention(x) for x in v]
    if isinstance(v, dict):
        return {k: strip_schema_mention(x) for k, x in v.items()}
    return v


# ---------------------------------------------------------------- construction
def build(json_path, out_dir, ref=None, software=DEFAULT_SOFTWARE, footer=DEFAULT_FOOTER,
          color=DEFAULT_COLOR, step=None, overwrite=False):
    obj = load_json(json_path)
    root, tables = extract_tables(obj)
    step = step or get_step(root, tables)
    ref = ref or DEFAULT_REF
    cover = bool(re.search(r"couverture", step, re.I))

    schema = None
    if cover:
        kept = []
        for n, k, v in tables:
            if isinstance(v, dict) and "Etape de mission" in v:
                kept.append((n, k, strip_schema_mention(v)))
                continue
            head = k
            if isinstance(v, dict) and len(v) == 1:
                head += " " + next(iter(v))
            if re.search(r"sch[ée]ma", head, re.I):
                inner = next(iter(v.values())) if isinstance(v, dict) and len(v) == 1 else v
                if isinstance(inner, (list, dict)):
                    schema = inner
                    continue
            kept.append((n, k, strip_schema_mention(v)))
        tables = kept

    doc = Document()
    sec = doc.sections[0]
    sec.orientation = WD_ORIENT.LANDSCAPE
    sec.page_width, sec.page_height = Emu(PAGE_W * DXA), Emu(PAGE_H * DXA)
    sec.top_margin, sec.bottom_margin = Emu(MARG["top"] * DXA), Emu(MARG["bottom"] * DXA)
    sec.left_margin, sec.right_margin = Emu(MARG["left"] * DXA), Emu(MARG["right"] * DXA)
    sec.header_distance = sec.footer_distance = Emu(708 * DXA)
    st = doc.styles["Normal"]
    st.font.name = FONT
    st.font.size = Pt(8.5)
    st.element.get_or_add_rPr().get_or_add_rFonts().set(qn("w:eastAsia"), FONT)
    st.paragraph_format.space_after = Pt(0)

    for part, txt, bold in ((sec.header, "%s - %s" % (software, step), True), (sec.footer, footer, False)):
        p = part.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for r in list(p.runs):
            r._r.getparent().remove(r._r)
        p._p.append(make_run(txt, bold, color, 16))

    body = doc.element.body
    for p in list(doc.paragraphs):
        body.remove(p._p)
    sectpr = body.find(qn("w:sectPr"))

    def put(el):
        sectpr.addprevious(el)

    def spacer():
        put(make_par("", after=100))

    first = True
    for n, k, v in tables:
        if not first:
            spacer()
        first = False
        if isinstance(v, dict):
            if n == 1 or len(v) != 1 or isinstance(next(iter(v.values())), (dict, list)):
                put(tbl_vertical(v, color, first_col_filled=(n == 1)))
            else:
                key, val = next(iter(v.items()))
                put(tbl_single(str(key), to_text(val), color))
        elif isinstance(v, list) and v and all(isinstance(x, dict) for x in v):
            put(tbl_columns(v, color))
        else:
            put(tbl_single("Description", to_text(v), color))
        if schema is not None and n == 4:
            spacer()
            rows = schema if isinstance(schema, list) else [schema]
            cols = []
            for r in rows:
                for c in r:
                    if c not in cols:
                        cols.append(c)
            put(tbl_columns(rows, color, schema_widths(rows, cols)))
    if cover and schema is None:
        print("INFO : etape couverture sans cle 'Schéma de calcul' dans le JSON -> aucun tableau de schema insere.",
              file=sys.stderr)

    end = make_par("", after=0)
    rpr = OxmlElement("w:rPr")
    sz = OxmlElement("w:sz")
    sz.set(qn("w:val"), "2")
    rpr.append(sz)
    end.find(qn("w:pPr")).append(rpr)
    put(end)

    os.makedirs(out_dir, exist_ok=True)
    out = os.path.join(out_dir, safe_name(ref, step, software))
    if os.path.exists(out) and not overwrite:
        raise FileExistsError("existe deja : %s (utiliser --overwrite ou une autre --ref)" % out)
    doc.save(out)
    return out, ref, step


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("json")
    ap.add_argument("-o", "--out", default=".")
    ap.add_argument("--ref", default=None, help="Valeur alphanumerique (defaut A210 ; 'auto' = generee)")
    ap.add_argument("--software", default=DEFAULT_SOFTWARE)
    ap.add_argument("--footer", default=DEFAULT_FOOTER)
    ap.add_argument("--color", default=DEFAULT_COLOR)
    ap.add_argument("--step", default=None)
    ap.add_argument("--overwrite", action="store_true")
    a = ap.parse_args()
    ref = gen_ref() if (a.ref or "").lower() == "auto" else a.ref
    try:
        out, ref, step = build(a.json, a.out, ref, a.software, a.footer, a.color, a.step, a.overwrite)
    except Exception as e:
        print("ERREUR :", e, file=sys.stderr)
        sys.exit(1)
    print("OK  ref=%s  etape=%s\n%s" % (ref, step, out))
