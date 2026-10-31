---
name: audit-etap-mission-frap-recos
description: Convertit un JSON d'audit ou de révision (clés "table 1", "table 2"..., étape de mission Frap, Recos, Cartographie des risques, Feuille couverture, matrice de surveillance permanente) en document Word .docx au format du modèle "Recos contrôle des comptes - Logiciel E-révision" (A4 paysage, uniquement des tableaux, en-têtes bordeaux 8B0000, en-tête "Logiciel automatisé E-audit pro - Etape de mission", pied de page WhatsApp). À utiliser dès que l'utilisateur parle de FRAP, de recommandations d'audit, de Recos, de "Logiciel automatisé E-audit pro", d'un JSON "Etape mission - ..." à transformer en Word, de json2word, ou demande "la même modélisation" que le modèle Recos, même sans citer le skill.
---

# Audit - Etape de mission (FRAP / Recos) : JSON vers Word

Ce skill est exécuté par un agent de code **en local**. Le script `scripts/json2word_frap.py` est l'outil de référence : on l'exécute tel quel, on ne reconstruit jamais le document à la main.

## Environnement (mini conda)

```bash
conda activate pdf_excel_env      # Python 3.11, python-docx >= 1.1.0 déjà installé
python -c "import docx"           # sinon : pip install python-docx
```
`requests` n'est pas nécessaire pour ce skill.

## Contenu

- `scripts/json2word_frap.py` : convertisseur (`--help`).
- `scripts/verifier_docx.py` : contrôle automatique du .docx produit.
- `assets/exemple_frap.json` : JSON FRAP d'exemple (A210).
- `references/modele_recos.md` : anatomie exacte du modèle Word à reproduire (valeurs XML, largeurs, polices).
- `references/couverture.md` : règles « Feuille couverture » (schéma de calcul).

## Variables

| Variable | Valeur par défaut | Source |
|---|---|---|
| Étape de mission | valeur de `Etape de mission` dans la table 1 (repli : clé racine après « Etape mission - ») | JSON |
| Nom logiciel | `Logiciel automatisé E-audit pro` | `--software` |
| Valeur alphanumérique | `A210` ; si vide/non définie : générée (1-2 lettres + 2-3 chiffres, `--ref auto`) | `--ref` |
| Couleur d'en-tête | `8B0000` (rouge bordeaux du modèle) | `--color` |

## Workflow

1. **Repérer** le JSON (`.json` ou `.txt` ; le script part de la première `{`). Ne jamais modifier la source.
2. **Contrôler** : JSON valide, au moins une clé `table N`. Un JSON invalide est signalé, pas corrigé.
3. **Convertir** :
   ```bash
   python scripts/json2word_frap.py "<fichier.json>" -o "<dossier_sortie>" [--ref A210]
   ```
   Ne pas écraser un fichier existant sans accord (`--overwrite` seulement si demandé). Deux documents ne partagent jamais la même référence.
4. **Vérifier** : `python scripts/verifier_docx.py "<docx>" "<json>"` doit afficher `CONFORME`.
5. **Livrer** : nom du fichier, référence, étape, écarts éventuels.

## Règles de modélisation (invariants)

1. **Retourner le JSON dans un document Word**, aucun contenu ajouté, reformulé ni traduit.
2. **A4 paysage**, Arial 8,5 pt, marges haut 1200 / bas 1100 / côtés 900 dxa.
3. **En-tête** : `<Nom logiciel> - <Etape de mission>` (ex. `Logiciel automatisé E-audit pro - Frap`), centré, gras, bordeaux.
4. **Pied de page** : `Automatisez vos activités d'audit, risques et contrôles - Whatsapp : + 225 05 44 13 07 98`, centré, bordeaux.
5. **Uniquement des tableaux** : aucun titre entre les tables ; seul un paragraphe vide les sépare.
6. **En-têtes de tableau** : fond rouge bordeaux, texte blanc gras, ligne répétée à chaque page.
7. **Table 1 et tout dictionnaire à plusieurs clés** (ex. « Etape de mission », « Signature worksheet ») : tableau **vertical** `Rubrique | Description` (4000 | 11038 dxa), jamais horizontal. **Table 1 uniquement : la colonne 1 (les rubriques) a le même fond rouge bordeaux que les en-têtes, avec texte blanc gras.** Les autres tableaux verticaux gardent une colonne 1 sans fond.
8. **Table à clé unique** `{"Observation": "..."}` : tableau 1 colonne pleine largeur, en-tête = nom de la clé (tel quel, ex. `Recommendation`), corps = texte.
9. **Texte** : une ligne = un paragraphe ; lignes `- ` conservées en puces à retrait ; ligne vide = espace entre paragraphes.
10. **Liste d'objets** `[{...}]` : tableau en colonnes (en-têtes = clés).
11. **Nom du fichier** : `<référence>-<Etape_de_mission>- <Nom logiciel>.docx` (espaces de l'étape → `_`), ex. `A210-Frap- Logiciel automatisé E-audit pro.docx`.
12. **Feuille couverture / Couverture** : voir `references/couverture.md` (mention « Schéma de calcul : C = A + B ; Écart = C − D » retirée, tableau de schéma entre table 4 et table 5, colonnes élargies sans retour à la ligne).

## Cas particuliers

- **Clé de table inconnue** (Cartographie, matrice...) : rendu générique selon les règles 7-10, sans modification du script.
- **Caractères illisibles** (`Ã©`) : signaler l'encodage, ne pas réparer.
- **Fichier existant** : le script s'arrête et demande une autre `--ref` ou `--overwrite`.
- **Le modèle diffère du JSON** : le modèle Recos a ses propres rubriques (Intitule, Description, Ajustement...) ; seules la **mise en forme** et la **structure** sont reproduites, jamais son contenu.

## Règles impératives

Ne modifier ni les sources ni le script (sauf erreur bloquante, correction minimale annoncée) ; un échec n'arrête pas les fichiers suivants en traitement par lots ; répondre en français.
