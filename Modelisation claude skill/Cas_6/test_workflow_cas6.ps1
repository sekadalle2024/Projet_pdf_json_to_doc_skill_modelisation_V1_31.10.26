# ============================================================================
# Script PowerShell : test_workflow_cas6.ps1
# Description : Tests automatisés du workflow Cas 6 - Feuilles de Révision
# ============================================================================

Write-Host "`n========================================================================" -ForegroundColor Cyan
Write-Host "  TESTS AUTOMATISÉS - CAS 6 : FEUILLES DE RÉVISION D'AUDIT" -ForegroundColor Cyan
Write-Host "========================================================================`n" -ForegroundColor Cyan

$ErrorActionPreference = "Continue"
$TestsPassed = 0
$TestsFailed = 0

# ============================================================================
# TEST 1 : Vérification de Python
# ============================================================================

Write-Host "TEST 1 : Vérification de Python..." -ForegroundColor Yellow

try {
    $pythonVersion = python --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  ✅ Python installé : $pythonVersion" -ForegroundColor Green
        $TestsPassed++
    } else {
        Write-Host "  ❌ Python non trouvé" -ForegroundColor Red
        $TestsFailed++
    }
} catch {
    Write-Host "  ❌ Python non installé" -ForegroundColor Red
    $TestsFailed++
}

# ============================================================================
# TEST 2 : Vérification des dépendances Python
# ============================================================================

Write-Host "`nTEST 2 : Vérification des dépendances Python..." -ForegroundColor Yellow

$dependencies = @("python-docx", "requests")
$allDepsInstalled = $true

foreach ($dep in $dependencies) {
    $result = python -c "import sys; import $($dep.Replace('-', '_')); print('OK')" 2>&1
    if ($result -like "*OK*") {
        Write-Host "  ✅ $dep installé" -ForegroundColor Green
    } else {
        Write-Host "  ❌ $dep manquant" -ForegroundColor Red
        $allDepsInstalled = $false
    }
}

if ($allDepsInstalled) {
    $TestsPassed++
} else {
    $TestsFailed++
    Write-Host "  💡 Pour installer : pip install python-docx requests" -ForegroundColor Yellow
}

# ============================================================================
# TEST 3 : Vérification des fichiers du skill
# ============================================================================

Write-Host "`nTEST 3 : Vérification des fichiers du skill..." -ForegroundColor Yellow

$requiredFiles = @(
    "json2word_feuilles_revision.py",
    "execute_cas6_production.py",
    "audit-feuilles-revision-json2word.skill.md"
)

$allFilesExist = $true

foreach ($file in $requiredFiles) {
    if (Test-Path $file) {
        Write-Host "  ✅ $file présent" -ForegroundColor Green
    } else {
        Write-Host "  ❌ $file manquant" -ForegroundColor Red
        $allFilesExist = $false
    }
}

if ($allFilesExist) {
    $TestsPassed++
} else {
    $TestsFailed++
}

# ============================================================================
# TEST 4 : Vérification de N8N
# ============================================================================

Write-Host "`nTEST 4 : Vérification de N8N..." -ForegroundColor Yellow

try {
    $response = Invoke-WebRequest -Uri "http://localhost:5678" -Method GET -TimeoutSec 5 -ErrorAction Stop
    Write-Host "  ✅ N8N est accessible (Status: $($response.StatusCode))" -ForegroundColor Green
    $TestsPassed++
} catch {
    Write-Host "  ❌ N8N non accessible sur localhost:5678" -ForegroundColor Red
    Write-Host "  💡 Démarrez N8N avec : n8n start" -ForegroundColor Yellow
    $TestsFailed++
}

# ============================================================================
# TEST 5 : Test du webhook N8N Cas 6
# ============================================================================

Write-Host "`nTEST 5 : Test du webhook N8N Cas 6..." -ForegroundColor Yellow

$webhookUrl = "http://localhost:5678/webhook/skill_feuilles_revision_cas6"

try {
    $body = @{} | ConvertTo-Json
    $response = Invoke-WebRequest -Uri $webhookUrl -Method POST -Body $body -ContentType "application/json" -TimeoutSec 10 -ErrorAction Stop
    
    Write-Host "  ✅ Webhook répond (Status: $($response.StatusCode))" -ForegroundColor Green
    
    # Vérifier la présence de Data_integrale
    $jsonResponse = $response.Content | ConvertFrom-Json
    
    if ($jsonResponse.Data_integrale) {
        Write-Host "  ✅ Data_integrale présent dans la réponse" -ForegroundColor Green
        $feuillesCount = $jsonResponse.Data_integrale.Count
        Write-Host "  📊 Nombre de feuilles : $feuillesCount" -ForegroundColor Cyan
        $TestsPassed++
    } else {
        Write-Host "  ⚠️  Data_integrale absent (vérifiez la configuration N8N)" -ForegroundColor Yellow
        $TestsFailed++
    }
    
} catch {
    Write-Host "  ❌ Webhook non accessible : $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "  💡 Vérifiez que le workflow 'skill_feuilles_revision_cas6' est actif dans N8N" -ForegroundColor Yellow
    $TestsFailed++
}

