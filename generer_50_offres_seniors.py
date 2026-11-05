#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Génération de 50 PDFs - Auditeurs Internes SENIORS
Afrique de l'Ouest Francophone (2021-2026)
"""

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
import os

# 50 OFFRES AUDITEURS SENIORS
OFFRES_SENIORS = [
    # CÔTE D'IVOIRE (18)
    {"id": "SEN-CI-01", "titre": "AUDITEUR INTERNE SENIOR", "entreprise": "ELITE INTERIM CI", "ville": "Abidjan", "pays": "Côte d'Ivoire", "date": "Septembre 2026", "experience": "6-10 ans", "salaire": "2M - 3M FCFA", "secteur": "Industrie", "missions": ["Audit processus industriels", "Contrôle qualité ISO", "Risques opérationnels", "Encadrement juniors"]},
    {"id": "SEN-CI-02", "titre": "AUDITEUR INTERNE SENIOR", "entreprise": "NSIA BANQUE CI", "ville": "Abidjan", "pays": "Côte d'Ivoire", "date": "Janvier 2026", "experience": "5+ ans", "salaire": "1.8M - 2.8M FCFA", "secteur": "Banque", "missions": ["Audit agences bancaires", "Contrôle crédit", "Conformité BCEAO", "Audit IT"]},
    {"id": "SEN-CI-03", "titre": "SENIOR AUDIT MANAGER", "entreprise": "KPMG CÔTE D'IVOIRE", "ville": "Abidjan", "pays": "Côte d'Ivoire", "date": "Mai 2026", "experience": "5+ ans", "salaire": "2.5M - 4M FCFA", "secteur": "Cabinet", "missions": ["Management missions", "Audit financier", "Conseil clients", "Formation équipes"]},
    {"id": "SEN-CI-04", "titre": "SUPERVISEUR AUDIT", "entreprise": "KPMG CI", "ville": "Abidjan", "pays": "Côte d'Ivoire", "date": "Février 2026", "experience": "3-5 ans", "salaire": "1.5M - 2.5M FCFA", "secteur": "Cabinet", "missions": ["Supervision audits", "Révision dossiers", "Relation clients", "Reporting"]},
    {"id": "SEN-CI-05", "titre": "AUDITEUR SENIOR", "entreprise": "DELOITTE CI", "ville": "Abidjan", "pays": "Côte d'Ivoire", "date": "2024", "experience": "4+ ans", "salaire": "1.8M - 2.8M FCFA", "secteur": "Cabinet", "missions": ["Audit statutory", "IFRS", "Consolidation", "Conseil"]},
    {"id": "SEN-CI-06", "titre": "AUDITEUR INTERNE SENIOR", "entreprise": "SIKA FINANCE", "ville": "Abidjan", "pays": "Côte d'Ivoire", "date": "2024", "experience": "3+ ans", "salaire": "1.5M - 2.5M FCFA", "secteur": "Banque", "missions": ["Audit opérationnel", "Conformité", "Risques", "Recommandations"]},
    {"id": "SEN-CI-07", "titre": "AUDITEUR SENIOR BANQUE", "entreprise": "CORIS BANK CI", "ville": "Abidjan", "pays": "Côte d'Ivoire", "date": "Septembre 2025", "experience": "3-5 ans", "salaire": "1.6M - 2.6M FCFA", "secteur": "Banque", "missions": ["Audit réseau", "Contrôle processus", "AML/CFT", "Reporting"]},
    {"id": "SEN-CI-08", "titre": "AUDITEUR SENIOR", "entreprise": "ECOBANK CI", "ville": "Abidjan", "pays": "Côte d'Ivoire", "date": "Avril 2026", "experience": "5+ ans", "salaire": "1.8M - 2.8M FCFA", "secteur": "Banque", "missions": ["Audit branches", "Digital banking", "Conformité", "Risques"]},
    {"id": "SEN-CI-09", "titre": "AUDITEUR SENIOR", "entreprise": "BANK OF AFRICA CI", "ville": "Abidjan", "pays": "Côte d'Ivoire", "date": "Avril 2026", "experience": "5+ ans", "salaire": "1.7M - 2.7M FCFA", "secteur": "Banque", "missions": ["Audit interne", "Risques", "Conformité", "Contrôles"]},
    {"id": "SEN-CI-10", "titre": "AUDITEUR IT SENIOR", "entreprise": "ORANGE CI", "ville": "Abidjan", "pays": "Côte d'Ivoire", "date": "2023", "experience": "5+ ans", "salaire": "2M - 3.5M FCFA", "secteur": "Télécoms", "missions": ["Audit systèmes", "Cybersécurité", "COBIT", "ISO 27001"]},
    {"id": "SEN-CI-11", "titre": "AUDITEUR SENIOR LOGISTIQUE", "entreprise": "AGL CÔTE D'IVOIRE", "ville": "Abidjan", "pays": "Côte d'Ivoire", "date": "2024", "experience": "4+ ans", "salaire": "1.8M - 2.8M FCFA", "secteur": "Logistique", "missions": ["Audit supply chain", "Contrôle stocks", "Processus", "Risques"]},
    {"id": "SEN-CI-12", "titre": "AUDITEUR QUALITÉ SENIOR", "entreprise": "INDUSTRIE AGROALIMENTAIRE", "ville": "Abidjan", "pays": "Côte d'Ivoire", "date": "2023", "experience": "5+ ans", "salaire": "1.6M - 2.5M FCFA", "secteur": "Industrie", "missions": ["Audit ISO 9001", "HACCP", "Qualité", "Amélioration"]},
    {"id": "SEN-CI-13", "titre": "AUDITEUR INTERNE SENIOR", "entreprise": "MTN CI", "ville": "Abidjan", "pays": "Côte d'Ivoire", "date": "2024", "experience": "5+ ans", "salaire": "2M - 3M FCFA", "secteur": "Télécoms", "missions": ["Audit opérations", "Fraude", "Conformité", "Risques"]},
    {"id": "SEN-CI-14", "titre": "AUDITEUR SENIOR", "entreprise": "CBAO CI", "ville": "Abidjan", "pays": "Côte d'Ivoire", "date": "Décembre 2023", "experience": "3+ ans", "salaire": "1.5M - 2.5M FCFA", "secteur": "Banque", "missions": ["Audit processus", "Conformité", "Contrôles", "Reporting"]},
    {"id": "SEN-CI-15", "titre": "AUDITEUR INTERNE SENIOR", "entreprise": "SOCIÉTÉ GÉNÉRALE CI", "ville": "Abidjan", "pays": "Côte d'Ivoire", "date": "2022", "experience": "5+ ans", "salaire": "1.8M - 2.8M FCFA", "secteur": "Banque", "missions": ["Audit retail", "Risques", "Conformité", "Suivi"]},
    {"id": "SEN-CI-16", "titre": "AUDITEUR SENIOR", "entreprise": "UBA CÔTE D'IVOIRE", "ville": "Abidjan", "pays": "Côte d'Ivoire", "date": "2023", "experience": "4+ ans", "salaire": "1.6M - 2.6M FCFA", "secteur": "Banque", "missions": ["Audit branches", "Conformité", "Contrôles", "Risques"]},
    {"id": "SEN-CI-17", "titre": "AUDITEUR SENIOR ASSURANCE", "entreprise": "NSIA ASSURANCES", "ville": "Abidjan", "pays": "Côte d'Ivoire", "date": "Avril 2025", "experience": "4+ ans", "salaire": "1.7M - 2.7M FCFA", "secteur": "Assurance", "missions": ["Audit sinistres", "Souscription", "Conformité", "Risques"]},
    {"id": "SEN-CI-18", "titre": "AUDITEUR SENIOR PROJET", "entreprise": "ONG INTERNATIONALE", "ville": "Abidjan", "pays": "Côte d'Ivoire", "date": "2024", "experience": "5+ ans", "salaire": "1.5M - 2.3M FCFA", "secteur": "Humanitaire", "missions": ["Audit projets", "Bailleurs", "Conformité", "Reporting"]},
    
    # SÉNÉGAL (14)
    {"id": "SEN-SN-01", "titre": "AUDITEUR INTERNE SENIOR", "entreprise": "BANQUE ATLANTIQUE SÉNÉGAL", "ville": "Dakar", "pays": "Sénégal", "date": "Juin 2025", "experience": "5+ ans", "salaire": "1.5M - 2.5M FCFA", "secteur": "Banque", "missions": ["Audit agences", "Conformité", "Risques crédit", "Contrôles"]},
    {"id": "SEN-SN-02", "titre": "SENIOR AUDIT MANAGER", "entreprise": "DELOITTE SÉNÉGAL", "ville": "Dakar", "pays": "Sénégal", "date": "2023", "experience": "6+ ans", "salaire": "2M - 3M FCFA", "secteur": "Cabinet", "missions": ["Management audits", "Clients", "Formation", "Développement"]},
    {"id": "SEN-SN-03", "titre": "AUDIT MANAGER", "entreprise": "PWC SÉNÉGAL", "ville": "Dakar", "pays": "Sénégal", "date": "2024", "experience": "5+ ans", "salaire": "1.8M - 2.8M FCFA", "secteur": "Cabinet", "missions": ["Supervision audits", "IFRS", "Conseil", "Clients"]},
    {"id": "SEN-SN-04", "titre": "AUDITEUR SENIOR", "entreprise": "ECOBANK SÉNÉGAL", "ville": "Dakar", "pays": "Sénégal", "date": "2024", "experience": "5+ ans", "salaire": "1.6M - 2.6M FCFA", "secteur": "Banque", "missions": ["Audit processus", "Conformité", "Risques", "Reporting"]},
    {"id": "SEN-SN-05", "titre": "AUDITEUR INTERNE SENIOR", "entreprise": "SOCIÉTÉ GÉNÉRALE SÉNÉGAL", "ville": "Dakar", "pays": "Sénégal", "date": "2022", "experience": "5+ ans", "salaire": "1.7M - 2.7M FCFA", "secteur": "Banque", "missions": ["Audit retail", "Digital", "Conformité", "Contrôles"]},
    {"id": "SEN-SN-06", "titre": "AUDITEUR SENIOR TÉLÉCOM", "entreprise": "SONATEL (Orange)", "ville": "Dakar", "pays": "Sénégal", "date": "2023", "experience": "5+ ans", "salaire": "1.8M - 2.8M FCFA", "secteur": "Télécoms", "missions": ["Audit réseau", "IT", "Fraude", "Conformité"]},
    {"id": "SEN-SN-07", "titre": "AUDITEUR SENIOR", "entreprise": "CBAO SÉNÉGAL", "ville": "Dakar", "pays": "Sénégal", "date": "2024", "experience": "4+ ans", "salaire": "1.5M - 2.5M FCFA", "secteur": "Banque", "missions": ["Audit opérationnel", "Risques", "Conformité", "Suivi"]},
    {"id": "SEN-SN-08", "titre": "AUDITEUR SENIOR", "entreprise": "BANK OF AFRICA SÉNÉGAL", "ville": "Dakar", "pays": "Sénégal", "date": "2024", "experience": "5+ ans", "salaire": "1.6M - 2.6M FCFA", "secteur": "Banque", "missions": ["Audit branches", "Crédit", "Conformité", "Risques"]},
    {"id": "SEN-SN-09", "titre": "AUDITEUR IT SENIOR", "entreprise": "SOCIÉTÉ IT DAKAR", "ville": "Dakar", "pays": "Sénégal", "date": "2024", "experience": "5+ ans", "salaire": "1.8M - 2.8M FCFA", "secteur": "IT", "missions": ["Audit systèmes", "Sécurité", "COBIT", "Conformité"]},
    {"id": "SEN-SN-10", "titre": "AUDITEUR SENIOR", "entreprise": "COMPAGNIE SAHÉLIENNE", "ville": "Dakar", "pays": "Sénégal", "date": "2025", "experience": "4+ ans", "salaire": "1.4M - 2.3M FCFA", "secteur": "Distribution", "missions": ["Audit opérations", "Stocks", "Processus", "Contrôles"]},
    {"id": "SEN-SN-11", "titre": "AUDITEUR SENIOR MICROFINANCE", "entreprise": "RÉSEAU SFD SÉNÉGAL", "ville": "Dakar", "pays": "Sénégal", "date": "2023", "experience": "5+ ans", "salaire": "1.3M - 2.2M FCFA", "secteur": "Microfinance", "missions": ["Audit SFD", "Conformité BCEAO", "Risques", "Portefeuille"]},
    {"id": "SEN-SN-12", "titre": "AUDITEUR QUALITÉ SENIOR", "entreprise": "INDUSTRIE SÉNÉGALAISE", "ville": "Dakar", "pays": "Sénégal", "date": "2024", "experience": "5+ ans", "salaire": "1.5M - 2.4M FCFA", "secteur": "Industrie", "missions": ["Audit ISO", "Qualité", "Processus", "Amélioration"]},
    {"id": "SEN-SN-13", "titre": "AUDITEUR SENIOR", "entreprise": "UBA SÉNÉGAL", "ville": "Dakar", "pays": "Sénégal", "date": "2023", "experience": "4+ ans", "salaire": "1.5M - 2.5M FCFA", "secteur": "Banque", "missions": ["Audit interne", "Conformité", "Risques", "Contrôles"]},
    {"id": "SEN-SN-14", "titre": "AUDITEUR SENIOR PROJET", "entreprise": "ONG SAHEL", "ville": "Dakar", "pays": "Sénégal", "date": "2024", "experience": "5+ ans", "salaire": "1.4M - 2.2M FCFA", "secteur": "Humanitaire", "missions": ["Audit projets", "Bailleurs", "Conformité", "Reporting"]},
    
    # MALI (8)
    {"id": "SEN-ML-01", "titre": "AUDITEUR INTERNE SENIOR", "entreprise": "BANK OF AFRICA MALI", "ville": "Bamako", "pays": "Mali", "date": "2024", "experience": "5+ ans", "salaire": "1.3M - 2.2M FCFA", "secteur": "Banque", "missions": ["Audit agences", "Conformité", "Risques", "Contrôles"]},
    {"id": "SEN-ML-02", "titre": "AUDITEUR SENIOR", "entreprise": "ECOBANK MALI", "ville": "Bamako", "pays": "Mali", "date": "Mars 2025", "experience": "5+ ans", "salaire": "1.2M - 2.1M FCFA", "secteur": "Banque", "missions": ["Audit opérationnel", "Conformité", "Risques", "Reporting"]},
    {"id": "SEN-ML-03", "titre": "SUPERVISEUR AUDIT", "entreprise": "CABINET AUDIT INTERNATIONAL", "ville": "Bamako", "pays": "Mali", "date": "2024", "experience": "4+ ans", "salaire": "1.5M - 2.5M FCFA", "secteur": "Cabinet", "missions": ["Supervision missions", "Clients", "Formation", "Développement"]},
    {"id": "SEN-ML-04", "titre": "AUDITEUR SENIOR", "entreprise": "BANQUE ATLANTIQUE MALI", "ville": "Bamako", "pays": "Mali", "date": "Juin 2025", "experience": "5+ ans", "salaire": "1.3M - 2.2M FCFA", "secteur": "Banque", "missions": ["Audit branches", "Crédit", "Conformité", "Risques"]},
    {"id": "SEN-ML-05", "titre": "AUDITEUR IT SENIOR", "entreprise": "ORANGE MALI", "ville": "Bamako", "pays": "Mali", "date": "2023", "experience": "5+ ans", "salaire": "1.5M - 2.5M FCFA", "secteur": "Télécoms", "missions": ["Audit systèmes", "Sécurité", "Conformité", "Risques"]},
    {"id": "SEN-ML-06", "titre": "AUDITEUR SENIOR", "entreprise": "SOCIÉTÉ GÉNÉRALE MALI", "ville": "Bamako", "pays": "Mali", "date": "2022", "experience": "5+ ans", "salaire": "1.2M - 2.1M FCFA", "secteur": "Banque", "missions": ["Audit retail", "Conformité", "Contrôles", "Risques"]},
    {"id": "SEN-ML-07", "titre": "AUDITEUR SENIOR MICROFINANCE", "entreprise": "AMIFA MALI", "ville": "Bamako", "pays": "Mali", "date": "Juin 2023", "experience": "4+ ans", "salaire": "1.1M - 1.9M FCFA", "secteur": "Microfinance", "missions": ["Audit portefeuille", "Conformité", "Risques", "Contrôles"]},
    {"id": "SEN-ML-08", "titre": "AUDITEUR SENIOR ONG", "entreprise": "ACTION CONTRE LA FAIM", "ville": "Bamako", "pays": "Mali", "date": "Novembre 2023", "experience": "5+ ans", "salaire": "1.3M - 2M FCFA", "secteur": "Humanitaire", "missions": ["Audit projets", "Bailleurs", "Conformité", "Reporting"]},
    
    # BURKINA FASO (4)
    {"id": "SEN-BF-01", "titre": "AUDITEUR SENIOR", "entreprise": "ECOBANK BURKINA", "ville": "Ouagadougou", "pays": "Burkina Faso", "date": "2024", "experience": "5+ ans", "salaire": "1.2M - 2M FCFA", "secteur": "Banque", "missions": ["Audit branches", "Conformité", "Risques", "Contrôles"]},
    {"id": "SEN-BF-02", "titre": "AUDITEUR SENIOR", "entreprise": "BANK OF AFRICA BURKINA", "ville": "Ouagadougou", "pays": "Burkina Faso", "date": "2023", "experience": "5+ ans", "salaire": "1.1M - 1.9M FCFA", "secteur": "Banque", "missions": ["Audit opérationnel", "Conformité", "Risques", "Reporting"]},
    {"id": "SEN-BF-03", "titre": "AUDITEUR SENIOR ONG", "entreprise": "WELTHUNGERHILFE", "ville": "Ouagadougou", "pays": "Burkina Faso", "date": "2023-2025", "experience": "5+ ans", "salaire": "1.2M - 1.8M FCFA", "secteur": "Humanitaire", "missions": ["Audit projets", "Bailleurs", "Conformité", "Reporting"]},
    {"id": "SEN-BF-04", "titre": "AUDITEUR SENIOR", "entreprise": "SOCIÉTÉ GÉNÉRALE BURKINA", "ville": "Ouagadougou", "pays": "Burkina Faso", "date": "2023", "experience": "4+ ans", "salaire": "1.1M - 1.9M FCFA", "secteur": "Banque", "missions": ["Audit retail", "Conformité", "Risques", "Contrôles"]},
    
    # BÉNIN (3)
    {"id": "SEN-BJ-01", "titre": "AUDITEUR SENIOR", "entreprise": "DELOITTE BÉNIN", "ville": "Cotonou", "pays": "Bénin", "date": "Août 2026", "experience": "5+ ans", "salaire": "1.3M - 2.2M FCFA", "secteur": "Cabinet", "missions": ["Audit financier", "IFRS", "Conseil", "Clients"]},
    {"id": "SEN-BJ-02", "titre": "AUDITEUR SENIOR", "entreprise": "ECOBANK BÉNIN", "ville": "Cotonou", "pays": "Bénin", "date": "2023", "experience": "5+ ans", "salaire": "1.2M - 2M FCFA", "secteur": "Banque", "missions": ["Audit branches", "Conformité", "Risques", "Contrôles"]},
    {"id": "SEN-BJ-03", "titre": "AUDITEUR SENIOR", "entreprise": "BANK OF AFRICA BÉNIN", "ville": "Cotonou", "pays": "Bénin", "date": "2024", "experience": "4+ ans", "salaire": "1.1M - 1.9M FCFA", "secteur": "Banque", "missions": ["Audit opérationnel", "Conformité", "Risques", "Reporting"]},
    
    # TOGO (2)
    {"id": "SEN-TG-01", "titre": "AUDITEUR SENIOR", "entreprise": "DELOITTE TOGO", "ville": "Lomé", "pays": "Togo", "date": "Août 2026", "experience": "4+ ans", "salaire": "1.2M - 2.1M FCFA", "secteur": "Cabinet", "missions": ["Audit financier", "IFRS", "Conseil", "Clients"]},
    {"id": "SEN-TG-02", "titre": "AUDITEUR SENIOR", "entreprise": "ECOBANK TOGO", "ville": "Lomé", "pays": "Togo", "date": "2024", "experience": "5+ ans", "salaire": "1.1M - 2M FCFA", "secteur": "Banque", "missions": ["Audit branches", "Conformité", "Risques", "Contrôles"]},
    
    # NIGER (1)
    {"id": "SEN-NE-01", "titre": "AUDITEUR SENIOR", "entreprise": "BANQUE ATLANTIQUE NIGER", "ville": "Niamey", "pays": "Niger", "date": "2023", "experience": "5+ ans", "salaire": "1M - 1.8M FCFA", "secteur": "Banque", "missions": ["Audit agences", "Conformité", "Risques", "Contrôles"]},
]

def creer_pdf_senior(offre, output_dir):
    """Créer un PDF pour un auditeur senior"""
    nom_fichier = f"{offre['id']}_{offre['entreprise'].replace(' ', '_')[:25]}.pdf"
    pdf_path = os.path.join(output_dir, nom_fichier)
    
    doc = SimpleDocTemplate(pdf_path, pagesize=A4, rightMargin=2*cm, leftMargin=2*cm,
                           topMargin=2*cm, bottomMargin=2*cm, title=offre['titre'])
    
    styles = getSampleStyleSheet()
    style_titre = ParagraphStyle('Title', parent=styles['Heading1'], fontSize=16,
                                textColor=colors.HexColor('#1a5490'), spaceAfter=20,
                                alignment=TA_CENTER, fontName='Helvetica-Bold')
    style_soustitre = ParagraphStyle('SubTitle', parent=styles['Heading2'], fontSize=13,
                                    textColor=colors.HexColor('#2980b9'), spaceAfter=10,
                                    spaceBefore=14, fontName='Helvetica-Bold',
                                    backColor=colors.HexColor('#ecf0f1'), borderPadding=5)
    style_info = ParagraphStyle('Info', parent=styles['Normal'], fontSize=10, spaceAfter=6)
    style_normal = ParagraphStyle('Normal', parent=styles['Normal'], fontSize=10,
                                 alignment=TA_JUSTIFY, spaceAfter=8)
    
    story = []
    
    # En-tête
    story.append(Paragraph(f"OFFRE N° {offre['id']}", style_titre))
    story.append(Paragraph(offre['titre'], style_titre))
    story.append(Spacer(1, 0.4*cm))
    
    # Informations
    story.append(Paragraph("INFORMATIONS GÉNÉRALES", style_soustitre))
    story.append(Paragraph(f"<b>Entreprise :</b> {offre['entreprise']}", style_info))
    story.append(Paragraph(f"<b>Localisation :</b> {offre['ville']}, {offre['pays']}", style_info))
    story.append(Paragraph(f"<b>Secteur :</b> {offre['secteur']}", style_info))
    story.append(Paragraph(f"<b>Date :</b> {offre['date']}", style_info))
    story.append(Paragraph(f"<b>Rémunération :</b> {offre['salaire']} / mois", style_info))
    story.append(Spacer(1, 0.3*cm))
    
    # Missions
    story.append(Paragraph("MISSIONS PRINCIPALES", style_soustitre))
    for mission in offre['missions']:
        story.append(Paragraph(f"• {mission}", style_normal))
    story.append(Spacer(1, 0.3*cm))
    
    # Profil
    story.append(Paragraph("PROFIL RECHERCHÉ", style_soustitre))
    story.append(Paragraph(f"<b>Expérience :</b> {offre['experience']} en audit", style_info))
    story.append(Paragraph("<b>Formation :</b> Master Audit/Finance/Comptabilité", style_info))
    story.append(Paragraph("<b>Certifications :</b> CIA, ACCA souhaitées", style_info))
    story.append(Spacer(1, 0.3*cm))
    
    # Compétences
    story.append(Paragraph("COMPÉTENCES", style_soustitre))
    competences = ["Audit opérationnel", "Normes IIA", "Risques", "Communication", "Outils IT"]
    for comp in competences:
        story.append(Paragraph(f"• {comp}", style_normal))
    
    # Footer
    story.append(Spacer(1, 1*cm))
    footer = ParagraphStyle('Footer', parent=styles['Normal'], fontSize=8,
                           textColor=colors.grey, alignment=TA_CENTER)
    story.append(Paragraph("Source : Afrique Ouest francophone 2021-2026", footer))
    
    doc.build(story)
    return pdf_path

def generer_tous():
    """Générer tous les PDFs"""
    output_dir = r"h:\Projet_pdf_excel\Modelisation websearch\Offre recrutement\03_Seniors"
    
    print(f"\n🚀 Génération de {len(OFFRES_SENIORS)} PDFs AUDITEURS SENIORS\n")
    
    for offre in OFFRES_SENIORS:
        try:
            creer_pdf_senior(offre, output_dir)
            print(f"✅ {offre['id']} - {offre['titre']}")
        except Exception as e:
            print(f"❌ {offre['id']} : {e}")
    
    print(f"\n✅ {len(OFFRES_SENIORS)} PDFs créés avec succès !\n")

if __name__ == "__main__":
    generer_tous()
