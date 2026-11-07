# 🚀 Guide de démarrage rapide

## 📋 Prérequis

✅ **Environnement** : `pdf_excel_env` (miniconda)  
✅ **Python** : 3.11+  
✅ **Dépendances** : Flask, Flask-CORS, python-docx, requests

## 🏁 Démarrage en 3 étapes

### Étape 1️⃣ : Installer les dépendances

```bash
cd "h:\Projet_pdf_excel\Modelisation claude skill\Cas_automation"
conda activate pdf_excel_env
pip install -r requirements_server.txt
```

**OU** exécutez simplement :
```bash
setup_server.bat
```

### Étape 2️⃣ : Vérifier les imports

```bash
python verifier_imports.py
```

**Résultat attendu :**
```
✅ Cas 6 (Feuille de révision)  : OK
✅ Cas 7 (Feuille de couverture): OK
✅ Cas 8 (Programme de travail) : OK

🎉 Tous les modules sont disponibles !
```

### Étape 3️⃣ : Démarrer le serveur

```bash
python server_automation.py
```

**OU** double-cliquez sur :
```
start_server.bat
```

**Sortie attendue :**
```
======================================================================
🚀 Serveur Automation Cas 6/7/8
======================================================================
📁 Output: h:\Projet_pdf_excel\Modelisation claude skill\Cas_automation\output
📄 JSON Standard: h:\Projet_pdf_excel\Modelisation claude skill\Cas_automation\json standard
✅ Cas 6 disponible: True
✅ Cas 7 disponible: True
✅ Cas 8 disponible: True
======================================================================
🌐 Démarrage du serveur sur http://localhost:5000
💡 Ctrl+C pour arrêter
======================================================================
```

## 🧪 Tests rapides

### Test 1 : Health Check

```bash
curl http://localhost:5000/health
```

### Test 2 : Tester avec JSON standard

```bash
# Cas 6
curl http://localhost:5000/automation/test/6

# Cas 7
curl http://localhost:5000/automation/test/7

# Cas 8
curl http://localhost:5000/automation/test/8
```

Chaque test crée un fichier `.docx` dans `Cas_automation/output/`

### Test 3 : Envoyer un JSON personnalisé

```bash
curl -X POST http://localhost:5000/automation/cas_6 ^
  -H "Content-Type: application/json" ^
  -d @mon_fichier.json
```

## 📡 Intégration N8N

Configurez un nœud **HTTP Request** dans N8N :

- **Méthode** : `POST`
- **URL** : `http://localhost:5000/automation/cas_6` (ou cas_7, cas_8)
- **Body** : JSON
- **Headers** : `Content-Type: application/json`

Voir `INTEGRATION_N8N.md` pour plus de détails.

## 📂 Structure des endpoints

| Endpoint | Méthode | Description |
|----------|---------|-------------|
| `/health` | GET | État du serveur |
| `/automation/cas_6` | POST | Feuille de révision |
| `/automation/cas_7` | POST | Feuille de couverture |
| `/automation/cas_8` | POST | Programme de travail |
| `/automation/test/<6\|7\|8>` | GET | Test avec JSON standard |

## ✅ Format des réponses

### Succès
```json
{
  "success": true,
  "filename": "REF001_Cas6_20261107_143022.docx",
  "path": "h:\\...\\output\\REF001_Cas6_20261107_143022.docx",
  "cas": 6,
  "type": "Feuille de révision",
  "timestamp": "2026-11-07T14:30:22.123456"
}
```

### Erreur
```json
{
  "success": false,
  "error": "Description de l'erreur",
  "traceback": "..."
}
```

## 🐛 Dépannage

### Problème : Le serveur ne démarre pas

**Erreur** : `No module named 'flask'`

**Solution** :
```bash
conda activate pdf_excel_env
pip install flask flask-cors
```

---

**Erreur** : `ImportError: No module named 'json2word_...'`

**Solution** :
```bash
# Vérifier que les scripts existent
dir "..\Cas_6\json2word_feuilles_revision.py"
dir "..\Cas_7\json2word_feuille_couverture.py"
dir "..\Cas_8\json2word_programme_travail.py"
```

### Problème : `capabilities` est `false`

Exécutez le script de vérification :
```bash
python verifier_imports.py
```

Il vous indiquera quel module pose problème et pourquoi.

### Problème : La génération échoue

1. Vérifiez le format du JSON (doit correspondre au JSON standard)
2. Regardez le champ `traceback` dans la réponse
3. Vérifiez les permissions du dossier `output/`
4. Vérifiez que les templates existent dans `template_standard/`

### Problème : Le fichier généré n'est pas trouvé

Les documents sont créés dans :
```
Cas_automation/output/
```

Vérifiez :
```bash
dir output
```

## 📚 Documentation complète

- **README_SERVEUR.md** : Documentation complète du serveur
- **INTEGRATION_N8N.md** : Guide d'intégration N8N
- **INDEX.md** : Vue d'ensemble du système
- **MISE_A_JOUR.md** : Dernières corrections apportées

## 💡 Conseils

1. **Toujours activer `pdf_excel_env`** avant de démarrer le serveur
2. **Tester avec les endpoints `/automation/test/<cas>`** avant d'intégrer N8N
3. **Consulter `/health`** pour vérifier que tous les cas sont disponibles
4. **Garder le serveur ouvert** pendant que N8N l'utilise
5. **Vérifier `output/`** pour voir les documents générés

## 🎯 Prochaines étapes

1. ✅ Démarrer le serveur
2. ✅ Tester les 3 endpoints
3. ⬜ Configurer N8N
4. ⬜ Intégrer le workflow complet
5. ⬜ Passer au Cas 10

---

**Besoin d'aide ?** Consultez les autres fichiers de documentation ou demandez à l'agent.
