#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script : execute_cas2_workflow.py
Description : Exécute le workflow complet du Cas 2 :
              1. Appel API vers N8N
              2. Collecte de Data_integrale
              3. Exécution du skill audit-procedures-json2word
Auteur : Expert Python & Automation
Date : 31 octobre 2026
"""

import subprocess
import sys
import json
from pathlib import Path
from datetime import datetime

def log(message, level="INFO"):
    """Affiche un message de log avec timestamp"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] [{level}] {message}")

def execute_step(title, command, cwd=None):
    """
    Exécute une étape du workflow
    
    Args:
        title: Titre de l'étape
        command: Commande à exécuter (liste)
        cwd: Dossier de travail
    
    Returns:
        tuple: (success, output)
    """
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60 + "\n")
    
    log(f"Commande : {' '.join(command)}")
    
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            cwd=cwd,
            timeout=300
        )
        
        # Afficher la sortie
        if result.stdout:
            print(result.stdout)
        
        if result.returncode == 0:
            log(f"✅ {title} - Succès", "SUCCESS")
            return True, result.stdout
        else:
            log(f"❌ {title} - Échec", "ERROR")
            if result.stderr:
                print(result.stderr)
            return False, result.stderr
    
    except subprocess.TimeoutExpired:
        log(f"❌ {title} - Timeout (> 5 min)", "ERROR")
        return False, "Timeout"
    
    except Exception as e:
        log(f"❌ {title} - Erreur : {e}", "ERROR")
        return False, str(e)

def extract_json_filepath(output):
    """
    Extrait le chemin du fichier JSON depuis la sortie
    
    Args:
        output: Sortie du script api_call_n8n.py
    
    Returns:
        str: Chemin du fichier JSON ou None
    """
    # Chercher la ligne "📁 Fichier JSON : ..."
    for line in output.split("\n"):
        if "📁 Fichier JSON :" in line or "Fichier JSON créé :" in line:
            parts = line.split(":")
            if len(parts) >= 2:
                filepath = ":".join(parts[1:]).strip()
                return filepath
    
    # Chercher dans data_json_from_n8n
    data_dir = Path("./data_json_from_n8n")
    if data_dir.exists():
        json_files = sorted(data_dir.glob("data_integrale_*.json"))
        if json_files:
            return str(json_files[-1])
    
    return None

def count_procedures(json_filepath):
    """
    Compte le nombre de procédures dans le fichier JSON
    
    Args:
        json_filepath: Chemin du fichier JSON
    
    Returns:
        int: Nombre de procédures
    """
    try:
        with open(json_filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        if isinstance(data, list):
            return len(data)
        return 0
    
    except Exception as e:
        log(f"Erreur lors du comptage : {e}", "ERROR")
        return 0

def main():
    """Fonction principale du workflow Cas 2"""
    
    print("\n" + "="*70)
    print("  🚀 WORKFLOW CAS 2 - Appel API N8N + Exécution Skill")
    print("="*70 + "\n")
    
    start_time = datetime.now()
    
    # Configuration
    WEBHOOK_URL = "http://localhost:5678/webhook/skill_manuel_audit"
    SCRIPT_DIR = Path(__file__).parent
    API_SCRIPT = SCRIPT_DIR / "api_call_n8n.py"
    SKILL_SCRIPT = SCRIPT_DIR / "json2word_audit.py"
    OUTPUT_DIR = SCRIPT_DIR / "sortie_word_cas2"
    
    log(f"Webhook N8N : {WEBHOOK_URL}")
    
    # Vérifier que les scripts existent
    if not API_SCRIPT.exists():
        log(f"Script API introuvable : {API_SCRIPT}", "ERROR")
        sys.exit(1)
    
    if not SKILL_SCRIPT.exists():
        log(f"Script skill introuvable : {SKILL_SCRIPT}", "ERROR")
        sys.exit(1)
    
    log(f"Script API : {API_SCRIPT}")
    log(f"Script Skill : {SKILL_SCRIPT}")
    log(f"Dossier de sortie : {OUTPUT_DIR}")
    
    # ========================================================================
    # ÉTAPE 1 : Appel API vers N8N et collecte de Data_integrale
    # ========================================================================
    
    success, output = execute_step(
        title="ÉTAPE 1 - Appel API N8N et Collecte de Data_integrale",
        command=["python", str(API_SCRIPT)],
        cwd=str(SCRIPT_DIR)
    )
    
    if not success:
        log("Échec de l'étape 1 : Appel API N8N", "ERROR")
        sys.exit(1)
    
    # Extraire le chemin du fichier JSON créé
    json_filepath = extract_json_filepath(output)
    
    if not json_filepath or not Path(json_filepath).exists():
        log("Impossible de trouver le fichier JSON créé", "ERROR")
        sys.exit(1)
    
    log(f"Fichier JSON collecté : {json_filepath}", "SUCCESS")
    
    # Compter les procédures
    nb_procedures = count_procedures(json_filepath)
    log(f"Nombre de procédures à traiter : {nb_procedures}")
    
    if nb_procedures == 0:
        log("Aucune procédure à traiter", "ERROR")
        sys.exit(1)
    
    # ========================================================================
    # ÉTAPE 2 : Exécution du skill audit-procedures-json2word
    # ========================================================================
    
    # Créer le dossier de sortie
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # Préparer la commande
    skill_command = [
        "python",
        str(SKILL_SCRIPT),
        json_filepath,
        "-o", str(OUTPUT_DIR),
        "--ref", "CAS2",
        "--software", "E-Procedure Automation N8N"
    ]
    
    success, output = execute_step(
        title="ÉTAPE 2 - Exécution du Skill audit-procedures-json2word",
        command=skill_command,
        cwd=str(SCRIPT_DIR)
    )
    
    if not success:
        log("Échec de l'étape 2 : Exécution du skill", "ERROR")
        sys.exit(1)
    
    # ========================================================================
    # RÉSUMÉ FINAL
    # ========================================================================
    
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    
    print("\n" + "="*70)
    print("  ✅ WORKFLOW CAS 2 TERMINÉ AVEC SUCCÈS")
    print("="*70)
    print(f"\n📊 Statistiques :")
    print(f"  • Procédures collectées : {nb_procedures}")
    print(f"  • Fichier JSON source   : {json_filepath}")
    print(f"  • Documents Word générés : {OUTPUT_DIR}")
    print(f"  • Durée totale          : {duration:.1f} secondes")
    print(f"  • Timestamp             : {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("\n" + "="*70 + "\n")
    
    log("🎉 Workflow Cas 2 terminé avec succès !", "SUCCESS")
    
    # Proposer d'ouvrir le dossier de sortie
    print(f"\n📁 Les documents Word sont dans : {OUTPUT_DIR.resolve()}")
    
    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n⚠️  Workflow interrompu par l'utilisateur")
        sys.exit(130)
    except Exception as e:
        log(f"Erreur fatale : {e}", "ERROR")
        import traceback
        traceback.print_exc()
        sys.exit(1)
