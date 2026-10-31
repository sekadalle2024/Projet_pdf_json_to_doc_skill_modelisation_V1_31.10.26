#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
Script de Conversion JSON vers Word - Cas 12 : Cartographie des Risques
================================================================================

Auteur: Afrika Group Holdings - Département Audit & Contrôle Interne
Date de création: 31 octobre 2026
Version: 1.0.0

Description:
    Convertit les données JSON de cartographie des risques en documents Word
    formatés selon le référentiel COSO ERM 2017, ISO 31000:2018 et BCEAO.
    
    Ce script gère 20 colonnes de données pour une cartographie complète:
    - Identification des risques (processus, catégorie, cause racine)
    - Évaluation des risques (probabilité, impact, risque inhérent)
    - Contrôles (préventif, détectif, correctif, efficacité)
    - Traitement (risque résiduel, propriétaire, recommandations)

Structure des colonnes (20):
    1. Processus
    2. Sous-processus
    3. Risque identifié
    4. Catégorie de risque
    5. Cause racine
    6. Événement déclencheur
    7. Impact potentiel
    8. Probabilité
    9. Impact
    10. Risque inhérent
    11. Contrôle préventif
    12. Contrôle détectif
    13. Contrôle correctif
    14. Efficacité contrôle
    15. Risque résiduel
    16. Propriétaire du risque
    17. Statut traitement
    18. Recommandation
    19. Échéance
    20. Coût traitement

Conformité réglementaire:
    - ISO 31000:2018 (Management du risque)
    - COSO ERM 2017 (Enterprise Risk Management)
    - Référentiel BCEAO/Commission Bancaire UMOA
    - Normes IIA (Institute of Internal Auditors)

Dépendances:
    - python-docx >= 0.8.11
    - Pillow >= 9.0.0

Usage:
    python json2word_cartographie_risques.py
    
    Le script recherche automatiquement les fichiers JSON dans le dossier
    et génère les documents Word correspondants.

================================================================================
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Any, Tuple, Optional
from datetime import datetime

# Import de python-docx avec gestion des erreurs
try:
    from docx import Document
    from docx.shared import Inches, Pt, RGBColor, Cm
    from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
    from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
    from docx.oxml.ns import qn
    from docx.oxml import OxmlElement
except ImportError as e:
    print("=" * 80)
    print("ERREUR: Module python-docx non installé")
    print("=" * 80)
    print(f"\nDétails: {e}")
    print("\nPour installer python-docx:")
    print("  pip install python-docx")
    print("\nOu avec conda:")
    print("  conda install -c conda-forge python-docx")
    print("=" * 80)
    sys.exit(1)


# ==============================================================================
# CONFIGURATION GLOBALE
# ==============================================================================

# Couleurs de marque Afrika Group Holdings
COULEUR_PRINCIPALE = RGBColor(0, 51, 102)      # Bleu foncé corporate
COULEUR_SECONDAIRE = RGBColor(255, 140, 0)     # Orange Afrika
COULEUR_HEADER = RGBColor(51, 51, 51)          # Gris anthracite
COULEUR_TEXTE = RGBColor(64, 64, 64)           # Gris texte

# Couleurs de niveau de risque (heat map)
COULEUR_RISQUE_CRITIQUE = RGBColor(139, 0, 0)   # Rouge foncé
COULEUR_RISQUE_ELEVE = RGBColor(255, 0, 0)      # Rouge
COULEUR_RISQUE_MOYEN = RGBColor(255, 140, 0)    # Orange
COULEUR_RISQUE_FAIBLE = RGBColor(255, 215, 0)   # Jaune
COULEUR_RISQUE_TRES_FAIBLE = RGBColor(50, 205, 50)  # Vert

# Marges du document (en cm)
MARGE_HAUTE = 2.0
MARGE_BASSE = 2.0
MARGE_GAUCHE = 2.5
MARGE_DROITE = 2.0

# Police de caractères
POLICE_TITRE = "Calibri"
POLICE_CORPS = "Calibri"
POLICE_TABLEAU = "Calibri"

