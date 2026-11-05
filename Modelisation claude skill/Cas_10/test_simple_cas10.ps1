# Test Simple du Cas 10
# Version simplifiée sans caractères spéciaux

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  CAS 10 - TESTS SIMPLIFIES" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$TotalTests = 0
$PassedTests = 0

# Test 1: Python
Write-Host "Test 1: Python..." -NoNewline
try {
    $result = python --version 2>&1
    if ($result -match "Python") {
        Write-Host " OK" -ForegroundColor Green
        $PassedTests++
    } else {
        Write-Host " ECHEC" -ForegroundColor Red
    }
} catch {
    Write-Host " ECHEC" -ForegroundColor Red
}
$TotalTests++

# Test 2: Requests
Write-Host "Test 2: Module requests..." -NoNewline
try {
    python -c "import requests" 2>&1 | Out-Null
    if ($LASTEXITCODE -eq 0) {
        Write-Host " OK" -ForegroundColor Green
        $PassedTests++
    } else {
        Write-Host " ECHEC" -ForegroundColor Red
    }
} catch {
    Write-Host " ECHEC" -ForegroundColor Red
}
$TotalTests++

# Test 3: python-docx
Write-Host "Test 3: Module docx..." -NoNewline
try {
    python -c "import docx" 2>&1 | Out-Null
    if ($LASTEXITCODE -eq 0) {
        Write-Host " OK" -ForegroundColor Green
        $PassedTests++
    } else {
        Write-Host " ECHEC" -ForegroundColor Red
    }
} catch {
    Write-Host " ECHEC" -ForegroundColor Red
}
$TotalTests++

# Test 4: Orchestrateur
Write-Host "Test 4: Fichier orchestrateur..." -NoNewline
if (Test-Path "execute_cas10_orchestrator.py") {
    Write-Host " OK" -ForegroundColor Green
    $PassedTests++
} else {
    Write-Host " ECHEC" -ForegroundColor Red
}
$TotalTests++

# Test 5: Routeur
Write-Host "Test 5: Fichier routeur..." -NoNewline
if (Test-Path "cas10_router.py") {
    Write-Host " OK" -ForegroundColor Green
    $PassedTests++
} else {
    Write-Host " ECHEC" -ForegroundColor Red
}
$TotalTests++

# Test 6: Dossier sortie
Write-Host "Test 6: Dossier de sortie..." -NoNewline
if (Test-Path "sortie_word_cas10") {
    Write-Host " OK" -ForegroundColor Green
    $PassedTests++
} else {
    Write-Host " ECHEC" -ForegroundColor Red
}
$TotalTests++

# Test 7: Routeur fonctionne
Write-Host "Test 7: Routeur intelligent..." -NoNewline
try {
    $result = python cas10_router.py 2>&1
    if ($result -match "tests passés") {
        Write-Host " OK" -ForegroundColor Green
        $PassedTests++
    } else {
        Write-Host " ECHEC" -ForegroundColor Red
    }
} catch {
    Write-Host " ECHEC" -ForegroundColor Red
}
$TotalTests++

# Résumé
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  RESULTAT" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Total tests : $TotalTests"
Write-Host "Reussis     : $PassedTests" -ForegroundColor Green
Write-Host "Echoues     : $($TotalTests - $PassedTests)" -ForegroundColor $(if ($PassedTests -eq $TotalTests) { "Green" } else { "Red" })

$percent = [math]::Round(($PassedTests / $TotalTests) * 100, 1)
Write-Host "Taux        : $percent%" -ForegroundColor $(if ($percent -ge 80) { "Green" } else { "Yellow" })
Write-Host ""

if ($PassedTests -eq $TotalTests) {
    Write-Host "TOUS LES TESTS SONT PASSES!" -ForegroundColor Green
    Write-Host "Le Cas 10 est pret a etre utilise." -ForegroundColor Green
    exit 0
} else {
    Write-Host "CERTAINS TESTS ONT ECHOUE" -ForegroundColor Yellow
    Write-Host "Verifiez les erreurs ci-dessus." -ForegroundColor Yellow
    exit 1
}
