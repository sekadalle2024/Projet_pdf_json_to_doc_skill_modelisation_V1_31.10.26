# Cas 6 - Feuilles de Révision (API N8N)

## 📋 Description

Conversion automatisée des **feuilles de révision d'audit** (avec tests et pointages) récupérées depuis un workflow **N8N** vers des documents Word au format E-procedure.

## ✅ Statut : DOCUMENTÉ - PRÊT POUR IMPLÉMENTATION

Le skill Cas 6 est **entièrement documenté** selon les standards des Cas 2 et 3. Les scripts Python restent à implémenter.

## 🎯 Objectif

Automatiser la génération de documents Word professionnels pour les feuilles de révision d'audit (tests, pointages, conclusions), en récupérant les données depuis une API N8N dédiée.

## 📦 Fichiers Disponibles

### Documentation
- ✅ `audit-feuilles-revision-json2word.skill.md` - Documentation complète du skill (NOUVEAU)
- ✅ `README.md` - Ce fichier (MIS À JOUR)
- 📋 `audit-etap_mission_feuille_revision.skill` - Archive du skill original

### Scripts à Implémenter
- ⏳ `json2word_feuilles_revision.py` - Script de conversion JSON → Word
- ⏳ `execute_cas6_production.py` - Orchestrateur principal (workflow complet)
- ⏳ `execute_cas6.bat` - Script batch Windows pour exécution simplifiée
- ⏳ `GUIDE_CONFIGURATION_N8N.md` - Guide détaillé de configuration N8N

## 🚀 Structure Prévue (À Implémenter)

### 1. Installation des Dépendances

```bash
# Avec Conda (recommandé)
conda activate pdf_excel_env
pip install python-docx requests

# Ou avec pip standard
pip install python-docx requests
```

### 2. Configuration N8N (À créer)

1. **Démarrer N8N** :
   ```bash
   n8n start
   ```

2. **Créer le workflow** : `skill_feuilles_revision_cas6`

3. **Configurer les nœuds** :
   - **Webhook** : `/webhook/skill_feuilles_revision_cas6`
   - **Edit Fields** : Champ `Data_integrale` (Array)
   - **Respond to Webhook** : Retourne le JSON

4. **Activer le workflow** dans l'interface N8N

### 3. Exécution (Une fois implémenté)

```bash
# Méthode 1 : Script Python
python execute_cas6_production.py

# Méthode 2 : Batch Windows
execute_cas6.bat
```

## 📊 Workflow Complet (Prévu)

```
┌──────────────────┐
│   N8N Workflow   │  ← Configuration : webhook skill_feuilles_revision_cas6
│   localhost:5678 │     Champ : Data_integrale (Array de feuilles)
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

## 📝 Format de Sortie (Prévu)

### Nom des Fichiers

**Format** : `[Etape de mission] ― [Logiciel]_V1_HH-MM-SS_DD.MM.YY.docx`

**Exemples** :
- `Feuille_revision_tests_controles ― Logiciel automatisé E-audit pro_V1_15-30-45_31.10.26.docx`
- `Feuille_pointage_operations ― Logiciel automatisé E-audit pro_V1_15-31-22_31.10.26.docx`

### Caractéristiques des Documents

- ✅ Format A4 **paysage**
- ✅ Marges : 0,5" (1,27 cm)
- ✅ En-tête : `[Logiciel] - [Étape de mission]` (fond bordeaux #7B1E3A)
- ✅ Pied de page : Contact WhatsApp centré
- ✅ Tables avec bordures visibles (colonnes) et invisibles (lignes)
- ✅ Ligne vide après chaque enregistrement
- ✅ 9 colonnes spécifiques aux feuilles de révision

## 🔧 Configuration Prévue

### URL du Webhook

**Par défaut** : `http://localhost:5678/webhook/skill_feuilles_revision_cas6`

### Dossiers de Sortie

- `sortie_word_cas6/` - Documents Word générés
- `temp_feuilles_cas6/` - Fichiers JSON temporaires
- `data_json_from_n8n_cas6/` - Réponses API sauvegardées

