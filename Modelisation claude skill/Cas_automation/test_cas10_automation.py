# -*- coding: utf-8 -*-
"""
Test du script json2word_cas10_automation.py avec le JSON standard Cas 10
"""
import subprocess
import sys
import json
from pathlib import Path

SCRIPT = Path(__file__).parent / 'Cas_10_automation' / 'json2word_cas10_automation.py'
JSON_STD = Path(__file__).parent / 'json standard' / 'Json_standard_[Cas 10].txt'
OUTPUT_DIR = Path.home() / 'Downloads'


def test_generation():
    """Test la generation du document Cas 10."""
    print('[TEST] Generation document Cas 10...')
    print(f'Script: {SCRIPT}')
    print(f'JSON: {JSON_STD}')
    print(f'Output: {OUTPUT_DIR}')
    print()
    
    if not SCRIPT.exists():
        print(f'[ERREUR] Script introuvable: {SCRIPT}')
        return False
    
    if not JSON_STD.exists():
        print(f'[ERREUR] JSON introuvable: {JSON_STD}')
        return False
    
    # Compter les fichiers avant
    files_before = set(OUTPUT_DIR.glob('Cas10_*.docx'))
    
    # Executer le script
    result = subprocess.run(
        [sys.executable, str(SCRIPT), str(JSON_STD), str(OUTPUT_DIR)],
        capture_output=True,
        text=True,
        encoding='utf-8',
        errors='replace'
    )
    
    print('STDOUT:')
    print(result.stdout)
    
    if result.stderr:
        print('STDERR:')
        print(result.stderr)
    
    if result.returncode != 0:
        print(f'[ERREUR] Le script a retourne le code {result.returncode}')
        return False
    
    # Verifier qu'un fichier Cas10_*.docx a ete cree
    files_after = set(OUTPUT_DIR.glob('Cas10_*.docx'))
    new_files = files_after - files_before
    
    if new_files:
        latest = max(new_files, key=lambda p: p.stat().st_mtime)
        size_kb = latest.stat().st_size / 1024
        print(f'[OK] Fichier cree : {latest.name}')
        print(f'[OK] Taille : {size_kb:.1f} KB')
        
        # Verifier la taille minimale (plus souple pour Cas 10)
        if size_kb < 40:
            print(f'[AVERTISSEMENT] Fichier trop petit (< 40 KB)')
            return False
        
        return True
    else:
        print('[ERREUR] Aucun fichier Cas10_*.docx trouve dans', OUTPUT_DIR)
        return False


if __name__ == '__main__':
    print('=' * 70)
    print('TEST CAS 10 AUTOMATION')
    print('=' * 70)
    print()
    
    ok = test_generation()
    
    print()
    print('=' * 70)
    if ok:
        print('[SUCCES] Test reussi')
        print('=' * 70)
        sys.exit(0)
    else:
        print('[ECHEC] Test echoue')
        print('=' * 70)
        sys.exit(1)
