# 📘 Guide d'Utilisation - Workflow Cas 2

## 🎯 Objectif

Le **Workflow Cas 2** automatise complètement le processus suivant :

1. **Appel API** vers le webhook N8N
2. **Collecte** des données JSON depuis `Data_integrale`
3. **Exécution automatique** du skill `audit-procedures-json2word`
4. **Génération** des documents Word professionnels

---

## 📁 Fichiers Créés

```
Modelisation claude skill/
├── api_call_n8n.py              ← Script d'appel API N8N
├── execute_cas2_workflow.py     ← Orchestrateur principal
├── execute_cas2.bat             ← Script batch Windows
├── json2word_audit.py           ← Skill de conversion
└── README_CAS2.md               ← Ce guide
```

---

## 🚀 Démarrage Rapide

### Méthode 1 : Script Batch (Recommandé pour Windows)

```bash
# Double-cliquer sur le fichier ou exécuter :
execute_cas2.bat
```

### Méthode 2 : Script Python

```bash
# Activer l'environnement
conda activate pdf_excel_env

# Exécuter le workflow
python execute_cas2_workflow.py
```

### Méthode 3 : Étape par Étape

```bash
# Étape 1 : Collecter les données depuis N8N
python api_call_n8n.py

# Étape 2 : Exécuter le skill sur les données collectées
python json2word_audit.py "data_json_from_n8n/data_integrale_20261031_*.json" -o sortie_word_cas2
```

---

## ⚙️ Configuration

### 1. URL du Webhook N8N

**Éditer `api_call_n8n.py` (ligne 16) :**

```python
WEBHOOK_URL = "https://VOTRE_URL_N8N/webhook/skill_manuel_audit"
```

**Ou** le script vous demandera l'URL à l'exécution.

### 2. Personnaliser les Paramètres

**Éditer `execute_cas2_workflow.py` (lignes 161-168) :**

```python
skill_command = [
    "python",
    str(SKILL_SCRIPT),
    json_filepath,
    "-o", str(OUTPUT_DIR),
    "--ref", "CAS2",                              # ← Modifier ici
    "--software", "E-Procedure Automation N8N"   # ← Modifier ici
]
```

---

## 📊 Workflow Détaillé

```
┌─────────────────────┐
│  Webhook N8N        │
│  (Données JSON)     │
└──────────┬──────────┘
           │
           │ 1. Requête HTTP POST
           ↓
┌─────────────────────┐
│ api_call_n8n.py     │
│                     │
│ • Appelle N8N       │
│ • Extrait           │
│   Data_integrale    │
│ • Sauvegarde JSON   │
└──────────┬──────────┘
           │
           │ 2. Fichier JSON créé
           │    data_integrale_*.json
           ↓
┌─────────────────────┐
│ json2word_audit.py  │
│ (Skill)             │
│                     │
│ • Parse JSON        │
│ • Pour chaque       │
│   procédure         │
│ • Génère Word       │
└──────────┬──────────┘
           │
           │ 3. Documents générés
           ↓
┌─────────────────────┐
│ sortie_word_cas2/   │
│                     │
│ ✓ CAS2001-*.docx    │
│ ✓ CAS2002-*.docx    │
│ ✓ CAS2003-*.docx    │
└─────────────────────┘
```

---

## 📂 Dossiers Générés

### `data_json_from_n8n/`

Contient les données JSON collectées depuis N8N :

```
data_integrale_20261031_153045.json
data_integrale_20261031_160212.json
```

### `sortie_word_cas2/`

Contient les documents Word générés :

```
CAS2001-Manuel_audit_interne- E-Procedure Automation N8N.docx
CAS2002-Manuel_phase_preparation- E-Procedure Automation N8N.docx
```

---

## 🔍 Exemple de Sortie

