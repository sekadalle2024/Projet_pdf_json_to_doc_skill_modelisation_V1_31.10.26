# 🚀 Guide de Démarrage Rapide - Cas 12

> **Convertissez vos données de cartographie des risques JSON en documents Word professionnels en 3 étapes**

---

## ⚡ Démarrage en 3 Étapes

### Étape 1 : Installation (1 minute)

```bash
# Installer python-docx
pip install python-docx
```

### Étape 2 : Placer vos Données (30 secondes)

Créez un fichier JSON nommé `exemple_*.json` dans le dossier `Cas_12/` :

```json
{
  "Cartographie des risques - Processus opérationnels": [
    {
      "table 1": {
        "Etablissement": "Votre Entreprise",
        "Reference": "CARTO-2026-Q4"
      }
    },
    {
      "table 2": [
        {
          "Processus": "Trésorerie",
          "Risque identifié": "Défaut de réconciliation",
          "Risque inhérent": "12 - Élevé",
          "Risque résiduel": "8 - Moyen"
        }
      ]
    }
  ]
}
```

### Étape 3 : Lancer la Conversion (10 secondes)

```bash
cd "h:\Projet_pdf_excel\Modelisation claude skill\Cas_12"
python json2word_cartographie_risques.py
```

**Résultat** : Vos documents Word sont générés dans `output_word/` ! 🎉

---

## 📊 Exemples Fournis

Le dossier contient déjà 2 exemples prêts à l'emploi :

1. **exemple_cartographie_minimal.json** - 1 risque simple
2. **exemple_cartographie_complet.json** - 7 risques variés

Lancez simplement le script pour les tester !

---

## 🎨 Ce Que Vous Obtenez

✅ Document Word professionnel avec :
- En-tête avec métadonnées complètes
- Tableau de 20 colonnes formaté
- Heat map colorée par niveau de risque :
  - 🟥 Rouge : Risque élevé/critique
  - 🟧 Orange : Risque moyen
  - 🟩 Vert : Risque faible
- Pied de page avec date de génération

---

## 📚 Documentation Complète

- **README.md** - Guide utilisateur détaillé
- **IMPLEMENTATION_CAS_12.md** - Documentation technique
- **RECAPITULATIF_CAS_12.md** - Vue d'ensemble du projet

---

## 🆘 Besoin d'Aide ?

### Erreur : Module python-docx non trouvé

```bash
pip install python-docx
```

### Erreur : Aucun fichier JSON trouvé

Vérifiez que vos fichiers JSON :
- Sont nommés `exemple_*.json`
- Sont dans le dossier `Cas_12/`

### Fichier JSON invalide

Validez votre JSON sur : https://jsonlint.com/

---

## 🎯 Prochaine Étape

Maintenant que vous maîtrisez les bases, consultez le **README.md** pour :
- Comprendre la structure des 20 colonnes
- Personnaliser les couleurs et le formatage
- Intégrer avec N8N (webhook)
- Respecter les référentiels ISO 31000 et COSO ERM

---

**Bon courage ! 🚀**

*Afrika Group Holdings - Département Audit & Contrôle Interne*
