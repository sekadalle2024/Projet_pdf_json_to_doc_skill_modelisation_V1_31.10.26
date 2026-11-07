#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Server Flask d'automation pour génération de documents Word
à partir des données JSON collectées par N8N.

PORT: 5000
ENVIRONNEMENT: pdf_excel_env (miniconda)
ACTIVATION: conda activate pdf_excel_env

Endpoints:
- GET  /health                  : État du serveur
- POST /automation/cas_6        : Feuille de révision
- POST /automation/cas_7        : Feuille de couverture
- POST /automation/cas_8        : Programme de travail
- GET  /automation/test/<cas>   : Test avec JSON standard
"""

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from pathlib import Path
import json
import sys
import os
import subprocess
from datetime import datetime
import traceback
import tempfile

# Configuration des chemins
SCRIPT_DIR = Path(__file__).parent
BASE_DIR = SCRIPT_DIR.parent

# Utiliser le dossier Téléchargements Windows (chemin court et accessible)
DOWNLOADS_DIR = Path.home() / "Downloads"
OUTPUT_DIR = DOWNLOADS_DIR
OUTPUT_DIR.mkdir(exist_ok=True)

JSON_STANDARD_DIR = SCRIPT_DIR / "json standard"

# Chemins vers les scripts Python des Cas
CAS_6_SCRIPT = BASE_DIR / "Cas_6" / "json2word_feuilles_revision_v5.py"  # Version 5 - Tables horizontales + sans lignes vides
CAS_7_SCRIPT = BASE_DIR / "Cas_7" / "json2word_feuille_couverture.py"
CAS_8_SCRIPT = BASE_DIR / "Cas_8" / "json2word_programme_travail.py"
CAS_10_SCRIPT = SCRIPT_DIR / "Cas_10_automation" / "json2word_cas10_automation.py"

# Vérifier la disponibilité des scripts
CAS_6_AVAILABLE = CAS_6_SCRIPT.exists()
CAS_7_AVAILABLE = CAS_7_SCRIPT.exists()
CAS_8_AVAILABLE = CAS_8_SCRIPT.exists()
CAS_10_AVAILABLE = CAS_10_SCRIPT.exists()

# Créer l'application Flask
app = Flask(__name__)
CORS(app)  # Activer CORS pour N8N

# =============================================================================
# FONCTIONS UTILITAIRES
# =============================================================================

def run_python_script(script_path, json_file_path, output_dir, use_dash_o=True, cas_number=None):
    """
    Exécute un script Python en tant que processus externe.
    
    Args:
        script_path: Chemin vers le script .py
        json_file_path: Chemin vers le fichier JSON d'entrée
        output_dir: Dossier de sortie
        use_dash_o: Si True, utilise "-o <dir>", sinon juste "<dir>"
        cas_number: Numéro du cas (pour le renommage)
        
    Returns:
        tuple: (success: bool, stdout: str, stderr: str, output_file: Path or None)
    """
    try:
        # Utiliser sys.executable pour garantir qu'on utilise le bon Python
        if use_dash_o:
            # Format: script.py <json> -o <output_dir>  (Cas 6)
            cmd = [
                sys.executable,
                str(script_path),
                str(json_file_path),
                "-o", str(output_dir)
            ]
        else:
            # Format: script.py <json> <output_dir>  (Cas 7, 8)
            cmd = [
                sys.executable,
                str(script_path),
                str(json_file_path),
                str(output_dir)
            ]
        
        # Compter les fichiers avant
        output_dir_path = Path(output_dir)
        files_before = set(output_dir_path.glob("*.docx"))
        
        # Forcer l'encodage UTF-8 pour éviter les problèmes avec les emojis
        env = os.environ.copy()
        env['PYTHONIOENCODING'] = 'utf-8'
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace',
            timeout=120,
            cwd=str(script_path.parent),
            env=env
        )
        
        success = result.returncode == 0
        
        # Trouver le fichier créé
        output_file = None
        if success:
            # Attendre un peu pour que Word finisse d'écrire le fichier
            import time
            time.sleep(0.5)
            
            files_after = set(output_dir_path.glob("*.docx"))
            new_files = files_after - files_before
            
            if new_files:
                output_file = max(new_files, key=lambda p: p.stat().st_mtime)
                
                # Toujours renommer avec un nom court et simple
                if cas_number:
                    # Attendre que le fichier soit fermé
                    time.sleep(0.5)
                    short_path = rename_to_short_name(output_file, cas_number)
                    if short_path:
                        output_file = short_path
        
        return success, result.stdout, result.stderr, output_file
        
    except subprocess.TimeoutExpired:
        return False, "", "Timeout: Le script a pris plus de 120 secondes", None
    except Exception as e:
        return False, "", str(e), None


def find_latest_docx(directory):
    """Trouve le dernier fichier .docx créé dans un dossier."""
    docx_files = list(Path(directory).glob("*.docx"))
    if not docx_files:
        return None
    return max(docx_files, key=lambda p: p.stat().st_mtime)


def generate_short_filename(cas_number, reference=None):
    """
    Génère un nom de fichier court et simple.
    Format: Cas{N}_{TIMESTAMP}.docx
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"Cas{cas_number}_{timestamp}.docx"