# Tailles de police
TAILLE_TITRE_PRINCIPAL = 16
TAILLE_TITRE_SECTION = 14
TAILLE_SOUS_TITRE = 11
TAILLE_TEXTE = 10
TAILLE_TABLEAU_HEADER = 9
TAILLE_TABLEAU_CELLULE = 9
TAILLE_PIED_PAGE = 8

# Mappings des niveaux de risque
NIVEAU_RISQUE_MAPPING = {
    "20": ("Critique", COULEUR_RISQUE_CRITIQUE),
    "15": ("Élevé", COULEUR_RISQUE_ELEVE),
    "12": ("Élevé", COULEUR_RISQUE_ELEVE),
    "10": ("Moyen", COULEUR_RISQUE_MOYEN),
    "8": ("Moyen", COULEUR_RISQUE_MOYEN),
    "6": ("Moyen", COULEUR_RISQUE_MOYEN),
    "4": ("Faible", COULEUR_RISQUE_FAIBLE),
    "3": ("Faible", COULEUR_RISQUE_FAIBLE),
    "2": ("Très faible", COULEUR_RISQUE_TRES_FAIBLE),
    "1": ("Très faible", COULEUR_RISQUE_TRES_FAIBLE),
}


# ==============================================================================
# FONCTIONS UTILITAIRES
# ==============================================================================

def nettoyer_texte(texte: Any) -> str:
    """
    Nettoie et normalise le texte.
    
    Args:
        texte: Texte à nettoyer (peut être None, str, int, float, list, dict)
        
    Returns:
        Texte nettoyé et normalisé
    """
    if texte is None:
        return ""
    
    if isinstance(texte, (int, float)):
        return str(texte)
    
    if isinstance(texte, list):
        return " | ".join(str(item) for item in texte)
    
    if isinstance(texte, dict):
        return str(texte)
    
    texte_str = str(texte).strip()
    
    # Remplacer les sauts de ligne multiples
    texte_str = texte_str.replace("\r\n", "\n").replace("\r", "\n")
    
    # Normaliser les espaces
    lignes = [ligne.strip() for ligne in texte_str.split("\n")]
    texte_str = "\n".join(ligne for ligne in lignes if ligne)
    
    return texte_str


def extraire_niveau_risque(texte_risque: str) -> Tuple[str, str, RGBColor]:
    """
    Extrait le niveau de risque et retourne le niveau, le label et la couleur.
    
    Args:
        texte_risque: Texte du risque (ex: "12 - Élevé (Rouge)")
        
    Returns:
        Tuple (score, niveau, couleur)
    """
    texte_risque = str(texte_risque).strip()
    
    # Extraire le score numérique
    score = ""
    for char in texte_risque:
        if char.isdigit():
            score += char
        elif score:
            break
    
    if score in NIVEAU_RISQUE_MAPPING:
        niveau, couleur = NIVEAU_RISQUE_MAPPING[score]
        return score, niveau, couleur
    
    # Par défaut
    return score or "N/A", "Non évalué", COULEUR_TEXTE


def formater_date(date_str: Optional[str] = None) -> str:
    """
    Formate une date au format standard français.
    
    Args:
        date_str: Date au format ISO ou None pour la date actuelle
        
    Returns:
        Date formatée (ex: "31 octobre 2026")
    """
    if date_str is None:
        date_obj = datetime.now()
    else:
        try:
            date_obj = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
        except (ValueError, AttributeError):
            date_obj = datetime.now()
    
    mois = [
        "janvier", "février", "mars", "avril", "mai", "juin",
        "juillet", "août", "septembre", "octobre", "novembre", "décembre"
    ]
    
    return f"{date_obj.day} {mois[date_obj.month - 1]} {date_obj.year}"


# ==============================================================================
# FONCTIONS DE FORMATAGE WORD
# ==============================================================================

