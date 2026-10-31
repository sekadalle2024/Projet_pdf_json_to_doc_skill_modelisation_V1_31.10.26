#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script : execute_workflow_simulation.py
Description : Exécute le workflow Cas 2 complet en mode simulation
Auteur : Expert Python & Automation
Date : 31 octobre 2026
"""

import json
import subprocess
import sys
from pathlib import Path
from datetime import datetime

def log(message, level="INFO"):
    """Affiche un message de log"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] [{level}] {message}")

def main():
    print("\n" + "="*70)
    print("  🚀 WORKFLOW CAS 2 - Mode Simulation Complete")
    print("="*70 + "\n")
    
    # Chemins
    script_dir = Path(__file__).parent
    json_file = script_dir / "data_json_from_n8n" / "data_integrale_simulation.json"
    output_dir = script_dir / "sortie_word_test"
    temp_dir = script_dir / "temp_procedures"
    
    # Créer les dossiers
    output_dir.mkdir(parents=True, exist_ok=True)
    temp_dir.mkdir(parents=True, exist_ok=True)
    
    # 1. Charger les données
    log(f"Chargement des données depuis {json_file}")
    
    try:
        with open(json_file, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        log(f"Erreur de chargement : {e}", "ERROR")
        return 1
    
    # 2. Extraire Data_integrale
    if isinstance(data, list) and len(data) > 0:
        data_integrale = data[0].get("Data_integrale", [])
    elif isinstance(data, dict):
        data_integrale = data.get("Data_integrale", [])
    else:
        log("Structure JSON non reconnue", "ERROR")
        return 1
    
    log(f"Nombre de procédures trouvées : {len(data_integrale)}", "SUCCESS")
    
    # 3. Traiter chaque procédure
    success_count = 0
    
    for idx, procedure in enumerate(data_integrale, start=1):
        log(f"\n{'='*60}")
        log(f"Traitement de la procédure {idx}/{len(data_integrale)}")
        log(f"{'='*60}")
        
        # Sauvegarder la procédure individuellement
        proc_file = temp_dir / f"procedure_{idx}.json"
        
        try:
            with open(proc_file, "w", encoding="utf-8") as f:
                json.dump(procedure, f, ensure_ascii=False, indent=2)
            
            log(f"Fichier temporaire créé : {proc_file}")
        
        except Exception as e:
            log(f"Erreur de sauvegarde : {e}", "ERROR")
            continue
        
        # Exécuter le skill
        ref = f"TEST{idx:03d}"
        cmd = [
            "python",
            str(script_dir / "json2word_audit.py"),
            str(proc_file),
            "-o", str(output_dir),
            "--ref", ref,
            "--software", "Simulation Test N8N Workflow Cas 2"
        ]
        
        log(f"Commande : {' '.join(cmd)}")
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode == 0:
                log(f"Procédure {idx} convertie avec succès", "SUCCESS")
                success_count += 1
                if result.stdout:
                    print(result.stdout)
            else:
                log(f"Échec de la conversion de la procédure {idx}", "ERROR")
                if result.stderr:
                    print(result.stderr)
        
        except subprocess.TimeoutExpired:
            log(f"Timeout pour la procédure {idx}", "ERROR")
        
        except Exception as e:
            log(f"Erreur lors de l'exécution : {e}", "ERROR")
    
    # 4. Résumé final
    print("\n" + "="*70)
    print("  RÉSUMÉ FINAL")
    print("="*70)
    log(f"Procédures traitées : {len(data_integrale)}")
    log(f"Conversions réussies : {success_count}")
    log(f"Conversions échouées : {len(data_integrale) - success_count}")
    log(f"Dossier de sortie : {output_dir.resolve()}")
    print("="*70 + "\n")
    
    if success_count == len(data_integrale):
        log("✅ Toutes les conversions ont réussi !", "SUCCESS")
        
        # Lister les fichiers générés
        word_files = list(output_dir.glob("*.docx"))
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

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n⚠️ Workflow interrompu")
        sys.exit(130)
    except Exception as e:
        print(f"\n❌ Erreur fatale : {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
