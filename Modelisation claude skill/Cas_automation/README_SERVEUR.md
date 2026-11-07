# Serveur d'Automation - Documentation

## Vue d'ensemble

Serveur Flask Python pour la génération automatique de documents Word à partir de JSON standards, sans intervention d'agent. Utilise l'environnement miniconda `pdf_excel_env` du projet.

## Architecture

```
Cas_automation/
├── server_automation.py       # Serveur Flask principal
├── start_server.bat          # Script de démarrage Windows
├── json standard/            # JSON de référence par cas
│   ├── Json_standard_[Cas 6].txt
│   ├── Json_standard_[Cas 7].txt
│   └── Json_standard_[Cas 8].txt
├── template_standard/        # Templates Word de référence
│   ├── template_standard_[Cas 6].docx
│   ├── template_standard_[Cas 7].docx
│   └── template_standard_[Cas 8].docx
└── output/                   # Documents générés (créé automatiquement)
```

## Prérequis

1. **Miniconda installé** avec l'environnement `pdf_excel_env`
2. **Python 3.11** (dans pdf_excel_env)
3. **Librairies requises** :
   - Flask
   - Flask-CORS
   - python-docx
   - Toutes les librairies de pdf_excel_env

## Installation

### 1. Activer l'environnement

```bash
conda activate pdf_excel_env
```

### 2. Installer Flask

```bash
pip install flask flask-cors
```

### 3. Vérifier l'installation

```bash
python server_automation.py
```

## Démarrage Rapide

### Windows

Double-cliquer sur `start_server.bat` ou exécuter :

```cmd
start_server.bat
```

### Manuel

```bash
conda activate pdf_excel_env
python server_automation.py
```

Le serveur démarre sur `http://localhost:5000`

## Endpoints API

### 1. Health Check

**GET** `/health`

Vérifie l'état du serveur et les skills chargés.

**Réponse :**
```json
{
  "status": "healthy",
  "timestamp": "2026-11-07T15:30:00",
  "environment": "pdf_excel_env",
  "available_endpoints": [...],
  "skills_loaded": {
    "cas_6": true,
    "cas_7": true,
    "cas_8": true
  }
}
```

**Exemple cURL :**
```bash
curl http://localhost:5000/health
```

---

### 2. Génération Feuille de Révision (Cas 6)

**POST** `/automation/cas_6`

Génère une Feuille de Révision à partir d'un JSON.

**Headers :**
- `Content-Type: application/json`

**Body :**
```json
{
  "Etape mission - Feuille revision": [
    {
      "table 0 - Signature worksheet": [...],
      "table 1": [...],
      "table 2": [...],
      ...
    }
  ]
}
```

**Réponse :**
- Fichier Word `.docx` en téléchargement

**Exemple cURL :**
```bash
curl -X POST http://localhost:5000/automation/cas_6 \
  -H "Content-Type: application/json" \
  -d @"json standard/Json_standard_[Cas 6].txt" \
  -o output_cas6.docx
```

**Exemple N8N :**
```json
{
  "method": "POST",
  "url": "http://localhost:5000/automation/cas_6",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": "{{ $json }}",
  "responseType": "file"
}
```

---

### 3. Génération Feuille de Couverture (Cas 7)

**POST** `/automation/cas_7`

Génère une Feuille de Couverture à partir d'un JSON.

**Structure similaire au Cas 6** avec la clé :
```json
{
  "Etape mission - Feuille couverture": [...]
}
```

**Exemple cURL :**
```bash
curl -X POST http://localhost:5000/automation/cas_7 \
  -H "Content-Type: application/json" \
  -d @"json standard/Json_standard_[Cas 7].txt" \
  -o output_cas7.docx
```

---

### 4. Génération Modèle Standard (Cas 8)

**POST** `/automation/cas_8`

Génère un document à partir du modèle standard :
- Programme de travail
- Cartographie des risques
- Matrice de surveillance permanente
- Plan de recommandation

**Structure :**
```json
{
  "Etape mission - Modele standard": [...]
}
```

**Exemple cURL :**
```bash
curl -X POST http://localhost:5000/automation/cas_8 \
  -H "Content-Type: application/json" \
  -d @"json standard/Json_standard_[Cas 8].txt" \
  -o output_cas8.docx
```

---

### 5. Test avec JSON Standard

**GET** `/automation/test/<cas_number>`

Génère un document de test en utilisant le JSON standard du dossier.

**Paramètres :**
- `cas_number` : 6, 7 ou 8

**Exemple :**
```bash
# Test Cas 6
curl http://localhost:5000/automation/test/6 -o test_cas6.docx

# Test Cas 7
curl http://localhost:5000/automation/test/7 -o test_cas7.docx

# Test Cas 8
curl http://localhost:5000/automation/test/8 -o test_cas8.docx
```

