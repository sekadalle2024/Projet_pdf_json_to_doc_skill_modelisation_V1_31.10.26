#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
═══════════════════════════════════════════════════════════════════════════════
    CAS 10 - ROUTEUR INTELLIGENT DE SKILLS N8N
    Détecte les types de missions et route vers les skills appropriées
═══════════════════════════════════════════════════════════════════════════════

Description:
    Cas 10 est un ROUTEUR DE SKILLS, pas un exécuteur direct.
    
    Workflow:
    1. Appelle le webhook source pour récupérer les données
    2. Détecte automatiquement les types d'étapes de mission
    3. Route vers la SKILL N8N appropriée (Cas 2, 3, 5, 6, 7, 8)
    4. Chaque skill génère ses propres documents Word
    
    Cas 10 NE génère PAS les documents lui-même !
    Il délègue à la skill spécialisée pour chaque type.

Auteur: Expert Python & Automation
Date: 5 novembre 2026
Version: 3.0.0

Dépendances:
    - requests
    - cas10_router.py (détection du type)
"""

import requests
import json
import sys
import subprocess
import tempfile
from pathlib import Path
from datetime import datetime
from cas10_router import Cas10Router

# ═══════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════

# Webhook source qui fournit les données multi-types
WEBHOOK_URL_SOURCE = "http://localhost:5678/webhook/skill_manuel_audit"
TIMEOUT = 30

# Mapping des cas vers leurs SCRIPTS PYTHON
# Cas 10 route vers les scripts Python directement
BASE_DIR = Path(__file__).parent.parent  # Dossier Modelisation claude skill/

CAS_SCRIPTS = {
    2: BASE_DIR / "Cas_2" / "json2word_audit.py",
    3: BASE_DIR / "Cas_3" / "json2word_audit.py",  # Réutilise Cas 2
    5: BASE_DIR / "Cas_5" / "json2word_frap_recos.py",
    6: BASE_DIR / "Cas_6" / "json2word_feuilles_revision.py",
    7: BASE_DIR / "Cas_7" / "json2word_feuille_couverture.py",
    8: BASE_DIR / "Cas_8" / "json2word_programme_travail.py",
}

# Dossiers de sortie par cas
CAS_OUTPUT_DIRS = {
    2: BASE_DIR / "Cas_2" / "sortie_word_cas2",
    3: BASE_DIR / "Cas_3" / "sortie_word_cas3",
    5: BASE_DIR / "Cas_5" / "sortie_word_cas5",
    6: BASE_DIR / "Cas_6" / "sortie_word_cas6",
    7: BASE_DIR / "Cas_7" / "sortie_word_cas7",
    8: BASE_DIR / "Cas_8" / "sortie_word_cas8",
}

# Noms descriptifs des cas pour les logs
CAS_NAMES = {
    2: "Procédures d'audit",
    3: "Manuels d'audit",
    5: "FRAP et Recommandations",
    6: "Feuilles de révision",
    7: "Feuilles de couverture",
    8: "Programme de travail / Cartographie",
}

# ═══════════════════════════════════════════════════════════════════════════
# FONCTIONS UTILITAIRES
# ═══════════════════════════════════════════════════════════════════════════

def log(message, level="INFO"):
    """Affiche un message de log avec timestamp"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] [{level}] {message}")

def print_header(title):
    """Affiche un titre formaté"""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80 + "\n")

def print_section(title):
    """Affiche un titre de section"""
    print(f"\n{'─' * 80}")
    print(f"  {title}")
    print(f"{'─' * 80}\n")

# ═══════════════════════════════════════════════════════════════════════════
# ÉTAPE 1 : COLLECTE DES DONNÉES
# ═══════════════════════════════════════════════════════════════════════════

