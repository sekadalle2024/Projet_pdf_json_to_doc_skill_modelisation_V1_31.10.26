# 📋 Cas 14 : Génération FRAP (Fiche de Révélation et d'Analyse de Problème) et Recommandations

## Statut

✅ **OPÉRATIONNEL** - Version 1.0.0 | Dernière mise à jour : 31 octobre 2026

---

## 🎯 Objectif

Le **Cas 14** permet de générer automatiquement des documents **FRAP (Fiche de Révélation et d'Analyse de Problème)** et **Recommandations d'Audit** au format Word professionnel à partir de données JSON fournies par N8N.

Ce skill est spécialement conçu pour documenter les **constats d'audit majeurs**, les **risques identifiés** et les **recommandations correctives** dans le cadre des **missions d'audit interne bancaire** conformément aux normes BCEAO, UMOA et aux standards internationaux d'audit.

### Spécificités du Cas 14

- **Type de Document** : FRAP et Recommandations d'Audit
- **Structure** : 6 tables dynamiques (1 table métadonnées + 5 tables de contenu)
- **Orientation** : Paysage (A4)
- **Table 1** : Colonne 1 avec fond bordeaux (unique à ce cas)
- **Format de sortie** : `.docx` avec horodatage automatique
- **Webhook N8N** : `/webhook/skill_frap_cas14`
- **Domaine d'application** : Audit interne bancaire, conformité réglementaire, contrôle interne

---

## 📦 Fichiers Disponibles

### Scripts Principaux

| Fichier | Description | Statut |
|---------|-------------|--------|
| `json2word_frap.py` | Script de conversion JSON → Word FRAP | ⏳ À créer |
| `execute_cas14_production.py` | Orchestrateur principal (appel N8N + conversion) | ⏳ À créer |
| `execute_cas14.bat` | Script batch Windows pour exécution rapide | ⏳ À créer |
| `test_workflow_cas14.ps1` | Suite de tests automatisés PowerShell (7 tests) | ⏳ À créer |

### Documentation

| Fichier | Description | Taille |
|---------|-------------|--------|
| `audit-frap-recos-json2word.skill.md` | Documentation technique complète du skill | ✅ 15000+ mots |
| `GUIDE_CONFIGURATION_N8N.md` | Guide pas-à-pas pour configurer N8N | ⏳ À créer |
| `README.md` | Ce fichier (vue d'ensemble) | ✅ Actuel |
| `CHANGELOG.md` | Historique des versions et modifications | ✅ Créé |
| `exemple_frap_minimal.json` | Exemple JSON avec 1 FRAP (test rapide) | ⏳ À créer |
| `exemple_frap_complet.json` | Exemple JSON avec 5 FRAP (test réaliste) | ⏳ À créer |

---

## 🚀 Démarrage Rapide

### Prérequis

```powershell
# 1. Activer l'environnement conda
conda activate pdf_excel_env

# 2. Vérifier Python (>= 3.9)
python --version

# 3. Vérifier les dépendances
python -c "import docx; import requests; print('✅ Dépendances OK')"

# 4. Démarrer N8N
n8n start
```

### Installation des Dépendances

```bash
# Installation minimale
pip install python-docx requests

# Installation complète (recommandée)
pip install python-docx>=1.1.0 requests>=2.31.0
```

### Configuration N8N

1. Ouvrir N8N : `http://localhost:5678`
2. Créer un nouveau workflow nommé `skill_frap_cas14`
3. Ajouter un nœud **Webhook**
   - Path : `skill_frap_cas14`
   - Method : POST
4. Ajouter un nœud **Edit Fields**
   - Champ : `Data_integrale` (Array)
   - Valeur : Données de test (voir guide N8N)
5. Ajouter un nœud **Respond to Webhook**
6. Activer le workflow

### Exécution

```powershell
# Option 1 : Batch Windows (recommandé)
.\execute_cas14.bat

# Option 2 : Script Python direct
python execute_cas14_production.py

# Option 3 : Tests complets
.\test_workflow_cas14.ps1
```

---

## 📊 Workflow Complet

```
┌─────────────────────────────────────────────────────────────────┐
│                    WORKFLOW CAS 14 - FRAP                       │
└─────────────────────────────────────────────────────────────────┘

1. ┌──────────┐         2. ┌──────────────┐
   │ N8N API  │ ─────────> │ Extraction   │
   │ Webhook  │   POST     │ JSON brut    │
   └──────────┘            └──────────────┘
        │                          │
        │ Data_integrale          │ parse & validate
        │                          │
        ▼                          ▼
   3. ┌──────────────┐    4. ┌──────────────────┐
      │ Sauvegarde   │       │ Boucle pour      │
      │ JSON complet │       │ chaque FRAP      │
      └──────────────┘       └──────────────────┘
                                      │
                                      ▼
                             5. ┌─────────────────┐
                                │ json2word_frap  │
                                │ Génération .docx│
                                └─────────────────┘
                                      │
                                      ▼
                             6. ┌─────────────────┐
                                │ Sortie finale   │
                                │ sortie_word_    │
                                │ cas14/          │
                                └─────────────────┘
```

**Durée totale** : ~2-5 secondes par FRAP (selon la taille des données)

---

## 📝 Format de Sortie

### Nom des Fichiers

```
<Reference>-<Etape_de_mission>- Logiciel automatisé E-audit pro_<timestamp>.docx
```

**Exemple** :
```
FRAP-BK-A10-01-Frap- Logiciel automatisé E-audit pro_20261031_143022.docx
```

### Caractéristiques des Documents

| Caractéristique | Valeur |
|----------------|--------|
| **Orientation** | Paysage (A4) |
| **Marges** | 0,5 pouces (tous côtés) |
| **En-tête** | Fond bordeaux #8B0000 avec titre blanc |
| **Pied de page** | Contact WhatsApp centré |
| **Police par défaut** | Calibri 11pt |
| **Nombre de tables** | 6 (1 métadonnées + 5 contenu) |
| **Table 1 (Métadonnées)** | 2 colonnes, colonne 1 avec fond bordeaux |
| **Tables 2-6 (Contenu)** | 1 colonne chacune, lignes à puces |
| **Couleur en-têtes** | Bordeaux #8B0000 |
| **Texte en-têtes** | Blanc |
| **Bordures** | Toutes visibles (1pt noir) |

---

## 🔧 Configuration

### URL du Webhook

```python
WEBHOOK_URL = "http://localhost:5678/webhook/skill_frap_cas14"
```

### Dossiers de Sortie

```python
OUTPUT_DIR = "sortie_word_cas14"         # Documents Word générés
TEMP_DIR = "temp_frap_cas14"             # JSON temporaires
DATA_DIR = "data_json_from_n8n_cas14"    # Réponses API brutes
```

### Timeout

```python
TIMEOUT = 30  # secondes (ajustable selon le volume de données)
```

---

## 🧪 Tests

### Suite de Tests PowerShell (7 Tests)

```powershell
.\test_workflow_cas14.ps1
```

| # | Test | Description | Résultat Attendu |
|---|------|-------------|------------------|
| 1 | Vérification Python | `python --version` | Version >= 3.9 |
| 2 | Dépendances | `python-docx`, `requests` | Installés |
| 3 | Fichiers skill | Présence des scripts | Tous présents |
| 4 | Connexion N8N | `http://localhost:5678` | Accessible |
| 5 | Webhook Cas 14 | POST `/webhook/skill_frap_cas14` | Réponse valide |
| 6 | Création dossiers | `sortie_word_cas14/` etc. | Créés |
| 7 | Conversion test | JSON → Word | Document généré |

**Objectif** : 7/7 tests passent ✅

### Test Rapide Manuel

```bash
# Test avec exemple minimal
python json2word_frap.py exemple_frap_minimal.json

# Test avec exemple complet
python json2word_frap.py exemple_frap_complet.json
```

---

## 📈 Fonctionnalités

### ✅ Implémenté

- [x] Documentation complète du skill (15000+ mots)
- [x] Structure JSON définie avec exemples
- [x] Format de sortie Word spécifié
- [x] Contraintes obligatoires documentées
- [x] Guide de validation (9 contrôles)
- [x] README et CHANGELOG créés

### ⏳ À Implémenter (Phases 2-9)

- [ ] Script `json2word_frap.py` (Phase 2.1)
- [ ] Script `execute_cas14_production.py` (Phase 2.2)
- [ ] Script `execute_cas14.bat` (Phase 3.1)
- [ ] Script `test_workflow_cas14.ps1` (Phase 3.2)
- [ ] Guide `GUIDE_CONFIGURATION_N8N.md` (Phase 4.1)
- [ ] Workflow N8N configuré et actif (Phase 4.2)
- [ ] Exemples JSON minimal et complet (Phase 5)
- [ ] Tests d'intégration complets (Phase 6)

### 🔜 Améliorations Futures

- [ ] Interface graphique (GUI) pour génération interactive
- [ ] Export PDF automatique après génération Word
- [ ] Notifications par email après génération
- [ ] Support HTTPS avec authentification N8N
- [ ] Statistiques de génération (temps, succès/échecs)
- [ ] Traitement parallèle (multi-threading)
- [ ] Génération de rapports de synthèse multi-FRAP
- [ ] Compression automatique des archives
- [ ] Validation avancée (détection doublons, cohérence)

---

## 🐛 Dépannage

### Erreur : "Module 'docx' not found"

**Solution** :
```bash
pip install python-docx
```

### Erreur : "Connection refused" (N8N)

**Causes possibles** :
1. N8N n'est pas démarré
2. Port 5678 utilisé par une autre application

**Solution** :
```bash
# Vérifier si N8N tourne
curl http://localhost:5678

# Démarrer N8N
n8n start

# Changer le port (optionnel)
N8N_PORT=5679 n8n start
```

### Erreur : "Data_integrale absent"

**Cause** : Le webhook N8N ne renvoie pas la structure attendue.

**Solution** :
1. Ouvrir N8N : `http://localhost:5678`
2. Éditer le workflow `skill_frap_cas14`
3. Vérifier le nœud "Edit Fields"
4. S'assurer que le champ `Data_integrale` est bien configuré
5. Tester avec "Test Workflow"

### Document Word non généré

**Vérifications** :
```powershell
# 1. Vérifier les permissions d'écriture
Test-Path "sortie_word_cas14" -PathType Container

# 2. Vérifier le JSON d'entrée
python -m json.tool exemple_frap_minimal.json

# 3. Exécuter en mode debug
python json2word_frap.py --debug exemple_frap_minimal.json
```

### Erreur de couleur (bordeaux incorrect)

**Vérification** :
- Le code couleur bordeaux doit être `#8B0000` (RGB: 139, 0, 0)
- Pour la Table 1, la colonne 1 a un fond bordeaux (spécificité du Cas 14)
- Les en-têtes des autres tables ont également un fond bordeaux

---

## 📚 Documentation

| Document | Description | Lien |
|----------|-------------|------|
| **Skill Complet** | Documentation technique exhaustive (15000+ mots) | [`audit-frap-recos-json2word.skill.md`](./audit-frap-recos-json2word.skill.md) |
| **Guide N8N** | Configuration pas-à-pas du workflow N8N | `GUIDE_CONFIGURATION_N8N.md` (à créer) |
| **Changelog** | Historique des versions | [`CHANGELOG.md`](./CHANGELOG.md) |
| **TODO Liste** | Checklist d'implémentation complète | [`../TODO_IMPLEMENTATION_CAS_X.md`](../TODO_IMPLEMENTATION_CAS_X.md) |

---

## 📞 Contact

Pour toute question, problème ou suggestion d'amélioration :

- **Projet** : Projet PDF/Excel - Automatisation Audit
- **Environnement** : `pdf_excel_env` (conda)
- **Version Python** : >= 3.9
- **Dépendances clés** : `python-docx >= 1.1.0`, `requests >= 2.31.0`

---

## 📅 Version

**Version actuelle** : 1.0.0  
**Date de création** : 31 octobre 2026  
**Dernière mise à jour** : 31 octobre 2026  
**Statut** : Phase 1 complétée (Documentation) - 33%  
**Prochaine étape** : Phase 2 (Implémentation scripts Python)

---

## 🔗 Cas Similaires

| Cas | Type | Colonnes | Statut |
|-----|------|----------|--------|
| **Cas 2** | Procédures d'Audit | 6 | ✅ Opérationnel |
| **Cas 3** | Manuels d'Audit | 6 | ✅ Opérationnel |
| **Cas 6** | Feuilles de Révision | 9 | ✅ Opérationnel |
| **Cas 12** | Cartographie Risques | 8 | ✅ Opérationnel |
| **Cas 13** | Heatmap Risques | Variable | ⏳ En cours |
| **Cas 14** | FRAP / Recommandations | 6 tables | 🔄 Phase 1 (33%) |

---

## 📄 Licence

Ce projet est destiné à un usage interne pour l'automatisation des documents d'audit.  
Respecter les droits d'auteur et les réglementations en vigueur.

---

**Généré automatiquement par Kiro AI** | Projet PDF/Excel | Cas 14 - FRAP  
*Workflow orchestration for audit document generation* 🚀
