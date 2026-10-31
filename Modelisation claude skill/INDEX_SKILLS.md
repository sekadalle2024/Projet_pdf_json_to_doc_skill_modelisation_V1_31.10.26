# Index des Skills - Modélisation Claude Audit

## Vue d'ensemble

Ce projet contient 8 cas d'utilisation de skills pour la génération automatisée de documents d'audit au format E-procedure.

---

## 📁 Cas 1 - JSON Local vers Word

**Dossier** : `Cas_1/`  
**Statut** : ✅ **COMPLÉTÉ**

### Description
Conversion de fichiers JSON locaux (fournis dans le prompt) en documents Word.

### Skill
- **Skill Natif** : `eprocedure-json2word.skill`
- **Skill Standard** : Déjà modelisé

### Mode d'utilisation
- Source : JSON dans le prompt (pas d'API)
- Workflow N8N : Non requis
- Dépendances : `python-docx`

### Fichiers principaux
- `eprocedure-json2word.skill` - Skill natif Claude Opus
- `MEMO_CREATION_SKILLS.md` - Mémo d'élaboration

---

## 📁 Cas 2 - Manuel des Procédures (N8N → Word)

**Dossier** : `Cas_2/`  
**Statut** : ✅ **COMPLÉTÉ** (v1.3.0)

### Description
Récupération automatique via API N8N webhook, puis conversion batch en documents Word.

### Skill
- **Skill Natif** : Claude Opus
- **Skill Standard** : `audit-procedures-json2word.skill` (v1.3.0)

### Étape de mission
- **Manuel des procédures** : Procédures d'audit interne complètes

### Configuration N8N
- **URL** : `http://localhost:5678/webhook/skill_manuel_audit`
- **Méthode** : POST ou GET
- **Champ** : `Data_integrale` (Array)

### Caractéristiques
- ✅ Appel API automatique
- ✅ Extraction `Data_integrale` (structure imbriquée)
- ✅ Batch processing (multiples procédures)
- ✅ Horodatage : `V1_HH-MM-SS_DD.MM.YY`
- ✅ Format : `[Etape] ― [Logiciel]_V1_15-22-03_31.10.26.docx`

### Fichiers principaux
- `audit-procedures-json2word.skill.md` - Documentation complète
- `execute_cas2_production.py` - Orchestrateur principal
- `json2word_audit.py` - Script de conversion
- `api_call_n8n.py` - Module API
- `execute_cas2.bat` - Script batch Windows
- `GUIDE_CONFIGURATION_N8N.md` - Configuration N8N

### Usage
```bash
python execute_cas2_production.py
```

---

## 📁 Cas 3 - Manuel Audit (N8N → Word)

**Dossier** : `Cas_3/`  
**Statut** : ✅ **COMPLÉTÉ** (v1.0.0)

### Description
Manuels méthodologiques d'audit interne récupérés depuis N8N et convertis en documents Word.

### Skill
- **Skill Natif** : Claude Opus
- **Skill Standard** : `audit-manuel-json2word.skill` (v1.0.0)

### Étape de mission
- **Manuel audit** : Manuels méthodologiques d'audit interne

### Configuration N8N
- **URL** : `http://localhost:5678/webhook/skill_manuel_audit_cas3`
- **Méthode** : POST
- **Champ** : `Data_integrale` (Array)

### Caractéristiques
- ✅ Appel API automatique (webhook dédié Cas 3)
- ✅ Extraction `Data_integrale` (structure imbriquée)
- ✅ Batch processing (multiples manuels)
- ✅ Horodatage : `V1_HH-MM-SS_DD.MM.YY`
- ✅ Format : `[Etape] ― [Logiciel]_V1_14-15-10_31.10.26.docx`
- ✅ Réutilisation du script `json2word_audit.py` (Cas 2)

### Fichiers principaux
- `audit-manuel-json2word.skill.md` - Documentation complète
- `execute_cas3_production.py` - Orchestrateur principal
- `json2word_audit.py` - Script de conversion (réutilisé)
- `execute_cas3.bat` - Script batch Windows
- `test_workflow_cas3.ps1` - Tests automatisés
- `GUIDE_CONFIGURATION_N8N.md` - Configuration N8N

### Usage
```bash
python execute_cas3_production.py
# ou
execute_cas3.bat
```

### Tests
```powershell
.\test_workflow_cas3.ps1
```

---

## 📁 Cas 4 - Suivi des Recommandations (N8N → Word)

**Dossier** : `Cas_4/`  
**Statut** : ⏳ **À DÉVELOPPER**

### Description
Tableaux de suivi des recommandations d'audit avec plans d'action.

### Skill à développer
- **Skill Natif** : À générer depuis Claude Opus
- **Skill Standard** : `audit-etap_mission_suivi_recos_standard.skill`

### Étape de mission
- **Suivi des recos** : Tableaux de suivi recommandations

### Tâches
1. ⏳ Générer skill natif Claude Opus
2. ⏳ Définir structure JSON
3. ⏳ Développer script Python
4. ⏳ Configurer N8N

---

## 📁 Cas 5 - FRAP et Recommandations (N8N → Word)

**Dossier** : `Cas_5/`  
**Statut** : ⏳ **À DÉVELOPPER**

### Description
Feuilles de Révélation et d'Analyse de Problème avec recommandations.

### Skill à développer
- **Skill Natif** : À générer depuis Claude Opus
- **Skill Standard** : `audit-etap_mission_frap_recos.skill`

### Étapes de mission
- **FRAP** : Feuilles révélation et analyse
- **Recos contrôle des comptes** : Recommandations comptables
- **Recos contrôle interne comptable** : Recommandations CI

### Structure FRAP
- Problème
- Constat étayé
- Causes racines
- Conséquences
- Recommandations

### Tâches
1. ⏳ Générer skill natif Claude Opus
2. ⏳ Définir structure FRAP JSON
3. ⏳ Développer script Python
4. ⏳ Configurer N8N

---

## 📁 Cas 6 - Feuilles de Révision (N8N → Word)

**Dossier** : `Cas_6/`  
**Statut** : ⏳ **À DÉVELOPPER**

### Description
Feuilles de révision d'audit avec tests et pointages.

### Skill à développer
- **Skill Natif** : À générer depuis Claude Opus
- **Skill Standard** : `audit-etap_mission_feuille_revision.skill`

### Étape de mission
- **Feuille révision** : Feuilles de test d'audit

### Éléments
- Critères de contrôle
- Tests effectués
- Pointages (+ / -)
- Conclusions

### Tâches
1. ⏳ Générer skill natif Claude Opus
2. ⏳ Définir structure tests JSON
3. ⏳ Développer script Python
4. ⏳ Configurer N8N

---

## 📁 Cas 7 - Feuilles de Couverture (N8N → Word)

**Dossier** : `Cas_7/`  
**Statut** : ⏳ **À DÉVELOPPER**

### Description
Feuilles de couverture d'audit avec schéma de calcul automatique.

### Skill à développer
- **Skill Natif** : À générer depuis Claude Opus
- **Skill Standard** : `audit-etap_mission_feuille_couverture.skill`

### Étape de mission
- **Feuille couverture** : Feuilles avec schéma de calcul

### Caractéristiques spéciales
- Insertion schéma de calcul entre table 5 et table 4
- Format cellules : `(A)`, `(B)`, `(C) = (A) - (D)`
- Ajustement largeurs colonnes automatique
- Retrait mention "Schéma de calcul : C = A + B..."

### Tâches
1. ⏳ Générer skill natif Claude Opus
2. ⏳ Implémenter logique schéma calcul
3. ⏳ Développer script Python
4. ⏳ Configurer N8N

---

## 📁 Cas 8 - Modèles Standards Multi-Usage (N8N → Word)

**Dossier** : `Cas_8/`  
**Statut** : ⏳ **À DÉVELOPPER**

### Description
Documents standardisés variés : cartographies, matrices, plans.

### Skill à développer
- **Skill Natif** : À générer depuis Claude Opus
- **Skill Standard** : `audit-etap_mission_feuille_modele_standard.skill`

### Étapes de mission
- **Programme de travail** : Planning missions
- **Cartographie des risques** : Heat maps risques
- **Modélisation** : Processus et flux
- **Plan de recommandation surveillance permanente** : Plans contrôle
- **Matrice de surveillance permanente** : Tableaux de bord

### Types de documents
1. Programme de travail avec jalons
2. Cartographie risques (Impact/Probabilité)
3. Flowcharts processus
4. Plans surveillance permanente
5. Matrices de suivi opérationnel

### Tâches
1. ⏳ Générer skill natif Claude Opus
2. ⏳ Support multi-formats
3. ⏳ Développer script Python
4. ⏳ Configurer N8N

---

## 🔧 Convention de Nommage

### Format Standard (sans timestamp)
```
[référence] ― [Etape_de_mission] ― [Nom_logiciel].docx
```

Exemple :
```
BB01 ― Leadsheet_Ventes ― Logiciel E-révision.docx
```

### Format avec Horodatage (Cas 2-8)
```
[Etape_de_mission] ― [Nom_logiciel]_V1_HH-MM-SS_DD.MM.YY.docx
```

Exemple :
```
Manuel_audit_interne ― Logiciel automatisé E-audit pro_V1_15-22-03_31.10.26.docx
```

**Composants du timestamp** :
- `V1` : Numéro de version
- `HH-MM-SS` : Heure (14h 15min 10sec)
- `DD.MM.YY` : Date française (31 octobre 2026)

---

## 📊 Tableau Récapitulatif

| Cas | Étape Mission | Skill Standard | Mode | Statut |
|-----|---------------|----------------|------|--------|
| 1 | Données locales | eprocedure-json2word | Local | ✅ Complété |
| 2 | Manuel procédures | audit-procedures-json2word v1.3.0 | N8N API | ✅ Complété |
| 3 | Manuel audit | audit-manuel-json2word v1.0.0 | N8N API | ✅ Complété |
| 4 | Suivi recos | suivi_recos_standard | N8N API | ⏳ À développer |
| 5 | FRAP & Recos | frap_recos | N8N API | ⏳ À développer |
| 6 | Feuille révision | feuille_revision | N8N API | ⏳ À développer |
| 7 | Feuille couverture | feuille_couverture | N8N API | ⏳ À développer |
| 8 | Modèles standards | feuille_modele_standard | N8N API | ⏳ À développer |

---

## 🛠️ Dépendances Communes

### Python
```bash
pip install python-docx requests
```

### N8N (Cas 2-8)
- Version : >= 0.x
- Webhook configuré
- Nœud "Edit Fields" avec `Data_integrale`

### Environnement
```bash
conda activate pdf_excel_env
```

---

## 📝 Prochaines Étapes

### Phase 1 - Génération Skills Natifs Claude Opus
1. ⏳ Cas 3 : Manuel audit
2. ⏳ Cas 4 : Suivi recommandations
3. ⏳ Cas 5 : FRAP
4. ⏳ Cas 6 : Feuille révision
5. ⏳ Cas 7 : Feuille couverture
6. ⏳ Cas 8 : Modèles standards

### Phase 2 - Développement Scripts Python
- Adapter `json2word_audit.py` pour chaque cas
- Créer orchestrateurs `execute_casX_production.py`
- Implémenter logiques spécifiques

### Phase 3 - Configuration N8N
- Créer webhooks pour chaque cas
- Configurer nœuds "Edit Fields"
- Tester workflows end-to-end

### Phase 4 - Documentation & Tests
- Rédiger skill.md pour chaque cas
- Créer exemples JSON
- Tests de validation

---

## 📚 Documentation

- `MEMO_CREATION_SKILLS.md` - Méthodologie création skills (Cas_1/)
- `README_PROJET_COMPLET.md` - Vue d'ensemble projet
- `INDEX_DOCUMENTATION.md` - Index général

---

## 🎯 Objectif Final

Système complet de génération automatisée de documents d'audit professionnels au format E-procedure, couvrant tous les types de documents utilisés en audit interne bancaire et industriel.

---

**Dernière mise à jour** : 31 octobre 2026  
**Version** : 1.0.0
