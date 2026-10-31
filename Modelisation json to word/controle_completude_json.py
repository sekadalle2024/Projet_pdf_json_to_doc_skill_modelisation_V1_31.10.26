#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Contrôle de complétude : vérifier que toutes les valeurs JSON sont dans le Word"""

import json
import re
from pathlib import Path
from docx import Document

def normaliser(texte):
    """Normalise un texte : espaces insécables, espaces multiples"""
    if not texte:
        return ""
    s = str(texte).replace('\xa0', ' ').replace('\r', '')
    s = re.sub(r'\s+', ' ', s).strip()
    return s.upper()

def extraire_valeurs_json(fichier_json):
    """Extrait toutes les valeurs texte significatives (≥3 caractères) du JSON"""
    text = Path(fichier_json).read_text(encoding="utf-8-sig")
    dec = json.JSONDecoder()
    obj, _ = dec.raw_decode(text)
    
    valeurs = []
    
    def parcourir(data, chemin=""):
        if isinstance(data, dict):
            for k, v in data.items():
                parcourir(v, f"{chemin}.{k}" if chemin else k)
        elif isinstance(data, list):
            for i, item in enumerate(data):
                parcourir(item, f"{chemin}[{i}]")
        elif data is not None:
            texte = str(data).strip()
            if len(texte) >= 3:
                valeurs.append({
                    'chemin': chemin,
                    'texte': texte,
                    'texte_norm': normaliser(texte)
                })
    
    parcourir(obj)
    return valeurs

def extraire_texte_word(fichier_docx):
    """Extrait tout le texte des tableaux du document Word"""
    doc = Document(fichier_docx)
    texte_complet = []
    
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                texte = cell.text.strip()
                if texte:
                    texte_complet.append(texte)
    
    # Concaténer et normaliser
    texte_word = ' '.join(texte_complet)
    return normaliser(texte_word)

def verifier_completude(fichier_json, fichier_docx):
    """Vérifie que toutes les valeurs JSON sont présentes dans le Word"""
    print("⏳ Extraction du contenu JSON...")
    valeurs_json = extraire_valeurs_json(fichier_json)
    print(f"   ✓ {len(valeurs_json)} valeurs extraites\n")
    
    print("⏳ Extraction du contenu Word...")
    texte_word = extraire_texte_word(fichier_docx)
    print(f"   ✓ {len(texte_word)} caractères extraits\n")
    
    print("⏳ Vérification de la complétude...")
    manquantes = []
    
    for val in valeurs_json:
        if val['texte_norm'] not in texte_word:
            manquantes.append(val)
    
    # Résultats
    print(f"\n{'='*100}")
    print(f"📊 RÉSULTATS DU CONTRÔLE DE COMPLÉTUDE")
    print(f"{'='*100}")
    print(f"Valeurs testées    : {len(valeurs_json)}")
    print(f"Valeurs retrouvées : {len(valeurs_json) - len(manquantes)}")
    print(f"Valeurs manquantes : {len(manquantes)}")
    print(f"Taux de complétude : {(len(valeurs_json) - len(manquantes)) / len(valeurs_json) * 100:.1f}%")
    
    if manquantes:
        print(f"\n❌ VALEURS NON RETROUVÉES (20 premières) :")
        print(f"{'-'*100}")
        for val in manquantes[:20]:
            texte_court = val['texte'][:70] + '...' if len(val['texte']) > 70 else val['texte']
            chemin_court = val['chemin'][:40] + '...' if len(val['chemin']) > 40 else val['chemin']
            print(f"  {chemin_court:<45} → {texte_court}")
    else:
        print(f"\n✅ Toutes les valeurs ont été retrouvées dans le document Word !")
    
    return len(valeurs_json), len(manquantes)

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 3:
        print("Usage: python controle_completude_json.py <fichier.json> <fichier.docx>")
        sys.exit(1)
    
    verifier_completude(sys.argv[1], sys.argv[2])
