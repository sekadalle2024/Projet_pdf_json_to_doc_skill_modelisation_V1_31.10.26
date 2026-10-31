# 📊 Cas 12 : Cartographie des Risques

> **Conversion automatisée de données JSON de cartographie des risques vers documents Word formatés**

## 🎯 Vue d'ensemble

Le **Cas 12** traite de la **cartographie des risques opérationnels et financiers** selon les référentiels internationaux :

- **ISO 31000:2018** (Management du risque - Lignes directrices)
- **COSO ERM 2017** (Enterprise Risk Management - Integrated Framework)
- **Référentiel BCEAO/Commission Bancaire UMOA**
- **Normes IIA** (Institute of Internal Auditors)

Ce module convertit des données structurées JSON en documents Word professionnels avec :
- ✅ Matrices de risques et contrôles (RCM - Risk & Control Matrix)
- ✅ Heat maps colorées par niveau de risque
- ✅ Évaluation complète : risque inhérent → contrôles → risque résiduel
- ✅ Conformité réglementaire bancaire UMOA

---

## 📋 Structure des Données

### Table 1 : Métadonnées du Document

```json
{
  "Etape de mission": "Cartographie des risques",
  "Document": "Cartographie des risques opérationnels et financiers",
  "Processus": "Gestion des risques - Cartographie et évaluation",
  "Cycle d'activité": "Management des Risques et Contrôle Interne",
  "Secteur d'activité": "Banque, Industrie et Assurance UMOA",
  "Méthodologie": "ISO 31000:2018, COSO ERM 2017, Référentiel BCEAO",
  "Reference": "CARTO-RISK-BK-2026-Q4",
  "Version": "V2.1 - Cartographie standard avec heat map",
  "Etablissement": "Afrika Group Holdings",
  "Périmètre": "Processus opérationnels critiques",
  "Date d'élaboration": "31 octobre 2026",
  "Approbation": "Comité des Risques / Direction des Risques",
  "Responsable": "Directeur des Risques / Risk Manager"
}
```

### Table 2 : Matrice des Risques et Contrôles (20 colonnes)

| # | Colonne | Description | Exemple |
|---|---------|-------------|---------|
| 1 | **Processus** | Processus métier concerné | "Gestion de la trésorerie" |
| 2 | **Sous-processus** | Sous-processus détaillé | "Réconciliation bancaire quotidienne" |
| 3 | **Risque identifié** | Description du risque | "Défaut de réconciliation entraînant des écarts" |
| 4 | **Catégorie de risque** | Type de risque | "Risque opérationnel - Processus" |
| 5 | **Cause racine** | Origine du risque | "Manque de ressources qualifiées" |
| 6 | **Événement déclencheur** | Événement qui déclenche le risque | "Non-réalisation pendant 3 jours" |
| 7 | **Impact potentiel** | Conséquences possibles | "Erreurs > 1M FCFA, fraudes non détectées" |
| 8 | **Probabilité** | Fréquence d'occurrence | "Moyenne (3/5)" |
| 9 | **Impact** | Gravité de l'impact | "Élevé (4/5)" |
| 10 | **Risque inhérent** | Risque brut (prob × impact) | "12 - Élevé (Rouge)" |
| 11 | **Contrôle préventif** | Contrôle pour éviter le risque | "Procédure formalisée avec checklist" |
| 12 | **Contrôle détectif** | Contrôle pour détecter le risque | "Rapprochement hebdomadaire" |
| 13 | **Contrôle correctif** | Contrôle pour corriger le risque | "Plan d'action si écart > 100k FCFA" |
| 14 | **Efficacité contrôle** | Niveau d'efficacité | "Partiellement efficace (2/4)" |
| 15 | **Risque résiduel** | Risque net après contrôles | "8 - Moyen (Orange)" |
| 16 | **Propriétaire du risque** | Responsable du traitement | "Directeur Financier" |
| 17 | **Statut traitement** | État d'avancement | "En cours / Urgent / Maîtrisé" |
| 18 | **Recommandation** | Actions correctrices | "Automatiser les réconciliations" |
| 19 | **Échéance** | Date limite de traitement | "31 décembre 2026" |
| 20 | **Coût traitement** | Budget nécessaire | "5M FCFA (formation + logiciel)" |

---

## 🎨 Échelle de Cotation des Risques

### Matrice Probabilité × Impact

