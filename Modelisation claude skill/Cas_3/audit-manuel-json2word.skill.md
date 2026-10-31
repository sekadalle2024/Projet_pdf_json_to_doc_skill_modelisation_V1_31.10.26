# Skill: audit-manuel-json2word

## Dependencies

### Installation Base (Conversion locale)

```bash
pip install python-docx
```

### Installation Complète (Workflow N8N)

```bash
# Avec Conda (recommandé)
conda activate pdf_excel_env
pip install python-docx requests

# Ou avec pip standard
pip install python-docx requests
```

### Fichiers Requis

**Pour la conversion simple :**
- `json2word_audit.py` - Script de conversion principal

**Pour le workflow N8N complet :**
- `json2word_audit.py` - Script de conversion
- `execute_cas3_production.py` - Orchestrateur principal
- `api_call_n8n.py` - Module d'appel API (partagé avec Cas 2)
- `execute_cas3.bat` - Script batch Windows (optionnel)

**Configuration N8N (workflow API) :**
- N8N installé et démarré sur `http://localhost:5678`
- Workflow `skill_manuel_audit_cas3` configuré avec :
  - Webhook actif
  - Nœud "Edit Fields" avec champ `Data_integrale`
  - Nœud "Respond to Webhook"

## Metadata
- **Name**: audit-manuel-json2word
- **Version**: 1.0.0
- **Author**: Expert Python & Document Automation
- **Description**: Convertit des données JSON de manuels d'audit interne en documents Word professionnels au format E-procedure (via API N8N)
- **Tags**: audit, manuel, json, word, automation, n8n, api
- **Dependencies**: python-docx, requests, json, pathlib

## Purpose

Ce skill (Cas 3) transforme des structures JSON de **manuels d'audit interne** récupérées depuis un **workflow N8N** en documents Word professionnels avec mise en forme standardisée E-procedure.

**Spécificité Cas 3** : Récupération automatique des données depuis une API N8N dédiée aux manuels d'audit.

## Use Cases

### Workflow Automatisé avec API N8N (Production)

**Description :** Récupère automatiquement les données depuis un workflow N8N spécifique au Cas 3, puis les convertit en documents Word.

**Utilisation :**
```bash
python execute_cas3_production.py
```

**Workflow complet :**
1. 🌐 **Appel API** : POST vers `http://localhost:5678/webhook/skill_manuel_audit_cas3`
2. 📥 **Extraction** : Récupère le champ `Data_integrale` (tableau de manuels)
3. 💾 **Sauvegarde** : Crée des fichiers JSON temporaires pour chaque manuel
4. 🔄 **Conversion** : Exécute `json2word_audit.py` sur chaque manuel
5. 📄 **Génération** : Produit les documents Word avec horodatage unique

**Avantages :**
- ✅ **Automatisation complète** : Workflow end-to-end depuis N8N
- ✅ **Intégration native** : S'intègre dans vos pipelines d'audit
- ✅ **Batch processing** : Traite plusieurs manuels en une seule exécution
- ✅ **Traçabilité** : Sauvegarde les réponses API et les fichiers intermédiaires
- ✅ **Production-ready** : Gestion d'erreurs, logs détaillés, statistiques

**Cas d'usage typiques :**
- Production documentaire en masse de manuels d'audit
- Génération automatique depuis bases de données d'audit
- Intégration dans workflows d'entreprise (gouvernance, conformité)
- Automatisation planifiée (génération mensuelle/trimestrielle)

**Configuration N8N requise :**
- Webhook : `http://localhost:5678/webhook/skill_manuel_audit_cas3`
- Nœud "Edit Fields" avec champ `Data_integrale` (type Array)
- Données formatées selon la structure Input Format (voir ci-dessous)

---

## Input Format

Le JSON d'entrée suit la même structure que le Cas 2 (manuels de procédures d'audit) :

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
- Exemple : `"Logiciel automatisé E-audit pro 2.0 - Manuel audit interne"`

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

### 5. Règles de Nommage des Fichiers (Cas 3 - Horodatage)

**Formule standard** :
```
[Etape de mission] ― [Nom logiciel]_V1_HH-MM-SS_DD.MM.YY.docx
```

**Exemple complet** :
```
Manuel_audit_interne ― Logiciel automatisé E-audit pro_V1_14-15-10_31.10.26.docx
```

**Décomposition** :
- `Manuel_audit_interne` : Étape de mission (espaces remplacés par `_`)
- `Logiciel automatisé E-audit pro` : Nom du logiciel (par défaut)
- `V1` : Version
- `14-15-10` : Heure (14h 15min 10sec)
- `31.10.26` : Date (31 octobre 2026)

