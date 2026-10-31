"""
Exemple 1: Découper un PDF en plusieurs parties
"""

from pypdf import PdfReader, PdfWriter
from pathlib import Path

def decouper_pdf(fichier_source, pages_debut, pages_fin, fichier_sortie):
    """
    Découpe un PDF en extrayant les pages spécifiées
    
    Args:
        fichier_source: Chemin du PDF source
        pages_debut: Numéro de la première page (commence à 0)
        pages_fin: Numéro de la dernière page (incluse)
        fichier_sortie: Chemin du fichier de sortie
    """
    # Lire le PDF source
    reader = PdfReader(fichier_source)
    writer = PdfWriter()
    
    # Extraire les pages
    for page_num in range(pages_debut, pages_fin + 1):
        if page_num < len(reader.pages):
            writer.add_page(reader.pages[page_num])
    
    # Sauvegarder
    with open(fichier_sortie, "wb") as output_file:
        writer.write(output_file)
    
    print(f"✅ PDF découpé: {pages_fin - pages_debut + 1} pages extraites")
    print(f"   Fichier créé: {fichier_sortie}")


if __name__ == "__main__":
    # Exemple d'utilisation
    print("=" * 60)
    print("Exemple: Découpage de PDF")
    print("=" * 60)
    
    # Vérifier s'il y a des PDFs dans le dossier Extraction
    extraction_dir = Path("../Extraction")
    
    if extraction_dir.exists():
        pdf_files = list(extraction_dir.glob("*.pdf"))
        
        if pdf_files:
            premier_pdf = pdf_files[0]
            print(f"\nFichier trouvé: {premier_pdf.name}")
            
            # Lire le nombre de pages
            reader = PdfReader(premier_pdf)
            nb_pages = len(reader.pages)
            print(f"Nombre de pages: {nb_pages}")
            
            # Extraire les 3 premières pages
            if nb_pages >= 3:
                decouper_pdf(
                    premier_pdf,
                    0,  # Première page
                    2,  # Troisième page (index 2)
                    "../Base_pdf/extrait_3_premieres_pages.pdf"
                )
            else:
                print(f"⚠️  Le PDF a seulement {nb_pages} pages")
        else:
            print("\n⚠️  Aucun fichier PDF trouvé dans le dossier Extraction")
            print("📌 Vous pouvez tester avec votre propre PDF:")
            print("   decouper_pdf('votre_fichier.pdf', 0, 4, 'extrait.pdf')")
    else:
        print("\n📌 Exemple d'utilisation:")
        print("   decouper_pdf('document.pdf', 0, 4, 'extrait.pdf')")
