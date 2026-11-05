#!/usr/bin/env python3
"""Rend un JSON de cartographie/etape de mission avec [Modélisation design]
(en-têtes horizontaux regroupés) en Word, Excel et/ou PDF.

Usage:
  conda activate pdf_excel_env
  python render_design.py --json data.json --format docx,xlsx,pdf \
      --software "Logiciel automatisé E-audit pro 2.0" --ref CR010 --out-dir ./out

Format JSON attendu (Formatage data Type 1):
 {"Etape mission - X":[{"table 1":{...}},{"table 2":[{"no":1,"Groupe":{"Col":"v",...},...}]}, ...autres tables...]}
Valeur scalaire = colonne pivot ; dict = groupe (niveau 1) ; dict de dict = 3 niveaux.
"""
import argparse, json, re, sys
from pathlib import Path

BORDEAUX = "800020"
FOOTER = "Automatisez vos activités d'audit, risques et contrôles - Whatsapp : + 225 05 44 13 07 98"
LVL = {"Élevé": "FF0000", "Eleve": "FF0000", "Moyen": "FFFF00", "Faible": "00B050"}


def level_fill(v):
    s = str(v)
    for k, c in LVL.items():
        if s.startswith(k):
            return c
    return None


def flat(v):
    if isinstance(v, list):
        return "\n".join(flat(x) for x in v)
    if isinstance(v, dict):
        return " ; ".join(f"{k} : {flat(x)}" for k, x in v.items())
    return "" if v is None else str(v)


# ---------- arbre d'en-têtes ----------
def build_tree(rows):
    tree = {}
    def merge(node, row):
        for k, v in row.items():
            if isinstance(v, dict):
                node.setdefault(k, {}); merge(node[k], v)
            else:
                node.setdefault(k, None)
    for r in rows:
        merge(tree, r)
    return tree

def leaves(tree, path=()):
    for k, v in tree.items():
        if v is None:
            yield path + (k,)
        else:
            yield from leaves(v, path + (k,))

def header_matrix(tree):
    """-> depth, cells[(r,c,rowspan,colspan,label)], leaf paths"""
    paths = list(leaves(tree))
    depth = max(len(p) for p in paths)
    cells, col = [], 0
    def count(node):
        return 1 if node is None else sum(count(v) for v in node.values())
    def walk(node, r, c):
        for k, v in node.items():
            n = count(v)
            if v is None:
                cells.append((r, c, depth - r, 1, k))
            else:
                cells.append((r, c, 1, n, k))
                walk(v, r + 1, c)
            c += n
        return c
    walk(tree, 0, 0)
    return depth, cells, paths

def get(row, path):
    v = row
    for k in path:
        v = v.get(k, "") if isinstance(v, dict) else ""
    return v


def col_weights(rows, paths):
    out = []
    for p in paths:
        L = max([len(str(get(r_, p))) for r_ in rows] + [0])
        hw = max(len(w) for w in p[-1].split())
        out.append(min(max(L, hw + 1, 4), 60))
    return out


# ---------- extraction du JSON ----------
def load(json_path):
    data = json.loads(Path(json_path).read_text(encoding="utf8"))
    title, tables = next(iter(data.items()))
    meta, main, others = None, None, []
    for t in tables:
        (name, content), = t.items()
        if isinstance(content, dict) and meta is None:
            meta = (name, content)
        elif isinstance(content, list) and main is None and content and any(isinstance(v, dict) for v in content[0].values()):
            main = (name, content)
        else:
            others.append((name, content))
    if main is None:  # pas de design: premiere table liste
        for i, (n, c) in enumerate(others):
            if isinstance(c, list):
                main = (n, c); others.pop(i); break
    return title, meta, main, others

def etape_name(meta, title):
    if meta and "Etape de mission" in meta[1]:
        return meta[1]["Etape de mission"]
    return title.replace("Etape mission - ", "")

def safe(s):
    return re.sub(r'[\\/:*?"<>|]', "", s).strip()


