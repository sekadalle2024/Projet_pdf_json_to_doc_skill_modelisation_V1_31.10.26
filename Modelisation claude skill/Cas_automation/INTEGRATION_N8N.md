# Intégration N8N - Guide Complet

## Vue d'ensemble

Ce guide explique comment intégrer le serveur Flask d'automation avec N8N pour automatiser complètement la génération de documents Word sans agent.

## Architecture du Workflow N8N

```
┌─────────────┐
│   Webhook   │  Reçoit le JSON
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Transform  │  Traite/Valide le JSON (optionnel)
│    JSON     │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ HTTP Request│  Appelle le serveur Flask
│   to Flask  │  localhost:5000/automation/cas_X
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Save File  │  Sauvegarde le .docx
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Response   │  Retourne l'URL/statut
└─────────────┘
```

## Configuration N8N

### 1. Node Webhook (Input)

Reçoit les données JSON de l'extérieur.

**Configuration :**
```json
{
  "name": "Webhook Reception",
  "type": "n8n-nodes-base.webhook",
  "parameters": {
    "httpMethod": "POST",
    "path": "generate_document",
    "responseMode": "responseNode",
    "options": {}
  }
}
```

**URL du webhook :**
```
http://your-n8n-url/webhook/generate_document
```

### 2. Node Function (Optionnel - Validation)

Valide et transforme le JSON avant envoi au serveur.

**Code JavaScript :**
```javascript
// Extraire le JSON du webhook
const inputData = $input.all();
const jsonData = inputData[0].json;

// Déterminer le cas à traiter
let cas_number = 6; // Par défaut

if (jsonData['Etape mission - Feuille revision']) {
  cas_number = 6;
} else if (jsonData['Etape mission - Feuille couverture']) {
  cas_number = 7;
} else if (jsonData['Etape mission - Modele standard']) {
  cas_number = 8;
}

// Retourner les données avec le cas détecté
return [{
  json: {
    cas_number: cas_number,
    data: jsonData
  }
}];
```

### 3. Node HTTP Request (Génération)

Appelle le serveur Flask pour générer le document.

**Configuration pour Cas 6 :**
```json
{
  "name": "Generate Document Cas 6",
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
    "contentType": "json",
    "body": "={{ $json.data }}",
    "options": {
      "response": {
        "response": {
          "responseFormat": "file",
          "outputPropertyName": "data"
        }
      },
      "timeout": 30000
    }
  }
}
```

**Configuration Dynamique (tous les cas) :**
```javascript
// Dans un node Function avant HTTP Request
const cas = $json.cas_number;
const url = `http://localhost:5000/automation/cas_${cas}`;

