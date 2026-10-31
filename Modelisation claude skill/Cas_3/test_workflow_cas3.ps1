# ===========================================================================
# Script : test_workflow_cas3.ps1
# Description : Test du workflow Cas 3 (Manuel Audit via N8N)
# Auteur : Expert Python & Automation
# Date : 31 octobre 2026
# ===========================================================================

Write-Host ""
Write-Host "=======================================================================" -ForegroundColor Cyan
Write-Host "  Test Workflow Cas 3 - Manuel Audit (API N8N)" -ForegroundColor Cyan
Write-Host "=======================================================================" -ForegroundColor Cyan
Write-Host ""

# Vérifier que N8N est accessible
$webhookUrl = "http://localhost:5678/webhook/skill_manuel_audit_cas3"
Write-Host "1. Test de connexion N8N..." -ForegroundColor Yellow
Write-Host "   URL : $webhookUrl" -ForegroundColor Gray

try {
    $response = Invoke-WebRequest -Uri $webhookUrl -Method POST -ContentType "application/json" -Body '{}' -UseBasicParsing -TimeoutSec 10
    Write-Host "   ✅ N8N accessible (Status: $($response.StatusCode))" -ForegroundColor Green
    
    # Afficher un aperçu de la réponse
    $json = $response.Content | ConvertFrom-Json
    Write-Host "   Réponse reçue : $($response.Content.Length) octets" -ForegroundColor Gray
    
    # Vérifier Data_integrale
    if ($json.PSObject.Properties.Name -contains "Data_integrale") {
        Write-Host "   ✅ Champ Data_integrale trouvé" -ForegroundColor Green
        if ($json.Data_integrale -is [Array]) {
            Write-Host "   ✅ Data_integrale est un Array ($($json.Data_integrale.Count) élément(s))" -ForegroundColor Green
        } else {
            Write-Host "   ⚠️  Data_integrale n'est pas un Array" -ForegroundColor Yellow
        }
    } else {
        Write-Host "   ⚠️  Champ Data_integrale absent" -ForegroundColor Yellow
        Write-Host "   Structure reçue : $($json.PSObject.Properties.Name -join ', ')" -ForegroundColor Gray
    }
    
} catch {
    Write-Host "   ❌ Erreur de connexion N8N" -ForegroundColor Red
    Write-Host "   Message : $($_.Exception.Message)" -ForegroundColor Red
    Write-Host ""
    Write-Host "Solutions possibles :" -ForegroundColor Yellow
    Write-Host "  1. Démarrer N8N : n8n start" -ForegroundColor Gray
    Write-Host "  2. Vérifier le port : netstat -an | findstr 5678" -ForegroundColor Gray
    Write-Host "  3. Activer le workflow 'skill_manuel_audit_cas3' dans N8N" -ForegroundColor Gray
    Write-Host ""
    exit 1
}

Write-Host ""
Write-Host "2. Test des dépendances Python..." -ForegroundColor Yellow

# Vérifier Python
try {
    $pythonVersion = python --version 2>&1
    Write-Host "   ✅ Python : $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "   ❌ Python non trouvé" -ForegroundColor Red
    exit 1
}

# Vérifier python-docx
try {
    $docxCheck = python -c "import docx; print(docx.__version__)" 2>&1
    Write-Host "   ✅ python-docx : $docxCheck" -ForegroundColor Green
} catch {
    Write-Host "   ❌ python-docx non installé" -ForegroundColor Red
    Write-Host "   Installer avec : pip install python-docx" -ForegroundColor Gray
}

# Vérifier requests
try {
    $requestsCheck = python -c "import requests; print(requests.__version__)" 2>&1
    Write-Host "   ✅ requests : $requestsCheck" -ForegroundColor Green
} catch {
    Write-Host "   ❌ requests non installé" -ForegroundColor Red
    Write-Host "   Installer avec : pip install requests" -ForegroundColor Gray
}

Write-Host ""
Write-Host "3. Vérification des fichiers..." -ForegroundColor Yellow

$files = @(
    "execute_cas3_production.py",
    "json2word_audit.py",
    "execute_cas3.bat",
    "audit-manuel-json2word.skill.md",
    "GUIDE_CONFIGURATION_N8N.md"
)

foreach ($file in $files) {
    if (Test-Path $file) {
        Write-Host "   ✅ $file" -ForegroundColor Green
    } else {
        Write-Host "   ❌ $file (manquant)" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "4. Test d'exécution du workflow..." -ForegroundColor Yellow
Write-Host "   Lancement de execute_cas3_production.py..." -ForegroundColor Gray
Write-Host ""

# Exécuter le script
try {
    python execute_cas3_production.py
    $exitCode = $LASTEXITCODE
    
    Write-Host ""
    if ($exitCode -eq 0) {
        Write-Host "   ✅ Workflow exécuté avec succès" -ForegroundColor Green
    } else {
        Write-Host "   ⚠️  Workflow terminé avec le code : $exitCode" -ForegroundColor Yellow
    }
} catch {
    Write-Host "   ❌ Erreur lors de l'exécution" -ForegroundColor Red
    Write-Host "   Message : $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""
Write-Host "5. Vérification des sorties..." -ForegroundColor Yellow

# Vérifier le dossier de sortie
if (Test-Path "sortie_word_cas3") {
    $wordFiles = Get-ChildItem -Path "sortie_word_cas3" -Filter "*.docx" -File
    Write-Host "   📁 Dossier sortie_word_cas3 : $($wordFiles.Count) fichier(s)" -ForegroundColor Green
    
    if ($wordFiles.Count -gt 0) {
        Write-Host ""
        Write-Host "   Documents générés :" -ForegroundColor Gray
        foreach ($file in $wordFiles | Select-Object -First 5) {
            Write-Host "      • $($file.Name)" -ForegroundColor Gray
        }
        if ($wordFiles.Count -gt 5) {
            Write-Host "      ... et $($wordFiles.Count - 5) autre(s)" -ForegroundColor Gray
        }
    }
} else {
    Write-Host "   ⚠️  Dossier sortie_word_cas3 absent" -ForegroundColor Yellow
}

# Vérifier les données sauvegardées
if (Test-Path "data_json_from_n8n_cas3") {
    $jsonFiles = Get-ChildItem -Path "data_json_from_n8n_cas3" -Filter "*.json" -File
    Write-Host "   📁 Données API sauvegardées : $($jsonFiles.Count) fichier(s)" -ForegroundColor Green
} else {
    Write-Host "   ⚠️  Dossier data_json_from_n8n_cas3 absent" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "=======================================================================" -ForegroundColor Cyan
Write-Host "  Fin des tests" -ForegroundColor Cyan
Write-Host "=======================================================================" -ForegroundColor Cyan
Write-Host ""

# Proposer d'ouvrir le dossier de sortie
$openFolder = Read-Host "Ouvrir le dossier de sortie ? (O/N)"
if ($openFolder -eq "O" -or $openFolder -eq "o") {
    if (Test-Path "sortie_word_cas3") {
        Start-Process "sortie_word_cas3"
    } else {
        Write-Host "Le dossier n'existe pas encore." -ForegroundColor Yellow
    }
}
