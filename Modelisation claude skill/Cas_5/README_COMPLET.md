# 📋 CAS 5 - FRAP ET RECOMMANDATIONS

**Skill Opérationnelle** - Génération automatique de documents FRAP

## 🎯 Description

Conversion automatique JSON → Word pour :
- **FRAP** : Feuilles de Révélation et d'Analyse de Problème
- **Recommandations** : Plans d'action et recommandations d'audit

## 📂 Fichiers

| Fichier | Description |
|---------|-------------|
| `json2word_frap_recos.py` | Script de conversion JSON → Word |
| `execute_cas5_production.py` | Orchestrateur production (appel N8N) |
| `execute_cas5.bat` | Lanceur Windows |
| `sortie_word_cas5/` | Dossier de sortie des documents |

## ⚙️ Configuration N8N

**Webhook** : `http://localhost:5678/webhook/skill_frap_recos_cas5`

**Structure JSON attendue** :
```json
{
  "Data_integrale": [
    {
      "table 1": {
        "Etape de mission": "FRAP",
        "Titre": "..."
      },
      "table 2": {
        "rows": [
          {
            "Problème": "...",
            "Constat": "...",
            "Causes": "...",
            "Conséquences": "...",
            "Recommandations": "...",
            "Plan d'action": "..."
          }
        ]
      }
    }
  ]
}
```

## 🚀 Utilisation

### Méthode 1 : Production (avec N8N)

```cmd
execute_cas5.bat
```

### Méthode 2 : Direct (JSON local)

```cmd
conda activate pdf_excel_env
python json2word_frap_recos.py donnees.json
```

## 📊 Format de Sortie

- **Format** : A4 paysage
- **Couleur** : Bordeaux #7B1E3A
- **Police** : Calibri 10pt
- **Nom** : `[Nom]_V1_HH-MM-SS_DD.MM.YY.docx`

## ✅ Status

🟢 **OPÉRATIONNEL** - Prêt pour intégration N8N

---

**Date création** : 5 novembre 2026  
**Version** : 1.0.0
