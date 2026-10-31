# 📚 Exemples d'Utilisation

Ce dossier contient des exemples pratiques pour manipuler PDF, Excel et Word.

## 🚀 Lancer les Exemples

```powershell
# Activer l'environnement
conda activate pdf_excel_env

# Se placer dans le dossier exemples
cd H:\Projet_pdf_excel\exemples

# Lancer un exemple
python exemple_01_decoupe_pdf.py
```

---

## 📄 Exemple 1: Découpage de PDF

**Fichier**: `exemple_01_decoupe_pdf.py`

**Ce qu'il fait**:
- Lit un PDF du dossier `../Extraction/`
- Extrait les 3 premières pages
- Sauvegarde dans `../Base_pdf/extrait_3_premieres_pages.pdf`

**Utilisation**:
```python
from pypdf import PdfReader, PdfWriter

decouper_pdf("document.pdf", 0, 2, "extrait.pdf")
# Extrait les pages 0, 1, 2 (3 premières pages)
```

---

## 📊 Exemple 2: Excel → PDF avec Style

**Fichier**: `exemple_02_excel_vers_pdf.py`

**Ce qu'il fait**:
- Crée un fichier Excel d'exemple avec des données de ventes
- Convertit en PDF avec un tableau stylé (couleurs, bordures)
- Sauvegarde dans `../Base_pdf/rapport_ventes.pdf`

**Résultat**:
- Tableau avec en-tête bleu
- Lignes alternées (blanc/gris)
- Bordures noires
- Centré et formaté

---

## 📝 Exemple 3: Excel → Word avec Style

**Fichier**: `exemple_03_excel_vers_word.py`

**Ce qu'il fait**:
- Crée un fichier Excel d'exemple avec un inventaire
- Convertit en document Word avec tableau stylé
- Sauvegarde dans `../Base_excel/rapport_inventaire.docx`

**Résultat**:
- Titre centré
- Tableau avec style "Light Grid Accent 1"
- Colonnes ajustées
- En-têtes en gras

---

## 🎯 Prochaines Étapes

Créez vos propres scripts en vous inspirant de ces exemples!

**Idées de projets**:
1. Automatiser la génération de rapports mensuels
2. Fusionner tous les PDFs d'un dossier
3. Extraire des données Excel et créer des graphiques PDF
4. Convertir des tableaux Word en Excel
5. Créer des factures PDF à partir d'Excel

---

Bon codage! 🚀
