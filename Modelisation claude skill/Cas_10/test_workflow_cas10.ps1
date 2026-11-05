# ═══════════════════════════════════════════════════════════════════════════
#     CAS 10 - TESTS AUTOMATISÉS POWERSHELL
#     Suite de tests pour valider l'orchestrateur Cas 10
# ═══════════════════════════════════════════════════════════════════════════
#
# Description:
#     Vérifie tous les aspects du Cas 10:
#     - Environnement Python
#     - Dépendances
#     - Structure des fichiers
#     - Connexion N8N
#     - Routeur intelligent
#     - Scripts des cas 5, 6, 7, 8
#
# Auteur: Expert Python & Automation
# Date: 5 novembre 2026
# Version: 1.0.0
# ═══════════════════════════════════════════════════════════════════════════

# Couleurs pour l'affichage
$ColorSuccess = "Green"
$ColorError = "Red"
$ColorInfo = "Cyan"
$ColorWarning = "Yellow"

# Compteurs
$TotalTests = 0
$PassedTests = 0
$FailedTests = 0

# Fonction d'affichage
function Write-TestHeader {
    param([string]$Title)
    Write-Host "`n═══════════════════════════════════════════════════════════════════════════" -ForegroundColor $ColorInfo
    Write-Host "  $Title" -ForegroundColor $ColorInfo
    Write-Host "═══════════════════════════════════════════════════════════════════════════`n" -ForegroundColor $ColorInfo
}

function Write-TestResult {
    param(
        [string]$TestName,
        [bool]$Success,
        [string]$Message = ""
    )
    
    $global:TotalTests++
    
    if ($Success) {
        $global:PassedTests++
        Write-Host "✅ TEST $global:TotalTests : $TestName" -ForegroundColor $ColorSuccess
        if ($Message) {
            Write-Host "   $Message" -ForegroundColor Gray
        }
    } else {
        $global:FailedTests++
        Write-Host "❌ TEST $global:TotalTests : $TestName" -ForegroundColor $ColorError
        if ($Message) {
            Write-Host "   $Message" -ForegroundColor $ColorError
        }
    }
}

# ═══════════════════════════════════════════════════════════════════════════
# DÉBUT DES TESTS
# ═══════════════════════════════════════════════════════════════════════════

Write-TestHeader "CAS 10 - TESTS AUTOMATISÉS"

# ═══════════════════════════════════════════════════════════════════════════
# TEST 1: Environnement Python
# ═══════════════════════════════════════════════════════════════════════════

Write-Host "`n🔍 CATÉGORIE 1: ENVIRONNEMENT PYTHON" -ForegroundColor $ColorInfo

try {
    $pythonVersion = python --version 2>&1
    Write-TestResult "Python installé" $true $pythonVersion
} catch {
    Write-TestResult "Python installé" $false "Python non trouvé"
}

# ═══════════════════════════════════════════════════════════════════════════
# TEST 2: Dépendances Python
# ═══════════════════════════════════════════════════════════════════════════

Write-Host "`n🔍 CATÉGORIE 2: DÉPENDANCES" -ForegroundColor $ColorInfo

$dependencies = @("requests", "docx")
foreach ($dep in $dependencies) {
    try {
        $result = python -c "import $dep; print('OK')" 2>&1
        $success = $result -match "OK"
        Write-TestResult "Module $dep" $success
    } catch {
        Write-TestResult "Module $dep" $false "Module non installé"
    }
}

# ═══════════════════════════════════════════════════════════════════════════
# TEST 3: Fichiers du Cas 10
# ═══════════════════════════════════════════════════════════════════════════

Write-Host "`n🔍 CATÉGORIE 3: FICHIERS CAS 10" -ForegroundColor $ColorInfo

$requiredFiles = @(
    "execute_cas10_orchestrator.py",
    "cas10_router.py",
    "execute_cas10.bat",
    "test_workflow_cas10.ps1"
)

foreach ($file in $requiredFiles) {
    $exists = Test-Path $file
    Write-TestResult "Fichier $file" $exists
}

# ═══════════════════════════════════════════════════════════════════════════
# TEST 4: Dossiers de sortie
# ═══════════════════════════════════════════════════════════════════════════

Write-Host "`n🔍 CATÉGORIE 4: STRUCTURE DES DOSSIERS" -ForegroundColor $ColorInfo

$sortieDir = "sortie_word_cas10"
if (-not (Test-Path $sortieDir)) {
    New-Item -ItemType Directory -Path $sortieDir -Force | Out-Null
}
Write-TestResult "Dossier de sortie $sortieDir" (Test-Path $sortieDir)

# ═══════════════════════════════════════════════════════════════════════════
# TEST 5: Scripts des autres cas
# ═══════════════════════════════════════════════════════════════════════════

Write-Host "`n🔍 CATÉGORIE 5: SCRIPTS DES CAS 5, 6, 7, 8" -ForegroundColor $ColorInfo