### Colonnes des Feuilles de Révision

1. **N° Test** - Identifiant unique
2. **Objectif de contrôle** - But du test
3. **Nature du contrôle** - Type (Préventif/Détectif/Correctif)
4. **Procédure de test** - Actions effectuées (multiligne)
5. **Taille échantillon** - Nombre testé / Total (%)
6. **Résultat observé** - Constat factuel
7. **Écart identifié** - Non-conformités
8. **Conclusion** - Synthèse
9. **Action recommandée** - Recommandation

## 📈 Fonctionnalités Prévues

### ✅ Documenté

- ✅ Spécifications complètes du skill
- ✅ Format d'entrée JSON défini
- ✅ Format de sortie Word spécifié
- ✅ Architecture du workflow N8N
- ✅ Exemples d'utilisation
- ✅ Validation Rules
- ✅ Error Handling
- ✅ Best Practices

### ⏳ À Implémenter

- ⏳ Script de conversion `json2word_feuilles_revision.py`
- ⏳ Orchestrateur `execute_cas6_production.py`
- ⏳ Configuration COLUMN_SPECS (9 colonnes)
- ⏳ Workflow N8N
- ⏳ Scripts de test
- ⏳ Guide de configuration N8N détaillé

## 🔗 Relation avec Autres Cas

### Similitudes avec Cas 2 et 3

| Aspect | Cas 2 | Cas 3 | Cas 6 |
|--------|-------|-------|-------|
| **Type de document** | Procédures | Manuels | Feuilles révision |
| **Source de données** | API N8N | API N8N | API N8N |
| **Script de base** | `json2word_audit.py` | Réutilisé | À adapter |
| **Nombre de colonnes** | 6 | 6 | **9** |
| **Format horodatage** | ✅ | ✅ | ✅ |

### Réutilisation Possible

Le script `json2word_audit.py` des Cas 2/3 peut servir de base pour le Cas 6, avec adaptation de :
- `COLUMN_SPECS` : 9 colonnes au lieu de 6
- Noms de colonnes spécifiques aux tests d'audit
- Traitement des résultats de tests (conformes/non-conformes)

## 📚 Documentation

- ✅ `audit-feuilles-revision-json2word.skill.md` - Documentation complète du skill
- ⏳ `GUIDE_CONFIGURATION_N8N.md` - Configuration N8N détaillée (à créer)
- ✅ `README.md` - Ce fichier

## 🔜 Prochaines Étapes

### Phase 1 : Implémentation Scripts (Priorité Haute)

1. Créer `json2word_feuilles_revision.py` basé sur Cas 2/3
2. Adapter `COLUMN_SPECS` pour les 9 colonnes
3. Créer `execute_cas6_production.py` basé sur Cas 3
4. Créer `execute_cas6.bat`

### Phase 2 : Configuration N8N

1. Créer le workflow N8N `skill_feuilles_revision_cas6`
2. Configurer le webhook
3. Tester l'intégration complète
4. Rédiger le guide de configuration détaillé

### Phase 3 : Tests et Validation

1. Tests unitaires du script de conversion
2. Tests d'intégration avec N8N
3. Validation des documents générés
4. Tests de performance (batch processing)

## 📞 Contact

**Support** : Whatsapp + 225 05 44 13 07 98

## 📅 Version

**Version actuelle** : 1.0.0-doc (31 octobre 2026)

**Statut** :
- ✅ **Documentation** : Complète et alignée sur Cas 2/3
- ⏳ **Implémentation** : À réaliser
- ⏳ **Tests** : À réaliser

**Changelog** :
- ✨ Création de la documentation complète du skill Cas 6
- ✅ Alignement sur les standards des Cas 2 et 3
- ✅ Définition de la structure JSON d'entrée (9 colonnes)
- ✅ Spécification du format de sortie Word
- ✅ Documentation du workflow N8N
- 📋 Prêt pour l'implémentation des scripts Python
