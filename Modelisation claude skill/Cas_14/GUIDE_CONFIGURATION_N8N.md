# 🔧 Guide de Configuration N8N - Cas 14 : FRAP et Recommandations

## 📋 Pré-requis

Avant de commencer la configuration du workflow N8N pour le Cas 14, assurez-vous que :

- ✅ **Node.js** est installé (version >= 16.x)
- ✅ **npm** est installé (généralement inclus avec Node.js)
- ✅ Vous avez des **droits administrateur** sur votre machine
- ✅ Le port **5678** est disponible (port par défaut de N8N)
- ✅ Python **>= 3.9** est installé avec les dépendances nécessaires

---

## 🚀 Installation de N8N

### Option 1 : Installation Globale (Recommandée)

```bash
# Installation globale via npm
npm install n8n -g

# Vérification de l'installation
n8n --version
```

**Avantages** :
- Commande `n8n` accessible depuis n'importe quel répertoire
- Configuration globale persistante
- Idéal pour un usage régulier

### Option 2 : Installation avec npx (Sans Installation)

```bash
# Exécution directe avec npx
npx n8n

# Ou avec une version spécifique
npx n8n@latest
```

**Avantages** :
- Aucune installation permanente
- Toujours la dernière version
- Idéal pour les tests ponctuels

### Démarrage de N8N

```bash
# Démarrage standard
n8n start

# Démarrage avec port personnalisé
N8N_PORT=5679 n8n start

# Démarrage en arrière-plan (Linux/Mac)
n8n start &

# Démarrage en arrière-plan (Windows avec PowerShell)
Start-Process n8n -ArgumentList "start" -WindowStyle Hidden
```

**URL d'accès** : `http://localhost:5678`

---

## 🔧 Configuration du Workflow

### Étape 1 : Créer un Nouveau Workflow

1. Ouvrir N8N dans votre navigateur : `http://localhost:5678`
2. Cliquer sur **"+ New Workflow"** (ou **"Nouveau workflow"**)
3. Nommer le workflow : **`skill_frap_cas14`**
4. Cliquer sur **"Save"** pour sauvegarder

### Étape 2 : Ajouter le Nœud Webhook

#### Configuration Détaillée

1. **Ajouter le nœud** :
   - Cliquer sur le bouton **"+"** pour ajouter un nœud
   - Chercher **"Webhook"** dans la liste
   - Sélectionner **"Webhook"**

2. **Paramètres du nœud Webhook** :

   | Paramètre | Valeur | Description |
   |-----------|--------|-------------|
   | **Node Name** | `Webhook Cas 14 FRAP` | Nom du nœud (facultatif) |
   | **HTTP Method** | `POST` | Méthode HTTP requise |
   | **Path** | `skill_frap_cas14` | Chemin du webhook (sans `/webhook/`) |
   | **Authentication** | `None` | Pas d'authentification (environnement local) |
   | **Response Mode** | `On Last Node` | Répondre après le dernier nœud |
   | **Response Data** | `All Entries` | Retourner toutes les données |

3. **URL complète du webhook** :
   ```
   http://localhost:5678/webhook/skill_frap_cas14
   ```

4. **Sauvegarder le nœud** : Cliquer sur **"Execute Node"** pour tester

### Étape 3 : Ajouter le Nœud "Edit Fields"

#### Configuration du Champ Data_integrale

1. **Ajouter le nœud** :
   - Connecter depuis le nœud Webhook
   - Chercher **"Edit Fields"** (ou **"Code"** > **"Set"**)
   - Sélectionner **"Edit Fields (Set)"**

2. **Paramètres** :

   | Paramètre | Valeur | Description |
   |-----------|--------|-------------|
   | **Node Name** | `Construct Data_integrale` | Nom du nœud |
   | **Mode** | `Manual Mapping` | Mapping manuel |
   | **Field** | `Data_integrale` | Nom du champ |
   | **Type** | `Array` | Type de données |

3. **Exemple de structure JSON** :

```json
{
  "Data_integrale": [
    {
      "Etape mission - Frap": [
        {
          "table 1": {
            "Etape de mission": "Frap",
            "Norme": "Norme 14.3 Évaluation des constats",
            "Méthode": "Méthode des recommandations par les constats d'audit",
            "Reference": "FRAP-DEMO-01"
          }
        },
        {
          "table 2": {
            "Intitule": "Exemple de constat d'audit pour démonstration"
          }
        },
        {
          "table 3": {
            "Observation": "Description détaillée de l'observation réalisée lors de la mission d'audit."
          }
        },
        {
          "table 4": {
            "Constat": "- Point 1 du constat identifié\n- Point 2 du constat identifié\n- Point 3 du constat identifié"
          }
        },
        {
          "table 5": {
            "Risque": "- Risque 1 associé au constat\n- Risque 2 associé au constat\n- Risque 3 associé au constat"
          }
        },
        {
          "table 6": {
            "Recommendation": "- Recommandation corrective 1\n- Recommandation corrective 2\n- Recommandation corrective 3"
          }
        }
      ]
    }
  ]
}
```

