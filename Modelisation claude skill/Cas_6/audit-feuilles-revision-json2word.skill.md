# Skill: audit-feuilles-revision-json2word

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
- `json2word_feuilles_revision.py` - Script de conversion principal

**Pour le workflow N8N complet :**
- `json2word_feuilles_revision.py` - Script de conversion
- `execute_cas6_production.py` - Orchestrateur principal
- `api_call_n8n.py` - Module d'appel API (partagé avec Cas 2 et 3)
- `execute_cas6.bat` - Script batch Windows (optionnel)

**Configuration N8N (workflow API) :**
- N8N installé et démarré sur `http://localhost:5678`
- Workflow `skill_feuilles_revision_cas6` configuré avec :
  - Webhook actif
  - Nœud "Edit Fields" avec champ `Data_integrale`
  - Nœud "Respond to Webhook"

## Metadata
- **Name**: audit-feuilles-revision-json2word
- **Version**: 1.0.0
- **Author**: Expert Python & Document Automation
- **Description**: Convertit des données JSON de feuilles de révision d'audit en documents Word professionnels avec tests et pointages (via API N8N)
- **Tags**: audit, feuilles-revision, tests, pointages, json, word, automation, n8n, api
- **Dependencies**: python-docx, requests, json, pathlib

## Purpose

Ce skill (Cas 6) transforme des structures JSON de **feuilles de révision d'audit** (incluant tests, pointages et conclusions) récupérées depuis un **workflow N8N** en documents Word professionnels avec mise en forme standardisée E-procedure.

**Spécificité Cas 6** : Génération de feuilles de test et de révision d'audit avec critères, diligences, pointages et conclusions.

## Use Cases

### Workflow Automatisé avec API N8N (Production)

**Description :** Récupère automatiquement les données depuis un workflow N8N spécifique au Cas 6, puis les convertit en documents Word.

**Utilisation :**
```bash
python execute_cas6_production.py
```

**Workflow complet :**
1. 🌐 **Appel API** : POST vers `http://localhost:5678/webhook/skill_feuilles_revision_cas6`
2. 📥 **Extraction** : Récupère le champ `Data_integrale` (tableau de feuilles de révision)
3. 💾 **Sauvegarde** : Crée des fichiers JSON temporaires pour chaque feuille
4. 🔄 **Conversion** : Exécute `json2word_feuilles_revision.py` sur chaque feuille
5. 📄 **Génération** : Produit les documents Word avec horodatage unique

**Avantages :**
- ✅ **Automatisation complète** : Workflow end-to-end depuis N8N
- ✅ **Intégration native** : S'intègre dans vos pipelines d'audit
- ✅ **Batch processing** : Traite plusieurs feuilles de révision en une seule exécution
- ✅ **Traçabilité** : Sauvegarde les réponses API et les fichiers intermédiaires
- ✅ **Production-ready** : Gestion d'erreurs, logs détaillés, statistiques

**Cas d'usage typiques :**
- Production documentaire en masse de feuilles de révision
- Génération automatique depuis bases de données d'audit
- Intégration dans workflows de mission d'audit (terrain)
- Automatisation planifiée (génération après chaque mission)

**Configuration N8N requise :**
- Webhook : `http://localhost:5678/webhook/skill_feuilles_revision_cas6`
- Nœud "Edit Fields" avec champ `Data_integrale` (type Array)
- Données formatées selon la structure Input Format (voir ci-dessous)

---

## Input Format

Le JSON d'entrée suit une structure dédiée aux feuilles de révision d'audit :

