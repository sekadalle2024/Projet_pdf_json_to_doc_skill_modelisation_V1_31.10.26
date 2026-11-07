#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
json2word_feuilles_revision_v2.py - Cas 6 (version 2)
Convertit les données de "Feuille de révision" en document Word
en utilisant le convertisseur Cas 2 (qui fonctionne bien)

Version 2: Wrapper autour de json2word_audit.py (Cas 2)
"""

import json
import sys
import tempfile
from pathlib import Path
from datetime import datetime
import argparse

# Import du convertisseur générique avec charte E-audit pro
# Utilise directement le script de référence du Cas 2
CAS2_DIR = Path(__file__).parent.parent / "Cas_2"
sys.path.insert(0, str(CAS2_DIR))

try:
    from json2word_audit import convert
except ImportError as e:
    print(f"❌ Erreur d'import: {e}", file=sys.stderr)
    print(f"   Chemin recherché: {CAS2_DIR}", file=sys.stderr)
    sys.exit(1)


def main():
    """Point d'entrée principal avec arguments CLI."""
    parser = argparse.ArgumentParser(
        description="Convertit un JSON de feuilles de révision en document Word (.docx)"
    )
    parser.add_argument("json_file", help="Chemin vers le fichier JSON d'entrée")
    parser.add_argument("-o", "--out-dir", default=".", help="Dossier de sortie")
    parser.add_argument("--software", default="Logiciel automatisé E-audit pro 2.0", 
                       help="Nom du logiciel")
    parser.add_argument("--footer", 
                       default="Automatisez vos activités d'audit, risques et contrôles - Whatsapp : + 225 05 44 13 07 98",
                       help="Texte du pied de page")
    parser.add_argument("--no-blank-rows", action="store_true", 
                       help="Ne pas ajouter de lignes vides entre les rangées")
    
    args = parser.parse_args()
    
    json_path = Path(args.json_file)
    if not json_path.exists():
        print(f"❌ Erreur : Le fichier {json_path} n'existe pas.")
        return False
    
    # Charger le JSON
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            raw_data = json.load(f)
    except Exception as e:
        print(f"❌ Erreur lecture JSON : {e}", file=sys.stderr)
        return False
    
    # Extraire les données réelles
    # Structure attendue: {"Etape mission - Feuille revision": [...]}
    data = raw_data
    if isinstance(raw_data, dict):
        # Si c'est un dict avec une clé "Etape mission", extraire
        for key in raw_data.keys():
            if "Etape mission" in key or "Feuille revision" in key:
                data = raw_data[key]
                break
    
    # Déterminer le dossier de sortie
    out_path = Path(args.out_dir)
    out_path.mkdir(parents=True, exist_ok=True)
    
    # Créer un fichier temporaire avec juste les données au bon format
    temp_json = None
    try:
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8') as tmp:
            # Le convertisseur Cas 2 attend un dict ou une liste
            json.dump(data, tmp, ensure_ascii=False, indent=2)
            temp_json = Path(tmp.name)
        
        # Extraire une référence si possible
        reference = None
        if isinstance(data, list) and data:
            for item in data:
                if isinstance(item, dict):
                    for key, value in item.items():
                        if "table 1" in key.lower() and isinstance(value, (list, dict)):
                            table1_data = value[0] if isinstance(value, list) else value
                            if isinstance(table1_data, dict):
                                reference = table1_data.get("Reference") or table1_data.get("Test")
                                if reference:
                                    reference = str(reference).strip()[:30]
                                    break
                if reference:
                    break
        
        # Générer une référence temporelle si absente
        if not reference:
            timestamp = datetime.now().strftime("%H-%M-%S_%d.%m.%y")
            reference = f"FREV001_V1_{timestamp}"
        
        # Appeler le convertisseur Cas 2 avec la charte E-audit pro
        out_file = convert(
            json_path=temp_json,
            out_dir=out_path,
            software=args.software,
            reference=reference,
            footer=args.footer,
            blank_rows=not args.no_blank_rows,
            strip_steps=False
        )
        
        # Affichage du résultat
        print(f"✅ Document généré : {out_file}")
        return True
        
    except Exception as e:
        print(f"❌ Erreur conversion : {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return False
    
    finally:
        # Nettoyer le fichier temporaire
        if temp_json and temp_json.exists():
            temp_json.unlink()


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