4. **Utilisation de Pinned Data (Données Épinglées)** :
   - Cliquer sur **"Pin Data"** dans le nœud "Edit Fields"
   - Coller la structure JSON ci-dessus
   - Cliquer sur **"Save"**
   - Cela permet de tester le workflow sans appel API externe

### Étape 4 : Ajouter le Nœud "Respond to Webhook"

#### Configuration de la Réponse

1. **Ajouter le nœud** :
   - Connecter depuis le nœud "Edit Fields"
   - Chercher **"Respond to Webhook"**
   - Sélectionner ce nœud

2. **Paramètres** :

   | Paramètre | Valeur | Description |
   |-----------|--------|-------------|
   | **Node Name** | `Send Response` | Nom du nœud |
   | **Respond With** | `JSON` | Format de réponse |
   | **Response Body** | `{{ $json }}` | Retourner les données JSON |
   | **Status Code** | `200` | Code HTTP de succès |

3. **Headers personnalisés** (optionnel) :

   | Header | Valeur |
   |--------|--------|
   | `Content-Type` | `application/json` |
   | `X-Workflow` | `skill_frap_cas14` |

### Étape 5 : Activer le Workflow

1. **Vérifier la connexion des nœuds** :
   - Webhook → Edit Fields → Respond to Webhook
   - Toutes les flèches doivent être connectées

2. **Activer le workflow** :
   - Cliquer sur le bouton **"Active"** (en haut à droite)
   - Le bouton doit passer en vert avec la mention **"Active"**

3. **Sauvegarder** :
   - Cliquer sur **"Save"** ou `Ctrl+S`
   - Le workflow est maintenant opérationnel

---

## ✅ Vérification de la Configuration

### Test 1 : Test avec curl (Ligne de commande)

#### Windows (PowerShell)

```powershell
# Test POST simple
Invoke-RestMethod -Uri "http://localhost:5678/webhook/skill_frap_cas14" -Method POST -ContentType "application/json" | ConvertTo-Json -Depth 10

# Test avec affichage formaté
(Invoke-WebRequest -Uri "http://localhost:5678/webhook/skill_frap_cas14" -Method POST).Content | ConvertFrom-Json | ConvertTo-Json -Depth 10
```

#### Linux / Mac

```bash
# Test POST simple
curl -X POST http://localhost:5678/webhook/skill_frap_cas14

# Test avec output formaté
curl -X POST http://localhost:5678/webhook/skill_frap_cas14 | jq .
```

**Résultat attendu** :
```json
{
  "Data_integrale": [
    {
      "Etape mission - Frap": [
        ...
      ]
    }
  ]
}
```

### Test 2 : Test avec Python

Créer un fichier `test_webhook_cas14.py` :

```python
import requests
import json

# URL du webhook
url = "http://localhost:5678/webhook/skill_frap_cas14"

try:
    # Appel POST
    response = requests.post(url, timeout=10)
    
    # Vérification du statut
    if response.status_code == 200:
        data = response.json()
        
        # Vérification de Data_integrale
        if "Data_integrale" in data:
            print("✅ Webhook fonctionne correctement")
            print(f"✅ Nombre d'éléments : {len(data['Data_integrale'])}")
            print("\n📄 Réponse complète :")
            print(json.dumps(data, indent=2, ensure_ascii=False))
        else:
            print("❌ Erreur : 'Data_integrale' absent de la réponse")
            print(f"Réponse reçue : {data}")
    else:
        print(f"❌ Erreur HTTP : {response.status_code}")
        print(f"Réponse : {response.text}")
        
except requests.exceptions.ConnectionError:
    print("❌ Erreur : Impossible de se connecter à N8N")
    print("💡 Solution : Vérifier que N8N est démarré (n8n start)")
    
except requests.exceptions.Timeout:
    print("❌ Erreur : Timeout lors de l'appel au webhook")
    print("💡 Solution : Augmenter le timeout ou vérifier le workflow N8N")
    
except Exception as e:
    print(f"❌ Erreur inattendue : {e}")
```

**Exécution** :
```bash
python test_webhook_cas14.py
```

### Test 3 : Test avec le Script Complet

```bash
# Exécuter le script de production
python execute_cas14_production.py
```

**Résultat attendu** :
- Appel API réussi
- Extraction de `Data_integrale`
- Génération de documents Word dans `sortie_word_cas14/`

