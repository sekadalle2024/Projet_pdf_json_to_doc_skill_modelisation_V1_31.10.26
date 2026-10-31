@echo off
REM ===========================================================================
REM Script : execute_cas3.bat
REM Description : Lance le workflow Cas 3 Production (Manuel Audit via N8N)
REM Auteur : Expert Python & Automation
REM Date : 31 octobre 2026
REM ===========================================================================

echo.
echo =======================================================================
echo   Workflow Cas 3 - Manuel Audit (Production)
echo   API N8N : http://localhost:5678/webhook/skill_manuel_audit_cas3
echo =======================================================================
echo.

REM Activer l'environnement conda si disponible
if exist "%USERPROFILE%\anaconda3\Scripts\activate.bat" (
    echo Activation de l'environnement Conda...
    call "%USERPROFILE%\anaconda3\Scripts\activate.bat" pdf_excel_env
)

REM Aller dans le dossier du script
cd /d "%~dp0"

REM Exécuter le script Python principal
echo Lancement du workflow Cas 3...
echo.
python execute_cas3_production.py

REM Vérifier le code de sortie
if %ERRORLEVEL% EQU 0 (
    echo.
    echo =======================================================================
    echo   Workflow termine avec succes !
    echo =======================================================================
) else (
    echo.
    echo =======================================================================
    echo   Erreur lors de l'execution du workflow
    echo   Code de sortie : %ERRORLEVEL%
    echo =======================================================================
)

echo.
pause