def rename_to_short_name(long_path, cas_number):
    """
    Renomme un fichier avec un nom long vers un nom court et simple.
    Retourne le nouveau chemin.
    """
    long_path = Path(long_path)
    if not long_path.exists():
        return None
    
    short_name = generate_short_filename(cas_number)
    short_path = long_path.parent / short_name
    
    try:
        long_path.rename(short_path)
        return short_path
    except Exception as e:
        print(f"Erreur lors du renommage: {e}")
        return long_path  # Retourner le chemin original en cas d'erreur


# =============================================================================
# ROUTES
# =============================================================================

@app.route('/health', methods=['GET'])
def health_check():
    """Vérification de l'état du serveur."""
    return jsonify({
        'status': 'ok',
        'timestamp': datetime.now().isoformat(),
        'capabilities': {
            'cas_6': CAS_6_AVAILABLE,
            'cas_7': CAS_7_AVAILABLE,
            'cas_8': CAS_8_AVAILABLE,
            'cas_10': CAS_10_AVAILABLE
        },
        'paths': {
            'output': str(OUTPUT_DIR),
            'json_standard': str(JSON_STANDARD_DIR),
            'cas_6_script': str(CAS_6_SCRIPT) if CAS_6_AVAILABLE else None,
            'cas_7_script': str(CAS_7_SCRIPT) if CAS_7_AVAILABLE else None,
            'cas_8_script': str(CAS_8_SCRIPT) if CAS_8_AVAILABLE else None,
            'cas_10_script': str(CAS_10_SCRIPT) if CAS_10_AVAILABLE else None
        }
    })


@app.route('/automation/cas_6', methods=['POST'])
def automation_cas_6():
    """
    Génère une Feuille de révision (Cas 6).
    
    Body JSON attendu:
    {
        "data": {
            "Etape mission - Feuille revision": [...]
        },
        "source": "n8n" (optionnel)
    }
    """
    if not CAS_6_AVAILABLE:
        return jsonify({
            'success': False,
            'error': f'Cas 6 non disponible: {CAS_6_SCRIPT} introuvable'
        }), 503
    
    try:
        # Récupérer les données JSON
        data = request.get_json()
        if not data:
            return jsonify({
                'success': False,
                'error': 'Aucune donnée JSON fournie'
            }), 400
        
        # Créer un fichier temporaire avec les données
        with tempfile.NamedTemporaryFile(
            mode='w', 
            suffix='.json', 
            delete=False, 
            encoding='utf-8',
            dir=str(OUTPUT_DIR)
        ) as tmp:
            json.dump(data, tmp, ensure_ascii=False, indent=2)
            temp_json_path = Path(tmp.name)
        
        # Exécuter le script Cas 6 (format: <json> -o <output_dir>)
        success, stdout, stderr, output_file = run_python_script(
            CAS_6_SCRIPT, temp_json_path, OUTPUT_DIR, use_dash_o=True, cas_number=6
        )
        
        # Nettoyer le fichier temporaire
        temp_json_path.unlink()
        
        if success and output_file:
            return jsonify({
                'success': True,
                'filename': output_file.name,
                'path': str(output_file),
                'cas': 6,
                'type': 'Feuille de révision',
                'timestamp': datetime.now().isoformat(),
                'stdout': stdout
            })
        
        return jsonify({
            'success': False,
            'error': 'La génération a échoué',
            'stderr': stderr,
            'stdout': stdout
        }), 500
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'traceback': traceback.format_exc()
        }), 500


