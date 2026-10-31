# Script PowerShell : test_workflow_cas2.ps1
# Description : Teste le workflow Cas 2 en mode simulation
# Date : 31 octobre 2026

Write-Host "`n======================================================================"
Write-Host "  TEST WORKFLOW CAS 2 - Mode Simulation"
Write-Host "======================================================================`n"

# Se placer dans le bon dossier
Set-Location "h:\Projet_pdf_excel\Modelisation claude skill"

# Étape 1 : Créer les données de simulation
Write-Host "[1/3] Creation des donnees de simulation...`n"
python simulate_n8n_response.py

if ($LASTEXITCODE -ne 0) {
    Write-Host "`n[ERREUR] Echec de la creation des donnees de simulation" -ForegroundColor Red
    exit 1
}

# Étape 2 : Vérifier que le fichier JSON existe
$jsonFile = "data_json_from_n8n\data_integrale_simulation.json"

if (Test-Path $jsonFile) {
    Write-Host "`n[SUCCESS] Fichier JSON de simulation cree : $jsonFile" -ForegroundColor Green
} else {
    Write-Host "`n[ERREUR] Fichier JSON introuvable" -ForegroundColor Red
    exit 1
}

# Étape 3 : Exécuter le skill sur les données de simulation
Write-Host "`n[2/3] Execution du skill sur les donnees de simulation...`n"

$outputDir = "sortie_word_test"
New-Item -ItemType Directory -Force -Path $outputDir | Out-Null

python json2word_audit.py $jsonFile -o $outputDir --ref "TEST" --software "Simulation Test N8N"

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n======================================================================"
    Write-Host "  SUCCESS - Test du workflow Cas 2 termine avec succes" -ForegroundColor Green
    Write-Host "======================================================================`n"
    
    Write-Host "Documents generes dans : $outputDir`n"
    
    # Lister les fichiers générés
    if (Test-Path $outputDir) {
        Write-Host "Fichiers generes :"
        Get-ChildItem -Path $outputDir -Filter "*.docx" | ForEach-Object {
            Write-Host "  - $($_.Name)" -ForegroundColor Cyan
        }
    }
    
    Write-Host "`n======================================================================"
    
    # Proposer d'ouvrir le dossier
    $openFolder = Read-Host "`nVoulez-vous ouvrir le dossier de sortie ? (O/N)"
    if ($openFolder -eq "O" -or $openFolder -eq "o") {
        Invoke-Item $outputDir
    }
    
} else {
    Write-Host "`n======================================================================"
    Write-Host "  ERREUR - Le test a echoue" -ForegroundColor Red
    Write-Host "======================================================================`n"
    exit 1
}

Write-Host "`nAppuyez sur une touche pour continuer..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