# ============================================================================
# TEST 6 : Création des dossiers de sortie
# ============================================================================

Write-Host "`nTEST 6 : Création des dossiers de sortie..." -ForegroundColor Yellow

$directories = @(
    "sortie_word_cas6",
    "temp_feuilles_cas6",
    "data_json_from_n8n_cas6"
)

$allDirsCreated = $true

foreach ($dir in $directories) {
    if (-not (Test-Path $dir)) {
        try {
            New-Item -ItemType Directory -Path $dir -Force | Out-Null
            Write-Host "  ✅ $dir créé" -ForegroundColor Green
        } catch {
            Write-Host "  ❌ Impossible de créer $dir" -ForegroundColor Red
            $allDirsCreated = $false
        }
    } else {
        Write-Host "  ✅ $dir existe déjà" -ForegroundColor Green
    }
}

if ($allDirsCreated) {
    $TestsPassed++
} else {
    $TestsFailed++
}

# ============================================================================
# TEST 7 : Test du script de conversion (avec JSON minimal)
# ============================================================================

Write-Host "`nTEST 7 : Test du script de conversion..." -ForegroundColor Yellow

$testJson = @"
{
  "Feuille de révision - Test minimal": [
    {
      "table 1": {
        "Etape de mission": "Test Feuille de révision",
        "Document": "Document de test",
        "Reference": "TEST-001"
      }
    },
    {
      "table 2": [
        {
          "N° Test": "T-001",
          "Objectif de contrôle": "Test de contrôle",
          "Nature du contrôle": "Préventif",
          "Procédure de test": "Procédure de test",
          "Taille échantillon": "10/100",
          "Résultat observé": "Conforme",
          "Écart identifié": "Aucun",
          "Conclusion": "OK",
          "Action recommandée": "Aucune"
        }
      ]
    }
  ]
}
"@

$testJsonFile = "temp_feuilles_cas6\test_minimal.json"

try {
    # Créer le fichier de test
    $testJson | Out-File -FilePath $testJsonFile -Encoding UTF8
    
    # Exécuter le script de conversion
    $result = python json2word_feuilles_revision.py $testJsonFile -o sortie_word_cas6 2>&1
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  ✅ Script de conversion fonctionne" -ForegroundColor Green
        $TestsPassed++
        
        # Vérifier qu'un fichier Word a été généré
        $wordFiles = Get-ChildItem -Path "sortie_word_cas6" -Filter "*.docx" | Where-Object { $_.LastWriteTime -gt (Get-Date).AddMinutes(-1) }
        if ($wordFiles) {
            Write-Host "  ✅ Document Word généré : $($wordFiles[0].Name)" -ForegroundColor Green
        }
    } else {
        Write-Host "  ❌ Erreur lors de la conversion" -ForegroundColor Red
        Write-Host "  $result" -ForegroundColor Gray
        $TestsFailed++
    }
    
    # Nettoyer le fichier de test
    if (Test-Path $testJsonFile) {
        Remove-Item $testJsonFile -Force
    }
    
} catch {
    Write-Host "  ❌ Test échoué : $($_.Exception.Message)" -ForegroundColor Red
    $TestsFailed++
}

# ============================================================================
# RÉSUMÉ DES TESTS
# ============================================================================

Write-Host "`n========================================================================" -ForegroundColor Cyan
Write-Host "  RÉSUMÉ DES TESTS" -ForegroundColor Cyan
Write-Host "========================================================================" -ForegroundColor Cyan

$TotalTests = $TestsPassed + $TestsFailed
$SuccessRate = [math]::Round(($TestsPassed / $TotalTests) * 100, 1)

Write-Host "`n  Tests réussis  : $TestsPassed / $TotalTests" -ForegroundColor Green
Write-Host "  Tests échoués  : $TestsFailed / $TotalTests" -ForegroundColor $(if ($TestsFailed -eq 0) { "Green" } else { "Red" })
Write-Host "  Taux de succès : $SuccessRate%" -ForegroundColor $(if ($SuccessRate -eq 100) { "Green" } elseif ($SuccessRate -ge 70) { "Yellow" } else { "Red" })

Write-Host "`n========================================================================`n" -ForegroundColor Cyan

if ($TestsFailed -eq 0) {
    Write-Host "✅ Tous les tests sont passés ! Le Cas 6 est prêt." -ForegroundColor Green
    exit 0
} elseif ($SuccessRate -ge 70) {
    Write-Host "⚠️  La plupart des tests sont passés. Vérifiez les points échoués." -ForegroundColor Yellow
    exit 1
} else {
    Write-Host "❌ Plusieurs tests ont échoué. Configuration requise." -ForegroundColor Red
    exit 1
}