@app.route('/automation/cas_7', methods=['POST'])
def automation_cas_7():
    """
    Génère une Feuille de couverture (Cas 7).
    
    Body JSON attendu:
    {
        "data": {
            "Etape mission - Feuille couverture": [...]
        },
        "source": "n8n" (optionnel)
    }
    """
    if not CAS_7_AVAILABLE:
        return jsonify({
            'success': False,
            'error': f'Cas 7 non disponible: {CAS_7_SCRIPT} introuvable'
        }), 503
    
    try:
        # Récupérer les données JSON
        data = request.get_json()
        if not data:
            return jsonify({
                'success': False,
                'error': 'Aucune donnée JSON fournie'
            }), 400
        
        # Créer un fichier temporaire avec les données
        with tempfile.NamedTemporaryFile(
            mode='w', 
            suffix='.json', 
            delete=False, 
            encoding='utf-8',
            dir=str(OUTPUT_DIR)
        ) as tmp:
            json.dump(data, tmp, ensure_ascii=False, indent=2)
            temp_json_path = Path(tmp.name)
        
        # Exécuter le script Cas 7 (format: <json> <output_dir>)
        success, stdout, stderr, output_file = run_python_script(
            CAS_7_SCRIPT, temp_json_path, OUTPUT_DIR, use_dash_o=False, cas_number=7
        )
        
        # Nettoyer le fichier temporaire
        temp_json_path.unlink()
        
        if success and output_file:
            return jsonify({
                'success': True,
                'filename': output_file.name,
                'path': str(output_file),
                'cas': 7,
                'type': 'Feuille de couverture',
                'timestamp': datetime.now().isoformat(),
                'stdout': stdout
            })
        
        return jsonify({
            'success': False,
            'error': 'La génération a échoué',
            'stderr': stderr,
            'stdout': stdout
        }), 500
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'traceback': traceback.format_exc()
        }), 500


@app.route('/automation/cas_8', methods=['POST'])
def automation_cas_8():
    """
    Génère un Programme de travail (Cas 8).
    
    Body JSON attendu:
    {
        "data": {
            "Etape mission - Programme de travail": [...]
        },
        "source": "n8n" (optionnel)
    }
    """
    if not CAS_8_AVAILABLE:
        return jsonify({
            'success': False,
            'error': f'Cas 8 non disponible: {CAS_8_SCRIPT} introuvable'
        }), 503
    
    try:
        # Récupérer les données JSON
        data = request.get_json()
        if not data:
            return jsonify({
                'success': False,
                'error': 'Aucune donnée JSON fournie'
            }), 400
        
        # Créer un fichier temporaire avec les données
        with tempfile.NamedTemporaryFile(
            mode='w', 
            suffix='.json', 
            delete=False, 
            encoding='utf-8',
            dir=str(OUTPUT_DIR)
        ) as tmp:
            json.dump(data, tmp, ensure_ascii=False, indent=2)
            temp_json_path = Path(tmp.name)
        
        # Exécuter le script Cas 8 (format: <json> <output_dir>)
        success, stdout, stderr, output_file = run_python_script(
            CAS_8_SCRIPT, temp_json_path, OUTPUT_DIR, use_dash_o=False, cas_number=8
        )
        
        # Nettoyer le fichier temporaire
        temp_json_path.unlink()
        
        if success and output_file:
            return jsonify({
                'success': True,
                'filename': output_file.name,
                'path': str(output_file),
                'cas': 8,
                'type': 'Programme de travail',
                'timestamp': datetime.now().isoformat(),
                'stdout': stdout
            })
        
        return jsonify({
            'success': False,
            'error': 'La génération a échoué',
            'stderr': stderr,
            'stdout': stdout
        }), 500
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'traceback': traceback.format_exc()
        }), 500