```json
{
  "Feuille de révision - Test des contrôles": [
    {
      "table 1": {
        "Etape de mission": "Feuille de révision - Tests des contrôles clés",
        "Document": "Feuille de test et de pointage des contrôles",
        "Processus": "Audit interne - Phase de réalisation",
        "Cycle d'activité": "Vérification de l'efficacité des contrôles",
        "Secteur d'activité": "Banque, Industrie et Assurance UMOA",
        "Critère d'audit": "Efficacité des contrôles préventifs et détectifs",
        "Reference": "FDR-AUD-TEST-CTRL-05",
        "Version": "V2.1 - Tests de contrôles renforcés",
        "Etablissement": "Afrika Group Holdings",
        "Auditeur responsable": "Chef de mission / Auditeur senior"
      }
    },
    {
      "table 2": [
        {
          "N° Test": "T-001",
          "Objectif de contrôle": "Séparer les fonctions d'engagement et de validation",
          "Nature du contrôle": "Préventif - Séparation des tâches",
          "Procédure de test": "- Examiner matrice des habilitations\n- Vérifier l'absence de cumul de rôles\n- Tester 15 opérations d'engagement",
          "Taille échantillon": "15 engagements / 120 total (12,5%)",
          "Résultat observé": "14/15 conformes - 1 anomalie détectée",
          "Écart identifié": "1 opérateur cumule engagement et validation (mission temporaire)",
          "Conclusion": "Contrôle efficace avec réserve mineure",
          "Action recommandée": "Régulariser la situation temporaire sous 30 jours"
        },
        {
          "N° Test": "T-002",
          "Objectif de contrôle": "Valider les limites d'autorisation par niveau",
          "Nature du contrôle": "Préventif - Limites d'autorisation",
          "Procédure de test": "- Extraire 20 transactions > seuil\n- Vérifier signatures conformes\n- Contrôler traçabilité des approbations",
          "Taille échantillon": "20 transactions / 85 total (23,5%)",
          "Résultat observé": "20/20 conformes - Aucune anomalie",
          "Écart identifié": "Aucun écart détecté",
          "Conclusion": "Contrôle efficace et bien appliqué",
          "Action recommandée": "Maintenir le dispositif actuel"
        }
      ]
    }
  ]
}
```

### Structure détaillée :

- **Clé principale** : `"Feuille de révision - [Titre]"` contient un array
- **table 1** : Dictionnaire avec métadonnées de la feuille (en-tête, références, critères)
- **table 2** : Array d'objets représentant les tests effectués avec résultats

### Colonnes de la table 2 :

1. **N° Test** : Identifiant unique du test (ex: "T-001")
2. **Objectif de contrôle** : But du test effectué
3. **Nature du contrôle** : Type de contrôle (Préventif/Détectif/Correctif)
4. **Procédure de test** : Actions effectuées (format multiligne avec puces)
5. **Taille échantillon** : Nombre d'éléments testés / Total (%)
6. **Résultat observé** : Constat factuel du test
7. **Écart identifié** : Non-conformités détectées
8. **Conclusion** : Synthèse de l'évaluation
9. **Action recommandée** : Recommandation de l'auditeur

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
- Exemple : `"Logiciel automatisé E-audit pro 2.0 - Feuille révision tests contrôles"`

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

### 5. Règles de Nommage des Fichiers (Cas 6 - Horodatage)

**Formule standard** :
```
[Etape de mission] ― [Nom logiciel]_V1_HH-MM-SS_DD.MM.YY.docx
```

**Exemple complet** :
```
Feuille_revision_tests_controles ― Logiciel automatisé E-audit pro_V1_15-30-45_31.10.26.docx
```

**Décomposition** :
- `Feuille_revision_tests_controles` : Étape de mission (espaces remplacés par `_`)
- `Logiciel automatisé E-audit pro` : Nom du logiciel (par défaut)
- `V1` : Version
- `15-30-45` : Heure (15h 30min 45sec)
- `31.10.26` : Date (31 octobre 2026)

**Avantages du timestamp (Cas 6)** :
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
- Valeurs simples ou complexes rendues proprement

