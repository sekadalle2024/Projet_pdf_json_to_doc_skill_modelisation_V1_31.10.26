# Guide de Configuration N8N - Cas 6 : Feuilles de Révision

Ce guide détaille la configuration complète du workflow N8N pour le Cas 6 (Feuilles de Révision d'Audit).

## 📋 Pré-requis

- N8N installé et fonctionnel
- Port 5678 disponible (port par défaut de N8N)
- Données de feuilles de révision formatées en JSON

## 🚀 Installation de N8N

### Option 1 : Installation Globale (Recommandé)

```bash
npm install -g n8n
```

### Option 2 : Installation avec npx

```bash
npx n8n
```

### Démarrage de N8N

```bash
n8n start
```

N8N sera accessible sur : `http://localhost:5678`

## 🔧 Configuration du Workflow

### Étape 1 : Créer un Nouveau Workflow

1. Ouvrez N8N dans votre navigateur : `http://localhost:5678`
2. Cliquez sur **"New workflow"**
3. Nommez le workflow : `skill_feuilles_revision_cas6`

### Étape 2 : Ajouter le Nœud Webhook

1. **Cliquer sur le bouton "+" pour ajouter un nœud**
2. **Rechercher et sélectionner : "Webhook"**
3. **Configurer le Webhook :**

```yaml
Node Name: Webhook Feuilles Révision
HTTP Method: POST
Path: skill_feuilles_revision_cas6
Authentication: None
Response Mode: When Last Node Finishes
Response Code: 200
```

**URL complète du webhook** : `http://localhost:5678/webhook/skill_feuilles_revision_cas6`

### Étape 3 : Ajouter le Nœud "Edit Fields"

1. **Connecter le Webhook au nœud "Edit Fields"**
2. **Cliquer sur le bouton "+" après le Webhook**
3. **Rechercher et sélectionner : "Edit Fields"**
4. **Configurer Edit Fields :**

```yaml
Node Name: Format Data_integrale
Mode: Define Below

Fields to Set:
  Field 1:
    Name: Data_integrale
    Type: Array
    Value: [Votre tableau JSON de feuilles de révision]
```

**📊 Exemple de structure Data_integrale :**

```json
{
  "Data_integrale": [
    {
      "Feuille de révision - Test des contrôles": [
        {
          "table 1": {
            "Etape de mission": "Feuille de révision - Tests des contrôles clés",
            "Document": "Feuille de test et de pointage des contrôles",
            "Processus": "Audit interne - Phase de réalisation",
            "Cycle d'activité": "Vérification de l'efficacité des contrôles",
            "Secteur d'activité": "Banque, Industrie et Assurance UMOA",
            "Critère d'audit": "Efficacité des contrôles préventifs et détectifs",
            "Reference": "FDR-AUD-TEST-CTRL-05",
            "Version": "V2.1 - Tests de contrôles renforcés",
            "Etablissement": "Afrika Group Holdings",
            "Auditeur responsable": "Chef de mission / Auditeur senior"
          }
        },
        {
          "table 2": [
            {
              "N° Test": "T-001",
              "Objectif de contrôle": "Séparer les fonctions d'engagement et de validation",
              "Nature du contrôle": "Préventif - Séparation des tâches",
              "Procédure de test": "- Examiner matrice des habilitations\n- Vérifier l'absence de cumul de rôles\n- Tester 15 opérations d'engagement",
              "Taille échantillon": "15 engagements / 120 total (12,5%)",
              "Résultat observé": "14/15 conformes - 1 anomalie détectée",
              "Écart identifié": "1 opérateur cumule engagement et validation (mission temporaire)",
              "Conclusion": "Contrôle efficace avec réserve mineure",
              "Action recommandée": "Régulariser la situation temporaire sous 30 jours"
            },
            {
              "N° Test": "T-002",
              "Objectif de contrôle": "Valider les limites d'autorisation par niveau",
              "Nature du contrôle": "Préventif - Limites d'autorisation",
              "Procédure de test": "- Extraire 20 transactions > seuil\n- Vérifier signatures conformes\n- Contrôler traçabilité des approbations",
              "Taille échantillon": "20 transactions / 85 total (23,5%)",
              "Résultat observé": "20/20 conformes - Aucune anomalie",
              "Écart identifié": "Aucun écart détecté",
              "Conclusion": "Contrôle efficace et bien appliqué",
              "Action recommandée": "Maintenir le dispositif actuel"
            }
          ]
        }
      ]
    }
  ]
}
```

### Étape 4 : Ajouter le Nœud "Respond to Webhook"

1. **Connecter Edit Fields à "Respond to Webhook"**
2. **Cliquer sur le bouton "+" après Edit Fields**
3. **Rechercher et sélectionner : "Respond to Webhook"**
4. **Configurer :**

```yaml
Node Name: Respond
Respond With: Using 'Respond to Webhook' Node
Response Body: {{ $json }}
```

### Étape 5 : Activer le Workflow

1. **Cliquer sur le bouton "Active" en haut à droite**
2. **Le workflow passe en mode actif (indicateur vert)**
3. **Sauvegarder le workflow (Ctrl+S)**

## ✅ Vérification de la Configuration

### Test 1 : Test avec curl

```bash
curl -X POST http://localhost:5678/webhook/skill_feuilles_revision_cas6 \
     -H "Content-Type: application/json" \
     -d '{}'
```

**Réponse attendue** : JSON contenant `Data_integrale`

### Test 2 : Test avec Python

```python
import requests
import json

url = "http://localhost:5678/webhook/skill_feuilles_revision_cas6"
response = requests.post(url, json={})
print(json.dumps(response.json(), indent=2, ensure_ascii=False))
```

### Test 3 : Test avec le script complet

```bash
python execute_cas6_production.py
```

### Test 4 : Test PowerShell

```powershell
.\test_workflow_cas6.ps1
```

## 📊 Structure des Données

### Format de `Data_integrale`

```json
{
  "Data_integrale": [
    {
      "Feuille de révision - [Titre]": [
        {
          "table 1": {
            "Etape de mission": "...",
            "Document": "...",
            "Processus": "...",
            "Reference": "..."
          }
        },
        {
          "table 2": [
            {
              "N° Test": "...",
              "Objectif de contrôle": "...",
              "Nature du contrôle": "...",
              "Procédure de test": "...",
              "Taille échantillon": "...",
              "Résultat observé": "...",
              "Écart identifié": "...",
              "Conclusion": "...",
              "Action recommandée": "..."
            }
          ]
        }
      ]
    }
  ]
}
```

### Colonnes Obligatoires (Table 2)

1. **N° Test** : Identifiant unique du test
2. **Objectif de contrôle** : But du test effectué
3. **Nature du contrôle** : Préventif/Détectif/Correctif
4. **Procédure de test** : Actions effectuées (multiligne avec `\n`)
5. **Taille échantillon** : Format "N/Total (X%)"
6. **Résultat observé** : Constat factuel
7. **Écart identifié** : Non-conformités détectées
8. **Conclusion** : Synthèse de l'évaluation
9. **Action recommandée** : Recommandation de l'auditeur

## 🔗 Connexion à une Base de Données

### Exemple avec PostgreSQL

Si vos feuilles de révision sont dans une base de données :

1. **Ajouter un nœud "Postgres"** avant "Edit Fields"
2. **Configurer la requête SQL :**

```sql
SELECT 
  json_build_object(
    'Feuille de révision - ' || f.titre, 
    json_build_array(
      json_build_object('table 1', f.metadonnees),
      json_build_object('table 2', f.tests)
    )
  ) as feuille
FROM feuilles_revision f
WHERE f.statut = 'validé'
ORDER BY f.date_creation DESC
```

3. **Dans "Edit Fields", utiliser :** `{{ $json.feuille }}`

## 🐛 Dépannage

### Erreur : "Connection refused"

**Cause** : N8N n'est pas démarré

**Solution** :
```bash
n8n start
```

### Erreur : "Webhook not found"

**Cause** : Le workflow n'est pas actif

**Solution** :
1. Ouvrez N8N
2. Ouvrez le workflow `skill_feuilles_revision_cas6`
3. Cliquez sur "Active" en haut à droite

### Erreur : "Data_integrale absent"

**Cause** : Configuration incorrecte du nœud "Edit Fields"

**Solution** :
1. Vérifiez que le champ s'appelle exactement `Data_integrale`
2. Vérifiez que le type est bien "Array"
3. Vérifiez que la structure JSON est valide

### Erreur : "Timeout"

**Cause** : N8N met trop de temps à répondre

**Solution** :
1. Augmentez le TIMEOUT dans `execute_cas6_production.py`
2. Optimisez votre workflow N8N
3. Réduisez la quantité de données retournées

## 💡 Conseils d'Optimisation

### 1. Utiliser des Pinned Data

Pour le développement, utilisez les "Pinned Data" de N8N :

1. Cliquez sur le nœud "Edit Fields"
2. Cliquez sur le menu (3 points) > "Pin data"
3. Collez votre JSON d'exemple
4. Cela permet de tester sans appeler la base de données

### 2. Pagination

Pour de grandes quantités de feuilles :

```json
{
  "Data_integrale": "{{ $json.feuilles.slice(0, 50) }}"
}
```

### 3. Filtrage

Filtrer les feuilles par critères :

```json
{
  "Data_integrale": "{{ $json.feuilles.filter(f => f.statut === 'validé') }}"
}
```

## 📞 Support

En cas de problème, vérifiez :

1. ✅ N8N est démarré : `http://localhost:5678`
2. ✅ Le workflow est actif (indicateur vert)
3. ✅ L'URL du webhook est correcte
4. ✅ Le champ `Data_integrale` est bien configuré
5. ✅ La structure JSON respecte le format attendu

**Contact** : Whatsapp + 225 05 44 13 07 98

## 📚 Ressources

- [Documentation N8N](https://docs.n8n.io/)
- [N8N Webhook Node](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.webhook/)
- [N8N Edit Fields Node](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.set/)
- [Skill Cas 6 Documentation](./audit-feuilles-revision-json2word.skill.md)

## 🎯 Workflow Complet : Vue d'Ensemble

```
┌─────────────────────┐
│   Webhook           │  ← POST /webhook/skill_feuilles_revision_cas6
│   (Trigger)         │
└──────────┬──────────┘
           │
           ↓
┌─────────────────────┐
│   Edit Fields       │  ← Définit Data_integrale (Array)
│   (Transform)       │
└──────────┬──────────┘
           │
           ↓
┌─────────────────────┐
│   Respond Webhook   │  ← Retourne {{ $json }}
│   (Output)          │
└─────────────────────┘
```

**Flux de données** :
1. Requête POST arrive au webhook
2. Edit Fields structure les données en `Data_integrale`
3. Respond Webhook retourne le JSON formaté
4. Le script Python consomme cette réponse et génère les documents Word

---

**Date de création** : 31 octobre 2026  
**Version** : 1.0.0  
**Auteur** : Expert Python & Automation
