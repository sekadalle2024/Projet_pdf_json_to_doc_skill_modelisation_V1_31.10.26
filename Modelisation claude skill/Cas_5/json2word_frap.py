#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
json2word_frap.py - Cas 5
Convertit les données FRAP en document Word
avec la charte graphique E-audit pro (bordeaux #7B1E3A)
"""

import json
import sys
import tempfile
from pathlib import Path
from datetime import datetime

# Import du convertisseur générique avec charte E-audit pro
CAS2_DIR = Path(__file__).parent.parent / "Cas_2"
sys.path.insert(0, str(CAS2_DIR))

try:
    from json2word_audit import convert
except ImportError as e:
    print(f"❌ Erreur d'import: {e}", file=sys.stderr)
    print(f"   Chemin recherché: {CAS2_DIR}", file=sys.stderr)
    sys.exit(1)


def main(json_file: str, output_dir: str = None):
    """
    Convertit un fichier JSON FRAP en document Word.
    
    Args:
        json_file: Chemin vers le fichier JSON
        output_dir: Dossier de sortie (optionnel, par défaut ./sortie_word_cas5)
    """
    json_path = Path(json_file)
    
    if not json_path.exists():
        print(f"❌ Fichier introuvable : {json_path}", file=sys.stderr)
        return False
    
    # Charger le JSON pour extraction de métadonnées
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            raw_data = json.load(f)
    except Exception as e:
        print(f"❌ Erreur lecture JSON : {e}", file=sys.stderr)
        return False
    
    # Extraire les données réelles depuis la structure du webhook
    data = raw_data
    if isinstance(raw_data, dict) and "data" in raw_data:
        data = raw_data["data"]
    
    # Déterminer le dossier de sortie
    if output_dir:
        out_path = Path(output_dir)
    else:
        out_path = Path(__file__).parent / "sortie_word_cas5"
    
    # Créer un fichier temporaire avec juste les données mission
    temp_json = None
    try:
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8') as tmp:
            json.dump(data, tmp, ensure_ascii=False, indent=2)
            temp_json = Path(tmp.name)
    
        # Extraire les métadonnées pour le nom de fichier
        reference = None
        for key, value in data.items():
            if isinstance(value, list) and value:
                for item in value:
                    if isinstance(item, dict) and "table 1" in item:
                        table1 = item["table 1"]
                        for k in ["Reference", "Référence", "Code", "Numero", "N° FRAP"]:
                            if k in table1:
                                ref_value = table1[k]
                                if isinstance(ref_value, str):
                                    reference = ref_value.strip()
                                    break
                        if reference:
                            break
                if reference:
                    break
        
        # Générer une référence temporelle si absente
        if not reference:
            timestamp = datetime.now().strftime("%H-%M-%S_%d.%m.%y")
            reference = f"FRAP001_V1_{timestamp}"
        
        # Appeler le convertisseur avec la charte E-audit pro
        # blank_rows=False pour Cas 5 (pas de lignes vides entre les rangées)
        out_file = convert(
            json_path=temp_json,
            out_dir=out_path,
            software="Logiciel automatisé E-audit pro",
            reference=reference,
            footer="Automatisez vos activités d'audit, risques et contrôles - Whatsapp : + 225 05 44 13 07 98",
            blank_rows=False,
            strip_steps=False
        )
        print(f"✅ Document créé : {out_file}")
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
    if len(sys.argv) < 2:
        print("Usage: python json2word_frap.py <fichier.json> [dossier_sortie]")
        sys.exit(1)
    
    json_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else None
    
    success = main(json_path, output_dir)
    sys.exit(0 if success else 1)
