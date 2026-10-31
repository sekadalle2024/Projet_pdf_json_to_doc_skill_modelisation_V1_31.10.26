"""
Extraire TOUTES les pages avec le nom du PDF source dans le nom de fichier
Format: NomDuPDF_page_001.pdf
"""

from pypdf import PdfReader, PdfWriter
from pathlib import Path
import re

def nettoyer_nom(nom):
    """Nettoyer le nom de fichier pour éviter les caractères problématiques"""
    # Remplacer les caractères spéciaux
    nom = nom.replace(' ', '_')
    nom = nom.replace('.', '_')
    nom = nom.replace('-', '_')
    nom = re.sub(r'[^\w_]', '', nom)  # Garder seulement lettres, chiffres et _
    # Supprimer les underscores multiples
    nom = re.sub(r'_+', '_', nom)
    return nom

print("=" * 80)
print("📄 EXTRACTION AVEC NOM SOURCE - TOUTES LES PAGES")
print("=" * 80)
print()

source = Path("Extraction")
sortie_base = source / "pdf_conso"

# Supprimer les anciens fichiers
if sortie_base.exists():
    print("🗑️  Suppression des anciens fichiers...")
    for item in sortie_base.rglob('*'):
        if item.is_file():
            item.unlink()
    for item in sorted(sortie_base.rglob('*'), reverse=True):
        if item.is_dir():
            item.rmdir()
    print("   ✅ Nettoyage terminé\n")

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
        nom_pdf_original = pdf_file.stem
        nom_pdf_propre = nettoyer_nom(nom_pdf_original)
        dossier_pdf = sortie_base / nom_pdf_original
        dossier_pdf.mkdir(exist_ok=True)
        
        print(f"📁 {pdf_file.name}")
        print(f"   📄 {nb_pages} pages à extraire...")
        
        # Extraire chaque page avec le nom du PDF dans le nom de fichier
        for i in range(nb_pages):
            writer = PdfWriter()
            writer.add_page(reader.pages[i])
            
            # Format: NomDuPDF_page_001.pdf
            nom_page = f"{nom_pdf_propre}_page_{i+1:03d}.pdf"
            fichier_page = dossier_pdf / nom_page
            
            with open(fichier_page, "wb") as f:
                writer.write(f)
            
            total_fichiers += 1
        
        total_pages += nb_pages
        print(f"   ✅ {nb_pages} fichiers créés: {nom_pdf_propre}_page_XXX.pdf")
        print()
        
    except Exception as e:
        print(f"   ❌ Erreur: {e}\n")

print("=" * 80)
print("📊 RÉSUMÉ")
print("=" * 80)
print(f"✅ PDFs traités: {len(pdfs)}")
print(f"📄 Pages extraites: {total_pages}")
print(f"📁 Fichiers PDF créés: {total_fichiers}")
print(f"📁 Emplacement: {sortie_base.absolute()}/")
print("=" * 80)
print()
print("✨ Extraction terminée!")
print()
print("Nomenclature utilisée:")
print("  Format: NomDuPDF_page_001.pdf")
print()
print("Exemples:")
for pdf_file in pdfs[:3]:
    nom_propre = nettoyer_nom(pdf_file.stem)
    print(f"  - {nom_propre}_page_001.pdf")
    print(f"  - {nom_propre}_page_002.pdf")
    print()
