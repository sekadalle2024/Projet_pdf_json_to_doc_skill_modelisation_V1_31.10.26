#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script de création PDF des offres d'emploi Directeurs Audit Interne
"""

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm, inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.platypus import Indenter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT

def creer_pdf_offres():
    """
    Créer un PDF professionnel avec les offres d'emploi
    """
    # Configuration du document
    pdf_file = r"h:\Projet_pdf_excel\Offres_Directeurs_Audit_Interne_CI.pdf"
    doc = SimpleDocTemplate(
        pdf_file,
        pagesize=A4,
        rightMargin=2*cm,
        leftMargin=2*cm,
        topMargin=2*cm,
        bottomMargin=2*cm,
        title="Offres Directeurs Audit Interne - Côte d'Ivoire"
    )
    
    # Styles
    styles = getSampleStyleSheet()
    
    # Style titre principal
    style_titre = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=20,
        textColor=colors.HexColor('#1a5490'),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    # Style titre offre
    style_offre = ParagraphStyle(
        'OfferTitle',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#2980b9'),
        spaceAfter=12,
        spaceBefore=20,
        fontName='Helvetica-Bold',
        leftIndent=10,
        borderColor=colors.HexColor('#3498db'),
        borderWidth=3,
        borderPadding=8
    )
    
    # Style sous-titre
    style_soustitre = ParagraphStyle(
        'SubTitle',
        parent=styles['Heading3'],
        fontSize=12,
        textColor=colors.HexColor('#34495e'),
        spaceAfter=6,
        spaceBefore=12,
        fontName='Helvetica-Bold'
    )
    
    # Style normal
    style_normal = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=10,
        alignment=TA_JUSTIFY,
        spaceAfter=8
    )
    
    # Contenu du document
    story = []
    
    # Page de titre
    story.append(Paragraph("TOP 10 - OFFRES D'EMPLOI", style_titre))
    story.append(Paragraph("DIRECTEURS & RESPONSABLES AUDIT INTERNE", style_titre))
    story.append(Paragraph("CÔTE D'IVOIRE - 2026", style_titre))
    story.append(Spacer(1, 1*cm))
    story.append(PageBreak())
    
    # OFFRE #1
    story.append(Paragraph("OFFRE #1 : CHEF DE MISSION AUDIT INTERNE", style_offre))
    story.append(Paragraph("<b>Entreprise :</b> NSIA ASSURANCES", style_normal))
    story.append(Paragraph("<b>Localisation :</b> Abidjan, Côte d'Ivoire", style_normal))
    story.append(Paragraph("<b>Type de contrat :</b> CDI", style_normal))
    
    story.append(Paragraph("RAISON D'ÊTRE", style_soustitre))
    story.append(Paragraph(
        "Contribuer à la réduction des pertes opérationnelles de la banque et fournir les conseils nécessaires "
        "aux différents domaines de gestion afin de protéger les résultats acquis et d'améliorer les processus "
        "internes et de management des risques.",
        style_normal
    ))
    
    story.append(Paragraph("MISSIONS PRINCIPALES", style_soustitre))
    missions = [
        "Mettre en œuvre le programme d'audit annuel",
        "Animer et coordonner les activités d'audit",
        "Organiser et superviser les ressources allouées",
        "Vérifier la conformité aux procédures internes"
    ]
    for mission in missions:
        story.append(Paragraph(f"• {mission}", style_normal))
    
    story.append(Paragraph("PROFIL RECHERCHÉ", style_soustitre))
    story.append(Paragraph(
        "<b>Formation :</b> BAC+4/5 en Finance, Comptabilité, Audit ou Contrôle de gestion",
        style_normal
    ))
    story.append(Paragraph(
        "<b>Certifications :</b> CIA, CFE, FRM, ACAMS (atout)",
        style_normal
    ))
    story.append(Paragraph(
        "<b>Expérience :</b> 3 ans minimum dans la fonction d'auditeur interne",
        style_normal
    ))
    story.append(Paragraph(
        "<b>Langues :</b> Bon niveau en anglais (lu, écrit et parlé)",
        style_normal
    ))
    
    story.append(Paragraph("CANDIDATURE", style_soustitre))
    story.append(Paragraph("<b>Email :</b> [email protected]", style_normal))
    story.append(Paragraph("<b>Date limite :</b> 11 avril 2025", style_normal))
    story.append(PageBreak())
    
    # OFFRE #2
    story.append(Paragraph("OFFRE #2 : DIRECTEUR AUDIT", style_offre))
    story.append(Paragraph("<b>Entreprise :</b> YESHI GROUP", style_normal))
    story.append(Paragraph("<b>Localisation :</b> Côte d'Ivoire", style_normal))
    story.append(Paragraph("<b>Niveau :</b> Cadre dirigeant (Plus de 10 ans)", style_normal))
    
    story.append(Paragraph("PROFIL RECHERCHÉ", style_soustitre))
    story.append(Paragraph(
        "<b>Expérience :</b> Plus de 10 ans dans l'audit et le contrôle interne",
        style_normal
    ))
    story.append(Paragraph(
        "<b>Secteur :</b> Multi-sectoriel (Industrie, Services)",
        style_normal
    ))
    
    story.append(Paragraph("COMPÉTENCES CLÉS", style_soustitre))
    competences = [
        "Direction et management d'équipes d'audit",
        "Élaboration de la stratégie d'audit",
        "Gestion des risques opérationnels et financiers",
        "Normes internationales d'audit"
    ]
    for comp in competences:
        story.append(Paragraph(f"• {comp}", style_normal))
    story.append(PageBreak())
    
    # OFFRE #3
    story.append(Paragraph("OFFRE #3 : AUDITEUR INTERNE (H/F)", style_offre))
    story.append(Paragraph("<b>Entreprise :</b> CORIS BANK INTERNATIONAL", style_normal))
    story.append(Paragraph("<b>Localisation :</b> Abidjan, Côte d'Ivoire", style_normal))
    story.append(Paragraph("<b>Type de contrat :</b> CDI", style_normal))
    
    story.append(Paragraph("MISSIONS", style_soustitre))
    missions_coris = [
        "Contrôle du respect des règles et procédures internes",
        "Vérification de la conformité réglementaire",
        "Contrôle des usages professionnels et déontologiques",
        "Suivi des orientations stratégiques de la banque"
    ]
    for mission in missions_coris:
        story.append(Paragraph(f"• {mission}", style_normal))
    
    story.append(Paragraph("PROFIL", style_soustitre))
    story.append(Paragraph(
        "<b>Formation :</b> BAC+4/5 en Audit, Finance, Comptabilité",
        style_normal
    ))
    story.append(Paragraph(
        "<b>Expérience :</b> 2 à 5 ans en audit bancaire",
        style_normal
    ))
    story.append(PageBreak())
    
    # OFFRE #4
    story.append(Paragraph("OFFRE #4 : AUDITEUR INTERNE JUNIOR", style_offre))
    story.append(Paragraph("<b>Entreprise :</b> SIKA FINANCE", style_normal))
    story.append(Paragraph("<b>Localisation :</b> Abidjan, Côte d'Ivoire", style_normal))
    
    story.append(Paragraph("ACTIVITÉS PRINCIPALES", style_soustitre))
    activites = [
        "Assurer la qualité du contrôle interne",
        "Élaborer la charte éthique",
        "Préparer et exécuter les missions d'audit",
        "Rédiger les rapports d'audit",
        "Suivre les recommandations"
    ]
    for act in activites:
        story.append(Paragraph(f"• {act}", style_normal))
    
    story.append(Paragraph("PROFIL", style_soustitre))
    story.append(Paragraph(
        "<b>Formation :</b> BAC+4/5 en Audit, Économie, Banque, Finance",
        style_normal
    ))
    story.append(Paragraph(
        "<b>Expérience :</b> 1 an minimum en Audit et Contrôle Interne",
        style_normal
    ))
    story.append(PageBreak())
    
    # OFFRE #5
    story.append(Paragraph("OFFRE #5 : AUDITEUR INTERNE JUNIOR", style_offre))
    story.append(Paragraph("<b>Entreprise :</b> CBAO (Groupe Attijariwafa Bank)", style_normal))
    story.append(Paragraph("<b>Localisation :</b> Abidjan, Côte d'Ivoire", style_normal))
    
    story.append(Paragraph("À PROPOS", style_soustitre))
    story.append(Paragraph(
        "CBAO, fondée en 1853, premier Groupe Bancaire du Maghreb avec 88 agences, "
        "400 000 clients et 1000 collaborateurs.",
        style_normal
    ))
    
    story.append(Paragraph("MISSIONS", style_soustitre))
    missions_cbao = [
        "Évaluer les dispositifs de maîtrise des risques",
        "Évaluer la conformité des processus",
        "Rédiger les rapports de mission",
        "Suivre les recommandations",
        "Réaliser des travaux méthodologiques"
    ]
    for mission in missions_cbao:
        story.append(Paragraph(f"• {mission}", style_normal))
    
    story.append(Paragraph("PROFIL", style_soustitre))
    story.append(Paragraph(
        "<b>Formation :</b> BAC+4/5 en Audit, Contrôle de Gestion, Finance",
        style_normal
    ))
    story.append(Paragraph(
        "<b>Expérience :</b> 1 à 3 ans en Banque ou cabinet d'Audit",
        style_normal
    ))
    story.append(PageBreak())
    
    # OFFRE #6
    story.append(Paragraph("OFFRE #6 : AUDITEUR INTERNE SENIOR", style_offre))
    story.append(Paragraph("<b>Entreprise :</b> ELITE INTERIM CI", style_normal))
    story.append(Paragraph("<b>Secteur :</b> Industrie", style_normal))
    story.append(Paragraph("<b>Niveau :</b> Manager (6 à 10 ans)", style_normal))
    
    story.append(Paragraph("COMPÉTENCES", style_soustitre))
    competences_elite = [
        "Audit des processus industriels",
        "Contrôle de gestion industrielle",
        "Normes ISO et qualité",
        "Gestion des risques industriels"
    ]
    for comp in competences_elite:
        story.append(Paragraph(f"• {comp}", style_normal))
    story.append(PageBreak())
    
    # OFFRE #7
    story.append(Paragraph("OFFRE #7 : HEAD OF INTERNAL AUDIT", style_offre))
    story.append(Paragraph("<b>Entreprise :</b> TEAMACE", style_normal))
    story.append(Paragraph("<b>Localisation :</b> Afrique de l'Ouest", style_normal))
    
    story.append(Paragraph("MISSIONS", style_soustitre))
    missions_head = [
        "Développer les plans d'audit basés sur les risques",
        "Réviser les contrôles internes",
        "Maintenir la charte d'audit",
        "Assurer l'efficacité des audits"
    ]
    for mission in missions_head:
        story.append(Paragraph(f"• {mission}", style_normal))
    
    story.append(Paragraph("PROFIL", style_soustitre))
    story.append(Paragraph(
        "<b>Expérience :</b> 8 ans minimum dont 3 ans en management",
        style_normal
    ))
    story.append(Paragraph(
        "<b>Certifications :</b> CIA, ACCA, CPA souhaité",
        style_normal
    ))
    story.append(PageBreak())
    
    # OFFRE #8
    story.append(Paragraph("OFFRE #8 : INTERNAL CONTROL AND AUDIT", style_offre))
    story.append(Paragraph("<b>Entreprise :</b> CARDINALSTONE REGISTRARS", style_normal))
    story.append(Paragraph("<b>Secteur :</b> Services financiers", style_normal))
    
    story.append(Paragraph("RESPONSABILITÉS", style_soustitre))
    responsabilites = [
        "Conception du plan d'audit annuel",
        "Audits périodiques des unités",
        "Évaluation des risques",
        "Reporting à la direction générale"
    ]
    for resp in responsabilites:
        story.append(Paragraph(f"• {resp}", style_normal))
    
    story.append(Paragraph("PROFIL", style_soustitre))
    story.append(Paragraph(
        "<b>Expérience :</b> 5 à 8 ans en audit interne",
        style_normal
    ))
    story.append(PageBreak())
    
    # OFFRE #9
    story.append(Paragraph("OFFRE #9 : INTERNAL AUDIT PARTNER", style_offre))
    story.append(Paragraph("<b>Entreprise :</b> RENMONEY", style_normal))
    story.append(Paragraph("<b>Secteur :</b> FinTech / Services financiers", style_normal))
    
    story.append(Paragraph("MISSIONS", style_soustitre))
    missions_partner = [
        "Évaluation des risques",
        "Auditer selon le plan d'audit",
        "Suivre les recommandations",
        "Implémenter les contrôles"
    ]
    for mission in missions_partner:
        story.append(Paragraph(f"• {mission}", style_normal))
    
    story.append(Paragraph("PROFIL", style_soustitre))
    story.append(Paragraph(
        "<b>Expérience :</b> 7 ans minimum en audit",
        style_normal
    ))
    story.append(Paragraph(
        "<b>Niveau :</b> Partner / Associé",
        style_normal
    ))
    story.append(PageBreak())
    
    # OFFRE #10
    story.append(Paragraph("OFFRE #10 : AUDITEUR QUALITÉ INTERNE", style_offre))
    story.append(Paragraph("<b>Entreprise :</b> NSIA BANQUE", style_normal))
    story.append(Paragraph("<b>Localisation :</b> Abidjan, Côte d'Ivoire", style_normal))
    
    story.append(Paragraph("MISSIONS", style_soustitre))
    missions_qualite = [
        "Réaliser les audits qualité internes",
        "Évaluer la conformité aux normes ISO",
        "Proposer des actions correctives",
        "Former les équipes",
        "Suivre les indicateurs de performance"
    ]
    for mission in missions_qualite:
        story.append(Paragraph(f"• {mission}", style_normal))
    
    story.append(Paragraph("PROFIL", style_soustitre))
    story.append(Paragraph(
        "<b>Formation :</b> BAC+4/5 en Qualité",
        style_normal
    ))
    story.append(Paragraph(
        "<b>Expérience :</b> 3 ans en audit ou qualité",
        style_normal
    ))
    story.append(Paragraph(
        "<b>Compétences :</b> Normes ISO 9001, 27001",
        style_normal
    ))
    story.append(PageBreak())
    
    # Page finale - Informations complémentaires
    story.append(Paragraph("INFORMATIONS COMPLÉMENTAIRES", style_titre))
    
    story.append(Paragraph("SALAIRES MOYENS (INDICATIF)", style_soustitre))
    
    # Tableau des salaires
    data_salaires = [
        ['Poste', 'Salaire mensuel (FCFA)'],
        ['Directeur Audit Interne', '3 500 000 - 8 000 000'],
        ['Chef de Mission Audit', '2 000 000 - 4 500 000'],
        ['Auditeur Senior', '1 500 000 - 3 000 000'],
        ['Auditeur Junior', '800 000 - 1 500 000']
    ]
    
    table_salaires = Table(data_salaires, colWidths=[7*cm, 7*cm])
    table_salaires.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498db')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
    ]))
    story.append(table_salaires)
    story.append(Spacer(1, 0.5*cm))
    
    story.append(Paragraph("CERTIFICATIONS VALORISÉES", style_soustitre))
    certifications = [
        "CIA (Certified Internal Auditor)",
        "ACCA (Chartered Certified Accountants)",
        "CFE (Certified Fraud Examiner)",
        "FRM (Financial Risk Manager)",
        "ACAMS (Anti-Money Laundering)",
        "CISA (Information Systems Auditor)"
    ]
    for cert in certifications:
        story.append(Paragraph(f"• {cert}", style_normal))
    
    story.append(Paragraph("SECTEURS QUI RECRUTENT", style_soustitre))
    secteurs = [
        "Banques (NSIA, CBAO, Coris Bank, BOA)",
        "Assurances (NSIA Assurances, AXA, Allianz)",
        "Industrie (Agroalimentaire, Cimenterie)",
        "Services financiers (FinTech, Microfinance)",
        "Télécommunications (Orange CI, MTN)"
    ]
    for secteur in secteurs:
        story.append(Paragraph(f"• {secteur}", style_normal))
    
    story.append(Spacer(1, 0.5*cm))
    story.append(Paragraph("SITES WEB RECOMMANDÉS", style_soustitre))
    sites = [
        "www.emploi.ci - Portail officiel",
        "www.novojob.com - Multi-secteurs",
        "www.educarriere.ci - Emplois qualifiés",
        "www.sikafinance.com - Finance/Banque",
        "LinkedIn - Réseau professionnel"
    ]
    for site in sites:
        story.append(Paragraph(f"• {site}", style_normal))
    
    story.append(Spacer(1, 1*cm))
    story.append(Paragraph(
        "<b>Document compilé le 2 novembre 2026</b><br/>"
        "Source : Recherche web multi-sources<br/>"
        "Expert Audit & RH - 30 ans d'expérience",
        ParagraphStyle('Footer', parent=style_normal, fontSize=9, textColor=colors.grey, alignment=TA_CENTER)
    ))
    
    # Générer le PDF
    doc.build(story)
    print(f"✅ PDF créé avec succès : {pdf_file}")
    return pdf_file

if __name__ == "__main__":
    try:
        pdf_file = creer_pdf_offres()
        print(f"\n📄 Fichier PDF disponible : {pdf_file}")
    except Exception as e:
        print(f"❌ Erreur : {e}")
        import traceback
        traceback.print_exc()
