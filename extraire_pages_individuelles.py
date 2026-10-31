"""
Extraire chaque page d'un PDF en fichiers PDF séparés
"""

from pypdf import PdfReader, PdfWriter
from pathlib import Path

print("=" * 80)
print("📄 EXTRACTION DES PAGES INDIVIDUELLES")
print("=" * 80)
print()

source = Path("Extraction")
sortie_base = source / "pdf_conso"

# Trouver tous les PDFs sources
pdfs = list(source.glob("*.pdf"))

print(f"🔍 {len(pdfs)} PDFs à traiter\n")

total_pages = 0

for pdf_file in pdfs:
    try:
        reader = PdfReader(pdf_file)
        nb_pages = len(reader.pages)
        
        # Créer un sous-dossier pour chaque PDF
        nom_pdf = pdf_file.stem  # Nom sans extension
        dossier_pdf = sortie_base / nom_pdf
        dossier_pdf.mkdir(exist_ok=True)
        
        print(f"📁 {pdf_file.name} ({nb_pages} pages)")
        
        # Extraire chaque page
        for i in range(nb_pages):
            writer = PdfWriter()
            writer.add_page(reader.pages[i])
            
            # Nom: NomPDF_page_001.pdf
            nom_page = f"{nom_pdf}_page_{i+1:03d}.pdf"
            fichier_page = dossier_pdf / nom_page
            
            with open(fichier_page, "wb") as f:
                writer.write(f)
            
            total_pages += 1
        
        print(f"   ✅ {nb_pages} pages extraites dans: {dossier_pdf.name}/")
        print()
        
    except Exception as e:
        print(f"   ❌ Erreur: {e}\n")

print("=" * 80)
print(f"📊 TOTAL: {total_pages} pages extraites individuellement")
print(f"📁 Fichiers dans: {sortie_base.absolute()}/[nom_pdf]/")
print("=" * 80)
print("\n✨ Extraction terminée!")