def configurer_marges(doc: Document) -> None:
    """Configure les marges du document."""
    sections = doc.sections
    for section in sections:
        section.top_margin = Cm(MARGE_HAUTE)
        section.bottom_margin = Cm(MARGE_BASSE)
        section.left_margin = Cm(MARGE_GAUCHE)
        section.right_margin = Cm(MARGE_DROITE)


def ajouter_bordure_paragraphe(paragraph, couleur: RGBColor = COULEUR_PRINCIPALE, 
                                 epaisseur: int = 4) -> None:
    """
    Ajoute une bordure en bas d'un paragraphe.
    
    Args:
        paragraph: Paragraphe cible
        couleur: Couleur de la bordure
        epaisseur: Épaisseur en pt
    """
    p = paragraph._element
    pPr = p.get_or_add_pPr()
    pBdr = OxmlElement('w:pBdr')
    
    bottom = OxmlElement('w:bottom')
    bottom.set(qn('w:val'), 'single')
    bottom.set(qn('w:sz'), str(epaisseur * 2))
    bottom.set(qn('w:space'), '1')
    # RGBColor n'a pas d'attribut .rgb, accès direct aux valeurs
    r, g, b = couleur
    bottom.set(qn('w:color'), f'{r:02X}{g:02X}{b:02X}')
    
    pBdr.append(bottom)
    pPr.append(pBdr)


def creer_en_tete_document(doc: Document, infos_table1: Dict[str, Any]) -> None:
    """
    Crée l'en-tête du document avec les métadonnées.
    
    Args:
        doc: Document Word
        infos_table1: Dictionnaire des informations de la table 1
    """
    # Titre principal
    titre = doc.add_paragraph()
    titre_run = titre.add_run("CARTOGRAPHIE DES RISQUES")
    titre_run.font.name = POLICE_TITRE
    titre_run.font.size = Pt(TAILLE_TITRE_PRINCIPAL)
    titre_run.font.color.rgb = COULEUR_PRINCIPALE
    titre_run.font.bold = True
    titre.alignment = WD_ALIGN_PARAGRAPH.CENTER
    titre.space_after = Pt(6)
    
    # Sous-titre
    etablissement = nettoyer_texte(infos_table1.get("Etablissement", ""))
    if etablissement:
        sous_titre = doc.add_paragraph()
        sous_titre_run = sous_titre.add_run(etablissement)
        sous_titre_run.font.name = POLICE_TITRE
        sous_titre_run.font.size = Pt(TAILLE_SOUS_TITRE)
        sous_titre_run.font.color.rgb = COULEUR_SECONDAIRE
        sous_titre_run.font.bold = True
        sous_titre.alignment = WD_ALIGN_PARAGRAPH.CENTER
        sous_titre.space_after = Pt(12)
    
    # Ligne de séparation
    separateur = doc.add_paragraph()
    ajouter_bordure_paragraphe(separateur, COULEUR_PRINCIPALE, 6)
    separateur.space_after = Pt(12)
    
    # Tableau de métadonnées (2 colonnes)
    table_meta = doc.add_table(rows=0, cols=2)
    table_meta.style = 'Light Grid Accent 1'
    table_meta.alignment = WD_TABLE_ALIGNMENT.CENTER
    
    # Configuration de la largeur des colonnes
    table_meta.columns[0].width = Cm(5.0)
    table_meta.columns[1].width = Cm(11.0)
    
    # Champs de métadonnées à afficher
    champs_meta = [
        ("Document", infos_table1.get("Document", "")),
        ("Processus", infos_table1.get("Processus", "")),
        ("Cycle d'activité", infos_table1.get("Cycle d'activité", "")),
        ("Secteur d'activité", infos_table1.get("Secteur d'activité", "")),
        ("Méthodologie", infos_table1.get("Méthodologie", "")),
        ("Périmètre", infos_table1.get("Périmètre", "")),
        ("Référence", infos_table1.get("Reference", "")),
        ("Version", infos_table1.get("Version", "")),
        ("Date d'élaboration", infos_table1.get("Date d'élaboration", formater_date())),
        ("Approbation", infos_table1.get("Approbation", "")),
        ("Responsable", infos_table1.get("Responsable", "")),
    ]
    
    for label, valeur in champs_meta:
        valeur_clean = nettoyer_texte(valeur)
        if not valeur_clean:
            continue
        
        row = table_meta.add_row()
        
        # Cellule label
        cell_label = row.cells[0]
        p_label = cell_label.paragraphs[0]
        run_label = p_label.add_run(label)
        run_label.font.name = POLICE_CORPS
        run_label.font.size = Pt(9)
        run_label.font.bold = True
        run_label.font.color.rgb = COULEUR_HEADER
        cell_label.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
        
        # Cellule valeur
        cell_valeur = row.cells[1]
        p_valeur = cell_valeur.paragraphs[0]
        run_valeur = p_valeur.add_run(valeur_clean)
        run_valeur.font.name = POLICE_CORPS
        run_valeur.font.size = Pt(9)
        run_valeur.font.color.rgb = COULEUR_TEXTE
        cell_valeur.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
    
    # Espacement après le tableau
    doc.add_paragraph().space_after = Pt(12)


