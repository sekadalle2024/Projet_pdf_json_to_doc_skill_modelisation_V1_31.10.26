"""
Script pour vérifier le découpage - Comparer avant/après
"""

from pypdf import PdfReader
from pathlib import Path

print("=" * 80)
print("📊 VÉRIFICATION DU DÉCOUPAGE")
print("=" * 80)
print()

source = Path("Extraction")
sortie = source / "pdf_conso"

pdfs_source = sorted(source.glob("*.pdf"))

print(f"{'Fichier':<50} {'Original':>10} {'Découpé':>10} {'Réduction':>10}")
print("=" * 80)

total_avant = 0
total_apres = 0

for pdf_original in pdfs_source:
    pdf_decoupe = sortie / pdf_original.name
    
    if pdf_decoupe.exists():
        try:
            pages_original = len(PdfReader(pdf_original).pages)
            pages_decoupe = len(PdfReader(pdf_decoupe).pages)
            
            total_avant += pages_original
            total_apres += pages_decoupe
            
            reduction = pages_original - pages_decoupe
            
            nom_court = pdf_original.name[:47] + "..." if len(pdf_original.name) > 50 else pdf_original.name
            
            print(f"{nom_court:<50} {pages_original:>10} {pages_decoupe:>10} {reduction:>10}")
            
        except Exception as e:
            print(f"{pdf_original.name:<50} {'Erreur':>10}")
    else:
        print(f"{pdf_original.name:<50} {'Non découpé':>10}")

print("=" * 80)
print(f"{'TOTAL':<50} {total_avant:>10} {total_apres:>10} {total_avant - total_apres:>10}")
print("=" * 80)
print()
print(f"📉 Taux de réduction: {100 - (total_apres/total_avant*100):.1f}%")
print(f"💾 Espace économisé: ~{total_avant - total_apres} pages")