def call_source_webhook(url, timeout=30):
    """
    Appelle le webhook source pour récupérer les données
    
    Args:
        url: URL du webhook N8N
        timeout: Timeout en secondes
    
    Returns:
        dict: Réponse JSON complète ou None
    """
    log(f"Appel du webhook source : {url}")
    
    try:
        response = requests.post(
            url,
            json={},
            headers={"Content-Type": "application/json"},
            timeout=timeout
        )
        
        response.raise_for_status()
        log(f"✅ Réponse reçue (Status: {response.status_code})", "SUCCESS")
        
        data = response.json()
        return data
    
    except requests.exceptions.Timeout:
        log(f"❌ Timeout après {timeout}s", "ERROR")
        return None
    
    except requests.exceptions.ConnectionError:
        log("❌ Erreur de connexion au webhook", "ERROR")
        return None
    
    except requests.exceptions.HTTPError as e:
        log(f"❌ Erreur HTTP : {e}", "ERROR")
        return None
    
    except Exception as e:
        log(f"❌ Erreur inattendue : {e}", "ERROR")
        return None

def extract_mission_data(response):
    """
    Extrait les données de mission selon la structure du webhook
    
    Supporte deux structures :
    1. Data_integrale (ancien format)
    2. DATA_COLLECTION (nouveau format)
    
    Args:
        response: Réponse du webhook
    
    Returns:
        list: Liste des éléments de mission ou None
    """
    log("Extraction des données de mission")
    
    try:
        # Structure 0 : [{ "DATA_COLLECTION": [...] }] - Liste avec objet contenant DATA_COLLECTION
        if isinstance(response, list) and len(response) > 0:
            first_item = response[0]
            if isinstance(first_item, dict) and "DATA_COLLECTION" in first_item:
                collection = first_item["DATA_COLLECTION"]
                if isinstance(collection, list):
                    log(f"✅ Structure '[{{DATA_COLLECTION}}]' détectée : {len(collection)} élément(s)", "SUCCESS")
                    return collection
        
        # Structure 1 : Data_integrale
        if isinstance(response, list) and len(response) > 0:
            if "Data_integrale" in response[0]:
                data = response[0]["Data_integrale"]
                log(f"✅ Structure 'Data_integrale' détectée : {len(data)} élément(s)", "SUCCESS")
                return data
        
        elif isinstance(response, dict):
            if "Data_integrale" in response:
                data = response["Data_integrale"]
                log(f"✅ Structure 'Data_integrale' détectée : {len(data)} élément(s)", "SUCCESS")
                return data
        
        # Structure 2 : DATA_COLLECTION
        if isinstance(response, dict) and "DATA_COLLECTION" in response:
            collection = response["DATA_COLLECTION"]
            
            # DATA_COLLECTION peut être une liste directement
            if isinstance(collection, list):
                log(f"✅ Structure 'DATA_COLLECTION' (liste) détectée : {len(collection)} élément(s)", "SUCCESS")
                return collection
            
            # Ou un dict avec "data" dedans
            if isinstance(collection, dict):
                # Chercher le champ qui contient les données (data, items, elements, etc.)
                for data_key in ["data", "items", "elements", "content", "list"]:
                    if data_key in collection and isinstance(collection[data_key], list):
                        data = collection[data_key]
                        log(f"✅ Structure 'DATA_COLLECTION.{data_key}' détectée : {len(data)} élément(s)", "SUCCESS")
                        return data
                
                # Si DATA_COLLECTION est un dict sans clé connue, le traiter comme 1 élément
                log(f"✅ Structure 'DATA_COLLECTION' (dict unique) détectée : 1 élément", "SUCCESS")
                return [collection]
        
        log("❌ Structure de données non reconnue", "ERROR")
        log(f"Clés trouvées : {list(response.keys()) if isinstance(response, dict) else 'Liste'}", "DEBUG")
        return None
    
    except Exception as e:
        log(f"❌ Erreur lors de l'extraction : {e}", "ERROR")
        return None

# ═══════════════════════════════════════════════════════════════════════════
# ÉTAPE 2 : DÉTECTION DES TYPES ET ROUTAGE
# ═══════════════════════════════════════════════════════════════════════════