def creer_tableau_risques(doc: Document, risques: List[Dict[str, Any]]) -> None:
    """
    Crée le tableau principal de cartographie des risques.
    
    Args:
        doc: Document Word
        risques: Liste des dictionnaires de risques
    """
    if not risques:
        p = doc.add_paragraph()
        run = p.add_run("⚠ Aucun risque identifié dans les données.")
        run.font.name = POLICE_CORPS
        run.font.size = Pt(TAILLE_TEXTE)
        run.font.color.rgb = COULEUR_SECONDAIRE
        run.font.italic = True
        return
    
    # Titre de section
    titre_section = doc.add_paragraph()
    titre_section_run = titre_section.add_run("MATRICE DES RISQUES ET CONTRÔLES")
    titre_section_run.font.name = POLICE_TITRE
    titre_section_run.font.size = Pt(TAILLE_TITRE_SECTION)
    titre_section_run.font.color.rgb = COULEUR_PRINCIPALE
    titre_section_run.font.bold = True
    titre_section.space_before = Pt(6)
    titre_section.space_after = Pt(6)
    
    # Définition des colonnes (20 colonnes)
    colonnes = [
        "Processus",
        "Sous-processus",
        "Risque identifié",
        "Catégorie de risque",
        "Cause racine",
        "Événement déclencheur",
        "Impact potentiel",
        "Probabilité",
        "Impact",
        "Risque inhérent",
        "Contrôle préventif",
        "Contrôle détectif",
        "Contrôle correctif",
        "Efficacité contrôle",
        "Risque résiduel",
        "Propriétaire du risque",
        "Statut traitement",
        "Recommandation",
        "Échéance",
        "Coût traitement",
    ]
    
    nb_colonnes = len(colonnes)
    
    # Création du tableau
    table = doc.add_table(rows=1, cols=nb_colonnes)
    table.style = 'Light Grid Accent 1'
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    
    # Configuration de la largeur des colonnes (en cm, total = 26 cm pour A4 paysage)
    largeurs_colonnes = [
        1.5,  # Processus
        1.3,  # Sous-processus
        2.5,  # Risque identifié
        1.2,  # Catégorie de risque
        2.0,  # Cause racine
        1.8,  # Événement déclencheur
        2.0,  # Impact potentiel
        1.0,  # Probabilité
        1.0,  # Impact
        1.2,  # Risque inhérent
        1.5,  # Contrôle préventif
        1.5,  # Contrôle détectif
        1.5,  # Contrôle correctif
        1.2,  # Efficacité contrôle
        1.2,  # Risque résiduel
        1.5,  # Propriétaire du risque
        1.0,  # Statut traitement
        2.0,  # Recommandation
        1.0,  # Échéance
        1.0,  # Coût traitement
    ]
    
    for i, largeur in enumerate(largeurs_colonnes):
        table.columns[i].width = Cm(largeur)
    
    # Ligne d'en-tête
    header_cells = table.rows[0].cells
    for i, colonne in enumerate(colonnes):
        cell = header_cells[i]
        cell.text = colonne
        
        # Formatage de l'en-tête
        for paragraph in cell.paragraphs:
            paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
            for run in paragraph.runs:
                run.font.name = POLICE_TABLEAU
                run.font.size = Pt(TAILLE_TABLEAU_HEADER)
                run.font.bold = True
                run.font.color.rgb = RGBColor(255, 255, 255)
        
        # Couleur de fond de l'en-tête
        shading_elm = OxmlElement('w:shd')
        r, g, b = COULEUR_PRINCIPALE
        shading_elm.set(qn('w:fill'), f'{r:02X}{g:02X}{b:02X}')
        cell._element.get_or_add_tcPr().append(shading_elm)
        
        cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
    
    # Lignes de données
    for risque in risques:
        row = table.add_row()
        
        # Extraction des valeurs
        valeurs = [
            nettoyer_texte(risque.get("Processus", "")),
            nettoyer_texte(risque.get("Sous-processus", "")),
            nettoyer_texte(risque.get("Risque identifié", "")),
            nettoyer_texte(risque.get("Catégorie de risque", "")),
            nettoyer_texte(risque.get("Cause racine", "")),
            nettoyer_texte(risque.get("Événement déclencheur", "")),
            nettoyer_texte(risque.get("Impact potentiel", "")),
            nettoyer_texte(risque.get("Probabilité", "")),
            nettoyer_texte(risque.get("Impact", "")),
            nettoyer_texte(risque.get("Risque inhérent", "")),
            nettoyer_texte(risque.get("Contrôle préventif", "")),
            nettoyer_texte(risque.get("Contrôle détectif", "")),
            nettoyer_texte(risque.get("Contrôle correctif", "")),
            nettoyer_texte(risque.get("Efficacité contrôle", "")),
            nettoyer_texte(risque.get("Risque résiduel", "")),
            nettoyer_texte(risque.get("Propriétaire du risque", "")),
            nettoyer_texte(risque.get("Statut traitement", "")),
            nettoyer_texte(risque.get("Recommandation", "")),
            nettoyer_texte(risque.get("Échéance", "")),
            nettoyer_texte(risque.get("Coût traitement", "")),
        ]
        
        # Remplissage des cellules
        for i, valeur in enumerate(valeurs):
            cell = row.cells[i]
            cell.text = valeur
            
            # Formatage de la cellule
            for paragraph in cell.paragraphs:
                # Alignement spécial pour certaines colonnes
                if i in [7, 8, 9, 14, 16]:  # Probabilité, Impact, Risques, Statut
                    paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
                else:
                    paragraph.alignment = WD_ALIGN_PARAGRAPH.LEFT
                
                for run in paragraph.runs:
                    run.font.name = POLICE_TABLEAU
                    run.font.size = Pt(TAILLE_TABLEAU_CELLULE)
                    run.font.color.rgb = COULEUR_TEXTE
            
            # Coloration des cellules de risque
            if i == 9:  # Risque inhérent
                _, _, couleur = extraire_niveau_risque(valeur)
                shading_elm = OxmlElement('w:shd')
                r, g, b = couleur
                shading_elm.set(qn('w:fill'), f'{r:02X}{g:02X}{b:02X}')
                cell._element.get_or_add_tcPr().append(shading_elm)
                
                # Texte en blanc pour meilleure lisibilité
                for paragraph in cell.paragraphs:
                    for run in paragraph.runs:
                        run.font.color.rgb = RGBColor(255, 255, 255)
                        run.font.bold = True
            
            if i == 14:  # Risque résiduel
                _, _, couleur = extraire_niveau_risque(valeur)
                shading_elm = OxmlElement('w:shd')
                r, g, b = couleur
                shading_elm.set(qn('w:fill'), f'{r:02X}{g:02X}{b:02X}')
                cell._element.get_or_add_tcPr().append(shading_elm)
                
                # Texte en blanc pour meilleure lisibilité
                for paragraph in cell.paragraphs:
                    for run in paragraph.runs:
                        run.font.color.rgb = RGBColor(255, 255, 255)
                        run.font.bold = True
            
            cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
    
    # Espacement après le tableau
    doc.add_paragraph().space_after = Pt(12)


