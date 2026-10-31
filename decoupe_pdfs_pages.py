"""
Script pour découper les PDFs - Extraire seulement les premières pages
"""

from pypdf import PdfReader, PdfWriter
from pathlib import Path

def decouper_pdf(fichier_source, fichier_sortie, nb_pages=10):
    """
    Découpe un PDF en extrayant seulement les premières pages
    
    Args:
        fichier_source: PDF source
        fichier_sortie: PDF de sortie
        nb_pages: Nombre de pages à extraire (défaut: 10)
    """
    try:
        reader = PdfReader(fichier_source)
        writer = PdfWriter()
        
        total_pages = len(reader.pages)
        pages_a_extraire = min(nb_pages, total_pages)
        
        # Extraire seulement les premières pages
        for i in range(pages_a_extraire):
            writer.add_page(reader.pages[i])
        
        # Sauvegarder
        with open(fichier_sortie, "wb") as f:
            writer.write(f)
        
        return (True, pages_a_extraire, total_pages)
        
    except Exception as e:
        return (False, 0, 0, str(e))


# Configuration
print("=" * 70)
print("✂️  DÉCOUPAGE DES PDFs - EXTRACTION DES PREMIÈRES PAGES")
print("=" * 70)
print()

# Demander combien de pages extraire
try:
    nb_pages = int(input("Combien de pages voulez-vous extraire par PDF? [défaut: 10]: ") or "10")
except ValueError:
    nb_pages = 10

print()
print(f"📏 Extraction des {nb_pages} premières pages de chaque PDF")
print("=" * 70)
print()

source = Path("Extraction")
sortie = source / "pdf_conso"

pdfs = list(source.glob("*.pdf"))

if not pdfs:
    print("⚠️  Aucun PDF trouvé!")
    exit(1)

print(f"🔍 {len(pdfs)} PDFs trouvés\n")

succes = 0
echecs = 0
total_pages_extraites = 0
total_pages_originales = 0

for i, pdf in enumerate(pdfs, 1):
    result = decouper_pdf(pdf, sortie / pdf.name, nb_pages)
    
    if result[0]:
        _, pages_extraites, pages_totales = result
        succes += 1
        total_pages_extraites += pages_extraites
        total_pages_originales += pages_totales
        
        print(f"{i}. ✅ {pdf.name}")
        print(f"   📄 {pages_extraites}/{pages_totales} pages extraites")
        
        if pages_extraites < nb_pages:
            print(f"   ℹ️  PDF plus court que {nb_pages} pages")
    else:
        echecs += 1
        print(f"{i}. ❌ {pdf.name} - Erreur: {result[3]}")
    
    print()

# Résumé
print("=" * 70)
print("📊 RÉSUMÉ DU DÉCOUPAGE")
print("=" * 70)
print(f"✅ Succès: {succes}/{len(pdfs)}")
print(f"❌ Échecs: {echecs}")
print(f"📄 Pages extraites: {total_pages_extraites} (sur {total_pages_originales} au total)")
print(f"📉 Réduction: {100 - (total_pages_extraites/total_pages_originales*100):.1f}% de pages en moins")
print(f"📁 Fichiers découpés dans: {sortie.absolute()}")
print("=" * 70)
print()
print("✨ Découpage terminé!")
