# Cas 2 - Workflow N8N vers Word (Manuel des Procédures)

## Description
Récupération automatique des données depuis N8N via API webhook, puis conversion en documents Word.

## Skill Natif
- **Skill Claude Opus** : `audit-procedures-json2word.skill`
- **Skill Standard** : `audit-procedures-json2word.skill` (version 1.3.0)

## Étape de Mission
- **Manuel des procédures** : Procédures d'audit interne complètes

## Workflow N8N
- **Webhook URL** : `http://localhost:5678/webhook/skill_manuel_audit`
- **Méthode** : POST ou GET
- **Champ de sortie** : `Data_integrale` (Array)

## Caractéristiques
- ✅ **Mode** : API N8N
- ✅ **Source** : Webhook N8N
- ✅ **Batch Processing** : Oui (multiples procédures)
- ✅ **Horodatage** : Format `V1_HH-MM-SS_DD.MM.YY`
- ✅ **Dépendances** : python-docx, requests

## Fichiers
- `audit-procedures-json2word.skill.md` : Documentation du skill standard
- `execute_cas2_production.py` : Orchestrateur principal
- `json2word_audit.py` : Script de conversion
- `api_call_n8n.py` : Module d'appel API
- `execute_cas2.bat` : Script batch Windows

## Format de Nommage
```
[Etape_de_mission] ― [Nom_logiciel]_V1_HH-MM-SS_DD.MM.YY.docx
```

**Exemple** :
```
Manuel_audit_interne ― Logiciel automatisé E-audit pro_V1_15-22-03_31.10.26.docx
```

## Usage
```bash
# Mode production avec N8N
python execute_cas2_production.py

# Mode simulation (données locales)
python execute_workflow_simulation.py
```

## Statut
✅ **COMPLÉTÉ** - Skill standard v1.3.0 fonctionnel avec horodatage optimisé