def detect_and_route_missions(mission_data):
    """
    Détecte le type de chaque mission et les regroupe par cas
    
    Args:
        mission_data: Liste des éléments de mission
    
    Returns:
        dict: Dictionnaire {cas_number: [list of mission items]}
    """
    log("Détection des types de mission")
    
    router = Cas10Router()
    routes = {}
    
    for idx, item in enumerate(mission_data, 1):
        # Détecter le type avec le routeur
        cas_number = router.detect_cas(item)
        
        if cas_number:
            cas_name = CAS_NAMES.get(cas_number, f"Cas {cas_number}")
            log(f"  [{idx}] → Cas {cas_number} ({cas_name})")
            
            # Ajouter à la route
            if cas_number not in routes:
                routes[cas_number] = []
            routes[cas_number].append(item)
        else:
            log(f"  [{idx}] → Type non reconnu (ignoré)", "WARNING")
    
    log(f"\n✅ Détection terminée : {len(routes)} type(s) détecté(s)", "SUCCESS")
    return routes

# ═══════════════════════════════════════════════════════════════════════════
# ÉTAPE 3 : EXÉCUTION DES SCRIPTS PYTHON
# ═══════════════════════════════════════════════════════════════════════════

def execute_script_for_cas(cas_number, mission_items):
    """
    Exécute le script Python approprié pour un cas donné
    
    Args:
        cas_number: Numéro du cas (2, 3, 5, 6, 7, 8)
        mission_items: Liste des items à traiter
    
    Returns:
        bool: True si succès, False sinon
    """
    script_path = CAS_SCRIPTS.get(cas_number)
    output_dir = CAS_OUTPUT_DIRS.get(cas_number)
    
    if not script_path or not script_path.exists():
        log(f"❌ Script non trouvé pour le Cas {cas_number}: {script_path}", "ERROR")
        return False
    
    cas_name = CAS_NAMES.get(cas_number, f"Cas {cas_number}")
    log(f"\nExécution du script : Cas {cas_number} - {cas_name}")
    log(f"  Script: {script_path.name}")
    log(f"  Items: {len(mission_items)}")
    
    # Créer le dossier de sortie si nécessaire
    output_dir.mkdir(parents=True, exist_ok=True)
    
    success_count = 0
    
    # Traiter chaque item
    for idx, item in enumerate(mission_items, 1):
        log(f"\n  Traitement item {idx}/{len(mission_items)}")
        
        # Créer un fichier JSON temporaire
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8') as tmp:
            json.dump(item, tmp, ensure_ascii=False, indent=2)
            tmp_path = tmp.name
        
        try:
            # Exécuter le script Python avec encoding UTF-8
            result = subprocess.run(
                [sys.executable, str(script_path), tmp_path, str(output_dir)],
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='replace',
                timeout=120
            )
            
            if result.returncode == 0:
                log(f"    ✅ Document {idx} créé", "SUCCESS")
                success_count += 1
            else:
                log(f"    ❌ Erreur document {idx}", "ERROR")
                if result.stderr:
                    log(f"    Détail: {result.stderr[:200]}", "ERROR")
        
        except subprocess.TimeoutExpired:
            log(f"    ❌ Timeout (120s) pour le document {idx}", "ERROR")
        
        except Exception as e:
            log(f"    ❌ Erreur : {e}", "ERROR")
        
        finally:
            # Supprimer le fichier temporaire
            try:
                Path(tmp_path).unlink()
            except:
                pass
    
    # Résumé
    log(f"\n  Résumé : {success_count}/{len(mission_items)} documents créés")
    
    return success_count > 0

# ═══════════════════════════════════════════════════════════════════════════
# ORCHESTRATEUR PRINCIPAL
# ═══════════════════════════════════════════════════════════════════════════

