# Rendu par format et sérialisation JSON

Le script `scripts/render_design.py` implémente ces règles (docx, xlsx, pdf). Pour un cas non couvert, adapter le script plutôt que de recoder.


Toujours préparer d'abord une structure interne unique :

```python
structure = {
  "meta": {...},                    # table d'informations (verticale)
  "design": [                       # arbre d'en-têtes
     {"label": "Cycle par sous-processus", "children": ["Cycle","Processus","Tâche clé","Opérationnel","Document"]},
     {"label": "Evaluation des risques par criticité", "children": ["Probabilité","Impact","Criticité brute"]}
  ],
  "pivot_columns": ["no"],          # colonnes hors groupe (fusion verticale)
  "rows": [ {...}, ... ]
}
```

### 6.1 Word (format par défaut, modèle par défaut)

- Librairie : `python-docx` (`from docx import Document`), activer l'environnement `pdf_excel_env`.
- Page : A4 **paysage** (`section.orientation = WD_ORIENT.LANDSCAPE`, intervertir largeur/hauteur), marges ~ 1,8 à 2 cm si beaucoup de colonnes.
- Police lisible : 9 à 10 pt pour les tables d'informations, 7 à 9 pt pour les grandes tables de données.
- En-tête de table : **fond rouge bordeaux `800020`**, texte blanc gras, centré.
- Cellules d'en-tête regroupées : `a.merge(b)` (fusion horizontale) pour le niveau 1 ; fusion verticale pour les colonnes sans parent ; marquer les deux lignes d'en-tête comme **répétées sur chaque page** (`w:tblHeader`).
- Ombrage de cellule via `lxml` : `shd = OxmlElement('w:shd'); shd.set(qn('w:val'),'clear'); shd.set(qn('w:fill'),'800020')`.
- Bordures fines grises (`808080`), marges internes de cellule (~ 50 twips haut/bas, 80 gauche/droite), alignement vertical centré.
- Niveaux de risque (si la colonne s'y prête) : fond rouge `FF0000` (Élevé), jaune `FFFF00` (Moyen), vert `00B050` (Faible), texte noir ; ajouter une légende dans une table de légende.
- Fusion verticale des valeurs répétées (Cycle, Processus, Sous-processus) quand le design le justifie.
- Éviter qu'une ligne se coupe sur deux pages (`cantSplit`).
- Enregistrer avec la codification de la section 8.

### 6.2 Word à partir d'un [Template source] (.docx / .dotx)

1. Ouvrir avec `Document(path)` (ou `docxtpl` si le modèle contient des balises Jinja2).
2. Lire styles, largeurs de colonnes, polices, en-tête/pied, orientation ; **les conserver**.
3. Insérer ou compléter les tables : ne pas modifier le reste du document.
4. Si le modèle contient déjà une cartographie, ne pas la dupliquer : ajouter seulement les en-têtes de design et les colonnes manquantes.
5. Enregistrer sous un **nouveau nom** (jamais écraser le modèle).

### 6.3 PDF

- Préférer `reportlab` (`SimpleDocTemplate` en `landscape(A4)`, `Table` avec `spans` pour fusions d'en-têtes, `repeatRows=2`, style `BACKGROUND` `#800020`, `TEXTCOLOR` blanc).
- Alternative : produire le Word (6.1) puis `docx2pdf` ; ou HTML + `weasyprint`.
- En-tête/pied de page par `onFirstPage`/`onLaterPages` (section 8).
- Contrôle visuel : rasteriser la 1re page avec `PyMuPDF` et vérifier l'absence de texte coupé.

### 6.4 Excel

- `openpyxl` : `ws.merge_cells(start_row=1,start_column=c1,end_row=1,end_column=c2)` pour le niveau 1 ; fusion verticale pour colonnes pivot ; `PatternFill('solid', fgColor='800020')`, police blanche grasse ; `wrap_text=True`, largeurs ajustées ; `ws.freeze_panes` sous les lignes d'en-tête ; `ws.auto_filter` sur la dernière ligne d'en-tête ; mise en forme conditionnelle pour Faible/Moyen/Élevé.
- Une feuille « Informations » (table verticale) puis une feuille « Données » ; autres tables (légende, cross-références) dans des feuilles séparées.
- Formules vivantes quand un calcul existe (criticité = probabilité × impact ; écart = C − D) plutôt que des valeurs figées.
- Si `[Template source]` est un `.xlsx` : `load_workbook`, reproduire styles et validations, ne jamais écraser l'original.
- En-tête / pied d'impression : `ws.oddHeader.center.text` / `ws.oddFooter.center.text`.

### 6.5 JSON

Section 7.

## 7. Sérialisation JSON ([Formatage data])

- **Type 1** (documents, pièces jointes, programme de travail, cartographie, modélisation) : **deux tables** : `table 1` = informations (étape de mission, document, normes CRIPP applicables, méthode, référence) ; `table 2` = colonnes/lignes de l'étape ou du document.
- **Type 2** (feuilles de test / couverture / révision) : **7 tables** (`table 0 - Signature worksheet` possible), conformes au format du prompt source.
- Avec modélisation design, **imbriquer chaque ligne par groupe** :

```json
{"Etape mission - Cartographie des risques":[
  {"table 1":{"Etape de mission":"Cartographie des risques","Norme":"...","Méthode":"...","Reference":"..."}},
  {"table 2":[
    {"no":1,
     "Cycle par sous-processus":{"Cycle":"...","Processus":"...","Tâche clé":"..."},
     "Evaluation des risques par criticité":{"Probabilité":"Moyen (2)","Impact":"Élevé (3)","Criticité brute":"Élevé (6)"}}
  ]}
]}
```

- Les clés des groupes = en-têtes de niveau 1 ; les clés internes = en-têtes feuilles. Aucun doublon de clé dans un groupe.
- Mentionner la liste des designs dans `table 1` (clé `Modélisation design`, avec niveaux) pour que l'agent de rendu en tienne compte.
- UTF-8, `ensure_ascii=False`, indentation 2, JSON **valide** (relire avec `json.load`).
- Si `[Contenu] = Activate` ou `[Contrainte obligatoire]` = « retourner uniquement le json » : ne produire **que** le JSON, sans commentaire.
