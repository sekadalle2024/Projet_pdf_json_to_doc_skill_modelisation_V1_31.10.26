#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test simple de Cas 10 - Vérification architecture
"""

import sys
from pathlib import Path

# Ajouter le chemin du module
sys.path.insert(0, str(Path(__file__).parent))

print("=" * 80)
print("TEST CAS 10 - ARCHITECTURE")
print("=" * 80)

# Test 1 : Import des modules
print("\n1. Test des imports...")
try:
    from cas10_router import Cas10Router
    print("   ✅ cas10_router importé")
except Exception as e:
    print(f"   ❌ Erreur: {e}")
    sys.exit(1)

# Test 2 : Configuration
print("\n2. Test de la configuration...")
BASE_DIR = Path(__file__).parent.parent
print(f"   BASE_DIR: {BASE_DIR}")

CAS_SCRIPTS = {
    2: BASE_DIR / "Cas_2" / "json2word_audit.py",
    3: BASE_DIR / "Cas_3" / "json2word_audit.py",
    5: BASE_DIR / "Cas_5" / "json2word_frap_recos.py",
    6: BASE_DIR / "Cas_6" / "json2word_feuilles_revision.py",
    7: BASE_DIR / "Cas_7" / "json2word_feuille_couverture.py",
    8: BASE_DIR / "Cas_8" / "json2word_programme_travail.py",
}

CAS_OUTPUT_DIRS = {
    2: BASE_DIR / "Cas_2" / "sortie_word_cas2",
    3: BASE_DIR / "Cas_3" / "sortie_word_cas3",
    5: BASE_DIR / "Cas_5" / "sortie_word_cas5",
    6: BASE_DIR / "Cas_6" / "sortie_word_cas6",
    7: BASE_DIR / "Cas_7" / "sortie_word_cas7",
    8: BASE_DIR / "Cas_8" / "sortie_word_cas8",
}

# Vérifier les fichiers
print("\n3. Vérification des scripts...")
for cas, script_path in CAS_SCRIPTS.items():
    exists = "✅" if script_path.exists() else "❌"
    print(f"   Cas {cas}: {exists} {script_path.name}")

# Test 3 : Routeur
print("\n4. Test du routeur...")
router = Cas10Router()

test_data = {
    "source": "Etape_mission_PROGRAMME_E-audit",
    "table 1": {"Etape de mission": "Programme de travail"}
}

cas_detected = router.detect_cas(test_data)
print(f"   Données test: {test_data.get('source', 'N/A')}")
print(f"   Cas détecté: {cas_detected}")

if cas_detected == 8:
    print("   ✅ Détection correcte (Cas 8)")
else:
    print(f"   ❌ Erreur: attendu Cas 8, obtenu {cas_detected}")

print("\n" + "=" * 80)
print("✅ TESTS TERMINÉS")
print("=" * 80)
