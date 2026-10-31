# Guide de Configuration N8N - Cas 3

## Vue d'ensemble

Ce guide explique comment configurer le workflow N8N pour le **Cas 3** (Manuel Audit via API).

## Prérequis

- ✅ N8N installé et fonctionnel
- ✅ Port 5678 disponible (défaut N8N)
- ✅ Python 3.9+ avec `requests` et `python-docx`

## Architecture du Workflow

```
┌─────────────────┐
│  Webhook Node   │  ← Entrée : POST http://localhost:5678/webhook/skill_manuel_audit_cas3
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│ Edit Fields     │  ← Configure Data_integrale (Array de manuels)
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│ Respond to      │  ← Retourne le JSON avec Data_integrale
│ Webhook         │
└─────────────────┘
```

## Configuration Détaillée

### 1. Créer le Workflow

1. **Ouvrir N8N** : `http://localhost:5678`
2. **Nouveau Workflow** : Cliquer sur "New Workflow"
3. **Nom du Workflow** : `skill_manuel_audit_cas3`

### 2. Nœud Webhook (Entrée)

**Configuration** :
- **Node** : Webhook
- **Webhook Path** : `skill_manuel_audit_cas3`
- **Method** : POST
- **Response Mode** : "Using 'Respond to Webhook' Node"

**URL finale** : `http://localhost:5678/webhook/skill_manuel_audit_cas3`

### 3. Nœud Edit Fields (Transformation)

**Configuration** :
- **Node** : Edit Fields (Set)
- **Mode** : "Define Below"
- **Operation** : "Set"

**Champ à configurer** :

| Field Name | Field Type | Field Value |
|------------|-----------|-------------|
| `Data_integrale` | Array | `{{ $json.manuels }}` ou votre source de données |

**Exemple de structure attendue** :

```json
{
  "Data_integrale": [
    {
      "Etape mission - Manuel des procedures": [
        {
          "table 1": {
            "Etape de mission": "Manuel audit interne - Phase de préparation",
            "Document": "Manuel méthodologique d'audit interne",
            "Processus": "Audit interne - Identification et évaluation des risques",
            "Reference": "MAN-AUD-METH-RISK-02",
            "Version": "V3.2"
          }
        },
        {
          "table 2": [
            {
              "Étape méthodologique": "Cadrage initial du périmètre",
              "Acteur audit": "Directeur de l'Audit Interne",
              "Traitement et diligences d'audit": "- Définit le périmètre\n- Délimite les frontières",
              "Document probant": "Lettre de cadrage, Note de stratégie",
              "Norme IIA / CRIPP": "Norme 13.3 Objectifs et périmètre",
              "Extrait de la norme": "Les auditeurs internes doivent déterminer..."
            }
          ]
        }
      ]
    }
  ]
}
```

### 4. Nœud Respond to Webhook (Sortie)

**Configuration** :
- **Node** : Respond to Webhook
- **Respond With** : "Using 'Respond to Webhook' Node"
- **Response Body** : `{{ $json }}`
- **Status Code** : `200`

## Exemple de Configuration Complète

### Option A : Données Statiques (Test)

**Nœud Edit Fields** :

```javascript
{
  "Data_integrale": [
    {
      "Etape mission - Manuel audit interne": [
        {
          "table 1": {
            "Etape de mission": "Manuel audit interne - Phase de préparation",
            "Document": "Manuel méthodologique d'audit interne",
            "Processus": "Audit interne - Méthodologie",
            "Cycle d'activité": "Conduite des Missions",
            "Secteur d'activité": "Banque UMOA",
            "Norme": {
              "Norme 1": "Norme 1.1 Honnêteté professionnelle",
              "Norme 2": "Norme 2.1 Objectivité",
              "Norme 3": "Norme 4.2 Conscience professionnelle"
            },
            "Reference": "MAN-AUD-PREP-01",
            "Version": "V1.0",
            "Etablissement": "Afrika Group Holdings",
            "Approbation": "Comité d'Audit"
          }
        },
        {
          "table 2": [
            {
              "Étape méthodologique": "Cadrage du périmètre",
              "Acteur audit": "Directeur de l'Audit Interne",
              "Traitement et diligences d'audit": "- Définir le périmètre d'analyse\n- Délimiter les frontières\n- Identifier les objectifs stratégiques",
              "Document probant": "Lettre de cadrage, Note de stratégie, Déclaration des objectifs",
              "Norme IIA / CRIPP": "Norme 13.3 Objectifs et périmètre",
              "Extrait de la norme": "Les auditeurs internes doivent déterminer les objectifs de la mission d'audit."
            },
            {
              "Étape méthodologique": "Identification des risques",
              "Acteur audit": "Chef de mission",
              "Traitement et diligences d'audit": "- Recenser les risques majeurs\n- Évaluer leur criticité\n- Prioriser les travaux",
              "Document probant": "Matrice des risques, Cartographie",
              "Norme IIA / CRIPP": "Norme 14.1 Évaluation des risques",
              "Extrait de la norme": "L'évaluation des risques doit couvrir l'ensemble du périmètre."
            }
          ]
        }
      ]
    }
  ]
}
```

