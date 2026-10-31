# Skill: audit-procedures-json2word

## Dependencies

### Installation Base (Cas 1 - Fichiers locaux)

```bash
pip install python-docx
```

### Installation Complète (Cas 2 - API N8N)

```bash
# Avec Conda (recommandé)
conda activate pdf_excel_env
pip install python-docx requests

# Ou avec pip standard
pip install python-docx requests
```

### Fichiers Requis

**Pour le Cas 1 (conversion simple) :**
- `json2word_audit.py` - Script de conversion principal

**Pour le Cas 2 (workflow N8N complet) :**
- `json2word_audit.py` - Script de conversion
- `execute_cas2_production.py` - Orchestrateur principal
- `api_call_n8n.py` - Module d'appel API
- `execute_cas2.bat` - Script batch Windows (optionnel)

**Configuration N8N (Cas 2 uniquement) :**
- N8N installé et démarré sur `http://localhost:5678`
- Workflow `skill_manuel_audit` configuré avec :
  - Webhook actif
  - Nœud "Edit Fields" avec champ `Data_integrale`
  - Nœud "Respond to Webhook"

## Metadata
- **Name**: audit-procedures-json2word
- **Version**: 1.2.0
- **Author**: Expert Python & Document Automation
- **Description**: Convertit des données JSON de procédures d'audit (Manuel des procédures d'audit interne) en documents Word professionnels au format E-procedure
- **Tags**: audit, json, word, automation, documentation, procedures
- **Dependencies**: python-docx, json, pathlib

## Purpose

Ce skill transforme des structures JSON complexes contenant des procédures d'audit interne (méthodologies, normes IIA/CRIPP, traitements et diligences) en documents Word professionnels avec mise en forme standardisée E-procedure.

## Use Cases

### Cas 1 : Conversion de Fichiers JSON Locaux

**Description :** Convertit un fichier JSON existant en document Word.

**Utilisation :**
```bash
python json2word_audit.py fichier.json -o ./sortie --ref REF001
```

**Avantages :**
- ✅ Simple et direct
- ✅ Pas de dépendances externes
- ✅ Idéal pour conversions ponctuelles

**Cas d'usage typiques :**
- Conversion de procédures préparées manuellement
- Tests et développement
- Archives et documentation statique

---

### Cas 2 : Workflow Automatisé avec API N8N

**Description :** Récupère automatiquement les données depuis un workflow N8N, puis les convertit en documents Word.

**Utilisation :**
```bash
python execute_cas2_production.py
```

**Workflow complet :**
1. 🌐 **Appel API** : POST vers `http://localhost:5678/webhook/skill_manuel_audit`
2. 📥 **Extraction** : Récupère le champ `Data_integrale` (tableau de procédures)
3. 💾 **Sauvegarde** : Crée des fichiers JSON temporaires pour chaque procédure
4. 🔄 **Conversion** : Exécute `json2word_audit.py` sur chaque procédure
5. 📄 **Génération** : Produit les documents Word avec références séquentielles (PROD001, PROD002...)

**Avantages :**
- ✅ **Automatisation complète** : Un seul script pour tout le workflow
- ✅ **Intégration N8N** : S'intègre dans vos pipelines d'automatisation
- ✅ **Batch processing** : Traite plusieurs procédures en une seule exécution
- ✅ **Traçabilité** : Sauvegarde les réponses API et les fichiers intermédiaires
- ✅ **Production-ready** : Gestion d'erreurs, logs détaillés, statistiques

**Cas d'usage typiques :**
- Production documentaire en masse
- Intégration dans des workflows d'entreprise
- Automatisation planifiée (cron jobs, scheduled tasks)
- Génération dynamique depuis bases de données

**Configuration N8N requise :**
- Nœud "Edit Fields" avec champ `Data_integrale` (type Array)
- Données formatées selon la structure Input Format (voir ci-dessous)

---

## Input Format

Le JSON d'entrée suit cette structure :