## Convention de Nommage

Les fichiers générés suivent la convention :

```
[REFERENCE]_Cas[N]_[TIMESTAMP].docx
```

Exemples :
- `FC-BK-A10_Cas6_20261107_153045.docx`
- `AUTO_Feuille_Revision_Cas6_20261107_153045.docx` (sans référence)

## Intégration N8N

### Node HTTP Request

```json
{
  "name": "Generer Document Cas 6",
  "type": "n8n-nodes-base.httpRequest",
  "parameters": {
    "method": "POST",
    "url": "http://localhost:5000/automation/cas_6",
    "authentication": "none",
    "sendHeaders": true,
    "headerParameters": {
      "parameters": [
        {
          "name": "Content-Type",
          "value": "application/json"
        }
      ]
    },
    "sendBody": true,
    "bodyParameters": {
      "parameters": []
    },
    "jsonParameters": true,
    "options": {
      "response": {
        "response": {
          "responseFormat": "file"
        }
      }
    },
    "body": "={{ $json }}"
  }
}
```

### Workflow N8N Complet

```
[Webhook] → [JSON Processing] → [HTTP Request to Flask] → [Save File] → [Response]
```

## Gestion des Erreurs

### Erreurs HTTP

- **400 Bad Request** : JSON invalide ou structure incorrecte
- **404 Not Found** : Endpoint inexistant
- **500 Internal Server Error** : Erreur de génération

### Format des erreurs

```json
{
  "error": "Description de l'erreur",
  "traceback": "Stack trace complet (si debug=True)"
}
```

### Logs

Les logs sont affichés dans la console du serveur :
```
[2026-11-07 15:30:00] INFO: Requête POST /automation/cas_6
[2026-11-07 15:30:05] SUCCESS: Document généré : output.docx
[2026-11-07 15:30:05] ERROR: Erreur dans cas_6: ...
```

## Configuration

### Port du serveur

Par défaut : `5000`

Pour changer, modifier dans `server_automation.py` :
```python
app.run(host='0.0.0.0', port=8080, debug=True)
```

### Dossier de sortie

Par défaut : `Cas_automation/output/`

Pour changer :
```python
OUTPUT_DIR = BASE_DIR / "mon_dossier_custom"
```

### Mode Debug

Pour production, désactiver :
```python
app.run(..., debug=False)
```

## Dépannage

### Le serveur ne démarre pas

1. Vérifier l'environnement :
```bash
conda activate pdf_excel_env
conda list
```

2. Réinstaller Flask :
```bash
pip install --force-reinstall flask flask-cors
```

### Les skills ne se chargent pas

Vérifier que les fichiers existent :
- `Cas_6/audit-etap-mission-feuille-revision/scripts/build_docx.py`
- `Cas_7/audit-etap-mission-feuille-couverture/scripts/build_docx.py`
- `Cas_8/audit-etap-mission-feuille-modele-standard/scripts/build_docx.py`

### Erreur "Document non généré"

Vérifier les permissions d'écriture sur le dossier `output/`

## Performance

- **Temps de génération** : 2-5 secondes par document
- **Taille maximale JSON** : 10 MB recommandé
- **Concurrence** : 10 requêtes simultanées (Flask dev server)

Pour production, utiliser **Gunicorn** :
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 server_automation:app
```

## Sécurité

### Recommandations

1. **Ne pas exposer directement sur Internet** sans authentification
2. **Utiliser HTTPS** en production
3. **Limiter les tailles de requêtes**
4. **Valider strictement les JSON**

### Ajout d'authentification (optionnel)

```python
from functools import wraps

def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        if api_key != 'VOTRE_CLE_SECRETE':
            return jsonify({"error": "API Key invalide"}), 401
        return f(*args, **kwargs)
    return decorated_function

@app.route('/automation/cas_6', methods=['POST'])
@require_api_key
def endpoint_automation_cas_6():
    ...
```

## Maintenance

### Logs

Les logs sont stockés dans la console. Pour persistence :

```python
import logging
from logging.handlers import RotatingFileHandler

handler = RotatingFileHandler('server.log', maxBytes=10000, backupCount=3)
app.logger.addHandler(handler)
```

### Monitoring

Utiliser `/health` pour monitoring :
```bash
# Cron job toutes les 5 minutes
*/5 * * * * curl -f http://localhost:5000/health || echo "Serveur down"
```

## Support

Pour toute question ou problème :
1. Vérifier les logs du serveur
2. Tester avec `/automation/test/<cas>`
3. Valider le JSON avec un validateur en ligne

---

**Version** : 1.0.0  
**Date** : 7 novembre 2026  
**Environnement** : pdf_excel_env (Python 3.11)
