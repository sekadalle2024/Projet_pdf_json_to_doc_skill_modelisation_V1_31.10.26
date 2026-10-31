#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Script d'inventaire des fichiers Excel pour conversion Word"""

import openpyxl
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

def analyser_fichier(fichier_path):
    """Analyse un fichier Excel et retourne ses caractéristiques"""
    try:
        wb = openpyxl.load_workbook(fichier_path, data_only=True)
        
        resultats = {
            'fichier': fichier_path.name,
            'nb_onglets': len(wb.worksheets),
            'onglets': [],
            'mode_global': 'generic'
        }
        
        for ws in wb.worksheets:
            # Détecter mode cartographie
            mode = 'generic'
            for row_idx in range(1, min(100, ws.max_row + 1)):
                cell_val = ws.cell(row_idx, 1).value
                if cell_val and isinstance(cell_val, str) and 'PROCESSUS /' in cell_val:
                    mode = 'cartographie'
                    resultats['mode_global'] = 'cartographie'
                    break
            
            # Compter lignes non vides
            lignes_non_vides = 0
            for row_idx in range(1, min(ws.max_row + 1, 1000)):
                row_vals = [ws.cell(row_idx, c).value for c in range(1, min(ws.max_column + 1, 20))]
                if any(v for v in row_vals):
                    lignes_non_vides += 1
            
            onglet_info = {
                'nom': ws.title,
                'dimensions': ws.dimensions,
                'max_row': ws.max_row,
                'max_col': ws.max_column,
                'cellules_fusionnees': len(ws.merged_cells.ranges),
                'lignes_non_vides': lignes_non_vides,
                'mode': mode
            }
            
            resultats['onglets'].append(onglet_info)
        
        wb.close()
        return resultats
        
    except Exception as e:
        return {
            'fichier': fichier_path.name,
            'erreur': str(e)
        }

def main():
    dossier = Path('.')
    fichiers = sorted([f for f in dossier.glob('*.xlsx') if not f.name.startswith('~$')])
    
    print(f"📊 INVENTAIRE DES FICHIERS EXCEL")
    print(f"{'='*100}\n")
    print(f"Nombre de fichiers trouvés : {len(fichiers)}\n")
    
    tous_resultats = []
    
    for fichier in fichiers:
        print(f"⏳ Analyse de : {fichier.name}")
        resultats = analyser_fichier(fichier)
        tous_resultats.append(resultats)
        
        if 'erreur' in resultats:
            print(f"   ❌ ERREUR : {resultats['erreur']}\n")
        else:
            print(f"   ✓ {resultats['nb_onglets']} onglet(s), mode : {resultats['mode_global']}")
            for ong in resultats['onglets']:
                print(f"     - {ong['nom']}: {ong['lignes_non_vides']} lignes, "
                      f"{ong['cellules_fusionnees']} fusions, mode {ong['mode']}")
            print()
    
    # Tableau récapitulatif
    print(f"\n{'='*100}")
    print(f"📋 TABLEAU RÉCAPITULATIF")
    print(f"{'='*100}\n")
    
    print(f"{'Fichier':<50} {'Onglets':<10} {'Mode':<15} {'Lignes total':<15}")
    print(f"{'-'*100}")
    
    for res in tous_resultats:
        if 'erreur' not in res:
            lignes_total = sum(o['lignes_non_vides'] for o in res['onglets'])
            fichier_court = res['fichier'][:47] + '...' if len(res['fichier']) > 50 else res['fichier']
            print(f"{fichier_court:<50} {res['nb_onglets']:<10} {res['mode_global']:<15} {lignes_total:<15}")
        else:
            print(f"{res['fichier']:<50} {'ERREUR':<10}")
    
    print(f"\n{'='*100}")
    print(f"✓ Inventaire terminé")

if __name__ == '__main__':
    main()