def ajouter_pied_de_page(doc: Document) -> None:
    """Ajoute un pied de page professionnel."""
    section = doc.sections[0]
    footer = section.footer
    
    # Ligne de séparation
    p_sep = footer.paragraphs[0]
    ajouter_bordure_paragraphe(p_sep, COULEUR_PRINCIPALE, 2)
    
    # Texte du pied de page
    p_footer = footer.add_paragraph()
    
    # Partie gauche : document confidentiel
    run_conf = p_footer.add_run("Document confidentiel - Afrika Group Holdings")
    run_conf.font.name = POLICE_CORPS
    run_conf.font.size = Pt(TAILLE_PIED_PAGE)
    run_conf.font.color.rgb = COULEUR_TEXTE
    run_conf.font.italic = True
    
    # Partie droite : date de génération
    date_generation = formater_date()
    run_date = p_footer.add_run(f"\t\tGénéré le {date_generation}")
    run_date.font.name = POLICE_CORPS
    run_date.font.size = Pt(TAILLE_PIED_PAGE)
    run_date.font.color.rgb = COULEUR_TEXTE
    run_date.font.italic = True
    
    p_footer.alignment = WD_ALIGN_PARAGRAPH.LEFT


# ==============================================================================
# FONCTION PRINCIPALE DE CONVERSION
# ==============================================================================

