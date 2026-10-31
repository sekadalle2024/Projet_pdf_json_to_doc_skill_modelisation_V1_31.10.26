"""
Conversion Excel vers PDF AMÉLIORÉE
- Colonnes élargies selon le contenu
- Mode paysage optimisé
- Meilleure visibilité des données
"""

import pandas as pd
from pathlib import Path
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.lib.enums import TA_CENTER
import warnings

warnings.filterwarnings('ignore')

def calculer_largeur_colonne(df, nom_colonne, largeur_disponible):
    """
    Calculer la largeur optimale d'une colonne selon son contenu
    """
    # Longueur maximale dans la colonne (en-tête + données)
    max_len_header = len(str(nom_colonne))
    max_len_data = df[nom_colonne].astype(str).str.len().max()
    max_len = max(max_len_header, max_len_data)
    
    # Largeur estimée (environ 7 points par caractère)
    largeur_estimee = min(max_len * 7, largeur_disponible * 0.8)
    
    # Minimum 1cm, maximum 8cm
    return max(1*cm, min(largeur_estimee, 8*cm))


def lire_tous_onglets(fichier_excel):
    """
    Lire tous les onglets d'un fichier Excel
    """
    try:
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


def creer_tableau_pdf_optimise(df, largeur_page):
    """
    Créer un tableau PDF optimisé avec largeurs de colonnes adaptatives
    """
    # Limiter le nombre de lignes si trop grand
    MAX_ROWS = 100
    if len(df) > MAX_ROWS:
        df = df.head(MAX_ROWS)
        note_troncature = True
    else:
        note_troncature = False
    
    # Limiter le nombre de colonnes pour éviter débordement
    MAX_COLS = 20
    if len(df.columns) > MAX_COLS:
        df = df.iloc[:, :MAX_COLS]
        note_colonnes = True
    else:
        note_colonnes = False
    
    # Préparer les données (garder plus de texte)
    MAX_CELL_LENGTH = 100  # Augmenté de 50 à 100
    data = [df.columns.tolist()] + df.values.tolist()
    
    for i, row in enumerate(data):
        data[i] = [str(cell)[:MAX_CELL_LENGTH] if pd.notna(cell) else '' 
                   for cell in row]
    
    # Calculer les largeurs de colonnes de manière intelligente
    nb_colonnes = len(data[0])
    largeur_disponible_par_colonne = largeur_page / nb_colonnes
    
    col_widths = []
    for idx, col_name in enumerate(df.columns):
        largeur = calculer_largeur_colonne(df, col_name, largeur_disponible_par_colonne)
        col_widths.append(largeur)
    
    # Ajuster si la somme dépasse la largeur de page
    somme_largeurs = sum(col_widths)
    if somme_largeurs > largeur_page:
        facteur = largeur_page / somme_largeurs
        col_widths = [w * facteur * 0.95 for w in col_widths]  # 95% pour marges
    
    # Créer le tableau
    table = Table(data, colWidths=col_widths, repeatRows=1)
    
    # Style amélioré
    style = TableStyle([
        # En-tête - plus visible
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2E5C8A')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 8),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('TOPPADDING', (0, 0), (-1, 0), 10),
        
        # Corps - plus d'espace
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),  # Alignement en haut
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 7),
        ('TOPPADDING', (0, 1), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
        
        # Grille
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('LINEBELOW', (0, 0), (-1, 0), 2, colors.HexColor('#2E5C8A')),
        
        # Alternance de couleurs - plus subtile
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), 
         [colors.white, colors.HexColor('#F5F5F5')]),
        
        # Retour à la ligne automatique
        ('WORDWRAP', (0, 0), (-1, -1), True),
    ])
    
    table.setStyle(style)
    
    return table, note_troncature, note_colonnes