@app.route('/automation/cas_10', methods=['POST'])
def automation_cas_10():
    """
    Génère un Programme de travail avec Modelisation design (Cas 10).
    
    Body JSON attendu:
    {
        "data": {
            "Etape mission - Programme": [...]
        },
        "source": "n8n" (optionnel)
    }
    """
    if not CAS_10_AVAILABLE:
        return jsonify({
            'success': False,
            'error': f'Cas 10 non disponible: {CAS_10_SCRIPT} introuvable'
        }), 503
    
    try:
        # Récupérer les données JSON
        data = request.get_json()
        if not data:
            return jsonify({
                'success': False,
                'error': 'Aucune donnée JSON fournie'
            }), 400
        
        # Créer un fichier temporaire avec les données
        with tempfile.NamedTemporaryFile(
            mode='w', 
            suffix='.json', 
            delete=False, 
            encoding='utf-8',
            dir=str(OUTPUT_DIR)
        ) as tmp:
            json.dump(data, tmp, ensure_ascii=False, indent=2)
            temp_json_path = Path(tmp.name)
        
        # Exécuter le script Cas 10 (format: <json> <output_dir>)
        success, stdout, stderr, output_file = run_python_script(
            CAS_10_SCRIPT, temp_json_path, OUTPUT_DIR, use_dash_o=False, cas_number=10
        )
        
        # Nettoyer le fichier temporaire
        temp_json_path.unlink()
        
        if success and output_file:
            return jsonify({
                'success': True,
                'filename': output_file.name,
                'path': str(output_file),
                'cas': 10,
                'type': 'Programme de travail avec Modelisation design',
                'timestamp': datetime.now().isoformat(),
                'stdout': stdout
            })
        
        return jsonify({
            'success': False,
            'error': 'La génération a échoué',
            'stderr': stderr,
            'stdout': stdout
        }), 500
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'traceback': traceback.format_exc()
        }), 500


@app.route('/automation/test/<int:cas>', methods=['GET'])
def test_cas(cas):
    """
    Endpoint de test qui utilise le JSON standard pour un cas donné.
    
    Usage: GET /automation/test/6
    """
    if cas not in [6, 7, 8, 10]:
        return jsonify({
            'success': False,
            'error': f'Cas {cas} non supporté (seulement 6, 7, 8, 10)'
        }), 400
    
    # Charger le JSON standard
    json_file = JSON_STANDARD_DIR / f"Json_standard_[Cas {cas}].txt"
    if not json_file.exists():
        return jsonify({
            'success': False,
            'error': f'JSON standard introuvable: {json_file.name}'
        }), 404
    
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Rediriger vers l'endpoint approprié
        with app.test_client() as client:
            response = client.post(
                f'/automation/cas_{cas}',
                json=data,
                headers={'Content-Type': 'application/json'}
            )
            return response.get_json(), response.status_code
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'traceback': traceback.format_exc()
        }), 500


@app.route('/')
def index():
    """Page d'accueil avec documentation."""
    return jsonify({
        'name': 'Serveur Automation Cas 6/7/8/10',
        'version': '2.2',
        'status': 'running',
        'endpoints': {
            'health': 'GET /health',
            'cas_6': 'POST /automation/cas_6',
            'cas_7': 'POST /automation/cas_7',
            'cas_8': 'POST /automation/cas_8',
            'cas_10': 'POST /automation/cas_10',
            'test': 'GET /automation/test/<6|7|8|10>'
        },
        'documentation': '/README_SERVEUR.md',
        'integration_n8n': '/INTEGRATION_N8N.md'
    })


# =============================================================================
# MAIN
# =============================================================================

if __name__ == '__main__':
    print("=" * 70)
    print("Serveur Automation Cas 6/7/8/10")
    print("=" * 70)
    print(f"Output: {OUTPUT_DIR}")
    print(f"JSON Standard: {JSON_STANDARD_DIR}")
    print(f"Cas 6 disponible: {CAS_6_AVAILABLE}")
    print(f"Cas 7 disponible: {CAS_7_AVAILABLE}")
    print(f"Cas 8 disponible: {CAS_8_AVAILABLE}")
    print(f"Cas 10 disponible: {CAS_10_AVAILABLE}")
    print("=" * 70)
    print("Demarrage du serveur sur http://localhost:5000")
    print("Ctrl+C pour arreter")
    print("=" * 70)
    
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )
