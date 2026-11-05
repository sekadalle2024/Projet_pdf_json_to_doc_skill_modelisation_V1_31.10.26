---
name: modelisation-design-audit
description: Active la [Modélisation design] (en-têtes horizontaux regroupés au-dessus des colonnes de base) d'une étape de mission ou d'un document d'audit, risque ou contrôle interne, et produit le livrable en Word (défaut), JSON, PDF ou Excel. À utiliser quand un user_message contient [Modélisation design], [Mode auto], [Cycle par sous processus], [Evaluation des risques par criticité], [Niveau 1/2/3], ou demande un Word/PDF/Excel de cartographie des risques, programme de travail, feuille de couverture ou FRAP.
---

# Modélisation design (en-têtes regroupés)

Ajoute des **en-têtes horizontaux (niveau 1) au-dessus des en-têtes de base (niveaux 2/3/4)** pour regrouper les colonnes qui partagent une désignation ou un attribut, puis restitue le livrable dans le format demandé. Le skill est exécuté par un **agent de code en local** dans l'environnement conda `pdf_excel_env` (Python 3.11).

## Démarrage rapide

1. `conda activate pdf_excel_env` (détails et librairies : `references/environnement-local.md`).
2. Extraire les variables du user_message (`references/variables.md`) ; une variable absente prend sa valeur par défaut, `= [Mode auto]` donne la liberté du LLM (`references/mode-auto.md`).
3. Choisir le format de sortie (section suivante), appliquer l'algorithme de design, générer le contenu (`references/generation-contenu.md`).
4. Produire le JSON interne, puis le rendre :
   `python scripts/render_design.py --json data.json --format docx,xlsx,pdf --software "<Nom logiciel>" --ref <ref> --out-dir ./out`
5. Vérifier le résultat (rouvrir le fichier, compter lignes et colonnes, contrôler en-tête, pied de page, couleur `800020`, absence de titres entre tables, rasteriser une page) et restituer le chemin du fichier avec les choix faits en `[Mode auto]`.

## Format de sortie (arbre de décision)

- `[Format sortie]` absent ou `docx` : **Word, modèle par défaut**. Si `[Template source]` est un .docx/.dotx, reproduire ses styles et l'enregistrer sous un nouveau nom (jamais écraser le modèle).
- `json` : JSON selon `[Formatage data]`, sans Word. Si `[Contenu] = Activate` ou « retourner uniquement le json » : ne renvoyer que le JSON valide.
- `pdf` : Word converti (docx2pdf) ou `reportlab` (le script gère ce cas).
- `xlsx` : classeur `openpyxl` (feuilles Informations / Données, fusions, filtres, couleurs). Si `[Template source]` est un .xlsx, le charger et reproduire son style.
- Plusieurs formats : un JSON interne unique, puis chaque format depuis ce JSON.
- `[Json source]` fourni : ne pas régénérer ; ajouter les colonnes du design, ne remplir que les cellules vides, puis convertir.
- Format inconnu ou impossible : le dire et produire le Word par défaut.

## Algorithme d'activation

1. Inventorier les designs (`[Modélisation design]` = liste ou `[Mode auto]`).
2. Définir chaque design : nom, nombre de `[Niveau]`, contenu des niveaux (exemples : `references/source-modelisation-design.md`).
3. Établir les colonnes de base : `[Modele]` fourni = le suivre ; vide = colonnes standard de l'étape.
4. Fusionner design et modèle **sans doublon** : colonne déjà dans `[Modele]` = l'utiliser et ajouter seulement l'en-tête de niveau supérieur ; colonne absente = l'ajouter, la remplir selon le contexte, l'inclure dans le regroupement.
5. Ordonner : colonnes d'un groupe **contiguës** ; `no`/`N°` en tête, hors groupe (fusion verticale).
6. Construire l'arbre d'en-têtes (colspan du parent = nombre de feuilles ; colonnes sans parent en rowspan).
7. Contrôler : aucun doublon, bornes `[Min]`/`[Max]` et `Nb de [Modélisation design]` respectées.
8. Générer les lignes (`[Nb de lignes]`), propager `[Correlation [Colonne X]]`.
9. Réinjecter la variable dans le user_message transmis à l'agent qui élabore l'étape (le design doit figurer dans la consigne de modélisation Word/Excel).
10. Rendre dans le format demandé en appliquant `references/contraintes-rendu.md`.

Format JSON attendu par le script : chaque ligne de `table 2` a des valeurs scalaires (colonnes pivot) et des objets (un groupe = en-tête de niveau 1 ; objet dans objet = 3 niveaux). Détails dans `references/rendu-formats.md`.

## Règles non négociables

- Contraintes de rendu Word : en-tête « [Nom logiciel] - [Etape de mission] », pied de page WhatsApp, **aucun titre entre les tables**, tables « Signature worksheet » et « Etape de mission » **verticales**, en-têtes **rouge bordeaux `800020`**, nom de fichier `[référence] + [Etape de mission] + [Nom logiciel]` (1-2 lettres + 2-3 chiffres, générée si vide), règles spécifiques de la feuille de couverture (schéma de calcul entre table 5 et table 4) : voir `references/contraintes-rendu.md`.
- `[Mode auto]` ne s'applique qu'aux variables qui le portent ; il ne lève aucune contrainte explicite. Ne jamais inventer d'article de loi ni de norme.
- `references/source-modelisation-design.md` reprend le contenu intégral de la `[Modélisation design]` du prompt source et fait foi en cas de doute.

## Fichiers du skill

- `references/source-modelisation-design.md` : contenu source verbatim.
- `references/variables.md` : variables d'entrée et valeurs par défaut.
- `references/mode-auto.md` : directives de liberté du LLM et catalogue de designs.
- `references/rendu-formats.md` : rendu Word/PDF/Excel/JSON.
- `references/contraintes-rendu.md` : contraintes de rendu et de nommage.
- `references/generation-contenu.md` : qualité du contenu, procédure de contrôle, cas limites.
- `references/environnement-local.md` : environnement conda et librairies.
- `references/exemple-reference.md` : exemple d'exécution attendu.
- `scripts/render_design.py` : rendu JSON vers docx/xlsx/pdf avec en-têtes regroupés.