$casScripts = @{
    "5" = "..\Cas_5\json2word_frap_recos.py"
    "6" = "..\Cas_6\json2word_feuilles_revision.py"
    "7" = "..\Cas_7\json2word_feuille_couverture.py"
    "8" = "..\Cas_8\json2word_modele_standard.py"
}

foreach ($cas in $casScripts.Keys) {
    $scriptPath = $casScripts[$cas]
    $exists = Test-Path $scriptPath
    $status = if ($exists) { "OK" } else { "À créer" }
    Write-TestResult "Script Cas $cas" $exists $status
}

# ═══════════════════════════════════════════════════════════════════════════
# TEST 6: Connexion N8N
# ═══════════════════════════════════════════════════════════════════════════

Write-Host "`n🔍 CATÉGORIE 6: CONNEXION N8N" -ForegroundColor $ColorInfo

try {
    $n8nUrl = "http://localhost:5678"
    $response = Invoke-WebRequest -Uri $n8nUrl -Method GET -TimeoutSec 5 -ErrorAction Stop
    Write-TestResult "N8N accessible sur $n8nUrl" $true "Status: $($response.StatusCode)"
} catch {
    Write-TestResult "N8N accessible" $false "N8N non démarré ou inaccessible"
    Write-Host "   💡 Démarrez N8N avec: n8n start" -ForegroundColor $ColorWarning
}

# ═══════════════════════════════════════════════════════════════════════════
# TEST 7: Test du routeur
# ═══════════════════════════════════════════════════════════════════════════

Write-Host "`n🔍 CATÉGORIE 7: TEST DU ROUTEUR" -ForegroundColor $ColorInfo

try {
    $routerTest = python cas10_router.py 2>&1
    $success = $routerTest -match "Tous les tests passés"
    Write-TestResult "Routeur intelligent" $success
    if (-not $success) {
        Write-Host $routerTest -ForegroundColor $ColorError
    }
} catch {
    Write-TestResult "Routeur intelligent" $false "Erreur lors du test"
}

# ═══════════════════════════════════════════════════════════════════════════
# TEST 8: Syntaxe Python des scripts
# ═══════════════════════════════════════════════════════════════════════════

Write-Host "`n🔍 CATÉGORIE 8: SYNTAXE PYTHON" -ForegroundColor $ColorInfo

$pythonScripts = @(
    "execute_cas10_orchestrator.py",
    "cas10_router.py"
)

foreach ($script in $pythonScripts) {
    try {
        $result = python -m py_compile $script 2>&1
        $success = -not ($result -match "SyntaxError")
        Write-TestResult "Syntaxe de $script" $success
    } catch {
        Write-TestResult "Syntaxe de $script" $false
    }
}

# ═══════════════════════════════════════════════════════════════════════════
# TEST 9: Webhook N8N Cas 10
# ═══════════════════════════════════════════════════════════════════════════

Write-Host "`n🔍 CATÉGORIE 9: WEBHOOK CAS 10" -ForegroundColor $ColorInfo

try {
    $webhookUrl = "http://localhost:5678/webhook/skill_cas10_multi"
    $testData = @{} | ConvertTo-Json
    
    $response = Invoke-RestMethod -Uri $webhookUrl -Method POST -Body $testData -ContentType "application/json" -TimeoutSec 10 -ErrorAction Stop
    Write-TestResult "Webhook Cas 10 accessible" $true "URL: $webhookUrl"
} catch {
    Write-TestResult "Webhook Cas 10 accessible" $false "Webhook non configuré"
    Write-Host "   💡 Configurez le webhook dans N8N: $webhookUrl" -ForegroundColor $ColorWarning
}

# ═══════════════════════════════════════════════════════════════════════════
# RÉSUMÉ FINAL
# ═══════════════════════════════════════════════════════════════════════════

Write-TestHeader "RÉSUMÉ DES TESTS"

$percentSuccess = [math]::Round(($PassedTests / $TotalTests) * 100, 1)

Write-Host "Total de tests    : $TotalTests" -ForegroundColor $ColorInfo
Write-Host "Tests réussis     : $PassedTests" -ForegroundColor $ColorSuccess
Write-Host "Tests échoués     : $FailedTests" -ForegroundColor $ColorError
Write-Host "Taux de réussite  : $percentSuccess%" -ForegroundColor $(if ($percentSuccess -ge 80) { $ColorSuccess } else { $ColorWarning })

Write-Host "`n"

if ($FailedTests -eq 0) {
    Write-Host "✅ TOUS LES TESTS SONT PASSÉS!" -ForegroundColor $ColorSuccess
    Write-Host "   Le Cas 10 est prêt à être utilisé." -ForegroundColor $ColorSuccess
    Write-Host ""
    exit 0
} else {
    Write-Host "⚠️  CERTAINS TESTS ONT ÉCHOUÉ" -ForegroundColor $ColorWarning
    Write-Host "   Corrigez les erreurs avant d'utiliser le Cas 10." -ForegroundColor $ColorWarning
    Write-Host ""
    exit 1
}
