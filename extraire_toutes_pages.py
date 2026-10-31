"""
Extraire TOUTES les pages de chaque PDF en fichiers individuels
Chaque page devient un fichier PDF séparé
"""

from pypdf import PdfReader, PdfWriter
from pathlib import Path

print("=" * 80)
print("📄 EXTRACTION DE TOUTES LES PAGES EN FICHIERS INDIVIDUELS")
print("=" * 80)
print()

source = Path("Extraction")
sortie_base = source / "pdf_conso"

# Supprimer les anciens fichiers dans pdf_conso
if sortie_base.exists():
    for item in sortie_base.iterdir():
        if item.is_file():
            item.unlink()
        elif item.is_dir():
            for sub_item in item.rglob('*'):
                if sub_item.is_file():
                    sub_item.unlink()
            for sub_dir in sorted(item.rglob('*'), reverse=True):
                if sub_dir.is_dir():
                    sub_dir.rmdir()
            item.rmdir()

sortie_base.mkdir(exist_ok=True)

# Trouver tous les PDFs sources
pdfs = sorted(source.glob("*.pdf"))

print(f"🔍 {len(pdfs)} PDFs à traiter\n")

total_pages = 0
total_fichiers = 0

for pdf_file in pdfs:
    try:
        reader = PdfReader(pdf_file)
        nb_pages = len(reader.pages)
        
        # Créer un sous-dossier pour chaque PDF
        nom_pdf = pdf_file.stem  # Nom sans extension
        dossier_pdf = sortie_base / nom_pdf
        dossier_pdf.mkdir(exist_ok=True)
        
        print(f"📁 {pdf_file.name}")
        print(f"   📄 {nb_pages} pages à extraire...")
        
        # Extraire chaque page individuellement
        for i in range(nb_pages):
            writer = PdfWriter()
            writer.add_page(reader.pages[i])
            
            # Nom: page_001.pdf, page_002.pdf, etc.
            nom_page = f"page_{i+1:03d}.pdf"
            fichier_page = dossier_pdf / nom_page
            
            with open(fichier_page, "wb") as f:
                writer.write(f)
            
            total_fichiers += 1
        
        total_pages += nb_pages
        print(f"   ✅ {nb_pages} fichiers PDF créés dans: {dossier_pdf.name}/")
        print()
        
    except Exception as e:
        print(f"   ❌ Erreur: {e}\n")

print("=" * 80)
print("📊 RÉSUMÉ")
print("=" * 80)
print(f"✅ PDFs traités: {len(pdfs)}")
print(f"📄 Total de pages extraites: {total_pages}")
print(f"📁 Total de fichiers PDF créés: {total_fichiers}")
print(f"📁 Emplacement: {sortie_base.absolute()}/")
print("=" * 80)
print()
print("✨ Extraction terminée!")
print()
print("Structure créée:")
print("  Extraction/pdf_conso/")
for pdf_file in pdfs:
    print(f"    ├── {pdf_file.stem}/")
    print(f"    │   ├── page_001.pdf")
    print(f"    │   ├── page_002.pdf")
    print(f"    │   └── ...")
