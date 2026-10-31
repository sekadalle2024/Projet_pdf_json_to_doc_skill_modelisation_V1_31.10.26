# 🔧 Guide de Configuration N8N pour le Workflow Cas 2

## ⚠️ Problème Détecté

La réponse du webhook N8N est vide : `{}`

Cela signifie que le nœud **"Edit Fields"** de votre workflow N8N n'a pas de données configurées.

---

## ✅ Solution : Configurer les Données dans N8N

### Étape 1 : Ouvrir N8N

1. Ouvrez votre navigateur
2. Allez sur : http://localhost:5678
3. Ouvrez le workflow : **skill_manuel_audit**

### Étape 2 : Configurer le Nœud "Edit Fields"

1. **Cliquez** sur le nœud "Edit Fields"
2. Dans l'interface, vous devriez voir l'option **"Pin Data"** (Épingler les données)
3. **Activez** l'option "Pin Data"
4. **Collez** les données JSON suivantes :

```json
{
  "Data_integrale": [
    {
      "Etape mission - Manuel des procedures": [
        {
          "table 1": {
            "Etape de mission": "Manuel audit interne",
            "Document": "Manuel méthodologique d'audit interne - Guide complet",
            "Processus": "Audit interne - Surveillance permanente",
            "Cycle d'activité": "Méthodologie d'Audit Interne Bancaire",
            "Secteur d'activité": "Banque et établissements financiers UMOA",
            "Norme": {
              "Norme 1": "Norme 1.1 Honnêteté et courage professionnel",
              "Norme 2": "Norme 4.2 Conscience professionnelle"
            },
            "Reference": "MAN-AUD-BK-001",
            "Version": "V3.0 - Production N8N",
            "Etablissement": "Afrika Financial Bank",
            "Approbation": "Comité d'Audit et des Risques"
          }
        },
        {
          "table 2": [
            {
              "Étape méthodologique": "Extraction de la population des comptes",
              "Acteur audit": "Auditeur Interne Senior SI",
              "Traitement et diligences d'audit": "- Extrait les tables des comptes via requêtes SQL.\n- Rapproche les soldes avec le grand livre.\n- Vérifie l'intégrité des données.",
              "Document probant": "Requête SQL, Journal des batchs, Grand livre",
              "Norme IIA / CRIPP": "Norme 14.1 Collecte d'informations",
              "Extrait de la norme": "Les auditeurs internes doivent recueillir des informations pertinentes, fiables et suffisantes."
            }
          ]
        }
      ]
    },
    {
      "Etape mission - Manuel des procedures": [
        {
          "table 1": {
            "Etape de mission": "Phase de préparation",
            "Document": "Manuel de préparation de mission d'audit",
            "Processus": "Audit interne - Planification",
            "Cycle d'activité": "Méthodologie d'Audit",
            "Secteur d'activité": "Banque UMOA",
            "Norme": {
              "Norme 1": "Norme 13.2 Évaluation des risques"
            },
            "Reference": "MAN-AUD-BK-002",
            "Version": "V3.0 - Production N8N",
            "Etablissement": "Afrika Financial Bank",
            "Approbation": "Direction de l'Audit Interne"
          }
        },
        {
          "table 2": [
            {
              "Étape méthodologique": "Cadrage initial du périmètre",
              "Acteur audit": "Directeur de l'Audit Interne",
              "Traitement et diligences d'audit": "- Définit le périmètre d'analyse.\n- Identifie les objectifs stratégiques.",
              "Document probant": "Lettre de cadrage, Note de stratégie",
              "Norme IIA / CRIPP": "Norme 13.3 Objectifs et périmètre",
              "Extrait de la norme": "Les auditeurs internes doivent déterminer les objectifs et le périmètre de la mission."
            }
          ]
        }
      ]
    }
  ]
}
```

### Étape 3 : Sauvegarder et Activer

1. **Sauvegardez** le workflow (Ctrl+S ou bouton Save)
2. **Activez** le workflow (toggle en haut à droite)
3. Le webhook est maintenant prêt !

---

## 🧪 Test du Webhook

### Test 1 : Avec cURL (depuis PowerShell)

```powershell
curl http://localhost:5678/webhook/skill_manuel_audit -Method POST -ContentType "application/json" -Body "{}"
```

### Test 2 : Avec Python

```python
import requests
response = requests.post("http://localhost:5678/webhook/skill_manuel_audit")
print(response.json())
```

### Test 3 : Avec le Script de Test

```bash
python execute_cas2_production.py
```

---

## 📊 Structure Attendue

Le webhook doit retourner un JSON avec cette structure :

```json
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
```

Ou dans un tableau :

```json
[
  {
    "Data_integrale": [...]
  }
]
```

---

## 🔍 Vérification

Après avoir configuré N8N, le script devrait afficher :

```
✅ Réponse reçue (Status: 200)
✅ Extraction réussie : 2 procédure(s)
```

Au lieu de :

```
❌ Structure non reconnue ou Data_integrale absent
```

---

## 📞 Support

Si le problème persiste :

1. Vérifiez que le nœud "Edit Fields" est bien connecté au nœud "Respond to Webhook"
2. Vérifiez que les données sont bien épinglées (Pin Data activé)
3. Testez le webhook directement dans un navigateur : http://localhost:5678/webhook/skill_manuel_audit

---

**Version** : 1.0.0  
**Date** : 31 octobre 2026
