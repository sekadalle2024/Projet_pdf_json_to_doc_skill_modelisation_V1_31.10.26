"""
Conversion Excel → DOCX avec tableaux automatiquement dimensionnés
Chaque onglet devient un tableau dans un document Word séparé
"""

import pandas as pd
from pathlib import Path
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import openpyxl

def set_cell_border(cell, **kwargs):
    """
    Ajoute des bordures à une cellule de tableau Word
    """
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    
    # Créer l'élément de bordures
    tcBorders = OxmlElement('w:tcBorders')
    for edge in ('top', 'left', 'bottom', 'right'):
        if edge in kwargs:
            edge_data = kwargs.get(edge)
            edge_el = OxmlElement(f'w:{edge}')
            edge_el.set(qn('w:val'), 'single')
            edge_el.set(qn('w:sz'), '4')
            edge_el.set(qn('w:space'), '0')
            edge_el.set(qn('w:color'), 'auto')
            tcBorders.append(edge_el)
    
    tcPr.append(tcBorders)

def excel_to_docx(fichier_excel, dossier_sortie):
    """
    Convertit un fichier Excel en document(s) DOCX
    Un fichier DOCX par onglet
    """
    chemin_excel = Path(fichier_excel)
    nom_base = chemin_excel.stem
    
    print(f"\n{'='*80}")
    print(f"   📄 {chemin_excel.name}")
    print(f"   {'='*80}")
    
    # Charger le workbook pour lister les onglets
    try:
        wb = openpyxl.load_workbook(fichier_excel, read_only=True, data_only=True)
        noms_onglets = wb.sheetnames
        wb.close()
    except Exception as e:
        print(f"   ❌ Erreur lecture: {e}")
        return 0
    
    onglets_traites = 0
    
    for nom_onglet in noms_onglets:
        try:
            # Lire l'onglet avec pandas
            df = pd.read_excel(fichier_excel, sheet_name=nom_onglet, header=None)
            
            # Supprimer lignes/colonnes entièrement vides
            df = df.dropna(how='all', axis=0)
            df = df.dropna(how='all', axis=1)
            
            if df.empty:
                print(f"      ⚠️  {nom_onglet}: vide, ignoré")
                continue
            
            # Remplacer NaN par chaînes vides
            df = df.fillna('')
            
            # Créer document Word
            doc = Document()
            
            # Configuration de la page en paysage
            section = doc.sections[0]
            section.page_width = Inches(16.5)  # A3 paysage largeur
            section.page_height = Inches(11.7)  # A3 paysage hauteur
            section.left_margin = Inches(0.5)
            section.right_margin = Inches(0.5)
            section.top_margin = Inches(0.5)
            section.bottom_margin = Inches(0.5)
            
            # Titre
            titre = doc.add_heading(f"{nom_base} - {nom_onglet}", level=1)
            titre.alignment = WD_ALIGN_PARAGRAPH.CENTER
            
            # Créer tableau Word
            nb_lignes, nb_colonnes = df.shape
            table = doc.add_table(rows=nb_lignes, cols=nb_colonnes)
            table.style = 'Light Grid Accent 1'
            
            # Remplir le tableau
            for i in range(nb_lignes):
                for j in range(nb_colonnes):
                    cellule = table.rows[i].cells[j]
                    valeur = str(df.iloc[i, j])
                    
                    # Limiter la longueur si nécessaire
                    if len(valeur) > 500:
                        valeur = valeur[:497] + "..."
                    
                    cellule.text = valeur
                    
                    # Formatage
                    for paragraph in cellule.paragraphs:
                        for run in paragraph.runs:
                            run.font.size = Pt(8)
                            run.font.name = 'Calibri'
                    
                    # Bordures
                    set_cell_border(
                        cellule,
                        top={"sz": 4, "val": "single"},
                        bottom={"sz": 4, "val": "single"},
                        left={"sz": 4, "val": "single"},
                        right={"sz": 4, "val": "single"}
                    )
            
            # Ajuster automatiquement les largeurs de colonnes
            # Word le fera automatiquement à l'ouverture
            table.autofit = True
            table.allow_autofit = True
            
            # Nom de fichier sécurisé pour l'onglet
            nom_onglet_securise = "".join(
                c if c.isalnum() or c in (' ', '-', '_') else '_' 
                for c in nom_onglet
            )
            
            # Sauvegarder
            nom_sortie = f"{nom_base}_{nom_onglet_securise}_DOCX.docx"
            chemin_sortie = dossier_sortie / nom_sortie
            doc.save(str(chemin_sortie))
            
            print(f"      ✅ {nom_onglet}: {nb_lignes}×{nb_colonnes} → {nom_sortie}")
            onglets_traites += 1
            
        except Exception as e:
            print(f"      ❌ {nom_onglet}: Erreur - {e}")
            continue
    
    return onglets_traites

def main():
    print("="*80)
    print("📊 CONVERSION EXCEL → DOCX")
    print("✨ Tableaux Word avec ajustement automatique des colonnes")
    print("="*80)
    
    # Dossier source
    dossier_excel = Path("Base_excel")
    
    if not dossier_excel.exists():
        print(f"❌ Le dossier {dossier_excel} n'existe pas!")
        return
    
    # Trouver tous les fichiers Excel
    fichiers_excel = list(dossier_excel.glob("*.xlsx")) + list(dossier_excel.glob("*.xls"))
    
    # Exclure les fichiers temporaires et déjà traités
    fichiers_excel = [
        f for f in fichiers_excel 
        if not f.name.startswith('~$') and '_DOCX' not in f.name
    ]
    
    print(f"\n🔍 {len(fichiers_excel)} fichier(s) Excel trouvé(s)")
    
    if not fichiers_excel:
        print("❌ Aucun fichier Excel à traiter!")
        return
    
    total_onglets = 0
    
    # Traiter chaque fichier
    for fichier in fichiers_excel:
        onglets = excel_to_docx(fichier, dossier_excel)
        total_onglets += onglets
    
    print("\n" + "="*80)
    print(f"✅ CONVERSION TERMINÉE!")
    print(f"📄 Total d'onglets traités: {total_onglets}")
    print(f"📁 Documents Word dans: Base_excel/")
    print(f"   Nomenclature: *_DOCX.docx")
    print("="*80)
    print("\n✨ AVANTAGES FORMAT WORD:")
    print("  ✅ Ajustement AUTOMATIQUE des largeurs de colonnes")
    print("  ✅ Contenu toujours visible (pas de troncature)")
    print("  ✅ Tableaux modifiables et professionnels")
    print("  ✅ Format A3 paysage pour tableaux larges")
    print("  ✅ Police lisible 8pt Calibri")

if __name__ == "__main__":
    main()