return [{
  json: {
    url: url,
    data: $json.data
  }
}];
```

Puis dans HTTP Request:
```json
{
  "url": "={{ $json.url }}",
  "body": "={{ JSON.stringify($json.data) }}"
}
```

### 4. Node Write Binary File (Sauvegarde)

Sauvegarde le fichier Word généré.

**Configuration :**
```json
{
  "name": "Save Document",
  "type": "n8n-nodes-base.writeBinaryFile",
  "parameters": {
    "fileName": "=/output/{{ $now.format('YYYYMMDDHHmmss') }}_cas_{{ $('Function').item.json.cas_number }}.docx",
    "dataPropertyName": "data"
  }
}
```

### 5. Node Respond to Webhook (Output)

Retourne une réponse au client.

**Configuration :**
```json
{
  "name": "Response Success",
  "type": "n8n-nodes-base.respondToWebhook",
  "parameters": {
    "respondWith": "json",
    "responseBody": "={{ { \"success\": true, \"filename\": $json.filename, \"cas\": $json.cas_number } }}"
  }
}
```

## Workflow Complet (JSON Export)

```json
{
  "name": "Automation Documents Audit",
  "nodes": [
    {
      "parameters": {
        "httpMethod": "POST",
        "path": "generate_audit_doc",
        "responseMode": "responseNode"
      },
      "name": "Webhook",
      "type": "n8n-nodes-base.webhook",
      "position": [250, 300]
    },
    {
      "parameters": {
        "functionCode": "const jsonData = $input.all()[0].json;\nlet cas_number = 6;\nif (jsonData['Etape mission - Feuille couverture']) cas_number = 7;\nif (jsonData['Etape mission - Modele standard']) cas_number = 8;\nreturn [{json: {cas_number: cas_number, data: jsonData}}];"
      },
      "name": "Detect Cas",
      "type": "n8n-nodes-base.function",
      "position": [450, 300]
    },
    {
      "parameters": {
        "method": "POST",
        "url": "=http://localhost:5000/automation/cas_{{ $json.cas_number }}",
        "sendBody": true,
        "contentType": "json",
        "body": "={{ JSON.stringify($json.data) }}",
        "options": {
          "response": {
            "response": {
              "responseFormat": "file"
            }
          }
        }
      },
      "name": "Generate Document",
      "type": "n8n-nodes-base.httpRequest",
      "position": [650, 300]
    },
    {
      "parameters": {
        "fileName": "=/output/{{ $now.format('YYYYMMDDHHmmss') }}_cas_{{ $('Detect Cas').item.json.cas_number }}.docx"
      },
      "name": "Save File",
      "type": "n8n-nodes-base.writeBinaryFile",
      "position": [850, 300]
    },
    {
      "parameters": {
        "respondWith": "json",
        "responseBody": "={{ { \"success\": true, \"cas\": $('Detect Cas').item.json.cas_number } }}"
      },
      "name": "Response",
      "type": "n8n-nodes-base.respondToWebhook",
      "position": [1050, 300]
    }
  ],
  "connections": {
    "Webhook": {"main": [[{"node": "Detect Cas"}]]},
    "Detect Cas": {"main": [[{"node": "Generate Document"}]]},
    "Generate Document": {"main": [[{"node": "Save File"}]]},
    "Save File": {"main": [[{"node": "Response"}]]}
  }
}
```

## Workflows Avancés

### Workflow avec Notification Email

```
Webhook → Detect Cas → Generate → Save → Send Email → Response
```

**Node Send Email :**
```json
{
  "name": "Send Email",
  "type": "n8n-nodes-base.emailSend",
  "parameters": {
    "fromEmail": "audit@example.com",
    "toEmail": "={{ $json.email }}",
    "subject": "Document généré - Cas {{ $('Detect Cas').item.json.cas_number }}",
    "text": "Votre document a été généré avec succès.",
    "attachments": "data"
  }
}
```

### Workflow avec Base de Données

```
Webhook → Save to DB → Generate → Update DB → Response
```

**Node Save to Database :**
```json
{
  "name": "Save Request",
  "type": "n8n-nodes-base.postgres",
  "parameters": {
    "operation": "insert",
    "table": "generation_requests",
    "columns": "cas_number, status, created_at",
    "values": "={{ $json.cas_number }}, 'pending', NOW()"
  }
}
```

### Workflow avec Stockage Cloud

```
Webhook → Generate → Upload to S3/Drive → Response
```

**Node Upload to Google Drive :**
```json
{
  "name": "Upload to Drive",
  "type": "n8n-nodes-base.googleDrive",
  "parameters": {
    "operation": "upload",
    "folderId": "YOUR_FOLDER_ID",
    "fileName": "={{ $('Detect Cas').item.json.cas_number }}_{{ $now.format('YYYYMMDD') }}.docx",
    "binaryData": true
  }
}
```

## Gestion des Erreurs

### Try/Catch avec Node Error Trigger

```json
{
  "name": "Error Handler",
  "type": "n8n-nodes-base.errorTrigger",
  "parameters": {},
  "position": [650, 500]
}
```

**Node Function pour logging d'erreur :**
```javascript
const error = $input.all()[0].json.error;
const cas = $('Detect Cas').item.json.cas_number;

// Logger l'erreur
console.error(`Erreur Cas ${cas}:`, error);

