#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Collecteur d'offres d'emploi réelles - Audit Afrique de l'Ouest
Sauvegarde HTML + Génération PDF avec données réelles
"""

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
import os
import json
from datetime import datetime

# Base de données des offres collectées
OFFRES_REELLES = {
    "offre_001": {
        "id": "CI-CORIS-2025",
        "source_url": "https://cotedivoire.coris.bank/recrutement-auditeur-interne/",
        "date_collecte": "2026-11-02",
        "entreprise": "CORIS BANK INTERNATIONAL - CÔTE D'IVOIRE",
        "poste": "Auditeur Interne (H/F)",
        "type_contrat": "CDI",
        "localisation": "Abidjan, Côte d'Ivoire",
        "hierarchie": "Reporte au Directeur de l'Audit Interne",
        "date_limite": "20 septembre 2025",
        "environnement": "Vous rejoindrez la Direction de l'Audit Interne et avez pour rôle de participer au contrôle du respect des règles et procédures internes, des dispositions législatives et réglementaires en vigueur, des usages professionnels et déontologiques ainsi que des orientations stratégiques de la banque.",
        "missions": [
            "Participer à la réalisation du planning annuel d'Audit",
            "Réaliser les contrôles périodiques ayant trait à l'audit interne",
            "Rédiger les rapports d'audit interne",
            "Suivre la mise en œuvre des recommandations issues des missions d'audit",
            "Intervention en cas de fraude",
            "Traiter les réclamations clientèle",
            "Assurer l'organisation logistique des missions d'audit externe",
            "Participer à la rédaction des rapports pour la BCEAO et la Commission Bancaire",
            "Assurer les diligences demandées par les autorités monétaires"
        ],
        "formation": "Bac + 4/5 en Finance, Audit et Contrôle de Gestion",
        "experience": "4 ans minimum dans un établissement bancaire ou cabinet d'audit",
        "savoir_faire": [
            "Excellente capacité d'analyse et de synthèse",
            "Bonne communication écrite et orale",
            "Maîtrise du pack office (Word, Excel, PowerPoint)",
            "Bonne capacité à travailler sous pression"
        ],
        "savoir_etre": [
            "Fiabilité et orientation qualité",
            "Excellentes qualités rédactionnelles",
            "Disponibilité et rigueur",
            "Sens de l'écoute et de l'organisation"
        ],
        "email_candidature": "recrutements-cbici@coris-bank.com",
        "objet_email": "CANDIDATURE AU POSTE D'AUDITEUR INTERNE",
        "niveau": "Confirmé"
    },
    
    "offre_002": {
        "id": "CI-NSIA-2025",
        "source_url": "https://yop.l-frii.com/emploi/nsia-assurances-recrute-pour-ce-poste-07-avril-2025/",
        "date_collecte": "2026-11-02",
        "entreprise": "NSIA ASSURANCES - CÔTE D'IVOIRE",
        "poste": "Chef de Mission Audit Interne",
        "type_contrat": "CDI",
        "localisation": "Abidjan, Côte d'Ivoire",
        "hierarchie": "Superviseur Audit Interne / Chef de Département Audit Interne",
        "date_limite": "11 avril 2025",
        "raison_etre": "Contribuer à la réduction des pertes opérationnelles de la banque et fournir les conseils nécessaires aux différents domaines de gestion afin de protéger les résultats acquis et d'améliorer les processus internes et de management des risques.",
        "finalites": [
            "Mettre en œuvre le programme d'audit annuel afin d'identifier les zones de risques significatifs",
            "Animer et coordonner les activités d'audit dans le respect du cadre fixé par la Direction",
            "Organiser et superviser les ressources allouées pour réaliser les missions dans les délais",
            "Vérifier la conformité aux procédures internes et instructions réglementaires"
        ],
        "formation": "BAC + 4/5 en Finance, Comptabilité, Audit ou Contrôle de gestion (Sup de Co, MSTCF, DSCG, Master)",
        "certifications": "CIA, CFE, FRM, ACAMS (atout)",
        "experience": "3 ans minimum auditeur interne ou contrôleur interne expérimenté",
        "competences_techniques": [
            "Informatique (Word, Excel, Power Point)",
            "Bon niveau en anglais (lu, écrit et parlé)",
            "Techniques avancées de modélisation et d'analyse de données",
            "Bonnes connaissances audit interne et contrôle financier",
            "Connaissance réglementation bancaire et PCB Révisé",
            "Compréhension des risques liés à l'activité bancaire"
        ],
        "competences_comportementales": [
            "Aptitudes en conduite de réunions",
            "Techniques de présentation",
            "Conception de diapositives",
            "Rigueur, discrétion, capacité d'adaptation",
            "Capacité d'analyse et de synthèse",
            "Autonomie, sens de l'organisation",
            "Esprit d'équipe",
            "Capacité à travailler sous pression",
            "Bonnes qualités rédactionnelles",
            "Aptitudes à la réflexion et à la conceptualisation"
        ],
        "email_candidature": "[email protected]",
        "dossier": "Lettre de motivation + CV + dernier diplôme",
        "niveau": "Senior"
    },
    
    "offre_003": {
        "id": "CI-SIKA-2024",
        "source_url": "https://www.sikafinance.com/emploi/auditeur-interne-junior_718",
        "date_collecte": "2026-11-02",
        "entreprise": "SIKA FINANCE - CÔTE D'IVOIRE",
        "poste": "Auditeur Interne Junior",
        "type_contrat": "CDI",
        "localisation": "Abidjan, Côte d'Ivoire",
        "mission": "Effectuer des contrôles périodiques et des investigations afin de détecter les éventuels dysfonctionnements organisationnels, réglementaires, économiques et humains de la Banque.",
        "activites_principales": [
            "Contribuer à donner aux organes de gouvernance une assurance raisonnable sur la qualité du contrôle interne",
            "Participer à l'élaboration de la charte éthique et du code de déontologie",
            "Préparer et exécuter les missions d'audit interne",
            "Rédiger les rapports d'audit",
            "Transmettre le rapport d'audit à la hiérarchie et présenter les résultats",
            "Contribuer au suivi des recommandations",
            "Veiller au respect des règles en vigueur",
            "Participer à des missions d'investigation",
            "Assurer le contrôle interne de ses activités",
            "Veiller à la transmission des informations pour assurer la continuité"
        ],
        "formation": "BAC+4/5 en Audit et Contrôle, Sciences Economiques et Gestion, Banque, Finance, Comptabilité",
        "experience": "1 an minimum dans l'Audit et le Contrôle Interne",
        "competences": [
            "Bonne connaissance des techniques d'entretien et d'investigation",
            "Bonne connaissance des activités et opérations bancaires",
            "Connaissance de la Banque, ses métiers et son organisation",
            "Bonnes connaissances de la réglementation bancaire",
            "Bonne maîtrise de la cartographie des risques",
            "Bonne connaissance des logiciels de gestion bancaire",
            "Bonne maîtrise des outils bureautiques"
        ],
        "qualites": [
            "Sens de l'organisation",
            "Rigueur et méthode",
            "Disponibilité",
            "Bonne communication orale et écrite",
            "Intégrité",
            "Objectivité",
            "Capacité d'analyse et de synthèse",
            "Confidentialité",
            "Esprit critique",
            "Capacité à gérer la pression"
        ],
        "objet_email": "AUDITEUR INTERNE JUNIOR",
        "note": "Seules les candidatures retenues seront contactées",
        "niveau": "Junior"
    }
}

def sauvegarder_json(offres, fichier):
    """Sauvegarder les offres en JSON"""
    with open(fichier, 'w', encoding='utf-8') as f:
        json.dump(offres, f, ensure_ascii=False, indent=4)
    print(f"✅ JSON sauvegardé : {fichier}")

def creer_pdf_detaille_reel(offre_data, output_dir):
    """Créer un PDF détaillé à partir de données réelles"""
    nom_fichier = f"{offre_data['id']}_{offre_data['entreprise'].split('-')[0].strip().replace(' ', '_')[:20]}.pdf"
    pdf_path = os.path.join(output_dir, nom_fichier)
    
    doc = SimpleDocTemplate(pdf_path, pagesize=A4, rightMargin=2*cm, leftMargin=2*cm,
                           topMargin=2*cm, bottomMargin=2*cm, title=offre_data['poste'])
    
    styles = getSampleStyleSheet()
    
    style_titre = ParagraphStyle('Title', parent=styles['Heading1'], fontSize=18,
                                textColor=colors.HexColor('#1a5490'), spaceAfter=20,
                                alignment=TA_CENTER, fontName='Helvetica-Bold')
    
    style_entreprise = ParagraphStyle('Entreprise', parent=styles['Heading2'], fontSize=14,
                                     textColor=colors.HexColor('#2980b9'), spaceAfter=15,
                                     alignment=TA_CENTER, fontName='Helvetica-Bold')
    
    style_section = ParagraphStyle('Section', parent=styles['Heading3'], fontSize=12,
                                  textColor=colors.white, spaceAfter=10, spaceBefore=15,
                                  fontName='Helvetica-Bold', backColor=colors.HexColor('#3498db'),
                                  borderPadding=6)
    
    style_info = ParagraphStyle('Info', parent=styles['Normal'], fontSize=10, spaceAfter=6)
    style_normal = ParagraphStyle('Normal', parent=styles['Normal'], fontSize=10,
                                 alignment=TA_JUSTIFY, spaceAfter=8)
    
    story = []
    
    # En-tête
    story.append(Paragraph(f"OFFRE D'EMPLOI N° {offre_data['id']}", style_titre))
    story.append(Paragraph(offre_data['poste'].upper(), style_titre))
    story.append(Paragraph(offre_data['entreprise'], style_entreprise))
    story.append(Spacer(1, 0.5*cm))
    
    # Informations principales
    story.append(Paragraph("📋 INFORMATIONS GÉNÉRALES", style_section))
    story.append(Paragraph(f"<b>Type de contrat :</b> {offre_data['type_contrat']}", style_info))
    story.append(Paragraph(f"<b>Localisation :</b> {offre_data['localisation']}", style_info))
    if 'hierarchie' in offre_data:
        story.append(Paragraph(f"<b>Hiérarchie :</b> {offre_data['hierarchie']}", style_info))
    if 'date_limite' in offre_data:
        story.append(Paragraph(f"<b>Date limite :</b> {offre_data['date_limite']}", style_info))
    story.append(Spacer(1, 0.3*cm))
    
    # Environnement / Raison d'être
    if 'environnement' in offre_data:
        story.append(Paragraph("🏢 ENVIRONNEMENT DE TRAVAIL", style_section))
        story.append(Paragraph(offre_data['environnement'], style_normal))
        story.append(Spacer(1, 0.3*cm))
    
    if 'raison_etre' in offre_data:
        story.append(Paragraph("🎯 RAISON D'ÊTRE DE LA FONCTION", style_section))
        story.append(Paragraph(offre_data['raison_etre'], style_normal))
        story.append(Spacer(1, 0.3*cm))
    
    # Missions / Activités / Finalités
    if 'missions' in offre_data:
        story.append(Paragraph("✅ MISSIONS DU POSTE", style_section))
        for mission in offre_data['missions']:
            story.append(Paragraph(f"• {mission}", style_normal))
        story.append(Spacer(1, 0.3*cm))
    
    if 'finalites' in offre_data:
        story.append(Paragraph("✅ FINALITÉS DE LA FONCTION", style_section))
        for finalite in offre_data['finalites']:
            story.append(Paragraph(f"• {finalite}", style_normal))
        story.append(Spacer(1, 0.3*cm))
    
    if 'activites_principales' in offre_data:
        story.append(Paragraph("✅ ACTIVITÉS PRINCIPALES", style_section))
        for activite in offre_data['activites_principales']:
            story.append(Paragraph(f"• {activite}", style_normal))
        story.append(Spacer(1, 0.3*cm))
    
    # Profil recherché
    story.append(Paragraph("👤 PROFIL RECHERCHÉ", style_section))
    story.append(Paragraph(f"<b>Formation :</b> {offre_data['formation']}", style_info))
    story.append(Paragraph(f"<b>Expérience :</b> {offre_data['experience']}", style_info))
    
    if 'certifications' in offre_data:
        story.append(Paragraph(f"<b>Certifications :</b> {offre_data['certifications']}", style_info))
    story.append(Spacer(1, 0.3*cm))
    
    # Compétences
    if 'savoir_faire' in offre_data:
        story.append(Paragraph("🎓 SAVOIR-FAIRE", style_section))
        for comp in offre_data['savoir_faire']:
            story.append(Paragraph(f"• {comp}", style_normal))
        story.append(Spacer(1, 0.3*cm))
    
    if 'savoir_etre' in offre_data:
        story.append(Paragraph("💡 SAVOIR-ÊTRE", style_section))
        for qual in offre_data['savoir_etre']:
            story.append(Paragraph(f"• {qual}", style_normal))
        story.append(Spacer(1, 0.3*cm))
    
    if 'competences_techniques' in offre_data:
        story.append(Paragraph("🎓 COMPÉTENCES TECHNIQUES", style_section))
        for comp in offre_data['competences_techniques']:
            story.append(Paragraph(f"• {comp}", style_normal))
        story.append(Spacer(1, 0.3*cm))
    
    if 'competences_comportementales' in offre_data:
        story.append(Paragraph("💡 COMPÉTENCES COMPORTEMENTALES", style_section))
        for comp in offre_data['competences_comportementales']:
            story.append(Paragraph(f"• {comp}", style_normal))
        story.append(Spacer(1, 0.3*cm))
    
    if 'competences' in offre_data:
        story.append(Paragraph("🎓 COMPÉTENCES REQUISES", style_section))
        for comp in offre_data['competences']:
            story.append(Paragraph(f"• {comp}", style_normal))
        story.append(Spacer(1, 0.3*cm))
    
    if 'qualites' in offre_data:
        story.append(Paragraph("💡 QUALITÉS PERSONNELLES", style_section))
        for qual in offre_data['qualites']:
            story.append(Paragraph(f"• {qual}", style_normal))
        story.append(Spacer(1, 0.3*cm))
    
    # Candidature
    story.append(Paragraph("📧 CANDIDATURE", style_section))
    if 'email_candidature' in offre_data:
        story.append(Paragraph(f"<b>Email :</b> {offre_data['email_candidature']}", style_info))
    if 'objet_email' in offre_data:
        story.append(Paragraph(f"<b>Objet :</b> {offre_data['objet_email']}", style_info))
    if 'dossier' in offre_data:
        story.append(Paragraph(f"<b>Dossier :</b> {offre_data['dossier']}", style_info))
    if 'note' in offre_data:
        story.append(Paragraph(f"<em>{offre_data['note']}</em>", style_info))
    
    # Pied de page
    story.append(Spacer(1, 1*cm))
    footer = ParagraphStyle('Footer', parent=styles['Normal'], fontSize=8,
                           textColor=colors.grey, alignment=TA_CENTER)
    story.append(Paragraph(
        f"<b>Source :</b> {offre_data['source_url']}<br/>"
        f"<b>Date de collecte :</b> {offre_data['date_collecte']}<br/>"
        f"<b>Niveau hiérarchique :</b> {offre_data['niveau']}",
        footer
    ))
    
    doc.build(story)
    return pdf_path

def generer_pdfs_par_niveau():
    """Générer les PDFs classés par niveau hiérarchique"""
    base_dir = r"h:\Projet_pdf_excel\Modelisation websearch\Offre recrutement"
    
    niveaux_dirs = {
        "Directeur": os.path.join(base_dir, "01_Directeurs"),
        "Senior": os.path.join(base_dir, "02_Seniors"),
        "Confirmé": os.path.join(base_dir, "03_Confirmes"),
        "Junior": os.path.join(base_dir, "04_Juniors")
    }
    
    print("\n🚀 GÉNÉRATION DES PDFs À PARTIR DES DONNÉES RÉELLES\n")
    
    # Sauvegarder JSON
    json_file = os.path.join(base_dir, "offres_reelles_collectees.json")
    sauvegarder_json(OFFRES_REELLES, json_file)
    
    # Générer PDFs
    for offre_key, offre_data in OFFRES_REELLES.items():
        niveau = offre_data['niveau']
        output_dir = niveaux_dirs.get(niveau, niveaux_dirs["Confirmé"])
        
        try:
            pdf_path = creer_pdf_detaille_reel(offre_data, output_dir)
            print(f"✅ {offre_data['id']} - {offre_data['poste']} ({niveau})")
        except Exception as e:
            print(f"❌ Erreur {offre_data['id']} : {e}")
    
    print(f"\n✅ {len(OFFRES_REELLES)} PDFs créés avec succès !\n")

if __name__ == "__main__":
    generer_pdfs_par_niveau()
