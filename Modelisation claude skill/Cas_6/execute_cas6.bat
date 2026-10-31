@echo off
REM ============================================================================
REM Script Batch : execute_cas6.bat
REM Description : Lance le workflow Cas 6 - Feuilles de Révision d'Audit
REM ============================================================================

echo.
echo ========================================================================
echo   WORKFLOW CAS 6 - FEUILLES DE REVISION D'AUDIT
echo   Execution du script Python execute_cas6_production.py
echo ========================================================================
echo.

REM Vérifier si Python est installé
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERREUR] Python n'est pas installé ou n'est pas dans le PATH
    pause
    exit /b 1
)

REM Vérifier si N8N est accessible
echo Verification de N8N...
curl -s http://localhost:5678 >nul 2>&1
if errorlevel 1 (
    echo [ATTENTION] N8N ne semble pas accessible sur localhost:5678
    echo Assurez-vous que N8N est demarre : n8n start
    echo.
)

REM Exécuter le script Python
python execute_cas6_production.py

REM Afficher le code de sortie
if errorlevel 1 (
    echo.
    echo [ERREUR] Le workflow a rencontre des erreurs
) else (
    echo.
    echo [SUCCES] Workflow termine avec succes
)

echo.
pause
