#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script de conversion Markdown vers PDF
"""

import markdown
from weasyprint import HTML, CSS
from pathlib import Path

def markdown_to_pdf(md_file, pdf_file):
    """
    Convertit un fichier Markdown en PDF avec mise en forme professionnelle
    """
    # Lire le contenu Markdown
    with open(md_file, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    # Convertir Markdown en HTML
    html_content = markdown.markdown(
        md_content,
        extensions=['tables', 'nl2br', 'sane_lists']
    )
    
    # CSS professionnel pour le PDF
    css_style = """
        @page {
            size: A4;
            margin: 2cm;
            @top-center {
                content: "Offres d'Emploi - Directeurs Audit Interne CI";
                font-size: 10pt;
                color: #666;
            }
            @bottom-right {
                content: "Page " counter(page) " / " counter(pages);
                font-size: 9pt;
                color: #666;
            }
        }
        
        body {
            font-family: 'Arial', 'Helvetica', sans-serif;
            line-height: 1.6;
            color: #333;
            font-size: 11pt;
        }
        
        h1 {
            color: #1a5490;
            font-size: 24pt;
            text-align: center;
            border-bottom: 4px solid #3498db;
            padding-bottom: 15px;
            margin-bottom: 30px;
            page-break-after: avoid;
        }
        
        h2 {
            color: #2980b9;
            font-size: 16pt;
            margin-top: 25px;
            margin-bottom: 15px;
            border-left: 5px solid #3498db;
            padding-left: 15px;
            background-color: #f8f9fa;
            padding-top: 8px;
            padding-bottom: 8px;
            page-break-after: avoid;
        }
        
        h3 {
            color: #34495e;
            font-size: 13pt;
            margin-top: 15px;
            margin-bottom: 10px;
            font-weight: bold;
            page-break-after: avoid;
        }
        
        hr {
            border: none;
            border-top: 2px solid #e0e0e0;
            margin: 25px 0;
            page-break-after: always;
        }
        
        ul, ol {
            margin-left: 25px;
            margin-bottom: 15px;
        }
        
        li {
            margin-bottom: 5px;
        }
        
        strong {
            color: #2c3e50;
            font-weight: bold;
        }
        
        p {
            margin-bottom: 10px;
            text-align: justify;
        }
        
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 15px 0;
        }
        
        th, td {
            border: 1px solid #ddd;
            padding: 8px;
            text-align: left;
        }
        
        th {
            background-color: #3498db;
            color: white;
        }
        
        tr:nth-child(even) {
            background-color: #f9f9f9;
        }
        
        .page-break {
            page-break-before: always;
        }
    """
    
    # Créer le HTML complet
    html_full = f"""
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <title>Offres Directeurs Audit Interne - Côte d'Ivoire</title>
    </head>
    <body>
        {html_content}
    </body>
    </html>
    """
    
    # Générer le PDF
    HTML(string=html_full).write_pdf(
        pdf_file,
        stylesheets=[CSS(string=css_style)]
    )
    
    print(f"✅ PDF créé avec succès : {pdf_file}")
    return pdf_file

if __name__ == "__main__":
    md_file = r"h:\Projet_pdf_excel\Offres_Directeurs_Audit_Interne_CI.md"
    pdf_file = r"h:\Projet_pdf_excel\Offres_Directeurs_Audit_Interne_CI.pdf"
    
    try:
        markdown_to_pdf(md_file, pdf_file)
    except Exception as e:
        print(f"❌ Erreur : {e}")
        import traceback
        traceback.print_exc()