def convertir_json_vers_word(fichier_json: Path, dossier_sortie: Path) -> Optional[Path]:
    """
    Convertit un fichier JSON de cartographie des risques en document Word.
    
    Args:
        fichier_json: Chemin du fichier JSON source
        dossier_sortie: Dossier de sortie pour le fichier Word
        
    Returns:
        Chemin du fichier Word généré ou None en cas d'erreur
    """
    print(f"\n{'=' * 80}")
    print(f"Traitement du fichier: {fichier_json.name}")
    print(f"{'=' * 80}")
    
    try:
        # Lecture du fichier JSON
        print("  [1/4] Lecture du fichier JSON...")
        with open(fichier_json, 'r', encoding='utf-8') as f:
            donnees = json.load(f)
        
        # Validation de la structure
        if not isinstance(donnees, dict):
            print("  ❌ ERREUR: Le fichier JSON doit contenir un objet (dictionnaire)")
            return None
        
        # Recherche de la clé principale
        cle_principale = None
        for cle in donnees.keys():
            if "cartographie" in cle.lower() or "risque" in cle.lower():
                cle_principale = cle
                break
        
        if cle_principale is None:
            cle_principale = list(donnees.keys())[0]
        
        print(f"  ✓ Clé principale détectée: '{cle_principale}'")
        
        contenu = donnees[cle_principale]
        
        if not isinstance(contenu, list) or len(contenu) < 2:
            print("  ❌ ERREUR: Format JSON invalide")
            print("     Le contenu doit être une liste avec au moins 2 éléments:")
            print("     - Element 0: table 1 (métadonnées)")
            print("     - Element 1: table 2 (liste des risques)")
            return None
        
        # Extraction de table 1 (métadonnées)
        infos_table1 = {}
        if "table 1" in contenu[0]:
            infos_table1 = contenu[0]["table 1"]
        elif "table1" in contenu[0]:
            infos_table1 = contenu[0]["table1"]
        else:
            print("  ⚠ AVERTISSEMENT: Table 1 non trouvée, utilisation de valeurs par défaut")
        
        # Extraction de table 2 (risques)
        risques = []
        if "table 2" in contenu[1]:
            risques = contenu[1]["table 2"]
        elif "table2" in contenu[1]:
            risques = contenu[1]["table2"]
        else:
            print("  ⚠ AVERTISSEMENT: Table 2 non trouvée, aucun risque à afficher")
        
        print(f"  ✓ {len(risques)} risque(s) identifié(s)")
        
        # Création du document Word
        print("  [2/4] Création du document Word...")
        doc = Document()
        
        # Configuration des marges
        configurer_marges(doc)
        
        # Ajout de l'en-tête
        print("  [3/4] Génération de l'en-tête...")
        creer_en_tete_document(doc, infos_table1)
        
        # Ajout du tableau des risques
        print("  [4/4] Génération du tableau de cartographie...")
        creer_tableau_risques(doc, risques)
        
        # Ajout du pied de page
        ajouter_pied_de_page(doc)
        
        # Génération du nom de fichier de sortie
        nom_base = fichier_json.stem
        nom_sortie = f"{nom_base}_CARTO_WORD.docx"
        chemin_sortie = dossier_sortie / nom_sortie
        
        # Sauvegarde du document
        doc.save(str(chemin_sortie))
        
        # Vérification de la création du fichier
        if chemin_sortie.exists():
            taille_mo = chemin_sortie.stat().st_size / (1024 * 1024)
            print(f"\n  ✅ SUCCÈS: Document Word généré")
            print(f"     Fichier: {chemin_sortie.name}")
            print(f"     Taille: {taille_mo:.2f} Mo")
            print(f"     Emplacement: {chemin_sortie.parent}")
            return chemin_sortie
        else:
            print(f"\n  ❌ ERREUR: Le fichier n'a pas été créé")
            return None
    
    except json.JSONDecodeError as e:
        print(f"\n  ❌ ERREUR JSON: {e}")
        print(f"     Ligne {e.lineno}, Colonne {e.colno}")
        return None
    
    except Exception as e:
        print(f"\n  ❌ ERREUR INATTENDUE: {type(e).__name__}")
        print(f"     {str(e)}")
        import traceback
        traceback.print_exc()
        return None


