#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script de création de PDFs individuels pour chaque offre d'emploi
"""

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
import os

def creer_style_personnalise():
    """Créer les styles personnalisés"""
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
    
    return style_titre, style_soustitre, style_normal, style_info

def creer_pdf_offre(numero, titre, entreprise, localisation, contrat, details, output_dir):
    """Créer un PDF pour une offre spécifique"""
    
    # Nom de fichier sécurisé
    nom_fichier = f"Offre_{numero:02d}_{entreprise.replace(' ', '_').replace('/', '_')}.pdf"
    pdf_path = os.path.join(output_dir, nom_fichier)
    
    # Configuration du document
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=A4,
        rightMargin=2*cm,
        leftMargin=2*cm,
        topMargin=2*cm,
        bottomMargin=2*cm,
        title=f"Offre {numero} - {titre}"
    )
    
    # Styles
    style_titre, style_soustitre, style_normal, style_info = creer_style_personnalise()
    
    # Contenu
    story = []
    
    # En-tête
    story.append(Paragraph(f"OFFRE D'EMPLOI N°{numero}", style_titre))
    story.append(Paragraph(titre, style_titre))
    story.append(Spacer(1, 0.5*cm))
    
    # Informations principales
    story.append(Paragraph(f"<b>Entreprise :</b> {entreprise}", style_info))
    story.append(Paragraph(f"<b>Localisation :</b> {localisation}", style_info))
    story.append(Paragraph(f"<b>Type de contrat :</b> {contrat}", style_info))
    story.append(Spacer(1, 0.5*cm))
    
    # Sections de détails
    for section_titre, contenu in details.items():
        story.append(Paragraph(section_titre, style_soustitre))
        
        if isinstance(contenu, list):
            for item in contenu:
                story.append(Paragraph(f"• {item}", style_normal))
        elif isinstance(contenu, dict):
            for key, value in contenu.items():
                story.append(Paragraph(f"<b>{key} :</b> {value}", style_normal))
        else:
            story.append(Paragraph(contenu, style_normal))
        
        story.append(Spacer(1, 0.3*cm))
    
    # Pied de page
    story.append(Spacer(1, 1*cm))
    story.append(Paragraph(
        "<b>Source :</b> Recherche web - Novembre 2026<br/>"
        "<b>Expert :</b> Directeur Audit & RH - 30 ans d'expérience",
        ParagraphStyle('Footer', parent=style_normal, fontSize=8, textColor=colors.grey, alignment=TA_CENTER)
    ))
    
    # Générer le PDF
    doc.build(story)
    print(f"✅ Créé : {nom_fichier}")
    return pdf_path

def generer_toutes_les_offres():
    """Générer tous les PDFs individuels"""
    
    output_dir = r"h:\Projet_pdf_excel\Modelisation websearch\Offre recrutement"
    
    # Définition des 10 offres
    offres = [
        {
            "numero": 1,
            "titre": "CHEF DE MISSION AUDIT INTERNE",
            "entreprise": "NSIA ASSURANCES",
            "localisation": "Abidjan, Côte d'Ivoire",
            "contrat": "CDI",
            "details": {
                "RAISON D'ÊTRE": "Contribuer à la réduction des pertes opérationnelles de la banque et fournir les conseils nécessaires aux différents domaines de gestion afin de protéger les résultats acquis et d'améliorer les processus internes et de management des risques.",
                "POSITION HIÉRARCHIQUE": [
                    "Superviseur : Chef de Département Audit Interne",
                    "Collaborateurs : Superviseur Audit Interne"
                ],
                "MISSIONS PRINCIPALES": [
                    "Mettre en œuvre le programme d'audit annuel pour identifier les zones de risques significatifs",
                    "Animer et coordonner les activités d'audit dans le respect du cadre fixé par la Direction",
                    "Organiser et superviser les ressources allouées pour réaliser les missions dans les délais",
                    "Vérifier la conformité aux procédures internes et instructions réglementaires"
                ],
                "PROFIL RECHERCHÉ": {
                    "Formation": "BAC+4/5 en Finance, Comptabilité, Audit ou Contrôle de gestion (MSTCF, DSCG, Master)",
                    "Certifications": "CIA, CFE, FRM, ACAMS (atout)",
                    "Informatique": "Word, Excel, PowerPoint",
                    "Langues": "Bon niveau en anglais (lu, écrit et parlé)",
                    "Expérience": "3 ans minimum dans la fonction d'auditeur interne ou contrôleur interne"
                },
                "COMPÉTENCES CLÉS": [
                    "Bonnes connaissances en audit interne et contrôle financier",
                    "Connaissance de la réglementation bancaire et du PCB Révisé",
                    "Compréhension des risques liés à l'activité bancaire",
                    "Aptitudes en conduite de réunions et techniques de présentation",
                    "Rigueur, discrétion, capacité d'analyse et de synthèse"
                ],
                "CANDIDATURE": {
                    "Email": "[email protected]",
                    "Date limite": "11 avril 2025",
                    "Dossier": "CV + Lettre de motivation + Dernier diplôme"
                }
            }
        },
        {
            "numero": 2,
            "titre": "DIRECTEUR AUDIT",
            "entreprise": "YESHI GROUP",
            "localisation": "Côte d'Ivoire",
            "contrat": "CDI - Cadre dirigeant",
            "details": {
                "PROFIL RECHERCHÉ": {
                    "Expérience": "Plus de 10 ans dans l'audit et le contrôle interne",
                    "Niveau": "Cadre dirigeant",
                    "Secteur": "Multi-sectoriel (Industrie, Services)"
                },
                "COMPÉTENCES CLÉS": [
                    "Direction et management d'équipes d'audit",
                    "Élaboration de la stratégie d'audit de l'entreprise",
                    "Gestion des risques opérationnels et financiers",
                    "Maîtrise des normes internationales d'audit (ISA, IIA)",
                    "Pilotage de projets d'amélioration des processus",
                    "Relations avec les organes de gouvernance et régulateurs"
                ],
                "RESPONSABILITÉS": [
                    "Définir la stratégie et le plan d'audit annuel",
                    "Superviser et manager l'équipe d'audit interne",
                    "Présenter les rapports d'audit aux comités de direction",
                    "Assurer la conformité réglementaire de l'organisation",
                    "Évaluer l'efficacité du contrôle interne"
                ],
                "CANDIDATURE": {
                    "Source": "NovoJob.com",
                    "Date publication": "Septembre 2026"
                }
            }
        },
        {
            "numero": 3,
            "titre": "AUDITEUR INTERNE (H/F)",
            "entreprise": "CORIS BANK INTERNATIONAL",
            "localisation": "Abidjan, Côte d'Ivoire",
            "contrat": "CDI",
            "details": {
                "ENVIRONNEMENT": "Vous rejoindrez la Direction de l'Audit Interne et aurez pour rôle de participer au contrôle du respect des règles et procédures internes, des dispositions législatives et réglementaires en vigueur, des usages professionnels et déontologiques ainsi que des orientations stratégiques de la banque.",
                "HIÉRARCHIE": "Reporte au Directeur de l'Audit Interne",
                "MISSIONS PRINCIPALES": [
                    "Contrôler le respect des règles et procédures internes de la banque",
                    "Vérifier la conformité aux dispositions législatives et réglementaires",
                    "Auditer les usages professionnels et déontologiques",
                    "Suivre l'application des orientations stratégiques de la banque",
                    "Réaliser des missions d'audit selon le plan annuel",
                    "Rédiger les rapports d'audit et formuler des recommandations"
                ],
                "PROFIL RECHERCHÉ": {
                    "Formation": "BAC+4/5 en Audit, Finance, Comptabilité",
                    "Expérience": "2 à 5 ans en audit bancaire",
                    "Secteur": "Bancaire de préférence"
                },
                "COMPÉTENCES": [
                    "Connaissance de la réglementation bancaire BCEAO",
                    "Maîtrise des techniques d'audit",
                    "Capacité d'analyse et de synthèse",
                    "Rigueur et confidentialité"
                ],
                "CANDIDATURE": {
                    "Site web": "cotedivoire.coris.bank",
                    "Date publication": "Septembre 2025"
                }
            }
        },
        {
            "numero": 4,
            "titre": "AUDITEUR INTERNE JUNIOR",
            "entreprise": "SIKA FINANCE",
            "localisation": "Abidjan, Côte d'Ivoire",
            "contrat": "CDI",
            "details": {
                "MISSION": "Effectuer des contrôles périodiques et des investigations afin de détecter les éventuels dysfonctionnements organisationnels, réglementaires, économiques et humains de la Banque.",
                "ACTIVITÉS PRINCIPALES": [
                    "Donner une assurance raisonnable sur la qualité du contrôle interne",
                    "Participer à l'élaboration de la charte éthique et du code de déontologie",
                    "Préparer et exécuter les missions d'audit interne",
                    "Rédiger les rapports d'audit et présenter les résultats",
                    "Contribuer au suivi des recommandations auprès des entités concernées",
                    "Veiller au respect des règles en vigueur",
                    "Participer à des missions d'investigation",
                    "Assurer le contrôle interne de ses propres activités"
                ],
                "PROFIL EXIGÉ": {
                    "Formation": "BAC+4/5 en Audit et Contrôle, Sciences Économiques, Banque, Finance, Comptabilité",
                    "Expérience": "1 an minimum dans l'Audit et le Contrôle Interne"
                },
                "COMPÉTENCES TECHNIQUES": [
                    "Techniques d'entretien, d'audit et d'investigation",
                    "Connaissance des activités et opérations bancaires",
                    "Connaissance de la réglementation bancaire",
                    "Maîtrise de la cartographie des risques et de leur gestion",
                    "Connaissance des logiciels de gestion bancaire",
                    "Maîtrise des outils bureautiques"
                ],
                "QUALITÉS PERSONNELLES": [
                    "Sens de l'organisation, rigueur et méthode",
                    "Disponibilité et bonne communication orale et écrite",
                    "Intégrité et objectivité",
                    "Capacité d'analyse et de synthèse",
                    "Confidentialité et esprit critique",
                    "Capacité à gérer la pression"
                ],
                "CANDIDATURE": {
                    "Site": "sikafinance.com",
                    "Objet": "AUDITEUR INTERNE JUNIOR"
                }
            }
        },
        {
            "numero": 5,
            "titre": "AUDITEUR INTERNE JUNIOR (H/F)",
            "entreprise": "CBAO - Groupe Attijariwafa Bank",
            "localisation": "Abidjan, Côte d'Ivoire",
            "contrat": "CDI",
            "details": {
                "À PROPOS DE CBAO": "CBAO, fondée en 1853, est une filiale du Groupe Attijariwafa bank, premier Groupe Bancaire du Maghreb. CBAO compte 88 agences, près de 400 000 clients, plus de 1000 collaborateurs et 3 succursales (Burkina Faso, Bénin, Niger).",
                "HIÉRARCHIE": "Rattaché au Manager Audit Interne",
                "MISSIONS DU POSTE": [
                    "Dérouler des travaux de contrôle et d'évaluation des dispositifs de maîtrise des risques",
                    "Évaluer la conformité et la qualité des processus opérationnels sur un périmètre délimité",
                    "Rédiger les rapports de mission d'audit et présenter des recommandations",
                    "Suivre la mise en place des recommandations émises",
                    "Gérer le classement des fichiers et dossiers de travail",
                    "Réaliser des travaux méthodologiques (référentiels, guides d'audit)",
                    "Réaliser des analyses et préparer des documents projets",
                    "Consolider les informations et élaborer des livrables projets",
                    "Élaborer des états d'avancement conformément au planning"
                ],
                "PROFIL RECHERCHÉ": {
                    "Formation": "BAC+4/5 en Audit et Contrôle de Gestion ou Finance",
                    "Expérience": "1 à 3 ans minimum en Banque ou cabinet d'Audit"
                },
                "SAVOIRS REQUIS": [
                    "Compréhension fine des processus sous contrôle",
                    "Capacité à coordonner une mission d'audit complète",
                    "Formulation de recommandations globales",
                    "Connaissance du fonctionnement bancaire",
                    "Connaissance des risques inhérents aux activités bancaires",
                    "Analyse financière et bases comptables solides",
                    "Identification des différentes natures de risques",
                    "Établissement de planning et priorisation des actions",
                    "Application de plans d'assurance qualité"
                ],
                "QUALITÉS": "Organisé, rigoureux, flexible, courtois, discret et curieux",
                "CANDIDATURE": {
                    "Site": "lesopportunites.com",
                    "Référence": "Date limite historique : Décembre 2023"
                }
            }
        },
        {
            "numero": 6,
            "titre": "AUDITEUR INTERNE SENIOR (H/F) - INDUSTRIE",
            "entreprise": "ELITE INTERIM CI",
            "localisation": "Côte d'Ivoire",
            "contrat": "CDI / Mission",
            "details": {
                "SECTEUR": "Industrie manufacturière",
                "NIVEAU": "Manager / Responsable département (6 à 10 ans d'expérience)",
                "PROFIL RECHERCHÉ": {
                    "Expérience": "6 à 10 ans minimum en audit industriel",
                    "Niveau": "Manager / Responsable département",
                    "Secteur": "Industrie (toutes branches)"
                },
                "COMPÉTENCES CLÉS": [
                    "Audit des processus industriels et de production",
                    "Contrôle de gestion industrielle",
                    "Connaissance des normes ISO (9001, 14001, 45001)",
                    "Gestion des risques industriels et opérationnels",
                    "Audit supply chain et logistique",
                    "Évaluation des systèmes de contrôle qualité",
                    "Audit énergétique et environnemental"
                ],
                "RESPONSABILITÉS": [
                    "Planifier et réaliser les audits des sites industriels",
                    "Évaluer la conformité aux normes et réglementations",
                    "Identifier les risques opérationnels et proposer des solutions",
                    "Manager une équipe d'auditeurs",
                    "Présenter les résultats à la direction"
                ],
                "CANDIDATURE": {
                    "Source": "NovoJob.com - Elite Interim CI",
                    "Date publication": "Septembre 2026"
                }
            }
        },
        {
            "numero": 7,
            "titre": "HEAD OF INTERNAL AUDIT & CONTROL",
            "entreprise": "TEAMACE",
            "localisation": "Afrique de l'Ouest (postes similaires en CI)",
            "contrat": "CDI",
            "details": {
                "MISSIONS PRINCIPALES": [
                    "Développer et exécuter les plans d'audit basés sur les risques",
                    "Réviser les contrôles internes et les procédures",
                    "Maintenir la charte d'audit et la méthodologie",
                    "Assurer l'efficacité et la qualité des audits",
                    "Superviser l'équipe d'audit interne",
                    "Rapporter directement au comité d'audit"
                ],
                "PROFIL RECHERCHÉ": {
                    "Expérience": "8 ans minimum dont 3 ans en position de management",
                    "Formation": "Finance, Comptabilité, Audit",
                    "Certifications": "CIA, ACCA, CPA (souhaité)"
                },
                "COMPÉTENCES": [
                    "Leadership et management d'équipe",
                    "Méthodologies d'audit avancées (risk-based audit)",
                    "Connaissance des réglementations bancaires/financières",
                    "Excellentes compétences en communication et présentation",
                    "Maîtrise des outils d'audit (ACL, IDEA)",
                    "Capacité à interagir avec la haute direction"
                ],
                "RESPONSABILITÉS STRATÉGIQUES": [
                    "Définir la stratégie d'audit de l'organisation",
                    "Évaluer et améliorer le système de contrôle interne",
                    "Assurer la conformité réglementaire",
                    "Gérer les relations avec les auditeurs externes",
                    "Développer les compétences de l'équipe"
                ],
                "CANDIDATURE": {
                    "Source": "Indeed.com / Teamace",
                    "Localisation": "Lagos (Nigeria) - Opportunités CI"
                }
            }
        },
        {
            "numero": 8,
            "titre": "HEAD, INTERNAL CONTROL AND AUDIT",
            "entreprise": "CARDINALSTONE REGISTRARS",
            "localisation": "Services financiers (Afrique de l'Ouest)",
            "contrat": "CDI",
            "details": {
                "RESPONSABILITÉS PRINCIPALES": [
                    "Concevoir le plan d'audit annuel de l'entreprise",
                    "Conduire des audits périodiques des différentes unités",
                    "Évaluer les risques et l'efficacité des contrôles",
                    "Assurer le reporting à la direction générale et au conseil",
                    "Coordonner avec les auditeurs externes",
                    "Suivre la mise en œuvre des recommandations"
                ],
                "PROFIL RECHERCHÉ": {
                    "Expérience": "5 à 8 ans en audit interne",
                    "Secteur": "Services financiers, registrariat, bourses",
                    "Formation": "Comptabilité, Audit, Finance"
                },
                "COMPÉTENCES CLÉS": [
                    "Audit des services financiers",
                    "Connaissance des réglementations des marchés financiers",
                    "Gestion des risques de conformité",
                    "Évaluation des systèmes d'information",
                    "Audit de la sécurité des données"
                ],
                "ENVIRONNEMENT DE TRAVAIL": "Entreprise de services financiers spécialisée dans le registrariat et la gestion des actionnaires, avec des exigences élevées en matière de conformité et de sécurité des données.",
                "CANDIDATURE": {
                    "Source": "Indeed.com / Cardinalstone",
                    "Note": "Postes similaires disponibles en Côte d'Ivoire"
                }
            }
        },
        {
            "numero": 9,
            "titre": "INTERNAL AUDIT PARTNER",
            "entreprise": "RENMONEY",
            "localisation": "FinTech / Services financiers digitaux",
            "contrat": "CDI - Niveau Partner",
            "details": {
                "MISSIONS PRINCIPALES": [
                    "Conduire l'évaluation stratégique des risques",
                    "Auditer les départements selon le plan d'audit approuvé",
                    "Suivre la résolution de toutes les recommandations d'audit/contrôle",
                    "Assurer la mise en œuvre effective des contrôles",
                    "Conseiller la direction sur les meilleures pratiques",
                    "Superviser les audits spéciaux et investigations"
                ],
                "PROFIL RECHERCHÉ": {
                    "Expérience": "7 ans minimum en audit, dont 3 ans en FinTech/services financiers",
                    "Niveau": "Partner / Associé",
                    "Secteur": "FinTech, Microfinance, Services financiers digitaux"
                },
                "COMPÉTENCES SPÉCIFIQUES": [
                    "Audit basé sur les risques (Risk-Based Audit)",
                    "Compréhension des technologies FinTech",
                    "Audit des systèmes d'information et cybersécurité",
                    "Connaissance des réglementations FinTech",
                    "Gestion des risques de fraude et AML/CFT",
                    "Leadership stratégique et influence"
                ],
                "RESPONSABILITÉS STRATÉGIQUES": [
                    "Participer à la définition de la stratégie de contrôle",
                    "Identifier les risques émergents dans le secteur FinTech",
                    "Développer des méthodologies d'audit innovantes",
                    "Représenter l'audit auprès des régulateurs",
                    "Mentorer les équipes d'audit"
                ],
                "ENVIRONNEMENT": "FinTech en forte croissance, environnement dynamique et innovant, avec des défis spécifiques liés à la transformation digitale et aux nouveaux modèles d'affaires.",
                "CANDIDATURE": {
                    "Source": "Indeed.com / Renmoney",
                    "Localisation": "Lagos (Nigeria) - Opportunités Afrique de l'Ouest"
                }
            }
        },
        {
            "numero": 10,
            "titre": "AUDITEUR QUALITÉ INTERNE",
            "entreprise": "NSIA BANQUE CÔTE D'IVOIRE",
            "localisation": "Abidjan, Côte d'Ivoire",
            "contrat": "CDI",
            "details": {
                "PROFIL REQUIS": {
                    "Formation": "BAC+4/5 en Qualité, Management de la Qualité ou domaine connexe",
                    "Expérience": "Au moins 3 ans en audit qualité ou gestion de la qualité",
                    "Certifications": "Auditeur ISO 9001 certifié (souhaité)"
                },
                "MISSIONS PRINCIPALES": [
                    "Réaliser les audits qualité internes selon le planning annuel",
                    "Évaluer la conformité aux normes ISO (9001, 27001, etc.)",
                    "Vérifier l'application des procédures et processus qualité",
                    "Proposer des actions correctives et préventives",
                    "Former les équipes aux processus qualité",
                    "Suivre les indicateurs de performance qualité (KPIs)",
                    "Préparer les audits de certification externes",
                    "Accompagner les services dans l'amélioration continue"
                ],
                "COMPÉTENCES REQUISES": [
                    "Connaissance approfondie des normes ISO 9001, 27001",
                    "Maîtrise des méthodologies d'audit qualité",
                    "Connaissance des outils de gestion de la qualité (6 Sigma, Lean)",
                    "Capacité d'analyse et de synthèse",
                    "Excellentes compétences en communication et pédagogie",
                    "Rigueur et sens du détail"
                ],
                "OUTILS ET MÉTHODES": [
                    "Diagrammes de cause à effet (Ishikawa)",
                    "PDCA (Plan-Do-Check-Act)",
                    "AMDEC (Analyse des Modes de Défaillance)",
                    "Cartographie des processus",
                    "Tableaux de bord qualité"
                ],
                "SECTEUR": "Bancaire - Focus sur la qualité de service et la conformité réglementaire",
                "CANDIDATURE": {
                    "Date limite": "29 janvier 2026",
                    "Source": "NSIA Banque CI",
                    "Référence": "Scribd.com - Avis de recrutement"
                }
            }
        }
    ]
    
    # Générer chaque PDF
    print(f"\n🚀 Génération de {len(offres)} PDFs individuels...\n")
    
    pdfs_crees = []
    for offre in offres:
        try:
            pdf_path = creer_pdf_offre(
                numero=offre["numero"],
                titre=offre["titre"],
                entreprise=offre["entreprise"],
                localisation=offre["localisation"],
                contrat=offre["contrat"],
                details=offre["details"],
                output_dir=output_dir
            )
            pdfs_crees.append(pdf_path)
        except Exception as e:
            print(f"❌ Erreur pour l'offre {offre['numero']} : {e}")
    
    print(f"\n✅ {len(pdfs_crees)} PDFs créés avec succès dans :")
    print(f"   {output_dir}\n")
    
    return pdfs_crees

if __name__ == "__main__":
    try:
        pdfs = generer_toutes_les_offres()
        print("📄 Fichiers créés :")
        for pdf in pdfs:
            print(f"   • {os.path.basename(pdf)}")
    except Exception as e:
        print(f"❌ Erreur générale : {e}")
        import traceback
        traceback.print_exc()
