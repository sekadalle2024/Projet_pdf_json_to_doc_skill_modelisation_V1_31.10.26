# Étape « Feuille couverture » / « Couverture »

Déclenchement : l'étape de mission contient « couverture » (insensible à la casse).

1. Retirer la mention `Schéma de calcul : C = A + B ; Écart = C − D` de tous les textes.
2. Insérer un tableau de schéma de calcul entre la table 4 et la table 5. Le JSON doit fournir une clé « Schéma de calcul » (liste d'objets ou dictionnaire) ; sinon le script le signale et n'invente rien.
3. Chaque cellule du schéma est soit une lettre `(A)`, `(D)`, soit une composition `(C) = (A) - (D)`.
4. Cellules composées : largeur de colonne augmentée (≈ 115 dxa par caractère + 260) pour tenir sur UNE seule ligne.
5. Les colonnes liées du tableau de test doivent recevoir la même largeur : à faire sur le tableau concerné lorsqu'il est en colonnes (même fonction `schema_widths`). Point à valider avec un vrai JSON de couverture.
