"""
Conversion Excel vers PDF PERSONNALISÉE
Approche fichier par fichier avec analyse détaillée de chaque colonne
Calcul optimal des largeurs pour CHAQUE fichier spécifiquement
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

def analyser_colonne(df, nom_colonne):
    """
    Analyse approfondie d'une colonne pour calculer sa largeur optimale
    """
    # Longueur de l'en-tête
    len_header = len(str(nom_colonne))
    
    # Analyse des données de la colonne
    serie = df[nom_colonne].astype(str)
    
    # Statistiques sur les longueurs
    longueurs = serie.str.len()
    
    # Longueur moyenne
    len_moyenne = longueurs.mean()
    
    # Longueur maximale
    len_max = longueurs.max()
    
    # Longueur du 95e percentile (pour ignorer les valeurs extrêmes)
    len_95 = longueurs.quantile(0.95)
    
    # Décision intelligente
    # Utiliser le max entre header et le 95e percentile (ou max si < 150 caractères)
    if len_max < 150:
        len_optimale = max(len_header, len_max)
    else:
        len_optimale = max(len_header, len_95)
    
    return {
        'nom': nom_colonne,
        'len_header': len_header,
        'len_moyenne': len_moyenne,
        'len_max': len_max,
        'len_95': len_95,
        'len_optimale': len_optimale
    }


def calculer_largeurs_optimales_personnalisees(df, largeur_page_disponible):
    """
    Calcule les largeurs optimales pour CHAQUE colonne de CE fichier spécifique
    """
    print(f"         🔍 Analyse détaillée de {len(df.columns)} colonnes...")
    
    # Analyser chaque colonne
    analyses = []
    for col in df.columns:
        analyse = analyser_colonne(df, col)
        analyses.append(analyse)
    
    # Calculer les largeurs brutes
    largeurs_brutes = []
    for analyse in analyses:
        # Formule: longueur optimale × 5 points/caractère
        # Minimum 2cm, maximum 15cm
        largeur = analyse['len_optimale'] * 5
        largeur = max(2*cm, min(largeur, 15*cm))
        largeurs_brutes.append(largeur)
    
    # Somme totale
    somme_brutes = sum(largeurs_brutes)
    
    print(f"         📏 Largeur brute totale: {somme_brutes/cm:.1f}cm")
    print(f"         📏 Largeur disponible: {largeur_page_disponible/cm:.1f}cm")
    
    # Ajustement si nécessaire
    if somme_brutes > largeur_page_disponible:
        # Réduction proportionnelle
        facteur = largeur_page_disponible / somme_brutes
        largeurs_finales = [l * facteur * 0.97 for l in largeurs_brutes]
        print(f"         ⚙️  Ajustement appliqué: facteur {facteur:.2f}")
    else:
        # Expansion pour utiliser toute la largeur disponible
        facteur = largeur_page_disponible / somme_brutes
        # Ne pas trop agrandir (max 1.2x)
        facteur = min(facteur, 1.2)
        largeurs_finales = [l * facteur * 0.97 for l in largeurs_brutes]
        print(f"         ✨ Expansion appliquée: facteur {facteur:.2f}")
    
    # Afficher quelques statistiques
    print(f"         📊 Largeurs finales: min={min(largeurs_finales)/cm:.1f}cm, "
          f"max={max(largeurs_finales)/cm:.1f}cm, "
          f"moy={sum(largeurs_finales)/len(largeurs_finales)/cm:.1f}cm")
    
    return largeurs_finales, analyses


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


def creer_tableau_personnalise(df, largeur_page, nom_onglet):
    """
    Créer un tableau avec largeurs PERSONNALISÉES pour ce fichier
    """
    # Limiter lignes
    MAX_ROWS = 150  # Augmenté à 150
    if len(df) > MAX_ROWS:
        df = df.head(MAX_ROWS)
        note_troncature = True
    else:
        note_troncature = False
    
    # Limiter colonnes si vraiment trop
    MAX_COLS = 25  # Augmenté à 25
    if len(df.columns) > MAX_COLS:
        df = df.iloc[:, :MAX_COLS]
        note_colonnes = True
    else:
        note_colonnes = False
    
    # Calculer largeurs OPTIMALES pour CE tableau
    col_widths, analyses = calculer_largeurs_optimales_personnalisees(df, largeur_page)
    
    # Préparer les données - BEAUCOUP de texte
    MAX_CELL_LENGTH = 300  # Triplé!
    data = [df.columns.tolist()] + df.values.tolist()
    
    for i, row in enumerate(data):
        data[i] = [str(cell)[:MAX_CELL_LENGTH] if pd.notna(cell) else '' 
                   for cell in row]
    
    # Créer le tableau
    table = Table(data, colWidths=col_widths, repeatRows=1)
    
    # Style professionnel
    style = TableStyle([
        # En-tête
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1F4788')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 7),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('TOPPADDING', (0, 0), (-1, 0), 8),
        
        # Corps
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 6),
        ('TOPPADDING', (0, 1), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
        
        # Grille
        ('GRID', (0, 0), (-1, -1), 0.3, colors.grey),
        ('LINEBELOW', (0, 0), (-1, 0), 1.5, colors.HexColor('#1F4788')),
        
        # Alternance
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), 
         [colors.white, colors.HexColor('#F8F8F8')]),
        
        # Retour à la ligne OBLIGATOIRE
        ('WORDWRAP', (0, 0), (-1, -1), True),
    ])
    
    table.setStyle(style)
    
    return table, note_troncature, note_colonnes


def excel_vers_pdf_personnalise(fichier_excel, dossier_sortie):
    """
    Convertir avec analyse PERSONNALISÉE pour ce fichier
    """
    nom_fichier = fichier_excel.stem
    fichier_pdf = dossier_sortie / f"{nom_fichier}_PERSONNALISE.pdf"
    
    print(f"\n   📄 {fichier_excel.name}")
    print(f"   {'='*70}")
    
    # Lire tous les onglets
    onglets = lire_tous_onglets(fichier_excel)
    
    if not onglets:
        print(f"      ⚠️  Aucun onglet valide trouvé")
        return False
    
    print(f"      📊 {len(onglets)} onglet(s) trouvé(s)")
    
    # Format A3 paysage
    page_format = landscape(A3)
    
    doc = SimpleDocTemplate(
        str(fichier_pdf),
        pagesize=page_format,
        rightMargin=12,
        leftMargin=12,
        topMargin=18,
        bottomMargin=18
    )
    
    # Styles
    styles = getSampleStyleSheet()
    style_titre = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=13,
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
    elements.append(Spacer(1, 0.12*inch))
    
    # Largeur disponible
    largeur_page = page_format[0] - 24
    
    print(f"      📐 Largeur page disponible: {largeur_page/cm:.1f}cm\n")
    
    # Traiter chaque onglet
    for i, (nom_onglet, df) in enumerate(onglets.items()):
        print(f"      📋 Onglet: '{nom_onglet}'")
        print(f"         📊 Dimensions: {len(df)} lignes × {len(df.columns)} colonnes")
        
        titre_onglet = Paragraph(f"<b>📊 {nom_onglet}</b>", style_onglet)
        elements.append(titre_onglet)
        
        info = Paragraph(
            f"<i>{len(df)} lignes × {len(df.columns)} colonnes</i>",
            styles['Normal']
        )
        elements.append(info)
        elements.append(Spacer(1, 0.08*inch))
        
        try:
            table, troncature_lignes, troncature_colonnes = creer_tableau_personnalise(
                df, largeur_page, nom_onglet
            )
            elements.append(table)
            
            if troncature_lignes:
                note = Paragraph(
                    "<i>⚠️  Affichage limité à 150 lignes</i>",
                    styles['Normal']
                )
                elements.append(Spacer(1, 0.05*inch))
                elements.append(note)
            
            if troncature_colonnes:
                note = Paragraph(
                    "<i>⚠️  Affichage limité aux 25 premières colonnes</i>",
                    styles['Normal']
                )
                elements.append(Spacer(1, 0.05*inch))
                elements.append(note)
            
            print(f"         ✅ Tableau créé avec succès\n")
        except Exception as e:
            print(f"         ❌ Erreur: {e}\n")
        
        if i < len(onglets) - 1:
            elements.append(PageBreak())
    
    # Générer
    try:
        doc.build(elements)
        print(f"      ✅ PDF PERSONNALISÉ créé: {fichier_pdf.name}")
        print(f"   {'='*70}")
        return True
    except Exception as e:
        print(f"      ❌ Erreur création PDF: {e}")
        return False


def traiter_tous_les_excel(dossier_source):
    """Traiter chaque fichier individuellement"""
    dossier_source = Path(dossier_source)
    fichiers_excel = list(dossier_source.glob("*.xlsx")) + list(dossier_source.glob("*.xls"))
    
    if not fichiers_excel:
        print("⚠️  Aucun fichier Excel trouvé!")
        return
    
    print(f"🔍 {len(fichiers_excel)} fichier(s) Excel trouvé(s)")
    print("="*80)
    
    succes = 0
    echecs = 0
    total_onglets = 0
    
    for fichier in fichiers_excel:
        try:
            onglets = lire_tous_onglets(fichier)
            nb_onglets = len(onglets)
            total_onglets += nb_onglets
            
            if excel_vers_pdf_personnalise(fichier, dossier_source):
                succes += 1
            else:
                echecs += 1
        except Exception as e:
            print(f"\n   ❌ Erreur: {e}\n")
            echecs += 1
    
    return succes, echecs, total_onglets


if __name__ == "__main__":
    print("=" * 80)
    print("📊 CONVERSION EXCEL → PDF PERSONNALISÉE")
    print("✨ Analyse fichier par fichier + Largeurs optimales individuelles")
    print("=" * 80)
    print()
    
    dossier = "Base_excel"
    
    succes, echecs, total_onglets = traiter_tous_les_excel(dossier)
    
    print("\n" + "=" * 80)
    print("📊 RÉSUMÉ FINAL")
    print("=" * 80)
    print(f"✅ Fichiers traités avec succès: {succes}")
    print(f"❌ Échecs: {echecs}")
    print(f"📄 Total d'onglets traités: {total_onglets}")
    print(f"📁 PDFs dans: Base_excel/")
    print("   Nomenclature: *_PERSONNALISE.pdf")
    print("=" * 80)
    print()
    print("✨ APPROCHE PERSONNALISÉE:")
    print("  ✅ Analyse colonne par colonne POUR CHAQUE FICHIER")
    print("  ✅ Largeurs calculées selon le contenu RÉEL")
    print("  ✅ Optimisation individuelle par tableau")
    print("  ✅ Utilisation maximale de l'espace disponible")
    print("  ✅ Format A3 paysage (~41cm)")
    print("  ✅ Jusqu'à 300 caractères par cellule")