| Probabilité ↓ / Impact → | 1 (Très faible) | 2 (Faible) | 3 (Moyen) | 4 (Élevé) | 5 (Critique) |
|--------------------------|-----------------|------------|-----------|-----------|--------------|
| **5 (Très élevée)** | 5 🟨 | 10 🟧 | 15 🟥 | 20 🟥🟥 | 25 🟥🟥 |
| **4 (Élevée)** | 4 🟨 | 8 🟧 | 12 🟥 | 16 🟥 | 20 🟥🟥 |
| **3 (Moyenne)** | 3 🟩 | 6 🟧 | 9 🟧 | 12 🟥 | 15 🟥 |
| **2 (Faible)** | 2 🟩 | 4 🟨 | 6 🟧 | 8 🟧 | 10 🟧 |
| **1 (Très faible)** | 1 🟩 | 2 🟩 | 3 🟩 | 4 🟨 | 5 🟨 |

### Légende des Niveaux de Risque

- 🟥🟥 **20-25 : Critique** - Action immédiate obligatoire
- 🟥 **12-16 : Élevé** - Action prioritaire sous 30 jours
- 🟧 **6-10 : Moyen** - Surveillance et plan d'action sous 90 jours
- 🟨 **3-5 : Faible** - Surveillance régulière
- 🟩 **1-2 : Très faible** - Risque acceptable, revue annuelle

---

## 🚀 Installation

### Prérequis

- Python 3.8+
- pip (gestionnaire de paquets Python)

### Installation des dépendances

```bash
# Installation via pip
pip install python-docx

# Ou via conda
conda install -c conda-forge python-docx
```

---

## 📖 Utilisation

### 1. Préparation des Données

Créez un fichier JSON avec la structure suivante :

```json
{
  "Cartographie des risques - Processus opérationnels": [
    {
      "table 1": {
        "Etape de mission": "Cartographie des risques",
        "Document": "...",
        "Etablissement": "Afrika Group Holdings"
      }
    },
    {
      "table 2": [
        {
          "Processus": "Gestion de la trésorerie",
          "Sous-processus": "Réconciliation bancaire",
          "Risque identifié": "Défaut de réconciliation...",
          "Risque inhérent": "12 - Élevé (Rouge)",
          "Risque résiduel": "8 - Moyen (Orange)",
          "Recommandation": "Automatiser les réconciliations"
        }
      ]
    }
  ]
}
```

### 2. Exécution du Script

```bash
python json2word_cartographie_risques.py
```

Le script :
1. ✅ Recherche automatiquement tous les fichiers `exemple_*.json`
2. ✅ Génère un document Word pour chaque fichier
3. ✅ Enregistre les résultats dans `output_word/`

### 3. Résultat

```
📁 output_word/
  ├── exemple_cartographie_minimal_CARTO_WORD.docx
  └── exemple_cartographie_complet_CARTO_WORD.docx
```

---

## 🎨 Caractéristiques du Document Word

### Mise en Page

- **Marges** : Gauche 2.5cm, Droite 2.0cm, Haut/Bas 2.0cm
- **Orientation** : Paysage (pour accueillir 20 colonnes)
- **Police** : Calibri (corporate standard)
- **Tailles** : Titre 16pt, Sous-titre 11pt, Texte 9pt

### En-tête

- Titre principal : **CARTOGRAPHIE DES RISQUES**
- Sous-titre : Nom de l'établissement
- Tableau de métadonnées avec 11 champs clés

### Tableau Principal

- 20 colonnes de données
- En-têtes en bleu foncé (RGB 0, 51, 102)
- Coloration automatique des risques :
  - 🟥 Rouge foncé : Risque critique (20)
  - 🟥 Rouge : Risque élevé (12-15)
  - 🟧 Orange : Risque moyen (6-10)
  - 🟨 Jaune : Risque faible (3-5)
  - 🟩 Vert : Risque très faible (1-2)

### Pied de Page

- Mention "Document confidentiel - Afrika Group Holdings"
- Date de génération automatique

---

## 📊 Exemples de Risques Traités

### 1. Risque Opérationnel - Trésorerie

**Risque** : Défaut de réconciliation bancaire quotidienne
- **Risque inhérent** : 12 - Élevé 🟥
- **Contrôles** : Procédure formalisée, rapprochement manuel
- **Risque résiduel** : 8 - Moyen 🟧
- **Recommandation** : Automatiser les réconciliations

### 2. Risque de Crédit

**Risque** : Octroi sans analyse approfondie
- **Risque inhérent** : 20 - Critique 🟥🟥
- **Contrôles** : Grille d'analyse, comité de crédit
- **Risque résiduel** : 15 - Élevé 🟥
- **Recommandation** : Renforcer comité et formation

