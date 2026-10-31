# Guide d'utilisation : Skill Audit Procedures JSON to Word

## 📋 Vue d'ensemble

Ce skill permet de transformer automatiquement des données JSON structurées de procédures d'audit interne en documents Word professionnels au format E-procedure.

**Cas d'usage :**
- Manuels de procédures d'audit interne
- Cartographies de risques méthodologiques
- FRAP (Feuilles de Révélation et d'Analyse de Problèmes)
- Guides méthodologiques CRIPP/IIA
- Documentation de processus d'audit

## 🎯 Objectif

Générer des documents Word structurés et formatés qui respectent :
- Les normes IIA (Institute of Internal Auditors)
- Le référentiel CRIPP 2025
- Le format E-procedure (standard documentaire)
- La mise en forme professionnelle pour l'audit bancaire et industriel

## 📂 Structure des fichiers

```
Modelisation claude skill/
├── audit-procedures-json2word.skill.md    # Documentation complète du skill
├── json2word_audit.py                      # Script Python de conversion (original)
├── json2word_audit_procedures.py           # Script adapté aux procédures d'audit
├── prompt_agent_code_local.md              # Prompt pour agent de code local
├── README_AUDIT_PROCEDURES.md              # Ce fichier
└── assets/
    ├── exemple_manuel_procedures_audit.json # Exemple de données JSON
    └── exemple_resultat.docx                # Exemple de résultat attendu
```

## 🔧 Installation

### Prérequis

- Python 3.9 ou supérieur
- pip (gestionnaire de paquets Python)

### Installation de la dépendance

```bash
pip install python-docx
```

Ou dans un environnement virtuel (recommandé) :

```bash
# Créer l'environnement virtuel
python -m venv .venv

# Activer l'environnement (Windows)
.venv\Scripts\activate

# Activer l'environnement (Linux/Mac)
source .venv/bin/activate

# Installer python-docx
pip install python-docx
```

## 📊 Format des données JSON

### Structure générale

```json
{
  "Etape mission - [Titre]": [
    {
      "table 1": {
        "Etape de mission": "...",
        "Document": "...",
        "Processus": "...",
        "Norme": {
          "Norme 1": "...",
          "Norme 2": "..."
        }
      }
    },
    {
      "table 2": [
        {
          "Étape méthodologique": "...",
          "Acteur audit": "...",
          "Traitement et diligences d'audit": "...",
          "Document probant": "...",
          "Norme IIA / CRIPP": "...",
          "Extrait de la norme": "..."
        }
      ]
    }
  ]
}
```

### Détail des champs

#### Table 1 (Métadonnées)
| Champ | Type | Description | Exemple |
|-------|------|-------------|---------|
| Etape de mission | Texte | Titre de l'étape | "Manuel audit interne - Phase de préparation" |
| Document | Texte | Nom du document | "Manuel méthodologique d'audit interne" |
| Processus | Texte | Processus concerné | "Audit interne - Identification des risques" |
| Cycle d'activité | Texte | Cycle méthodologique | "CRIPP 2025" |
| Secteur d'activité | Texte | Secteur | "Banque UMOA" |
| Norme | Objet | Normes IIA/CRIPP | `{"Norme 1": "...", "Norme 2": "..."}` |
| Reference | Texte | Référence document | "MAN-AUD-METH-RISK-02" |
| Version | Texte | Version | "V3.2 - Démarche normée" |
| Etablissement | Texte | Nom établissement | "Afrika Group Holdings" |
| Approbation | Texte | Organe approbateur | "Comité d'Audit et des Risques" |

#### Table 2 (Étapes détaillées)
| Colonne | Type | Format | Description |
|---------|------|--------|-------------|
| Étape méthodologique | Texte | Gras | Nom de l'étape (sans préfixe "Étape NN -") |
| Acteur audit | Texte | Normal | Responsable de l'étape |
| Traitement et diligences d'audit | Multiligne | Puces `\n` | Actions détaillées (une par ligne) |
| Document probant | CSV | Puces `, ` | Documents séparés par des virgules |
| Norme IIA / CRIPP | Texte | Normal | Référence de la norme |
| Extrait de la norme | Texte | Normal | Citation textuelle |

### Exemples de valeurs

**Traitement multiligne (avec `\n`) :**
```json
"Traitement et diligences d'audit": "- Définit le périmètre d'analyse\n- Délimite les frontières\n- Identifie les objectifs"
```

**Document probant (CSV) :**
```json
"Document probant": "Lettre de cadrage, Note de stratégie, Déclaration des objectifs"
```

## 🚀 Utilisation

### Commande de base

```bash
python json2word_audit.py donnees.json
```

**Résultat :**
- Fichier : `XX472-Etape_de_mission- Logiciel automatisé E-procedure.docx`
- Répertoire : Même dossier que le JSON

### Options avancées

#### 1. Spécifier le dossier de sortie

```bash
python json2word_audit.py donnees.json -o ./sortie_word
```

#### 2. Définir une référence personnalisée

```bash
python json2word_audit.py donnees.json --ref A210
```

**Format de référence :**
- 1-2 lettres + 2-3 chiffres
- Exemples : `A210`, `MA417`, `FRAP01`

#### 3. Personnaliser le nom du logiciel

```bash
python json2word_audit.py donnees.json --software "E-Audit Pro 3.0"
```

Apparaît dans :
- En-tête du document
- Nom du fichier

#### 4. Modifier le pied de page

```bash
python json2word_audit.py donnees.json --footer "Service Audit - contact@entreprise.com"
```

#### 5. Options de formatage

**Ne pas insérer de lignes vides entre les enregistrements :**
```bash
python json2word_audit.py donnees.json --no-blank-rows
```

**Conserver le préfixe "Étape NN -" :**
```bash
python json2word_audit.py donnees.json --keep-step-prefix
```

### Exemple complet

```bash
python json2word_audit.py manuel_audit_phase1.json \
    --ref A210 \
    --software "E-Procedure Suite 2.0" \
    --footer "Direction Audit Interne - Whatsapp: +225 05 44 13 07 98" \
    -o ./documents_generes
```

## 📄 Format du document Word généré

### Mise en page
- **Format** : A4 Paysage (297mm × 210mm)
- **Marges** : 0,5 pouces (1,27 cm) sur tous les côtés
- **Police** : Calibri 9pt
- **Orientation** : Paysage

### En-tête
```
[Nom du logiciel] - [Étape de mission]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  (ligne bordeaux)
```

### Table 1 : Métadonnées (verticale)

| Rubrique | Description |
|----------|-------------|
| Etape de mission | Manuel audit interne - Phase de préparation |
| Document | Manuel méthodologique d'audit interne |
| Norme | - Norme 1.1 Honnêteté<br>- Norme 2.1 Objectivité<br>- Norme 4.2 Conscience |

**Style :**
- En-tête : Fond bordeaux (#7B1E3A), texte blanc gras
- Colonne "Rubrique" : Fond rose pâle (#F2E6EA), texte noir gras
- Colonne "Description" : Fond blanc, texte noir

### Table 2 : Étapes détaillées (grille)

| Etape | Acteur | Traitement | Document | Normes | Extrait de norme |
|-------|--------|------------|----------|--------|------------------|
| **Cadrage initial** | Directeur AI | - Définit le périmètre<br>- Délimite les frontières | - Lettre de cadrage<br>- Note de stratégie | Norme 13.3 | Les auditeurs internes... |
|  |  |  |  |  |  |
| **Collecte documentaire** | Auditeur Senior | - Recueille le corpus<br>- Identifie les flux | - Dossier permanent<br>- Manuels | Norme 14.1 | Pour effectuer des analyses... |

**Style :**
- En-tête : Fond bordeaux (#7B1E3A), texte blanc gras
- Bordures colonnes : Visibles (grises)
- Bordures lignes : Invisibles (blanches)
- Ligne vide : Insérée après chaque enregistrement (pour séparation visuelle)

### Pied de page
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  (ligne bordeaux)
       Automatisez vos activités d'audit, risques et contrôles
                Whatsapp : + 225 05 44 13 07 98
```

### Nom du fichier
Format : `<référence>-<Etape_de_mission>- <Logiciel>.docx`

Exemples :
- `A210-Manuel_audit_interne- Logiciel automatisé E-procedure.docx`
- `FRAP01-Cartographie_risques- E-Risk Management.docx`

## ✅ Validation et contrôle qualité

### Contrôles automatiques effectués

Le script vérifie :
1. ✅ JSON valide et bien formé
2. ✅ Présence des clés `table 1` et `table 2`
3. ✅ Colonne `Etape de mission` dans table 1
4. ✅ Table 2 non vide
5. ✅ Colonnes reconnues dans COLUMN_SPECS

### Contrôle manuel recommandé

Après génération, vérifier :
1. **Orientation** : Document en paysage
2. **En-tête/Pied de page** : Textes corrects
3. **Tables** : Nombre = nombre de `table N` dans le JSON
4. **Couleurs** : En-têtes en bordeaux (#7B1E3A)
5. **Contenu** : Aucune donnée JSON manquante
6. **Formatage** : Puces et multilignes correctes

### Conversion PDF (optionnel)

Pour un contrôle visuel rapide :

```bash
# Avec LibreOffice (si installé)
soffice --headless --convert-to pdf "fichier.docx" --outdir ./pdf

# Avec Microsoft Word (Windows PowerShell)
$word = New-Object -ComObject Word.Application
$doc = $word.Documents.Open("C:\chemin\fichier.docx")
$doc.SaveAs("C:\chemin\fichier.pdf", 17)
$doc.Close()
$word.Quit()
```

## 🔧 Personnalisation avancée

### Ajouter de nouvelles colonnes

Si votre JSON contient d'autres colonnes (ex: FRAP, cartographie) :

**1. Éditer le fichier `json2word_audit.py`**

Trouver la section `COLUMN_SPECS` :

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

**2. Ajouter votre colonne**

```python
# Exemple pour un FRAP
COLUMN_SPECS["Risque identifié"] = ("Risque", 3000, "text")
COLUMN_SPECS["Niveau de criticité"] = ("Criticité", 1200, "bold")
COLUMN_SPECS["Plan d'action"] = ("Actions", 4000, "nl")

# Exemple pour une cartographie
COLUMN_SPECS["Impact"] = ("Impact", 1000, "bold")
COLUMN_SPECS["Probabilité"] = ("Proba", 1000, "bold")
COLUMN_SPECS["Contrôles existants"] = ("Contrôles", 3500, "nl")
```

**Types de rendu disponibles :**
- `"text"` : Texte simple
- `"bold"` : Texte en gras
- `"nl"` : Multiligne avec puces (séparation sur `\n`)
- `"csv"` : CSV converti en puces (séparation sur `, `)

**Largeurs (en DXA) :**
- Largeur totale disponible : 15000 DXA
- 1 DXA ≈ 0,05 mm
- Exemples : 1900 ≈ 9,5 cm, 5100 ≈ 25,5 cm

### Modifier les couleurs

Éditer les constantes en début de script :

```python
BORDEAUX = "7B1E3A"  # Fond en-têtes (défaut: bordeaux)
LIGHT = "F2E6EA"     # Fond colonne Rubrique (défaut: rose pâle)
GREY = "999999"      # Bordures visibles (défaut: gris)
WHITE = "FFFFFF"     # Bordures invisibles (défaut: blanc)
```

Exemples de palettes :

**Palette bleue :**
```python
BORDEAUX = "1F4E78"  # Bleu marine
LIGHT = "D9E2F3"     # Bleu clair
```

**Palette verte :**
```python
BORDEAUX = "2E5C3E"  # Vert forêt
LIGHT = "E2EFDA"     # Vert pâle
```

### Changer la police et la taille

```python
FONT = "Calibri"     # Police par défaut
FONT_SIZE = 9        # Taille en points
```

Polices recommandées : Calibri, Arial, Times New Roman, Helvetica

## 🐛 Dépannage

### Erreur : `ModuleNotFoundError: No module named 'docx'`

**Solution :**
```bash
pip install python-docx
```

### Erreur : `Aucun objet JSON trouvé dans le fichier`

**Causes possibles :**
- JSON mal formé (virgules manquantes, guillemets non fermés)
- Fichier vide
- Encodage incorrect

**Solution :**
1. Valider le JSON avec un linter : https://jsonlint.com/
2. Vérifier l'encodage : UTF-8 avec ou sans BOM
3. Tester avec un JSON minimal :

```json
{
  "Etape mission - Test": [
    {"table 1": {"Etape de mission": "Test"}},
    {"table 2": [{"Colonne A": "Valeur A"}]}
  ]
}
```

### Erreur : `Aucune clé "table N" trouvée`

**Solution :**
Vérifier que le JSON contient au moins `table 1` et `table 2` :

```json
{
  "Etape mission - ...": [
    {"table 1": {...}},
    {"table 2": [...]}
  ]
}
```

### Warning : Colonnes non reconnues

**Message :**
```
Warning: Colonne "Nouvelle colonne" non configurée dans COLUMN_SPECS
```

**Impact :**
- La colonne est créée avec une largeur par défaut
- Le rendu est en texte simple

**Solution :**
Ajouter la configuration dans `COLUMN_SPECS` (voir section Personnalisation)

### Fichier Word ne s'ouvre pas

**Causes possibles :**
- Corruption pendant la génération
- Espace disque insuffisant
- Antivirus bloquant l'écriture

**Solution :**
1. Vérifier l'espace disque
2. Relancer la conversion
3. Tester l'ouverture avec LibreOffice ou Google Docs

## 📚 Ressources complémentaires

### Normes IIA / CRIPP
- [Institute of Internal Auditors (IIA)](https://www.theiia.org/)
- Cadre de Référence International des Pratiques Professionnelles (CRIPP 2025)

### Python-docx
- [Documentation officielle](https://python-docx.readthedocs.io/)
- [GitHub Repository](https://github.com/python-openxml/python-docx)

### JSON
- [Validateur JSON](https://jsonlint.com/)
- [Specification JSON](https://www.json.org/)

## 🤝 Support

**Contact :**
- WhatsApp : +225 05 44 13 07 98
- Email : Automatisez vos activités d'audit, risques et contrôles

**Assistance :**
- Conversion de JSON en Word
- Personnalisation de templates
- Formation sur l'outil
- Support technique

## 📝 Licence

Ce skill est fourni pour l'automatisation documentaire des activités d'audit interne, gestion des risques et contrôle interne.

**Utilisation libre pour :**
- Départements d'audit interne
- Cabinets de conseil en audit
- Directions des risques et du contrôle interne
- Formation et enseignement

---

**Version du guide :** 1.0.0  
**Date :** 31 octobre 2026  
**Auteur :** Expert Python & Document Automation
