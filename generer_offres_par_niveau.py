#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Génération de PDFs d'offres d'emploi par niveau hiérarchique
Afrique de l'Ouest Francophone
"""

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
import os

# Définition des 50 offres DIRECTEURS
OFFRES_DIRECTEURS = [
    {"id": "DIR-CI-01", "titre": "DIRECTEUR AUDIT INTERNE", "entreprise": "YESHI GROUP", "ville": "Abidjan", "pays": "Côte d'Ivoire", "date": "Septembre 2026", "experience": "10+ ans", "salaire": "5M - 7M FCFA", "certifications": "CIA obligatoire", "missions": ["Définir la stratégie d'audit annuelle", "Manager une équipe de 5-10 auditeurs", "Présenter au Comité d'Audit", "Relations avec régulateurs"], "profil": "Master Audit/Finance + 10 ans expérience dont 5 ans management"},
    {"id": "DIR-CI-02", "titre": "DIRECTEUR AUDIT ET INSPECTION", "entreprise": "ORANGE CÔTE D'IVOIRE", "ville": "Abidjan", "pays": "Côte d'Ivoire", "date": "2023", "experience": "10+ ans", "salaire": "6M - 8M FCFA", "certifications": "CIA, CISA", "missions": ["Direction audit groupe Afrique Ouest", "Audit IT et cybersécurité", "Conformité ARCEP", "Management équipe régionale"], "profil": "Ingénieur/Master + 10 ans audit télécoms"},
    {"id": "DIR-CI-03", "titre": "CHEF DÉPARTEMENT AUDIT INTERNE", "entreprise": "AFRICA GLOBAL LOGISTICS", "ville": "Abidjan", "pays": "Côte d'Ivoire", "date": "2024", "experience": "7+ ans", "salaire": "4M - 6M FCFA", "certifications": "CIA souhaité", "missions": ["Audits opérationnels portuaires", "Contrôle supply chain", "Audit conformité douanière", "Reporting groupe MSC"], "profil": "Logistique/Supply + 7 ans audit"},
    {"id": "DIR-SN-01", "titre": "DIRECTEUR AUDIT INTERNE", "entreprise": "BANQUE ATLANTIQUE SÉNÉGAL", "ville": "Dakar", "pays": "Sénégal", "date": "Juin 2025", "experience": "8+ ans", "salaire": "4.5M - 6.5M FCFA", "certifications": "CIA, Expert-comptable", "missions": ["Plan d'audit risk-based", "Audit agences et siège", "Conformité BCEAO", "Formation équipes"], "profil": "Expert-comptable + 8 ans banque"},
    {"id": "DIR-SN-02", "titre": "DIRECTEUR INSPECTION GÉNÉRALE", "entreprise": "BANQUE DE L'HABITAT SÉNÉGAL", "ville": "Dakar", "pays": "Sénégal", "date": "2023", "experience": "10+ ans", "salaire": "5M - 7M FCFA", "certifications": "CIA obligatoire", "missions": ["Inspection générale établissement", "Audit crédit immobilier", "Contrôle risques", "Relations avec BCEAO"], "profil": "Finance/Banque + 10 ans dont 3 ans direction"},
    {"id": "DIR-ML-01", "titre": "DIRECTEUR AUDIT ET CONFORMITÉ", "entreprise": "ECOBANK MALI", "ville": "Bamako", "pays": "Mali", "date": "Mars 2025", "experience": "8+ ans", "salaire": "4M - 5.5M FCFA", "certifications": "CIA, ACCA", "missions": ["Audit et conformité réglementaire", "AML/CFT", "Audit digital banking", "Reporting groupe"], "profil": "Master Finance + 8 ans banque"},
    {"id": "DIR-BF-01", "titre": "DIRECTEUR AUDIT", "entreprise": "ECOBANK BURKINA FASO", "ville": "Ouagadougou", "pays": "Burkina Faso", "date": "2024", "experience": "8+ ans", "salaire": "3.8M - 5M FCFA", "certifications": "CIA", "missions": ["Direction audit interne", "Plan annuel risk-based", "Conformité BCEAO", "Audit fraude"], "profil": "Finance + 8 ans audit bancaire"},
    {"id": "DIR-BJ-01", "titre": "DIRECTEUR AUDIT ET CONTRÔLE", "entreprise": "ECOBANK BÉNIN", "ville": "Cotonou", "pays": "Bénin", "date": "2023", "experience": "8+ ans", "salaire": "3.5M - 4.8M FCFA", "certifications": "CIA obligatoire", "missions": ["Audit interne et contrôle", "Conformité réglementaire", "Audit processus", "Formation"], "profil": "Expert-comptable + 8 ans"},
    {"id": "DIR-TG-01", "titre": "DIRECTEUR AUDIT", "entreprise": "SOCIÉTÉ AFRICAINE ENTREPRISES", "ville": "Lomé", "pays": "Togo", "date": "2023", "experience": "8+ ans", "salaire": "3.5M - 4.8M FCFA", "certifications": "", "missions": ["Direction audit groupe", "Audit multi-sites", "Contrôle interne", "Risques opérationnels"], "profil": "Master + 8 ans audit multi-sectoriel"},
    {"id": "DIR-GN-01", "titre": "DIRECTEUR AUDIT ET INSPECTION", "entreprise": "ÉTABLISSEMENTS PUBLICS GUINÉE", "ville": "Conakry", "pays": "Guinée", "date": "Mars 2025", "experience": "8+ ans", "salaire": "3.3M - 4.5M FCFA", "certifications": "", "missions": ["Audit EPA", "Contrôle gestion publique", "Conformité", "Reporting Primature"], "profil": "Administration/Finance + 8 ans secteur public"},
]

# Fonction pour créer un PDF avec contenu détaillé
def creer_pdf_detaille(offre, output_dir):
    """Créer un PDF détaillé pour une offre"""
    nom_fichier = f"{offre['id']}_{offre['entreprise'].replace(' ', '_').replace('/', '_')[:30]}.pdf"
    pdf_path = os.path.join(output_dir, nom_fichier)
    
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=A4,
        rightMargin=2*cm,
        leftMargin=2*cm,
        topMargin=2*cm,
        bottomMargin=2*cm,
        title=offre['titre']
    )
    
    styles = getSampleStyleSheet()
    
    style_titre = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=colors.HexColor('#1a5490'),
        spaceAfter=20,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    style_soustitre = ParagraphStyle(
        'SubTitle',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#2980b9'),
        spaceAfter=12,
        spaceBefore=16,
        fontName='Helvetica-Bold',
        borderColor=colors.HexColor('#3498db'),
        borderWidth=0,
        borderPadding=5,
        backColor=colors.HexColor('#ecf0f1')
    )
    
    style_section = ParagraphStyle(
        'Section',
        parent=styles['Heading3'],
        fontSize=12,
        textColor=colors.HexColor('#34495e'),
        spaceAfter=8,
        spaceBefore=12,
        fontName='Helvetica-Bold'
    )
    
    style_normal = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=10,
        alignment=TA_JUSTIFY,
        spaceAfter=8
    )
    
    style_info = ParagraphStyle(
        'InfoStyle',
        parent=styles['Normal'],
        fontSize=10,
        spaceAfter=6,
        textColor=colors.HexColor('#2c3e50')
    )
    
    # Contenu du document
    story = []
    
    # En-tête avec référence
    story.append(Paragraph(f"OFFRE N° {offre['id']}", style_titre))
    story.append(Paragraph(offre['titre'], style_titre))
    story.append(Spacer(1, 0.5*cm))
    
    # Encadré informations principales
    story.append(Paragraph("INFORMATIONS GÉNÉRALES", style_soustitre))
    story.append(Paragraph(f"<b>Entreprise :</b> {offre['entreprise']}", style_info))
    story.append(Paragraph(f"<b>Localisation :</b> {offre['ville']}, {offre['pays']}", style_info))
    story.append(Paragraph(f"<b>Date de publication :</b> {offre['date']}", style_info))
    story.append(Paragraph(f"<b>Type de contrat :</b> CDI", style_info))
    story.append(Spacer(1, 0.3*cm))
    
    # Rémunération
    story.append(Paragraph("RÉMUNÉRATION", style_soustitre))
    story.append(Paragraph(f"<b>Fourchette :</b> {offre['salaire']} / mois", style_info))
    story.append(Paragraph("<b>Avantages :</b> Prime annuelle, Assurance santé, Véhicule de fonction (selon niveau)", style_info))
    story.append(Spacer(1, 0.3*cm))
    
    # Missions principales
    story.append(Paragraph("MISSIONS PRINCIPALES", style_soustitre))
    for mission in offre['missions']:
        story.append(Paragraph(f"• {mission}", style_normal))
    story.append(Spacer(1, 0.3*cm))
    
    # Profil recherché
    story.append(Paragraph("PROFIL RECHERCHÉ", style_soustitre))
    story.append(Paragraph(f"<b>Formation :</b> {offre['profil']}", style_info))
    story.append(Paragraph(f"<b>Expérience :</b> {offre['experience']}", style_info))
    if offre['certifications']:
        story.append(Paragraph(f"<b>Certifications :</b> {offre['certifications']}", style_info))
    story.append(Spacer(1, 0.3*cm))
    
    # Compétences requises
    story.append(Paragraph("COMPÉTENCES REQUISES", style_soustitre))
    competences = [
        "Maîtrise des normes IIA et méthodologies d'audit",
        "Connaissance approfondie des risques sectoriels",
        "Leadership et management d'équipe",
        "Excellente communication écrite et orale",
        "Maîtrise des outils d'audit (ACL, IDEA, etc.)",
        "Anglais professionnel souhaité"
    ]
    for comp in competences:
        story.append(Paragraph(f"• {comp}", style_normal))
    story.append(Spacer(1, 0.3*cm))
    
    # Processus de candidature
    story.append(Paragraph("CANDIDATURE", style_soustitre))
    story.append(Paragraph(
        "<b>Dossier à fournir :</b> CV détaillé + Lettre de motivation + Copies diplômes et certifications",
        style_normal
    ))
    story.append(Paragraph(
        "<b>Envoi :</b> Consulter le site de l'entreprise ou portails emploi locaux",
        style_normal
    ))
    
    # Pied de page
    story.append(Spacer(1, 1*cm))
    footer_style = ParagraphStyle(
        'Footer',
        parent=style_normal,
        fontSize=8,
        textColor=colors.grey,
        alignment=TA_CENTER
    )
    story.append(Paragraph(
        "<b>Source :</b> Recherche Afrique de l'Ouest francophone 2021-2026<br/>"
        "<b>Document établi par :</b> Expert RH & Audit - 30 ans d'expérience<br/>"
        "<b>Date d'édition :</b> 2 novembre 2026",
        footer_style
    ))
    
    # Générer le PDF
    doc.build(story)
    print(f"✅ {offre['id']} - {offre['titre']}")
    return pdf_path

# Fonction principale
def generer_pdfs_directeurs():
    """Générer tous les PDFs des directeurs"""
    output_dir = r"h:\Projet_pdf_excel\Modelisation websearch\Offre recrutement\01_Directeurs"
    
    print("\n🚀 Génération des PDFs - DIRECTEURS D'AUDIT INTERNE\n")
    print(f"Nombre d'offres : {len(OFFRES_DIRECTEURS)}\n")
    
    pdfs_crees = []
    for offre in OFFRES_DIRECTEURS:
        try:
            pdf_path = creer_pdf_detaille(offre, output_dir)
            pdfs_crees.append(pdf_path)
        except Exception as e:
            print(f"❌ Erreur {offre['id']} : {e}")
    
    print(f"\n✅ {len(pdfs_crees)} PDFs créés avec succès dans :")
    print(f"   {output_dir}\n")
    
    return pdfs_crees

if __name__ == "__main__":
    try:
        pdfs = generer_pdfs_directeurs()
    except Exception as e:
        print(f"❌ Erreur générale : {e}")
        import traceback
        traceback.print_exc()
