# Script PowerShell pour configurer l'environnement Miniconda
# Auteur: Expert Python Senior
# Date: 2026-10-30

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Configuration de l'environnement Python" -ForegroundColor Cyan
Write-Host "Projet: PDF-Excel-Word Manipulation" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Vérifier si conda est installé
Write-Host "Vérification de Miniconda..." -ForegroundColor Yellow
$condaCommand = Get-Command conda -ErrorAction SilentlyContinue

if (-not $condaCommand) {
    Write-Host "❌ Miniconda n'est pas installé!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Veuillez installer Miniconda depuis:" -ForegroundColor Yellow
    Write-Host "https://docs.conda.io/en/latest/miniconda.html" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Ou utilisez cette commande pour télécharger l'installateur Windows:" -ForegroundColor Yellow
    Write-Host "Invoke-WebRequest -Uri 'https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe' -OutFile 'MinicondaInstaller.exe'" -ForegroundColor Green
    exit 1
}

Write-Host "✓ Miniconda détecté" -ForegroundColor Green
Write-Host ""

# Initialiser conda pour PowerShell si nécessaire
Write-Host "Initialisation de conda pour PowerShell..." -ForegroundColor Yellow
conda init powershell 2>&1 | Out-Null

# Créer l'environnement à partir du fichier environment.yml
Write-Host "Création de l'environnement 'pdf_excel_env'..." -ForegroundColor Yellow
Write-Host "Cela peut prendre plusieurs minutes..." -ForegroundColor Gray
Write-Host ""

# Vérifier si l'environnement existe déjà
$envExists = conda env list | Select-String "pdf_excel_env"

if ($envExists) {
    Write-Host "⚠️  L'environnement 'pdf_excel_env' existe déjà" -ForegroundColor Yellow
    $response = Read-Host "Voulez-vous le supprimer et le recréer? (o/n)"
    
    if ($response -eq 'o' -or $response -eq 'O') {
        Write-Host "Suppression de l'environnement existant..." -ForegroundColor Yellow
        conda env remove -n pdf_excel_env -y
        Write-Host "✓ Environnement supprimé" -ForegroundColor Green
    } else {
        Write-Host "Installation annulée" -ForegroundColor Red
        exit 0
    }
}

# Créer l'environnement
conda env create -f environment.yml

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "✓ Environnement créé avec succès!" -ForegroundColor Green
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host "Pour activer l'environnement, utilisez:" -ForegroundColor Yellow
    Write-Host "conda activate pdf_excel_env" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Librairies installées:" -ForegroundColor Yellow
    Write-Host "  📄 PDF: pypdf, PyMuPDF, pikepdf, pdfplumber, reportlab, fpdf2" -ForegroundColor White
    Write-Host "  📊 Excel: openpyxl, xlsxwriter, xlwings, formulas, pandas" -ForegroundColor White
    Write-Host "  📝 Word: python-docx, docxtpl, mammoth, docx2pdf" -ForegroundColor White
    Write-Host "  📈 Analyse: pandas, numpy, matplotlib, seaborn, plotly" -ForegroundColor White
    Write-Host ""
} else {
    Write-Host ""
    Write-Host "❌ Erreur lors de la création de l'environnement" -ForegroundColor Red
    Write-Host "Veuillez vérifier les messages d'erreur ci-dessus" -ForegroundColor Yellow
    exit 1
}
