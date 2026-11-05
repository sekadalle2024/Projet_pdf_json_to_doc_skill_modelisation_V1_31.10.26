@echo off
REM ============================================================
REM Script d'Exécution Cas 14 - FRAP et Recommandations
REM ============================================================
REM
REM Description:
REM   Ce script batch exécute le workflow complet du Cas 14:
REM   1. Appel API N8N pour récupérer les données FRAP
REM   2. Conversion JSON → Word (documents .docx)
REM
REM Prérequis:
REM   - Python >= 3.9 installé
REM   - Environnement conda 'pdf_excel_env' activé
REM   - N8N en cours d'exécution (http://localhost:5678)
REM   - Dépendances Python installées (python-docx, requests)
REM
REM Usage:
REM   execute_cas14.bat
REM
REM Auteur: Kiro AI
REM Date: 31 octobre 2026
REM Version: 1.0.0
REM ============================================================

echo.
echo ============================================================
echo    CAS 14 - FRAP ET RECOMMANDATIONS D'AUDIT
echo    Workflow Automatise de Generation de Documents
echo ============================================================
echo.
echo [INFO] Demarrage du workflow Cas 14...
echo [INFO] Date/Heure: %date% %time%
echo.

REM Vérification de Python
echo [ETAPE 1/3] Verification de Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERREUR] Python n'est pas installe ou n'est pas dans le PATH.
    echo [SOLUTION] Installer Python ^>= 3.9 et relancer le script.
    pause
    exit /b 1
)
python --version
echo [OK] Python detecte.
echo.

REM Vérification de l'environnement conda (optionnel)
echo [ETAPE 2/3] Verification de l'environnement conda...
conda info --envs | findstr "pdf_excel_env" >nul 2>&1
if %errorlevel% equ 0 (
    echo [INFO] Environnement conda 'pdf_excel_env' detecte.
    echo [INFO] Assurez-vous qu'il est active: conda activate pdf_excel_env
) else (
    echo [WARNING] Environnement conda 'pdf_excel_env' non detecte.
    echo [INFO] Execution avec l'environnement Python par defaut.
)
echo.

REM Vérification de N8N (optionnel mais recommandé)
echo [INFO] Verification rapide de N8N...
curl -s http://localhost:5678 >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] N8N est accessible sur http://localhost:5678
) else (
    echo [WARNING] N8N ne semble pas accessible sur http://localhost:5678
    echo [INFO] Assurez-vous que N8N est demarre: n8n start
    echo [INFO] Le script continuera mais pourrait echouer si N8N n'est pas actif.
)
echo.

REM Exécution du script principal
echo [ETAPE 3/3] Execution du script de production...
echo.
echo ============================================================
echo    DEBUT DE L'EXECUTION
echo ============================================================
echo.

python execute_cas14_production.py

REM Capture du code de sortie
set EXIT_CODE=%errorlevel%

echo.
echo ============================================================
echo    FIN DE L'EXECUTION
echo ============================================================
echo.

if %EXIT_CODE% equ 0 (
    echo [SUCCES] Le workflow Cas 14 s'est termine avec succes.
    echo [INFO] Code de sortie: %EXIT_CODE%
    echo [INFO] Verifiez les documents generes dans: sortie_word_cas14\
) else (
    echo [ERREUR] Le workflow Cas 14 a echoue.
    echo [INFO] Code de sortie: %EXIT_CODE%
    echo [INFO] Consultez les logs ci-dessus pour plus de details.
)

echo.
echo [INFO] Fin du script - %date% %time%
echo.

pause
exit /b %EXIT_CODE%