# ==============================================================================
# FONCTION PRINCIPALE
# ==============================================================================

def main():
    """Point d'entrée principal du script."""
    print("\n" + "=" * 80)
    print("CONVERSION JSON → WORD - CAS 12 : CARTOGRAPHIE DES RISQUES")
    print("Afrika Group Holdings - Département Audit & Contrôle Interne")
    print("=" * 80)
    
    # Détermination des dossiers
    script_dir = Path(__file__).parent
    dossier_sortie = script_dir / "output_word"
    dossier_sortie.mkdir(exist_ok=True)
    
    print(f"\n📁 Dossier de travail: {script_dir}")
    print(f"📁 Dossier de sortie: {dossier_sortie}")
    
    # Recherche des fichiers JSON
    fichiers_json = list(script_dir.glob("exemple_*.json"))
    
    if not fichiers_json:
        print("\n⚠ AUCUN FICHIER JSON TROUVÉ")
        print("\nLe script recherche des fichiers correspondant au pattern:")
        print("  - exemple_*.json")
        print(f"\nDans le dossier: {script_dir}")
        print("\nVeuillez créer ou déplacer vos fichiers JSON dans ce dossier.")
        return
    
    print(f"\n✓ {len(fichiers_json)} fichier(s) JSON trouvé(s)")
    
    # Traitement de chaque fichier
    fichiers_generes = []
    fichiers_erreur = []
    
    for fichier_json in fichiers_json:
        resultat = convertir_json_vers_word(fichier_json, dossier_sortie)
        if resultat:
            fichiers_generes.append(resultat)
        else:
            fichiers_erreur.append(fichier_json)
    
    # Rapport final
    print("\n" + "=" * 80)
    print("RAPPORT FINAL")
    print("=" * 80)
    print(f"\n✅ Fichiers générés avec succès: {len(fichiers_generes)}")
    for fichier in fichiers_generes:
        print(f"   - {fichier.name}")
    
    if fichiers_erreur:
        print(f"\n❌ Fichiers en erreur: {len(fichiers_erreur)}")
        for fichier in fichiers_erreur:
            print(f"   - {fichier.name}")
    
    print("\n" + "=" * 80)
    print(f"Conversion terminée - {len(fichiers_generes)}/{len(fichiers_json)} fichiers traités")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    main()
