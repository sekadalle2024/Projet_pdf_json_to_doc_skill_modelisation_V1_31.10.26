# Cas 3 - Manuel Audit (API N8N)

## 📋 Description

Conversion automatisée des **manuels d'audit interne** récupérés depuis un workflow **N8N** vers des documents Word au format E-procedure.

## ✅ Statut : OPÉRATIONNEL

Le skill Cas 3 est **100% fonctionnel** et prêt pour la production.

## 🎯 Objectif

Automatiser la génération de documents Word professionnels pour les manuels d'audit interne, en récupérant les données depuis une API N8N dédiée.

## 📦 Fichiers Disponibles

### Scripts Principaux
- ✅ `audit-manuel-json2word.skill.md` - Documentation complète du skill
- ✅ `execute_cas3_production.py` - Orchestrateur principal (workflow complet)
- ✅ `json2word_audit.py` - Script de conversion JSON → Word (réutilisé du Cas 2)
- ✅ `execute_cas3.bat` - Script batch Windows pour exécution simplifiée

### Documentation
- ✅ `GUIDE_CONFIGURATION_N8N.md` - Guide détaillé de configuration N8N
- ✅ `README.md` - Ce fichier

## 🚀 Démarrage Rapide

### 1. Installation des Dépendances

```bash
# Avec Conda (recommandé)
conda activate pdf_excel_env
pip install python-docx requests

# Ou avec pip standard
pip install python-docx requests
```

### 2. Configuration N8N

1. **Démarrer N8N** :
   ```bash
   n8n start
   ```

2. **Créer le workflow** : `skill_manuel_audit_cas3`

3. **Configurer les nœuds** :
   - **Webhook** : `/webhook/skill_manuel_audit_cas3`
   - **Edit Fields** : Champ `Data_integrale` (Array)
   - **Respond to Webhook** : Retourne le JSON

4. **Activer le workflow** dans l'interface N8N

📖 Voir `GUIDE_CONFIGURATION_N8N.md` pour les détails complets.

### 3. Exécution

```bash
# Méthode 1 : Script Python
python execute_cas3_production.py

# Méthode 2 : Batch Windows
execute_cas3.bat
```

## 📊 Workflow Complet

```
┌──────────────────┐
│   N8N Workflow   │  ← Configuration : webhook skill_manuel_audit_cas3
│   localhost:5678 │     Champ : Data_integrale (Array de manuels)
└────────┬─────────┘
         │ HTTP POST
         ↓
┌──────────────────────────────┐
│ execute_cas3_production.py   │
│                              │
│ 1. call_n8n_api()            │  ← Requête POST + extraction JSON
│ 2. extract_data_integrale()  │  ← Parse Data_integrale
│ 3. process_procedures()      │  ← Boucle sur chaque manuel
│    └─> json2word_audit.py    │  ← Conversion individuelle
└────────┬─────────────────────┘
         │
         ↓
┌──────────────────────────────┐
│ Documents Word Générés       │
│ sortie_word_cas3/            │
│                              │
│ • Manuel_audit_*_V1_*.docx   │
│ • Manuel_phase_*_V1_*.docx   │
└──────────────────────────────┘
```

## 📝 Format de Sortie

### Nom des Fichiers

**Format** : `[Etape de mission] ― [Logiciel]_V1_HH-MM-SS_DD.MM.YY.docx`

**Exemples** :
- `Manuel_audit_interne ― Logiciel automatisé E-audit pro_V1_14-15-10_31.10.26.docx`
- `Manuel_phase_preparation ― Logiciel automatisé E-audit pro_V1_14-16-22_31.10.26.docx`

### Caractéristiques des Documents

- ✅ Format A4 **paysage**
- ✅ Marges : 0,5" (1,27 cm)
- ✅ En-tête : `[Logiciel] - [Étape de mission]` (fond bordeaux #7B1E3A)
- ✅ Pied de page : Contact WhatsApp centré
- ✅ Tables avec bordures visibles (colonnes) et invisibles (lignes)
- ✅ Ligne vide après chaque enregistrement

## 🔧 Configuration

### URL du Webhook

**Par défaut** : `http://localhost:5678/webhook/skill_manuel_audit_cas3`

**Modifier** dans `execute_cas3_production.py` :
```python
WEBHOOK_URL = "http://localhost:5678/webhook/skill_manuel_audit_cas3"
```

### Dossiers de Sortie

- `sortie_word_cas3/` - Documents Word générés
- `temp_procedures_cas3/` - Fichiers JSON temporaires
- `data_json_from_n8n_cas3/` - Réponses API sauvegardées

### Timeout

**Par défaut** : 30 secondes

**Modifier** dans `execute_cas3_production.py` :
```python
TIMEOUT = 60  # Augmenter si nécessaire
```

## 🧪 Tests

### Test 1 : Connexion N8N

```bash
curl -X POST http://localhost:5678/webhook/skill_manuel_audit_cas3 \
     -H "Content-Type: application/json" \
     -d '{}'
```

### Test 2 : Workflow Complet

```bash
python execute_cas3_production.py
```

**Vérifier les sorties** :
- Console : Logs détaillés du workflow
- `sortie_word_cas3/` : Documents Word générés
- `data_json_from_n8n_cas3/` : Réponses API

## 📈 Fonctionnalités

### ✅ Implémenté

- ✅ Appel API N8N automatique
- ✅ Extraction de `Data_integrale`
- ✅ Batch processing (plusieurs manuels)
- ✅ Conversion JSON → Word
- ✅ Horodatage unique (V1_HH-MM-SS_DD.MM.YY)
- ✅ Logs détaillés
- ✅ Gestion d'erreurs complète
- ✅ Sauvegarde des données intermédiaires
- ✅ Statistiques de conversion

### 🔜 Améliorations Futures

- ⏳ Interface graphique (GUI)
- ⏳ Conversion PDF automatique
- ⏳ Notification par email
- ⏳ Support HTTPS avec authentification

## 🐛 Dépannage

### Erreur : Connection Refused

**Cause** : N8N n'est pas démarré

**Solution** :
```bash
n8n start
```

### Erreur : Data_integrale absent

**Cause** : Workflow N8N mal configuré

**Solution** :
- Vérifier le nœud "Edit Fields"
- Vérifier que `Data_integrale` est un Array
- Consulter `GUIDE_CONFIGURATION_N8N.md`

### Erreur : ModuleNotFoundError

**Cause** : Dépendances manquantes

**Solution** :
```bash
pip install python-docx requests
```

### Erreur : Timeout

**Cause** : N8N trop lent

**Solution** :
- Augmenter `TIMEOUT` dans le script
- Optimiser le workflow N8N

## 📚 Documentation

- `audit-manuel-json2word.skill.md` - Documentation complète du skill
- `GUIDE_CONFIGURATION_N8N.md` - Configuration N8N détaillée
- `README.md` - Ce fichier

## 🔗 Liens

- [Documentation N8N](https://docs.n8n.io/)
- [Python-docx](https://python-docx.readthedocs.io/)
- [Requests](https://requests.readthedocs.io/)

## 📞 Contact

**Support** : Whatsapp + 225 05 44 13 07 98

## 📅 Version

**Version actuelle** : 1.0.0 (31 octobre 2026)

**Changelog** :
- ✨ Création initiale du skill Cas 3
- ✅ Support complet du workflow N8N
- ✅ Réutilisation du script `json2word_audit.py`
- ✅ Horodatage au format V1_HH-MM-SS_DD.MM.YY
- ✅ Documentation complète
