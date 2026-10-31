"""
Script automatique: Découpe les PDFs en gardant seulement les 10 premières pages
"""

from pypdf import PdfReader, PdfWriter
from pathlib import Path

NB_PAGES_A_EXTRAIRE = 10  # Modifier ce nombre selon vos besoins

print("=" * 70)
print(f"✂️  DÉCOUPAGE AUTOMATIQUE - {NB_PAGES_A_EXTRAIRE} PREMIÈRES PAGES")
print("=" * 70)
print()

source = Path("Extraction")
sortie = source / "pdf_conso"
sortie.mkdir(exist_ok=True)

pdfs = list(source.glob("*.pdf"))

print(f"🔍 {len(pdfs)} PDFs à découper\n")

succes = 0
total_pages_extraites = 0
total_pages_originales = 0

for i, pdf in enumerate(pdfs, 1):
    try:
        reader = PdfReader(pdf)
        writer = PdfWriter()
        
        total_pages = len(reader.pages)
        pages_a_extraire = min(NB_PAGES_A_EXTRAIRE, total_pages)
        
        # Extraire les premières pages
        for page_num in range(pages_a_extraire):
            writer.add_page(reader.pages[page_num])
        
        # Sauvegarder
        fichier_sortie = sortie / pdf.name
        with open(fichier_sortie, "wb") as f:
            writer.write(f)
        
        succes += 1
        total_pages_extraites += pages_a_extraire
        total_pages_originales += total_pages
        
        print(f"{i}. ✅ {pdf.name}")
        print(f"   📄 {pages_a_extraire}/{total_pages} pages extraites", end="")
        
        if pages_a_extraire < NB_PAGES_A_EXTRAIRE:
            print(f" (PDF plus court)")
        else:
            print()
        
    except Exception as e:
        print(f"{i}. ❌ {pdf.name} - Erreur: {e}")

print()
print("=" * 70)
print("📊 RÉSUMÉ")
print("=" * 70)
print(f"✅ Succès: {succes}/{len(pdfs)}")
print(f"📄 Pages extraites: {total_pages_extraites}")
print(f"📄 Pages originales: {total_pages_originales}")
print(f"📉 Réduction: {total_pages_originales - total_pages_extraites} pages supprimées")
print(f"📉 Taux de réduction: {100 - (total_pages_extraites/total_pages_originales*100):.1f}%")
print(f"📁 Fichiers dans: {sortie.absolute()}")
print("=" * 70)
print("\n✨ Découpage terminé!")
