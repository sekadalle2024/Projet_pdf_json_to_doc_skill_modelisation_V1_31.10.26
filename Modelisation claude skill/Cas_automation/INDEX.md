# Index - Système d'Automation

## 📋 Vue d'ensemble

Système complet d'automation pour la génération de documents Word à partir de JSON standards, sans intervention d'agent IA. Utilise un serveur Flask Python avec l'environnement miniconda `pdf_excel_env`.

## 📁 Structure du Projet

```
Cas_automation/
├── server_automation.py          # ⚙️ Serveur Flask principal
├── start_server.bat             # 🚀 Script de démarrage
├── setup_server.bat             # 🔧 Configuration initiale
├── test_server.py               # 🧪 Suite de tests
├── exemples_curl.bat            # 📝 Exemples de requêtes
├── requirements_server.txt      # 📦 Dépendances Python
│
├── README_SERVEUR.md            # 📖 Documentation complète
├── INTEGRATION_N8N.md           # 🔗 Guide intégration N8N
├── INDEX.md                     # 📍 Ce fichier
│
├── json standard/               # 📄 JSON de référence
│   ├── Json_standard_[Cas 6].txt
│   ├── Json_standard_[Cas 7].txt
│   └── Json_standard_[Cas 8].txt
│
├── template_standard/           # 📋 Templates Word
│   ├── template_standard_[Cas 6].docx
│   ├── template_standard_[Cas 7].docx
│   └── template_standard_[Cas 8].docx
│
└── output/                      # 📤 Documents générés (auto)
```

## 🎯 Cas d'Usage Supportés

| Cas | Étape de Mission | Endpoint | JSON Key |
|-----|------------------|----------|----------|
| **6** | Feuille de Révision | `/automation/cas_6` | `Etape mission - Feuille revision` |
| **7** | Feuille de Couverture | `/automation/cas_7` | `Etape mission - Feuille couverture` |
| **8** | Modèle Standard | `/automation/cas_8` | `Etape mission - Modele standard` |

**Cas 8 inclut :**
- Programme de travail
- Cartographie des risques
- Matrice de surveillance permanente
- Plan de recommandation

## 🚀 Démarrage Rapide

### 1. Configuration (première fois)

```bash
setup_server.bat
```

### 2. Démarrage du serveur

```bash
start_server.bat
```

### 3. Test du serveur

```bash
python test_server.py
```

### 4. Vérification

```bash
curl http://localhost:5000/health
```

## 📚 Documentation

### Guides Principaux

1. **[README_SERVEUR.md](README_SERVEUR.md)**
   - Installation complète
   - Documentation API détaillée
   - Exemples cURL
   - Gestion des erreurs
   - Configuration avancée

2. **[INTEGRATION_N8N.md](INTEGRATION_N8N.md)**
   - Workflows N8N complets
   - Configuration des nodes
   - Exemples de requêtes
   - Gestion des erreurs
   - Sécurité et monitoring

## 🔌 Endpoints API

### Health Check
```bash
GET /health
```

### Génération Documents
```bash
POST /automation/cas_6   # Feuille Révision
POST /automation/cas_7   # Feuille Couverture
POST /automation/cas_8   # Modèle Standard
```

### Tests
```bash
GET /automation/test/6   # Test avec JSON standard Cas 6
GET /automation/test/7   # Test avec JSON standard Cas 7
GET /automation/test/8   # Test avec JSON standard Cas 8
```

## 💻 Exemples d'Utilisation

### cURL

```bash
# Test rapide
curl http://localhost:5000/health

# Génération Cas 6
curl -X POST http://localhost:5000/automation/cas_6 \
  -H "Content-Type: application/json" \
  -d @"json standard/Json_standard_[Cas 6].txt" \
  -o output.docx
```

### Python

```python
import requests
import json

# Charger le JSON
with open('json standard/Json_standard_[Cas 6].txt', 'r') as f:
    data = json.load(f)

# Appeler l'API
response = requests.post(
    'http://localhost:5000/automation/cas_6',
    json=data
)

# Sauvegarder le document
with open('output.docx', 'wb') as f:
    f.write(response.content)
```

### JavaScript

```javascript
const response = await fetch('http://localhost:5000/automation/cas_6', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify(jsonData)
});

const blob = await response.blob();
// Télécharger ou sauvegarder le blob
```

## 🛠️ Scripts Disponibles

| Script | Description |
|--------|-------------|
| `setup_server.bat` | Configuration initiale du serveur |
| `start_server.bat` | Démarrage du serveur Flask |
| `test_server.py` | Suite de tests automatiques |
| `exemples_curl.bat` | Menu interactif d'exemples cURL |

## 📊 Flux de Données

