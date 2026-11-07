#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de vérification des imports pour le serveur d'automation.
Teste si tous les modules nécessaires peuvent être importés.
"""

import sys
from pathlib import Path

print("=" * 70)
print("🔍 Vérification des imports pour le serveur d'automation")
print("=" * 70)

# Ajouter les chemins
BASE_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(BASE_DIR / "Cas_6"))
sys.path.insert(0, str(BASE_DIR / "Cas_7"))
sys.path.insert(0, str(BASE_DIR / "Cas_8"))

print(f"\n📁 Chemins ajoutés au PYTHONPATH:")
print(f"   - {BASE_DIR / 'Cas_6'}")
print(f"   - {BASE_DIR / 'Cas_7'}")
print(f"   - {BASE_DIR / 'Cas_8'}")

# Tester Cas 6
print("\n" + "=" * 70)
print("📦 Test Cas 6 : json2word_feuilles_revision")
print("=" * 70)
try:
    from json2word_feuilles_revision import main as generate_cas_6
    print("✅ Import réussi")
    print(f"   Fonction: {generate_cas_6}")
    print(f"   Module: {generate_cas_6.__module__}")
    CAS_6_OK = True
except ImportError as e:
    print(f"❌ Échec: {e}")
    CAS_6_OK = False

# Tester Cas 7
print("\n" + "=" * 70)
print("📦 Test Cas 7 : json2word_feuille_couverture")
print("=" * 70)
try:
    from json2word_feuille_couverture import main as generate_cas_7
    print("✅ Import réussi")
    print(f"   Fonction: {generate_cas_7}")
    print(f"   Module: {generate_cas_7.__module__}")
    CAS_7_OK = True
except ImportError as e:
    print(f"❌ Échec: {e}")
    CAS_7_OK = False

# Tester Cas 8
print("\n" + "=" * 70)
print("📦 Test Cas 8 : json2word_programme_travail")
print("=" * 70)
try:
    from json2word_programme_travail import main as generate_cas_8
    print("✅ Import réussi")
    print(f"   Fonction: {generate_cas_8}")
    print(f"   Module: {generate_cas_8.__module__}")
    CAS_8_OK = True
except ImportError as e:
    print(f"❌ Échec: {e}")
    CAS_8_OK = False

# Résumé
print("\n" + "=" * 70)
print("📊 RÉSUMÉ")
print("=" * 70)
print(f"Cas 6 (Feuille de révision)  : {'✅ OK' if CAS_6_OK else '❌ ÉCHEC'}")
print(f"Cas 7 (Feuille de couverture): {'✅ OK' if CAS_7_OK else '❌ ÉCHEC'}")
print(f"Cas 8 (Programme de travail) : {'✅ OK' if CAS_8_OK else '❌ ÉCHEC'}")

total = sum([CAS_6_OK, CAS_7_OK, CAS_8_OK])
print(f"\nTotal : {total}/3 modules disponibles")

if total == 3:
    print("\n🎉 Tous les modules sont disponibles !")
    print("   Le serveur peut démarrer sans problème.")
    sys.exit(0)
else:
    print("\n⚠️ Certains modules sont indisponibles.")
    print("   Le serveur démarrera mais certains endpoints seront désactivés.")
    print("\n💡 Pour corriger :")
    if not CAS_6_OK:
        print("   - Vérifiez que Cas_6/json2word_feuilles_revision.py existe")
    if not CAS_7_OK:
        print("   - Vérifiez que Cas_7/json2word_feuille_couverture.py existe")
    if not CAS_8_OK:
        print("   - Vérifiez que Cas_8/json2word_programme_travail.py existe")
        print("   - Vérifiez que Cas_2/json2word_audit.py existe (dépendance de Cas 8)")
    sys.exit(1)