// Retourner un message d'erreur formaté
return [{
  json: {
    success: false,
    error: error.message || 'Erreur inconnue',
    cas_number: cas,
    timestamp: new Date().toISOString()
  }
}];
```

### Retry Logic

```json
{
  "name": "Generate with Retry",
  "type": "n8n-nodes-base.httpRequest",
  "parameters": {
    "...": "...",
    "options": {
      "retry": {
        "retry": {
          "maxTries": 3,
          "waitBetweenTries": 5000
        }
      }
    }
  }
}
```

## Exemples de Requêtes

### cURL vers N8N Webhook

```bash
# Cas 6 - Feuille Révision
curl -X POST https://your-n8n.com/webhook/generate_audit_doc \
  -H "Content-Type: application/json" \
  -d @"Json_standard_[Cas 6].txt"

# Réponse
{
  "success": true,
  "cas": 6,
  "filename": "20261107153045_cas_6.docx"
}
```

### JavaScript/Fetch

```javascript
async function generateDocument(jsonData) {
  const response = await fetch('https://your-n8n.com/webhook/generate_audit_doc', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(jsonData)
  });
  
  return await response.json();
}

// Utilisation
const result = await generateDocument(myJsonData);
console.log('Document généré:', result.filename);
```

### Python/Requests

```python
import requests
import json

def generate_document(json_data):
    url = "https://your-n8n.com/webhook/generate_audit_doc"
    headers = {"Content-Type": "application/json"}
    
    response = requests.post(url, json=json_data, headers=headers)
    return response.json()

# Utilisation
with open('Json_standard_[Cas 6].txt', 'r') as f:
    data = json.load(f)

result = generate_document(data)
print(f"Document généré: {result['filename']}")
```

## Monitoring et Logs

### Node pour Logs

```javascript
// Function Node "Log Activity"
const startTime = $('Webhook').item.json.timestamp;
const endTime = new Date().toISOString();
const cas = $('Detect Cas').item.json.cas_number;
const filename = $json.filename;

// Log dans la console N8N
console.log({
  event: 'document_generated',
  cas_number: cas,
  start_time: startTime,
  end_time: endTime,
  filename: filename,
  duration_ms: new Date(endTime) - new Date(startTime)
});

return $input.all();
```

### Webhook pour Prometheus/Grafana

```json
{
  "name": "Send Metrics",
  "type": "n8n-nodes-base.httpRequest",
  "parameters": {
    "method": "POST",
    "url": "http://prometheus-pushgateway:9091/metrics/job/n8n_automation",
    "sendBody": true,
    "body": "=document_generation_total{cas=\"{{ $('Detect Cas').item.json.cas_number }}\"} 1"
  }
}
```

## Sécurité

### Authentification par Header

**Dans N8N Webhook:**
```javascript
// Function Node "Verify API Key"
const apiKey = $('Webhook').item.headers['x-api-key'];
const validKey = 'your-secret-key-here';

if (apiKey !== validKey) {
  throw new Error('API Key invalide');
}

return $input.all();
```

### Rate Limiting

```javascript
// Function Node "Check Rate Limit"
const redis = require('redis'); // Nécessite redis installé
const client = redis.createClient();

const ip = $('Webhook').item.headers['x-forwarded-for'];
const key = `ratelimit:${ip}`;

const count = await client.incr(key);
if (count === 1) {
  await client.expire(key, 3600); // 1 heure
}

if (count > 10) {
  throw new Error('Rate limit dépassé');
}

return $input.all();
```

## Dépannage

### Problème: Timeout

**Solution:** Augmenter le timeout dans HTTP Request
```json
{
  "options": {
    "timeout": 60000
  }
}
```

### Problème: Fichier non sauvegardé

**Solution:** Vérifier le format de réponse
```json
{
  "options": {
    "response": {
      "response": {
        "responseFormat": "file",
        "outputPropertyName": "data"
      }
    }
  }
}
```

### Problème: JSON invalide

**Solution:** Ajouter validation avant envoi
```javascript
try {
  JSON.parse(JSON.stringify($json.data));
} catch (e) {
  throw new Error('JSON invalide: ' + e.message);
}
```

## Ressources

- **Documentation N8N:** https://docs.n8n.io/
- **Serveur Flask:** `README_SERVEUR.md`
- **Exemples:** `/Cas_automation/exemples_curl.bat`

---

**Version:** 1.0.0  
**Date:** 7 novembre 2026
