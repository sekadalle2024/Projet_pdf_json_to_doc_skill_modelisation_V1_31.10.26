"""
Script pour découper tous les PDFs d'un dossier
et sauvegarder les copies dans un sous-dossier 'pdf_conso'
"""

from pypdf import PdfReader, PdfWriter
from pathlib import Path
import sys

def decouper_pdf(fichier_source, fichier_sortie, pages_debut=0, pages_fin=None):
    """
    Découpe un PDF en extrayant les pages spécifiées
    
    Args:
        fichier_source: Chemin du PDF source
        fichier_sortie: Chemin du fichier de sortie
        pages_debut: Numéro de la première page (défaut: 0, première page)
        pages_fin: Numéro de la dernière page (défaut: None, toutes les pages)
    
    Returns:
        Tuple (succès, nombre_pages, message)
    """
    try:
        # Lire le PDF source
        reader = PdfReader(fichier_source)
        nb_total_pages = len(reader.pages)
        
        # Si pages_fin n'est pas spécifié, prendre toutes les pages
        if pages_fin is None:
            pages_fin = nb_total_pages - 1
        
        # Vérifier que pages_fin ne dépasse pas
        pages_fin = min(pages_fin, nb_total_pages - 1)
        
        # Créer le writer
        writer = PdfWriter()
        
        # Extraire les pages
        for page_num in range(pages_debut, pages_fin + 1):
            if page_num < nb_total_pages:
                writer.add_page(reader.pages[page_num])
        
        # Sauvegarder
        with open(fichier_sortie, "wb") as output_file:
            writer.write(output_file)
        
        nb_pages_extraites = pages_fin - pages_debut + 1
        return (True, nb_pages_extraites, f"Succès: {nb_pages_extraites} pages extraites sur {nb_total_pages}")
        
    except Exception as e:
        return (False, 0, f"Erreur: {str(e)}")


def decouper_tous_les_pdfs(dossier_source, sous_dossier_sortie="pdf_conso", 
                           pages_debut=0, pages_fin=None, max_pages=None):
    """
    Découpe tous les PDFs d'un dossier et les sauvegarde dans un sous-dossier
    
    Args:
        dossier_source: Dossier contenant les PDFs sources
        sous_dossier_sortie: Nom du sous-dossier de sortie (défaut: "pdf_conso")
        pages_debut: Page de début pour le découpage (défaut: 0)
        pages_fin: Page de fin pour le découpage (défaut: None, toutes les pages)
        max_pages: Si spécifié, limite le nombre de pages à extraire par PDF
    """
    # Convertir en Path
    dossier_source = Path(dossier_source)
    
    # Créer le dossier de sortie
    dossier_sortie = dossier_source / sous_dossier_sortie
    dossier_sortie.mkdir(exist_ok=True)
    
    # Trouver tous les PDFs
    pdf_files = list(dossier_source.glob("*.pdf"))
    
    if not pdf_files:
        print(f"⚠️  Aucun fichier PDF trouvé dans {dossier_source}")
        return
    
    print("=" * 70)
    print(f"🔪 DÉCOUPAGE DE {len(pdf_files)} PDFs")
    print("=" * 70)
    print(f"📁 Dossier source: {dossier_source}")
    print(f"📁 Dossier sortie: {dossier_sortie}")
    print(f"📄 Pages à extraire: {pages_debut} à {pages_fin if pages_fin else 'fin'}")
    if max_pages:
        print(f"📏 Limite: {max_pages} pages maximum par PDF")
    print("=" * 70)
    print()
    
    succes = 0
    echecs = 0
    total_pages_extraites = 0
    
    for i, pdf_file in enumerate(pdf_files, 1):
        print(f"[{i}/{len(pdf_files)}] {pdf_file.name}")
        
        # Calculer la page de fin si max_pages est spécifié
        fin = pages_fin
        if max_pages:
            fin = pages_debut + max_pages - 1
        
        # Nom du fichier de sortie
        fichier_sortie = dossier_sortie / pdf_file.name
        
        # Découper le PDF
        success, nb_pages, message = decouper_pdf(pdf_file, fichier_sortie, pages_debut, fin)
        
        if success:
            succes += 1
            total_pages_extraites += nb_pages
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
    print(f"📄 Total pages extraites: {total_pages_extraites}")
    print(f"📁 Fichiers sauvegardés dans: {dossier_sortie}")
    print("=" * 70)


if __name__ == "__main__":
    # Configuration par défaut
    DOSSIER_SOURCE = "Extraction"  # Dossier contenant les PDFs
    SOUS_DOSSIER = "pdf_conso"      # Sous-dossier de sortie
    
    print("=" * 70)
    print("🔪 DÉCOUPAGE AUTOMATIQUE DE PDFs")
    print("=" * 70)
    print()
    
    # Vérifier que le dossier source existe
    dossier = Path(DOSSIER_SOURCE)
    if not dossier.exists():
        print(f"❌ Le dossier {DOSSIER_SOURCE} n'existe pas!")
        sys.exit(1)
    
    # Options de découpage
    print("Choisissez une option:")
    print()
    print("1. Copier tous les PDFs complets (toutes les pages)")
    print("2. Extraire les 5 premières pages de chaque PDF")
    print("3. Extraire les 10 premières pages de chaque PDF")
    print("4. Extraire un nombre de pages personnalisé")
    print()
    
    choix = input("Votre choix (1-4) [défaut: 1]: ").strip() or "1"
    
    print()
    
    if choix == "1":
        # Copier tous les PDFs complets
        decouper_tous_les_pdfs(
            dossier_source=DOSSIER_SOURCE,
            sous_dossier_sortie=SOUS_DOSSIER,
            pages_debut=0,
            pages_fin=None
        )
    
    elif choix == "2":
        # Extraire les 5 premières pages
        decouper_tous_les_pdfs(
            dossier_source=DOSSIER_SOURCE,
            sous_dossier_sortie=SOUS_DOSSIER,
            pages_debut=0,
            max_pages=5
        )
    
    elif choix == "3":
        # Extraire les 10 premières pages
        decouper_tous_les_pdfs(
            dossier_source=DOSSIER_SOURCE,
            sous_dossier_sortie=SOUS_DOSSIER,
            pages_debut=0,
            max_pages=10
        )
    
    elif choix == "4":
        # Nombre personnalisé
        try:
            nb_pages = int(input("Nombre de pages à extraire par PDF: "))
            decouper_tous_les_pdfs(
                dossier_source=DOSSIER_SOURCE,
                sous_dossier_sortie=SOUS_DOSSIER,
                pages_debut=0,
                max_pages=nb_pages
            )
        except ValueError:
            print("❌ Nombre invalide!")
            sys.exit(1)
    
    else:
        print("❌ Choix invalide!")
        sys.exit(1)
    
    print()
    print("✨ Terminé!")
