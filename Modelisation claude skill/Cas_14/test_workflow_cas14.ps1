# ============================================================
# Script de Test Complet - Cas 14 : FRAP et Recommandations
# ============================================================
#
# Description:
#   Suite de 7 tests automatisés pour valider l'ensemble
#   du workflow Cas 14 (FRAP et Recommandations d'Audit)
#
# Tests:
#   TEST 1 - Vérification de Python
#   TEST 2 - Vérification des dépendances Python
#   TEST 3 - Vérification des fichiers du skill
#   TEST 4 - Vérification de N8N
#   TEST 5 - Test du webhook N8N Cas 14
#   TEST 6 - Création des dossiers de sortie
#   TEST 7 - Test du script de conversion
#
# Usage:
#   .\test_workflow_cas14.ps1
#
# Prérequis:
#   - PowerShell >= 5.1
#   - Python >= 3.9
#   - N8N en cours d'exécution (http://localhost:5678)
#
# Auteur: Kiro AI
# Date: 31 octobre 2026
# Version: 1.0.0
# ============================================================

# Configuration
$ErrorActionPreference = "Continue"
$ProgressPreference = "SilentlyContinue"

# Compteurs
$TestsPassed = 0
$TestsFailed = 0
$TotalTests = 7

# Couleurs
$ColorSuccess = "Green"
$ColorError = "Red"
$ColorInfo = "Cyan"
$ColorWarning = "Yellow"

# Bannière
Write-Host ""
Write-Host "============================================================" -ForegroundColor $ColorInfo
Write-Host "    SUITE DE TESTS - CAS 14 : FRAP ET RECOMMANDATIONS" -ForegroundColor $ColorInfo
Write-Host "============================================================" -ForegroundColor $ColorInfo
Write-Host ""
Write-Host "[INFO] Date/Heure: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" -ForegroundColor $ColorInfo
Write-Host "[INFO] Total de tests: $TotalTests" -ForegroundColor $ColorInfo
Write-Host ""

# ============================================================
# TEST 1 : Vérification de Python
# ============================================================
Write-Host "------------------------------------------------------------" -ForegroundColor $ColorInfo
Write-Host "TEST 1/7 - Vérification de Python" -ForegroundColor $ColorInfo
Write-Host "------------------------------------------------------------" -ForegroundColor $ColorInfo

try {
    $pythonVersion = python --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "[OK] Python est installé: $pythonVersion" -ForegroundColor $ColorSuccess
        $TestsPassed++
    } else {
        throw "Python n'est pas installé ou n'est pas dans le PATH"
    }
} catch {
    Write-Host "[ERREUR] $($_.Exception.Message)" -ForegroundColor $ColorError
    Write-Host "[SOLUTION] Installer Python >= 3.9 et l'ajouter au PATH" -ForegroundColor $ColorWarning
    $TestsFailed++
}
Write-Host ""

# ============================================================
# TEST 2 : Vérification des dépendances Python
# ============================================================
Write-Host "------------------------------------------------------------" -ForegroundColor $ColorInfo
Write-Host "TEST 2/7 - Vérification des dépendances Python" -ForegroundColor $ColorInfo
Write-Host "------------------------------------------------------------" -ForegroundColor $ColorInfo

$dependencies = @("docx", "requests")
$depOK = $true

foreach ($dep in $dependencies) {
    try {
        $result = python -c "import $dep; print(f'$dep OK')" 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Host "[OK] Dépendance '$dep' installée" -ForegroundColor $ColorSuccess
        } else {
            Write-Host "[ERREUR] Dépendance '$dep' manquante" -ForegroundColor $ColorError
            $depOK = $false
        }
    } catch {
        Write-Host "[ERREUR] Impossible de vérifier '$dep'" -ForegroundColor $ColorError
        $depOK = $false
    }
}

if ($depOK) {
    $TestsPassed++
} else {
    Write-Host "[SOLUTION] Installer les dépendances: pip install python-docx requests" -ForegroundColor $ColorWarning
    $TestsFailed++
}
Write-Host ""

# ============================================================
# TEST 3 : Vérification des fichiers du skill
# ============================================================
Write-Host "------------------------------------------------------------" -ForegroundColor $ColorInfo
Write-Host "TEST 3/7 - Vérification des fichiers du skill" -ForegroundColor $ColorInfo
Write-Host "------------------------------------------------------------" -ForegroundColor $ColorInfo

$requiredFiles = @(
    "json2word_frap.py",
    "execute_cas14_production.py",
    "audit-frap-recos-json2word.skill.md",
    "README.md",
    "CHANGELOG.md",
    "exemple_frap_minimal.json",
    "exemple_frap_complet.json"
)

$filesOK = $true
foreach ($file in $requiredFiles) {
    if (Test-Path $file) {
        Write-Host "[OK] Fichier trouvé: $file" -ForegroundColor $ColorSuccess
    } else {
        Write-Host "[ERREUR] Fichier manquant: $file" -ForegroundColor $ColorError
        $filesOK = $false
    }
}

