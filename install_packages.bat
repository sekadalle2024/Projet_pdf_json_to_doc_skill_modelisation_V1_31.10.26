@echo off
echo ==========================================
echo Installation des packages Python
echo ==========================================
echo.

call conda activate pdf_excel_env

echo Etape 1/5: Installation des packages PDF de base...
pip install --no-cache-dir pypdf pikepdf pdfplumber reportlab fpdf2
if %errorlevel% neq 0 echo Erreur PDF, mais on continue...

echo.
echo Etape 2/5: Installation de PyMuPDF...
pip install --no-cache-dir PyMuPDF
if %errorlevel% neq 0 echo Erreur PyMuPDF, mais on continue...

echo.
echo Etape 3/5: Installation des packages Excel...
pip install --no-cache-dir xlsxwriter xlwt pyexcel pyexcel-xls pyexcel-xlsx xlwings pyxlsb formulas
if %errorlevel% neq 0 echo Erreur Excel, mais on continue...

echo.
echo Etape 4/5: Installation des packages Word...
pip install --no-cache-dir python-docx docx2txt docxtpl mammoth
if %errorlevel% neq 0 echo Erreur Word, mais on continue...

echo.
echo Etape 5/5: Installation des packages d'analyse...
pip install --no-cache-dir matplotlib seaborn plotly scipy scikit-learn
if %errorlevel% neq 0 echo Erreur analyse, mais on continue...

echo.
echo Etape 6/6: Installation des packages systeme...
pip install --no-cache-dir watchdog send2trash fs filetype pillow lxml beautifulsoup4 tqdm
if %errorlevel% neq 0 echo Erreur systeme, mais on continue...

echo.
echo ==========================================
echo Installation terminee!
echo ==========================================
echo.
echo Pour tester: python test_installation.py
pause