### 3. Risque Technologique - Cybersécurité

**Risque** : Accès non autorisés aux données sensibles
- **Risque inhérent** : 15 - Élevé 🟥
- **Contrôles** : Matrice RACI, audit trail
- **Risque résiduel** : 12 - Élevé 🟥
- **Recommandation** : Déployer IAM et automatiser révocations

### 4. Risque de Conformité - AML/CFT

**Risque** : Non-déclaration d'opérations suspectes
- **Risque inhérent** : 15 - Élevé 🟥
- **Contrôles** : Formation AML, screening automatique
- **Risque résiduel** : 10 - Moyen 🟧
- **Recommandation** : Déployer solution AML et certification CAMS

---

## 🔧 Personnalisation

### Modifier les Couleurs de Risque

Éditez le fichier `json2word_cartographie_risques.py` :

```python
# Couleurs de niveau de risque
COULEUR_RISQUE_CRITIQUE = RGBColor(139, 0, 0)   # Rouge foncé
COULEUR_RISQUE_ELEVE = RGBColor(255, 0, 0)      # Rouge
COULEUR_RISQUE_MOYEN = RGBColor(255, 140, 0)    # Orange
COULEUR_RISQUE_FAIBLE = RGBColor(255, 215, 0)   # Jaune
COULEUR_RISQUE_TRES_FAIBLE = RGBColor(50, 205, 50)  # Vert
```

### Ajouter/Modifier des Colonnes

Modifiez la liste `colonnes` dans la fonction `creer_tableau_risques()` :

```python
colonnes = [
    "Processus",
    "Sous-processus",
    # ... ajoutez vos colonnes ici
    "Nouvelle Colonne",
]
```

Ajustez également les `largeurs_colonnes` en conséquence.

---

## 📚 Conformité Réglementaire

### Référentiels Appliqués

| Référentiel | Version | Application |
|-------------|---------|-------------|
| **ISO 31000** | 2018 | Management du risque - Principes et lignes directrices |
| **COSO ERM** | 2017 | Enterprise Risk Management - Cadre intégré |
| **Référentiel BCEAO** | 2024 | Dispositif de gestion des risques et de contrôle interne |
| **Normes IIA** | 2021 | Professional Practices Framework (PPF) |
| **Bâle III** | 2023 | Adéquation des fonds propres et risques bancaires |

### Exigences Réglementaires UMOA

Pour les établissements bancaires de l'UMOA, la cartographie des risques doit :

1. ✅ Couvrir tous les processus critiques
2. ✅ Être mise à jour annuellement (ou après événement majeur)
3. ✅ Être validée par le Comité des Risques
4. ✅ Faire l'objet d'une revue par l'Audit Interne
5. ✅ Être communiquée à la Commission Bancaire sur demande

---

## 🧪 Tests et Validation

### Tests Unitaires

```bash
# Exécuter les tests
python -m pytest tests/

# Avec couverture de code
python -m pytest tests/ --cov=json2word_cartographie_risques
```

### Validation des Données

Le script valide automatiquement :
- ✅ Format JSON valide
- ✅ Présence des tables 1 et 2
- ✅ Structure des données conforme
- ✅ Niveaux de risque cohérents

---

## 🐛 Dépannage

### Erreur : Module python-docx non trouvé

```bash
pip install python-docx
```

### Erreur : Fichier JSON invalide

Vérifiez la structure JSON avec un validateur en ligne : [jsonlint.com](https://jsonlint.com/)

### Tableau trop large pour la page

Réduisez les largeurs de colonnes dans la liste `largeurs_colonnes` :

```python
largeurs_colonnes = [
    1.3,  # Réduire de 1.5 à 1.3
    1.0,  # Réduire de 1.3 à 1.0
    # ...
]
```

---

## 📞 Support et Contact

- **Équipe** : Afrika Group Holdings - Département Audit & Contrôle Interne
- **Documentation** : [README.md](README.md)
- **Exemples** : Dossier `exemples/`

---

## 📄 Licence

© 2026 Afrika Group Holdings. Tous droits réservés.

Document confidentiel - Usage interne uniquement.

---

## 🔄 Historique des Versions

| Version | Date | Modifications |
|---------|------|---------------|
| **1.0.0** | 31 oct 2026 | Version initiale - 20 colonnes, heat map, conformité ISO 31000 |

---

**Généré avec ❤️ par l'équipe Audit & Contrôle Interne d'Afrika Group Holdings**
