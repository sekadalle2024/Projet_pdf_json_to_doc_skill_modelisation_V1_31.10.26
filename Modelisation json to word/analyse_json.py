#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Script d'analyse des fichiers JSON pour inventaire avant conversion"""

import json
import sys
from pathlib import Path

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
            print(f"❌ JSON invalide dans {path}")
            print(f"   Ligne {e.lineno}, colonne {e.colno} : {e.msg}")
            print(f"   Contexte : ...{text[max(0, e.pos-50):e.pos+50]}...")
            return None
        objs.append(obj)
    return objs

def analyser_structure(obj, indent="  "):
    """Analyse la structure d'un objet JSON"""
    info = []
    
    if isinstance(obj, dict):
        # Structure attendue : {"Feuille": [{"table N": [...]}, ...]}
        for feuille_nom, feuille_contenu in obj.items():
            info.append(f"{indent}Feuille : {feuille_nom}")
            
            if isinstance(feuille_contenu, list):
                tableaux = []
                for item in feuille_contenu:
                    if isinstance(item, dict) and len(item) == 1:
                        # {"table N": [...]}
                        table_nom, table_data = next(iter(item.items()))
                        if isinstance(table_data, list):
                            nb_enreg = len(table_data)
                            nb_cols = len(table_data[0]) if table_data and isinstance(table_data[0], dict) else 0
                            tableaux.append({
                                'nom': table_nom,
                                'enregistrements': nb_enreg,
                                'colonnes': nb_cols
                            })
                
                info.append(f"{indent}  Nombre de tableaux : {len(tableaux)}")
                for t in tableaux:
                    info.append(f"{indent}    - {t['nom']}: {t['enregistrements']} enreg., {t['colonnes']} colonnes")
                
                # Chercher la colonne Reference pour le nom de fichier
                ref = None
                for item in feuille_contenu:
                    if isinstance(item, dict):
                        for table_data in item.values():
                            if isinstance(table_data, list) and table_data:
                                premier = table_data[0]
                                if isinstance(premier, dict):
                                    for k, v in premier.items():
                                        if k.lower() == 'reference' and v:
                                            ref = str(v).split(' - ')[0].strip()
                                            break
                                if ref:
                                    break
                    if ref:
                        break
                
                info.append(f"{indent}  Nom de fichier prévu : {ref if ref else 'feuille_couverture_1'}.docx")
    
    return info

def main():
    fichiers = sorted(Path('.').glob('*.json'))
    
    if not fichiers:
        print("❌ Aucun fichier .json trouvé dans le dossier")
        return
    
    print(f"📊 INVENTAIRE DES FICHIERS JSON")
    print(f"{'='*100}\n")
    print(f"Nombre de fichiers trouvés : {len(fichiers)}\n")
    
    resultats = []
    
    for fichier in fichiers:
        taille_ko = fichier.stat().st_size / 1024
        print(f"⏳ Analyse de : {fichier.name} ({taille_ko:.1f} Ko)")
        
        if taille_ko > 5000:
            print(f"   ⚠️  FICHIER TRÈS VOLUMINEUX (>{taille_ko/1024:.1f} Mo)")
        
        objets = load_json_objects(fichier)
        
        if objets is None:
            resultats.append({
                'fichier': fichier.name,
                'erreur': True
            })
            continue
        
        print(f"   ✓ {len(objets)} objet(s) JSON racine")
        
        for i, obj in enumerate(objets, 1):
            print(f"\n   Objet #{i} :")
            info = analyser_structure(obj)
            for ligne in info:
                print(ligne)
        
        resultats.append({
            'fichier': fichier.name,
            'nb_objets': len(objets),
            'taille_ko': taille_ko
        })
        print()
    
    # Tableau récapitulatif
    print(f"\n{'='*100}")
    print(f"📋 TABLEAU RÉCAPITULATIF")
    print(f"{'='*100}\n")
    
    print(f"{'Fichier':<30} {'Taille (Ko)':<15} {'Objets JSON':<15} {'Statut':<20}")
    print(f"{'-'*100}")
    
    for res in resultats:
        if 'erreur' in res:
            print(f"{res['fichier']:<30} {'-':<15} {'-':<15} {'❌ ERREUR':<20}")
        else:
            print(f"{res['fichier']:<30} {res['taille_ko']:<15.1f} {res['nb_objets']:<15} {'✅ OK':<20}")
    
    print(f"\n{'='*100}")
    print(f"✓ Inventaire terminé")

if __name__ == '__main__':
    main()