**Avantages du timestamp (Cas 3)** :
- ✅ **Pas d'écrasement** : Générations multiples dans le même dossier
- ✅ **Traçabilité** : Date et heure exactes de génération
- ✅ **Archivage automatique** : Historique complet des versions
- ✅ **Lisibilité** : Format français (JJ.MM.AA) facile à comprendre
- ✅ **Tri chronologique** : Les fichiers se rangent dans l'ordre de création

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

---

## Technical Implementation

### Script Python : `json2word_audit.py`

Le script utilise :
- `python-docx` pour la génération Word
- Configuration des colonnes dans `COLUMN_SPECS`
- Gestion automatique des largeurs de colonnes
- Extraction intelligente du JSON (même entouré de texte)

**Ce script est réutilisé du Cas 2** (aucune modification nécessaire).

### Workflow Cas 3 : Appel API N8N + Conversion Automatique

**Script principal : `execute_cas3_production.py`**

Fonctionnalités :
- Appelle le webhook N8N : `http://localhost:5678/webhook/skill_manuel_audit_cas3`
- Extrait automatiquement `Data_integrale`
- Traite chaque manuel avec le skill `json2word_audit.py`
- Génère les documents dans `sortie_word_cas3/`
- Références avec timestamp : `V1_HH-MM-SS_DD.MM.YY`

**Architecture du Cas 3 :**

```
┌──────────────────┐
│   N8N Workflow   │  ← Configuration : webhook skill_manuel_audit_cas3
│   localhost:5678 │
└────────┬─────────┘
         │ HTTP POST
         ↓
┌──────────────────────────────┐
│ execute_cas3_production.py   │
│                              │
│ 1. call_n8n_api()            │  ← Requête POST + extraction JSON
│ 2. extract_data_integrale()  │  ← Parse Data_integrale
│ 3. process_procedures()      │  ← Boucle sur chaque manuel
│    └─> json2word_audit.py    │  ← Conversion individuelle
└────────┬─────────────────────┘
         │
         ↓
┌──────────────────────────────┐
│ Documents Word Générés       │
│ sortie_word_cas3/            │
│                              │
│ • Manuel_audit_*_V1_*.docx   │
│ • Manuel_phase_*_V1_*.docx   │
└──────────────────────────────┘
```

**Configuration N8N requise :**

Dans le workflow N8N `skill_manuel_audit_cas3` :

1. **Nœud "Webhook"** : 
   - Path : `/webhook/skill_manuel_audit_cas3`
   - Method : POST

2. **Nœud "Edit Fields"** :
   - Mode : "Define Below"
   - Field : `Data_integrale` (Type: Array)
   - Value : Tableau de manuels JSON

3. **Nœud "Respond to Webhook"** :
   - Respond With : "Using 'Respond to Webhook' Node"
   - Response Body : `{{ $json }}`

**Dépendances Cas 3 :**
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

---

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
9. ✅ Nom de fichier conforme au format avec horodatage

---

## Usage Examples

### Exemple 1 : Workflow Production (Cas 3 - API N8N)

```bash
# Récupère les manuels depuis N8N et les convertit automatiquement
# URL : http://localhost:5678/webhook/skill_manuel_audit_cas3
# Sortie : sortie_word_cas3/*.docx avec horodatage
python execute_cas3_production.py
```

**Ce qui se passe en Cas 3 :**
1. 🌐 Appel API POST vers le webhook N8N Cas 3
2. 📥 Extraction du champ `Data_integrale` (liste de manuels)
3. 💾 Sauvegarde temporaire de chaque manuel en JSON
4. 🔄 Exécution automatique du skill pour chaque manuel
5. 📄 Génération des documents Word avec timestamp unique
6. 📁 Sortie : `Manuel_audit_interne ― E-audit pro_V1_14-15-10_31.10.26.docx`

**Format du nom de fichier (Cas 3)** :
```
<Etape_de_mission> ― <Logiciel>_V1_<HH-MM-SS>_<DD.MM.YY>.docx
```

Exemples :
- `Manuel_audit_interne ― Logiciel automatisé E-audit pro_V1_14-15-10_31.10.26.docx`
- `Manuel_phase_preparation ― Logiciel automatisé E-audit pro_V1_14-16-22_31.10.26.docx`

**Configuration requise pour le Cas 3 :**

Dans N8N (nœud "Edit Fields") :
- **Mode** : "Define Below"
- **Field Name** : `Data_integrale`
- **Field Type** : `Array`
- **Field Value** : Tableau JSON de manuels (voir structure Input Format)

