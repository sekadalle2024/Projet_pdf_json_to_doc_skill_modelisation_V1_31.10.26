"""
Script simple pour copier tous les PDFs - Version rapide
"""

from pypdf import PdfReader, PdfWriter
from pathlib import Path

# Configuration
source = Path("Extraction")
sortie = source / "pdf_conso"
sortie.mkdir(exist_ok=True)

pdfs = list(source.glob("*.pdf"))

print(f"Copie de {len(pdfs)} PDFs...")

for i, pdf in enumerate(pdfs, 1):
    try:
        reader = PdfReader(pdf)
        writer = PdfWriter()
        
        for page in reader.pages:
            writer.add_page(page)
        
        with open(sortie / pdf.name, "wb") as f:
            writer.write(f)
        
        print(f"{i}. ✅ {pdf.name} ({len(reader.pages)} pages)")
    except Exception as e:
        print(f"{i}. ❌ {pdf.name} - Erreur: {e}")

print(f"\n✨ Terminé! Fichiers dans: {sortie}")
