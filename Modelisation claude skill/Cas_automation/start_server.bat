@echo off
chcp 65001 > nul
REM Script de démarrage du serveur d'automation
REM Utilise l'environnement miniconda pdf_excel_env

echo ======================================================================
echo DEMARRAGE SERVEUR AUTOMATION
echo ======================================================================
echo.

REM Activer l'environnement conda
echo Activation de l'environnement pdf_excel_env...
call conda activate pdf_excel_env

REM Vérifier l'activation
if errorlevel 1 (
    echo [ERREUR] Impossible d'activer l'environnement pdf_excel_env
    echo Verifiez que miniconda est installe et que l'environnement existe
    pause
    exit /b 1
)

echo [OK] Environnement pdf_excel_env active
echo.

REM Vérifier les imports
echo Verification des modules...
python verifier_imports.py
if errorlevel 1 (
    echo.
    echo [AVERTISSEMENT] Certains modules sont indisponibles
    echo Le serveur demarrera mais avec des fonctionnalites limitees
    echo.
    choice /C ON /M "Continuer quand meme (O=Oui, N=Non)"
    if errorlevel 2 exit /b 1
)
echo.

REM Démarrer le serveur
echo ======================================================================
echo Demarrage du serveur sur http://localhost:5000
echo Appuyez sur Ctrl+C pour arreter le serveur
echo ======================================================================
echo.

python server_automation.py

pause
