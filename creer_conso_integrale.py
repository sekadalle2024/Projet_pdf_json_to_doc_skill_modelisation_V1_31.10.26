"""
Créer un dossier conso_integrale regroupant toutes les pages de tous les PDFs
Tous les fichiers au même niveau (pas de sous-dossiers)
"""

from pathlib import Path
import shutil

print("=" * 80)
print("📦 CRÉATION DU DOSSIER CONSO_INTEGRALE")
print("=" * 80)
print()

source = Path("Extraction/pdf_conso")
destination = Path("Extraction/conso_integrale")

# Créer le dossier de destination
destination.mkdir(exist_ok=True)
print(f"📁 Dossier créé: {destination.absolute()}\n")

# Supprimer les anciens fichiers s'il y en a
print("🗑️  Nettoyage du dossier...")
for fichier in destination.glob("*.pdf"):
    fichier.unlink()
print("   ✅ Nettoyage terminé\n")

# Copier tous les fichiers PDF de tous les sous-dossiers
print("📋 Copie de tous les fichiers PDF...\n")

total_fichiers = 0
fichiers_par_dossier = {}

# Parcourir tous les sous-dossiers
for sous_dossier in sorted(source.iterdir()):
    if sous_dossier.is_dir():
        nom_dossier = sous_dossier.name
        fichiers_pdf = list(sous_dossier.glob("*.pdf"))
        nb_fichiers = len(fichiers_pdf)
        
        fichiers_par_dossier[nom_dossier] = nb_fichiers
        
        print(f"📂 {nom_dossier}")
        print(f"   Copie de {nb_fichiers} fichiers...", end=" ")
        
        # Copier chaque fichier
        for fichier in fichiers_pdf:
            destination_fichier = destination / fichier.name
            shutil.copy2(fichier, destination_fichier)
            total_fichiers += 1
        
        print("✅")

print()
print("=" * 80)
print("📊 RÉSUMÉ")
print("=" * 80)
print(f"✅ Dossiers traités: {len(fichiers_par_dossier)}")
print(f"📄 Total fichiers copiés: {total_fichiers}")
print()
print("Détails par source:")
for dossier, nb in fichiers_par_dossier.items():
    print(f"  - {dossier}: {nb} fichiers")
print()
print(f"📁 Tous les fichiers sont dans: {destination.absolute()}")
print("=" * 80)
print()
print("✨ Consolidation terminée!")
print()
print(f"🎯 Vous avez maintenant {total_fichiers} fichiers PDF dans un seul dossier!")