### Test 4 : Test PowerShell (Suite Complète)

```powershell
# Exécuter la suite de tests complète
.\test_workflow_cas14.ps1
```

**Résultat attendu** : `7/7 tests passent` ✅

---

## 📊 Structure des Données

### Format de Data_integrale

```json
{
  "Data_integrale": [
    {
      "Etape mission - Frap": [
        { "table 1": { ... } },  // Métadonnées
        { "table 2": { ... } },  // Intitulé
        { "table 3": { ... } },  // Observation
        { "table 4": { ... } },  // Constat
        { "table 5": { ... } },  // Risque
        { "table 6": { ... } }   // Recommandation
      ]
    },
    {
      "Etape mission - Frap": [
        ...  // FRAP 2
      ]
    }
  ]
}
```

### Colonnes Obligatoires

#### Table 1 (Métadonnées)

| Champ | Type | Obligatoire | Description |
|-------|------|-------------|-------------|
| `Etape de mission` | String | ✅ | Nom de l'étape (ex: "Frap") |
| `Norme` | String | ✅ | Référence normative (ex: "Norme 14.3") |
| `Méthode` | String | ✅ | Méthode appliquée |
| `Reference` | String | ✅ | Référence unique du FRAP |

#### Tables 2-6 (Contenu)

| Table | Champ | Type | Description |
|-------|-------|------|-------------|
| **Table 2** | `Intitule` | String | Titre du constat |
| **Table 3** | `Observation` | String | Description de l'observation |
| **Table 4** | `Constat` | String | Points du constat (lignes à puces) |
| **Table 5** | `Risque` | String | Risques identifiés (lignes à puces) |
| **Table 6** | `Recommendation` | String | Recommandations correctives (lignes à puces) |

---

## 🔗 Connexion à une Base de Données (Optionnel)

### Exemple avec PostgreSQL

Si vos données FRAP proviennent d'une base PostgreSQL :

1. **Ajouter un nœud "Postgres"** :
   - Placer avant le nœud "Edit Fields"
   - Configurer la connexion à la base

2. **Requête SQL type** :

```sql
SELECT 
    json_build_object(
        'Data_integrale', 
        json_agg(
            json_build_object(
                'Etape mission - Frap',
                json_build_array(
                    json_build_object('table 1', json_build_object(
                        'Etape de mission', etape_mission,
                        'Norme', norme,
                        'Méthode', methode,
                        'Reference', reference
                    )),
                    json_build_object('table 2', json_build_object('Intitule', intitule)),
                    json_build_object('table 3', json_build_object('Observation', observation)),
                    json_build_object('table 4', json_build_object('Constat', constat)),
                    json_build_object('table 5', json_build_object('Risque', risque)),
                    json_build_object('table 6', json_build_object('Recommendation', recommendation))
                )
            )
        )
    ) AS result
FROM audit_frap
WHERE statut = 'Validé'
AND date_mission >= CURRENT_DATE - INTERVAL '30 days';
```

3. **Mapper le résultat** :
   - Extraire `result.Data_integrale`
   - Passer au nœud "Respond to Webhook"

---

## 🐛 Dépannage

### Erreur : "Connection refused" (localhost:5678)

**Cause** : N8N n'est pas démarré ou le port est incorrect.

**Solutions** :
```bash
# Vérifier si N8N tourne
curl http://localhost:5678

# Démarrer N8N
n8n start

# Vérifier le processus (Windows)
Get-Process -Name node | Where-Object {$_.Path -like "*n8n*"}

# Vérifier le processus (Linux/Mac)
ps aux | grep n8n

# Changer le port si occupé
N8N_PORT=5679 n8n start
```

### Erreur : "Webhook not found" (404)

**Cause** : Le workflow n'est pas activé ou le path est incorrect.

**Solutions** :
1. Vérifier que le workflow est **Active** (bouton vert)
2. Vérifier le path : doit être `skill_frap_cas14` (sans `/webhook/`)
3. URL complète : `http://localhost:5678/webhook/skill_frap_cas14`
4. Recharger la page N8N et réactiver le workflow

### Erreur : "Data_integrale absent" dans la réponse

**Cause** : Le nœud "Edit Fields" n'est pas configuré correctement.

**Solutions** :
1. Ouvrir le nœud "Edit Fields"
2. Vérifier que le champ s'appelle exactement `Data_integrale` (sensible à la casse)
3. Vérifier que le type est **Array**
4. Utiliser "Pinned Data" pour tester avec des données statiques
5. Exécuter le nœud manuellement avec "Execute Node"

### Erreur : "Timeout" lors de l'appel API

**Cause** : Le workflow N8N est trop lent ou bloqué.

