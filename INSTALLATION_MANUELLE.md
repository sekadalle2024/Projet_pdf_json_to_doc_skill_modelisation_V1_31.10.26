# 📦 Guide d'Installation Manuelle

L'environnement `pdf_excel_env` existe déjà. Il faut simplement installer les packages Python nécessaires.

## ✅ Option 1: Installation Automatique (Recommandé)

Ouvrez PowerShell et exécutez:

```powershell
cd H:\Projet_pdf_excel
.\install_packages.bat
```

Ce script installera tous les packages nécessaires par étapes.

---

## 🔧 Option 2: Installation Manuelle pas à pas

### Étape 1: Activer l'environnement

```powershell
conda activate pdf_excel_env
```

### Étape 2: Installer les packages PDF

```powershell
pip install pypdf pikepdf pdfplumber reportlab fpdf2
```

### Étape 3: Installer PyMuPDF (peut prendre du temps)

```powershell
pip install PyMuPDF
```

### Étape 4: Installer les packages Excel

```powershell
pip install xlsxwriter xlwt pyexcel pyexcel-xls pyexcel-xlsx formulas
```

### Étape 5: Installer les packages Word

```powershell
pip install python-docx docx2txt docxtpl mammoth
```

### Étape 6: Installer Pandas et NumPy

```powershell
pip install pandas numpy
```

### Étape 7: Installer les packages de visualisation

```powershell
pip install matplotlib seaborn plotly scipy scikit-learn
```

### Étape 8: Installer les utilitaires

```powershell
pip install watchdog send2trash fs filetype pillow lxml beautifulsoup4 tqdm
```

---

## 🧪 Vérifier l'Installation

Une fois l'installation terminée:

```powershell
conda activate pdf_excel_env
python test_installation.py
```

Vous devriez voir:
```
✨ Toutes les librairies sont installées avec succès!
🎉 TOUS LES TESTS SONT PASSÉS AVEC SUCCÈS! 🎉
```

---

## 📝 Packages Déjà Installés

D'après les vérifications, ces packages sont déjà présents:
- ✅ pypdf
- ✅ pikepdf
- ✅ reportlab
- ✅ fpdf2
- ✅ pillow
- ✅ lxml
- ✅ numpy

Il reste à installer:
- ⏳ PyMuPDF (gros package, prend du temps)
- ⏳ pdfplumber
- ⏳ xlsxwriter
- ⏳ python-docx
- ⏳ pandas
- ⏳ matplotlib
- ⏳ Et autres packages listés ci-dessus

---

## ⚡ Installation Rapide (Packages Essentiels Uniquement)

Si vous voulez juste les packages essentiels pour commencer rapidement:

```powershell
conda activate pdf_excel_env
pip install -r requirements_minimal.txt
```

---

## ⚠️ Notes Importantes

### Temps d'Installation
- PyMuPDF peut prendre 5-10 minutes à télécharger (package volumineux)
- matplotlib peut prendre 3-5 minutes
- Soyez patient, les packages se téléchargent en arrière-plan

### Si pip freeze ou timeout
- Appuyez sur `Ctrl+C` pour annuler
- Réessayez avec `--no-cache-dir`:
  ```powershell
  pip install --no-cache-dir nom_du_package
  ```

### Si "normal site-packages is not writeable"
C'est normal! Les packages s'installent dans votre espace utilisateur.
Cela n'empêche pas l'installation de fonctionner.

---

## 🎯 Test Rapide

Créez un fichier `test_rapide.py`:

```python
# Test rapide des imports critiques
try:
    import pypdf
    print("✅ pypdf")
except: print("❌ pypdf")

try:
    import pikepdf
    print("✅ pikepdf")
except: print("❌ pikepdf")

try:
    import reportlab
    print("✅ reportlab")
except: print("❌ reportlab")

try:
    import pandas as pd
    print("✅ pandas")
except: print("❌ pandas")

try:
    from docx import Document
    print("✅ python-docx")
except: print("❌ python-docx")

try:
    import xlsxwriter
    print("✅ xlsxwriter")
except: print("❌ xlsxwriter")

try:
    import matplotlib
    print("✅ matplotlib")
except: print("❌ matplotlib")

print("\nTest terminé!")
```

Exécutez:
```powershell
conda activate pdf_excel_env
python test_rapide.py
```

---

## 📞 En cas de problème

### Problème: Package ne s'installe pas
```powershell
# Essayer avec --upgrade
pip install --upgrade --no-cache-dir nom_package

# Ou avec --force-reinstall
pip install --force-reinstall nom_package
```

### Problème: "No module named 'xxx'"
```powershell
# Vérifier que l'environnement est activé
conda activate pdf_excel_env

# Vérifier que le package est installé
pip list | findstr nom_package

# Réinstaller si nécessaire
pip install nom_package
```

### Problème: Timeout lors de l'installation
Les gros packages (PyMuPDF, matplotlib) prennent du temps.
Installez-les séparément et laissez le temps au téléchargement.

---

**💡 Astuce**: Ouvrez plusieurs fenêtres PowerShell et installez différents packages en parallèle pour gagner du temps!

```powershell
# Fenêtre 1
conda activate pdf_excel_env
pip install PyMuPDF

# Fenêtre 2
conda activate pdf_excel_env
pip install pandas matplotlib

# Fenêtre 3
conda activate pdf_excel_env
pip install python-docx xlsxwriter
```

---

Bonne installation! 🚀
