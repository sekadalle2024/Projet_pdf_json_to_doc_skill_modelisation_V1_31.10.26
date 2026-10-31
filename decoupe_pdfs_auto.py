"""
Script automatique pour copier tous les PDFs du dossier Extraction
vers un sous-dossier pdf_conso (copie complète de tous les PDFs)
"""

from pypdf import PdfReader, PdfWriter
from pathlib import Path

def copier_pdf_complet(fichier_source, fichier_sortie):
    """
    Copie un PDF complet (toutes les pages)
    
    Args:
        fichier_source: Chemin du PDF source
        fichier_sortie: Chemin du fichier de sortie
    
    Returns:
        Tuple (succès, nombre_pages, message)
    """
    try:
        reader = PdfReader(fichier_source)
        writer = PdfWriter()
        
        # Copier toutes les pages
        for page in reader.pages:
            writer.add_page(page)
        
        # Sauvegarder
        with open(fichier_sortie, "wb") as output_file:
            writer.write(output_file)
        
        nb_pages = len(reader.pages)
        return (True, nb_pages, f"{nb_pages} pages copiées")
        
    except Exception as e:
        return (False, 0, f"Erreur: {str(e)}")


# Configuration
DOSSIER_SOURCE = Path("Extraction")
SOUS_DOSSIER = "pdf_conso"

print("=" * 70)
print("📋 COPIE AUTOMATIQUE DE TOUS LES PDFs")
print("=" * 70)
print()

# Créer le dossier de sortie
dossier_sortie = DOSSIER_SOURCE / SOUS_DOSSIER
dossier_sortie.mkdir(exist_ok=True)

print(f"📁 Dossier source: {DOSSIER_SOURCE}")
print(f"📁 Dossier sortie: {dossier_sortie}")
print()

# Trouver tous les PDFs
pdf_files = list(DOSSIER_SOURCE.glob("*.pdf"))

if not pdf_files:
    print(f"⚠️  Aucun fichier PDF trouvé dans {DOSSIER_SOURCE}")
    exit(0)

print(f"🔍 {len(pdf_files)} fichiers PDF trouvés")
print("=" * 70)
print()

succes = 0
echecs = 0
total_pages = 0

for i, pdf_file in enumerate(pdf_files, 1):
    print(f"[{i}/{len(pdf_files)}] {pdf_file.name}")
    
    # Nom du fichier de sortie
    fichier_sortie = dossier_sortie / pdf_file.name
    
    # Copier le PDF
    success, nb_pages, message = copier_pdf_complet(pdf_file, fichier_sortie)
    
    if success:
        succes += 1
        total_pages += nb_pages
        print(f"   ✅ {message}")
    else:
        echecs += 1
        print(f"   ❌ {message}")
    
    print()

# Résumé
print("=" * 70)
print("📊 RÉSUMÉ")
print("=" * 70)
print(f"✅ Réussis: {succes}/{len(pdf_files)}")
print(f"❌ Échecs: {echecs}/{len(pdf_files)}")
print(f"📄 Total pages copiées: {total_pages}")
print(f"📁 Fichiers dans: {dossier_sortie.absolute()}")
print("=" * 70)
print()
print("✨ Terminé!")
