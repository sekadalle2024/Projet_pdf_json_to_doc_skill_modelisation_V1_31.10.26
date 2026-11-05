"""
Script de conversion Markdown vers PDF
Convertit les rapports de recherche d'offres d'emploi en PDF professionnels
"""

import os
import sys
from pathlib import Path

def convert_md_to_pdf_markdown(md_file, pdf_file):
    """
    Convertit un fichier Markdown en PDF en utilisant markdown
    Alternative simple si reportlab seul ne suffit pas
    """
    try:
        import markdown
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import cm
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
        from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
        from reportlab.pdfbase import pdfmetrics
        from reportlab.pdfbase.ttfonts import TTFont
        
        # Lire le contenu Markdown
        with open(md_file, 'r', encoding='utf-8') as f:
            md_content = f.read()
        
        # Créer le PDF
        doc = SimpleDocTemplate(
            pdf_file,
            pagesize=A4,
            rightMargin=2*cm,
            leftMargin=2*cm,
            topMargin=2*cm,
            bottomMargin=2*cm
        )
        
        # Styles
        styles = getSampleStyleSheet()
        
        # Style personnalisé pour le titre
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=18,
            textColor='#2C3E50',
            spaceAfter=12,
            alignment=TA_CENTER
        )
        
        # Style pour les en-têtes
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=14,
            textColor='#34495E',
            spaceAfter=10,
            spaceBefore=10
        )
        
        # Style pour le texte normal
        normal_style = ParagraphStyle(
            'CustomNormal',
            parent=styles['Normal'],
            fontSize=10,
            alignment=TA_JUSTIFY,
            spaceAfter=6
        )
        
        # Construire le contenu
        story = []
        
        # Parser le markdown ligne par ligne
        lines = md_content.split('\n')
        
        for line in lines:
            line = line.strip()
            
            if not line:
                story.append(Spacer(1, 0.3*cm))
                continue
            
            # Titre principal (# )
            if line.startswith('# '):
                text = line[2:].strip()
                story.append(Paragraph(text, title_style))
                story.append(Spacer(1, 0.5*cm))
            
            # Sous-titre (## )
            elif line.startswith('## '):
                text = line[3:].strip()
                story.append(Paragraph(text, heading_style))
                story.append(Spacer(1, 0.3*cm))
            
            # Sous-sous-titre (### )
            elif line.startswith('### '):
                text = line[4:].strip()
                para_style = ParagraphStyle(
                    'SubHeading',
                    parent=styles['Heading3'],
                    fontSize=12,
                    textColor='#7F8C8D',
                    spaceAfter=8
                )
                story.append(Paragraph(text, para_style))
            
            # Liste à puces
            elif line.startswith('- ') or line.startswith('* '):
                text = '• ' + line[2:].strip()
                story.append(Paragraph(text, normal_style))
            
            # Liste numérotée
            elif len(line) > 2 and line[0].isdigit() and line[1] == '.':
                story.append(Paragraph(line, normal_style))
            
            # Ligne horizontale
            elif line.startswith('---'):
                story.append(Spacer(1, 0.5*cm))
            
            # Texte normal
            else:
                # Nettoyer le markdown basique
                text = line.replace('**', '<b>').replace('**', '</b>')
                text = text.replace('*', '<i>').replace('*', '</i>')
                text = text.replace('`', '<font face="Courier">')
                text = text.replace('`', '</font>')
                
                # Éviter les lignes vides
                if text.strip():
                    story.append(Paragraph(text, normal_style))
        
        # Générer le PDF
        doc.build(story)
        return True
        
    except Exception as e:
        print(f"Erreur avec markdown: {e}")
        return False


def convert_md_to_pdf_simple(md_file, pdf_file):
    """
    Convertit un fichier Markdown en PDF en utilisant une approche simple
    """
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import cm
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
        from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
        
        # Lire le contenu
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Créer le PDF
        doc = SimpleDocTemplate(
            pdf_file,
            pagesize=A4,
            rightMargin=2*cm,
            leftMargin=2*cm,
            topMargin=2*cm,
            bottomMargin=2*cm
        )
        
        styles = getSampleStyleSheet()
        story = []
        
        # Style de base
        normal_style = styles['Normal']
        normal_style.fontSize = 9
        normal_style.leading = 12
        
        # Traiter le contenu par lignes
        lines = content.split('\n')
        
        for line in lines:
            if line.strip():
                # Nettoyer les caractères markdown
                clean_line = line.replace('**', '').replace('*', '').replace('#', '').replace('`', '')
                clean_line = clean_line.replace('✅', '[OK]').replace('❌', '[NON]')
                clean_line = clean_line.replace('⭐', '*').replace('🎯', '[CIBLE]')
                clean_line = clean_line.replace('📊', '[STATS]').replace('💡', '[INFO]')
                
                if clean_line.strip():
                    try:
                        para = Paragraph(clean_line, normal_style)
                        story.append(para)
                        story.append(Spacer(1, 0.2*cm))
                    except:
                        # Si erreur, ajouter comme texte brut
                        pass
        
        doc.build(story)
        return True
        
    except Exception as e:
        print(f"Erreur conversion simple: {e}")
        return False


def main():
    """Fonction principale"""
    print("=== Conversion Markdown vers PDF ===\n")
    
    # Chemins
    base_dir = Path(r"h:\Projet_pdf_excel\Websearch_skill")
    resultats_dir = base_dir / "resultats"
    pdf_dir = base_dir / "resultats_pdf" / "Directeur_Audit_Interne"
    
    # Créer le dossier si nécessaire
    pdf_dir.mkdir(parents=True, exist_ok=True)
    
    # Fichiers à convertir
    files_to_convert = [
        ("Test_Directeurs_Audit_Afrique_Ouest_2026-11-02.md", 
         "01_Recherche_32_Offres_Directeur_Audit_Afrique_Ouest.pdf"),
        ("Recherche_10_Offres_Directeur_Audit_2026-11-02.md",
         "02_Top_10_Offres_Directeur_Audit_Afrique_Ouest.pdf"),
        ("SYNTHESE_10_OFFRES.md",
         "03_Synthese_Rapide_10_Offres.pdf")
    ]
    
    success_count = 0
    
    for md_filename, pdf_filename in files_to_convert:
        md_file = resultats_dir / md_filename
        pdf_file = pdf_dir / pdf_filename
        
        if not md_file.exists():
            print(f"❌ Fichier non trouvé: {md_filename}")
            continue
        
        print(f"📄 Conversion: {md_filename}")
        print(f"   → {pdf_filename}")
        
        # Essayer d'abord avec markdown
        success = convert_md_to_pdf_markdown(str(md_file), str(pdf_file))
        
        # Si échec, essayer méthode simple
        if not success:
            print("   Tentative méthode simple...")
            success = convert_md_to_pdf_simple(str(md_file), str(pdf_file))
        
        if success:
            print(f"   ✅ Succès!\n")
            success_count += 1
        else:
            print(f"   ❌ Échec\n")
    
    print(f"\n{'='*50}")
    print(f"Conversion terminée: {success_count}/{len(files_to_convert)} fichiers")
    print(f"Dossier de sortie: {pdf_dir}")
    print(f"{'='*50}")


if __name__ == "__main__":
    main()
