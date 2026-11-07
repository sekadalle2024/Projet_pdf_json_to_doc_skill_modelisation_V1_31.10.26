@echo off
REM Exemples de requêtes cURL pour tester le serveur d'automation

echo ========================================
echo Exemples de requetes cURL
echo ========================================
echo.

echo 1. Test Health Check
echo curl http://localhost:5000/health
echo.

echo 2. Generation Cas 6 (Feuille Revision)
echo curl -X POST http://localhost:5000/automation/cas_6 ^
echo      -H "Content-Type: application/json" ^
echo      -d @"json standard/Json_standard_[Cas 6].txt" ^
echo      -o output_cas6.docx
echo.

echo 3. Generation Cas 7 (Feuille Couverture)
echo curl -X POST http://localhost:5000/automation/cas_7 ^
echo      -H "Content-Type: application/json" ^
echo      -d @"json standard/Json_standard_[Cas 7].txt" ^
echo      -o output_cas7.docx
echo.

echo 4. Generation Cas 8 (Modele Standard)
echo curl -X POST http://localhost:5000/automation/cas_8 ^
echo      -H "Content-Type: application/json" ^
echo      -d @"json standard/Json_standard_[Cas 8].txt" ^
echo      -o output_cas8.docx
echo.

echo 5. Test avec JSON standard (Cas 6)
echo curl http://localhost:5000/automation/test/6 -o test_cas6.docx
echo.

echo ========================================
echo Choisissez une action:
echo ========================================
echo 1 - Test Health Check
echo 2 - Generation Cas 6
echo 3 - Generation Cas 7
echo 4 - Generation Cas 8
echo 5 - Test avec JSON standard (Cas 6)
echo 6 - Test avec JSON standard (Cas 7)
echo 7 - Test avec JSON standard (Cas 8)
echo 0 - Quitter
echo.

set /p choix="Votre choix: "

if "%choix%"=="1" (
    echo.
    echo Execution: Health Check
    curl http://localhost:5000/health
    echo.
    goto :end
)

if "%choix%"=="2" (
    echo.
    echo Execution: Generation Cas 6
    curl -X POST http://localhost:5000/automation/cas_6 -H "Content-Type: application/json" -d @"json standard/Json_standard_[Cas 6].txt" -o output_cas6.docx
    echo.
    echo Fichier genere: output_cas6.docx
    goto :end
)

if "%choix%"=="3" (
    echo.
    echo Execution: Generation Cas 7
    curl -X POST http://localhost:5000/automation/cas_7 -H "Content-Type: application/json" -d @"json standard/Json_standard_[Cas 7].txt" -o output_cas7.docx
    echo.
    echo Fichier genere: output_cas7.docx
    goto :end
)

if "%choix%"=="4" (
    echo.
    echo Execution: Generation Cas 8
    curl -X POST http://localhost:5000/automation/cas_8 -H "Content-Type: application/json" -d @"json standard/Json_standard_[Cas 8].txt" -o output_cas8.docx
    echo.
    echo Fichier genere: output_cas8.docx
    goto :end
)

if "%choix%"=="5" (
    echo.
    echo Execution: Test Cas 6
    curl http://localhost:5000/automation/test/6 -o test_cas6.docx
    echo.
    echo Fichier genere: test_cas6.docx
    goto :end
)

if "%choix%"=="6" (
    echo.
    echo Execution: Test Cas 7
    curl http://localhost:5000/automation/test/7 -o test_cas7.docx
    echo.
    echo Fichier genere: test_cas7.docx
    goto :end
)

if "%choix%"=="7" (
    echo.
    echo Execution: Test Cas 8
    curl http://localhost:5000/automation/test/8 -o test_cas8.docx
    echo.
    echo Fichier genere: test_cas8.docx
    goto :end
)

if "%choix%"=="0" (
    goto :end
)

echo Choix invalide

:end
pause
