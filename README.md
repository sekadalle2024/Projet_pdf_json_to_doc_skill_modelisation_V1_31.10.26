# 🚀 Projet PDF-Excel-Word Manipulation

Environnement Python professionnel pour la manipulation avancée de fichiers PDF, Excel et Word.

## 📋 Objectifs du Projet

1. ✂️ **Découper les pages de PDF**
2. 📑 **Consolider plusieurs PDF**
3. 📊 **Excel → Tableau PDF** (extraction et conversion)
4. 📝 **Excel → Tableau Word** (extraction et intégration)
5. 📄 **Word → Excel** (extraction de tableaux)
6. 🎨 **Mise en page Excel avancée** (cellules fusionnées, tables stylées)

---

## 🛠️ Installation

### Prérequis

- **Miniconda** ou **Anaconda** installé
- Windows PowerShell (ou Terminal)

Si Miniconda n'est pas installé, téléchargez-le depuis:
- [Miniconda officiel](https://docs.conda.io/en/latest/miniconda.html)

### Installation automatique

Exécutez le script PowerShell:

```powershell
.\setup_environment.ps1
```

### Installation manuelle

```powershell
# Créer l'environnement à partir du fichier YAML
conda env create -f environment.yml

# Activer l'environnement
conda activate pdf_excel_env

# Vérifier l'installation
python --version
pip list
```

### Installation avec requirements.txt (alternative)

```powershell
# Créer un environnement conda basique
conda create -n pdf_excel_env python=3.11 -y

# Activer l'environnement
conda activate pdf_excel_env

# Installer les dépendances
pip install -r requirements.txt
```

---

## 📦 Librairies Installées

### 📄 Manipulation PDF

| Librairie | Usage principal |
|-----------|----------------|
| **pypdf** | Découpage, fusion, rotation de pages PDF |
| **PyMuPDF (fitz)** | Extraction rapide de texte et tableaux, très performant |
| **pikepdf** | Réparation et optimisation de PDF complexes |
| **pdfplumber** | Extraction précise de tableaux depuis PDF |
| **reportlab** | Génération de PDF avec tableaux stylés |
| **fpdf2** | Création légère de PDF |
| **weasyprint** | Conversion HTML/CSS vers PDF |
| **camelot-py** | Extraction avancée de tableaux PDF |
| **tabula-py** | Extraction de tableaux PDF (backend Java) |

### 📊 Manipulation Excel

| Librairie | Usage principal |
|-----------|----------------|
| **pandas** | Lecture/écriture Excel, manipulation de données |
| **openpyxl** | Lecture/écriture .xlsx avec formules et styles |
| **xlsxwriter** | Création Excel avancée (graphiques, formatage) |
| **xlwings** | Automatisation Excel bidirectionnelle |
| **formulas** | Évaluation de formules Excel en Python |
| **xlrd/xlwt** | Support fichiers .xls anciens |
| **pyexcel** | Interface unifiée multi-formats |

### 📝 Manipulation Word

| Librairie | Usage principal |
|-----------|----------------|
| **python-docx** | Création et modification de documents .docx |
| **docxtpl** | Templates Word avec syntaxe Jinja2 |
| **mammoth** | Conversion Word vers HTML |
| **docx2pdf** | Conversion Word vers PDF |
| **docx2txt** | Extraction de texte depuis Word |
| **textract** | Extraction multi-formats |

### 📈 Analyse de Données

| Librairie | Usage principal |
|-----------|----------------|
| **pandas** | DataFrames, manipulation de données |
| **numpy** | Calculs numériques, algèbre linéaire |
| **matplotlib** | Visualisations graphiques |
| **seaborn** | Visualisations statistiques |
| **plotly** | Graphiques interactifs |
| **scipy** | Calculs scientifiques avancés |
| **scikit-learn** | Machine Learning |
| **polars** | Alternative rapide à Pandas |
| **dask** | Traitement de gros volumes de données |

### 🗂️ Système de Fichiers

- **pathlib** (standard) - Manipulation moderne de chemins
- **watchdog** - Surveillance de fichiers en temps réel
- **send2trash** - Suppression sécurisée vers la corbeille
- **filetype** - Détection de type MIME

---

## 🎯 Exemples d'Utilisation

### 1. Découper un PDF

```python
from pypdf import PdfReader, PdfWriter

# Lire le PDF
reader = PdfReader("document.pdf")

# Extraire les pages 1 à 5
writer = PdfWriter()
for page_num in range(0, 5):
    writer.add_page(reader.pages[page_num])

# Sauvegarder
with open("extrait.pdf", "wb") as output_file:
    writer.write(output_file)
```

### 2. Consolider plusieurs PDF

```python
from pypdf import PdfWriter

# Fusionner plusieurs PDF
writer = PdfWriter()
for pdf_file in ["doc1.pdf", "doc2.pdf", "doc3.pdf"]:
    writer.append(pdf_file)

writer.write("consolidé.pdf")
```

### 3. Excel → Tableau PDF (avec ReportLab)

```python
import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors

# Lire Excel
df = pd.read_excel("data.xlsx")

# Créer PDF
pdf = SimpleDocTemplate("rapport.pdf", pagesize=A4)
data = [df.columns.tolist()] + df.values.tolist()

# Créer tableau stylé
table = Table(data)
table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 14),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
    ('GRID', (0, 0), (-1, -1), 1, colors.black)
]))

pdf.build([table])
```

### 4. Excel → Word (avec python-docx)

```python
import pandas as pd
from docx import Document

# Lire Excel
df = pd.read_excel("data.xlsx")

# Créer document Word
doc = Document()
doc.add_heading('Rapport de Données', 0)

# Ajouter tableau
table = doc.add_table(rows=1, cols=len(df.columns))
table.style = 'Light Grid Accent 1'

# Headers
hdr_cells = table.rows[0].cells
for i, col in enumerate(df.columns):
    hdr_cells[i].text = str(col)

# Données
for _, row in df.iterrows():
    row_cells = table.add_row().cells
    for i, value in enumerate(row):
        row_cells[i].text = str(value)

doc.save("rapport.docx")
```

### 5. Word → Excel (extraction de tableaux)

```python
from docx import Document
import pandas as pd

# Lire document Word
doc = Document("document.docx")

# Extraire le premier tableau
table = doc.tables[0]
data = []

for row in table.rows:
    data.append([cell.text for cell in row.cells])

# Convertir en DataFrame
df = pd.DataFrame(data[1:], columns=data[0])

# Sauvegarder en Excel
df.to_excel("extrait.xlsx", index=False)
```

### 6. Mise en page Excel avancée

```python
import pandas as pd
import xlsxwriter

# Créer workbook
workbook = xlsxwriter.Workbook('rapport_stylé.xlsx')
worksheet = workbook.add_worksheet()

# Formats
header_format = workbook.add_format({
    'bold': True,
    'text_wrap': True,
    'valign': 'top',
    'fg_color': '#4472C4',
    'font_color': 'white',
    'border': 1
})

cell_format = workbook.add_format({
    'border': 1,
    'align': 'center',
    'valign': 'vcenter'
})

# Fusionner cellules
worksheet.merge_range('A1:D1', 'RAPPORT MENSUEL', header_format)

# Données
data = {
    'Mois': ['Janvier', 'Février', 'Mars'],
    'Ventes': [15000, 18000, 22000],
    'Coûts': [8000, 9500, 11000],
    'Profit': [7000, 8500, 11000]
}

df = pd.DataFrame(data)

# Écrire headers
for col_num, value in enumerate(df.columns.values):
    worksheet.write(1, col_num, value, header_format)

# Écrire données
for row_num, row_data in enumerate(df.values):
    for col_num, cell_data in enumerate(row_data):
        worksheet.write(row_num + 2, col_num, cell_data, cell_format)

# Ajuster largeurs
worksheet.set_column('A:D', 15)

workbook.close()
```

---

## 🧪 Vérifier l'Installation

```python
# test_installation.py
import sys

print("🔍 Vérification de l'environnement...\n")

libraries = {
    'PDF': ['pypdf', 'fitz', 'pikepdf', 'pdfplumber', 'reportlab', 'fpdf'],
    'Excel': ['openpyxl', 'xlsxwriter', 'pandas', 'formulas'],
    'Word': ['docx', 'docxtpl', 'mammoth'],
    'Analyse': ['pandas', 'numpy', 'matplotlib', 'seaborn', 'plotly']
}

for category, libs in libraries.items():
    print(f"📦 {category}:")
    for lib in libs:
        try:
            __import__(lib)
            print(f"  ✓ {lib}")
        except ImportError:
            print(f"  ❌ {lib} - NON INSTALLÉ")
    print()

print(f"🐍 Python version: {sys.version}")
```

Exécutez avec:
```powershell
conda activate pdf_excel_env
python test_installation.py
```

---

## 📚 Documentation

- [pypdf Documentation](https://pypdf.readthedocs.io/)
- [PyMuPDF Documentation](https://pymupdf.readthedocs.io/)
- [pandas Documentation](https://pandas.pydata.org/docs/)
- [python-docx Documentation](https://python-docx.readthedocs.io/)
- [ReportLab User Guide](https://www.reportlab.com/docs/reportlab-userguide.pdf)
- [xlsxwriter Documentation](https://xlsxwriter.readthedocs.io/)

---

## 🤝 Support

Pour toute question sur l'environnement ou les librairies, consultez la documentation officielle des librairies ou créez une issue.

---

## 📄 Licence

Projet éducatif - Libre d'utilisation

---

**Développé par un expert Python Senior avec 30 ans d'expérience** 🚀
