# Génération du contenu, contrôle qualité, cas limites


- **Cohérence logique** : chaque ligne relie tâche, risque, cause, évaluation, dispositif, plan d'action. Le plan d'action traite la **cause racine**.
- **Évaluation** : échelle explicite (par ex. Faible 1, Moyen 2, Élevé 3 ; criticité = probabilité × impact ; Faible 1 à 2, Moyen 3 à 4, Élevé 6 à 9). La criticité nette est toujours ≤ criticité brute après dispositif de maîtrise.
- **Couverture** : répartir les lignes sur tous les sous-processus du processus (au moins 3 à 5 par sous-processus pour 20 lignes).
- **Unicité** : aucun risque, tâche ou plan d'action en doublon.
- **Contexte** : reprendre les faits, entités, montants, normes du `[Contenu data]` ; ne pas inventer de références réglementaires (section 5.2.7).
- **Feuilles de test (`[Demo] = Activate`)** : remplir toutes les cellules de [Tableau de test] ; définir Assertion (Validité, Exhaustivité, Comptabilisation, Séparation des exercices, Évaluation), Pointage (`+`, `-`, N/A), Conclusion (Satisfaisant, Non-satisfaisant, Limitation, Non applicable) ; produire le tableau explicatif d'une colonne qui justifie, pour chaque ligne, le lien entre données, assertion, pointage et conclusion.
- **Calculs** : A, B, C, D numériques ; B taux ; C = A × B ; Écart = C − D (voir [Estimation]) ; vérifier par code (`pandas`) avant rendu.

## 10. Procédure d'exécution et contrôle qualité

1. `conda activate pdf_excel_env` ; vérifier les imports nécessaires.
2. Lire le user_message, extraire les variables (tableau section 2), noter les valeurs par défaut utilisées.
3. Appliquer la section 3 (format) puis la section 4 (design).
4. Générer la structure interne ; valider le schéma (aucun doublon, colspan cohérents, bornes respectées).
5. Rendre dans le(s) format(s) ; sauvegarder avec la codification (section 8.7).
6. **Vérifier** : (a) rouvrir le fichier (`python-docx`, `openpyxl`, `pdfplumber`, `json.load`) ; (b) compter lignes et colonnes ; (c) vérifier l'en-tête, le pied de page, la couleur `800020`, l'absence de titres entre tables, l'orientation verticale des tables d'informations ; (d) pour PDF/Word, rasteriser une page et contrôler visuellement.
7. **Restituer** : chemin du fichier, format, liste courte des choix `[Mode auto]` et des valeurs par défaut utilisées. Si `[Contrainte obligatoire]` impose « uniquement le json », ne renvoyer que le JSON.

## 11. Cas limites

- Design défini sans `[Modele]` : prendre le modèle standard de l'étape, ajouter les colonnes du design.
- Colonne du design déjà présente avec un autre libellé : la rapprocher (synonyme) au lieu de la dupliquer ; conserver le libellé de `[Modele]`.
- Conflit entre `[Max]` de colonnes et colonnes du design : réduire d'abord les colonnes facultatives hors design, puis signaler la limite.
- `[Json source]` invalide : indiquer la ligne en erreur et ne rien produire de partiel.
- Trop de colonnes pour la page : réduire la police (minimum 7 pt), répartir sur 2 tables sans titres intermédiaires, ou proposer A3 / Excel.
- Template inaccessible ou format non pris en charge : indiquer précisément la cause et basculer vers le modèle Word par défaut.
- Plusieurs étapes dans un seul user_message : traiter chacune séparément avec sa référence ; appliquer `[Correlation]`.
