"""
Exemple 3: Convertir un tableau Excel vers Word avec style
"""

import pandas as pd
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

def excel_vers_word_style(fichier_excel, fichier_word, nom_feuille=0):
    """
    Convertit un fichier Excel en document Word avec tableau stylé
    
    Args:
        fichier_excel: Chemin du fichier Excel
        fichier_word: Chemin du fichier Word de sortie
        nom_feuille: Nom ou index de la feuille (défaut: première feuille)
    """
    # Lire le fichier Excel
    df = pd.read_excel(fichier_excel, sheet_name=nom_feuille)
    
    # Créer le document Word
    doc = Document()
    
    # Titre
    titre = doc.add_heading('Rapport de Données', 0)
    titre.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    # Ajouter un paragraphe
    doc.add_paragraph(f'Ce rapport contient {len(df)} lignes et {len(df.columns)} colonnes.')
    doc.add_paragraph()  # Ligne vide
    
    # Créer le tableau
    table = doc.add_table(rows=1, cols=len(df.columns))
    table.style = 'Light Grid Accent 1'
    
    # En-têtes
    hdr_cells = table.rows[0].cells
    for i, column_name in enumerate(df.columns):
        cell = hdr_cells[i]
        cell.text = str(column_name)
        # Style de l'en-tête
        run = cell.paragraphs[0].runs[0]
        run.font.bold = True
        run.font.size = Pt(12)
        cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    # Données
    for _, row in df.iterrows():
        row_cells = table.add_row().cells
        for i, value in enumerate(row):
            cell = row_cells[i]
            cell.text = str(value)
            cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    # Ajuster la largeur des colonnes
    for row in table.rows:
        for cell in row.cells:
            cell.width = Inches(1.5)
    
    # Sauvegarder
    doc.save(fichier_word)
    
    print(f"✅ Document Word créé: {fichier_word}")
    print(f"   Lignes: {len(df)}")
    print(f"   Colonnes: {len(df.columns)}")


def creer_excel_exemple():
    """Crée un fichier Excel d'exemple"""
    data = {
        'Produit': ['Ordinateur', 'Souris', 'Clavier', 'Écran', 'Imprimante'],
        'Prix (€)': [899, 25, 45, 299, 199],
        'Stock': [15, 120, 85, 30, 22],
        'Fournisseur': ['TechCorp', 'Logitech', 'Microsoft', 'Samsung', 'HP']
    }
    
    df = pd.DataFrame(data)
    fichier = "../Base_excel/exemple_inventaire.xlsx"
    df.to_excel(fichier, index=False)
    
    print(f"✅ Fichier Excel d'exemple créé: {fichier}")
    return fichier


if __name__ == "__main__":
    print("=" * 60)
    print("Exemple: Conversion Excel → Word avec style")
    print("=" * 60)
    print()
    
    # Créer un fichier Excel d'exemple
    fichier_excel = creer_excel_exemple()
    
    # Convertir en Word
    excel_vers_word_style(
        fichier_excel,
        "../Base_excel/rapport_inventaire.docx"
    )
    
    print("\n✨ Conversion terminée avec succès!")
    print("📄 Vérifiez le fichier: ../Base_excel/rapport_inventaire.docx")
