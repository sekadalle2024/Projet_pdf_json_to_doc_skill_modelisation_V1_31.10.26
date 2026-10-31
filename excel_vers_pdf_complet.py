"""
Extraire tous les tableaux de tous les onglets de tous les fichiers Excel
et créer un PDF par fichier Excel avec tous les tableaux
"""

import pandas as pd
from pathlib import Path
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER
import warnings

warnings.filterwarnings('ignore')

def lire_tous_onglets(fichier_excel):
    """
    Lire tous les onglets d'un fichier Excel
    Retourne un dictionnaire {nom_onglet: DataFrame}
    """
    try:
        # Lire tous les onglets
        excel_file = pd.ExcelFile(fichier_excel)
        onglets = {}
        
        for nom_onglet in excel_file.sheet_names:
            try:
                df = pd.read_excel(fichier_excel, sheet_name=nom_onglet)
                # Supprimer les colonnes et lignes complètement vides
                df = df.dropna(how='all').dropna(axis=1, how='all')
                
                if not df.empty:
                    onglets[nom_onglet] = df
            except Exception as e:
                print(f"      ⚠️  Erreur lecture onglet '{nom_onglet}': {e}")
        
        return onglets
    except Exception as e:
        print(f"      ❌ Erreur lecture fichier: {e}")
        return {}


def creer_tableau_pdf(df, largeur_page):
    """
    Créer un tableau PDF à partir d'un DataFrame
    """
    # Limiter le nombre de lignes affichées si trop grand
    MAX_ROWS = 100
    if len(df) > MAX_ROWS:
        df = df.head(MAX_ROWS)
        note_troncature = True
    else:
        note_troncature = False
    
    # Préparer les données
    data = [df.columns.tolist()] + df.values.tolist()
    
    # Convertir tout en string et limiter la longueur
    MAX_CELL_LENGTH = 50
    for i, row in enumerate(data):
        data[i] = [str(cell)[:MAX_CELL_LENGTH] if pd.notna(cell) else '' 
                   for cell in row]
    
    # Calculer la largeur des colonnes
    nb_colonnes = len(data[0])
    largeur_colonne = min(largeur_page / nb_colonnes, 2*inch)
    col_widths = [largeur_colonne] * nb_colonnes
    
    # Créer le tableau
    table = Table(data, colWidths=col_widths, repeatRows=1)
    
    # Style du tableau
    style = TableStyle([
        # En-tête
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4472C4')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('TOPPADDING', (0, 0), (-1, 0), 8),
        
        # Corps
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('TOPPADDING', (0, 1), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 4),
        
        # Grille
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        
        # Alternance de couleurs
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
    ])
    
    table.setStyle(style)
    
    return table, note_troncature


