@echo off
REM Script : execute_cas5.bat
REM Description : Lanceur Windows pour Cas 5 - FRAP et Recommandations
REM Date : 5 novembre 2026

echo ========================================
echo   CAS 8 - PROGRAMME DE TRAVAIL
echo ========================================
echo.

REM Activer l'environnement conda
call conda activate pdf_excel_env

REM Vérifier l'activation
if %ERRORLEVEL% NEQ 0 (
    echo ERREUR : Impossible d'activer l'environnement pdf_excel_env
    pause
    exit /b 1
)

REM Exécuter le script
python execute_cas8_production.py

REM Afficher le résultat
if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================
    echo   SUCCES
    echo ========================================
) else (
    echo.
    echo ========================================
    echo   ERREUR
    echo ========================================
)

pause
