#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script : execute_cas5_production.py
Description : Orchestrateur Production Cas 5 - FRAP et Recommandations
Auteur : Expert Python & Automation
Date : 5 novembre 2026
"""

import requests
import json
import sys
import subprocess
from pathlib import Path
from datetime import datetime

# Configuration
WEBHOOK_URL = "http://localhost:5678/webhook/skill_frap_recos_cas5"
OUTPUT_DIR = Path(__file__).parent / "sortie_word_cas5"
SCRIPT_PATH = Path(__file__).parent / "json2word_frap_recos.py"
TIMEOUT = 30

def log(message, level="INFO"):
    """Log avec timestamp"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] [{level}] {message}")

def call_n8n_webhook():
    """Appelle le webhook N8N"""
    log(f"Appel webhook : {WEBHOOK_URL}")
    
    try:
        response = requests.post(
            WEBHOOK_URL,
            json={},
            headers={"Content-Type": "application/json"},
            timeout=TIMEOUT
        )
        response.raise_for_status()
        log("✅ Données récupérées", "SUCCESS")
        return response.json()
    
    except Exception as e:
        log(f"❌ Erreur : {e}", "ERROR")
        return None

def extract_data_integrale(response):
    """Extrait Data_integrale"""
    if isinstance(response, list) and len(response) > 0:
        if "Data_integrale" in response[0]:
            return response[0]["Data_integrale"]
    
    if isinstance(response, dict) and "Data_integrale" in response:
        return response["Data_integrale"]
    
    return None

def process_frap(data_item, index):
    """Traite un élément FRAP"""
    log(f"Traitement élément {index + 1}")
    
    # Créer fichier JSON temporaire
    temp_json = OUTPUT_DIR / f"temp_frap_{index}.json"
    with open(temp_json, 'w', encoding='utf-8') as f:
        json.dump(data_item, f, ensure_ascii=False, indent=2)
    
    # Appeler le script de conversion
    result = subprocess.run(
        [sys.executable, str(SCRIPT_PATH), str(temp_json), str(OUTPUT_DIR)],
        capture_output=True,
        text=True
    )
    
    # Supprimer le fichier temporaire
    temp_json.unlink(missing_ok=True)
    
    if result.returncode == 0:
        log(f"✅ Document {index + 1} créé", "SUCCESS")
        return True
    else:
        log(f"❌ Erreur document {index + 1}: {result.stderr}", "ERROR")
        return False

def main():
    """Fonction principale"""
    print("\n" + "=" * 80)
    print("  CAS 5 - FRAP ET RECOMMANDATIONS - PRODUCTION")
    print("=" * 80 + "\n")
    
    # Créer dossier de sortie
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # Étape 1 : Appel N8N
    log("Étape 1 : Appel du webhook N8N")
    response = call_n8n_webhook()
    
    if not response:
        log("❌ Impossible de récupérer les données", "ERROR")
        sys.exit(1)
    
    # Étape 2 : Extraction
    log("Étape 2 : Extraction Data_integrale")
    data = extract_data_integrale(response)
    
    if not data or len(data) == 0:
        log("❌ Aucune donnée trouvée", "ERROR")
        sys.exit(1)
    
    log(f"✅ {len(data)} élément(s) trouvé(s)", "SUCCESS")
    
    # Étape 3 : Traitement
    log("Étape 3 : Génération des documents")
    
    success_count = 0
    for i, item in enumerate(data):
        if process_frap(item, i):
            success_count += 1
    
    # Résumé
    print("\n" + "=" * 80)
    print("  RÉSUMÉ")
    print("=" * 80)
    log(f"Documents créés : {success_count}/{len(data)}")
    log(f"Dossier de sortie : {OUTPUT_DIR.resolve()}")
    print("=" * 80 + "\n")
    
    if success_count == len(data):
        log("✅ Production terminée avec succès", "SUCCESS")
        sys.exit(0)
    else:
        log("⚠️  Production terminée avec des erreurs", "WARNING")
        sys.exit(1)

if __name__ == "__main__":
    main()
