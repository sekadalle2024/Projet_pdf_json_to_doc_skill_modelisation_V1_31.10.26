# 📋 audit-frap-recos-json2word.skill

## Dependencies

### Installation Base (Minimal)
```bash
conda activate pdf_excel_env
pip install python-docx requests
```

### Installation Complète (Optionnelle)
```bash
conda activate pdf_excel_env
pip install python-docx requests openpyxl pandas
```

---

## Metadata

| Métadonnée | Valeur |
|------------|--------|
| **Name** | `audit-frap-recos-json2word` |
| **Version** | `1.0.0` |
| **Author** | Équipe Kiro AI |
| **Description** | Convertit un JSON d'audit contenant des FRAP (Feuilles de Révélation et d'Analyse de Problème), Recommandations, et Recos en document Word structuré au format E-audit pro |
| **Tags** | `audit`, `frap`, `recommandations`, `recos`, `json2word`, `etape-mission`, `n8n`, `api` |
| **Dependencies** | `python-docx >= 1.1.0`, `requests >= 2.28.0` |
| **Python Version** | `>= 3.9` |
| **Created** | 31 octobre 2026 |
| **Last Updated** | 31 octobre 2026 |

---

## Purpose

Ce skill automatise la conversion de données JSON structurées en documents Word professionnels pour les **FRAP (Feuilles de Révélation et d'Analyse de Problème)**, **Recommandations d'audit**, et **Recos** (Recommandations de surveillance permanente).

### Types de documents supportés

1. **FRAP** (Feuille de Révélation et d'Analyse de Problème)
2. **Recommandations d'Audit** (Recos contrôle des comptes)
3. **Recommandations de Contrôle Interne Comptable**
4. **Cartographie des Risques** (si structure compatible)
5. **Matrice de Surveillance Permanente** (si structure compatible)
6. **Feuille de Couverture**

### Caractéristiques clés

- **Tables dynamiques** : Support de `table 1` à `table N` (illimité)
- **Mise en forme professionnelle** : Fond bordeaux (#8B0000), police Arial
- **Structure verticale** : Table 1 en format vertical (Rubrique | Description)
- **Tables horizontales** : Tables 2+ en format grille multi-colonnes
- **Horodatage automatique** : Noms de fichiers avec timestamp

---

## Use Cases

### Workflow Automatisé avec API N8N

```
┌──────────────┐
│   N8N API    │
│   Webhook    │  → JSON brut
└──────┬───────┘
       │
       ▼
┌──────────────────┐
│ execute_cas14    │
│ _production.py   │  → Extraction Data_integrale
└──────┬───────────┘
       │
       ▼
┌──────────────────┐
│ json2word_frap   │
│ _recos.py        │  → Documents Word
└──────┬───────────┘
       │
       ▼
┌──────────────────┐
│  Documents Word  │
│    générés       │
└──────────────────┘
```

**Avantages** :
- ✅ Automatisation complète
- ✅ Traitement en masse
- ✅ Sauvegarde de l'historique
- ✅ Zéro intervention manuelle

---

## Input Format

### Structure Globale

Le JSON doit contenir une structure **Data_integrale** qui peut être encapsulée dans différents niveaux :

```json
{
  "Data_integrale": [
    {
      "Etape mission - FRAP": [ ... ]
    }
  ]
}
```

**Ou directement** :

```json
[
  {
    "Etape mission - FRAP": [ ... ]
  }
]
```

### Structure Détaillée : Etape mission

La clé principale est de la forme `"Etape mission - <Type>"` où `<Type>` peut être :
- `Frap`
- `Recos contrôle des comptes`
- `Recos contrôle interne comptable`
- `Feuille couverture`
- `Matrice de surveillance`

**Format** :

```json
{
  "Etape mission - Frap": [
    {
      "table 1": {
        "Etape de mission": "Frap",
        "Norme": "Norme 14.3 Évaluation des constats",
        "Méthode": "Méthode des recommandations par les constats d'audit",
        "Reference": "FRAP-BK-A10-01"
      }
    },
    {
      "table 2": {
        "Intitule": "Détournement de 34 millions FCFA sur compte dormant"
      }
    },
    {
      "table 3": {
        "Observation": "Le cadre réglementaire (Circulaire N°03-2017/CB/C..."
      }
    },
    {
      "table 4": {
        "Constat": "- Suppression manuelle du contrôle obligatoire...\n- Réactivation unilatérale..."
      }
    },
    {
      "table 5": {
        "Risque": "- Risque de sanction disciplinaire...\n- Risque de perte financière..."
      }
    },
    {
      "table 6": {
        "Recommendation": "Afin de rétablir la conformité réglementaire..."
      }
    }
  ]
}
```

### Tables Supportées

#### Table 1 (Métadonnées - Format Vertical)

**Structure** : Dictionnaire de clés/valeurs

```json
{
  "table 1": {
    "Etape de mission": "Frap",
    "Norme": "Norme 14.3 Évaluation des constats",
    "Méthode": "Méthode des recommandations",
    "Reference": "FRAP-BK-A10-01",
    "Date": "31 octobre 2026",
    "Auditeur": "Chef de mission Audit Interne"
  }
}
```

**Rendu** : Tableau vertical 2 colonnes
- **Colonne 1** : Rubrique (fond bordeaux, texte blanc gras)
- **Colonne 2** : Description (texte noir)

#### Tables 2+ (Contenu - Format Variable)

**Format 1 : Dictionnaire à clé unique** (rendu : tableau 1 colonne)

```json
{
  "table 2": {
    "Intitule": "Texte du titre ou description"
  }
}
```

**Format 2 : Dictionnaire multi-clés** (rendu : tableau vertical)

```json
{
  "table 3": {
    "Observation": "Texte de l'observation détaillée...",
    "Contexte": "Contexte réglementaire...",
    "Périmètre": "Échantillon A10, agence de Bouaké"
  }
}
```

**Format 3 : Liste d'objets** (rendu : tableau horizontal multi-colonnes)

```json
{
  "table 4": [
    {
      "N°": "1",
      "Constat": "Suppression du contrôle",
      "Gravité": "Élevée",
      "Responsable": "Contrôle Interne"
    },
    {
      "N°": "2",
      "Constat": "Réactivation unilatérale",
      "Gravité": "Critique",
      "Responsable": "Chef d'Agence"
    }
  ]
}
```

---

## Contraintes Obligatoires

### 1. Format du Document

- **Orientation** : Paysage (A4)
- **Police** : Arial 8,5 pt
- **Marges** :
  - Haut : 1200 twips (0,5")
  - Bas : 1100 twips (~0,46")
  - Gauche/Droite : 900 twips (~0,38")
- **Structure** : Uniquement des tableaux (pas de paragraphes libres)

### 2. En-tête et Pied de Page

**En-tête** :
```
Logiciel automatisé E-audit pro - Frap
```
- **Alignement** : Centré
- **Police** : Arial, gras
- **Couleur** : Bordeaux (#8B0000)

**Pied de page** :
```
Automatisez vos activités d'audit, risques et contrôles - Whatsapp : + 225 05 44 13 07 98
```
- **Alignement** : Centré
- **Couleur** : Bordeaux (#8B0000)

### 3. Orientation des Tables

**Table 1 (Métadonnées)** : Format vertical **obligatoire**
- 2 colonnes : `Rubrique | Description`
- Largeurs : 4000 twips | 11038 twips
- Fond colonne 1 : Bordeaux (#8B0000)
- Texte colonne 1 : Blanc, gras

**Tables 2+** : Format adapté au contenu
- Dictionnaire à 1 clé → Tableau 1 colonne
- Dictionnaire multi-clés → Tableau vertical
- Liste d'objets → Tableau horizontal (grille)

### 4. Couleurs et Mise en Forme

| Élément | Couleur RGB | Code Hex | Usage |
|---------|-------------|----------|-------|
| En-têtes de tableau | (139, 0, 0) | #8B0000 | Fond bordeaux |
| Texte en-têtes | (255, 255, 255) | #FFFFFF | Blanc |
| Colonne 1 Table 1 | (139, 0, 0) | #8B0000 | Fond bordeaux |
| Texte colonne 1 Table 1 | (255, 255, 255) | #FFFFFF | Blanc gras |
| Texte corps | (0, 0, 0) | #000000 | Noir |
| Fond corps | (255, 255, 255) | #FFFFFF | Blanc |

### 5. Règles de Nommage des Fichiers

**Format** :
```
<Reference>-<Etape_de_mission>- Logiciel automatisé E-audit pro_<timestamp>.docx
```

**Exemples** :
```
FRAP-BK-A10-01-Frap- Logiciel automatisé E-audit pro_20261031_143022.docx
AUTO-Recos- Logiciel automatisé E-audit pro_20261031_143055.docx
```

**Composants** :
- `<Reference>` : Valeur de `Reference` dans table 1, ou référence auto-générée (ex: AUTO)
- `<Etape_de_mission>` : Valeur de `Etape de mission` dans table 1
- `<timestamp>` : Format `AAAAMMJJ_HHMMSS`

---

## Output Format

### Structure du Document Généré

```
┌─────────────────────────────────────────────────────────┐
│ EN-TÊTE (Bordeaux centré)                               │
│ Logiciel automatisé E-audit pro - Frap                  │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│ TABLE 1 : Métadonnées (Format Vertical)                │
├────────────────────┬────────────────────────────────────┤
│ Etape de mission   │ Frap                               │
│ (fond bordeaux)    │                                    │
├────────────────────┼────────────────────────────────────┤
│ Norme              │ Norme 14.3 Évaluation...           │
│ (fond bordeaux)    │                                    │
├────────────────────┼────────────────────────────────────┤
│ Reference          │ FRAP-BK-A10-01                     │
│ (fond bordeaux)    │                                    │
└────────────────────┴────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│ TABLE 2 : Intitulé (Format 1 colonne)                  │
├─────────────────────────────────────────────────────────┤
│ Intitule (en-tête bordeaux)                             │
├─────────────────────────────────────────────────────────┤
│ Détournement de 34 millions FCFA sur compte dormant... │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│ TABLE 3 : Observation (Format 1 colonne)               │
├─────────────────────────────────────────────────────────┤
│ Observation (en-tête bordeaux)                          │
├─────────────────────────────────────────────────────────┤
│ Le cadre réglementaire (Circulaire N°03-2017/CB/C...  │
└─────────────────────────────────────────────────────────┘

[... Tables 4, 5, 6 suivent le même principe ...]

┌─────────────────────────────────────────────────────────┐
│ PIED DE PAGE (Bordeaux centré)                         │
│ Automatisez vos activités d'audit... WhatsApp...       │
└─────────────────────────────────────────────────────────┘
```

---

## Technical Implementation

### Architecture des Scripts

```
Cas_14/
├── json2word_frap_recos.py         # Script principal de conversion
├── execute_cas14_production.py     # Orchestrateur avec API N8N
├── api_call_n8n.py                 # Module d'appel API (partagé Cas 2)
├── execute_cas14.bat               # Script batch Windows
├── test_workflow_cas14.ps1         # Tests PowerShell
├── audit-frap-recos-json2word.skill.md  # Cette documentation
├── GUIDE_CONFIGURATION_N8N.md      # Configuration N8N détaillée
├── README.md                       # Vue d'ensemble du cas
├── CHANGELOG.md                    # Historique des versions
├── exemple_frap_minimal.json       # Exemple minimal
├── exemple_frap_complet.json       # Exemple complet
├── sortie_word_cas14/              # Dossier de sortie Word
├── temp_frap_cas14/                # Dossier temporaire JSON
└── data_json_from_n8n_cas14/       # Historique des réponses API
```

### COLUMN_SPECS (Unused - Tables dynamiques)

**Note** : Contrairement aux Cas 2, 3, 6, le Cas 14 utilise des **tables dynamiques** sans spécification fixe de colonnes. Chaque table est analysée et rendue selon sa structure JSON.

### Types de Rendu Supportés

| Type JSON | Rendu | Exemple |
|-----------|-------|---------|
| `dict` avec 1 clé | Tableau 1 colonne | `{"Intitule": "Texte"}` |
| `dict` avec 2+ clés | Tableau vertical | `{"Obs": "...", "Ctx": "..."}` |
| `list` d'objets | Tableau horizontal | `[{"N°": "1", ...}, ...]` |

---

## Validation Rules

### Contrôles Avant Conversion

1. ✅ **JSON valide** : Structure syntaxiquement correcte
2. ✅ **Clé principale présente** : `"Etape mission - <Type>"` existe
3. ✅ **Au moins une table** : Minimum `table 1` présent
4. ✅ **Table 1 est un dictionnaire** : Format vertical obligatoire
5. ✅ **Encodage UTF-8** : Caractères spéciaux correctement encodés

### Contrôles Après Conversion

1. ✅ **Fichier .docx ouvrable** : Sans erreur dans Word
2. ✅ **Orientation paysage** : Largeur > Hauteur
3. ✅ **En-tête et pied de page corrects** : Textes et couleurs conformes
4. ✅ **Nombre de tables** : = Nombre de clés `table N` dans JSON
5. ✅ **Table 1 : 2 colonnes** : Format vertical respecté
6. ✅ **Table 1 : Colonne 1 bordeaux** : Fond #8B0000, texte blanc gras
7. ✅ **En-têtes bordeaux** : Couleur #8B0000 pour tous les en-têtes
8. ✅ **Aucune donnée perdue** : Tout le JSON est dans le Word
9. ✅ **Nom de fichier conforme** : Format avec timestamp

---

## Usage Examples

### Exemple 1 : Workflow Production avec N8N

#### Étape 1 : Démarrer N8N

```bash
# Terminal 1
n8n start
```

**Résultat** : N8N accessible sur `http://localhost:5678`

#### Étape 2 : Configurer le Webhook

Dans N8N, créer un workflow avec :
- **Webhook** : Path = `skill_frap_cas14`, Method = POST
- **Edit Fields** : Champ `Data_integrale` (type Array)
- **Respond to Webhook** : Body = `{{ $json }}`

#### Étape 3 : Tester le Webhook

```bash
# Terminal 2
python
>>> import requests
>>> url = "http://localhost:5678/webhook/skill_frap_cas14"
>>> r = requests.post(url)
>>> print(r.status_code)  # Doit afficher 200
>>> print("Data_integrale" in r.json())  # Doit afficher True
```

#### Étape 4 : Exécuter le Workflow Complet

```bash
# Terminal 2
cd "h:\Projet_pdf_excel\Modelisation claude skill\Cas_14"
python execute_cas14_production.py
```

**Résultat attendu** :

```
═══════════════════════════════════════════════════════
   🎯 EXECUTION SKILL CAS 14 : FRAP / RECOS (PRODUCTION)
═══════════════════════════════════════════════════════

[ÉTAPE 1] 📡 Appel API N8N
URL : http://localhost:5678/webhook/skill_frap_cas14
Méthode : POST
Réponse reçue : 200 OK
Taille : 15247 caractères
Data_integrale extrait : 2 éléments

Réponse complète sauvegardée :
→ data_json_from_n8n_cas14/reponse_api_20261031_143022.json

[ÉTAPE 2] 🔄 Exécution du Skill json2word
Traitement de 2 FRAP...

[1/2] FRAP-BK-A10-01-Frap- Logiciel automatisé E-audit pro_20261031_143022.docx
✅ Succès

[2/2] AUTO-Recos- Logiciel automatisé E-audit pro_20261031_143055.docx
✅ Succès

═══════════════════════════════════════════════════════
   📊 RÉSUMÉ FINAL
═══════════════════════════════════════════════════════
Total traités : 2
Succès : 2
Échecs : 0
Taux de succès : 100%

Documents générés dans : sortie_word_cas14/
═══════════════════════════════════════════════════════
```

### Exemple 2 : Conversion d'un Fichier JSON Local

```bash
python json2word_frap_recos.py exemple_frap_complet.json -o sortie_word_cas14
```

**Résultat** :

```
✅ Document Word généré avec succès
📄 Fichier : FRAP-BK-A10-01-Frap- Logiciel automatisé E-audit pro_20261031_143022.docx
📍 Emplacement : sortie_word_cas14/
```

---

## Error Handling

### Erreurs Communes et Solutions

| Code Erreur | Message | Cause | Solution |
|-------------|---------|-------|----------|
| **ERR-JSON-001** | JSON invalide | Syntaxe incorrecte | Valider avec jsonlint.com |
| **ERR-JSON-002** | Clé principale manquante | Pas de `"Etape mission - ..."` | Vérifier la structure |
| **ERR-JSON-003** | Table 1 absente | Pas de `"table 1"` | Ajouter la table 1 |
| **ERR-JSON-004** | Table 1 invalide | Table 1 n'est pas un dict | Convertir en dictionnaire |
| **ERR-CONV-001** | Échec création document | Erreur python-docx | Vérifier python-docx >= 1.1.0 |
| **ERR-CONV-002** | Échec écriture fichier | Permissions insuffisantes | Vérifier droits en écriture |
| **ERR-API-001** | N8N inaccessible | Connection refused | Démarrer N8N |
| **ERR-API-002** | Webhook introuvable | 404 Not Found | Activer le workflow N8N |
| **ERR-API-003** | Timeout API | Pas de réponse | Augmenter timeout (--timeout 60) |
| **ERR-API-004** | Data_integrale absent | Mauvaise config N8N | Vérifier Edit Fields |

### Gestion des Erreurs dans le Script

```python
try:
    # Conversion
    generate_word_document(...)
except json.JSONDecodeError as e:
    print(f"❌ ERR-JSON-001 : JSON invalide - {e}")
except KeyError as e:
    print(f"❌ ERR-JSON-002 : Clé manquante - {e}")
except PermissionError:
    print(f"❌ ERR-CONV-002 : Permissions insuffisantes")
except Exception as e:
    print(f"❌ Erreur inattendue : {e}")
```

---

## Best Practices

### 1. Structuration des Données JSON

**✅ Bonne pratique** :

```json
{
  "Etape mission - Frap": [
    {"table 1": {"Etape de mission": "Frap", "Reference": "FRAP-01"}},
    {"table 2": {"Intitule": "Titre clair et concis"}},
    {"table 3": {"Observation": "Texte détaillé avec puces :\n- Point 1\n- Point 2"}}
  ]
}
```

**❌ Mauvaise pratique** :

```json
{
  "Frap": {  // ❌ Manque "Etape mission - "
    "table 1": "Texte brut",  // ❌ Doit être un dictionnaire
    "table 2": null  // ❌ Valeur null
  }
}
```

### 2. Utilisation des Puces

**Format avec puces** :

```json
{
  "Constat": "- Suppression du contrôle\n- Réactivation unilatérale\n- Falsification du numéro"
}
```

**Rendu** :
```
• Suppression du contrôle
• Réactivation unilatérale
• Falsification du numéro
```

### 3. Gestion des Références

**Référence explicite** (recommandé) :

```json
{
  "table 1": {
    "Reference": "FRAP-BK-A10-01"
  }
}
```

**Référence auto-générée** (fallback) :

Si `Reference` absent → `AUTO-<timestamp>`

### 4. Tests Systématiques

```bash
# Avant chaque livraison
.\test_workflow_cas14.ps1
```

**Résultat attendu** : `7/7 tests passés (100%)`

---

## Extending the Skill

### Ajouter un Nouveau Type de Table

Le skill supporte déjà **toutes les structures JSON** sans modification. Pour personnaliser le rendu :

1. **Identifier le type** : Dict 1 clé, Dict multi-clés, ou Liste
2. **Modifier `json2word_frap_recos.py`** (si besoin de logique spécifique)
3. **Tester avec un exemple** : `exemple_custom.json`

### Exemple : Table avec Calculs

```json
{
  "table 7": {
    "Schéma de calcul": "C = A + B ; Écart = C − D",
    "A": "10000",
    "B": "5000",
    "C": "15000",
    "D": "14500",
    "Écart": "500"
  }
}
```

**Rendu** : Tableau vertical automatique (pas de code supplémentaire nécessaire)

---

## Limitations

### 1. Tables Imbriquées Non Supportées

**Non supporté** :

```json
{
  "table 1": {
    "Rubrique": {
      "Sous-rubrique 1": "Valeur",
      "Sous-rubrique 2": "Valeur"
    }
  }
}
```

**Solution** : Aplatir la structure

```json
{
  "table 1": {
    "Rubrique - Sous-rubrique 1": "Valeur",
    "Rubrique - Sous-rubrique 2": "Valeur"
  }
}
```

### 2. Images et Graphiques Non Supportés

Le skill génère **uniquement du texte** et des **tableaux**. Les images doivent être ajoutées manuellement.

### 3. Formules Word Non Générées

Les calculs dans `"Schéma de calcul"` sont du **texte statique**, pas des formules Word dynamiques.

### 4. Limite de Tables

Théoriquement **illimité**, mais pratiquement recommandé **≤ 20 tables** pour maintenir la lisibilité.

### 5. Encodage

Le script attend du **UTF-8**. Les fichiers en ISO-8859-1 ou Windows-1252 peuvent afficher des caractères corrompus (`Ã©` au lieu de `é`).

**Solution** : Convertir en UTF-8 avant traitement

```python
import json
with open("fichier.json", "r", encoding="utf-8") as f:
    data = json.load(f)
```

---

## Testing

### Test 1 : Connexion N8N

**Objectif** : Vérifier que N8N est accessible

```bash
curl http://localhost:5678
```

**Résultat attendu** : Code HTTP 200

### Test 2 : Webhook Cas 14

**Objectif** : Vérifier que le webhook répond

```bash
curl -X POST http://localhost:5678/webhook/skill_frap_cas14
```

**Résultat attendu** :

```json
{
  "Data_integrale": [
    {
      "Etape mission - Frap": [...]
    }
  ]
}
```

### Test 3 : Workflow Complet PowerShell

**Commande** :

```powershell
.\test_workflow_cas14.ps1
```

**Tests exécutés** :

1. ✅ Python installé
2. ✅ Dépendances Python (python-docx, requests)
3. ✅ Fichiers du skill présents
4. ✅ N8N accessible
5. ✅ Webhook Cas 14 fonctionnel
6. ✅ Dossiers de sortie créés
7. ✅ Conversion JSON → Word

**Résultat attendu** :

```
═══════════════════════════════════════
   RÉSUMÉ DES TESTS
═══════════════════════════════════════
Tests réussis   : 7
Tests échoués   : 0
Taux de succès  : 100%
═══════════════════════════════════════
```

---

## License & Attribution

### License

Ce skill est fourni "tel quel", sans garantie d'aucune sorte.

### Attribution

- **Créateur** : Équipe Kiro AI
- **Basé sur** : Cas 2 (Procédures), Cas 3 (Manuels), Cas 6 (Feuilles Révision)
- **Modèle** : E-audit pro - Logiciel automatisé
- **Version python-docx** : >= 1.1.0

---

## Changelog

### [1.0.0] - 31 octobre 2026

#### ✨ Ajouté
- Script principal `json2word_frap_recos.py`
- Script orchestrateur `execute_cas14_production.py`
- Script de tests `test_workflow_cas14.ps1`
- Support complet des tables dynamiques (table 1 à table N)
- Format vertical pour table 1 (Rubrique | Description)
- Fond bordeaux pour colonne 1 de table 1
- Support des 3 types de rendu (1 colonne, vertical, horizontal)
- Horodatage automatique des fichiers

#### 📋 Documenté
- `audit-frap-recos-json2word.skill.md` (ce document)
- `README.md` avec démarrage rapide
- `CHANGELOG.md` avec historique complet
- `GUIDE_CONFIGURATION_N8N.md` détaillé

#### 🔧 Spécifié
- Format A4 paysage obligatoire
- En-tête et pied de page bordeaux (#8B0000)
- Table 1 avec colonne 1 bordeaux (spécificité Cas 14)
- Règles de nommage avec timestamp
- 9 règles de validation

#### 📚 Aligné
- Architecture conforme aux Cas 2, 3, 6
- Module API réutilisé du Cas 2
- Workflow N8N standardisé
- Tests PowerShell harmonisés

---

## Version

- **Version du Skill** : 1.0.0
- **Date de Création** : 31 octobre 2026
- **Dernière Mise à Jour** : 31 octobre 2026
- **Auteur** : Équipe Kiro AI
- **Statut** : ✅ Production-ready

---

**Document créé le** : 31 octobre 2026  
**Auteur** : Kiro AI  
**Contact** : WhatsApp +225 05 44 13 07 98