**Exécution batch Windows :**
```bash
execute_cas3.bat
```

---

## Error Handling

### Erreurs communes et solutions :

| Erreur | Cause | Solution |
|--------|-------|----------|
| `Aucun objet JSON trouvé` | JSON mal formé ou absent | Vérifier la syntaxe JSON |
| `Aucune clé "table N" trouvée` | Structure JSON non conforme | Ajouter au moins `table 1` et `table 2` |
| `ModuleNotFoundError: python-docx` | Bibliothèque manquante | `pip install python-docx` |
| `Connection refused` | N8N non démarré | `n8n start` ou vérifier le port 5678 |
| `Timeout API` | N8N trop lent | Augmenter TIMEOUT dans le script |
| Colonnes non reconnues | Nouvelles colonnes dans le JSON | Ajouter la configuration dans `COLUMN_SPECS` |

---

## Best Practices

### 1. Préparation N8N

✅ **À faire :**
- Démarrer N8N avant l'exécution : `n8n start`
- Activer le workflow `skill_manuel_audit_cas3`
- Tester le webhook avec un outil (Postman, curl)
- Vérifier que `Data_integrale` est bien configuré

❌ **À éviter :**
- Exécuter le script sans N8N actif
- Oublier d'activer le workflow dans N8N
- Utiliser une URL de webhook incorrecte

### 2. Organisation des fichiers

```
Cas_3/
├── json2word_audit.py              # Script de conversion (réutilisé)
├── execute_cas3_production.py      # Orchestrateur principal
├── execute_cas3.bat                # Batch Windows
├── sortie_word_cas3/               # Documents générés
├── temp_procedures_cas3/           # JSON temporaires
└── data_json_from_n8n_cas3/        # Réponses API sauvegardées
```

### 3. Workflow recommandé

```bash
# 1. Vérifier N8N
n8n start

# 2. Vérifier l'environnement Python
python --version  # Python 3.9+
pip show python-docx requests

# 3. Créer les dossiers de sortie (automatique)
# Les dossiers sont créés automatiquement par le script

# 4. Exécuter le workflow Cas 3
python execute_cas3_production.py

# 5. Vérifier les documents générés
ls sortie_word_cas3/
```

---

## Extending the Skill

### Ajouter de nouvelles colonnes

Si votre JSON contient d'autres colonnes spécifiques aux manuels d'audit :

```python
# Dans le script json2word_audit.py (section COLUMN_SPECS)
COLUMN_SPECS["Référence méthodologique"] = ("Ref", 1500, "text")
COLUMN_SPECS["Niveau d'application"] = ("Niveau", 1200, "bold")
COLUMN_SPECS["Points de contrôle"] = ("Contrôles", 4000, "nl")
```

### Modifier l'URL du webhook

```python
# Dans execute_cas3_production.py
WEBHOOK_URL = "http://localhost:5678/webhook/skill_manuel_audit_cas3"
```

---

## Limitations

1. **Dépendance N8N** : Le workflow nécessite N8N actif
2. **Images** : Pas de support pour l'insertion d'images dans le JSON
3. **Graphiques** : Les graphiques Excel ne sont pas générés
4. **Fusion de cellules** : Pas de fusion automatique des cellules dans les tables
5. **Timeout** : Par défaut 30 secondes (configurable)

---

## Testing

### Test de connexion N8N

```bash
# Test simple du webhook
curl -X POST http://localhost:5678/webhook/skill_manuel_audit_cas3 \
     -H "Content-Type: application/json" \
     -d '{}'
```

### Test du workflow complet

```bash
# Exécuter en mode test
python execute_cas3_production.py
```

---

## License & Attribution

Ce skill est basé sur le script `json2word_audit.py` développé pour l'automatisation documentaire E-procedure.

**Utilisation** : Libre pour automatisation de manuels d'audit interne.

**Référence normative** : Normes IIA (Institute of Internal Auditors) / CRIPP 2025

**Contact** : Whatsapp + 225 05 44 13 07 98

---

## Changelog

### Version 1.0.0 (2026-10-31)
- ✨ Création initiale du skill Cas 3
- ✅ Support complet du workflow N8N dédié
- ✅ Réutilisation du script `json2word_audit.py` (Cas 2)
- ✅ Horodatage au format V1_HH-MM-SS_DD.MM.YY
- ✅ Orchestrateur `execute_cas3_production.py` avec logs détaillés
- ✅ Batch processing de multiples manuels
- ✅ Documentation complète avec exemples
- 📦 Dépendances : `python-docx`, `requests`