### Option B : Données Dynamiques (Production)

**Nœud HTTP Request** (avant Edit Fields) :

```
URL : https://votre-api.com/manuels
Method : GET
Headers : Authorization: Bearer YOUR_TOKEN
```

**Nœud Edit Fields** :

```javascript
{
  "Data_integrale": {{ $json.body.manuels }}
}
```

## Test du Workflow

### Test 1 : Via N8N Interface

1. **Activer le workflow** : Toggle "Active" en haut à droite
2. **Cliquer sur "Execute Workflow"**
3. **Vérifier la sortie** du nœud "Respond to Webhook"

### Test 2 : Via cURL

```bash
curl -X POST http://localhost:5678/webhook/skill_manuel_audit_cas3 \
     -H "Content-Type: application/json" \
     -d '{}'
```

**Réponse attendue** :

```json
{
  "Data_integrale": [
    { /* manuel 1 */ },
    { /* manuel 2 */ }
  ]
}
```

### Test 3 : Via Python

```python
import requests

url = "http://localhost:5678/webhook/skill_manuel_audit_cas3"
response = requests.post(url, json={})

print(response.json())
```

## Exécution du Workflow Complet

Une fois N8N configuré :

```bash
# Méthode 1 : Script Python
python execute_cas3_production.py

# Méthode 2 : Batch Windows
execute_cas3.bat
```

## Troubleshooting

### Erreur : Connection Refused

**Cause** : N8N n'est pas démarré

**Solution** :
```bash
n8n start
```

### Erreur : Data_integrale absent

**Cause** : Nœud Edit Fields mal configuré

**Solution** :
- Vérifier que le champ `Data_integrale` est bien défini
- Vérifier la structure du JSON source

### Erreur : Timeout

**Cause** : Le workflow est trop lent

**Solution** :
- Augmenter `TIMEOUT` dans `execute_cas3_production.py`
- Optimiser le workflow N8N (moins de nœuds)

### Erreur : Structure JSON non reconnue

**Cause** : La structure ne correspond pas au format attendu

**Solution** :
- Vérifier que `Data_integrale` est un **Array**
- Vérifier que chaque élément contient `table 1` et `table 2`

## Monitoring

### Vérifier les logs N8N

1. Ouvrir N8N : `http://localhost:5678`
2. Aller dans "Executions"
3. Consulter les exécutions récentes

### Vérifier les données sauvegardées

```bash
# Réponses API
ls data_json_from_n8n_cas3/

# JSON temporaires
ls temp_procedures_cas3/

# Documents générés
ls sortie_word_cas3/
```

## Configuration Avancée

### Utiliser un Port Différent

**Dans N8N** :
```bash
N8N_PORT=8080 n8n start
```

**Dans le script Python** (`execute_cas3_production.py`) :
```python
WEBHOOK_URL = "http://localhost:8080/webhook/skill_manuel_audit_cas3"
```

### Ajouter une Authentification

**Nœud Webhook** :
- **Authentication** : Basic Auth
- **User** : `votre_user`
- **Password** : `votre_password`

**Script Python** :
```python
response = requests.post(
    url,
    json={},
    auth=("votre_user", "votre_password")
)
```

### Intégration avec Base de Données

**Ajouter un nœud Database** avant Edit Fields :

```
[Webhook] → [PostgreSQL/MySQL] → [Edit Fields] → [Respond to Webhook]
```

**Requête SQL** :
```sql
SELECT * FROM manuels_audit WHERE statut = 'valide'
```

## Bonnes Pratiques

1. ✅ **Activer le workflow** avant de lancer le script Python
2. ✅ **Tester avec des données simples** avant la production
3. ✅ **Sauvegarder les réponses API** pour debug
4. ✅ **Versionner le workflow N8N** (export JSON)
5. ✅ **Monitorer les exécutions** dans l'interface N8N

## Ressources

- [Documentation N8N](https://docs.n8n.io/)
- [Webhook Node](https://docs.n8n.io/integrations/core-nodes/n8n-nodes-base.webhook/)
- [Edit Fields Node](https://docs.n8n.io/integrations/core-nodes/n8n-nodes-base.set/)

## Contact

Pour toute question : Whatsapp + 225 05 44 13 07 98
