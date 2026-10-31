#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script : execute_cas2_production.py
Description : Workflow Cas 2 Production - Appel API N8N Local + Exécution Skill
              URL : http://localhost:5678/webhook/skill_manuel_audit
Auteur : Expert Python & Automation
Date : 31 octobre 2026
"""

import requests
import json
import subprocess
import sys
from pathlib import Path
from datetime import datetime

# ============================================================================
# CONFIGURATION
# ============================================================================

WEBHOOK_URL = "http://localhost:5678/webhook/skill_manuel_audit"
OUTPUT_DIR = Path("./sortie_word_production")
TEMP_DIR = Path("./temp_procedures_production")
DATA_DIR = Path("./data_json_from_n8n")
TIMEOUT = 30

# ============================================================================
# FONCTIONS UTILITAIRES
# ============================================================================

def log(message, level="INFO"):
    """Affiche un message de log avec timestamp"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    colors = {
        "INFO": "",
        "SUCCESS": "",
        "WARNING": "",
        "ERROR": ""
    }
    print(f"[{timestamp}] [{level}] {message}")

def call_n8n_api(url, method="POST", timeout=30):
    """
    Appelle le webhook N8N et retourne les données
    
    Args:
        url: URL du webhook
        method: Méthode HTTP
        timeout: Timeout en secondes
    
    Returns:
        dict: Données JSON ou None
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
        log(f"✅ Réponse reçue (Status: {response.status_code})", "SUCCESS")
        
        return response.json()
    
    except requests.exceptions.Timeout:
        log(f"❌ Timeout après {timeout}s", "ERROR")
        return None
    
    except requests.exceptions.ConnectionError:
        log("❌ Erreur de connexion - Vérifiez que N8N est démarré", "ERROR")
        return None
    
    except requests.exceptions.HTTPError as e:
        log(f"❌ Erreur HTTP : {e}", "ERROR")
        return None
    
    except json.JSONDecodeError:
        log("❌ Erreur de parsing JSON", "ERROR")
        return None
    
    except Exception as e:
        log(f"❌ Erreur inattendue : {e}", "ERROR")
        return None

def extract_data_integrale(response):
    """Extrait Data_integrale de la réponse (gère les niveaux imbriqués)"""
    log("Extraction de Data_integrale...")
    
    try:
        # Cas 1 : Réponse est une liste
        if isinstance(response, list) and len(response) > 0:
            if "Data_integrale" in response[0]:
                data = response[0]["Data_integrale"]
                
                # Vérifier si c'est un niveau imbriqué supplémentaire
                if isinstance(data, list) and len(data) > 0:
                    if isinstance(data[0], dict) and "Data_integrale" in data[0]:
                        log("Détection d'une structure imbriquée (double Data_integrale)")
                        # Extraire du niveau supplémentaire
                        data = data[0]["Data_integrale"]
                
                log(f"✅ Extraction réussie : {len(data)} procédure(s)", "SUCCESS")
                return data
        
        # Cas 2 : Réponse est un dict
        elif isinstance(response, dict):
            if "Data_integrale" in response:
                data = response["Data_integrale"]
                
                # Vérifier si c'est un niveau imbriqué supplémentaire
                if isinstance(data, list) and len(data) > 0:
                    if isinstance(data[0], dict) and "Data_integrale" in data[0]:
                        log("Détection d'une structure imbriquée (double Data_integrale)")
                        # Extraire du niveau supplémentaire
                        data = data[0]["Data_integrale"]
                
                log(f"✅ Extraction réussie : {len(data)} procédure(s)", "SUCCESS")
                return data
        
        log("❌ Structure non reconnue ou Data_integrale absent", "ERROR")
        log(f"Type reçu : {type(response)}", "ERROR")
        return None
    
    except Exception as e:
        log(f"❌ Erreur lors de l'extraction : {e}", "ERROR")
        return None

def save_full_response(data, data_dir):
    """Sauvegarde la réponse complète"""
    data_dir = Path(data_dir)
    data_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filepath = data_dir / f"response_complete_{timestamp}.json"
    
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        log(f"📁 Réponse complète sauvegardée : {filepath}")
        return filepath
    
    except Exception as e:
        log(f"Erreur de sauvegarde : {e}", "ERROR")
        return None

def process_procedures(data_integrale, output_dir, temp_dir, ref_prefix="PROD", software="Logiciel automatisé E-audit pro"):
    """
    Traite toutes les procédures avec le skill
    
    Args:
        data_integrale: Liste des procédures
        output_dir: Dossier de sortie Word
        temp_dir: Dossier temporaire JSON
        ref_prefix: Préfixe des références
        software: Nom du logiciel
    
    Returns:
        int: Nombre de conversions réussies
    """
    output_dir = Path(output_dir)
    temp_dir = Path(temp_dir)
    
    output_dir.mkdir(parents=True, exist_ok=True)
    temp_dir.mkdir(parents=True, exist_ok=True)
    
    log(f"\n{'='*60}")
    log(f"Traitement de {len(data_integrale)} procédure(s)")
    log(f"{'='*60}\n")
    
    success_count = 0
    script_dir = Path(__file__).parent
    skill_script = script_dir / "json2word_audit.py"
    
    if not skill_script.exists():
        log(f"❌ Script skill introuvable : {skill_script}", "ERROR")
        return 0
    
    for idx, procedure in enumerate(data_integrale, start=1):
        log(f"\n--- Procédure {idx}/{len(data_integrale)} ---")
        
        # Sauvegarder temporairement
        proc_file = temp_dir / f"procedure_{idx}.json"
        
        try:
            with open(proc_file, "w", encoding="utf-8") as f:
                json.dump(procedure, f, ensure_ascii=False, indent=2)
        except Exception as e:
            log(f"❌ Erreur de sauvegarde : {e}", "ERROR")
            continue
        
        # Préparer la commande avec timestamp au format V1_HH-MM-SS_DD.MM.YY
        now = datetime.now()
        timestamp = f"V1_{now.strftime('%H-%M-%S')}_{now.strftime('%d.%m.%y')}"
        ref = f"{ref_prefix}{idx:03d}_{timestamp}"
        cmd = [
            "python",
            str(skill_script),
            str(proc_file),
            "-o", str(output_dir),
            "--ref", ref,
            "--software", software
        ]
        
        # Exécuter le skill
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=120,
                encoding='utf-8',
                errors='replace'
            )
            
            if result.returncode == 0:
                log(f"✅ Procédure {idx} convertie avec succès", "SUCCESS")
                success_count += 1
                if result.stdout:
                    # Afficher seulement le nom du fichier généré
                    for line in result.stdout.split("\n"):
                        if "Fichier généré" in line or ".docx" in line:
                            print(f"    {line.strip()}")
            else:
                log(f"❌ Échec de la conversion de la procédure {idx}", "ERROR")
                if result.stderr:
                    # Afficher l'erreur complète pour debug
                    print(f"    Return code: {result.returncode}")
                    print(f"    Stdout: {result.stdout[:300]}")
                    print(f"    Stderr: {result.stderr[:500]}")
        
        except subprocess.TimeoutExpired:
            log(f"❌ Timeout pour la procédure {idx}", "ERROR")
        
        except Exception as e:
            log(f"❌ Erreur d'exécution : {e}", "ERROR")
    
    return success_count

# ============================================================================
# FONCTION PRINCIPALE
# ============================================================================

def main():
    """Fonction principale du workflow Cas 2 Production"""
    
    # Forcer l'encodage UTF-8 pour la console Windows
    import sys
    if sys.platform == 'win32':
        try:
            sys.stdout.reconfigure(encoding='utf-8')
            sys.stderr.reconfigure(encoding='utf-8')
        except:
            pass
    
    print("\n" + "="*70)
    print("  🚀 WORKFLOW CAS 2 - PRODUCTION")
    print("  📡 N8N Local : http://localhost:5678")
    print("="*70 + "\n")
    
    start_time = datetime.now()
    
    log(f"Webhook URL : {WEBHOOK_URL}")
    log(f"Dossier de sortie : {OUTPUT_DIR.resolve()}")
    
    # ========================================================================
    # ÉTAPE 1 : Appel API N8N
    # ========================================================================
    
    print("\n" + "="*60)
    print("  ÉTAPE 1 - Appel API N8N et Collecte de Data_integrale")
    print("="*60 + "\n")
    
    response = call_n8n_api(WEBHOOK_URL, method="POST", timeout=TIMEOUT)
    
    if response is None:
        log("❌ Impossible de récupérer les données depuis N8N", "ERROR")
        log("Vérifiez que N8N est démarré et que le workflow est actif", "ERROR")
        return 1
    
    # Sauvegarder la réponse complète
    save_full_response(response, DATA_DIR)
    
    # Extraire Data_integrale
    data_integrale = extract_data_integrale(response)
    
    if data_integrale is None or len(data_integrale) == 0:
        log("❌ Aucune procédure trouvée dans Data_integrale", "ERROR")
        return 1
    
    # ========================================================================
    # ÉTAPE 2 : Exécution du Skill
    # ========================================================================
    
    print("\n" + "="*60)
    print("  ÉTAPE 2 - Exécution du Skill audit-procedures-json2word")
    print("="*60 + "\n")
    
    success_count = process_procedures(
        data_integrale=data_integrale,
        output_dir=OUTPUT_DIR,
        temp_dir=TEMP_DIR,
        ref_prefix="PROD",
        software="Logiciel automatisé E-audit pro"
    )
    
    # ========================================================================
    # RÉSUMÉ FINAL
    # ========================================================================
    
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    
    print("\n" + "="*70)
    print("  📊 RÉSUMÉ FINAL")
    print("="*70)
    print(f"\n  • Procédures collectées    : {len(data_integrale)}")
    print(f"  • Conversions réussies     : {success_count}")
    print(f"  • Conversions échouées     : {len(data_integrale) - success_count}")
    print(f"  • Dossier de sortie        : {OUTPUT_DIR.resolve()}")
    print(f"  • Durée totale             : {duration:.1f} secondes")
    print(f"  • Timestamp                : {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("\n" + "="*70 + "\n")
    
    if success_count == len(data_integrale):
        log("✅ Toutes les conversions ont réussi !", "SUCCESS")
        
        # Lister les fichiers générés
        word_files = sorted(OUTPUT_DIR.glob("*.docx"))
        if word_files:
            print("\n📄 Documents Word générés :")
            for doc in word_files:
                print(f"  • {doc.name}")
        
        return 0
    
    elif success_count > 0:
        log("⚠️ Certaines conversions ont échoué", "WARNING")
        return 1
    
    else:
        log("❌ Aucune conversion n'a réussi", "ERROR")
        return 1

# ============================================================================
# POINT D'ENTRÉE
# ============================================================================

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n⚠️ Workflow interrompu par l'utilisateur")
        sys.exit(130)
    except Exception as e:
        print(f"\n❌ Erreur fatale : {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
