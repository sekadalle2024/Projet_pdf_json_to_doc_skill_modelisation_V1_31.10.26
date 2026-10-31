"""
Script de vérification de l'installation
Teste toutes les librairies critiques du projet
"""

import sys

def test_imports():
    print("=" * 60)
    print("🔍 VÉRIFICATION DE L'ENVIRONNEMENT PYTHON")
    print("=" * 60)
    print()
    
    # Définir les catégories et librairies à tester
    libraries = {
        '📄 PDF': {
            'pypdf': 'pypdf',
            'PyMuPDF': 'fitz',
            'pikepdf': 'pikepdf',
            'pdfplumber': 'pdfplumber',
            'reportlab': 'reportlab',
            'fpdf2': 'fpdf',
            'weasyprint': 'weasyprint',
            'camelot': 'camelot',
            'tabula': 'tabula'
        },
        '📊 Excel': {
            'pandas': 'pandas',
            'openpyxl': 'openpyxl',
            'xlsxwriter': 'xlsxwriter',
            'xlrd': 'xlrd',
            'xlwt': 'xlwt',
            'xlwings': 'xlwings',
            'formulas': 'formulas',
            'pyexcel': 'pyexcel'
        },
        '📝 Word': {
            'python-docx': 'docx',
            'docxtpl': 'docxtpl',
            'mammoth': 'mammoth',
            'docx2txt': 'docx2txt',
            'docx-mailmerge': 'mailmerge'
        },
        '📈 Analyse': {
            'pandas': 'pandas',
            'numpy': 'numpy',
            'matplotlib': 'matplotlib',
            'seaborn': 'seaborn',
            'plotly': 'plotly',
            'scipy': 'scipy',
            'scikit-learn': 'sklearn',
            'polars': 'polars',
            'dask': 'dask'
        },
        '🗂️ Système': {
            'pathlib': 'pathlib',
            'watchdog': 'watchdog',
            'send2trash': 'send2trash',
            'filetype': 'filetype',
            'pillow': 'PIL'
        }
    }
    
    total_libs = 0
    installed_libs = 0
    failed_libs = []
    
    for category, libs in libraries.items():
        print(f"\n{category}")
        print("-" * 60)
        
        for display_name, import_name in libs.items():
            total_libs += 1
            try:
                module = __import__(import_name)
                version = getattr(module, '__version__', 'N/A')
                print(f"  ✅ {display_name:20} - version: {version}")
                installed_libs += 1
            except ImportError as e:
                print(f"  ❌ {display_name:20} - NON INSTALLÉ")
                failed_libs.append(display_name)
            except Exception as e:
                print(f"  ⚠️  {display_name:20} - Erreur: {str(e)[:40]}")
    
    # Résumé
    print("\n" + "=" * 60)
    print("📊 RÉSUMÉ")
    print("=" * 60)
    print(f"Total de librairies testées: {total_libs}")
    print(f"✅ Installées: {installed_libs}")
    print(f"❌ Manquantes: {len(failed_libs)}")
    
    if failed_libs:
        print(f"\n⚠️  Librairies manquantes:")
        for lib in failed_libs:
            print(f"   - {lib}")
        print(f"\n💡 Pour installer les librairies manquantes:")
        print(f"   conda activate pdf_excel_env")
        print(f"   pip install -r requirements.txt")
    else:
        print("\n✨ Toutes les librairies sont installées avec succès!")
    
    print(f"\n🐍 Python version: {sys.version}")
    print(f"📍 Exécutable: {sys.executable}")
    print("=" * 60)
    
    return len(failed_libs) == 0


def test_basic_operations():
    """Teste des opérations basiques avec chaque type de librairie"""
    print("\n\n" + "=" * 60)
    print("🧪 TESTS FONCTIONNELS BASIQUES")
    print("=" * 60)
    
    tests_passed = 0
    tests_total = 0
    
    # Test 1: Pandas
    tests_total += 1
    try:
        import pandas as pd
        df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
        assert len(df) == 3
        print("\n✅ Test Pandas: OK")
        tests_passed += 1
    except Exception as e:
        print(f"\n❌ Test Pandas: ÉCHEC - {e}")
    
    # Test 2: NumPy
    tests_total += 1
    try:
        import numpy as np
        arr = np.array([1, 2, 3])
        assert arr.sum() == 6
        print("✅ Test NumPy: OK")
        tests_passed += 1
    except Exception as e:
        print(f"❌ Test NumPy: ÉCHEC - {e}")
    
    # Test 3: openpyxl (création mémoire)
    tests_total += 1
    try:
        from openpyxl import Workbook
        wb = Workbook()
        ws = wb.active
        ws['A1'] = 'Test'
        print("✅ Test openpyxl: OK")
        tests_passed += 1
    except Exception as e:
        print(f"❌ Test openpyxl: ÉCHEC - {e}")
    
    # Test 4: python-docx (création mémoire)
    tests_total += 1
    try:
        from docx import Document
        doc = Document()
        doc.add_heading('Test', 0)
        print("✅ Test python-docx: OK")
        tests_passed += 1
    except Exception as e:
        print(f"❌ Test python-docx: ÉCHEC - {e}")
    
    # Test 5: pypdf (création mémoire)
    tests_total += 1
    try:
        from pypdf import PdfWriter
        writer = PdfWriter()
        print("✅ Test pypdf: OK")
        tests_passed += 1
    except Exception as e:
        print(f"❌ Test pypdf: ÉCHEC - {e}")
    
    print("\n" + "=" * 60)
    print(f"Tests réussis: {tests_passed}/{tests_total}")
    print("=" * 60)
    
    return tests_passed == tests_total


if __name__ == "__main__":
    print("\n🚀 Démarrage des tests...\n")
    
    # Test 1: Imports
    imports_ok = test_imports()
    
    # Test 2: Opérations basiques
    if imports_ok:
        operations_ok = test_basic_operations()
        
        if operations_ok:
            print("\n\n🎉 TOUS LES TESTS SONT PASSÉS AVEC SUCCÈS! 🎉\n")
            sys.exit(0)
        else:
            print("\n\n⚠️  Certains tests fonctionnels ont échoué\n")
            sys.exit(1)
    else:
        print("\n\n⚠️  Des librairies sont manquantes. Installez-les avant de continuer.\n")
        sys.exit(1)
