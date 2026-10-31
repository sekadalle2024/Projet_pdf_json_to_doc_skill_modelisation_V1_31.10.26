#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Controle d'un .docx genere : python verifier_docx.py <docx> <json> [--software ...] [--color 8B0000]"""
import os
import re
import sys
import argparse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from docx import Document
from docx.oxml.ns import qn
from json2word_frap import (load_json, extract_tables, get_step, DEFAULT_SOFTWARE,
                            DEFAULT_FOOTER, DEFAULT_COLOR, SCHEMA_RE)


def norm(s):
    return re.sub(r"\s+", " ", s).strip()


def leaves(x):
    if isinstance(x, dict):
        for vv in x.values():
            yield from leaves(vv)
    elif isinstance(x, list):
        for i in x:
            yield from leaves(i)
    elif isinstance(x, str):
        yield SCHEMA_RE.sub("", x)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("docx")
    ap.add_argument("json")
    ap.add_argument("--software", default=DEFAULT_SOFTWARE)
    ap.add_argument("--color", default=DEFAULT_COLOR)
    a = ap.parse_args()
    d = Document(a.docx)
    state = {"ok": True}

    def chk(cond, msg):
        print(("OK    " if cond else "ECHEC ") + msg)
        state["ok"] = state["ok"] and bool(cond)

    root, tabs = extract_tables(load_json(a.json))
    step = get_step(root, tabs)
    s = d.sections[0]
    chk(s.page_width > s.page_height, "A4 paysage")
    chk(norm(s.header.paragraphs[0].text) == "%s - %s" % (a.software, step),
        "entete = '%s - %s'" % (a.software, step))
    chk(norm(s.footer.paragraphs[0].text) == DEFAULT_FOOTER, "pied de page WhatsApp")
    chk(all(p.text.strip() == "" for p in d.paragraphs), "aucun titre/texte hors tableaux")
    minimum = len(tabs) - (1 if re.search("couverture", step, re.I) else 0)
    chk(len(d.tables) >= minimum, "nombre de tableaux (%d)" % len(d.tables))
    fills = [t.rows[0].cells[0]._tc.find(qn("w:tcPr")).find(qn("w:shd")) for t in d.tables]
    chk(all(f is not None and f.get(qn("w:fill")) == a.color for f in fills),
        "fond d'en-tete %s sur tous les tableaux" % a.color)
    chk(all(t.rows[0]._tr.find(qn("w:trPr")) is not None for t in d.tables), "ligne d'en-tete repetee")
    chk(d.tables[0].rows[0].cells[0].text == "Rubrique" and len(d.tables[0].columns) == 2,
        "table 1 verticale (Rubrique | Description)")
    t1 = d.tables[0]
    c1 = [r.cells[0]._tc for r in t1.rows]
    def okc(tc):
        shd = tc.find(qn("w:tcPr")).find(qn("w:shd"))
        col = tc.find(".//" + qn("w:color"))
        return shd is not None and shd.get(qn("w:fill")) == a.color and col is not None and col.get(qn("w:val")) == "FFFFFF"
    chk(all(okc(tc) for tc in c1), "table 1 : colonne 1 en fond %s, texte blanc" % a.color)
    doc_txt = norm(" ".join(c.text for t in d.tables for r in t.rows for c in r.cells))
    miss = []
    for n, k, v in tabs:
        for t in leaves(v):
            for line in t.split("\n"):
                if line.strip() and norm(line) not in doc_txt:
                    miss.append(norm(line)[:70])
    chk(not miss, "aucun texte du JSON perdu" + ("" if not miss else " -> manquants : %s" % miss[:3]))
    print("\nRESULTAT :", "CONFORME" if state["ok"] else "NON CONFORME")
    sys.exit(0 if state["ok"] else 1)


main()