```json
{
  "Etape mission - Manuel des procedures": [
    {
      "table 1": {
        "Etape de mission": "Manuel audit interne - Phase de préparation",
        "Document": "Manuel méthodologique d'audit interne",
        "Processus": "Audit interne - Identification et évaluation des risques",
        "Cycle d'activité": "Méthodologie de Conduite des Missions",
        "Secteur d'activité": "Banque, Industrie et Assurance UMOA",
        "Norme": {
          "Norme 1": "Norme 1.1 Honnêteté et courage professionnel",
          "Norme 2": "Norme 2.1 Objectivité individuelle",
          "Norme 3": "Norme 4.2 Conscience professionnelle"
        },
        "Reference": "MAN-AUD-METH-RISK-02",
        "Version": "V3.2 - Démarche normée d'identification des risques",
        "Etablissement": "Afrika Group Holdings",
        "Approbation": "Comité d'Audit et des Risques"
      }
    },
    {
      "table 2": [
        {
          "Étape méthodologique": "Cadrage initial du périmètre",
          "Acteur audit": "Directeur de l'Audit Interne / Chef de mission",
          "Traitement et diligences d'audit": "- Définit le périmètre d'analyse\n- Délimite les frontières\n- Identifie les objectifs",
          "Document probant": "Lettre de cadrage, Note de stratégie, Déclaration des objectifs",
          "Norme IIA / CRIPP": "Norme 13.3 Objectifs et périmètre",
          "Extrait de la norme": "Les auditeurs internes doivent déterminer les objectifs..."
        }
      ]
    }
  ]
}
```

### Structure détaillée :

- **Clé principale** : `"Etape mission - [Titre]"` contient un array
- **table 1** : Dictionnaire avec métadonnées du manuel (en-tête, références, normes)
- **table 2** : Array d'objets représentant les étapes méthodologiques détaillées

### Colonnes de la table 2 :

1. **Étape méthodologique** : Nom de l'étape (ex: "Cadrage initial")
2. **Acteur audit** : Responsable de l'étape
3. **Traitement et diligences d'audit** : Actions à effectuer (format multiligne avec puces)
4. **Document probant** : Documents produits/requis (séparés par virgules)
5. **Norme IIA / CRIPP** : Référence normative
6. **Extrait de la norme** : Citation textuelle de la norme

---

## Contraintes Obligatoires

### 1. Format du Document

- ✅ **Retourner le JSON dans un document Word**
- ✅ **N'afficher QUE des tableaux** : Ne pas mettre de titre entre les tables
- ✅ **Format A4 paysage** avec marges 0,5" (1,27 cm)

### 2. En-tête et Pied de Page

