# 📝 MÉMO : Création et Exécution de Skills

## 📋 Informations Générales

**Sujet :** Guide complet de création de skills - De la modélisation à l'exécution  
**Date :** 31 octobre 2026  
**Version :** 1.0.0  
**Auteur :** Expert Python & Document Automation

---

## 🎯 Objectifs de ce Mémo

1. ✅ Expliquer comment transformer un **skill nature Claude** en **skill normal**
2. ✅ Décrire la structure et les composants d'un skill
3. ✅ Fournir les étapes de modélisation détaillées
4. ✅ Guider l'exécution du skill dans **Miniconda**
5. ✅ Documenter les bonnes pratiques et pièges à éviter

---

## 📚 Table des Matières

1. [Qu'est-ce qu'un Skill ?](#quest-ce-quun-skill)
2. [Types de Skills](#types-de-skills)
3. [Transformation Skill Nature Claude → Skill Normal](#transformation-skill-nature-claude--skill-normal)
4. [Structure d'un Skill Normal](#structure-dun-skill-normal)
5. [Étapes de Modélisation](#étapes-de-modélisation)
6. [Exécution dans Miniconda](#exécution-dans-miniconda)
7. [Validation et Tests](#validation-et-tests)
8. [Bonnes Pratiques](#bonnes-pratiques)
9. [Cas Pratique : audit-procedures-json2word](#cas-pratique--audit-procedures-json2word)

---

## 1. Qu'est-ce qu'un Skill ?

### Définition

Un **skill** est un module fonctionnel réutilisable qui :
- Résout un problème spécifique
- Contient du code exécutable (Python, JavaScript, etc.)
- Inclut de la documentation
- Peut être partagé et réutilisé

### Composants d'un Skill

```
mon-skill/
├── SKILL.md                    # Documentation principale
├── script_principal.py         # Code exécutable
├── prompt_agent.md             # Prompt pour agents IA (optionnel)
├── assets/                     # Fichiers d'exemple
│   ├── exemple_input.json
│   └── exemple_output.docx
└── tests/                      # Tests unitaires (optionnel)
    └── test_script.py
```

### Types de Skills

| Type | Description | Exemple |
|------|-------------|---------|
| **Conversion** | Transforme des données d'un format à un autre | JSON → Word, Excel → PDF |
| **Analyse** | Traite et analyse des données | Analyse de logs, extraction de données |
| **Génération** | Crée du contenu | Génération de rapports, création de documents |
| **Automation** | Automatise des tâches répétitives | Backup, déploiement, tests |

---

## 2. Types de Skills

### 2.1 Skill Nature Claude

**Définition :** Un skill natif Claude est un format spécifique utilisé par l'assistant Claude, souvent sous forme de fichier `.skill` (format ZIP compressé).

**Caractéristiques :**
- 📦 Format compressé (ZIP avec extension `.skill`)
- 📝 Documentation intégrée (SKILL.md)
- 🐍 Scripts Python ou autres langages
- 📊 Exemples et assets inclus
- 🤖 Prompt pour agents IA

**Exemple de structure interne :**
```
eprocedure-json2word.skill (ZIP)
├── SKILL.md
├── json2word_audit.py
├── prompt_agent_code_local.md
└── assets/
    ├── exemple_input.json
    └── exemple_output.docx
```

**Avantages :**
- ✅ Packaging complet
- ✅ Distribution facile (1 seul fichier)
- ✅ Compatible avec l'écosystème Claude

**Inconvénients :**
- ❌ Nécessite décompression pour utiliser
- ❌ Difficile à modifier sans re-zipper
- ❌ Moins accessible pour les développeurs

### 2.2 Skill Normal (Décompressé)

**Définition :** Un skill normal est un dossier organisé contenant tous les fichiers accessibles directement.

**Caractéristiques :**
- 📁 Dossier structuré
- 📝 Fichiers accessibles directement
- 🔧 Facile à modifier et personnaliser
- 📚 Documentation séparée

**Exemple de structure :**
```
audit-procedures-json2word/
├── audit-procedures-json2word.skill.md
├── json2word_audit.py
├── README_AUDIT_PROCEDURES.md
├── prompt_agent_code_local.md
├── assets/
│   └── exemple_manuel_procedures_audit.json
└── sortie_word/
```

**Avantages :**
- ✅ Facile à modifier
- ✅ Pas de décompression nécessaire
- ✅ Visible dans l'explorateur de fichiers
- ✅ Compatible Git/versioning

**Inconvénients :**
- ❌ Multiple fichiers à gérer
- ❌ Distribution moins pratique

---

## 3. Transformation Skill Nature Claude → Skill Normal

### 🔄 Processus de Transformation

#### Étape 1 : Décompression du Skill Claude

```bash
# Méthode 1 : Renommer et décompresser
# Renommer le fichier .skill en .zip
ren eprocedure-json2word.skill eprocedure-json2word.zip

# Extraire le contenu
Expand-Archive -Path eprocedure-json2word.zip -DestinationPath skill_decompresse

# Méthode 2 : Utiliser 7-Zip ou WinRAR
# Clic droit sur le fichier .skill > Extraire ici
```

#### Étape 2 : Analyse de la Structure

```bash
# Lister le contenu extrait
cd skill_decompresse
ls -R
```

**Identifier les composants :**
1. 📝 **SKILL.md** : Documentation principale
2. 🐍 **Scripts** : Fichiers .py, .js, etc.
3. 📊 **Assets** : Exemples, données de test
4. 📋 **Prompt** : Fichiers pour agents IA

#### Étape 3 : Restructuration

```
Avant (Skill Claude)          Après (Skill Normal)
───────────────────          ─────────────────────
skill.zip/                   mon-skill/
├── SKILL.md          →      ├── mon-skill.skill.md
├── script.py         →      ├── script.py
├── prompt.md         →      ├── prompt_agent.md
└── assets/           →      ├── README_UTILISATEUR.md
    └── exemple.json         ├── GUIDE_MODELISATION.md
                             ├── assets/
                             │   └── exemple.json
                             └── sortie/
```

#### Étape 4 : Enrichissement de la Documentation

**Créer des fichiers supplémentaires :**

1. **README_UTILISATEUR.md**
   - Guide d'installation
   - Utilisation du skill
   - Exemples pratiques
   - Dépannage

2. **GUIDE_MODELISATION.md**
   - Structure des données
   - Configuration technique
   - Personnalisation
   - Extension du skill

3. **INDEX_DOCUMENTATION.md**
   - Table des matières
   - Références croisées
   - Guide de navigation

4. **RAPPORT_EXECUTION.md**
   - Exemple d'exécution
   - Résultats de validation
   - Contrôles de qualité

#### Étape 5 : Adaptation du Code (si nécessaire)

**Vérifier et adapter :**

```python
# Avant (Skill Claude - chemins relatifs au ZIP)
import os
script_dir = os.path.dirname(__file__)
asset_path = os.path.join(script_dir, "assets", "exemple.json")

# Après (Skill Normal - chemins relatifs au dossier)
from pathlib import Path
script_dir = Path(__file__).parent
asset_path = script_dir / "assets" / "exemple.json"
```

#### Étape 6 : Validation de la Transformation

**Checklist de validation :**
- [ ] Tous les fichiers extraits et accessibles
- [ ] Scripts Python exécutables sans erreur
- [ ] Documentation complète (SKILL.md + README)
- [ ] Exemples fournis et fonctionnels
- [ ] Structure logique et claire
- [ ] Chemins de fichiers corrects

---

## 4. Structure d'un Skill Normal

### 4.1 Architecture Recommandée

```
mon-skill/
│
├── 📘 DOCUMENTATION (3-6 fichiers)
│   ├── mon-skill.skill.md              # Documentation technique complète
│   ├── README_UTILISATEUR.md           # Guide utilisateur
│   ├── GUIDE_MODELISATION.md           # Guide de modélisation (optionnel)
│   ├── INDEX_DOCUMENTATION.md          # Index de navigation (optionnel)
│   └── COMPARAISON_VERSIONS.md         # Comparaison avec versions précédentes (optionnel)
│
├── 🐍 CODE EXÉCUTABLE (1-N fichiers)
│   ├── script_principal.py             # Script principal
│   ├── utilitaires.py                  # Fonctions utilitaires (optionnel)
│   └── configuration.py                # Configuration (optionnel)
│
├── 🤖 PROMPTS AGENTS (optionnel)
│   └── prompt_agent_code_local.md      # Prompt pour agents IA
│
├── 📊 ASSETS / EXEMPLES
│   ├── exemple_input.json              # Exemple d'entrée
│   ├── exemple_output.docx             # Exemple de sortie
│   └── template.json                   # Template réutilisable
│
├── 📤 SORTIE (créé automatiquement)
│   └── documents_generes/
│
└── 🧪 TESTS (optionnel)
    ├── test_script.py                  # Tests unitaires
    └── test_data/                      # Données de test
```

### 4.2 Fichier SKILL.md (Documentation Technique)

**Structure type :**

```markdown
# Skill: mon-skill

## Metadata
- Name: mon-skill
- Version: 1.0.0
- Author: Nom de l'auteur
- Description: Description courte
- Tags: tag1, tag2, tag3
- Dependencies: python-docx, pandas

## Purpose
Description détaillée du problème résolu

## Input Format
Structure des données d'entrée

## Output Format
Structure des données de sortie

## Technical Implementation
Configuration et code technique

## Usage Examples
Exemples d'utilisation CLI

## Error Handling
Gestion des erreurs

## Best Practices
Bonnes pratiques

## Extending the Skill
Guide de personnalisation

## Limitations
Limites connues

## Testing
Tests unitaires et validation

## License & Attribution
Licence et crédits
```

### 4.3 Fichier README_UTILISATEUR.md (Guide Pratique)

**Structure type :**

```markdown
# Guide d'utilisation : mon-skill

## Vue d'ensemble
Introduction et objectifs

## Installation
Prérequis et dépendances

## Format des données
Détail des champs et structure

## Utilisation
Commandes CLI avec exemples

## Format de sortie
Spécifications du résultat

## Validation et contrôle qualité
Règles de validation

## Personnalisation avancée
Modification de la configuration

## Dépannage
Erreurs communes et solutions

## Ressources complémentaires
Liens et références

## Support
Contact et assistance
```

---

## 5. Étapes de Modélisation

### Phase 1 : Analyse du Besoin

#### 1.1 Identifier le Problème

**Questions à se poser :**
- Quel problème spécifique ce skill résout-il ?
- Quelles sont les données d'entrée ?
- Quel est le résultat attendu ?
- Quels sont les cas d'usage principaux ?

**Exemple (audit-procedures-json2word) :**
```
Problème : Convertir des procédures d'audit JSON en documents Word professionnels
Entrée   : Fichier JSON avec structure spécifique (table 1 + table 2)
Sortie   : Document Word au format E-procedure (A4 paysage, tables formatées)
Cas      : Manuels d'audit, cartographies de risques, FRAP
```

#### 1.2 Définir la Structure de Données

**JSON d'entrée :**
```json
{
  "Cle principale": [
    {"table 1": {...}},
    {"table 2": [...]}
  ]
}
```

**Document de sortie :**
- Format : Word .docx
- Orientation : Paysage
- Tables : 2 (métadonnées + détails)
- Style : E-procedure standardisé

### Phase 2 : Analyse du Skill Existant (si applicable)

#### 2.1 Décompresser le Skill Claude

```bash
# Extraire le contenu
Expand-Archive -Path skill-existant.skill -DestinationPath analyse_skill
cd analyse_skill
```

#### 2.2 Lire et Comprendre le Code

**Identifier :**
1. **Point d'entrée** : Fonction `main()` ou script principal
2. **Configuration** : Constantes, dictionnaires de configuration
3. **Dépendances** : `import` et bibliothèques utilisées
4. **Logique métier** : Fonctions de traitement

**Exemple (json2word_audit.py) :**
```python
# Point d'entrée
def main(argv=None):
    ap = argparse.ArgumentParser(...)
    args = ap.parse_args(argv)
    convert(args.json, args.out_dir, ...)

# Configuration clé
COLUMN_SPECS = {
    "Colonne JSON": ("Label Word", largeur_DXA, "type_rendu"),
    ...
}

# Dépendances
from docx import Document
from docx.shared import Pt, RGBColor
```

#### 2.3 Vérifier la Compatibilité

**Checklist :**
- [ ] Le code Python est-il compatible avec votre version Python ?
- [ ] Les bibliothèques sont-elles disponibles ?
- [ ] La structure JSON attendue est-elle documentée ?
- [ ] Les exemples fournis sont-ils fonctionnels ?

### Phase 3 : Modélisation de la Structure JSON

#### 3.1 Analyser les Données Fournies

**Pour chaque niveau de structure :**

1. **Identifier les clés** (noms exacts, sensibles à la casse)
2. **Déterminer les types** (string, number, object, array)
3. **Noter les valeurs spéciales** (null, imbriquées, multilignes)

**Exemple :**
```json
{
  "Etape mission - Manuel des procedures": [          ← Array principal
    {
      "table 1": {                                    ← Object (métadonnées)
        "Etape de mission": "...",                    ← String obligatoire
        "Norme": {                                    ← Object imbriqué
          "Norme 1": "...",                           ← Sous-clés dynamiques
          "Norme 2": "..."
        }
      }
    },
    {
      "table 2": [                                    ← Array (liste d'objets)
        {
          "Colonne 1": "...",                         ← String
          "Colonne 2": "Action 1\nAction 2"          ← Multiligne (\n)
        }
      ]
    }
  ]
}
```

#### 3.2 Créer un Template JSON

**Fichier : `template_structure.json`**

```json
{
  "Cle_principale": [
    {
      "table 1": {
        "Champ_1": "Valeur exemple",
        "Champ_2": "Valeur exemple",
        "Champ_objet": {
          "Sous_champ_1": "Valeur",
          "Sous_champ_2": "Valeur"
        }
      }
    },
    {
      "table 2": [
        {
          "Colonne_1": "Valeur",
          "Colonne_2": "Valeur multiligne\nLigne 2\nLigne 3",
          "Colonne_3": "Val1, Val2, Val3"
        }
      ]
    }
  ]
}
```

#### 3.3 Documenter les Champs

**Tableau de spécification :**

| Champ JSON | Type | Obligatoire | Format | Description |
|------------|------|-------------|--------|-------------|
| Cle_principale | string | ✅ | `"Etape mission - [Titre]"` | Clé racine |
| table 1 | object | ✅ | Dictionnaire | Métadonnées |
| Champ_1 | string | ✅ | Texte libre | Description |
| Champ_objet | object | ⚪ | Sous-dictionnaire | Valeurs imbriquées |
| table 2 | array | ✅ | Liste d'objets | Données détaillées |
| Colonne_1 | string | ✅ | Texte | Première colonne |
| Colonne_2 | string | ✅ | Multiligne (`\n`) | Actions |
| Colonne_3 | string | ⚪ | CSV (`, `) | Valeurs séparées |

### Phase 4 : Configuration du Script

#### 4.1 Adapter COLUMN_SPECS (pour skills Word)

**Structure :**
```python
COLUMN_SPECS = {
    "Nom_colonne_JSON": ("Label_Word", largeur_DXA, "type_rendu"),
    ...
}
```

**Types de rendu :**
- `"text"` : Texte simple
- `"bold"` : Texte en gras
- `"nl"` : Multiligne avec puces (séparation `\n`)
- `"csv"` : CSV en puces (séparation `, `)

**Calcul des largeurs :**
```
Largeur totale : 15000 DXA (A4 paysage)
1 DXA ≈ 0.05 mm
Exemple : 3000 DXA ≈ 15 cm
```

**Exemple :**
```python
COLUMN_SPECS = {
    "Étape méthodologique":            ("Etape",      1900, "bold"),
    "Acteur audit":                    ("Acteur",     1500, "text"),
    "Traitement et diligences":        ("Traitement", 5100, "nl"),
    "Document probant":                ("Document",   2300, "csv"),
    "Norme IIA / CRIPP":               ("Normes",     1700, "text"),
    "Extrait de la norme":             ("Extrait",    2500, "text"),
}
# Total : 1900 + 1500 + 5100 + 2300 + 1700 + 2500 = 15000 DXA ✓
```

#### 4.2 Configurer les Couleurs et Styles

```python
# Couleurs (format hexadécimal sans #)
BORDEAUX = "7B1E3A"  # Fond en-têtes tableau
LIGHT = "F2E6EA"     # Fond colonne Rubrique
GREY = "999999"      # Bordures visibles
WHITE = "FFFFFF"     # Bordures invisibles

# Typographie
FONT = "Calibri"
FONT_SIZE = 9  # points

# Textes par défaut
DEFAULT_SOFTWARE = "Nom de mon logiciel"
DEFAULT_FOOTER = "Pied de page personnalisé"
```

### Phase 5 : Création des Exemples

#### 5.1 Créer un Exemple JSON Réaliste

**Fichier : `assets/exemple_complet.json`**

```json
{
  "Etape mission - Exemple complet": [
    {
      "table 1": {
        "Etape de mission": "Phase de test",
        "Document": "Document de démonstration",
        "Processus": "Processus exemple",
        "Reference": "EX-001",
        "Version": "V1.0",
        "Norme": {
          "Norme 1": "Première norme applicable",
          "Norme 2": "Deuxième norme applicable"
        }
      }
    },
    {
      "table 2": [
        {
          "Colonne 1": "Première étape",
          "Colonne 2": "Responsable A",
          "Colonne 3": "- Action 1\n- Action 2\n- Action 3",
          "Colonne 4": "Document A, Document B",
          "Colonne 5": "Norme X.Y",
          "Colonne 6": "Extrait de la norme expliquant..."
        },
        {
          "Colonne 1": "Deuxième étape",
          "Colonne 2": "Responsable B",
          "Colonne 3": "- Action 4\n- Action 5",
          "Colonne 4": "Document C",
          "Colonne 5": "Norme Z.W",
          "Colonne 6": "Autre extrait normatif..."
        }
      ]
    }
  ]
}
```

#### 5.2 Tester avec l'Exemple

```bash
# Tester la conversion
conda activate pdf_excel_env
python script_principal.py "assets/exemple_complet.json" --ref TEST001 -o sortie_test
```

### Phase 6 : Documentation

#### 6.1 Rédiger la Documentation Technique (SKILL.md)

**Sections obligatoires :**
1. Metadata (nom, version, tags, dépendances)
2. Purpose (objectif du skill)
3. Input Format (structure JSON détaillée)
4. Output Format (spécifications de sortie)
5. Technical Implementation (configuration)
6. Usage Examples (exemples CLI)
7. Validation Rules (règles de contrôle)

#### 6.2 Rédiger le Guide Utilisateur (README.md)

**Sections obligatoires :**
1. Vue d'ensemble
2. Installation (prérequis, dépendances)
3. Format des données (tableaux détaillés)
4. Utilisation (commandes avec exemples)
5. Dépannage (erreurs communes)

#### 6.3 Créer l'Index de Navigation

**Fichier : `INDEX_DOCUMENTATION.md`**

```markdown
# Index de la Documentation

## Fichiers Disponibles

1. **mon-skill.skill.md** - Documentation technique
2. **README_UTILISATEUR.md** - Guide pratique
3. **GUIDE_MODELISATION.md** - Guide de modélisation

## Ordre de Lecture Recommandé

### Pour Démarrer
1. INDEX_DOCUMENTATION.md (ce fichier)
2. README_UTILISATEUR.md
3. assets/exemple_complet.json

### Pour Comprendre
1. mon-skill.skill.md
2. GUIDE_MODELISATION.md
3. script_principal.py
```

---

## 6. Exécution dans Miniconda

### 6.1 Qu'est-ce que Miniconda ?

**Miniconda** est une version minimale de Anaconda, un gestionnaire d'environnements Python qui permet :
- ✅ Créer des environnements isolés
- ✅ Installer des packages spécifiques par projet
- ✅ Éviter les conflits de versions
- ✅ Gérer plusieurs versions de Python

### 6.2 Vérification de l'Installation

```bash
# Vérifier que conda est installé
conda --version

# Résultat attendu : conda X.Y.Z
```

**Si conda n'est pas installé :**
1. Télécharger Miniconda : https://docs.conda.io/en/latest/miniconda.html
2. Installer pour Windows, macOS ou Linux
3. Redémarrer le terminal

### 6.3 Liste des Environnements Existants

```bash
# Lister tous les environnements conda
conda env list

# Résultat exemple :
# conda environments:
# base                 *   C:\Users\LEADER\miniconda3
# pdf_excel_env            C:\Users\LEADER\miniconda3\envs\pdf_excel_env
```

**Symboles :**
- `*` = environnement actif
- Sans `*` = environnement disponible mais inactif

### 6.4 Créer un Nouvel Environnement (si nécessaire)

```bash
# Créer un environnement pour le skill
conda create -n mon_skill_env python=3.11

# Répondre 'y' pour confirmer
```

**Paramètres :**
- `-n mon_skill_env` : Nom de l'environnement
- `python=3.11` : Version de Python

### 6.5 Activer l'Environnement

```bash
# Activer l'environnement
conda activate pdf_excel_env

# Le prompt change pour indiquer l'environnement actif :
# (pdf_excel_env) PS C:\Users\...>
```

**Vérifications :**
```bash
# Vérifier la version de Python dans l'environnement
python --version
# Résultat : Python 3.11.18

# Lister les packages installés
pip list
```

### 6.6 Installer les Dépendances du Skill

#### Méthode 1 : Installation Manuelle

```bash
# Activer l'environnement
conda activate pdf_excel_env

# Installer les packages nécessaires
pip install python-docx
pip install pandas
pip install openpyxl
```

#### Méthode 2 : Fichier requirements.txt

**Créer le fichier `requirements.txt` :**
```txt
python-docx>=1.2.0
pandas>=2.0.0
openpyxl>=3.1.0
```

**Installer depuis le fichier :**
```bash
conda activate pdf_excel_env
pip install -r requirements.txt
```

#### Méthode 3 : Fichier environment.yml (Conda)

**Créer le fichier `environment.yml` :**
```yaml
name: mon_skill_env
channels:
  - defaults
  - conda-forge
dependencies:
  - python=3.11
  - pip
  - pip:
    - python-docx>=1.2.0
    - pandas>=2.0.0
    - openpyxl>=3.1.0
```

**Créer l'environnement depuis le fichier :**
```bash
conda env create -f environment.yml
conda activate mon_skill_env
```

### 6.7 Vérifier les Dépendances Installées

```bash
# Vérifier un package spécifique
pip show python-docx

# Résultat :
# Name: python-docx
# Version: 1.2.0
# Summary: Create, read, and update Microsoft Word .docx files.
# ...
```

### 6.8 Exécuter le Skill

#### Étape 1 : Se Placer dans le Dossier du Skill

```bash
# Naviguer vers le dossier
cd "h:\Projet_pdf_excel\Modelisation claude skill"

# Vérifier le contenu
ls
```

#### Étape 2 : Activer l'Environnement

```bash
conda activate pdf_excel_env
```

#### Étape 3 : Exécuter le Script

**Syntaxe générale :**
```bash
python script_principal.py [FICHIER_ENTREE] [OPTIONS]
```

**Exemple (audit-procedures-json2word) :**
```bash
# Exécution simple
python json2word_audit.py "assets\exemple_manuel_procedures_audit.json"

# Avec options
python json2word_audit.py "assets\exemple_manuel_procedures_audit.json" \
    --ref A210 \
    -o sortie_word

# Avec toutes les options
python json2word_audit.py "assets\exemple_manuel_procedures_audit.json" \
    --ref A210 \
    --software "Mon Logiciel" \
    --footer "Mon pied de page" \
    --no-blank-rows \
    -o sortie_word
```

#### Étape 4 : Vérifier le Résultat

```bash
# Lister les fichiers générés
ls sortie_word

# Résultat attendu :
# A210-Titre_document- Mon Logiciel.docx
```

### 6.9 Dépannage Miniconda

#### Problème 1 : Conda Non Reconnu

**Erreur :**
```
'conda' n'est pas reconnu en tant que commande interne...
```

**Solution :**
```bash
# Ajouter conda au PATH (Windows)
# 1. Ouvrir "Modifier les variables d'environnement système"
# 2. Variables d'environnement > Path > Modifier
# 3. Ajouter : C:\Users\LEADER\miniconda3\Scripts
# 4. Ajouter : C:\Users\LEADER\miniconda3
# 5. Redémarrer le terminal
```

#### Problème 2 : Environnement Non Trouvé

**Erreur :**
```
Could not find conda environment: mon_skill_env
```

**Solution :**
```bash
# Vérifier les environnements existants
conda env list

# Si l'environnement n'existe pas, le créer
conda create -n mon_skill_env python=3.11
```

#### Problème 3 : Package Non Trouvé

**Erreur :**
```
ModuleNotFoundError: No module named 'docx'
```

**Solution :**
```bash
# Vérifier que l'environnement est activé
conda activate pdf_excel_env

# Installer le package manquant
pip install python-docx

# Vérifier l'installation
pip show python-docx
```

#### Problème 4 : Conflit de Versions

**Erreur :**
```
ERROR: pip's dependency resolver does not currently take into account...
```

**Solution :**
```bash
# Créer un nouvel environnement propre
conda create -n mon_skill_env_v2 python=3.11
conda activate mon_skill_env_v2

# Installer les packages dans l'ordre
pip install python-docx
pip install pandas
```

### 6.10 Commandes Utiles Miniconda

| Commande | Description |
|----------|-------------|
| `conda env list` | Lister les environnements |
| `conda activate ENV` | Activer un environnement |
| `conda deactivate` | Désactiver l'environnement actuel |
| `conda create -n ENV python=3.11` | Créer un nouvel environnement |
| `conda remove -n ENV --all` | Supprimer un environnement |
| `conda update conda` | Mettre à jour conda |
| `pip list` | Lister les packages installés |
| `pip install PACKAGE` | Installer un package |
| `pip uninstall PACKAGE` | Désinstaller un package |
| `pip freeze > requirements.txt` | Exporter les dépendances |

---

## 7. Validation et Tests

### 7.1 Tests Manuels

#### Test 1 : Exécution Simple

```bash
# 1. Activer l'environnement
conda activate pdf_excel_env

# 2. Exécuter avec l'exemple
python script_principal.py "assets/exemple.json" -o test_sortie

# 3. Vérifier que le fichier est créé
ls test_sortie
```

**Résultat attendu :** Fichier créé sans erreur

#### Test 2 : Validation du Contenu

**Créer un script de validation :**

```python
# verifier_resultat.py
from docx import Document

# Ouvrir le document généré
doc = Document('test_sortie/resultat.docx')

# Vérifications
print(f"Nombre de tables: {len(doc.tables)}")
print(f"Nombre de paragraphes: {len(doc.paragraphs)}")
print(f"En-tête: {doc.sections[0].header.paragraphs[0].text}")

# Tests spécifiques
assert len(doc.tables) == 2, "Nombre de tables incorrect"
print("✅ Tous les tests passés")
```

**Exécuter :**
```bash
python verifier_resultat.py
```

### 7.2 Tests Automatisés

#### Créer des Tests Unitaires

**Fichier : `tests/test_skill.py`**

```python
import unittest
from pathlib import Path
import json
import sys

# Ajouter le dossier parent au path
sys.path.insert(0, str(Path(__file__).parent.parent))

from script_principal import convert, load_json

class TestSkill(unittest.TestCase):
    
    def setUp(self):
        """Préparation avant chaque test"""
        self.test_json = Path("assets/exemple.json")
        self.test_output = Path("test_output")
        self.test_output.mkdir(exist_ok=True)
    
    def test_load_json(self):
        """Test du chargement JSON"""
        data = load_json(self.test_json)
        self.assertIsInstance(data, dict)
        self.assertIn("Cle_principale", data)
    
    def test_convert(self):
        """Test de la conversion"""
        output = convert(
            self.test_json,
            self.test_output,
            reference="TEST001",
            software="Test Software"
        )
        self.assertTrue(output.exists())
    
    def test_output_structure(self):
        """Test de la structure du document"""
        from docx import Document
        output = self.test_output / "TEST001-Document- Test Software.docx"
        doc = Document(str(output))
        
        # Vérifications
        self.assertEqual(len(doc.tables), 2, "Nombre de tables incorrect")
        self.assertEqual(len(doc.tables[0].columns), 2, "Table 1 : colonnes")
        self.assertGreater(len(doc.tables[1].columns), 0, "Table 2 : colonnes")
    
    def tearDown(self):
        """Nettoyage après chaque test"""
        import shutil
        if self.test_output.exists():
            shutil.rmtree(self.test_output)

if __name__ == "__main__":
    unittest.main()
```

#### Exécuter les Tests

```bash
# Activer l'environnement
conda activate pdf_excel_env

# Exécuter tous les tests
python -m unittest tests/test_skill.py

# Exécuter avec verbosité
python -m unittest tests/test_skill.py -v
```

### 7.3 Checklist de Validation

**Avant de considérer le skill comme prêt :**

- [ ] **Code**
  - [ ] Le script s'exécute sans erreur
  - [ ] Toutes les dépendances sont documentées
  - [ ] Les chemins de fichiers sont corrects
  - [ ] La gestion des erreurs est implémentée

- [ ] **Documentation**
  - [ ] SKILL.md complet (toutes sections)
  - [ ] README_UTILISATEUR.md rédigé
  - [ ] Exemples fournis et fonctionnels
  - [ ] INDEX_DOCUMENTATION.md créé

- [ ] **Tests**
  - [ ] Exemple JSON testé et validé
  - [ ] Résultat conforme aux spécifications
  - [ ] Tests unitaires écrits (optionnel)
  - [ ] Validation automatique fonctionnelle

- [ ] **Packaging**
  - [ ] Structure de dossiers logique
  - [ ] requirements.txt ou environment.yml fourni
  - [ ] Fichiers d'exemple inclus
  - [ ] Dossier de sortie créé automatiquement

---

## 8. Bonnes Pratiques

### 8.1 Structure de Code

#### ✅ À Faire

```python
# 1. Utiliser pathlib pour les chemins
from pathlib import Path
script_dir = Path(__file__).parent
input_file = script_dir / "assets" / "exemple.json"

# 2. Gérer les erreurs proprement
try:
    data = load_json(input_file)
except FileNotFoundError:
    print(f"Erreur : Fichier non trouvé : {input_file}")
    sys.exit(1)
except json.JSONDecodeError as e:
    print(f"Erreur : JSON invalide : {e}")
    sys.exit(1)

# 3. Utiliser argparse pour les arguments CLI
import argparse
parser = argparse.ArgumentParser(description="Description du skill")
parser.add_argument("input", type=Path, help="Fichier d'entrée")
parser.add_argument("-o", "--output", type=Path, default=Path("."))
args = parser.parse_args()

# 4. Documenter les fonctions
def convert(input_file: Path, output_dir: Path) -> Path:
    """
    Convertit un fichier JSON en document Word.
    
    Args:
        input_file: Chemin du fichier JSON d'entrée
        output_dir: Dossier de sortie pour le document
    
    Returns:
        Chemin du fichier Word généré
    
    Raises:
        ValueError: Si le JSON est invalide
        FileNotFoundError: Si le fichier n'existe pas
    """
    pass
```

#### ❌ À Éviter

```python
# 1. Chemins en dur
input_file = "C:\\Users\\User\\Documents\\fichier.json"  # ❌

# 2. Ignorer les erreurs
data = json.loads(text)  # ❌ Pas de try/except

# 3. Arguments sans validation
import sys
input_file = sys.argv[1]  # ❌ Pas de vérification

# 4. Fonctions sans documentation
def convert(f, o):  # ❌ Noms cryptiques, pas de docstring
    pass
```

### 8.2 Documentation

#### ✅ À Faire

- ✅ Documenter **toutes** les fonctions publiques
- ✅ Fournir des **exemples concrets** et testés
- ✅ Expliquer les **erreurs possibles** et leurs solutions
- ✅ Créer un **index de navigation** pour les gros projets
- ✅ Inclure des **captures d'écran** si pertinent

#### ❌ À Éviter

- ❌ Documentation vague ("Convertit des données")
- ❌ Exemples qui ne fonctionnent pas
- ❌ Absence de section dépannage
- ❌ Documentation obsolète

### 8.3 Gestion des Versions

#### Versionning Sémantique

```
Format : MAJEUR.MINEUR.CORRECTIF

Exemples :
1.0.0 → Version initiale stable
1.1.0 → Ajout de fonctionnalités (rétrocompatible)
1.1.1 → Correction de bugs
2.0.0 → Changements incompatibles
```

#### Changelog

**Fichier : `CHANGELOG.md`**

```markdown
# Changelog

## [1.1.0] - 2026-11-15
### Ajouté
- Support des colonnes personnalisées
- Option --no-blank-rows

### Modifié
- Amélioration de la gestion des erreurs

### Corrigé
- Bug sur les accents dans les noms de fichiers

## [1.0.0] - 2026-10-31
### Ajouté
- Version initiale du skill
- Support JSON → Word
- 6 colonnes prédéfinies
```

### 8.4 Organisation des Fichiers

#### ✅ Structure Recommandée

```
mon-skill/
├── mon-skill.skill.md              # Documentation technique
├── README.md                        # Guide de démarrage rapide
├── README_UTILISATEUR.md            # Guide utilisateur complet
├── CHANGELOG.md                     # Historique des versions
├── requirements.txt                 # Dépendances Python
├── environment.yml                  # Environnement Conda (optionnel)
│
├── script_principal.py              # Code principal
├── utilitaires.py                   # Fonctions utilitaires (optionnel)
│
├── assets/                          # Fichiers d'exemple
│   ├── exemple_complet.json
│   └── template.json
│
├── sortie/                          # Dossier de sortie (créé auto)
│
└── tests/                           # Tests (optionnel)
    ├── test_skill.py
    └── test_data/
```

### 8.5 Sécurité et Bonnes Pratiques

#### ✅ À Faire

1. **Valider les entrées**
   ```python
   if not input_file.exists():
       raise FileNotFoundError(f"Fichier introuvable : {input_file}")
   
   if not input_file.suffix == ".json":
       raise ValueError("Le fichier doit être au format JSON")
   ```

2. **Utiliser des chemins relatifs**
   ```python
   # ✅ Bien
   script_dir = Path(__file__).parent
   asset = script_dir / "assets" / "exemple.json"
   
   # ❌ Mal
   asset = "C:\\Users\\Moi\\Projet\\assets\\exemple.json"
   ```

3. **Encoder en UTF-8**
   ```python
   with open(file, "r", encoding="utf-8") as f:
       data = json.load(f)
   ```

4. **Nettoyer les ressources**
   ```python
   try:
       file = open("data.json", "r")
       data = file.read()
   finally:
       file.close()
   
   # Ou mieux : utiliser un context manager
   with open("data.json", "r") as f:
       data = f.read()
   ```

#### ❌ À Éviter

- ❌ Exécuter du code non validé
- ❌ Stocker des credentials en dur dans le code
- ❌ Ignorer les erreurs avec `pass`
- ❌ Utiliser `eval()` ou `exec()` sur des données utilisateur

---

## 9. Cas Pratique : audit-procedures-json2word

### 9.1 Contexte du Projet

**Besoin :**
Convertir des procédures d'audit interne (format JSON) en documents Word professionnels conformes aux normes IIA/CRIPP 2025.

**Données d'entrée :**
```json
{
  "Etape mission - Manuel des procedures": [
    {
      "table 1": {
        "Etape de mission": "Manuel audit interne - Phase de préparation",
        "Norme": {
          "Norme 1": "Norme 1.1 Honnêteté",
          ...
        }
      }
    },
    {
      "table 2": [
        {
          "Étape méthodologique": "Cadrage initial",
          "Acteur audit": "Directeur AI",
          "Traitement et diligences d'audit": "- Action 1\n- Action 2",
          ...
        }
      ]
    }
  ]
}
```

**Résultat attendu :**
Document Word A4 paysage avec 2 tables formatées.

### 9.2 Analyse du Skill Existant

```bash
# 1. Décompresser le skill Claude
Expand-Archive -Path eprocedure-json2word.skill -DestinationPath analyse

# 2. Examiner le contenu
cd analyse
ls

# Résultat :
# SKILL.md
# json2word_audit.py
# prompt_agent_code_local.md
# assets/
```

**Découverte importante :**
Le script `json2word_audit.py` contient déjà la configuration exacte nécessaire !

```python
COLUMN_SPECS = {
    "Étape méthodologique":            ("Etape",      1900, "bold"),
    "Acteur audit":                    ("Acteur",     1500, "text"),
    "Traitement et diligences d'audit": ("Traitement", 5100, "nl"),
    "Document probant":                ("Document",   2300, "csv"),
    "Norme IIA / CRIPP":               ("Normes",     1700, "text"),
    "Extrait de la norme":             ("Extrait",    2500, "text"),
}
```

**Conclusion :** ✅ Le script est 100% réutilisable sans modification !

### 9.3 Modélisation de la Structure

#### Étape 1 : Créer le JSON Exemple

**Fichier : `assets/exemple_manuel_procedures_audit.json`**

Créé avec :
- Table 1 : 10 champs métadonnées
- Table 1 : Objet Norme avec 19 normes IIA/CRIPP
- Table 2 : 5 étapes méthodologiques complètes
- Données réalistes (Afrika Group Holdings, UMOA)

#### Étape 2 : Documentation Complète

**6 fichiers créés :**
1. `audit-procedures-json2word.skill.md` (2500 lignes)
2. `README_AUDIT_PROCEDURES.md` (800 lignes)
3. `SKILL_MODELISATION_COMPLETE.md` (850 lignes)
4. `COMPARAISON_SKILLS.md` (700 lignes)
5. `INDEX_DOCUMENTATION.md` (100 lignes)
6. `TACHE_ACCOMPLIE.md`

### 9.4 Exécution dans Miniconda

```bash
# 1. Vérifier les environnements
conda env list
# Résultat : pdf_excel_env existe déjà

# 2. Activer l'environnement
conda activate pdf_excel_env

# 3. Vérifier python-docx
pip show python-docx
# Résultat : Version 1.2.0 installée ✓

# 4. Créer le dossier de sortie
New-Item -ItemType Directory -Force -Path "sortie_word"

# 5. Exécuter la conversion
python json2word_audit.py "assets\exemple_manuel_procedures_audit.json" --ref A210 -o sortie_word

# 6. Résultat
# Fichier généré : sortie_word\A210-Manuel_audit_interne_-_Phase_de_préparation- Logiciel automatisé E-procedure.docx
```

### 9.5 Validation

**Script de validation créé : `verifier_document.py`**

```python
from docx import Document

doc = Document('sortie_word/A210-Manuel_audit_interne-...docx')

# Vérifications automatiques
checks = [
    ("Orientation paysage", doc.sections[0].page_width > doc.sections[0].page_height),
    ("2 tables présentes", len(doc.tables) == 2),
    ("Table 1 : 2 colonnes", len(doc.tables[0].columns) == 2),
    ("Table 2 : 6 colonnes", len(doc.tables[1].columns) == 6),
    # ... autres vérifications
]

# Résultat : ✅ 8/8 CONTRÔLES PASSÉS
```

### 9.6 Résultats

**Fichiers générés :**
- Document Word conforme aux spécifications
- 8/8 contrôles de validation passés
- Rapport d'exécution détaillé créé
- Documentation exhaustive (13 fichiers, ~5600 lignes)

**Temps total :**
- Modélisation : ~6h
- Documentation : ~2h
- Tests et validation : ~30min
- **Total : ~8h30**

---

## 📝 Récapitulatif Final

### Processus Complet : Skill Claude → Skill Normal

```
1. Décompression
   ├── Extraire le .skill (ZIP)
   └── Analyser le contenu

2. Analyse
   ├── Lire le code existant
   ├── Identifier la configuration
   └── Vérifier la compatibilité

3. Modélisation
   ├── Créer le JSON exemple
   ├── Documenter la structure
   └── Adapter la configuration (si besoin)

4. Documentation
   ├── Rédiger SKILL.md
   ├── Créer README utilisateur
   └── Ajouter guides et index

5. Tests
   ├── Exécuter dans Miniconda
   ├── Valider le résultat
   └── Créer rapport d'exécution

6. Finalisation
   ├── Vérifier la checklist
   ├── Créer CHANGELOG
   └── Packager (optionnel)
```

### Checklist Complète

**Phase 1 : Préparation**
- [ ] Skill Claude décompressé
- [ ] Code analysé et compris
- [ ] Dépendances identifiées
- [ ] Environnement Miniconda configuré

**Phase 2 : Modélisation**
- [ ] Structure JSON documentée
- [ ] Exemple JSON créé et testé
- [ ] Configuration adaptée (si nécessaire)
- [ ] Template fourni

**Phase 3 : Documentation**
- [ ] SKILL.md rédigé (toutes sections)
- [ ] README utilisateur créé
- [ ] Guide de modélisation écrit
- [ ] Index de navigation ajouté
- [ ] Exemples fournis et fonctionnels

**Phase 4 : Exécution**
- [ ] Environnement activé
- [ ] Dépendances installées
- [ ] Script exécuté avec succès
- [ ] Résultat validé (8+ contrôles)

**Phase 5 : Validation**
- [ ] Tests manuels effectués
- [ ] Script de validation créé
- [ ] Rapport d'exécution rédigé
- [ ] Documentation vérifiée

**Phase 6 : Finalisation**
- [ ] Structure de fichiers propre
- [ ] CHANGELOG créé
- [ ] README_PROJET_COMPLET.md rédigé
- [ ] Skill prêt à l'utilisation

---

## 🎓 Ressources Complémentaires

### Documentation Officielle

- **Python :** https://docs.python.org/
- **python-docx :** https://python-docx.readthedocs.io/
- **Miniconda :** https://docs.conda.io/en/latest/miniconda.html
- **Pandas :** https://pandas.pydata.org/docs/
- **JSON :** https://www.json.org/

### Outils Utiles

- **Validateur JSON :** https://jsonlint.com/
- **Éditeur Markdown :** https://stackedit.io/
- **Python Tutor :** https://pythontutor.com/

### Communautés

- **Stack Overflow :** https://stackoverflow.com/
- **Python Discord :** https://discord.gg/python
- **GitHub Discussions :** Chercher des projets similaires

---

## 📞 Support

**Pour toute question sur :**
- La transformation d'un skill Claude en skill normal
- La modélisation de structures JSON
- L'exécution dans Miniconda
- La création de documentation

**Contact :**
WhatsApp : +225 05 44 13 07 98  
Sujet : Création de skills et automatisation

---

## ✅ Conclusion

Ce mémo fournit un **guide complet** pour :

1. ✅ **Transformer** un skill nature Claude en skill normal
2. ✅ **Modéliser** des structures JSON complexes
3. ✅ **Exécuter** des skills dans Miniconda
4. ✅ **Documenter** exhaustivement
5. ✅ **Valider** avec des tests automatiques

**Résultat :** Un skill professionnel, documenté, testé et prêt à l'emploi.

---

**Version du mémo :** 1.0.0  
**Date :** 31 octobre 2026  
**Auteur :** Expert Python & Document Automation

**Ce mémo est un document de référence à conserver et consulter pour tout projet de création de skills. 📚**
