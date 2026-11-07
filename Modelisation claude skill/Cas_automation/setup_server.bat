@echo off
REM Script de configuration initiale du serveur d'automation

echo ========================================
echo Configuration Serveur Automation
echo ========================================
echo.

REM Vérifier que miniconda est installé
where conda >nul 2>&1
if errorlevel 1 (
    echo [ERREUR] Miniconda non trouve
    echo Installez miniconda d'abord : https://docs.conda.io/en/latest/miniconda.html
    pause
    exit /b 1
)

echo [OK] Miniconda detecte
echo.

REM Activer l'environnement
echo Activation de l'environnement pdf_excel_env...
call conda activate pdf_excel_env

if errorlevel 1 (
    echo [ERREUR] Environnement pdf_excel_env non trouve
    echo Creez-le d'abord avec: conda env create -f ../../environment.yml
    pause
    exit /b 1
)

echo [OK] Environnement active
echo.

REM Installer les dépendances du serveur
echo Installation des dependances serveur...
pip install -r requirements_server.txt

if errorlevel 1 (
    echo [ERREUR] Installation des dependances echouee
    pause
    exit /b 1
)

echo [OK] Dependances installees
echo.

REM Créer le dossier output
if not exist "output" mkdir output
echo [OK] Dossier output cree
echo.

REM Vérifier les fichiers JSON standards
echo Verification des fichiers JSON standards...
set ERROR_JSON=0

if not exist "json standard\Json_standard_[Cas 6].txt" (
    echo [ATTENTION] Json_standard_[Cas 6].txt manquant
    set ERROR_JSON=1
)

if not exist "json standard\Json_standard_[Cas 7].txt" (
    echo [ATTENTION] Json_standard_[Cas 7].txt manquant
    set ERROR_JSON=1
)

if not exist "json standard\Json_standard_[Cas 8].txt" (
    echo [ATTENTION] Json_standard_[Cas 8].txt manquant
    set ERROR_JSON=1
)

if %ERROR_JSON%==0 (
    echo [OK] Tous les JSON standards presents
) else (
    echo [ATTENTION] Certains JSON standards manquent
)
echo.

REM Vérifier les templates standards
echo Verification des templates standards...
set ERROR_TEMPLATE=0

if not exist "template_standard\template_standard_[Cas 6].docx" (
    echo [ATTENTION] template_standard_[Cas 6].docx manquant
    set ERROR_TEMPLATE=1
)

if not exist "template_standard\template_standard_[Cas 7].docx" (
    echo [ATTENTION] template_standard_[Cas 7].docx manquant
    set ERROR_TEMPLATE=1
)

if not exist "template_standard\template_standard_[Cas 8].docx" (
    echo [ATTENTION] template_standard_[Cas 8].docx manquant
    set ERROR_TEMPLATE=1
)

if %ERROR_TEMPLATE%==0 (
    echo [OK] Tous les templates standards presents
) else (
    echo [ATTENTION] Certains templates standards manquent
)
echo.

REM Résumé
echo ========================================
echo Configuration terminee
echo ========================================
echo.
echo Prochaines etapes:
echo 1. Demarrer le serveur : start_server.bat
echo 2. Tester le serveur  : python test_server.py
echo 3. Consulter la doc   : README_SERVEUR.md
echo.

pause