def excel_vers_pdf_optimise(fichier_excel, dossier_sortie):
    """
    Convertir un fichier Excel en PDF optimisé
    """
    nom_fichier = fichier_excel.stem
    fichier_pdf = dossier_sortie / f"{nom_fichier}_tables_optimise.pdf"
    
    print(f"   📄 {fichier_excel.name}")
    
    # Lire tous les onglets
    onglets = lire_tous_onglets(fichier_excel)
    
    if not onglets:
        print(f"      ⚠️  Aucun onglet valide trouvé")
        return False
    
    print(f"      📊 {len(onglets)} onglet(s) trouvé(s)")
    
    # Créer le PDF en mode PAYSAGE avec plus d'espace
    page_width, page_height = landscape(A4)
    
    doc = SimpleDocTemplate(
        str(fichier_pdf),
        pagesize=landscape(A4),
        rightMargin=20,
        leftMargin=20,
        topMargin=25,
        bottomMargin=25
    )
    
    # Styles
    styles = getSampleStyleSheet()
    style_titre = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=14,
        textColor=colors.HexColor('#2E5C8A'),
        spaceAfter=15,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    style_onglet = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=11,
        textColor=colors.HexColor('#2E5C8A'),
        spaceAfter=8,
        spaceBefore=12,
        fontName='Helvetica-Bold'
    )
    
    # Éléments du PDF
    elements = []
    
    # Titre principal
    titre = Paragraph(f"<b>{nom_fichier}</b>", style_titre)
    elements.append(titre)
    elements.append(Spacer(1, 0.2*inch))
    
    # Largeur disponible pour les tableaux
    largeur_page = page_width - 40  # Marges
    
    # Ajouter chaque onglet
    for i, (nom_onglet, df) in enumerate(onglets.items()):
        # Titre de l'onglet
        titre_onglet = Paragraph(
            f"<b>📊 Onglet: {nom_onglet}</b>", 
            style_onglet
        )
        elements.append(titre_onglet)
        
        # Info sur les données
        info = Paragraph(
            f"<i>{len(df)} lignes × {len(df.columns)} colonnes</i>",
            styles['Normal']
        )
        elements.append(info)
        elements.append(Spacer(1, 0.1*inch))
        
        # Créer le tableau optimisé
        try:
            table, troncature_lignes, troncature_colonnes = creer_tableau_pdf_optimise(df, largeur_page)
            elements.append(table)
            
            # Notes de troncature
            if troncature_lignes:
                note = Paragraph(
                    "<i>⚠️  Tableau tronqué à 100 lignes pour l'affichage</i>",
                    styles['Normal']
                )
                elements.append(Spacer(1, 0.1*inch))
                elements.append(note)
            
            if troncature_colonnes:
                note = Paragraph(
                    "<i>⚠️  Affichage limité aux 20 premières colonnes</i>",
                    styles['Normal']
                )
                elements.append(Spacer(1, 0.1*inch))
                elements.append(note)
            
            print(f"      ✅ '{nom_onglet}': {len(df)} lignes × {len(df.columns)} colonnes")
        except Exception as e:
            print(f"      ❌ Erreur création tableau '{nom_onglet}': {e}")
        
        # Saut de page entre onglets
        if i < len(onglets) - 1:
            elements.append(PageBreak())
    
    # Générer le PDF
    try:
        doc.build(elements)
        print(f"      ✅ PDF optimisé créé: {fichier_pdf.name}")
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
            onglets = lire_tous_onglets(fichier)
            nb_onglets = len(onglets)
            total_onglets += nb_onglets
            
            if excel_vers_pdf_optimise(fichier, dossier_source):
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
    print("📊 CONVERSION EXCEL → PDF OPTIMISÉE")
    print("✨ Colonnes élargies selon le contenu - Mode paysage")
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
    print(f"📁 PDFs optimisés créés dans: Base_excel/")
    print("   Nomenclature: *_tables_optimise.pdf")
    print("=" * 80)
    print()
    print("✨ Conversion optimisée terminée!")
    print()
    print("Améliorations appliquées:")
    print("  ✅ Largeurs de colonnes calculées selon le contenu")
    print("  ✅ Mode paysage (landscape A4)")
    print("  ✅ Texte plus long par cellule (100 caractères)")
    print("  ✅ Retour à la ligne automatique")
    print("  ✅ Marges réduites pour plus d'espace")
