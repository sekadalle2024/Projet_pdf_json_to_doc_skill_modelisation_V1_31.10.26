# Script d'installation simplifié - Installation par étapes
# Auteur: Expert Python Senior
# Date: 2026-10-30

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "Installation Simplifiée - Environnement Python" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# Étape 1: Créer l'environnement de base
Write-Host "Étape 1/4: Création de l'environnement de base..." -ForegroundColor Yellow
conda create -n pdf_excel_env python=3.11 -y

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Erreur lors de la création de l'environnement" -ForegroundColor Red
    exit 1
}

Write-Host "✓ Environnement de base créé" -ForegroundColor Green
Write-Host ""

# Étape 2: Installer les packages conda essentiels
Write-Host "Étape 2/4: Installation des packages conda essentiels..." -ForegroundColor Yellow
conda install -n pdf_excel_env -c conda-forge numpy pandas openpyxl xlrd -y

if ($LASTEXITCODE -ne 0) {
    Write-Host "⚠️  Attention: Erreur lors de l'installation conda, mais on continue..." -ForegroundColor Yellow
}

Write-Host "✓ Packages conda installés" -ForegroundColor Green
Write-Host ""

# Étape 3: Installer les packages PDF
Write-Host "Étape 3/4: Installation des packages PDF..." -ForegroundColor Yellow
conda run -n pdf_excel_env pip install --no-cache-dir pypdf PyMuPDF pikepdf pdfplumber reportlab fpdf2

Write-Host "✓ Packages PDF installés" -ForegroundColor Green
Write-Host ""

# Étape 4: Installer les packages Excel et Word
Write-Host "Étape 4/4: Installation des packages Excel et Word..." -ForegroundColor Yellow
conda run -n pdf_excel_env pip install --no-cache-dir xlsxwriter xlwt python-docx docx2txt docxtpl mammoth

Write-Host "✓ Packages Excel et Word installés" -ForegroundColor Green
Write-Host ""

# Étape 5: Installer les packages d'analyse
Write-Host "Étape 5/5: Installation des packages d'analyse..." -ForegroundColor Yellow
conda run -n pdf_excel_env pip install --no-cache-dir matplotlib seaborn plotly scipy scikit-learn

Write-Host "✓ Packages d'analyse installés" -ForegroundColor Green
Write-Host ""

# Résumé
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "✨ Installation terminée avec succès!" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Pour activer l'environnement:" -ForegroundColor Yellow
Write-Host "conda activate pdf_excel_env" -ForegroundColor Green
Write-Host ""
Write-Host "Pour tester l'installation:" -ForegroundColor Yellow
Write-Host "conda activate pdf_excel_env" -ForegroundColor White
Write-Host "python test_installation.py" -ForegroundColor White
Write-Host ""
