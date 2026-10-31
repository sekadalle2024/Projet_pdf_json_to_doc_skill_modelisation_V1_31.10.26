#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script : api_call_n8n.py
Description : Appel API vers le webhook N8N et sauvegarde des données JSON
Auteur : Expert Python & Automation
Date : 31 octobre 2026
"""

import requests
import json
import sys
from pathlib import Path
from datetime import datetime

# Configuration
WEBHOOK_URL = "http://localhost:5678/webhook/skill_manuel_audit"
OUTPUT_DIR = Path("./data_json_from_n8n")
TIMEOUT = 30

def log(message, level="INFO"):
    """Affiche un message de log avec timestamp"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] [{level}] {message}")

def call_n8n_webhook(url, method="POST", timeout=30):
    """
    Appelle le webhook N8N et retourne les données JSON
    
    Args:
        url: URL du webhook N8N
        method: Méthode HTTP (GET ou POST)
        timeout: Timeout en secondes
    
    Returns:
        dict: Données JSON de la réponse
    """
    log(f"Appel API vers {url}")
    log(f"Méthode : {method}")
    
    try:
        if method.upper() == "GET":
            response = requests.get(url, timeout=timeout)
        else:
            response = requests.post(
                url,
                json={},
                headers={"Content-Type": "application/json"},
                timeout=timeout
            )
        
        response.raise_for_status()
        log(f"Réponse reçue (Status: {response.status_code})", "SUCCESS")
        
        data = response.json()
        return data
    
    except requests.exceptions.Timeout:
        log(f"Timeout après {timeout}s", "ERROR")
        return None
    
    except requests.exceptions.ConnectionError:
        log("Erreur de connexion", "ERROR")
        return None
    
    except requests.exceptions.HTTPError as e:
        log(f"Erreur HTTP : {e}", "ERROR")
        return None
    
    except json.JSONDecodeError:
        log("Erreur de parsing JSON", "ERROR")
        return None
    
    except Exception as e:
        log(f"Erreur inattendue : {e}", "ERROR")
        return None

def extract_data_integrale(response):
    """
    Extrait le champ Data_integrale de la réponse
    
    Args:
        response: Réponse de l'API (liste ou dict)
    
    Returns:
        list: Liste des procédures ou None
    """
    log("Extraction de Data_integrale")
    
    try:
        # Cas 1 : Réponse est une liste
        if isinstance(response, list) and len(response) > 0:
            if "Data_integrale" in response[0]:
                data = response[0]["Data_integrale"]
                log(f"Extraction réussie : {len(data)} procédure(s)", "SUCCESS")
                return data
        
        # Cas 2 : Réponse est un dict
        elif isinstance(response, dict):
            if "Data_integrale" in response:
                data = response["Data_integrale"]
                log(f"Extraction réussie : {len(data)} procédure(s)", "SUCCESS")
                return data
        
        log("Structure non reconnue ou Data_integrale absent", "ERROR")
        return None
    
    except Exception as e:
        log(f"Erreur lors de l'extraction : {e}", "ERROR")
        return None

def save_data_integrale(data, output_dir):
    """
    Sauvegarde Data_integrale dans un fichier JSON
    
    Args:
        data: Données à sauvegarder
        output_dir: Dossier de sortie
    
    Returns:
        Path: Chemin du fichier créé ou None
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"data_integrale_{timestamp}.json"
    filepath = output_dir / filename
    
    log(f"Sauvegarde dans {filepath}")
    
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        log(f"Fichier créé : {filepath}", "SUCCESS")
        return filepath
    
    except Exception as e:
        log(f"Erreur lors de la sauvegarde : {e}", "ERROR")
        return None

def main():
    """Fonction principale"""
    print("\n" + "="*60)
    print("  Script d'Appel API N8N - Collecte de Data_integrale")
    print("="*60 + "\n")
    
    # Demander l'URL du webhook si besoin
    url = input(f"URL du webhook N8N [{WEBHOOK_URL}] : ").strip()
    if not url:
        url = WEBHOOK_URL
    
    # 1. Appeler le webhook
    response = call_n8n_webhook(url, method="POST", timeout=TIMEOUT)
    
    if response is None:
        log("Impossible de récupérer les données", "ERROR")
        sys.exit(1)
    
    # 2. Extraire Data_integrale
    data_integrale = extract_data_integrale(response)
    
    if data_integrale is None or len(data_integrale) == 0:
        log("Aucune procédure trouvée", "ERROR")
        sys.exit(1)
    
    # 3. Sauvegarder les données
    filepath = save_data_integrale(data_integrale, OUTPUT_DIR)
    
    if filepath is None:
        log("Échec de la sauvegarde", "ERROR")
        sys.exit(1)
    
    # 4. Résumé
    print("\n" + "="*60)
    print("  RÉSUMÉ")
    print("="*60)
    log(f"Procédures collectées : {len(data_integrale)}")
    log(f"Fichier JSON créé : {filepath}")
    log(f"Dossier de sortie : {OUTPUT_DIR.resolve()}")
    print("="*60 + "\n")
    
    log("✅ Collecte terminée avec succès", "SUCCESS")
    
    # Retourner le chemin du fichier pour utilisation ultérieure
    print(f"\n📁 Fichier JSON : {filepath}")
    return str(filepath)

if __name__ == "__main__":
    main()
