# ⚡ Mise à jour du serveur - 7 novembre 2026

## 🔧 Corrections apportées

### Problème identifié
Les scripts `build_docx.py` n'existaient pas dans les dossiers Cas. Le serveur utilisait des chemins incorrects.

### Solution implémentée
Le serveur a été **complètement réécrit** pour utiliser les vrais scripts existants :

| Cas | Script réel | Fonction |
|-----|------------|----------|
| **Cas 6** | `Cas_6/json2word_feuilles_revision.py` | `main(json_path, output_dir)` |
| **Cas 7** | `Cas_7/json2word_feuille_couverture.py` | `main(json_path, output_dir)` |
| **Cas 8** | `Cas_8/json2word_programme_travail.py` | `main(json_path, output_dir)` |

## ✅ Changements dans `server_automation.py`

### Avant
```python
# Chemins incorrects
sys.path.insert(0, str(Path(...) / "Cas_6" / "audit-etap-mission-feuille-revision" / "scripts"))

# Fonctions inexistantes
from build_docx import generate_document_cas_6
```

### Après
```python
# Chemins corrects
sys.path.insert(0, str(BASE_DIR / "Cas_6"))
sys.path.insert(0, str(BASE_DIR / "Cas_7"))
sys.path.insert(0, str(BASE_DIR / "Cas_8"))

# Vraies fonctions
from json2word_feuilles_revision import main as generate_cas_6
from json2word_feuille_couverture import main as generate_cas_7
from json2word_programme_travail import main as generate_cas_8
```

## 📋 Fonctionnement des endpoints

Chaque endpoint :

1. **Reçoit** un JSON via POST
2. **Crée** un fichier temporaire `.json` dans `output/`
3. **Appelle** la fonction `main()` du script Cas correspondant
4. **Nettoie** le fichier temporaire
5. **Retourne** les infos du document Word généré

### Exemple Cas 8

```python
@app.route('/automation/cas_8', methods=['POST'])
def automation_cas_8():
    # 1. Récupérer le JSON
    data = request.get_json()
    
    # 2. Créer un fichier temporaire
    with tempfile.NamedTemporaryFile(...) as tmp:
        json.dump(data, tmp)
        temp_json_path = tmp.name
    
    # 3. Appeler le script Cas 8
    success = generate_cas_8(temp_json_path, str(OUTPUT_DIR))
    
    # 4. Nettoyer
    Path(temp_json_path).unlink()
    
    # 5. Retourner le résultat
    return jsonify({
        'success': True,
        'filename': output_file.name,
        'path': str(output_file)
    })
```

## 🧪 Tests à effectuer

### 1. Vérifier que les modules s'importent

```bash
conda activate pdf_excel_env
python -c "from json2word_feuilles_revision import main; print('Cas 6 OK')"
python -c "from json2word_feuille_couverture import main; print('Cas 7 OK')"
python -c "from json2word_programme_travail import main; print('Cas 8 OK')"
```

### 2. Démarrer le serveur

```bash
cd "h:\Projet_pdf_excel\Modelisation claude skill\Cas_automation"
conda activate pdf_excel_env
python server_automation.py
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

### 3. Tester le health check

```bash
curl http://localhost:5000/health
```

**Réponse attendue :**
```json
{
  "status": "ok",
  "timestamp": "2026-11-07T...",
  "capabilities": {
    "cas_6": true,
    "cas_7": true,
    "cas_8": true
  },
  "paths": {
    "output": "h:\\Projet_pdf_excel\\Modelisation claude skill\\Cas_automation\\output",
    "json_standard": "h:\\Projet_pdf_excel\\Modelisation claude skill\\Cas_automation\\json standard"
  }
}
```

### 4. Tester avec JSON standard

```bash
# Test Cas 6
curl http://localhost:5000/automation/test/6

# Test Cas 7
curl http://localhost:5000/automation/test/7

# Test Cas 8
curl http://localhost:5000/automation/test/8
```

Chaque test devrait créer un fichier `.docx` dans le dossier `output/`.

## 🐛 Diagnostics

### Si le serveur ne démarre pas

**Erreur** : `ImportError: No module named 'json2word_...'`

**Solution** :
```bash
# Vérifier que vous êtes dans le bon environnement
conda activate pdf_excel_env

# Vérifier que les scripts existent
ls "../Cas_6/json2word_feuilles_revision.py"
ls "../Cas_7/json2word_feuille_couverture.py"
ls "../Cas_8/json2word_programme_travail.py"
```

### Si `capabilities` est `false`

**Problème** : Le module n'a pas pu s'importer

**Actions** :
1. Lire les logs au démarrage du serveur (lignes `⚠️ Cas X non disponible`)
2. Vérifier les dépendances du script (ex: Cas 8 utilise Cas 2)
3. S'assurer que tous les fichiers `.skill` et dépendances sont présents

### Si la génération échoue

**Erreur** : `"success": false, "error": "..."`

**Actions** :
1. Regarder le champ `traceback` dans la réponse
2. Vérifier le format du JSON (doit correspondre au standard)
3. Vérifier les permissions du dossier `output/`
4. Vérifier que les templates existent dans `template_standard/`

## 📚 Documentation mise à jour

- ✅ **server_automation.py** : Réécrit avec vrais scripts
- ⏳ **README_SERVEUR.md** : À mettre à jour (structure dossiers)
- ✅ **INTEGRATION_N8N.md** : Reste valide
- ✅ **INDEX.md** : Reste valide
- ⏳ **test_server.py** : À mettre à jour (appels HTTP)

## 🚀 Prochaines étapes

1. **Tester** le serveur avec les 3 cas
2. **Vérifier** que les documents Word sont bien générés
3. **Configurer** N8N pour appeler les endpoints
4. **Passer au Cas 10** une fois que tout fonctionne

## 📞 Support

Si vous rencontrez des problèmes :
1. Vérifiez cette page
2. Consultez `README_SERVEUR.md`
3. Consultez `INTEGRATION_N8N.md`
4. Demandez à l'agent d'investiguer
