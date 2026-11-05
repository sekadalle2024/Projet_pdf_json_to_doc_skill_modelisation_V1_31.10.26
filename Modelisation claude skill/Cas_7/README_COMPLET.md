# 📋 CAS 7 - FEUILLES DE COUVERTURE

**Skill Opérationnelle** - Génération automatique de feuilles de couverture

## 🎯 Description

Conversion automatique JSON → Word pour :
- **Feuilles de couverture** avec schéma de calcul automatique
- **Tests d'audit** avec calculs intégrés

## 📂 Fichiers

| Fichier | Description |
|---------|-------------|
| `json2word_feuille_couverture.py` | Script de conversion JSON → Word |
| `execute_cas7_production.py` | Orchestrateur production (appel N8N) |
| `execute_cas7.bat` | Lanceur Windows |
| `sortie_word_cas7/` | Dossier de sortie des documents |

## ⚙️ Configuration N8N

**Webhook** : `http://localhost:5678/webhook/skill_feuille_couverture_cas7`

**Structure JSON attendue** :
```json
{
  "Data_integrale": [
    {
      "table 1": {
        "Etape de mission": "Feuille couverture",
        "Titre": "..."
      },
      "table 2": { "rows": [...] },
      "table 4": { "rows": [...] },
      "table 5": { "rows": [...] }
    }
  ]
}
```

## 🔧 Spécificité : Schéma de Calcul

Le script insère automatiquement un schéma de calcul entre table 5 et table 4 :

```
Table 5 (sources)
↓
[SCHÉMA: (A), (B), (C) = (A) - (D)]
↓
Table 4 (résultats)
```

## 🚀 Utilisation

### Production (avec N8N)

```cmd
execute_cas7.bat
```

### Direct (JSON local)

```cmd
conda activate pdf_excel_env
python json2word_feuille_couverture.py donnees.json
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
