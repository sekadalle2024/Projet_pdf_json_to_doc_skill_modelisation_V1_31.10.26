@echo off
REM ═══════════════════════════════════════════════════════════════════════════
REM     CAS 10 - LANCEUR WINDOWS
REM     Script batch pour exécuter l'orchestrateur Cas 10
REM ═══════════════════════════════════════════════════════════════════════════
REM
REM Description:
REM     Lance l'orchestrateur Cas 10 dans l'environnement conda pdf_excel_env
REM
REM Utilisation:
REM     execute_cas10.bat
REM
REM Auteur: Expert Python & Automation
REM Date: 5 novembre 2026
REM Version: 1.0.0
REM ═══════════════════════════════════════════════════════════════════════════

echo.
echo ═══════════════════════════════════════════════════════════════════════════
echo     CAS 10 - ORCHESTRATEUR MULTI-WORKFLOW
echo ═══════════════════════════════════════════════════════════════════════════
echo.

REM Activation de l'environnement conda
echo [ÉTAPE 1] Activation de l'environnement conda...
call conda activate pdf_excel_env
if errorlevel 1 (
    echo ❌ ERREUR: Impossible d'activer l'environnement conda pdf_excel_env
    echo.
    echo Vérifiez que:
    echo   1. Conda est installé
    echo   2. L'environnement pdf_excel_env existe
    echo.
    pause
    exit /b 1
)
echo ✅ Environnement activé
echo.

REM Vérification de Python
echo [ÉTAPE 2] Vérification de Python...
python --version
if errorlevel 1 (
    echo ❌ ERREUR: Python n'est pas disponible
    pause
    exit /b 1
)
echo ✅ Python OK
echo.

REM Vérification des dépendances
echo [ÉTAPE 3] Vérification des dépendances...
python -c "import requests; import docx; print('✅ Dépendances OK')"
if errorlevel 1 (
    echo ❌ ERREUR: Dépendances manquantes
    echo.
    echo Installation des dépendances...
    pip install requests python-docx
    if errorlevel 1 (
        echo ❌ Échec de l'installation
        pause
        exit /b 1
    )
)
echo.

REM Exécution de l'orchestrateur
echo [ÉTAPE 4] Lancement de l'orchestrateur...
echo.
python execute_cas10_orchestrator.py
set EXIT_CODE=%errorlevel%

echo.
if %EXIT_CODE% == 0 (
    echo ═══════════════════════════════════════════════════════════════════════════
    echo     ✅ ORCHESTRATION TERMINÉE AVEC SUCCÈS
    echo ═══════════════════════════════════════════════════════════════════════════
) else (
    echo ═══════════════════════════════════════════════════════════════════════════
    echo     ❌ ORCHESTRATION ÉCHOUÉE (Code: %EXIT_CODE%^)
    echo ═══════════════════════════════════════════════════════════════════════════
)

echo.
echo Appuyez sur une touche pour quitter...
pause >nul

exit /b %EXIT_CODE%
