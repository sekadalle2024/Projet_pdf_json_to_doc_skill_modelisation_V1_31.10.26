@echo off
REM ============================================================================
REM Script Batch : execute_cas2.bat
REM Description : Exécute le workflow complet du Cas 2
REM              1. Appel API N8N
REM              2. Collecte Data_integrale  
REM              3. Exécution skill audit-procedures-json2word
REM Date : 31 octobre 2026
REM ============================================================================

echo.
echo ======================================================================
echo   WORKFLOW CAS 2 - Appel API N8N + Execution Skill
echo ======================================================================
echo.

REM Se placer dans le dossier du script
cd /d "%~dp0"

REM Activer l'environnement Conda
echo [INFO] Activation de l'environnement pdf_excel_env...
call conda activate pdf_excel_env

if %ERRORLEVEL% NEQ 0 (
    echo [ERREUR] Impossible d'activer l'environnement Conda
    pause
    exit /b 1
)

echo [SUCCESS] Environnement active
echo.

REM Demander confirmation
set /p CONFIRM="Voulez-vous lancer le workflow Cas 2 ? (O/N) : "
if /i "%CONFIRM%" NEQ "O" (
    echo [INFO] Operation annulee
    pause
    exit /b 0
)

echo.
echo [INFO] Lancement du workflow...
echo.

REM Exécuter le script Python principal
python execute_cas2_workflow.py

REM Vérifier le code de sortie
if %ERRORLEVEL% EQU 0 (
    echo.
    echo ======================================================================
    echo   SUCCESS - Workflow Cas 2 termine avec succes
    echo ======================================================================
    echo.
    
    REM Proposer d'ouvrir le dossier de sortie
    set /p OPEN_FOLDER="Voulez-vous ouvrir le dossier des documents Word ? (O/N) : "
    if /i "%OPEN_FOLDER%" EQU "O" (
        start "" "sortie_word_cas2"
    )
) else (
    echo.
    echo ======================================================================
    echo   ERREUR - Le workflow a echoue
    echo ======================================================================
    echo.
    echo Consultez les logs ci-dessus pour plus de details
)

echo.
echo Appuyez sur une touche pour quitter...
pause >nul
exit /b %ERRORLEVEL%