# ---------- DOCX ----------
def to_docx(path, title, meta, main, others, software, etape):
    from docx import Document
    from docx.enum.section import WD_ORIENT
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.enum.table import WD_ALIGN_VERTICAL
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn
    from docx.shared import Pt, Cm, RGBColor

    doc = Document()
    sec = doc.sections[0]
    sec.orientation = WD_ORIENT.LANDSCAPE
    sec.page_width, sec.page_height = Cm(29.7), Cm(21.0)
    for m in ("left_margin", "right_margin"): setattr(sec, m, Cm(1.5))
    sec.top_margin = sec.bottom_margin = Cm(1.8)
    for part, txt in ((sec.header, f"{software} - {etape}"), (sec.footer, FOOTER)):
        p = part.paragraphs[0]; p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(txt); r.font.size = Pt(8); r.font.color.rgb = RGBColor(0x80, 0x80, 0x80)

    def shade(cell, fill):
        tcPr = cell._tc.get_or_add_tcPr()
        for e in tcPr.findall(qn("w:shd")): tcPr.remove(e)
        s = OxmlElement("w:shd"); s.set(qn("w:val"), "clear"); s.set(qn("w:color"), "auto"); s.set(qn("w:fill"), fill)
        tcPr.append(s)

    def borders(table):
        tblPr = table._tbl.tblPr
        b = OxmlElement("w:tblBorders")
        for side in ("top", "left", "bottom", "right", "insideH", "insideV"):
            e = OxmlElement(f"w:{side}"); e.set(qn("w:val"), "single"); e.set(qn("w:sz"), "4"); e.set(qn("w:color"), "808080"); b.append(e)
        tblPr.append(b)

    def put(cell, text, size, bold=False, white=False, center=False):
        cell.text = ""
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER if center else WD_ALIGN_PARAGRAPH.LEFT
        r = p.add_run(str(text)); r.font.size = Pt(size); r.bold = bold
        if white: r.font.color.rgb = RGBColor(255, 255, 255)
        cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER

    def repeat_header(row):
        trPr = row._tr.get_or_add_trPr(); e = OxmlElement("w:tblHeader"); e.set(qn("w:val"), "true"); trPr.append(e)

    def no_split(row):
        trPr = row._tr.get_or_add_trPr(); trPr.append(OxmlElement("w:cantSplit"))

    def vertical_table(content):  # tables d'information : libellé | valeur
        t = doc.add_table(rows=0, cols=2); borders(t); t.autofit = False
        for k, v in content.items():
            cells = t.add_row().cells
            put(cells[0], k, 9.5, bold=True, white=True); shade(cells[0], BORDEAUX)
            put(cells[1], flat(v), 9.5)
        t.columns[0].width = Cm(5); t.columns[1].width = Cm(21.5)
        for row in t.rows:
            row.cells[0].width = Cm(5); row.cells[1].width = Cm(21.5)

    def spacer():
        p = doc.add_paragraph(); p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.space_before = Pt(0)
        for r in p.runs: r.font.size = Pt(2)

    first = True
    if meta:
        vertical_table(meta[1]); first = False
    # légende E/M/F (couleurs)
    if main:
        if not first: spacer()
        lg = doc.add_table(rows=1, cols=3); borders(lg)
        for c, (txt, col) in zip(lg.rows[0].cells, (("E : Élevé", "FF0000"), ("M : Moyen", "FFFF00"), ("F : Faible", "00B050"))):
            put(c, txt, 9.5, bold=True, center=True); shade(c, col)
        spacer()
        rows = main[1]
        tree = build_tree(rows); depth, hcells, paths = header_matrix(tree)
        ncols = len(paths)
        t = doc.add_table(rows=depth + len(rows), cols=ncols); borders(t); t.autofit = False
        for (r, c, rs, cs, label) in hcells:
            a = t.cell(r, c); b = t.cell(r + rs - 1, c + cs - 1)
            m = a.merge(b) if (rs > 1 or cs > 1) else a
            put(m, label, 8, bold=True, white=True, center=True); shade(m, BORDEAUX)
        for i in range(depth): repeat_header(t.rows[i])
        # largeurs: proportion du contenu
        total = 26.5
        lens = col_weights(rows, paths)
        s = sum(lens); widths = [Cm(total * l / s) for l in lens]
        for ri, row in enumerate(rows):
            tr = t.rows[depth + ri]; no_split(tr)
            for ci, p in enumerate(paths):
                v = get(row, p); cell = tr.cells[ci]
                f = level_fill(v) if re.search(r"probab|impact|criticit|évaluation|evaluation", p[-1], re.I) else None
                put(cell, v, 7, bold=bool(f), center=bool(f) or ci == 0)
                if f: shade(cell, f)
        for row in t.rows:
            for ci, w in enumerate(widths): row.cells[ci].width = w
        # fusion verticale des valeurs répétées (Cycle, Processus, Sous-processus...)
        for ci, p in enumerate(paths):
            if re.search(r"^(cycle|processus|sous[- ]?processus)$", p[-1], re.I):
                start = 0
                for ri in range(1, len(rows) + 1):
                    if ri == len(rows) or get(rows[ri], p) != get(rows[start], p):
                        if ri - start > 1:
                            m = t.cell(depth + start, ci).merge(t.cell(depth + ri - 1, ci))
                            put(m, get(rows[start], p), 7, bold=True)
                        start = ri
    for name, content in others:
        spacer()
        if isinstance(content, dict):
            vertical_table(content)
        elif isinstance(content, list) and content and isinstance(content[0], dict):
            keys = list(content[0].keys())
            t = doc.add_table(rows=1 + len(content), cols=len(keys)); borders(t)
            for i, k in enumerate(keys):
                put(t.cell(0, i), k, 8, bold=True, white=True, center=True); shade(t.cell(0, i), BORDEAUX)
            repeat_header(t.rows[0])
            for ri, row in enumerate(content, 1):
                for i, k in enumerate(keys):
                    put(t.cell(ri, i), flat(row.get(k, "")), 8)
    doc.save(path)


