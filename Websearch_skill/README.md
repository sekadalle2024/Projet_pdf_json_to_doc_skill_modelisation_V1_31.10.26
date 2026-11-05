# Websearch Skill - Collecteur d'Offres d'Emploi

## Description

Ce dossier contient le skill **Job Search Collector** pour rechercher et collecter des offres de recrutement sur le web.

## Contenu

- `job-search-collector.md` : Le skill principal avec toutes les stratégies de recherche
- `test_recherche_audit.md` : Résultat du test de recherche
- `resultats/` : Dossier pour stocker les rapports de recherche

## Utilisation

Le skill permet de rechercher des offres d'emploi selon :
- **Fonction** : Poste recherché (ex: Directeur Audit Interne)
- **Nombre** : Quantité d'offres à collecter (ex: 50)
- **Zone géographique** : Pays ou région (ex: Côte d'Ivoire, Afrique de l'Ouest)
- **Période** : Dernières années (1 à 5 ans)

## Exemple de Commande

```
Trouve 50 offres pour des directeurs audit interne en Côte d'Ivoire et Afrique de l'Ouest
```

## Test en Cours

Exécution d'une recherche test avec les paramètres suivants :
- Fonction : Directeur Audit Interne
- Nombre cible : 50 offres
- Zone : Côte d'Ivoire + Afrique de l'Ouest
- Période : 5 dernières années (2020-2024)