```
======================================================================
  🚀 WORKFLOW CAS 2 - Appel API N8N + Exécution Skill
======================================================================

[2026-10-31 15:30:45] [INFO] Script API : api_call_n8n.py
[2026-10-31 15:30:45] [INFO] Script Skill : json2word_audit.py

============================================================
  ÉTAPE 1 - Appel API N8N et Collecte de Data_integrale
============================================================

[2026-10-31 15:30:46] [INFO] Appel API vers https://...
[2026-10-31 15:30:47] [SUCCESS] Réponse reçue (Status: 200)
[2026-10-31 15:30:47] [SUCCESS] Extraction réussie : 3 procédure(s)
[2026-10-31 15:30:47] [SUCCESS] Fichier créé : data_integrale_20261031_153047.json
[2026-10-31 15:30:47] [SUCCESS] ✅ ÉTAPE 1 - Appel API N8N - Succès

[2026-10-31 15:30:47] [SUCCESS] Fichier JSON collecté : data_integrale_20261031_153047.json
[2026-10-31 15:30:47] [INFO] Nombre de procédures à traiter : 3

============================================================
  ÉTAPE 2 - Exécution du Skill audit-procedures-json2word
============================================================

[2026-10-31 15:30:48] [INFO] Traitement de la procédure 1/3
[2026-10-31 15:30:50] [SUCCESS] Document généré : CAS2001-Manuel_audit_interne.docx
[2026-10-31 15:30:50] [INFO] Traitement de la procédure 2/3
[2026-10-31 15:30:52] [SUCCESS] Document généré : CAS2002-Manuel_phase_preparation.docx
[2026-10-31 15:30:52] [INFO] Traitement de la procédure 3/3
[2026-10-31 15:30:54] [SUCCESS] Document généré : CAS2003-Cartographie_risques.docx

======================================================================
  ✅ WORKFLOW CAS 2 TERMINÉ AVEC SUCCÈS
======================================================================

📊 Statistiques :
  • Procédures collectées : 3
  • Fichier JSON source   : data_integrale_20261031_153047.json
  • Documents Word générés : sortie_word_cas2
  • Durée totale          : 9.2 secondes
  • Timestamp             : 2026-10-31 15:30:54

======================================================================
```

---

## ❌ Dépannage

### Erreur : Module 'requests' introuvable

```bash
conda activate pdf_excel_env
pip install requests
```

### Erreur : Connexion au webhook

1. Vérifier l'URL du webhook dans `api_call_n8n.py`
2. Tester manuellement :

```bash
curl https://votre-webhook-n8n.com/webhook/skill_manuel_audit
```

### Erreur : Aucune procédure trouvée

La réponse du webhook ne contient pas `Data_integrale`. Vérifier :

1. La structure de la réponse API
2. Le fichier JSON créé dans `data_json_from_n8n/`

### Erreur : Skill ne génère pas les documents

1. Vérifier que `json2word_audit.py` existe
2. Vérifier les dépendances :

```bash
pip install python-docx
```

---

## 🔧 Tests Unitaires

### Tester l'appel API seul

```bash
python api_call_n8n.py
```

### Tester le skill seul (avec données de test)

```bash
python json2word_audit.py "data_json_from_n8n/data_integrale_test.json" -o test_output
```

### Tester le workflow complet

```bash
python execute_cas2_workflow.py
```

---

## 📞 Support

**Contact :** WhatsApp +225 05 44 13 07 98  
**Sujet :** Workflow Cas 2 - Automation N8N

---

## 📝 Notes Importantes

### Structure Attendue de l'API N8N

Le webhook doit retourner :

```json
[
  {
    "Data_integrale": [
      {
        "Etape mission - Manuel des procedures": [
          {"table 1": {...}},
          {"table 2": [...]}
        ]
      }
    ]
  }
]
```

### Références Automatiques

Les documents générés utilisent automatiquement :
- Préfixe : `CAS2`
- Numérotation : `001`, `002`, `003`, etc.
- Logiciel : `E-Procedure Automation N8N`

---

**Version :** 1.0.0  
**Date :** 31 octobre 2026  
**Statut :** ✅ Prêt à l'emploi
