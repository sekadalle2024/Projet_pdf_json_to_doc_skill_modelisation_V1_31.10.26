# Environnement local (miniconda)


- Ce skill est destiné à être exécuté par un **agent de code en local**.
- Un environnement **miniconda** a été créé pour les librairies et le code : nom `pdf_excel_env`, Python 3.11.
- Activation obligatoire avant tout code : `conda activate pdf_excel_env`.
- Installation supplémentaire requise (une seule fois) : `pip install requests` (appels API N8N).
- Créer / mettre à jour l'environnement : `conda env create -f environment.yml` (complet, ~50 libs) ou `environment_core.yml` (core, ~35 libs ; exclut weasyprint, camelot, tabula, docx2pdf, statsmodels, polars, dask) ; mise à jour : `conda env update -f environment.yml --prune` ; lister : `conda list` ; désactiver : `conda deactivate`.
- Librairies utiles selon le format de sortie :
  - **Word (défaut)** : `python-docx >= 1.1.0` (principal), `docxtpl`/`python-docx-template` (templates Jinja2), `docx2pdf` (conversion, si installé), `mammoth` / `docx2txt` (relecture), `lxml` (XML bas niveau pour fusions/ombrages).
  - **PDF** : `reportlab >= 4.0.0` (génération tabulaire fine, recommandé), `fpdf2`, `weasyprint` (HTML vers PDF), `pypdf`/`PyMuPDF`/`pdfplumber` (relecture, contrôle visuel), `docx2pdf`.
  - **Excel** : `openpyxl >= 3.1.0` (cellules fusionnées, styles), `xlsxwriter >= 3.1.0` (création), `pandas` (mise en forme des lignes).
  - **JSON** : bibliothèque standard `json` (`ensure_ascii=False`, `indent=2`).
  - Contrôle : `pillow`, `PyMuPDF` (rasteriser une page pour vérification visuelle), `tqdm`.
- N'utiliser que des librairies de cet environnement. Si une librairie manque, l'indiquer et proposer l'alternative la plus proche de la liste (par exemple `reportlab` à la place de `weasyprint`).
