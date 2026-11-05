#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Génération de 50 PDFs individuels pour les offres d'Audit Interne
Afrique de l'Ouest Francophone (2021-2026)
"""

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
import os

# Définition des 50 offres
OFFRES = [
    # CÔTE D'IVOIRE (15)
    {"id": "CI-01", "titre": "CHEF DE MISSION AUDIT INTERNE", "entreprise": "NSIA ASSURANCES", "ville": "Abidjan", "pays": "Côte d'Ivoire", "date": "Avril 2025", "experience": "3 ans minimum", "certifications": "CIA, CFE, FRM", "type": "CDI", "secteur": "Assurance"},
    {"id": "CI-02", "titre": "DIRECTEUR AUDIT INTERNE", "entreprise": "YESHI GROUP", "ville": "Abidjan", "pays": "Côte d'Ivoire", "date": "Septembre 2026", "experience": "10+ ans", "certifications": "CIA", "type": "CDI", "secteur": "Multi-sectoriel"},
    {"id": "CI-03", "titre": "RESPONSABLE AUDIT INTERNE", "entreprise": "CORIS BANK INTERNATIONAL CI", "ville": "Abidjan", "pays": "Côte d'Ivoire", "date": "Septembre 2025", "experience": "2-5 ans banque", "certifications": "", "type": "CDI", "secteur": "Banque"},
    {"id": "CI-04", "titre": "CHEF DÉPARTEMENT AUDIT INTERNE", "entreprise": "AFRICA GLOBAL LOGISTICS", "ville": "Abidjan", "pays": "Côte d'Ivoire", "date": "2024", "experience": "7+ ans", "certifications": "", "type": "CDI", "secteur": "Logistique"},
    {"id": "CI-05", "titre": "AUDITEUR INTERNE SENIOR", "entreprise": "SIKA FINANCE", "ville": "Abidjan", "pays": "Côte d'Ivoire", "date": "2024", "experience": "1+ an", "certifications": "", "type": "CDI", "secteur": "Banque"},
    {"id": "CI-06", "titre": "DIRECTEUR AUDIT ET CONFORMITÉ", "entreprise": "CBAO ATTIJARIWAFA BANK", "ville": "Abidjan", "pays": "Côte d'Ivoire", "date": "Décembre 2023", "experience": "1-3 ans", "certifications": "", "type": "CDI", "secteur": "Banque"},
    {"id": "CI-07", "titre": "AUDITEUR INTERNE SENIOR INDUSTRIE", "entreprise": "ELITE INTERIM CI", "ville": "Abidjan", "pays": "Côte d'Ivoire", "date": "Septembre 2026", "experience": "6-10 ans", "certifications": "ISO", "type": "CDI", "secteur": "Industrie"},
    {"id": "CI-08", "titre": "RESPONSABLE AUDIT INTERNE", "entreprise": "NSIA BANQUE CI", "ville": "Abidjan", "pays": "Côte d'Ivoire", "date": "Janvier 2026", "experience": "5+ ans", "certifications": "CIA", "type": "CDI", "secteur": "Banque"},
    {"id": "CI-09", "titre": "AUDITEUR QUALITÉ INTERNE", "entreprise": "NSIA BANQUE", "ville": "Abidjan", "pays": "Côte d'Ivoire", "date": "Janvier 2026", "experience": "3+ ans", "certifications": "ISO 9001, 27001", "type": "CDI", "secteur": "Banque"},
    {"id": "CI-10", "titre": "DIRECTEUR AUDIT INTERNE", "entreprise": "CREDITINFO WEST AFRICA", "ville": "Abidjan", "pays": "Côte d'Ivoire", "date": "Juillet 2025", "experience": "4-5 ans", "certifications": "", "type": "CDI", "secteur": "Services financiers"},
    {"id": "CI-11", "titre": "HEAD OF INTERNAL AUDIT", "entreprise": "ECOBANK CÔTE D'IVOIRE", "ville": "Abidjan", "pays": "Côte d'Ivoire", "date": "Avril 2026", "experience": "8+ ans", "certifications": "CIA, ACCA", "type": "CDI", "secteur": "Banque"},
    {"id": "CI-12", "titre": "RESPONSABLE AUDIT ET RISQUES", "entreprise": "BANK OF AFRICA CI", "ville": "Abidjan", "pays": "Côte d'Ivoire", "date": "Avril 2026", "experience": "6+ ans", "certifications": "", "type": "CDI", "secteur": "Banque"},
    {"id": "CI-13", "titre": "SENIOR AUDIT MANAGER", "entreprise": "KPMG CÔTE D'IVOIRE", "ville": "Abidjan", "pays": "Côte d'Ivoire", "date": "Mai 2026", "experience": "5+ ans", "certifications": "Expert-comptable", "type": "CDI", "secteur": "Cabinet Big 4"},
    {"id": "CI-14", "titre": "SUPERVISEUR AUDIT", "entreprise": "KPMG CI", "ville": "Abidjan", "pays": "Côte d'Ivoire", "date": "Février 2026", "experience": "3-5 ans", "certifications": "", "type": "CDI", "secteur": "Cabinet Big 4"},
    {"id": "CI-15", "titre": "DIRECTEUR AUDIT ET INSPECTION", "entreprise": "ORANGE CÔTE D'IVOIRE", "ville": "Abidjan", "pays": "Côte d'Ivoire", "date": "2023", "experience": "10+ ans", "certifications": "", "type": "CDI", "secteur": "Télécommunications"},
    
    # SÉNÉGAL (12)
    {"id": "SN-01", "titre": "AUDITEUR INTERNE", "entreprise": "CETUD", "ville": "Dakar", "pays": "Sénégal", "date": "Octobre 2025", "experience": "7+ ans", "certifications": "", "type": "CDI", "secteur": "Transport public"},
    {"id": "SN-02", "titre": "RESPONSABLE AUDIT INTERNE", "entreprise": "IIA SÉNÉGAL", "ville": "Dakar", "pays": "Sénégal", "date": "2024", "experience": "10+ ans", "certifications": "CA, CIA, CFE", "type": "CDI", "secteur": "Association professionnelle"},
    {"id": "SN-03", "titre": "DIRECTEUR AUDIT INTERNE", "entreprise": "BANQUE ATLANTIQUE SÉNÉGAL", "ville": "Dakar", "pays": "Sénégal", "date": "Juin 2025", "experience": "8+ ans", "certifications": "", "type": "CDI", "secteur": "Banque"},
    {"id": "SN-04", "titre": "CHEF DÉPARTEMENT AUDIT", "entreprise": "CBAO SÉNÉGAL", "ville": "Dakar", "pays": "Sénégal", "date": "2024", "experience": "7+ ans", "certifications": "", "type": "CDI", "secteur": "Banque"},
    {"id": "SN-05", "titre": "REGIONAL INTERNAL AUDITOR SAHEL", "entreprise": "MSI CHOICES (ONG)", "ville": "Dakar", "pays": "Sénégal", "date": "Juin 2026", "experience": "5+ ans", "certifications": "", "type": "CDI", "secteur": "Humanitaire"},
    {"id": "SN-06", "titre": "RESPONSABLE AUDIT ET CONTRÔLE", "entreprise": "SONATEL (Orange)", "ville": "Dakar", "pays": "Sénégal", "date": "2023", "experience": "8+ ans", "certifications": "", "type": "CDI", "secteur": "Télécoms"},
    {"id": "SN-07", "titre": "DIRECTEUR AUDIT INTERNE", "entreprise": "ECOBANK SÉNÉGAL", "ville": "Dakar", "pays": "Sénégal", "date": "2024", "experience": "10+ ans", "certifications": "CIA", "type": "CDI", "secteur": "Banque"},
    {"id": "SN-08", "titre": "SENIOR AUDIT MANAGER", "entreprise": "DELOITTE SÉNÉGAL", "ville": "Dakar", "pays": "Sénégal", "date": "2023", "experience": "6+ ans", "certifications": "Expert-comptable", "type": "CDI", "secteur": "Cabinet conseil"},
    {"id": "SN-09", "titre": "AUDIT MANAGER", "entreprise": "PWC SÉNÉGAL", "ville": "Dakar", "pays": "Sénégal", "date": "2024", "experience": "5+ ans", "certifications": "Expert-comptable", "type": "CDI", "secteur": "Cabinet Big 4"},
    {"id": "SN-10", "titre": "RESPONSABLE AUDIT INTERNE", "entreprise": "SOCIÉTÉ GÉNÉRALE SÉNÉGAL", "ville": "Dakar", "pays": "Sénégal", "date": "2022", "experience": "6+ ans", "certifications": "", "type": "CDI", "secteur": "Banque"},
    {"id": "SN-11", "titre": "DIRECTEUR INSPECTION GÉNÉRALE", "entreprise": "BANQUE DE L'HABITAT", "ville": "Dakar", "pays": "Sénégal", "date": "2023", "experience": "10+ ans", "certifications": "", "type": "CDI", "secteur": "Banque"},
    {"id": "SN-12", "titre": "CHEF SERVICE AUDIT", "entreprise": "COMPAGNIE SAHÉLIENNE", "ville": "Dakar", "pays": "Sénégal", "date": "2025", "experience": "5+ ans", "certifications": "", "type": "CDI", "secteur": "Distribution"},
    
    # MALI (8)
    {"id": "ML-01", "titre": "AUDITEUR INTERNE", "entreprise": "AMIFA MALI", "ville": "Bamako", "pays": "Mali", "date": "Juin 2023", "experience": "3+ ans", "certifications": "", "type": "CDI", "secteur": "Microfinance"},
    {"id": "ML-02", "titre": "COORDINATEUR AUDIT", "entreprise": "ACTION CONTRE LA FAIM", "ville": "Bamako", "pays": "Mali", "date": "Novembre 2023", "experience": "5+ ans", "certifications": "", "type": "CDI", "secteur": "Humanitaire"},
    {"id": "ML-03", "titre": "SUPERVISEUR AUDIT", "entreprise": "CABINET AUDIT INTERNATIONAL", "ville": "Bamako", "pays": "Mali", "date": "2024", "experience": "4+ ans", "certifications": "", "type": "CDI", "secteur": "Cabinet"},
    {"id": "ML-04", "titre": "RESPONSABLE AUDIT INTERNE", "entreprise": "BANK OF AFRICA MALI", "ville": "Bamako", "pays": "Mali", "date": "2024", "experience": "6+ ans", "certifications": "", "type": "CDI", "secteur": "Banque"},
    {"id": "ML-05", "titre": "DIRECTEUR AUDIT ET CONFORMITÉ", "entreprise": "ECOBANK MALI", "ville": "Bamako", "pays": "Mali", "date": "Mars 2025", "experience": "8+ ans", "certifications": "", "type": "CDI", "secteur": "Banque"},
    {"id": "ML-06", "titre": "CHEF DÉPARTEMENT AUDIT", "entreprise": "BANQUE ATLANTIQUE MALI", "ville": "Bamako", "pays": "Mali", "date": "Juin 2025", "experience": "7+ ans", "certifications": "", "type": "CDI", "secteur": "Banque"},
    {"id": "ML-07", "titre": "AUDITEUR INTERNE SENIOR", "entreprise": "ORANGE MALI", "ville": "Bamako", "pays": "Mali", "date": "2023", "experience": "5+ ans", "certifications": "", "type": "CDI", "secteur": "Télécoms"},
    {"id": "ML-08", "titre": "RESPONSABLE AUDIT ET RISQUES", "entreprise": "SOCIÉTÉ GÉNÉRALE MALI", "ville": "Bamako", "pays": "Mali", "date": "2022", "experience": "6+ ans", "certifications": "", "type": "CDI", "secteur": "Banque"},
    
    # BURKINA FASO (5)
    {"id": "BF-01", "titre": "EXPERT SENIOR AUDIT", "entreprise": "SWISS TPH", "ville": "Ouagadougou", "pays": "Burkina Faso", "date": "Novembre 2022", "experience": "10+ ans", "certifications": "", "type": "Contrat", "secteur": "Santé"},
    {"id": "BF-02", "titre": "AUDITEUR INTERNE", "entreprise": "WELTHUNGERHILFE (WHH)", "ville": "Ouagadougou", "pays": "Burkina Faso", "date": "2023-2025", "experience": "5+ ans", "certifications": "", "type": "Contrat", "secteur": "Humanitaire"},
    {"id": "BF-03", "titre": "DIRECTEUR AUDIT", "entreprise": "ECOBANK BURKINA", "ville": "Ouagadougou", "pays": "Burkina Faso", "date": "2024", "experience": "8+ ans", "certifications": "", "type": "CDI", "secteur": "Banque"},
    {"id": "BF-04", "titre": "RESPONSABLE AUDIT INTERNE", "entreprise": "BANK OF AFRICA BURKINA", "ville": "Ouagadougou", "pays": "Burkina Faso", "date": "2023", "experience": "6+ ans", "certifications": "", "type": "CDI", "secteur": "Banque"},
    {"id": "BF-05", "titre": "AUDITEUR INTERNE", "entreprise": "ENTREPRISE LOCALE", "ville": "Ouagadougou", "pays": "Burkina Faso", "date": "2024", "experience": "2-3 ans", "certifications": "CIA candidat", "type": "CDI", "secteur": "Divers"},
    
    # BÉNIN (4)
    {"id": "BJ-01", "titre": "AUDITEUR INTERNE", "entreprise": "SECTEUR BANCAIRE", "ville": "Cotonou", "pays": "Bénin", "date": "2024-2025", "experience": "3+ ans", "certifications": "", "type": "CDI", "secteur": "Banque"},
    {"id": "BJ-02", "titre": "RESPONSABLE AUDIT", "entreprise": "DELOITTE BÉNIN", "ville": "Cotonou", "pays": "Bénin", "date": "Août 2026", "experience": "5+ ans", "certifications": "", "type": "CDI", "secteur": "Cabinet"},
    {"id": "BJ-03", "titre": "DIRECTEUR AUDIT", "entreprise": "ECOBANK BÉNIN", "ville": "Cotonou", "pays": "Bénin", "date": "2023", "experience": "8+ ans", "certifications": "", "type": "CDI", "secteur": "Banque"},
    {"id": "BJ-04", "titre": "CHEF SERVICE AUDIT", "entreprise": "BANK OF AFRICA BÉNIN", "ville": "Cotonou", "pays": "Bénin", "date": "2024", "experience": "5+ ans", "certifications": "", "type": "CDI", "secteur": "Banque"},
    
    # TOGO (3)
    {"id": "TG-01", "titre": "AUDITEUR SENIOR", "entreprise": "DELOITTE TOGO", "ville": "Lomé", "pays": "Togo", "date": "Août 2026", "experience": "4+ ans", "certifications": "", "type": "CDI", "secteur": "Cabinet"},
    {"id": "TG-02", "titre": "RESPONSABLE AUDIT INTERNE", "entreprise": "ECOBANK TOGO", "ville": "Lomé", "pays": "Togo", "date": "2024", "experience": "6+ ans", "certifications": "", "type": "CDI", "secteur": "Banque"},
    {"id": "TG-03", "titre": "DIRECTEUR AUDIT", "entreprise": "SOCIÉTÉ AFRICAINE ENTREPRISES", "ville": "Lomé", "pays": "Togo", "date": "2023", "experience": "8+ ans", "certifications": "", "type": "CDI", "secteur": "Multi-sectoriel"},
    
    # NIGER (2)
    {"id": "NE-01", "titre": "AUDITEUR DES EBNL", "entreprise": "SECTEUR ASSOCIATIF", "ville": "Niamey", "pays": "Niger", "date": "2024-2025", "experience": "5+ ans", "certifications": "", "type": "Contrat", "secteur": "ONG"},
    {"id": "NE-02", "titre": "RESPONSABLE AUDIT INTERNE", "entreprise": "BANQUE ATLANTIQUE NIGER", "ville": "Niamey", "pays": "Niger", "date": "2023", "experience": "6+ ans", "certifications": "", "type": "CDI", "secteur": "Banque"},
    
    # GUINÉE (1)
    {"id": "GN-01", "titre": "DIRECTEUR AUDIT ET INSPECTION", "entreprise": "ÉTABLISSEMENTS PUBLICS", "ville": "Conakry", "pays": "Guinée", "date": "Mars 2025", "experience": "8+ ans", "certifications": "", "type": "CDI", "secteur": "Administration"},
]

def creer_pdf_offre(offre, output_dir):
    """Créer un PDF pour une offre"""
    nom_fichier = f"{offre['id']}_{offre['entreprise'].replace(' ', '_')}.pdf"
    pdf_path = os.path.join(output_dir, nom_fichier)
    
    doc = SimpleDocTemplate(pdf_path, pagesize=A4, rightMargin=2*cm, leftMargin=2*cm, 
                           topMargin=2*cm, bottomMargin=2*cm)
    
    styles = getSampleStyleSheet()
    style_titre = ParagraphStyle('Title', parent=styles['Heading1'], fontSize=16,
                                textColor=colors.HexColor('#1a5490'), spaceAfter=20,
                                alignment=TA_CENTER, fontName='Helvetica-Bold')
    style_info = ParagraphStyle('Info', parent=styles['Normal'], fontSize=10, spaceAfter=6)
    style_section = ParagraphStyle('Section', parent=styles['Heading3'], fontSize=12,
                                  textColor=colors.HexColor('#34495e'), spaceAfter=8,
                                  spaceBefore=12, fontName='Helvetica-Bold')
    
    story = []
    
    # En-tête
    story.append(Paragraph(f"OFFRE {offre['id']}", style_titre))
    story.append(Paragraph(offre['titre'], style_titre))
    story.append(Spacer(1, 0.5*cm))
    
    # Informations principales
    story.append(Paragraph(f"<b>Entreprise :</b> {offre['entreprise']}", style_info))
    story.append(Paragraph(f"<b>Localisation :</b> {offre['ville']}, {offre['pays']}", style_info))
    story.append(Paragraph(f"<b>Date de publication :</b> {offre['date']}", style_info))
    story.append(Paragraph(f"<b>Type de contrat :</b> {offre['type']}", style_info))
    story.append(Paragraph(f"<b>Secteur :</b> {offre['secteur']}", style_info))
    story.append(Spacer(1, 0.5*cm))
    
    # Profil
    story.append(Paragraph("PROFIL RECHERCHÉ", style_section))
    story.append(Paragraph(f"<b>Expérience :</b> {offre['experience']}", style_info))
    if offre['certifications']:
        story.append(Paragraph(f"<b>Certifications :</b> {offre['certifications']}", style_info))
    
    # Pied de page
    story.append(Spacer(1, 1*cm))
    footer = ParagraphStyle('Footer', parent=styles['Normal'], fontSize=8, 
                           textColor=colors.grey, alignment=TA_CENTER)
    story.append(Paragraph(
        "<b>Source :</b> Recherche Afrique de l'Ouest francophone 2021-2026<br/>"
        "<b>Document :</b> Expert Audit & RH - 30 ans d'expérience",
        footer
    ))
    
    doc.build(story)
    return pdf_path

def generer_tous_les_pdfs():
    """Générer tous les PDFs"""
    output_dir = r"h:\Projet_pdf_excel\Modelisation websearch\Offre recrutement"
    
    print(f"\n🚀 Génération de {len(OFFRES)} PDFs...\n")
    
    pdfs_crees = []
    for offre in OFFRES:
        try:
            pdf_path = creer_pdf_offre(offre, output_dir)
            pdfs_crees.append(pdf_path)
            print(f"✅ Créé : {offre['id']} - {offre['titre'][:40]}...")
        except Exception as e:
            print(f"❌ Erreur {offre['id']} : {e}")
    
    print(f"\n✅ {len(pdfs_crees)} PDFs créés avec succès !\n")
    return pdfs_crees

if __name__ == "__main__":
    try:
        pdfs = generer_tous_les_pdfs()
    except Exception as e:
        print(f"❌ Erreur générale : {e}")
        import traceback
        traceback.print_exc()
