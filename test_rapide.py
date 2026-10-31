"""
Test rapide des packages déjà installés
"""

print("=" * 60)
print("🧪 TEST RAPIDE DE L'ENVIRONNEMENT")
print("=" * 60)
print()

def test_import(nom_package, nom_import):
    """Teste l'import d'un package"""
    try:
        __import__(nom_import)
        print(f"✅ {nom_package:30} - OK")
        return True
    except ImportError:
        print(f"❌ {nom_package:30} - NON INSTALLÉ")
        return False
    except Exception as e:
        print(f"⚠️  {nom_package:30} - ERREUR: {str(e)[:30]}")
        return False

# Test des packages critiques
packages = {
    '📄 PDF': [
        ('pypdf', 'pypdf'),
        ('pikepdf', 'pikepdf'),
        ('reportlab', 'reportlab'),
        ('fpdf2', 'fpdf'),
    ],
    '📊 Excel': [
        ('pandas', 'pandas'),
        ('openpyxl', 'openpyxl'),
        ('xlsxwriter', 'xlsxwriter'),
        ('xlrd', 'xlrd'),
    ],
    '📝 Word': [
        ('python-docx', 'docx'),
    ],
    '📈 Visualisation': [
        ('matplotlib', 'matplotlib'),
        ('numpy', 'numpy'),
    ],
    '🛠️ Utilitaires': [
        ('pillow', 'PIL'),
        ('lxml', 'lxml'),
    ]
}

total = 0
installe = 0

for categorie, liste in packages.items():
    print(f"\n{categorie}")
    print("-" * 60)
    for nom, import_name in liste:
        total += 1
        if test_import(nom, import_name):
            installe += 1

print("\n" + "=" * 60)
print(f"📊 RÉSULTAT: {installe}/{total} packages fonctionnels")
print("=" * 60)

if installe == total:
    print("\n✨ PARFAIT! Tous les packages critiques fonctionnent!")
elif installe >= total * 0.7:
    print(f"\n👍 BON! {installe} packages sur {total} fonctionnent.")
    print("Vous pouvez déjà commencer à travailler!")
else:
    print(f"\n⚠️  Seulement {installe}/{total} packages fonctionnent.")
    print("Installez les packages manquants avec:")
    print("pip install -r requirements_minimal.txt")

print()
