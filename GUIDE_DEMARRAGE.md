# 🚀 Guide de Démarrage Rapide

## Étape 1: Installation de Miniconda (si nécessaire)

### Téléchargement Windows

Ouvrez PowerShell et exécutez:

```powershell
# Télécharger l'installateur Miniconda
Invoke-WebRequest -Uri "https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe" -OutFile "$env:USERPROFILE\Downloads\MinicondaInstaller.exe"

# Lancer l'installateur
Start-Process "$env:USERPROFILE\Downloads\MinicondaInstaller.exe" -Wait
```

Ou téléchargez manuellement depuis: https://docs.conda.io/en/latest/miniconda.html

**Important**: Cochez l'option "Add Miniconda to PATH" pendant l'installation.

---

## Étape 2: Configuration de l'Environnement

### Option A: Installation Automatique (Recommandé)

```powershell
# Se placer dans le répertoire du projet
cd H:\Projet_pdf_excel

# Exécuter le script d'installation
.\setup_environment.ps1
```

### Option B: Installation Manuelle

```powershell
# Se placer dans le répertoire du projet
cd H:\Projet_pdf_excel

# Créer l'environnement
conda env create -f environment.yml

# Activer l'environnement
conda activate pdf_excel_env
```

---

## Étape 3: Vérification de l'Installation

```powershell
# Activer l'environnement
conda activate pdf_excel_env

# Tester l'installation
python test_installation.py
```

Vous devriez voir:
```
✨ Toutes les librairies sont installées avec succès!
🎉 TOUS LES TESTS SONT PASSÉS AVEC SUCCÈS! 🎉
```

---

## Étape 4: Premier Test

Créez un fichier `test_simple.py`:

```python
import pandas as pd
from pypdf import PdfWriter
from docx import Document

print("✅ Toutes les imports fonctionnent!")
print("🎉 Vous êtes prêt à travailler!")
```

Exécutez:
```powershell
python test_simple.py
```

---

## 📝 Commandes Utiles

### Gestion de l'environnement

```powershell
# Activer l'environnement
conda activate pdf_excel_env

# Désactiver l'environnement
conda deactivate

# Lister les environnements
conda env list

# Lister les packages installés
conda list
pip list

# Mettre à jour un package
pip install --upgrade nom_package

# Supprimer l'environnement
conda env remove -n pdf_excel_env
```

### Installer des packages supplémentaires

```powershell
# Activer l'environnement d'abord
conda activate pdf_excel_env

# Installer via pip
pip install nom_package

# Installer via conda
conda install nom_package
```

---

## 🎯 Prochaines Étapes

1. **Consulter les exemples** dans `README.md`
2. **Créer vos premiers scripts** de manipulation PDF/Excel/Word
3. **Tester les fonctionnalités** avancées:
   - Découpage de PDF
   - Consolidation de documents
   - Extraction de tableaux
   - Génération de rapports

---

## ⚠️ Dépannage

### Problème: "conda not recognized"

**Solution**: Redémarrez PowerShell après l'installation de Miniconda, ou ajoutez manuellement Miniconda au PATH.

```powershell
# Vérifier le PATH
$env:PATH

# Ajouter temporairement (remplacez par votre chemin)
$env:PATH += ";C:\Users\LEADER\miniconda3\Scripts"
$env:PATH += ";C:\Users\LEADER\miniconda3"
```

### Problème: Erreurs lors de l'installation de packages

**Solution**: Installer les packages un par un pour identifier le problème.

```powershell
conda activate pdf_excel_env
pip install pypdf
pip install PyMuPDF
# ... etc
```

### Problème: "Execution policy" lors de l'exécution du script .ps1

**Solution**: Autoriser l'exécution de scripts temporairement.

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
.\setup_environment.ps1
```

### Problème: Camelot ou Tabula ne fonctionnent pas

**Solution**: Ces librairies nécessitent des dépendances système supplémentaires.

- **Camelot**: Nécessite Ghostscript et Tkinter
- **Tabula**: Nécessite Java Runtime Environment (JRE)

Si vous n'en avez pas besoin, vous pouvez les ignorer.

---

## 📞 Support

- **Documentation Miniconda**: https://docs.conda.io/
- **Documentation Pandas**: https://pandas.pydata.org/
- **Documentation PyPDF**: https://pypdf.readthedocs.io/

---

**Bonne chance avec votre projet! 🚀**
