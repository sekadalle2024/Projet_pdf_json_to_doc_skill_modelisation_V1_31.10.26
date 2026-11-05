# Job Search Collector Skill

## Métadonnées
- **Nom**: Job Search Collector
- **Version**: 1.0.0
- **Domaine**: Recherche d'emploi et recrutement
- **Langues**: Français, Anglais

## Objectif
Rechercher et collecter des offres de recrutement pour une fonction spécifique dans une zone géographique donnée, sur une période définie (jusqu'à 5 ans). Le skill structure les résultats et génère un rapport consolidé.

## Capacités

### 1. Recherche Multi-Sources
- Sites d'emploi internationaux (LinkedIn, Indeed, Glassdoor)
- Sites africains spécialisés (Emploi.ci, Jumia Jobs, BrighterMonday)
- Sites institutionnels (banques, organisations internationales)
- Sites d'entreprises directement
- Agrégateurs d'offres d'emploi

### 2. Filtres de Recherche
- **Fonction/Poste**: Titre exact ou mots-clés (ex: "Directeur Audit Interne")
- **Nombre cible**: Quantité d'offres à collecter
- **Zone géographique**: Pays ou région (ex: Côte d'Ivoire, Afrique de l'Ouest)
- **Période**: Dernières années (1 à 5 ans)
- **Secteur**: Banque, Finance, Industrie, etc. (optionnel)

### 3. Extraction de Données
Pour chaque offre collectée:
- Titre du poste
- Entreprise/Organisation
- Localisation précise
- Date de publication
- Description du poste
- Compétences requises
- Niveau d'expérience
- Type de contrat
- Fourchette salariale (si disponible)
- Source/URL

## Processus de Recherche

### Phase 1: Préparation
1. Analyser la requête utilisateur
2. Identifier les mots-clés en français et anglais
3. Définir les variantes du poste (ex: "Directeur Audit" = "Head of Internal Audit", "Chief Audit Officer")
4. Lister les pays de la zone géographique

### Phase 2: Recherche Itérative
Pour atteindre le nombre cible d'offres:

1. **Recherche par mots-clés principaux**
   ```
   Requête type: "[Fonction] [Pays] job offer [Année]"
   Exemple: "Directeur Audit Interne Côte d'Ivoire offre emploi 2024"
   ```

2. **Recherche par variantes linguistiques**
   ```
   - Version française: "Directeur Audit Interne Abidjan"
   - Version anglaise: "Internal Audit Director Ivory Coast"
   ```

3. **Recherche par secteur**
   ```
   "[Fonction] banque [Pays]"
   "[Fonction] finance [Pays]"
   ```

4. **Recherche par année**
   - Commencer par l'année en cours
   - Remonter progressivement (2024, 2023, 2022...)
   - S'arrêter à 5 ans maximum

5. **Recherche élargie géographiquement**
   Si zone = "Afrique de l'Ouest", rechercher par pays:
   - Côte d'Ivoire, Sénégal, Mali, Burkina Faso
   - Bénin, Togo, Niger, Guinée
   - Ghana, Nigeria (si pertinent)

### Phase 3: Validation et Déduplication
- Vérifier la pertinence de chaque offre
- Éliminer les doublons (même offre sur plusieurs sites)
- Valider que l'offre correspond aux critères
- S'assurer de la fraîcheur des données

### Phase 4: Structuration
Organiser les offres par:
- Pays
- Année de publication
- Entreprise
- Type de contrat

## Stratégies de Recherche Avancées

### A. Requêtes Optimisées

**Pour maximiser les résultats:**
```
1. "[Fonction exacte] + [Ville principale] + emploi"
2. "[Fonction] + [Pays] + recrutement + [Année]"
3. "[Fonction anglaise] + [Pays anglais] + vacancy"
4. "offre d'emploi [Fonction] [Région]"
5. "[Entreprise type] recrute [Fonction] [Pays]"
```

**Exemples concrets pour Directeur Audit:**
- "Directeur Audit Interne Abidjan offre 2024"
- "Head of Internal Audit Ivory Coast job"
- "Chief Audit Officer West Africa vacancy"
- "Banque recrute Directeur Audit Côte d'Ivoire"
- "Directeur Contrôle Interne Dakar emploi"

### B. Sites Prioritaires par Région

**Côte d'Ivoire:**
- emploi.ci
- jobinivoire.net
- abidjan.net (rubrique emploi)
- LinkedIn (filtré Côte d'Ivoire)

**Sénégal:**
- emploisenegal.com
- senegal-emploi.com
- expat-dakar.com

**Afrique de l'Ouest (général):**
- afrimalin.com
- jobartis.com
- emploiafrique.com

**International (filtré Afrique):**
- LinkedIn Jobs
- Indeed Africa
- Glassdoor
- ReliefWeb (ONG)

### C. Recherche par Type d'Organisation

**Secteur Bancaire:**
```
"[Fonction] + [Banque régionale connue]"
Exemples: "Directeur Audit Ecobank", "Audit Director UBA"
Banques cibles: Ecobank, UBA, BOA, Société Générale, BNP Paribas
```

**Organisations Internationales:**
```
"[Fonction] + [Organisation] + [Région]"
Exemples: "Internal Audit World Bank West Africa"
Organisations: Banque Mondiale, BAD, FMI, UN, UNICEF
```

**Cabinets d'Audit:**
```
"[Fonction] + [Cabinet] + [Pays]"
Exemples: "Audit Manager Deloitte Abidjan"
Cabinets: Big 4 (Deloitte, PwC, EY, KPMG), cabinets locaux
```

## Format de Sortie

### Rapport Markdown Structuré

```markdown
# Rapport de Recherche: [Fonction] - [Zone Géographique]

**Date de recherche**: [Date]
**Période couverte**: [Années]
**Nombre d'offres collectées**: X / [Nombre cible]

---

## Résumé Exécutif

- Offres trouvées: X
- Pays couverts: [Liste]
- Secteurs représentés: [Liste]
- Période la plus active: [Année]

---

## Offres par Pays

### [Pays 1] (X offres)

#### Offre 1: [Titre Complet]
- **Entreprise**: [Nom]
- **Localisation**: [Ville, Pays]
- **Date de publication**: [Date]
- **Source**: [URL ou site]
- **Type de contrat**: [CDI/CDD/Consultant]
- **Expérience requise**: [Années]

**Description**:
[Résumé de l'offre]

**Compétences clés**:
- Compétence 1
- Compétence 2
- Compétence 3

**Profil recherché**:
[Résumé du profil]

---

[Répéter pour chaque offre]

---

## Analyse des Tendances

### Compétences les Plus Demandées
1. [Compétence] - X mentions
2. [Compétence] - X mentions
3. [Compétence] - X mentions

### Secteurs les Plus Actifs
1. [Secteur] - X offres
2. [Secteur] - X offres

### Évolution Temporelle
- 2024: X offres
- 2023: X offres
- 2022: X offres

---

## Annexes

### Sources Consultées
- [Liste des sites et requêtes utilisées]

### Notes Méthodologiques
- [Limitations, défis rencontrés, ajustements effectués]
```

## Instructions d'Exécution

Quand l'utilisateur demande une recherche d'offres:

1. **Clarifier les paramètres**:
   - Fonction exacte
   - Nombre cible d'offres
   - Zone géographique précise
   - Période (par défaut: 2 dernières années)
   - Secteurs prioritaires (optionnel)

2. **Planifier la recherche**:
   - Calculer le nombre de recherches nécessaires
   - Prioriser les requêtes (fonction + ville principale d'abord)
   - Prévoir recherche en français ET anglais

3. **Exécuter les recherches web**:
   - Lancer 5-10 recherches par itération
   - Analyser les résultats
   - Extraire les informations pertinentes
   - Continuer jusqu'à atteindre le nombre cible

4. **Structurer les résultats**:
   - Créer le fichier markdown
   - Organiser par pays et date
   - Ajouter l'analyse des tendances

5. **Livrer**:
   - Fichier markdown complet
   - Résumé des statistiques
   - Recommandations si pertinent

## Gestion des Cas Limites

### Si moins d'offres que demandé:
- Élargir la zone géographique
- Étendre la période (au-delà de 2 ans)
- Inclure des postes similaires/adjacents
- Documenter les ajustements effectués

### Si beaucoup trop d'offres:
- Prioriser les plus récentes
- Filtrer par pertinence (entreprises connues)
- Se concentrer sur les offres complètes

### Si offres anciennes (>3 ans):
- Indiquer clairement l'ancienneté
- Préciser que les offres peuvent être clôturées
- Valeur: analyse des tendances historiques

## Exemples de Requêtes

### Exemple 1: Directeur Audit Interne
```
Fonction: Directeur Audit Interne
Nombre: 50
Zone: Côte d'Ivoire + Afrique de l'Ouest
Période: 5 ans

Recherches à lancer:
1. "Directeur Audit Interne Côte d'Ivoire offre 2024"
2. "Internal Audit Director Ivory Coast job 2024"
3. "Directeur Audit Interne Abidjan emploi"
4. "Head of Internal Audit West Africa vacancy"
5. "Directeur Contrôle Interne banque Abidjan"
6. "Directeur Audit Interne Sénégal 2023"
7. "Internal Audit Manager Mali job offer"
8. "Chief Audit Officer Ecobank West Africa"
9. "Responsable Audit Interne Burkina Faso"
10. "Directeur Audit Interne groupe bancaire Afrique"
```

### Exemple 2: Data Scientist
```
Fonction: Data Scientist
Nombre: 30
Zone: Sénégal
Période: 3 ans

Recherches à lancer:
1. "Data Scientist Dakar emploi 2024"
2. "Data Scientist Senegal job offer 2024"
3. "Analyste de données Sénégal recrutement"
4. "Machine Learning Engineer Dakar"
5. "Data Scientist fintech Sénégal"
6. "Data Analyst Senegal 2023 vacancy"
```

## Optimisations

### Utiliser les opérateurs de recherche:
- `site:linkedin.com "Directeur Audit" "Côte d'Ivoire"`
- `"offre d'emploi" AND "audit interne" AND (Abidjan OR "Côte d'Ivoire")`
- `intitle:"audit director" "west africa" 2024..2025`

### Recherches complémentaires:
- Articles sur le recrutement dans le secteur
- Annuaires d'entreprises qui recrutent
- Rapports de marché de l'emploi

## Notes Techniques

- **Limite API web_search**: ~200 caractères par requête
- **Stratégie**: Préférer 10 recherches ciblées à 2 génériques
- **Déduplication**: Comparer titres + entreprises
- **Citation sources**: Toujours inclure l'URL ou la source
- **Compliance**: Respecter robots.txt et termes d'utilisation

## Métriques de Succès

Une recherche réussie doit:
- ✅ Atteindre ≥80% du nombre cible d'offres
- ✅ Couvrir ≥70% de la zone géographique demandée
- ✅ Inclure des offres de ≥2 années différentes
- ✅ Fournir des informations complètes (titre, entreprise, lieu, date)
- ✅ Éliminer les doublons
- ✅ Générer un rapport structuré et exploitable

---

**Activation**: Ce skill s'active automatiquement quand l'utilisateur demande de rechercher, trouver, ou collecter des offres d'emploi avec des critères spécifiques (fonction, nombre, localisation).
