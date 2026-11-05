# [Mode auto] : liberté du LLM


`[Mode auto]` donne **libre cours** au LLM : il choisit, justifie en une ligne dans sa note de sortie, et reste cohérent avec `[Contenu data]`, le processus et le secteur. Directives :

### 5.1 Étendue de la liberté

- `[Modélisation design] = [Mode auto]` : choisir les designs les plus pertinents pour l'étape et le processus ; nombre = `Nb de [Modélisation design]` si fixé, sinon entre 3 et 6 (ou `[Min]`/`[Max]`).
- `Conception de [Modélisation design] = [Mode auto]` : concevoir librement les designs selon le contexte **sans se limiter aux exemples** de l'annexe A (créer des groupes inédits : par exemple « Référentiel réglementaire », « Preuve et traçabilité », « Responsabilité », « Calendrier »).
- `[Nb de lignes] = [Mode auto]` : choisir le nombre de lignes adapté (typiquement 10 à 30 pour une cartographie, 5 à 15 pour une feuille de test).
- `[Modele] = [Mode auto]` : choisir les colonnes de base les plus adaptées.
- `[Etape de mission] = [Mode auto]` : choisir l'étape la plus adaptée.
- `[Nb de colonnes] = [Mode auto]` : choisir le nombre de colonnes (respecter `[Max]`/`[Min]` si présents).
- `[Format sortie] = [Mode auto]` : Word par défaut ; JSON si l'usage est intégration logicielle ; Excel si calculs/filtrage ; PDF si diffusion figée.
- `[Demo] = [Mode auto]` : activer si le contexte est une formation ou démonstration.
- Toute autre variable `= [Mode auto]` : prendre la valeur la plus utile au lecteur final.

### 5.2 Directives de conception libre (checklist du LLM)

1. **Partir du lecteur** : qui lit le document (auditeur senior, RAI, DAI, comité d'audit, régulateur) et quelle décision doit-il prendre ? Les en-têtes de niveau 1 doivent répondre à cette question.
2. **Un groupe = une idée.** Chaque en-tête de niveau 1 regroupe 2 à 6 colonnes qui partagent une même désignation ou un même attribut (identification, évaluation, maîtrise, action, preuve, responsabilité, calendrier, référentiel).
3. **Équilibre** : 3 à 6 groupes ; éviter un groupe d'une seule colonne (sauf colonne pivot), éviter plus de 8 colonnes dans un groupe.
4. **Hiérarchie** : 2 niveaux par défaut ; 3 niveaux si l'utilisateur le demande ou si un sous-regroupement clarifie nettement (ex. Cycle > Processus > Sous-processus/tâche/document).
5. **Normes et métiers** : s'appuyer sur les rubriques d'audit usuelles (annexe A, `[Rubrique audit]`) et sur la terminologie du secteur et du pays (UMOA/OHADA, SYSCOHADA, Commission Bancaire, BCEAO, CRIPP/IFACI) quand le contenu data les mentionne.
6. **Cohérence inter-étapes** : une colonne présente dans plusieurs étapes (par exemple Risque) a le même contenu partout (`[Correlation]`).
7. **Pas d'invention de références** : ne jamais inventer un numéro d'article, de circulaire ou de norme. Utiliser uniquement ceux fournis (contenu data, user_message) ou des références générales certaines. En cas de doute, citer la norme au niveau de la circulaire ou de l'instruction sans article.
8. **Données de démonstration** : plausibles, chiffrées en FCFA si monétaires, noms de fonctions plutôt que de personnes réelles, scénarios issus du contenu data quand il existe.
9. **Transparence** : terminer l'exécution par une note courte (hors document) listant les choix faits en `[Mode auto]` (designs retenus, nombre de lignes, format).
10. **Limites de la liberté** : ne jamais violer une contrainte explicite du user_message, la section 8 (rendu), ni l'annexe A. La liberté s'exerce là où la variable vaut `[Mode auto]`, nulle part ailleurs.

### 5.3 Catalogue de designs de départ (réutilisables ou à dépasser)

- Cycle par sous-processus : Cycle > Processus > tâches, opérationnel, document.
- Cycle par opérations : Cycle > opérations financières, administratives, opérationnelles > tâches, opérationnel, document.
- Évaluation des risques par criticité : Évaluation des risques > probabilité, impact, criticité.
- Risque inhérent par impact : RISQUE INHÉRENT > Prob, Impact, Amplitude.
- Dispositif de contrôle interne par échelon : DISPOSITIF DE CONTRÔLE INTERNE > 1er échelon (auto-contrôle / contrôle hiérarchique), 2e échelon (contrôle permanent / audit interne).
- Plan d'action : Plan d'action > niveau 1, niveau 2, niveau 3 / point de contrôle, contrôle à réaliser, document.
- Risque résiduel : Risque résiduel > criticité nette, plan d'action complémentaire, échéance.
- Preuve et traçabilité : Preuve > document, référence, X-ref, date.
- Responsabilité et calendrier : Responsabilité > propriétaire, contributeurs ; Calendrier > délai, statut.
- Programme de travail : Contrôle > point de contrôle, contrôle audit, assertion ; Preuve > document, échantillon, X-ref.
- Feuille de test : Données de test > colonnes jusqu'à Écart ; Assertion ; Pointage > CTR 1..n ; Conclusion.