# ---------- XLSX ----------
def to_xlsx(path, title, meta, main, others, software, etape):
    from openpyxl import Workbook
    from openpyxl.styles import PatternFill, Font, Alignment, Border, Side
    from openpyxl.utils import get_column_letter
    wb = Workbook(); thin = Side(style="thin", color="808080"); B = Border(left=thin, right=thin, top=thin, bottom=thin)
    hf = PatternFill("solid", fgColor=BORDEAUX); hfont = Font(bold=True, color="FFFFFF")
    def foot(ws):
        ws.oddHeader.center.text = f"{software} - {etape}"; ws.oddFooter.center.text = FOOTER
        ws.page_setup.orientation = "landscape"
    if meta:
        ws = wb.active; ws.title = "Informations"
        for i, (k, v) in enumerate(meta[1].items(), 1):
            a = ws.cell(i, 1, k); a.fill = hf; a.font = hfont; a.border = B
            b = ws.cell(i, 2, flat(v)); b.alignment = Alignment(wrap_text=True, vertical="top"); b.border = B
        ws.column_dimensions["A"].width = 28; ws.column_dimensions["B"].width = 110; foot(ws)
    if main:
        ws = wb.create_sheet("Données") if meta else wb.active
        rows = main[1]; tree = build_tree(rows); depth, hcells, paths = header_matrix(tree)
        for (r, c, rs, cs, label) in hcells:
            if rs > 1 or cs > 1:
                ws.merge_cells(start_row=r + 1, start_column=c + 1, end_row=r + rs, end_column=c + cs)
            cell = ws.cell(r + 1, c + 1, label); cell.fill = hf; cell.font = hfont
            cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        for r in range(1, depth + 1):
            for c in range(1, len(paths) + 1): ws.cell(r, c).border = B; ws.cell(r, c).fill = hf
        for ri, row in enumerate(rows, depth + 1):
            for ci, p in enumerate(paths, 1):
                v = get(row, p); cell = ws.cell(ri, ci, v if not isinstance(v, (dict, list)) else flat(v))
                cell.border = B; cell.alignment = Alignment(wrap_text=True, vertical="top")
                f = level_fill(v) if re.search(r"probab|impact|criticit", p[-1], re.I) else None
                if f: cell.fill = PatternFill("solid", fgColor=f); cell.font = Font(bold=True)
        for ci, p in enumerate(paths, 1):
            L = max([len(str(get(r_, p))) for r_ in rows] + [len(p[-1])])
            ws.column_dimensions[get_column_letter(ci)].width = min(max(L * 0.9, 8), 45)
        ws.freeze_panes = ws.cell(depth + 1, 1)
        ws.auto_filter.ref = f"A{depth}:{get_column_letter(len(paths))}{depth + len(rows)}"; foot(ws)
    for name, content in others:
        ws = wb.create_sheet(re.sub(r"[\\/*?:\[\]]", "", name)[:31])
        if isinstance(content, dict): content = [{"Rubrique": k, "Valeur": flat(v)} for k, v in content.items()]
        if content and isinstance(content[0], dict):
            keys = list(content[0].keys())
            for i, k in enumerate(keys, 1):
                c = ws.cell(1, i, k); c.fill = hf; c.font = hfont; ws.column_dimensions[get_column_letter(i)].width = 40
            for ri, row in enumerate(content, 2):
                for i, k in enumerate(keys, 1): ws.cell(ri, i, flat(row.get(k, ""))).alignment = Alignment(wrap_text=True)
        foot(ws)
    wb.save(path)


