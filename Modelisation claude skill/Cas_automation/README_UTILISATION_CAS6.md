# Guide d'utilisation - Cas 6 : Feuille de révision

## Vue d'ensemble

Le Cas 6 génère automatiquement des **Feuilles de révision d'audit** au format Word à partir de données JSON structurées.

Le document généré contient **9 tables complètes** avec toutes les informations d'audit:
- Signature worksheet
- Informations de mission
- Objectifs
- Travaux à effectuer
- Résultats des tests
- **Données détaillées d'audit** (15 comptes avec 18 colonnes)
- Références croisées documentaires
- Légendes
- Revue du manager

## Utilisation via API (Serveur Flask)

### 1. Démarrer le serveur

```bash
# Méthode 1: Via le script batch
start_server.bat

# Méthode 2: Ligne de commande
conda activate pdf_excel_env
python server_automation.py
```

Le serveur démarre sur: `http://localhost:5000`

### 2. Appel API

#### Avec des données JSON personnalisées
```bash
curl -X POST http://localhost:5000/automation/cas_6 \
  -H "Content-Type: application/json" \
  -d @mes_donnees.json
```

#### Avec les données de test standard
```bash
curl -X GET http://localhost:5000/automation/test/6
```

### 3. Réponse

Le serveur renvoie:
- **Content-Type**: `application/vnd.openxmlformats-officedocument.wordprocessingml.document`
- **Fichier**: Document Word (.docx)
- **Emplacement**: Téléchargé automatiquement dans le dossier **Downloads** de Windows

Nom du fichier: `Cas6_YYYYMMDD_HHMMSS.docx`

## Utilisation en ligne de commande

### Script standalone

```bash
conda activate pdf_excel_env

python "h:\Projet_pdf_excel\Modelisation claude skill\Cas_6\json2word_feuilles_revision_v3.py" \
  "chemin/vers/donnees.json" \
  -o "C:\Users\LEADER\Downloads"
```

### Options disponibles

| Option | Description | Requis | Exemple |
|--------|-------------|--------|---------|
| `json_file` | Fichier JSON d'entrée | ✅ | `donnees.json` |
| `-o, --out-dir` | Dossier de sortie | ❌ | `-o ./output` |

### Exemple complet

```bash
# Activer l'environnement
conda activate pdf_excel_env

# Générer le document
python json2word_feuilles_revision_v3.py "audit_data.json" -o "C:\Users\LEADER\Downloads"

# Résultat
[OK] Document genere : C:\Users\LEADER\Downloads\Cas6_20261107_194204.docx
```

## Format JSON attendu

### Structure globale

```json
{
  "Etape mission - Feuille revision": [
    { "table 0 - Signature worksheet": [...] },
    { "table 1": [...] },
    { "table 2": [...] },
    { "table 3": [...] },
    { "table 4": [...] },
    { "table 5": [...] },
    { "table 6 - Cross references documentaire": [...] },
    { "table 7 - Legendes": [...] },
    { "table 8 - Revue manager": [...] }
  ]
}
```

### Tables verticales (dictionnaire)

Tables 0, 1, 2, 4 : Format clé/valeur

```json
{
  "table 0 - Signature worksheet": [
    {
      "Client": "Afrika Financial Bank",
      "Exercice": "2024",
      "Preparer": "Y.K. / Contrôleur Junior",
      "Reviewer": "D.A.I. / Chef de Mission"
    }
  ]
}
```

**Résultat dans Word**: Table 2 colonnes (Clé | Valeur)

| Clé | Valeur |
|-----|--------|
| Client | Afrika Financial Bank |
| Exercice | 2024 |
| ... | ... |

### Tables horizontales (liste)

Tables 3, 5, 6, 7, 8 : Format colonnes

```json
{
  "table 5": [
    {
      "N° Ordre": "1",
      "N° Compte Client": "CPT-DOR-04412",
      "Date Réactivation": "14/05/2024",
      "Intitulé Compte": "SOC. IVOIRIENNE LIQUIDATION",
      "Solde Veille Réactivation": "34 000 000",
      "Visa Agence (Maker)": "Oui",
      "Visa Conformité Siège (Checker)": "Non",
      "..."
    },
    { "N° Ordre": "2", "..." }
  ]
}
```

**Résultat dans Word**: Table avec en-têtes colonnes

| N° Ordre | N° Compte Client | Date Réactivation | ... |
|----------|------------------|-------------------|-----|
| 1 | CPT-DOR-04412 | 14/05/2024 | ... |
| 2 | CPT-DOR-01205 | 18/01/2024 | ... |

## Contenu du document généré

### Structure complète