if ($filesOK) {
    $TestsPassed++
} else {
    Write-Host "[SOLUTION] Vérifier que tous les fichiers du Cas 14 sont présents" -ForegroundColor $ColorWarning
    $TestsFailed++
}
Write-Host ""

# ============================================================
# TEST 4 : Vérification de N8N
# ============================================================
Write-Host "------------------------------------------------------------" -ForegroundColor $ColorInfo
Write-Host "TEST 4/7 - Vérification de N8N" -ForegroundColor $ColorInfo
Write-Host "------------------------------------------------------------" -ForegroundColor $ColorInfo

try {
    $response = Invoke-WebRequest -Uri "http://localhost:5678" -Method GET -TimeoutSec 5 -UseBasicParsing -ErrorAction Stop
    Write-Host "[OK] N8N est accessible sur http://localhost:5678" -ForegroundColor $ColorSuccess
    Write-Host "[INFO] Status Code: $($response.StatusCode)" -ForegroundColor $ColorInfo
    $TestsPassed++
} catch {
    Write-Host "[ERREUR] N8N n'est pas accessible" -ForegroundColor $ColorError
    Write-Host "[ERREUR] $($_.Exception.Message)" -ForegroundColor $ColorError
    Write-Host "[SOLUTION] Démarrer N8N avec: n8n start" -ForegroundColor $ColorWarning
    $TestsFailed++
}
Write-Host ""

# ============================================================
# TEST 5 : Test du webhook N8N Cas 14
# ============================================================
Write-Host "------------------------------------------------------------" -ForegroundColor $ColorInfo
Write-Host "TEST 5/7 - Test du webhook N8N Cas 14" -ForegroundColor $ColorInfo
Write-Host "------------------------------------------------------------" -ForegroundColor $ColorInfo

$webhookUrl = "http://localhost:5678/webhook/skill_frap_cas14"

try {
    $response = Invoke-WebRequest -Uri $webhookUrl -Method POST -ContentType "application/json" -TimeoutSec 10 -UseBasicParsing -ErrorAction Stop
    $jsonResponse = $response.Content | ConvertFrom-Json
    
    if ($jsonResponse.Data_integrale) {
        Write-Host "[OK] Webhook répond correctement" -ForegroundColor $ColorSuccess
        Write-Host "[INFO] URL: $webhookUrl" -ForegroundColor $ColorInfo
        
        # Compter les éléments
        $count = 0
        if ($jsonResponse.Data_integrale -is [Array]) {
            $count = $jsonResponse.Data_integrale.Count
        } else {
            $count = 1
        }
        Write-Host "[INFO] Nombre d'éléments dans Data_integrale: $count" -ForegroundColor $ColorInfo
        $TestsPassed++
    } else {
        throw "La réponse ne contient pas 'Data_integrale'"
    }
} catch {
    Write-Host "[ERREUR] Le webhook ne répond pas correctement" -ForegroundColor $ColorError
    Write-Host "[ERREUR] $($_.Exception.Message)" -ForegroundColor $ColorError
    Write-Host "[SOLUTION] Configurer le workflow N8N selon GUIDE_CONFIGURATION_N8N.md" -ForegroundColor $ColorWarning
    $TestsFailed++
}
Write-Host ""

# ============================================================
# TEST 6 : Création des dossiers de sortie
# ============================================================
Write-Host "------------------------------------------------------------" -ForegroundColor $ColorInfo
Write-Host "TEST 6/7 - Création des dossiers de sortie" -ForegroundColor $ColorInfo
Write-Host "------------------------------------------------------------" -ForegroundColor $ColorInfo

$directories = @(
    "sortie_word_cas14",
    "temp_frap_cas14",
    "data_json_from_n8n_cas14"
)

$dirsOK = $true
foreach ($dir in $directories) {
    try {
        if (-not (Test-Path $dir)) {
            New-Item -ItemType Directory -Path $dir -Force | Out-Null
        }
        Write-Host "[OK] Dossier créé/vérifié: $dir" -ForegroundColor $ColorSuccess
    } catch {
        Write-Host "[ERREUR] Impossible de créer le dossier: $dir" -ForegroundColor $ColorError
        Write-Host "[ERREUR] $($_.Exception.Message)" -ForegroundColor $ColorError
        $dirsOK = $false
    }
}

if ($dirsOK) {
    $TestsPassed++
} else {
    Write-Host "[SOLUTION] Vérifier les permissions d'écriture dans le répertoire courant" -ForegroundColor $ColorWarning
    $TestsFailed++
}
Write-Host ""

# ============================================================
# TEST 7 : Test du script de conversion
# ============================================================
Write-Host "------------------------------------------------------------" -ForegroundColor $ColorInfo
Write-Host "TEST 7/7 - Test du script de conversion" -ForegroundColor $ColorInfo
Write-Host "------------------------------------------------------------" -ForegroundColor $ColorInfo