def main():
    """Fonction principale d'orchestration"""
    
    print_header("CAS 10 - ROUTEUR INTELLIGENT DE SKILLS N8N")
    
    log("Démarrage de l'orchestration multi-workflow")
    
    # ─────────────────────────────────────────────────────────────────────────
    # Étape 1 : Collecter les données du webhook source
    # ─────────────────────────────────────────────────────────────────────────
    
    print_section("ÉTAPE 1 : Collecte des données")
    
    response = call_source_webhook(WEBHOOK_URL_SOURCE, timeout=TIMEOUT)
    
    if response is None:
        log("❌ Impossible de récupérer les données", "ERROR")
        sys.exit(1)
    
    # ─────────────────────────────────────────────────────────────────────────
    # Étape 2 : Extraire et détecter les types de mission
    # ─────────────────────────────────────────────────────────────────────────
    
    print_section("ÉTAPE 2 : Extraction et détection")
    
    mission_data = extract_mission_data(response)
    
    if not mission_data or len(mission_data) == 0:
        log("❌ Aucune donnée de mission trouvée", "ERROR")
        sys.exit(1)
    
    log(f"✅ {len(mission_data)} élément(s) de mission trouvé(s)", "SUCCESS")
    
    # Détecter et router
    routes = detect_and_route_missions(mission_data)
    
    if not routes:
        log("❌ Aucun type de mission reconnu", "ERROR")
        sys.exit(1)
    
    # ─────────────────────────────────────────────────────────────────────────
    # Étape 3 : Exécuter les scripts Python appropriés
    # ─────────────────────────────────────────────────────────────────────────
    
    print_section("ÉTAPE 3 : Exécution des scripts de conversion")
    
    results = {}
    
    for cas_number in sorted(routes.keys()):
        cas_name = CAS_NAMES.get(cas_number, f"Cas {cas_number}")
        items = routes[cas_number]
        
        log(f"\n{'═' * 80}")
        log(f"Traitement : Cas {cas_number} - {cas_name}")
        log(f"Nombre d'items : {len(items)}")
        log(f"{'═' * 80}")
        
        success = execute_script_for_cas(cas_number, items)
        results[cas_number] = success
    
    # ─────────────────────────────────────────────────────────────────────────
    # Résumé final
    # ─────────────────────────────────────────────────────────────────────────
    
    print_section("RÉSUMÉ DE L'ORCHESTRATION")
    
    total_cas = len(results)
    total_success = sum(1 for success in results.values() if success)
    total_failed = total_cas - total_success
    
    log(f"Total de cas traités : {total_cas}")
    log(f"Scripts exécutés avec succès : {total_success}")
    log(f"Scripts échoués : {total_failed}")
    
    print("\nDétail par cas :")
    for cas_number in sorted(results.keys()):
        cas_name = CAS_NAMES.get(cas_number, f"Cas {cas_number}")
        status = "✅ SUCCÈS" if results[cas_number] else "❌ ÉCHEC"
        items_count = len(routes[cas_number])
        output_dir = CAS_OUTPUT_DIRS.get(cas_number, "")
        print(f"  • Cas {cas_number} ({cas_name}) : {status} - {items_count} item(s)")
        if results[cas_number] and output_dir:
            print(f"    → Sortie : {output_dir}")
    
    print("\n" + "=" * 80)
    
    if total_failed > 0:
        log("⚠️  Orchestration terminée avec des erreurs", "WARNING")
        log("   Vérifier que tous les scripts Python existent et fonctionnent", "INFO")
        sys.exit(1)
    else:
        log("✅ Orchestration terminée avec succès", "SUCCESS")
        log("   Les documents Word ont été générés dans leurs dossiers respectifs", "INFO")
        sys.exit(0)

# ═══════════════════════════════════════════════════════════════════════════
# POINT D'ENTRÉE
# ═══════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        log("\n\n⚠️  Interruption par l'utilisateur (Ctrl+C)", "WARNING")
        sys.exit(130)
    except Exception as e:
        log(f"\n\n❌ Erreur fatale : {e}", "ERROR")
        import traceback
        traceback.print_exc()
        sys.exit(1)
