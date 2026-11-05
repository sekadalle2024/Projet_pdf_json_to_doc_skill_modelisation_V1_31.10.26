#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script : json2word_feuille_couverture.py
Description : Conversion JSON → Word pour Feuilles de couverture
              Utilise la charte graphique E-audit pro (rouge bordeaux #7B1E3A)
              Basé sur le script Cas 2 (json2word_audit.py)
Auteur : Expert Python & Automation
Date : 5 novembre 2026
Version : 2.0.0

RÉFÉRENCE TEMPLATE :
    exemple_template_design/A210 - Feuille couverture- Logiciel automatisé E-Contrôle interne bancaire.docx
"""

import json
import sys
from pathlib import Path

# Importer le script Cas 2 qui a la bonne charte graphique
sys.path.insert(0, str(Path(__file__).parent.parent / "Cas_2"))
from json2word_audit import main as cas2_main

def main(json_path, output_dir=None):
    """
    Fonction principale - Utilise le script Cas 2 avec la charte E-audit pro
    """
    
    # Lire le JSON
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Extraire les données si elles sont imbriquées
    if "data" in data and isinstance(data["data"], dict):
        for key, value in data["data"].items():
            if isinstance(value, list) and len(value) >= 2:
                if "table 1" in value[0]:
                    data["table 1"] = value[0]["table 1"]
                if "table 2" in value[1]:
                    table2 = value[1]["table 2"]
                    data["table 2"] = table2 if isinstance(table2, list) else table2.get("rows", [])
                break
    
    # Sauvegarder dans un fichier temporaire au bon format
    temp_json = Path(json_path).parent / "temp_formatted.json"
    with open(temp_json, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    # Appeler le script Cas 2
    if output_dir is None:
        output_dir = Path(__file__).parent / "sortie_word_cas7"
    
    try:
        result = cas2_main(str(temp_json), str(output_dir))
        print(f"✅ Document créé : {output_dir}")
        return True
    finally:
        if temp_json.exists():
            temp_json.unlink()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python json2word_feuille_couverture.py <fichier.json> [dossier_sortie]")
        sys.exit(1)
    
    json_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else None
    
    main(json_path, output_dir)
