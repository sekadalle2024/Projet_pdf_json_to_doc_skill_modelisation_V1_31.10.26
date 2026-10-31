"""
Comparer les PDFs avant/après découpage
"""

from pypdf import PdfReader
from pathlib import Path

print("=" * 90)
print("📊 COMPARAISON AVANT/APRÈS DÉCOUPAGE")
print("=" * 90)
print()
print(f"{'Fichier':<60} {'Original':>12} {'Découpé':>12}")
print("=" * 90)

source = Path("Extraction")
sortie = source / "pdf_conso"

for pdf_original in sorted(source.glob("*.pdf")):
    pdf_decoupe = sortie / pdf_original.name
    
    if pdf_decoupe.exists():
        try:
            pages_orig = len(PdfReader(pdf_original).pages)
            pages_dec = len(PdfReader(pdf_decoupe).pages)
            
            status = "✅ DÉCOUPÉ" if pages_dec < pages_orig else "⚠️ IDENTIQUE"
            
            print(f"{pdf_original.name:<60} {pages_orig:>12} {pages_dec:>12}  {status}")
            
        except Exception as e:
            print(f"{pdf_original.name:<60} {'ERREUR':>12}")

print("=" * 90)
print()
print("✅ = Le PDF a été réduit (découpage réussi)")
print("⚠️  = Le PDF a le même nombre de pages (pas de découpage)")