**En-tête** :
- Format : `[Nom logiciel] - [Etape de mission]`
- Fond : Rouge bordeaux (#7B1E3A)
- Exemple : `"Logiciel automatisé E-audit pro 2.0 - Cartographie des risques"`

**Pied de page** :
- Texte fixe : `"Automatisez vos activités d'audit, risques et contrôles - Whatsapp : + 225 05 44 13 07 98"`
- Alignement : Centré

### 3. Orientation des Tables

**Tables verticales** (2 colonnes : Rubrique | Description) :
- Table "Signature worksheet"
- Table "Etape de mission" (table 1)

**Tables horizontales** (grille multi-colonnes) :
- Table 2 et suivantes

### 4. Couleurs et Mise en Forme

**En-têtes de tableau** :
- Fond : Rouge bordeaux (#7B1E3A)
- Texte : Blanc, gras

**Bordures** :
- Colonnes : Visibles (grises #999999)
- Lignes : Invisibles (blanches #FFFFFF) pour table 2+
- Ligne vide après chaque ligne renseignée

### 5. Règles de Nommage des Fichiers

**Composants** :
- `[référence numérotation]` : Format alphanumérique (ex: BB01, A210, BB040)
- `[Etape de mission]` : Nom extrait du JSON
- `[Nom logiciel]` : Nom du logiciel utilisé

**Formule standard (Cas 1)** :
```
[référence numérotation] ― [Etape de mission] ― [Nom logiciel].docx
```

**Exemples** :
- `BB01 ― Leadsheet_Ventes ― Logiciel E-révision.docx`
- `BB010 ― Etat_des_ventes_Sage100_Metalux_2025 ― Logiciel E-révision.docx`
- `BB040 ― Test_de_cadrage_du_chiffre_d'affaires ― Logiciel E-révision.docx`

**Formule avec horodatage (Cas 2)** :
```
[référence] ― [Etape de mission] ― [Nom logiciel]_V1_HH-MM-SS_DD.MM.YY.docx
```

**Exemple** :
```
PROD001 ― Manuel_audit_interne ― Logiciel automatisé E-audit pro_V1_14-15-10_31.10.26.docx
```

**Génération automatique** :
- Si `[Valeur alphanumerique]` est vide ou non définie, générer automatiquement une référence (2 lettres + 3 chiffres, ex: FX251)

### 6. Cas Spécial : Feuille Couverture

**Condition** : Si `[Etape de mission]` = "Feuille couverture" ou "Couverture"

**Instructions supplémentaires** :

1. **Insérer une table entre table 5 et table 4**
   - Nom : Table "Schéma de calcul"

2. **Élaborer le Schéma de calcul**
   - **NE PAS** inclure la mention : `"Schéma de calcul : C = A + B ; Écart = C − D"`
   - Chaque cellule contient :
     - Soit une lettre simple : `(A)`, `(B)`, `(D)`
     - Soit une composition : `(C) = (A) - (D)`, `(E) = (B) + (C)`

3. **Ajustement des largeurs de colonnes**
   - Pour les cellules avec lettres composées : augmenter la largeur pour affichage sur une seule ligne (pas de retour à la ligne)
   - Synchroniser la largeur des colonnes liées dans la table de test (table 4)
   
4. **Ordre d'insertion** :
   ```
   [Table 1 - Métadonnées]
   [Table 2 - ...]
   [Table 3 - ...]
   [Table 5 - Données source]
   [NOUVEAU: Table Schéma de calcul]  ← Insérer ici
   [Table 4 - Table de test]
   ```

---

## Output Format

Le document Word généré respecte les spécifications E-procedure :

### Mise en page :
- Format A4 **paysage**
- Marges : 0,5" (1,27 cm)
- En-tête : `[Logiciel] - [Étape de mission]` (fond bordeaux)
- Pied de page : Contact WhatsApp centré

### Table 1 (verticale) :
- 2 colonnes : **Rubrique** | **Description**
- En-tête : fond bordeaux (#7B1E3A), texte blanc gras
- Colonne Rubrique : fond rose pâle (#F2E6EA), texte gras
- Valeurs imbriquées (normes) : rendues en puces `- `

### Table 2 (grille) :
- Colonnes configurées avec largeurs spécifiques
- En-tête : fond bordeaux (#7B1E3A), texte blanc gras
- **Bordures** :
  - Colonnes : visibles (grises #999999)
  - Lignes : invisibles (blanches #FFFFFF)
- **Ligne vide** insérée après chaque ligne renseignée (pour lisibilité)
- Colonne "Étape" : en gras, préfixe "Étape NN -" retiré par défaut
- Colonne "Traitement" : actions en puces (une par ligne `\n`)
- Colonne "Document" : valeurs CSV converties en puces

### Nom du fichier : Règles de Nommage

#### Composants du nom de fichier

**[Etape de mission]**
- **Description** : Le nom de la variable "Etape de mission" dans le JSON de données
- **Exemples** :
  - Cartographie des risques
  - Frap
  - Feuilles couvertures
  - Matrice de surveillance permanente
  - Manuel audit interne

**[Valeur alphanumerique]** (Référence de numérotation)
- **Format** : Une ou deux lettres alphabétiques + 2 ou 3 chiffres
- **Exemples valides** :
  - `A210`
  - `BB01`
  - `BB010`
  - `BB040`
- **Génération automatique** : Si non définie, le système génère automatiquement une référence (ex: `FX251`)

**[Nom logiciel]**
- **Défaut** : `Logiciel automatisé E-audit pro`
- **Exemples** :
  - `Logiciel automatisé E-Contrôle interne bancaire`
  - `Logiciel automatisé E-audit pro 2.0`
  - `Logiciel E-révision`
  - `Logiciel automatisé E-audit pro`

#### Format de nommage standard (Cas 1)

**Formule** : `[référence numérotation]-[Etape de mission]- [Nom logiciel].docx`

**Exemples** :
- `BB01-Leadsheet_Ventes- Logiciel E-révision.docx`
- `BB010-Etat_des_ventes_Sage100_Metalux_2025- Logiciel E-révision.docx`
- `BB040-Test_de_cadrage_du_chiffre_d'affaires- Logiciel E-révision.docx`
- `A210-Manuel_audit_interne- Logiciel automatisé E-procedure.docx`

#### Format avec horodatage (Cas 2 - Production N8N)

**Formule** : `[référence]-[Etape de mission]- [Nom logiciel]_[timestamp].docx`

**Format du timestamp** : `V1_HH-MM-SS_DD.MM.YY`

**Exemple complet** :
```
PROD001 ― Manuel_audit_interne ― Logiciel automatisé E-audit pro_V1_14-15-10_31.10.26.docx
```

**Décomposition** :
- `PROD001` : Référence séquentielle de production
- `Manuel_audit_interne` : Étape de mission (espaces remplacés par `_`)
- `Logiciel automatisé E-audit pro` : Nom du logiciel (par défaut)
- `V1` : Version
- `14-15-10` : Heure (14h 15min 10sec)
- `31.10.26` : Date (31 octobre 2026)

**Avantages du timestamp (Cas 2)** :
- ✅ **Pas d'écrasement** : Générations multiples dans le même dossier
- ✅ **Traçabilité** : Date et heure exactes de génération
- ✅ **Archivage automatique** : Historique complet des versions
- ✅ **Lisibilité** : Format français (JJ.MM.AA) facile à comprendre
- ✅ **Tri chronologique** : Les fichiers se rangent dans l'ordre de création

## Technical Implementation

### Script Python : `json2word_audit.py`

Le script utilise :
- `python-docx` pour la génération Word
- Configuration des colonnes dans `COLUMN_SPECS`
- Gestion automatique des largeurs de colonnes
- Extraction intelligente du JSON (même entouré de texte)

### Workflow Cas 2 : Appel API N8N + Conversion Automatique

**Scripts disponibles :**

1. **`execute_cas2_production.py`** (Principal - Production)
   - Appelle le webhook N8N : `http://localhost:5678/webhook/skill_manuel_audit`
   - Extrait automatiquement `Data_integrale`
   - Traite chaque procédure avec le skill `json2word_audit.py`
   - Génère les documents dans `sortie_word_production/`
   - Références : PROD001, PROD002, PROD003, etc.

2. **`execute_workflow_simulation.py`** (Test)
   - Utilise des données de simulation locales
   - Permet de tester sans N8N actif
   - Sortie : `sortie_word_test/`

3. **`api_call_n8n.py`** (Utilitaire)
   - Script d'appel API isolé
   - Sauvegarde la réponse dans `data_json_from_n8n/`
   - Peut être utilisé indépendamment

**Architecture du Cas 2 :**

```
┌──────────────────┐
│   N8N Workflow   │  ← Configuration : nœud "Edit Fields" avec Data_integrale
│   localhost:5678 │
└────────┬─────────┘
         │ HTTP POST
         ↓
┌──────────────────────────────┐
│ execute_cas2_production.py   │
│                              │
│ 1. call_n8n_api()            │  ← Requête POST + extraction JSON
│ 2. extract_data_integrale()  │  ← Parse Data_integrale
│ 3. process_procedures()      │  ← Boucle sur chaque procédure
│    └─> json2word_audit.py    │  ← Conversion individuelle
└────────┬─────────────────────┘
         │
         ↓
┌──────────────────────────────┐
│ Documents Word Générés       │
│ sortie_word_production/      │
│                              │
│ • PROD001-*.docx             │
│ • PROD002-*.docx             │
│ • PROD003-*.docx             │
└──────────────────────────────┘
```

**Configuration N8N requise :**

Dans le workflow N8N `skill_manuel_audit` :

1. **Nœud "Webhook"** : 
   - Path : `/webhook/skill_manuel_audit`
   - Method : POST

2. **Nœud "Edit Fields"** :
   - Mode : "Define Below"
   - Field : `Data_integrale` (Type: Array)
   - Value : Tableau de procédures JSON

3. **Nœud "Respond to Webhook"** :
   - Respond With : "Using 'Respond to Webhook' Node"
   - Response Body : `{{ $json }}`

**Dépendances Cas 2 :**
```bash
pip install requests python-docx
```

### Configuration des colonnes (COLUMN_SPECS) :

```python
COLUMN_SPECS = {
    "Étape méthodologique":            ("Etape",            1900, "bold"),
    "Acteur audit":                    ("Acteur",           1500, "text"),
    "Traitement et diligences d'audit": ("Traitement",      5100, "nl"),
    "Document probant":                ("Document",         2300, "csv"),
    "Norme IIA / CRIPP":               ("Normes",           1700, "text"),
    "Extrait de la norme":             ("Extrait de norme", 2500, "text"),
}
```

Types de rendu :
- `"bold"` : texte en gras
- `"text"` : texte simple
- `"nl"` : multiligne avec puces (séparation sur `\n`)
- `"csv"` : valeurs CSV converties en puces

### Options de ligne de commande :

```bash
# Utilisation basique
python json2word_audit_procedures.py donnees.json

# Avec référence personnalisée
python json2word_audit_procedures.py donnees.json --ref A210 -o ./sortie

# Personnalisation du logiciel
python json2word_audit_procedures.py donnees.json --software "E-audit Pro 3.0"

# Sans lignes vides entre les enregistrements
python json2word_audit_procedures.py donnees.json --no-blank-rows

# Conserver le préfixe "Étape NN -"
python json2word_audit_procedures.py donnees.json --keep-step-prefix
```

## Validation Rules

### Contrôles avant conversion :
1. ✅ JSON valide et parsable
2. ✅ Présence d'au moins une clé `table N`
3. ✅ Table 1 contient `"Etape de mission"`
4. ✅ Table 2 est une liste non vide
5. ✅ Colonnes de table 2 reconnues dans COLUMN_SPECS

### Contrôles après génération :
1. ✅ Fichier .docx ouvrable sans erreur
2. ✅ Orientation paysage (largeur > hauteur)
3. ✅ En-tête et pied de page corrects
4. ✅ Nombre de tables = nombre de clés `table N`
5. ✅ Table 1 : 2 colonnes, N+1 lignes (N rubriques + en-tête)
6. ✅ Table 2 : M colonnes, 1 + 2×N lignes (en-tête + N enregistrements + N lignes vides)
7. ✅ Couleur en-têtes = #7B1E3A
8. ✅ Aucune donnée JSON perdue
9. ✅ Nom de fichier conforme au format

## Usage Examples

### Exemple 1 : Conversion simple (Cas 1 - Fichier JSON local)

```bash
# Données d'entrée : manuel_audit.json
# Sortie : MN472-Manuel_audit_interne- Logiciel automatisé E-procedure.docx
python json2word_audit.py manuel_audit.json -o ./documents
```

### Exemple 2 : Appel API N8N avec conversion automatique (Cas 2 - Production)

```bash
# Récupère les données depuis N8N et les convertit automatiquement
# URL : http://localhost:5678/webhook/skill_manuel_audit
# Sortie : sortie_word_production/PROD001-*.docx, PROD002-*.docx, etc.
python execute_cas2_production.py
```

**Ce qui se passe en Cas 2 :**
1. 🌐 Appel API POST vers le webhook N8N local
2. 📥 Extraction du champ `Data_integrale` (liste de procédures)
3. 💾 Sauvegarde temporaire de chaque procédure en JSON
4. 🔄 Exécution automatique du skill pour chaque procédure
5. 📄 Génération des documents Word avec timestamp unique
6. 📁 Sortie : `PROD001_20261031_144658-*.docx`, `PROD002_20261031_144658-*.docx`, etc.

**Format du nom de fichier (Cas 2)** :
```
<REF><NUM>_<YYYYMMDD_HHMMSS>-<Etape_de_mission>- <Logiciel>.docx
```

Exemples :
- `PROD001_20261031_143000-Manuel_audit_interne- E-Procedure N8N Production.docx`
- `PROD002_20261031_143002-Manuel_phase_preparation- E-Procedure N8N Production.docx`

**Configuration requise pour le Cas 2 :**

Dans N8N (nœud "Edit Fields") :
- **Mode** : "Define Below"
- **Field Name** : `Data_integrale`
- **Field Type** : `Array`
- **Field Value** : Tableau JSON de procédures (voir structure Input Format)

**Exécution batch Windows :**
```bash
execute_cas2.bat
```

### Exemple 3 : Série de procédures (fichiers locaux)

```bash
# Convertir tous les JSON d'un dossier
for file in procedures/*.json; do
    python json2word_audit.py "$file" -o ./sortie_word
done
```

### Exemple 4 : Personnalisation complète

```bash
python json2word_audit.py cartographie.json \
    --ref CARTO001 \
    --software "E-Risk Management Suite" \
    --no-blank-rows \
    -o ./output
```

### Exemple 5 : Mode simulation (Cas 2 - Test)

```bash
# Teste le workflow complet avec des données de simulation
python execute_workflow_simulation.py
```

## Error Handling

### Erreurs communes et solutions :

| Erreur | Cause | Solution |
|--------|-------|----------|
| `Aucun objet JSON trouvé` | JSON mal formé ou absent | Vérifier la syntaxe JSON |
| `Aucune clé "table N" trouvée` | Structure JSON non conforme | Ajouter au moins `table 1` et `table 2` |
| `ModuleNotFoundError: python-docx` | Bibliothèque manquante | `pip install python-docx` |
| Colonnes non reconnues | Nouvelles colonnes dans le JSON | Ajouter la configuration dans `COLUMN_SPECS` |
| Fichier déjà existant | Nom en conflit | Utiliser `--ref` différent ou renommer |

## Best Practices

### 1. Préparation des données JSON

✅ **À faire :**
- Encoder en UTF-8 avec BOM si accents
- Valider le JSON avec un linter
- Utiliser des retours à ligne `\n` pour les actions multiples
- Séparer les documents par des virgules dans "Document probant"

❌ **À éviter :**
- Caractères de contrôle dans les valeurs
- JSON invalide (virgules en trop, guillemets manquants)
- Laisser des lignes vides dans la table 2 (le script les gère)

### 2. Organisation des fichiers

```
Projet_audit/
├── json2word_audit_procedures.py  # Script de conversion
├── donnees/                       # JSON sources (lecture seule)
│   ├── manuel_phase1.json
│   ├── manuel_phase2.json
│   └── cartographie_risques.json
└── sortie_word/                   # Documents générés
    ├── A210-Manuel_phase1- E-procedure.docx
    └── A211-Manuel_phase2- E-procedure.docx
```

### 3. Workflow recommandé

```bash
# 1. Vérifier l'environnement
python --version  # Python 3.9+
pip show python-docx

# 2. Créer le dossier de sortie
mkdir -p sortie_word

# 3. Convertir avec validation
python json2word_audit_procedures.py donnees.json -o sortie_word

# 4. Contrôle qualité (optionnel : conversion PDF)
soffice --headless --convert-to pdf sortie_word/*.docx --outdir sortie_pdf
```

## Extending the Skill

### Ajouter de nouvelles colonnes

Si votre JSON contient d'autres colonnes (ex: FRAP, cartographie des risques) :

```python
# Dans le script json2word_audit_procedures.py
COLUMN_SPECS["Risque identifié"] = ("Risque", 3000, "text")
COLUMN_SPECS["Niveau de criticité"] = ("Criticité", 1200, "bold")
COLUMN_SPECS["Plan d'action"] = ("Actions", 4000, "nl")
```

Types de rendu disponibles :
- `"text"` : texte brut
- `"bold"` : texte en gras
- `"nl"` : puces séparées par `\n`
- `"csv"` : puces séparées par `, `

### Modifier les couleurs

```python
BORDEAUX = "7B1E3A"  # En-têtes tableau
LIGHT = "F2E6EA"     # Fond colonne Rubrique
GREY = "999999"      # Bordures visibles
WHITE = "FFFFFF"     # Bordures invisibles
```

## Limitations

1. **Schéma de calcul** : La règle des feuilles de couverture (insertion de lignes de formules entre tables) n'est pas gérée automatiquement
2. **Images** : Pas de support pour l'insertion d'images dans le JSON
3. **Graphiques** : Les graphiques Excel ne sont pas générés
4. **Fusion de cellules** : Pas de fusion automatique des cellules dans les tables
5. **Styles personnalisés** : Les styles Word personnalisés doivent être ajoutés manuellement après génération

## Testing

### Test unitaire de conversion

```python
# test_conversion.py
from pathlib import Path
import json
from docx import Document

def test_audit_procedures_conversion():
    # Données de test
    test_data = {
        "Etape mission - Test": [
            {"table 1": {"Etape de mission": "Test Phase", "Document": "Test Doc"}},
            {"table 2": [{"Étape méthodologique": "Test Step", "Acteur audit": "Testeur"}]}
        ]
    }
    
    # Sauvegarder le JSON
    test_json = Path("test_input.json")
    test_json.write_text(json.dumps(test_data, ensure_ascii=False, indent=2), encoding="utf-8")
    
    # Convertir
    from json2word_audit_procedures import convert
    output = convert(test_json, Path("test_output"), software="Test", reference="TST001",
                    footer="Test", blank_rows=True, strip_steps=True)
    
    # Vérifier
    assert output.exists(), "Fichier non créé"
    doc = Document(str(output))
    assert doc.sections[0].orientation == 1, "Pas en paysage"  # WD_ORIENT.LANDSCAPE = 1
    assert len(doc.tables) == 2, "Nombre de tables incorrect"
    
    # Nettoyage
    test_json.unlink()
    output.unlink()
    print("✅ Test réussi")

if __name__ == "__main__":
    test_audit_procedures_conversion()
```

## License & Attribution

Ce skill est basé sur le script `json2word_audit.py` développé pour l'automatisation documentaire E-procedure.

**Utilisation** : Libre pour automatisation de procédures d'audit interne, cartographies de risques, FRAP et documents de méthodologie.

**Référence normative** : Normes IIA (Institute of Internal Auditors) / CRIPP 2025

**Contact** : Whatsapp + 225 05 44 13 07 98

---

## Changelog

### Version 1.2.0 (2026-10-31)
- ✨ **Horodatage déplacé à la fin du nom de fichier**
- ✅ Nouveau format : `[ref]-[etape]- [logiciel]_V1_HH-MM-SS_DD.MM.YY.docx`
- ✅ Format français pour la date (JJ.MM.AA)
- ✅ Meilleure lisibilité des noms de fichiers
- 📖 **Documentation complète des contraintes obligatoires**
- 📖 Section dédiée aux règles de nommage avec exemples multiples
- 📖 Documentation du cas spécial "Feuille couverture" avec schéma de calcul
- 📖 Spécification des composants : [Etape de mission], [Valeur alphanumérique], [Nom logiciel]
- 📖 Exemples de nommage : BB01, BB010, BB040, A210
- 📖 Contraintes en-tête, pied de page, couleurs et bordures
- 📖 Règles pour tables verticales (Signature worksheet, Etape de mission)

### Version 1.1.0 (2026-10-31)
- ✨ **Nouveau : Cas 2 - Workflow automatisé avec API N8N**
- ✅ Ajout du script `execute_cas2_production.py` pour appel API automatique
- ✅ Intégration complète avec N8N (webhook + extraction Data_integrale)
- ✅ Script batch Windows `execute_cas2.bat` pour exécution simplifiée
- ✅ Mode simulation avec `execute_workflow_simulation.py`
- ✅ Module d'appel API isolé `api_call_n8n.py`
- ✅ Documentation complète du Cas 2 dans le skill
- ✅ Architecture de production avec logs, gestion d'erreurs et statistiques
- ✅ Support du traitement batch de multiples procédures
- 📦 Dépendance ajoutée : `requests` pour les appels HTTP

### Version 1.0.0 (2026-10-31)
- ✨ Création initiale du skill (Cas 1)
- ✅ Support complet de la structure JSON audit interne
- ✅ Configuration COLUMN_SPECS pour 6 colonnes méthodologiques
- ✅ Validation en entrée et sortie
- ✅ Gestion des lignes vides entre enregistrements
- ✅ Référence alphanumérique auto-générée
- ✅ Documentation complète avec exemples
