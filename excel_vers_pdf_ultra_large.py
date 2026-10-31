"""
Conversion Excel vers PDF ULTRA OPTIMISÉE
- Colonnes TRÈS LARGES pour afficher tout le contenu
- Taille de police réduite pour gagner de l'espace
- Mode paysage avec marges minimales
"""

import pandas as pd
from pathlib import Path
from reportlab.lib.pagesizes import A4, landscape, A3
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm, mm
from reportlab.lib.enums import TA_CENTER
import warnings

warnings.filterwarnings('ignore')

def lire_tous_onglets(fichier_excel):
    """Lire tous les onglets d'un fichier Excel"""
    try:
        excel_file = pd.ExcelFile(fichier_excel)
        onglets = {}
        
        for nom_onglet in excel_file.sheet_names:
            try:
                df = pd.read_excel(fichier_excel, sheet_name=nom_onglet)
                df = df.dropna(how='all').dropna(axis=1, how='all')
                
                if not df.empty:
                    onglets[nom_onglet] = df
            except Exception as e:
                print(f"      ⚠️  Erreur lecture onglet '{nom_onglet}': {e}")
        
        return onglets
    except Exception as e:
        print(f"      ❌ Erreur lecture fichier: {e}")
        return {}


def creer_tableau_pdf_ultra_large(df, largeur_page):
    """
    Créer un tableau PDF avec colonnes TRÈS LARGES
    """
    # Limiter les lignes
    MAX_ROWS = 100
    if len(df) > MAX_ROWS:
        df = df.head(MAX_ROWS)
        note_troncature = True
    else:
        note_troncature = False
    
    # Limiter les colonnes si trop nombreuses
    MAX_COLS = 15
    if len(df.columns) > MAX_COLS:
        df = df.iloc[:, :MAX_COLS]
        note_colonnes = True
    else:
        note_colonnes = False
    
    # Préparer les données - BEAUCOUP plus de texte
    MAX_CELL_LENGTH = 200  # Doublé!
    data = [df.columns.tolist()] + df.values.tolist()
    
    for i, row in enumerate(data):
        data[i] = [str(cell)[:MAX_CELL_LENGTH] if pd.notna(cell) else '' 
                   for cell in row]
    
    # Calcul TRÈS GÉNÉREUX des largeurs
    nb_colonnes = len(data[0])
    
    # Analyser le contenu de chaque colonne
    col_widths = []
    for idx in range(nb_colonnes):
        # Longueur max dans la colonne
        max_len = 0
        for row in data:
            if idx < len(row):
                max_len = max(max_len, len(str(row[idx])))
        
        # Largeur TRÈS généreuse: 5-6 points par caractère
        largeur = max(max_len * 5.5, 15*mm)  # Minimum 15mm
        
        # Maximum 12cm au lieu de 8cm
        largeur = min(largeur, 12*cm)
        
        col_widths.append(largeur)
    
    # Si débordement, réduire proportionnellement
    somme_largeurs = sum(col_widths)
    if somme_largeurs > largeur_page:
        facteur = largeur_page / somme_largeurs
        col_widths = [w * facteur * 0.98 for w in col_widths]
    
    # Créer le tableau
    table = Table(data, colWidths=col_widths, repeatRows=1)
    
    # Style OPTIMISÉ pour lisibilité maximale
    style = TableStyle([
        # En-tête - plus compact
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1F4788')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 7),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('TOPPADDING', (0, 0), (-1, 0), 8),
        
        # Corps - police réduite pour plus d'espace
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 6),  # Police 6pt au lieu de 7pt
        ('TOPPADDING', (0, 1), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 3),
        ('RIGHTPADDING', (0, 0), (-1, -1), 3),
        
        # Grille fine
        ('GRID', (0, 0), (-1, -1), 0.3, colors.grey),
        ('LINEBELOW', (0, 0), (-1, 0), 1.5, colors.HexColor('#1F4788')),
        
        # Alternance subtile
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), 
         [colors.white, colors.HexColor('#F8F8F8')]),
        
        # Retour à la ligne ACTIF
        ('WORDWRAP', (0, 0), (-1, -1), True),
    ])
    
    table.setStyle(style)
    
    return table, note_troncature, note_colonnes