```
┌──────────────┐
│  Client      │  (N8N, cURL, Python, etc.)
│  (JSON)      │
└──────┬───────┘
       │ POST /automation/cas_X
       ▼
┌──────────────┐
│  Flask       │  Validation + Routage
│  Server      │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  Skill       │  Génération Document
│  (build_docx)│
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  Output      │  Document Word (.docx)
│  File        │
└──────────────┘
```

## 🔧 Prérequis Techniques

- **Système:** Windows 10/11
- **Python:** 3.11 (via pdf_excel_env)
- **Miniconda:** Installé et configuré
- **Environnement:** pdf_excel_env activé
- **Librairies:**
  - Flask >= 3.0.0
  - Flask-CORS >= 4.0.0
  - python-docx >= 1.1.0
  - Toutes les librairies de pdf_excel_env

## 📈 Performance

- **Temps de génération:** 2-5 secondes par document
- **Taille max JSON:** 10 MB recommandé
- **Concurrence:** 10 requêtes simultanées (dev server)
- **Production:** Utiliser Gunicorn pour > 10 req/s

## 🔒 Sécurité

### Recommandations

- ✅ Utiliser HTTPS en production
- ✅ Ajouter authentification par API Key
- ✅ Limiter les tailles de requêtes
- ✅ Valider strictement les JSON
- ❌ Ne pas exposer directement sur Internet

### Authentification (optionnelle)

Ajouter dans `server_automation.py`:

```python
@app.before_request
def check_api_key():
    api_key = request.headers.get('X-API-Key')
    if api_key != 'YOUR_SECRET_KEY':
        return jsonify({"error": "Unauthorized"}), 401
```

## 📝 Logs et Monitoring

### Logs Console

Le serveur affiche en temps réel:
```
[2026-11-07 15:30:00] INFO: POST /automation/cas_6
[2026-11-07 15:30:05] SUCCESS: Document généré
```

### Monitoring

```bash
# Health check périodique
curl -f http://localhost:5000/health || echo "Serveur down"
```

## 🐛 Dépannage

### Le serveur ne démarre pas

1. Vérifier l'environnement:
   ```bash
   conda activate pdf_excel_env
   conda list
   ```

2. Réinstaller Flask:
   ```bash
   pip install --force-reinstall flask flask-cors
   ```

### Les skills ne se chargent pas

Vérifier la structure des dossiers:
```
Modelisation claude skill/
├── Cas_6/audit-etap-mission-feuille-revision/scripts/build_docx.py
├── Cas_7/audit-etap-mission-feuille-couverture/scripts/build_docx.py
└── Cas_8/audit-etap-mission-feuille-modele-standard/scripts/build_docx.py
```

### Erreur "Document non généré"

Vérifier les permissions sur le dossier `output/`

## 📞 Support

### Commandes de diagnostic

```bash
# 1. Vérifier l'environnement
conda activate pdf_excel_env
python --version

# 2. Tester le serveur
python test_server.py

# 3. Vérifier les JSON standards
dir "json standard"

# 4. Tester un endpoint
curl http://localhost:5000/automation/test/6 -o test.docx
```

### Fichiers de log

- Console du serveur
- `output/` (documents générés)
- `test_output/` (résultats des tests)

## 🔄 Mise à Jour

### Mettre à jour les skills

1. Modifier les scripts dans `Cas_X/`
2. Redémarrer le serveur: `start_server.bat`

### Mettre à jour le serveur

1. Modifier `server_automation.py`
2. Redémarrer le serveur

Pas besoin de reconstruire les skills !

## 📦 Déploiement Production

### Utiliser Gunicorn

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 server_automation:app
```

### Utiliser Docker (optionnel)

```dockerfile
FROM python:3.11
COPY . /app
WORKDIR /app
RUN pip install -r requirements_server.txt
CMD ["python", "server_automation.py"]
```

## 🎓 Ressources Complémentaires

- **Environnement PDF Excel:** `../../environment.yml`
- **Skills Cas 6-8:** `../Cas_X/`
- **Documentation N8N:** https://docs.n8n.io/
- **Flask Docs:** https://flask.palletsprojects.com/

## 📅 Changelog

### Version 1.0.0 (7 Nov 2026)
- ✨ Création du serveur Flask
- ✨ Support Cas 6, 7, 8
- ✨ Endpoints de test
- ✨ Documentation complète
- ✨ Intégration N8N
- ✨ Scripts de démarrage

## 🚧 Roadmap

### Version 1.1.0 (À venir)
- [ ] Support Cas 10 (multi-cas)
- [ ] Cache des documents générés
- [ ] Dashboard de monitoring
- [ ] Authentification OAuth2

### Version 1.2.0 (Futur)
- [ ] Support Cas 12-13 (Cartographie + Heatmap)
- [ ] Export PDF direct
- [ ] Webhooks de notification
- [ ] API REST complète avec Swagger

---

**Maintenu par:** Équipe Automation  
**Version:** 1.0.0  
**Date:** 7 novembre 2026  
**Environnement:** pdf_excel_env (Python 3.11)
