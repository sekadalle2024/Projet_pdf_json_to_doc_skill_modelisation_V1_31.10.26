"""
Exemple 2: Convertir un tableau Excel en PDF stylé
"""

import pandas as pd
from reportlab.lib.pagesizes import A4, letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch

def excel_vers_pdf_style(fichier_excel, fichier_pdf, nom_feuille=0):
    """
    Convertit un fichier Excel en PDF avec un tableau stylé
    
    Args:
        fichier_excel: Chemin du fichier Excel
        fichier_pdf: Chemin du fichier PDF de sortie
        nom_feuille: Nom ou index de la feuille (défaut: première feuille)
    """
    # Lire le fichier Excel
    df = pd.read_excel(fichier_excel, sheet_name=nom_feuille)
    
    # Créer le document PDF
    doc = SimpleDocTemplate(fichier_pdf, pagesize=A4)
    elements = []
    
    # Styles
    styles = getSampleStyleSheet()
    
    # Titre
    title = Paragraph(f"<b>Rapport de Données</b>", styles['Title'])
    elements.append(title)
    elements.append(Spacer(1, 0.3*inch))
    
    # Préparer les données pour le tableau
    data = [df.columns.tolist()] + df.values.tolist()
    
    # Créer le tableau
    table = Table(data)
    
    # Appliquer le style
    table.setStyle(TableStyle([
        # En-tête
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4472C4')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        
        # Corps du tableau
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('TOPPADDING', (0, 1), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
        
        # Grille
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        
        # Alternance de couleurs
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
    ]))
    
    elements.append(table)
    
    # Générer le PDF
    doc.build(elements)
    
    print(f"✅ PDF créé: {fichier_pdf}")
    print(f"   Lignes: {len(df)}")
    print(f"   Colonnes: {len(df.columns)}")


def creer_excel_exemple():
    """Crée un fichier Excel d'exemple"""
    data = {
        'Mois': ['Janvier', 'Février', 'Mars', 'Avril', 'Mai'],
        'Ventes': [15000, 18000, 22000, 19000, 25000],
        'Coûts': [8000, 9500, 11000, 10000, 12000],
        'Profit': [7000, 8500, 11000, 9000, 13000]
    }
    
    df = pd.DataFrame(data)
    fichier = "../Base_excel/exemple_ventes.xlsx"
    df.to_excel(fichier, index=False)
    
    print(f"✅ Fichier Excel d'exemple créé: {fichier}")
    return fichier


if __name__ == "__main__":
    print("=" * 60)
    print("Exemple: Conversion Excel → PDF avec style")
    print("=" * 60)
    print()
    
    # Créer un fichier Excel d'exemple
    fichier_excel = creer_excel_exemple()
    
    # Convertir en PDF
    excel_vers_pdf_style(
        fichier_excel,
        "../Base_pdf/rapport_ventes.pdf"
    )
    
    print("\n✨ Conversion terminée avec succès!")
    print("📄 Vérifiez le fichier: ../Base_pdf/rapport_ventes.pdf")