# ---------- PDF ----------
def to_pdf(path, title, meta, main, others, software, etape):
    from reportlab.lib.pagesizes import A4, landscape
    from reportlab.lib import colors
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    font, fontb = "Helvetica", "Helvetica-Bold"
    for reg, bold in (("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"),
                      ("C:/Windows/Fonts/arial.ttf", "C:/Windows/Fonts/arialbd.ttf")):
        if Path(reg).exists() and Path(bold).exists():
            pdfmetrics.registerFont(TTFont("F", reg)); pdfmetrics.registerFont(TTFont("FB", bold)); font, fontb = "F", "FB"; break
    bord = colors.HexColor("#" + BORDEAUX)
    st = ParagraphStyle("c", fontName=font, fontSize=6.5, leading=7.6)
    sth = ParagraphStyle("h", fontName=fontb, fontSize=7, leading=8, textColor=colors.white, alignment=1)
    sti = ParagraphStyle("i", fontName=font, fontSize=8.5, leading=10)
    stib = ParagraphStyle("ib", fontName=fontb, fontSize=8.5, leading=10, textColor=colors.white)
    esc = lambda s: str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace("\n", "<br/>")
    W = landscape(A4)[0] - 40
    story = []
    grid = [("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#808080")), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("LEFTPADDING", (0, 0), (-1, -1), 2.5), ("RIGHTPADDING", (0, 0), (-1, -1), 2.5), ("TOPPADDING", (0, 0), (-1, -1), 2), ("BOTTOMPADDING", (0, 0), (-1, -1), 2)]
    if meta:
        data = [[Paragraph(esc(k), stib), Paragraph(esc(flat(v)), sti)] for k, v in meta[1].items()]
        t = Table(data, colWidths=[120, W - 120]); t.setStyle(TableStyle(grid + [("BACKGROUND", (0, 0), (0, -1), bord)])); story += [t, Spacer(1, 8)]
    if main:
        rows = main[1]; tree = build_tree(rows); depth, hcells, paths = header_matrix(tree)
        data = [[""] * len(paths) for _ in range(depth)]; spans = []; style = list(grid)
        for (r, c, rs, cs, label) in hcells:
            data[r][c] = Paragraph(esc(label), sth)
            if rs > 1 or cs > 1: spans.append(("SPAN", (c, r), (c + cs - 1, r + rs - 1)))
        for ri, row in enumerate(rows):
            line = []
            for ci, p in enumerate(paths):
                v = get(row, p); line.append(Paragraph(esc(flat(v)), st))
                f = level_fill(v) if re.search(r"probab|impact|criticit", p[-1], re.I) else None
                if f: style.append(("BACKGROUND", (ci, depth + ri), (ci, depth + ri), colors.HexColor("#" + f)))
            data.append(line)
        lens = col_weights(rows, paths)
        base = 22; cw = [base + (W - base * len(lens)) * l / sum(lens) for l in lens]
        t = Table(data, colWidths=cw, repeatRows=depth)
        t.setStyle(TableStyle(style + spans + [("BACKGROUND", (0, 0), (-1, depth - 1), bord)])); story.append(t)
    for name, content in others:
        story.append(Spacer(1, 8))
        if isinstance(content, dict): content = [{"Rubrique": k, "Valeur": flat(v)} for k, v in content.items()]
        if content and isinstance(content[0], dict):
            keys = list(content[0].keys())
            data = [[Paragraph(esc(k), sth) for k in keys]] + [[Paragraph(esc(flat(r.get(k, ""))), st) for k in keys] for r in content]
            t = Table(data, repeatRows=1); t.setStyle(TableStyle(grid + [("BACKGROUND", (0, 0), (-1, 0), bord)])); story.append(t)
    def deco(c, d):
        c.saveState(); c.setFont(font, 7); c.setFillColor(colors.grey)
        w, h = landscape(A4); c.drawCentredString(w / 2, h - 22, f"{software} - {etape}"); c.drawCentredString(w / 2, 16, FOOTER); c.restoreState()
    SimpleDocTemplate(str(path), pagesize=landscape(A4), leftMargin=20, rightMargin=20, topMargin=36, bottomMargin=32).build(story, onFirstPage=deco, onLaterPages=deco)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", required=True); ap.add_argument("--format", default="docx")
    ap.add_argument("--software", default="Logiciel automatisé E-audit pro 2.0")
    ap.add_argument("--ref", default=""); ap.add_argument("--out-dir", default=".")
    a = ap.parse_args()
    title, meta, main_t, others = load(a.json)
    etape = etape_name(meta, title)
    ref = a.ref or (meta[1].get("Reference") if meta and meta[1].get("Reference") else "")
    if not re.fullmatch(r"[A-Za-z]{1,2}\d{2,3}", ref):
        ref = "".join(w[0] for w in etape.split()[:2]).upper()[:2] + "010"
    base = safe(f"{ref} - {etape}- {a.software}")
    out = Path(a.out_dir); out.mkdir(parents=True, exist_ok=True)
    for f in [x.strip().lower() for x in a.format.split(",")]:
        p = out / f"{base}.{f}"
        if f == "docx": to_docx(p, title, meta, main_t, others, a.software, etape)
        elif f == "xlsx": to_xlsx(p, title, meta, main_t, others, a.software, etape)
        elif f == "pdf": to_pdf(p, title, meta, main_t, others, a.software, etape)
        elif f == "json": (out / f"{base}.json").write_text(Path(a.json).read_text(encoding="utf8"), encoding="utf8")
        else: print(f"format inconnu: {f}", file=sys.stderr); continue
        print(p)

if __name__ == "__main__":
    main()