**Solutions** :
1. Vérifier les logs N8N (console où N8N a été démarré)
2. Simplifier le workflow (retirer les nœuds complexes temporairement)
3. Augmenter le timeout dans le script Python :
   ```python
   TIMEOUT = 60  # Au lieu de 30
   ```
4. Redémarrer N8N :
   ```bash
   # Arrêter N8N
   Ctrl+C (dans la console N8N)
   
   # Redémarrer
   n8n start
   ```

### Erreur : "Invalid JSON" dans la réponse

**Cause** : La structure JSON retournée est malformée.

**Solutions** :
1. Vérifier la structure avec un validateur JSON en ligne (jsonlint.com)
2. Utiliser "Pinned Data" avec une structure JSON valide
3. Vérifier les guillemets et accolades dans "Edit Fields"
4. Tester la réponse avec `| jq .` (Linux/Mac) ou `| ConvertFrom-Json` (PowerShell)

---

## 💡 Conseils d'Optimisation

### 1. Utiliser des Pinned Data pour les Tests

**Avantage** : Tester le workflow sans dépendre d'une base de données externe.

**Comment** :
1. Cliquer sur "Pin Data" dans le nœud "Edit Fields"
2. Coller votre structure JSON complète
3. Le workflow utilisera ces données au lieu de données dynamiques

### 2. Pagination pour Gros Volumes

Si vous avez plus de 100 FRAP à traiter :

```javascript
// Node "Code" (JavaScript)
const limit = 50;  // Nombre de FRAP par lot
const offset = 0;  // Décalage

return {
  json: {
    limit: limit,
    offset: offset
  }
};
```

### 3. Filtrage des Données

Ajouter un nœud "Filter" pour ne traiter que certains FRAP :

```javascript
// Condition : Traiter uniquement les FRAP validés
return items.filter(item => {
  const frap = item.json["Etape mission - Frap"];
  return frap && frap.length > 0;
});
```

### 4. Logging Détaillé

Ajouter un nœud "HTTP Request" pour logger les résultats :

```javascript
// POST vers un serveur de logs
{
  "webhook_called": true,
  "timestamp": new Date().toISOString(),
  "frap_count": items.length
}
```

---

## 📞 Support

### Ressources N8N

- **Documentation officielle** : https://docs.n8n.io/
- **Forum communautaire** : https://community.n8n.io/
- **GitHub** : https://github.com/n8n-io/n8n

### Ressources Cas 14

- **Skill complet** : `audit-frap-recos-json2word.skill.md`
- **README** : `README.md`
- **Tests** : `test_workflow_cas14.ps1`

---

## 📚 Ressources

### Documentation Externe

- [N8N Documentation](https://docs.n8n.io/)
- [Webhook Node](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.webhook/)
- [Set Node (Edit Fields)](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.set/)
- [Respond to Webhook](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.respondtowebhook/)

### Tutoriels Vidéo (Externes)

- Installation de N8N
- Configuration de workflows
- Intégration avec bases de données

---

## 🎯 Workflow Complet : Vue d'Ensemble

```
┌──────────────────────────────────────────────────────────────┐
│                    WORKFLOW N8N CAS 14                       │
└──────────────────────────────────────────────────────────────┘

1. [Webhook]
   ↓ POST /webhook/skill_frap_cas14
   ↓ Réception de la requête
   │
2. [Edit Fields / Set]
   ↓ Construction de Data_integrale
   ↓ Format JSON structuré avec 6 tables
   │
3. [Respond to Webhook]
   ↓ Envoi de la réponse JSON
   ↓ Status 200 OK
   │
   ▼
   Réponse reçue par execute_cas14_production.py
   → Conversion JSON → Word
   → Documents FRAP générés
```

---

## ✅ Checklist de Configuration

Avant de considérer la configuration complète, vérifier :

- [ ] N8N est installé et démarre sans erreur
- [ ] Le workflow `skill_frap_cas14` est créé
- [ ] Le nœud Webhook est configuré avec le path `skill_frap_cas14`
- [ ] Le nœud "Edit Fields" contient `Data_integrale` (type Array)
- [ ] Le nœud "Respond to Webhook" est connecté
- [ ] Le workflow est **Actif** (bouton vert)
- [ ] Test curl/PowerShell réussi (réponse JSON valide)
- [ ] Test Python réussi (`test_webhook_cas14.py`)
- [ ] Test complet réussi (`.\test_workflow_cas14.ps1` - 7/7)

---

**Document créé le** : 31 octobre 2026  
**Version** : 1.0.0  
**Cas** : 14 - FRAP et Recommandations  
**Webhook** : `http://localhost:5678/webhook/skill_frap_cas14`  
**Statut** : ✅ Prêt pour production