def excel_vers_pdf_ultra_large(fichier_excel, dossier_sortie):
    """
    Convertir avec colonnes ULTRA LARGES
    """
    nom_fichier = fichier_excel.stem
    fichier_pdf = dossier_sortie / f"{nom_fichier}_ULTRA_LARGE.pdf"
    
    print(f"   📄 {fichier_excel.name}")
    
    # Lire tous les onglets
    onglets = lire_tous_onglets(fichier_excel)
    
    if not onglets:
        print(f"      ⚠️  Aucun onglet valide trouvé")
        return False
    
    print(f"      📊 {len(onglets)} onglet(s) trouvé(s)")
    
    # Format A3 paysage pour ENCORE PLUS d'espace
    # A3 paysage = 420mm × 297mm
    page_format = landscape(A3)
    
    doc = SimpleDocTemplate(
        str(fichier_pdf),
        pagesize=page_format,
        rightMargin=15,   # Marges TRÈS réduites
        leftMargin=15,
        topMargin=20,
        bottomMargin=20
    )
    
    # Styles
    styles = getSampleStyleSheet()
    style_titre = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=12,
        textColor=colors.HexColor('#1F4788'),
        spaceAfter=12,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    style_onglet = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=10,
        textColor=colors.HexColor('#1F4788'),
        spaceAfter=6,
        spaceBefore=10,
        fontName='Helvetica-Bold'
    )
    
    elements = []
    
    # Titre
    titre = Paragraph(f"<b>{nom_fichier}</b>", style_titre)
    elements.append(titre)
    elements.append(Spacer(1, 0.15*inch))
    
    # Largeur disponible (A3 paysage - marges)
    largeur_page = page_format[0] - 30  # ~41cm!
    
    # Ajouter chaque onglet
    for i, (nom_onglet, df) in enumerate(onglets.items()):
        titre_onglet = Paragraph(f"<b>📊 {nom_onglet}</b>", style_onglet)
        elements.append(titre_onglet)
        
        info = Paragraph(
            f"<i>{len(df)} lignes × {len(df.columns)} colonnes</i>",
            styles['Normal']
        )
        elements.append(info)
        elements.append(Spacer(1, 0.08*inch))
        
        try:
            table, troncature_lignes, troncature_colonnes = creer_tableau_pdf_ultra_large(df, largeur_page)
            elements.append(table)
            
            if troncature_lignes:
                note = Paragraph(
                    "<i>⚠️  Tableau limité à 100 lignes</i>",
                    styles['Normal']
                )
                elements.append(Spacer(1, 0.05*inch))
                elements.append(note)
            
            if troncature_colonnes:
                note = Paragraph(
                    "<i>⚠️  Affichage limité aux 15 premières colonnes</i>",
                    styles['Normal']
                )
                elements.append(Spacer(1, 0.05*inch))
                elements.append(note)
            
            print(f"      ✅ '{nom_onglet}': {len(df)} lignes × {len(df.columns)} colonnes")
        except Exception as e:
            print(f"      ❌ Erreur '{nom_onglet}': {e}")
        
        if i < len(onglets) - 1:
            elements.append(PageBreak())
    
    # Générer
    try:
        doc.build(elements)
        print(f"      ✅ PDF ULTRA LARGE créé: {fichier_pdf.name}")
        return True
    except Exception as e:
        print(f"      ❌ Erreur: {e}")
        return False


def traiter_tous_les_excel(dossier_source):
    """Traiter tous les fichiers Excel"""
    dossier_source = Path(dossier_source)
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
            
            if excel_vers_pdf_ultra_large(fichier, dossier_source):
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
    print("📊 CONVERSION EXCEL → PDF ULTRA OPTIMISÉE")
    print("✨ Format A3 PAYSAGE + Colonnes TRÈS LARGES")
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
    print(f"✅ Fichiers traités: {succes}")
    print(f"❌ Échecs: {echecs}")
    print(f"📄 Onglets traités: {total_onglets}")
    print(f"📁 PDFs dans: Base_excel/")
    print("   Nomenclature: *_ULTRA_LARGE.pdf")
    print("=" * 80)
    print()
    print("✨ Améliorations ULTRA:")
    print("  ✅ Format A3 PAYSAGE (420mm × 297mm)")
    print("  ✅ Colonnes jusqu'à 12cm de large")
    print("  ✅ Texte jusqu'à 200 caractères/cellule")
    print("  ✅ Police 6pt (très petite mais lisible)")
    print("  ✅ Marges 15pt (minimales)")
    print("  ✅ ~41cm de largeur utilisable!")
