# Contraintes de rendu ([Contrainte] de [Skill])


S'appliquent à tout livrable Word (et, par analogie, PDF/Excel) :

1. **Retourner le JSON dans un document Word** (quand le livrable est un Word, le contenu du JSON est entièrement restitué sous forme de tables).
2. **En-tête de page** : `[Nom logiciel] - [Etape de mission]`. Exemple : « Logiciel automatisé E-audit pro 2.0 - Cartographie des risques ».
3. **Pied de page** : « Automatisez vos activités d'audit, risques et contrôles - Whatsapp : + 225 05 44 13 07 98 ».
4. **Aucun titre entre les tables** : afficher uniquement des éléments table (pas de titres, sous-titres ni paragraphes explicatifs entre les tables). Seuls un paragraphe vide minimal d'espacement est toléré.
5. **Tables « Signature worksheet » et « Etape de mission » : orientation verticale** (libellé dans la colonne de gauche, valeur à droite, une rubrique par ligne), et non horizontale. Suivre l'exemple en pièce jointe s'il existe.
6. **Couleur de fond des en-têtes de tableau : rouge bordeaux** (`#800020`), texte blanc.
7. **Nom du fichier** : `[reference numérotation] + [Etape de mission] + [Nom logiciel]`.
   - `[reference numérotation]` = alphanumérique : **une ou deux lettres et deux ou trois chiffres** (ex. BB01, BB010, BB040). Utiliser `[Valeur alphanumerique]` ; si vide ou non défini, **générer automatiquement** une référence de son choix respectant ce format.
   - Exemples : `BB01-Leadsheet_Ventes__- Logiciel E-révision` ; `BB010 - Etat_des_ventes_Sage100_Metalux_2025- Logiciel E-révision` ; `BB040- Test de cadrage du chiffre d'affaires- Logiciel E-révision`.
   - Nettoyer les caractères interdits du système de fichiers (`\ / : * ? " < > |`) ; conserver les accents ; extension selon le format (`.docx`, `.pdf`, `.xlsx`, `.json`).
8. **Si [Etape de mission] = « Feuille couverture » ou « Couverture »**, appliquer en plus :
   - insérer une ligne (table) **entre la table « table 5 » et la table « table 4 »** ;
   - dans cette table, élaborer le **[Schéma de calcul]** ;
   - **retirer** la mention « Schéma de calcul : C = A + B ; Écart = C − D » ;
   - chaque cellule du schéma de calcul est soit **une lettre** : (A), (D), etc., soit **une composition de lettres** : (C) = (A) − (D) ;
   - pour les cellules à lettres composées, **augmenter la largeur de colonne** pour afficher le contenu **sur une seule ligne**, sans retour à la ligne ;
   - **augmenter à l'identique la largeur des colonnes liées dans la table de test** (même largeur que la colonne du schéma de calcul correspondante).
9. **Qualité de mise en page** : colonnes lisibles (pas de mot coupé en caractères isolés), largeurs adaptées au contenu, tableaux qui tiennent dans la largeur de page, en-têtes répétés sur chaque page.