```
📄 Document Word: Cas6_YYYYMMDD_HHMMSS.docx
├── 📋 Titre: "table 0 - Signature worksheet"
├── 📊 Table 1: Informations signature (2x4)
│
├── 📋 Titre: "table 1"
├── 📊 Table 2: Informations mission (2x4)
│
├── 📋 Titre: "table 2"
├── 📊 Table 3: Objectifs (2x1)
│
├── 📋 Titre: "table 3"
├── 📊 Table 4: Travaux à effectuer (6x2)
│
├── 📋 Titre: "table 4"
├── 📊 Table 5: Résultats des tests (2x1)
│
├── 📋 Titre: "table 5"
├── 📊 Table 6: Données d'audit (16x18) ⭐ TABLE PRINCIPALE
│
├── 📋 Titre: "table 6 - Cross references documentaire"
├── 📊 Table 7: Références documentaires (5x5)
│
├── 📋 Titre: "table 7 - Legendes"
├── 📊 Table 8: Légendes (4x2)
│
├── 📋 Titre: "table 8 - Revue manager"
└── 📊 Table 9: Revue du manager (4x3)
```

### Table principale (table 5) - 18 colonnes

Les colonnes de la table d'audit détaillée:

1. N° Ordre
2. N° Compte Client
3. Date Réactivation
4. Intitulé Compte
5. Solde Veille Réactivation
6. Visa Agence (Maker)
7. Visa Conformité Siège (Checker)
8. Contact Liquidateur Conforme
9. Montant Débit Réalisé
10. Ecart
11. Assertion
12. CTR 1
13. CTR 2
14. CTR 3
15. CTR 4
16. CTR 5
17. Description
18. Conclusion

## Charte graphique

Le document respecte la charte **E-audit pro**:

### Couleurs
- **Bordeaux (#7B1E3A)**: En-têtes de tables, titres
- **Fond clair (#F2E6EA)**: Colonne des clés dans tables verticales
- **Gris (#999999)**: Bordures
- **Blanc (#FFFFFF)**: Texte des en-têtes

### Typographie
- **Police**: Calibri
- **Taille**: 9 pt
- **En-têtes**: Gras + Blanc + Centré

### Mise en page
- **Format**: A4 Portrait
- **Marges**: 0.5 pouces
- **Largeur tables**: Ajustée automatiquement au contenu

## Dépannage

### Problème: "Fichier JSON non trouvé"

**Cause**: Chemin incorrect ou fichier manquant

**Solution**:
```bash
# Vérifier le chemin absolu
ls "h:\Projet_pdf_excel\Modelisation claude skill\Cas_automation\json standard\Json_standard_[Cas 6].txt"

# Utiliser des chemins absolus
python json2word_feuilles_revision_v3.py "h:\chemin\complet\vers\fichier.json" -o "C:\output"
```

### Problème: "Serveur inaccessible"

**Cause**: Serveur non démarré ou port 5000 occupé

**Solution**:
```bash
# Vérifier si le serveur tourne
curl http://localhost:5000/health

# Redémarrer le serveur
conda activate pdf_excel_env
python server_automation.py
```

### Problème: "Document vide ou incomplet"

**Cause**: JSON mal formaté ou version ancienne du script

**Solution**:
1. Vérifier que vous utilisez **v3** du script: `json2word_feuilles_revision_v3.py`
2. Valider le JSON avec un validateur en ligne
3. Vérifier la structure: clé racine `"Etape mission - Feuille revision"` doit exister
4. Tester avec le JSON standard fourni

### Problème: "Encodage caractères spéciaux"

**Cause**: Encodage Windows vs UTF-8

**Solution**: Le script v3 gère automatiquement l'encodage Windows (pas d'emojis)

## Intégration N8N

### Workflow type

```
1. [Webhook/API] → Récupération données
2. [Function Node] → Formatage JSON selon structure attendue
3. [HTTP Request Node] → POST http://localhost:5000/automation/cas_6
   - Method: POST
   - Body Content Type: JSON
   - Body: {{ $json }}
4. [Move Binary Data] → Conversion réponse en fichier
5. [Write Binary File] / [Email] → Sauvegarde ou envoi
```

### Configuration HTTP Request Node

```json
{
  "method": "POST",
  "url": "http://localhost:5000/automation/cas_6",
  "headers": {
    "Content-Type": "application/json"
  },
  "bodyContentType": "json",
  "body": "={{ $json }}",
  "responseFormat": "file"
}
```

## Support et contact

Pour toute question ou problème:

1. Consulter les logs du serveur: `server_automation.py` affiche les erreurs détaillées
2. Tester avec le JSON standard: `Json_standard_[Cas 6].txt`
3. Vérifier la documentation: `SOLUTION_CAS6_V3.md`

---

**Version**: 3.0  
**Dernière mise à jour**: 7 novembre 2026  
**Statut**: ✅ Validé et opérationnel
