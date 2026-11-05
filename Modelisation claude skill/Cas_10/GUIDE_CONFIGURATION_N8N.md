# 🔧 Guide de Configuration N8N - Cas 10

**Version:** 1.0.0  
**Date:** 5 novembre 2026  
**Auteur:** Expert Python & Automation

---

## 📋 Table des Matières

1. [Introduction](#introduction)
2. [Prérequis](#prérequis)
3. [Installation N8N](#installation-n8n)
4. [Configuration du Workflow](#configuration-du-workflow)
5. [Structure des données](#structure-des-données)
6. [Tests](#tests)
7. [Dépannage](#dépannage)

---

## 🎯 Introduction

Ce guide vous accompagne dans la configuration complète de N8N pour le **Cas 10 - Orchestrateur Multi-Workflow**.

### Objectif

Créer un workflow N8N qui :
1. Reçoit des requêtes via webhook
2. Retourne un JSON contenant `Data_integrale` (Array multi-types)
3. Permet à l'orchestrateur Cas 10 de traiter automatiquement différents types d'étapes

---

## ✅ Prérequis

### Logiciels requis

- **Node.js** : Version 18+ recommandée
- **npm** : Inclus avec Node.js
- **N8N** : Version 1.0+

### Vérifications

```bash
# Vérifier Node.js
node --version
# Attendu: v18.x.x ou supérieur

# Vérifier npm
npm --version
# Attendu: 9.x.x ou supérieur
```

---

## 📥 Installation N8N

### Méthode 1 : Installation globale (Recommandé)

```bash
# Installation
npm install n8n -g

# Vérification
n8n --version
```

### Méthode 2 : npx (Sans installation)

```bash
npx n8n
```

### Démarrage de N8N

```bash
# Démarrage standard
n8n start

# Avec tunnel public (optionnel)
n8n start --tunnel
```

**URL d'accès:** http://localhost:5678

---

## 🔧 Configuration du Workflow

### Étape 1 : Créer un nouveau workflow

1. Accédez à N8N : http://localhost:5678
2. Cliquez sur **"+ Créer un workflow"**
3. Nommez le workflow : **"Cas 10 - Multi Workflow"**

### Étape 2 : Ajouter le nœud Webhook

1. Cliquez sur **"+"** pour ajouter un nœud
2. Recherchez et sélectionnez **"Webhook"**
3. Configurez :

```
HTTP Method: POST
Path: skill_cas10_multi
Response Mode: Response Node
```

**URL générée:** `http://localhost:5678/webhook/skill_cas10_multi`

### Étape 3 : Ajouter le nœud Edit Fields

1. Connectez le Webhook à un nœud **"Edit Fields"**
2. Configuration optionnelle : Formatage des données

### Étape 4 : Ajouter le nœud Respond to Webhook

1. Connectez Edit Fields à **"Respond to Webhook"**
2. Configurez :

```
Respond With: JSON
Response Body: {{ $json }}
```

### Étape 5 : Configuration avancée (Optionnelle)

#### Ajout de données de test

Dans le nœud **Edit Fields**, configurez les données de test :

```json
{
  "Data_integrale": [
    {
      "table 1": {
        "Etape de mission": "FRAP",
        "Document": "Feuille de Révélation et d'Analyse de Problème - Test Trésorerie",
        "Processus": "Gestion de la trésorerie",
        "Secteur d'activité": "Banque UMOA",
        "Reference": "FRAP-TRE-001"
      },
      "table 2": [
        {
          "Problème": "Absence de rapprochements bancaires",
          "Constat": "Aucun rapprochement sur 6 mois",
          "Cause": "Manque de ressources",
          "Conséquence": "Risque de fraude élevé",
          "Recommandation": "Mettre en place un processus mensuel"
        }
      ]
    },
    {
      "table 1": {
        "Etape de mission": "Feuille de révision",
        "Document": "Test de révision des comptes - Caisse",
        "Processus": "Inventaire de caisse",
        "Secteur d'activité": "Banque UMOA",
        "Reference": "REV-CAI-001"
      },
      "table 2": [
        {
          "N° Test": "TC-001",
          "Objectif de contrôle": "Exhaustivité des inventaires",
          "Nature du contrôle": "Substantif",
          "Procédure de test": "Vérification des PV d'inventaire",
          "Taille échantillon": "10 PV",
          "Résultat observé": "2 PV manquants",
          "Écart identifié": "20% de non-conformité",
          "Conclusion": "Risque modéré",
          "Action recommandée": "Renforcer le suivi"
        }
      ]
    },
    {
      "table 1": {
        "Etape de mission": "Cartographie des risques",
        "Document": "Cartographie - Processus Trésorerie",
        "Processus": "Gestion des flux de trésorerie",
        "Secteur d'activité": "Banque UMOA",
        "Reference": "CARTO-TRE-001"
      },
      "table 2": [
        {
          "Processus": "Rapprochements bancaires",
          "Risque": "Erreurs de saisie non détectées",
          "Impact": "Élevé",
          "Probabilité": "Moyenne",
          "Criticité": "Haute",
          "Contrôle": "Double vérification mensuelle"
        }
      ]
    }
  ]
}
```

### Étape 6 : Sauvegarder et activer

1. Cliquez sur **"Enregistrer"** (en haut à droite)
2. Activez le workflow avec le toggle **"Actif"**

---

## 📦 Structure des données

### Format attendu par l'orchestrateur

```json
[
  {
    "Data_integrale": [
      {
        "table 1": {
          "Etape de mission": "<Type d'étape>",
          "Document": "<Nom du document>",
          "Processus": "<Processus audité>",
          ...
        },
        "table 2": [
          {
            "<Colonne1>": "<Valeur1>",
            "<Colonne2>": "<Valeur2>",
            ...
          }
        ]
      }
    ]
  }
]
```

### Champs obligatoires

#### `table 1` (Métadonnées)

| Champ | Type | Obligatoire | Description |
|-------|------|-------------|-------------|
| `Etape de mission` | String | **Oui** | Type d'étape pour la détection du cas |
| `Document` | String | Oui | Titre du document |
| `Processus` | String | Oui | Processus audité |
| `Secteur d'activité` | String | Non | Secteur d'activité |
| `Reference` | String | Non | Référence du document |

#### `table 2` (Données)

Les colonnes de `table 2` varient selon le type d'étape :

**Cas 5 (FRAP):**
- Problème, Constat, Cause, Conséquence, Recommandation

**Cas 6 (Révision):**
- N° Test, Objectif, Nature, Procédure, Échantillon, Résultat, Écart, Conclusion, Action

**Cas 7 (Couverture):**
- Processus, Contrôle, Modèle de test, Résultats

**Cas 8 (Modèles standard):**
- Variable selon le modèle spécifique

---

## 🧪 Tests

### Test 1 : Webhook accessible

```powershell
# PowerShell
Invoke-RestMethod -Uri "http://localhost:5678/webhook/skill_cas10_multi" -Method POST -Body '{}' -ContentType "application/json"
```

```bash
# cURL (Linux/Mac)
curl -X POST http://localhost:5678/webhook/skill_cas10_multi \
  -H "Content-Type: application/json" \
  -d '{}'
```

**Résultat attendu:** Réponse JSON avec `Data_integrale`

### Test 2 : Depuis Python

```python
import requests

url = "http://localhost:5678/webhook/skill_cas10_multi"
response = requests.post(url, json={})

print(f"Status: {response.status_code}")
print(f"Data: {response.json()}")
```

### Test 3 : Avec l'orchestrateur

```bash
conda activate pdf_excel_env
python execute_cas10_orchestrator.py
```

---

## 🔍 Dépannage

### Problème 1 : N8N ne démarre pas

**Symptômes:**
```
Error: Port 5678 is already in use
```

**Solutions:**

```bash
# 1. Trouver le processus
netstat -ano | findstr :5678

# 2. Tuer le processus (Windows)
taskkill /PID <PID> /F

# 3. Redémarrer N8N
n8n start
```

### Problème 2 : Webhook non accessible

**Symptômes:**
```
Connection refused
```

**Solutions:**

1. Vérifier que N8N est démarré
2. Vérifier l'URL : `http://localhost:5678`
3. Vérifier le chemin du webhook : `/webhook/skill_cas10_multi`
4. Vérifier que le workflow est **activé**

### Problème 3 : Réponse vide

**Symptômes:**
```json
{}
```

**Solutions:**

1. Vérifier la configuration du nœud **Edit Fields**
2. Ajouter les données de test
3. Vérifier le nœud **Respond to Webhook** :
   - Response Body : `{{ $json }}`

### Problème 4 : Erreur 404

**Symptômes:**
```
404 Not Found
```

**Solutions:**

1. Vérifier que le workflow est **sauvegardé**
2. Vérifier que le workflow est **activé**
3. Vérifier le chemin : `/webhook/skill_cas10_multi`

---

## 📊 Monitoring

### Logs N8N

```bash
# Démarrer avec logs
n8n start --log-level debug
```

### Historique d'exécution

1. Dans N8N, cliquez sur **"Executions"**
2. Consultez l'historique des exécutions
3. Cliquez sur une exécution pour voir les détails

### Métriques

- **Temps de réponse** : ~100-300ms
- **Taux de succès** : 100% attendu
- **Throughput** : ~10-50 requêtes/seconde

---

## 🚀 Optimisations

### Performance

1. **Cache** : Activer le cache N8N
2. **Timeout** : Augmenter si traitement long
3. **Retry** : Configurer les tentatives automatiques

### Sécurité

1. **Authentication** : Ajouter une clé API
2. **HTTPS** : Utiliser un reverse proxy (nginx)
3. **Rate limiting** : Limiter les requêtes

### Exemple avec authentication

```javascript
// Dans le nœud Edit Fields
if (!$input.headers.authorization || 
    $input.headers.authorization !== 'Bearer MA_CLE_SECRETE') {
  throw new Error('Unauthorized');
}

return $input.item;
```

---

## 📞 Support

### Contact

**WhatsApp:** +225 05 44 13 07 98

### Ressources

- **Documentation N8N:** https://docs.n8n.io
- **Forum N8N:** https://community.n8n.io
- **Documentation Cas 10:** `README.md`

---

## ✅ Checklist de production

- [ ] N8N installé et démarré
- [ ] Workflow créé et configuré
- [ ] Webhook activé (`/webhook/skill_cas10_multi`)
- [ ] Données de test ajoutées
- [ ] Tests manuels réussis
- [ ] Orchestrateur Cas 10 testé
- [ ] Logs vérifiés
- [ ] Documentation lue

---

**© 2026 - Configuration N8N pour le Cas 10**  
**Automatisez vos activités d'audit, risques et contrôles**
