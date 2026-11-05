# 🎯 CAS 10 - ROUTEUR INTELLIGENT DE SKILLS N8N

**Détection automatique et routage vers les skills appropriées**

> **Concept clé** : Cas 10 est un **ROUTEUR**, pas un exécuteur.  
> Il détecte le type de mission et appelle la **skill N8N appropriée**.  
> Chaque skill génère ses propres documents Word.

---

## 📋 Table des Matières

- [Principe de Fonctionnement](#principe-de-fonctionnement)
- [Installation](#installation)
- [Configuration](#configuration)
- [Utilisation](#utilisation)
- [Mapping des Types](#mapping-des-types)
- [Architecture](#architecture)
- [Dépannage](#dépannage)

---

## 🎯 Principe de Fonctionnement

### Le Rôle de Cas 10

Cas 10 est un **orchestrateur intelligent** qui :

1. ✅ Récupère les données du webhook source
2. ✅ **Détecte automatiquement** le type de chaque mission
3. ✅ **Route vers la skill N8N appropriée** (Cas 2, 3, 5, 6, 7, 8)
4. ✅ **Laisse chaque skill générer ses documents**

### Ce que Cas 10 NE fait PAS

❌ Cas 10 ne génère PAS les documents Word lui-même  
❌ Cas 10 n'appelle PAS les scripts Python directement  
❌ Cas 10 ne remplace PAS les skills existantes

### Workflow Complet

```
┌─────────────────────────────────────────────────────────────────┐
│  Cas 10 - Routeur Intelligent                                   │
│                                                                   │
│  1. Appelle webhook source                                       │
│     http://localhost:5678/webhook/skill_manuel_audit            │
│                                                                   │
│  2. Extrait les données (Data_integrale ou DATA_COLLECTION)     │
│                                                                   │
│  3. Détecte les types avec cas10_router.py                      │
│     → Cas 2 : Procédures audit                                  │
│     → Cas 3 : Manuels audit                                     │
│     → Cas 5 : FRAP et Recommandations                           │
│     → Cas 6 : Feuilles de révision                              │
│     → Cas 7 : Feuilles de couverture                            │
│     → Cas 8 : Programme de travail / Cartographie               │
│                                                                   │
│  4. Route vers la skill N8N appropriée                          │
│     POST http://localhost:5678/webhook/skill_xxx_casX           │
│     Payload: { "Data_integrale": [...] }                        │
│                                                                   │
│  5. Chaque skill génère ses documents Word                      │
│     → Cas 2: sortie_word_cas2/                                  │
│     → Cas 3: sortie_word_cas3/                                  │
│     → Cas 5: sortie_word_cas5/                                  │
│     → Cas 6: sortie_word_cas6/                                  │
│     → Cas 7: sortie_word_cas7/                                  │
│     → Cas 8: sortie_word_cas8/                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🔧 Installation

### Prérequis

```powershell
# 1. Environnement conda
conda activate pdf_excel_env

# 2. Python 3.11+
python --version

# 3. Dépendances
pip install requests
```

### Fichiers Requis

```
Cas_10/
├── execute_cas10_orchestrator.py   ← Orchestrateur principal
├── cas10_router.py                 ← Détection intelligente des types
├── execute_cas10.bat               ← Lanceur Windows
└── README.md                       ← Ce fichier
```

---

## ⚙️ Configuration

### Webhooks N8N

Le fichier `execute_cas10_orchestrator.py` contient le mapping des webhooks :

```python
# Webhook source (existant)
WEBHOOK_URL_SOURCE = "http://localhost:5678/webhook/skill_manuel_audit"

# Webhooks des skills (à créer si nécessaire)
CAS_SKILLS_WEBHOOKS = {
    2: "http://localhost:5678/webhook/skill_audit_procedures_cas2",
    3: "http://localhost:5678/webhook/skill_manuel_audit_cas3",
    5: "http://localhost:5678/webhook/skill_frap_recos_cas5",
    6: "http://localhost:5678/webhook/skill_feuilles_revision_cas6",
    7: "http://localhost:5678/webhook/skill_feuille_couverture_cas7",
    8: "http://localhost:5678/webhook/skill_programme_travail_cas8",
}
```

### Skills Existantes (Opérationnelles)

✅ **Cas 2** : Procédures d'audit  
✅ **Cas 3** : Manuels d'audit  
✅ **Cas 6** : Feuilles de révision

### Skills à Créer

⚠️ **Cas 5** : FRAP et Recommandations (webhook + script)  
⚠️ **Cas 7** : Feuilles de couverture (webhook + script)  
⚠️ **Cas 8** : Programme de travail (webhook + script)

---

## 🚀 Utilisation

### Méthode 1 : Windows (.bat)

```powershell
# Lancer l'orchestrateur
cd "h:\Projet_pdf_excel\Modelisation claude skill\Cas_10"
.\execute_cas10.bat
```

### Méthode 2 : Python Direct

```powershell
# Activer l'environnement
conda activate pdf_excel_env

# Lancer
python execute_cas10_orchestrator.py
```

### Exemple de Sortie

```
================================================================================
  CAS 10 - ROUTEUR INTELLIGENT DE SKILLS N8N
================================================================================

[2026-11-05 14:30:00] [INFO] Démarrage de l'orchestration multi-workflow

────────────────────────────────────────────────────────────────────────────────
  ÉTAPE 1 : Collecte des données
────────────────────────────────────────────────────────────────────────────────

[2026-11-05 14:30:00] [INFO] Appel du webhook source
[2026-11-05 14:30:01] [SUCCESS] ✅ Réponse reçue (Status: 200)

────────────────────────────────────────────────────────────────────────────────
  ÉTAPE 2 : Extraction et détection
────────────────────────────────────────────────────────────────────────────────

[2026-11-05 14:30:01] [INFO] Extraction des données de mission
[2026-11-05 14:30:01] [SUCCESS] ✅ Structure 'DATA_COLLECTION' détectée : 5 élément(s)
[2026-11-05 14:30:01] [SUCCESS] ✅ 5 élément(s) de mission trouvé(s)
[2026-11-05 14:30:01] [INFO] Détection des types de mission
[2026-11-05 14:30:01] [INFO]   [1] → Cas 8 (Programme de travail / Cartographie)
[2026-11-05 14:30:01] [INFO]   [2] → Cas 8 (Programme de travail / Cartographie)
[2026-11-05 14:30:01] [INFO]   [3] → Cas 6 (Feuilles de révision)
[2026-11-05 14:30:01] [INFO]   [4] → Cas 2 (Procédures d'audit)
[2026-11-05 14:30:01] [INFO]   [5] → Cas 5 (FRAP et Recommandations)

[2026-11-05 14:30:01] [SUCCESS] ✅ Détection terminée : 4 type(s) détecté(s)

────────────────────────────────────────────────────────────────────────────────
  ÉTAPE 3 : Routage vers les skills
────────────────────────────────────────────────────────────────────────────────

[2026-11-05 14:30:01] [INFO] Appel de la skill : Cas 2 - Procédures d'audit
[2026-11-05 14:30:02] [SUCCESS] ✅ Skill exécutée avec succès (Status: 200)

[2026-11-05 14:30:02] [INFO] Appel de la skill : Cas 5 - FRAP et Recommandations
[2026-11-05 14:30:03] [ERROR] ❌ Erreur de connexion - La skill N8N existe-t-elle ?

[2026-11-05 14:30:03] [INFO] Appel de la skill : Cas 6 - Feuilles de révision
[2026-11-05 14:30:04] [SUCCESS] ✅ Skill exécutée avec succès (Status: 200)

[2026-11-05 14:30:04] [INFO] Appel de la skill : Cas 8 - Programme de travail
[2026-11-05 14:30:05] [ERROR] ❌ Erreur de connexion - La skill N8N existe-t-elle ?

────────────────────────────────────────────────────────────────────────────────
  RÉSUMÉ DE L'ORCHESTRATION
────────────────────────────────────────────────────────────────────────────────

[2026-11-05 14:30:05] [INFO] Total de cas traités : 4
[2026-11-05 14:30:05] [INFO] Skills exécutées avec succès : 2
[2026-11-05 14:30:05] [INFO] Skills échouées : 2

Détail par cas :
  • Cas 2 (Procédures d'audit) : ✅ SUCCÈS - 1 item(s)
  • Cas 5 (FRAP et Recommandations) : ❌ ÉCHEC - 1 item(s)
  • Cas 6 (Feuilles de révision) : ✅ SUCCÈS - 1 item(s)
  • Cas 8 (Programme de travail / Cartographie) : ❌ ÉCHEC - 2 item(s)

[2026-11-05 14:30:05] [WARNING] ⚠️  Orchestration terminée avec des erreurs
[2026-11-05 14:30:05] [INFO]    Vérifier que toutes les skills N8N existent et sont actives
```

---

## 🗺️ Mapping des Types de Mission

Le fichier `cas10_router.py` détecte automatiquement les types selon 3 méthodes :

### Méthode 1 : Champ `Etape de mission`

| Valeur | Cas | Description |
|--------|-----|-------------|
| `Frap` | 5 | FRAP |
| `Recos contrôle des comptes` | 5 | Recommandations |
| `Feuille revision` | 6 | Feuilles de révision |
| `Feuille couverture` | 7 | Feuilles de couverture |
| `Programme de travail` | 8 | Programme de travail |
| `Cartographie des risques` | 8 | Cartographie |

### Méthode 2 : Source N8N

| Pattern dans source | Cas | Exemple |
|---------------------|-----|---------|
| `PROCEDURE` | 2 | `Etape_mission_PROCEDURE_E-audit` |
| `MANUEL` | 3 | `Etape_mission_MANUEL_E-audit` |
| `FRAP` | 5 | `Etape_mission_FRAP_E-audit` |
| `FEUILLE_REVISION` | 6 | `Etape_mission_FEUILLE_REVISION_E-audit` |
| `PROGRAMME` | 8 | `Etape_mission_PROGRAMME_E-audit` |

### Méthode 3 : Mots-clés

Recherche dans les valeurs du JSON :
- **Cas 5** : "frap", "recommandation"
- **Cas 6** : "révision", "test d'audit"
- **Cas 7** : "couverture"
- **Cas 8** : "programme", "cartographie", "matrice"

---

## 🏗️ Architecture Technique

### Fichiers Principaux

```python
# execute_cas10_orchestrator.py
# ↓ Importe
# cas10_router.py (détection intelligente)

# Flux d'exécution :
1. call_source_webhook()       → Récupère les données
2. extract_mission_data()      → Parse JSON
3. detect_and_route_missions() → Détecte types
4. call_skill_webhook()        → Route vers skills
```

### Structures de Données

#### Entrée (Webhook Source)

```json
{
  "DATA_COLLECTION": {
    "source": "Etape_mission_PROGRAMME_E-audit",
    "data": [
      {
        "Etape de mission": "Programme de travail",
        "table 1": { ... },
        "table 2": { ... }
      }
    ]
  }
}
```

#### Sortie (Vers Skill)

```json
{
  "Data_integrale": [
    {
      "Etape de mission": "Programme de travail",
      "table 1": { ... },
      "table 2": { ... }
    }
  ]
}
```

---

## 🛠️ Dépannage

### Erreur : "Webhook non configuré"

**Problème** : La skill pour ce cas n'existe pas encore

**Solution** :
1. Créer le workflow N8N pour ce cas
2. Configurer le webhook dans N8N
3. Mettre à jour `CAS_SKILLS_WEBHOOKS` si nécessaire

### Erreur : "Erreur de connexion"

**Problème** : N8N n'est pas démarré ou le webhook n'existe pas

**Solution** :
```powershell
# Vérifier N8N
curl http://localhost:5678

# Tester le webhook
curl -X POST http://localhost:5678/webhook/skill_xxx_casX
```

### Erreur : "Structure non reconnue"

**Problème** : Format JSON inattendu

**Solution** :
1. Vérifier que le webhook source retourne bien `Data_integrale` ou `DATA_COLLECTION`
2. Consulter les logs pour voir la structure reçue

### Erreur : "Type non reconnu"

**Problème** : Le routeur ne reconnaît pas le type de mission

**Solution** :
1. Ouvrir `cas10_router.py`
2. Ajouter le mapping dans `ETAPE_TO_CAS`
3. Ou ajouter des mots-clés dans `CAS_KEYWORDS`

---

## 📊 Statistiques

### Fichiers

| Fichier | Lignes | Description |
|---------|--------|-------------|
| `execute_cas10_orchestrator.py` | ~450 | Orchestrateur principal |
| `cas10_router.py` | ~400 | Détection intelligente |
| `execute_cas10.bat` | ~30 | Lanceur Windows |
| `README.md` | ~500 | Documentation |

**Total** : ~1400 lignes

### Skills Supportées

| Cas | Status | Webhook | Script |
|-----|--------|---------|--------|
| 2 | ✅ Opérationnel | ✅ | ✅ |
| 3 | ✅ Opérationnel | ✅ | ✅ |
| 5 | ⚠️ À créer | ❌ | ❌ |
| 6 | ✅ Opérationnel | ✅ | ✅ |
| 7 | ⚠️ À créer | ❌ | ❌ |
| 8 | ⚠️ À créer | ❌ | ❌ |

---

## 📞 Support

**Contact** : Whatsapp +225 05 44 13 07 98

### En cas de problème

1. Vérifier que N8N est démarré
2. Tester le webhook source manuellement
3. Consulter les logs de Cas 10
4. Vérifier que les skills cibles existent
5. Contacter le support si nécessaire

---

## 📝 Historique

| Version | Date | Modifications |
|---------|------|---------------|
| 3.0.0 | 05/11/2026 | **REFONTE MAJEURE** : Cas 10 devient routeur de skills |
| 2.0.0 | 05/11/2026 | Support DATA_COLLECTION |
| 1.0.0 | 31/10/2026 | Version initiale |

---

**Auteur** : Expert Python & Automation  
**Date** : 5 novembre 2026  
**Version** : 3.0.0