# Vérifier que le script existe
if (-not (Test-Path "json2word_frap.py")) {
    Write-Host "[ERREUR] Le script json2word_frap.py n'existe pas" -ForegroundColor $ColorError
    Write-Host "[SOLUTION] Créer le script selon Phase 2 du TODO" -ForegroundColor $ColorWarning
    $TestsFailed++
    Write-Host ""
} else {
    # Créer un JSON de test minimal
    $testJson = @"
{
  "Data_integrale": [
    {
      "Etape mission - Frap": [
        {
          "table 1": {
            "Etape de mission": "Frap",
            "Norme": "Norme Test",
            "Méthode": "Méthode Test",
            "Reference": "TEST-AUTO-01"
          }
        },
        {
          "table 2": {
            "Intitule": "Test automatisé de conversion"
          }
        },
        {
          "table 3": {
            "Observation": "Observation de test"
          }
        },
        {
          "table 4": {
            "Constat": "Constat de test"
          }
        },
        {
          "table 5": {
            "Risque": "Risque de test"
          }
        },
        {
          "table 6": {
            "Recommendation": "Recommandation de test"
          }
        }
      ]
    }
  ]
}
"@

    $testJsonFile = "test_frap_auto.json"
    $testJson | Out-File -FilePath $testJsonFile -Encoding UTF8

    try {
        # Exécuter le script de conversion
        Write-Host "[INFO] Exécution: python json2word_frap.py $testJsonFile" -ForegroundColor $ColorInfo
        python json2word_frap.py $testJsonFile 2>&1 | Out-String | Write-Host
        
        if ($LASTEXITCODE -eq 0) {
            # Vérifier qu'un fichier .docx a été créé
            $docxFiles = Get-ChildItem -Path "sortie_word_cas14" -Filter "TEST-AUTO-01*.docx" -ErrorAction SilentlyContinue
            
            if ($docxFiles) {
                Write-Host "[OK] Document Word généré avec succès" -ForegroundColor $ColorSuccess
                Write-Host "[INFO] Fichier: $($docxFiles[0].Name)" -ForegroundColor $ColorInfo
                $TestsPassed++
            } else {
                throw "Aucun fichier .docx généré"
            }
        } else {
            throw "Le script a retourné une erreur (code: $LASTEXITCODE)"
        }
    } catch {
        Write-Host "[ERREUR] La conversion a échoué" -ForegroundColor $ColorError
        Write-Host "[ERREUR] $($_.Exception.Message)" -ForegroundColor $ColorError
        Write-Host "[SOLUTION] Vérifier les logs du script et corriger les erreurs" -ForegroundColor $ColorWarning
        $TestsFailed++
    } finally {
        # Nettoyage
        if (Test-Path $testJsonFile) {
            Remove-Item $testJsonFile -Force -ErrorAction SilentlyContinue
        }
    }
    Write-Host ""
}

# ============================================================
# RÉSUMÉ FINAL
# ============================================================
Write-Host ""
Write-Host "============================================================" -ForegroundColor $ColorInfo
Write-Host "    RÉSUMÉ DES TESTS" -ForegroundColor $ColorInfo
Write-Host "============================================================" -ForegroundColor $ColorInfo
Write-Host ""
Write-Host "Total de tests: $TotalTests" -ForegroundColor $ColorInfo
Write-Host "Tests réussis:  $TestsPassed" -ForegroundColor $ColorSuccess
Write-Host "Tests échoués:  $TestsFailed" -ForegroundColor $(if ($TestsFailed -eq 0) { $ColorSuccess } else { $ColorError })
Write-Host ""

$successRate = [math]::Round(($TestsPassed / $TotalTests) * 100, 2)
Write-Host "Taux de succès: $successRate%" -ForegroundColor $(if ($successRate -eq 100) { $ColorSuccess } elseif ($successRate -ge 70) { $ColorWarning } else { $ColorError })
Write-Host ""

if ($TestsFailed -eq 0) {
    Write-Host "============================================================" -ForegroundColor $ColorSuccess
    Write-Host "    ✅ TOUS LES TESTS SONT PASSÉS AVEC SUCCÈS ✅" -ForegroundColor $ColorSuccess
    Write-Host "============================================================" -ForegroundColor $ColorSuccess
    Write-Host ""
    Write-Host "[INFO] Le Cas 14 est opérationnel et prêt pour la production." -ForegroundColor $ColorSuccess
    Write-Host "[INFO] Vous pouvez maintenant exécuter: .\execute_cas14.bat" -ForegroundColor $ColorInfo
    $exitCode = 0
} else {
    Write-Host "============================================================" -ForegroundColor $ColorError
    Write-Host "    ❌ CERTAINS TESTS ONT ÉCHOUÉ ❌" -ForegroundColor $ColorError
    Write-Host "============================================================" -ForegroundColor $ColorError
    Write-Host ""
    Write-Host "[ACTION] Corriger les erreurs identifiées et relancer les tests." -ForegroundColor $ColorWarning
    Write-Host "[COMMANDE] .\test_workflow_cas14.ps1" -ForegroundColor $ColorInfo
    $exitCode = 1
}

Write-Host ""
Write-Host "[INFO] Fin des tests - $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" -ForegroundColor $ColorInfo
Write-Host ""

# Code de sortie
exit $exitCode