def excel_vers_pdf(fichier_excel, dossier_sortie):
    """
    Convertir un fichier Excel en PDF
    Un PDF par fichier Excel contenant tous les onglets
    """
    nom_fichier = fichier_excel.stem
    fichier_pdf = dossier_sortie / f"{nom_fichier}_tables.pdf"
    
    print(f"   📄 {fichier_excel.name}")
    
    # Lire tous les onglets
    onglets = lire_tous_onglets(fichier_excel)
    
    if not onglets:
        print(f"      ⚠️  Aucun onglet valide trouvé")
        return False
    
    print(f"      📊 {len(onglets)} onglet(s) trouvé(s)")
    
    # Créer le PDF en mode paysage pour plus de largeur
    doc = SimpleDocTemplate(
        str(fichier_pdf),
        pagesize=landscape(A4),
        rightMargin=30,
        leftMargin=30,
        topMargin=30,
        bottomMargin=30
    )
    
    # Styles
    styles = getSampleStyleSheet()
    style_titre = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        textColor=colors.HexColor('#4472C4'),
        spaceAfter=20,
        alignment=TA_CENTER
    )
    style_onglet = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=12,
        textColor=colors.HexColor('#2E5C8A'),
        spaceAfter=10,
        spaceBefore=15
    )
    
    # Éléments du PDF
    elements = []
    
    # Titre principal
    titre = Paragraph(f"<b>{nom_fichier}</b>", style_titre)
    elements.append(titre)
    elements.append(Spacer(1, 0.3*inch))
    
    largeur_page = landscape(A4)[0] - 60  # Largeur utile
    
    # Ajouter chaque onglet
    for i, (nom_onglet, df) in enumerate(onglets.items()):
        # Titre de l'onglet
        titre_onglet = Paragraph(f"<b>Onglet: {nom_onglet}</b>", style_onglet)
        elements.append(titre_onglet)
        
        # Info sur les données
        info = Paragraph(
            f"<i>{len(df)} lignes × {len(df.columns)} colonnes</i>",
            styles['Normal']
        )
        elements.append(info)
        elements.append(Spacer(1, 0.1*inch))
        
        # Créer le tableau
        try:
            table, troncature = creer_tableau_pdf(df, largeur_page)
            elements.append(table)
            
            if troncature:
                note = Paragraph(
                    "<i>Note: Tableau tronqué à 100 lignes pour l'affichage</i>",
                    styles['Normal']
                )
                elements.append(Spacer(1, 0.1*inch))
                elements.append(note)
            
            print(f"      ✅ '{nom_onglet}': {len(df)} lignes × {len(df.columns)} colonnes")
        except Exception as e:
            print(f"      ❌ Erreur création tableau '{nom_onglet}': {e}")
        
        # Saut de page entre les onglets (sauf le dernier)
        if i < len(onglets) - 1:
            elements.append(PageBreak())
    
    # Générer le PDF
    try:
        doc.build(elements)
        print(f"      ✅ PDF créé: {fichier_pdf.name}")
        return True
    except Exception as e:
        print(f"      ❌ Erreur création PDF: {e}")
        return False


def traiter_tous_les_excel(dossier_source):
    """
    Traiter tous les fichiers Excel d'un dossier
    """
    dossier_source = Path(dossier_source)
    
    # Trouver tous les fichiers Excel
    fichiers_excel = list(dossier_source.glob("*.xlsx")) + list(dossier_source.glob("*.xls"))
    
    if not fichiers_excel:
        print("⚠️  Aucun fichier Excel trouvé!")
        return
    
    print(f"🔍 {len(fichiers_excel)} fichier(s) Excel trouvé(s)\n")
    
    succes = 0
    echecs = 0
    total_onglets = 0
    
    for fichier in fichiers_excel:
        try:
            # Lire les onglets pour compter
            onglets = lire_tous_onglets(fichier)
            nb_onglets = len(onglets)
            total_onglets += nb_onglets
            
            # Créer le PDF
            if excel_vers_pdf(fichier, dossier_source):
                succes += 1
            else:
                echecs += 1
            
            print()
        except Exception as e:
            print(f"   ❌ Erreur: {e}\n")
            echecs += 1
    
    return succes, echecs, total_onglets


if __name__ == "__main__":
    print("=" * 80)
    print("📊 CONVERSION EXCEL → PDF - EXTRACTION DE TOUS LES TABLEAUX")
    print("=" * 80)
    print()
    
    dossier = "Base_excel"
    
    print(f"📁 Dossier source: {dossier}")
    print("=" * 80)
    print()
    
    succes, echecs, total_onglets = traiter_tous_les_excel(dossier)
    
    print("=" * 80)
    print("📊 RÉSUMÉ")
    print("=" * 80)
    print(f"✅ Fichiers traités avec succès: {succes}")
    print(f"❌ Échecs: {echecs}")
    print(f"📄 Total d'onglets traités: {total_onglets}")
    print(f"📁 PDFs créés dans: Base_excel/")
    print("=" * 80)
    print()
    print("✨ Conversion terminée!")
