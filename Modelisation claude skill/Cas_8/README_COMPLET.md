# 📋 CAS 8 - PROGRAMME DE TRAVAIL / CARTOGRAPHIE

**Skill Opérationnelle** - Génération multi-format de documents d'audit

## 🎯 Description

Conversion automatique JSON → Word pour **5 types de documents** :

1. **Programme de travail** : Planning détaillé des missions
2. **Cartographie des risques** : Matrices et heat maps
3. **Modélisation** : Flowcharts et processus
4. **Plans de surveillance** : Contrôles permanents
5. **Matrices de surveillance** : Tableaux de bord

## 📂 Fichiers

| Fichier | Description |
|---------|-------------|
| `json2word_programme_travail.py` | Script de conversion JSON → Word (multi-format) |
| `execute_cas8_production.py` | Orchestrateur production (appel N8N) |
| `execute_cas8.bat` | Lanceur Windows |
| `sortie_word_cas8/` | Dossier de sortie des documents |

## ⚙️ Configuration N8N

**Webhook** : `http://localhost:5678/webhook/skill_programme_travail_cas8`

**Structure JSON attendue** :
```json
{
  "Data_integrale": [
    {
      "table 1": {
        "Etape de mission": "Programme de travail",  // Détection auto
        "Titre": "..."
      },
      "table 2": {
        "rows": [...]
      }
    }
  ]
}
```

## 🗂️ Types Supportés

### 1. Programme de Travail
Colonnes : Phase, Tâche, Responsable, Date début, Date fin, Statut

### 2. Cartographie des Risques
Colonnes : Processus, Risque, Impact, Probabilité, Criticité, Contrôle

### 3. Modélisation
Colonnes : Étape, Description, Input, Output, Responsable

### 4-5. Plans/Matrices Surveillance
Colonnes : Contrôle, Fréquence, Responsable, Indicateur, Seuil

## 🚀 Utilisation

### Production (avec N8N)

```cmd
execute_cas8.bat
```

### Direct (JSON local)

```cmd
conda activate pdf_excel_env
python json2word_programme_travail.py donnees.json
```

## 📊 Format de Sortie

- **Format** : A4 paysage
- **Couleur** : Bordeaux #7B1E3A
- **Police** : Calibri 10pt
- **Nom** : `[Nom]_V1_HH-MM-SS_DD.MM.YY.docx`
- **Détection automatique** du type selon "Etape de mission"

## ✅ Status

🟢 **OPÉRATIONNEL** - Prêt pour intégration N8N

---

**Date création** : 5 novembre 2026  
**Version** : 1.0.0