### Table 2 (grille) :
- 9 colonnes configurées avec largeurs spécifiques
- En-tête : fond bordeaux (#7B1E3A), texte blanc gras
- **Bordures** :
  - Colonnes : visibles (grises #999999)
  - Lignes : invisibles (blanches #FFFFFF)
- **Ligne vide** insérée après chaque ligne renseignée (pour lisibilité)
- Colonne "N° Test" : en gras
- Colonne "Procédure de test" : actions en puces (une par ligne `\n`)
- Colonnes de résultats : mise en forme claire et lisible

---

## Technical Implementation

### Script Python : `json2word_feuilles_revision.py`

Le script utilise :
- `python-docx` pour la génération Word
- Configuration des colonnes dans `COLUMN_SPECS`
- Gestion automatique des largeurs de colonnes
- Extraction intelligente du JSON (même entouré de texte)

**Ce script est adapté du Cas 2/3** avec colonnes spécifiques aux feuilles de révision.

### Workflow Cas 6 : Appel API N8N + Conversion Automatique

**Script principal : `execute_cas6_production.py`**

Fonctionnalités :
- Appelle le webhook N8N : `http://localhost:5678/webhook/skill_feuilles_revision_cas6`
- Extrait automatiquement `Data_integrale`
- Traite chaque feuille avec le skill `json2word_feuilles_revision.py`
- Génère les documents dans `sortie_word_cas6/`
- Références avec timestamp : `V1_HH-MM-SS_DD.MM.YY`

**Architecture du Cas 6 :**

```
┌──────────────────┐
│   N8N Workflow   │  ← Configuration : webhook skill_feuilles_revision_cas6
│   localhost:5678 │
└────────┬─────────┘
         │ HTTP POST
         ↓
┌──────────────────────────────┐
│ execute_cas6_production.py   │
│                              │
│ 1. call_n8n_api()            │  ← Requête POST + extraction JSON
│ 2. extract_data_integrale()  │  ← Parse Data_integrale
│ 3. process_feuilles()        │  ← Boucle sur chaque feuille
│    └─> json2word_feuilles.py │  ← Conversion individuelle
└────────┬─────────────────────┘
         │
         ↓
┌──────────────────────────────┐
│ Documents Word Générés       │
│ sortie_word_cas6/            │
│                              │
│ • Feuille_revision_*_V1*.docx│
│ • Feuille_test_*_V1*.docx    │
└──────────────────────────────┘
```

**Configuration N8N requise :**

Dans le workflow N8N `skill_feuilles_revision_cas6` :

1. **Nœud "Webhook"** : 
   - Path : `/webhook/skill_feuilles_revision_cas6`
   - Method : POST

2. **Nœud "Edit Fields"** :
   - Mode : "Define Below"
   - Field : `Data_integrale` (Type: Array)
   - Value : Tableau de feuilles de révision JSON

3. **Nœud "Respond to Webhook"** :
   - Respond With : "Using 'Respond to Webhook' Node"
   - Response Body : `{{ $json }}`

**Dépendances Cas 6 :**
```bash
pip install requests python-docx
```

### Configuration des colonnes (COLUMN_SPECS) :

```python
COLUMN_SPECS = {
    "N° Test":              ("N° Test",        800,  "bold"),
    "Objectif de contrôle": ("Objectif",       1800, "text"),
    "Nature du contrôle":   ("Nature",         1400, "text"),
    "Procédure de test":    ("Procédure",      2400, "nl"),
    "Taille échantillon":   ("Échantillon",    1200, "text"),
    "Résultat observé":     ("Résultat",       1600, "text"),
    "Écart identifié":      ("Écart",          1800, "text"),
    "Conclusion":           ("Conclusion",     1400, "text"),
    "Action recommandée":   ("Action",         1600, "text"),
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
6. ✅ Table 2 : 9 colonnes, 1 + 2×N lignes (en-tête + N tests + N lignes vides)
7. ✅ Couleur en-têtes = #7B1E3A
8. ✅ Aucune donnée JSON perdue
9. ✅ Nom de fichier conforme au format avec horodatage

---

## Usage Examples

### Exemple 1 : Workflow Production (Cas 6 - API N8N)

```bash
# Récupère les feuilles de révision depuis N8N et les convertit automatiquement
# URL : http://localhost:5678/webhook/skill_feuilles_revision_cas6
# Sortie : sortie_word_cas6/*.docx avec horodatage
python execute_cas6_production.py
```

**Ce qui se passe en Cas 6 :**
1. 🌐 Appel API POST vers le webhook N8N Cas 6
2. 📥 Extraction du champ `Data_integrale` (liste de feuilles de révision)
3. 💾 Sauvegarde temporaire de chaque feuille en JSON
4. 🔄 Exécution automatique du skill pour chaque feuille
5. 📄 Génération des documents Word avec timestamp unique
6. 📁 Sortie : `Feuille_revision_tests ― E-audit pro_V1_15-30-45_31.10.26.docx`

**Format du nom de fichier (Cas 6)** :
```
<Etape_de_mission> ― <Logiciel>_V1_<HH-MM-SS>_<DD.MM.YY>.docx
```

Exemples :
- `Feuille_revision_tests_controles ― Logiciel automatisé E-audit pro_V1_15-30-45_31.10.26.docx`
- `Feuille_pointage_operations ― Logiciel automatisé E-audit pro_V1_15-31-22_31.10.26.docx`

**Configuration requise pour le Cas 6 :**

Dans N8N (nœud "Edit Fields") :
- **Mode** : "Define Below"
- **Field Name** : `Data_integrale`
- **Field Type** : `Array`
- **Field Value** : Tableau JSON de feuilles de révision (voir structure Input Format)

**Exécution batch Windows :**
```bash
execute_cas6.bat
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
- Activer le workflow `skill_feuilles_revision_cas6`
- Tester le webhook avec un outil (Postman, curl)
- Vérifier que `Data_integrale` est bien configuré

❌ **À éviter :**
- Exécuter le script sans N8N actif
- Oublier d'activer le workflow dans N8N
- Utiliser une URL de webhook incorrecte

### 2. Organisation des fichiers

```
Cas_6/
├── json2word_feuilles_revision.py   # Script de conversion
├── execute_cas6_production.py       # Orchestrateur principal
├── execute_cas6.bat                 # Batch Windows
├── sortie_word_cas6/                # Documents générés
├── temp_feuilles_cas6/              # JSON temporaires
└── data_json_from_n8n_cas6/         # Réponses API sauvegardées
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

# 4. Exécuter le workflow Cas 6
python execute_cas6_production.py

# 5. Vérifier les documents générés
ls sortie_word_cas6/
```

---

## Extending the Skill

### Ajouter de nouvelles colonnes

Si votre JSON contient d'autres colonnes spécifiques aux feuilles de révision :

```python
# Dans le script json2word_feuilles_revision.py (section COLUMN_SPECS)
COLUMN_SPECS["Risque associé"] = ("Risque", 1500, "text")
COLUMN_SPECS["Impact évalué"] = ("Impact", 1200, "bold")
COLUMN_SPECS["Recommandations détaillées"] = ("Recommandations", 4000, "nl")
```

### Modifier l'URL du webhook

```python
# Dans execute_cas6_production.py
WEBHOOK_URL = "http://localhost:5678/webhook/skill_feuilles_revision_cas6"
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
curl -X POST http://localhost:5678/webhook/skill_feuilles_revision_cas6 \
     -H "Content-Type: application/json" \
     -d '{}'
```

### Test du workflow complet

```bash
# Exécuter en mode test
python execute_cas6_production.py
```

---

## License & Attribution

Ce skill est basé sur le script `json2word_audit.py` développé pour l'automatisation documentaire E-procedure, adapté aux feuilles de révision d'audit.

**Utilisation** : Libre pour automatisation de feuilles de révision et de test d'audit.

**Référence normative** : Normes IIA (Institute of Internal Auditors) / CRIPP 2025

**Contact** : Whatsapp + 225 05 44 13 07 98

---

## Changelog

### Version 1.0.0 (2026-10-31)
- ✨ Création initiale du skill Cas 6
- ✅ Support complet du workflow N8N dédié aux feuilles de révision
- ✅ Adaptation du script pour 9 colonnes de tests d'audit
- ✅ Horodatage au format V1_HH-MM-SS_DD.MM.YY
- ✅ Orchestrateur `execute_cas6_production.py` avec logs détaillés
- ✅ Batch processing de multiples feuilles de révision
- ✅ Documentation complète avec exemples
- 📦 Dépendances : `python-docx`, `requests`
