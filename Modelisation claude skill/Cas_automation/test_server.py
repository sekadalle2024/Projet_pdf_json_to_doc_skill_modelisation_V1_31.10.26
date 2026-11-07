"""
Script de test du serveur d'automation.
Teste tous les endpoints et vérifie la génération des documents.
"""

import requests
import json
from pathlib import Path
import time

BASE_URL = "http://localhost:5000"
OUTPUT_TEST_DIR = Path(__file__).parent / "test_output"
OUTPUT_TEST_DIR.mkdir(exist_ok=True)

def test_health():
    """Test l'endpoint /health"""
    print("=" * 70)
    print("TEST 1: Health Check")
    print("=" * 70)
    
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✓ Serveur actif")
            print(f"  Environment: {data.get('environment')}")
            print(f"  Skills chargés:")
            for cas, loaded in data.get('skills_loaded', {}).items():
                status = "✓" if loaded else "✗"
                print(f"    {status} {cas}")
            return True
        else:
            print("✗ Erreur serveur")
            return False
            
    except requests.exceptions.ConnectionError:
        print("✗ Impossible de se connecter au serveur")
        print("  Assurez-vous que le serveur est démarré (start_server.bat)")
        return False
    except Exception as e:
        print(f"✗ Erreur: {e}")
        return False


def test_cas(cas_number):
    """Test un endpoint d'automation"""
    print("\n" + "=" * 70)
    print(f"TEST {cas_number + 1}: Génération Cas {cas_number}")
    print("=" * 70)
    
    try:
        # Charger le JSON standard
        json_file = Path(__file__).parent / "json standard" / f"Json_standard_[Cas {cas_number}].txt"
        
        if not json_file.exists():
            print(f"✗ Fichier JSON non trouvé: {json_file}")
            return False
        
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"✓ JSON chargé ({len(json.dumps(data))} caractères)")
        
        # Appel API
        print(f"  Envoi requête POST /automation/cas_{cas_number}...")
        start_time = time.time()
        
        response = requests.post(
            f"{BASE_URL}/automation/cas_{cas_number}",
            json=data,
            headers={"Content-Type": "application/json"}
        )
        
        duration = time.time() - start_time
        
        if response.status_code == 200:
            # Sauvegarder le fichier
            output_file = OUTPUT_TEST_DIR / f"test_cas_{cas_number}_{int(time.time())}.docx"
            with open(output_file, 'wb') as f:
                f.write(response.content)
            
            file_size = output_file.stat().st_size
            print(f"✓ Document généré en {duration:.2f}s")
            print(f"  Fichier: {output_file.name}")
            print(f"  Taille: {file_size:,} octets ({file_size/1024:.1f} KB)")
            return True
        else:
            print(f"✗ Erreur {response.status_code}")
            try:
                error = response.json()
                print(f"  Message: {error.get('error')}")
            except:
                print(f"  Réponse: {response.text[:200]}")
            return False
            
    except Exception as e:
        print(f"✗ Erreur: {e}")
        return False


def test_endpoint_test(cas_number):
    """Test l'endpoint /automation/test/<cas>"""
    print("\n" + "=" * 70)
    print(f"TEST: Endpoint test/cas_{cas_number}")
    print("=" * 70)
    
    try:
        print(f"  Envoi requête GET /automation/test/{cas_number}...")
        start_time = time.time()
        
        response = requests.get(f"{BASE_URL}/automation/test/{cas_number}")
        duration = time.time() - start_time
        
        if response.status_code == 200:
            output_file = OUTPUT_TEST_DIR / f"test_endpoint_{cas_number}_{int(time.time())}.docx"
            with open(output_file, 'wb') as f:
                f.write(response.content)
            
            file_size = output_file.stat().st_size
            print(f"✓ Document généré en {duration:.2f}s")
            print(f"  Fichier: {output_file.name}")
            print(f"  Taille: {file_size:,} octets")
            return True
        else:
            print(f"✗ Erreur {response.status_code}")
            return False
            
    except Exception as e:
        print(f"✗ Erreur: {e}")
        return False


def test_invalid_json():
    """Test avec un JSON invalide"""
    print("\n" + "=" * 70)
    print("TEST: JSON Invalide (doit échouer)")
    print("=" * 70)
    
    try:
        invalid_data = {"invalid": "structure"}
        response = requests.post(
            f"{BASE_URL}/automation/cas_6",
            json=invalid_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 400:
            error = response.json()
            print(f"✓ Erreur correctement détectée")
            print(f"  Message: {error.get('error')}")
            return True
        else:
            print(f"✗ Devrait retourner 400, a retourné {response.status_code}")
            return False
            
    except Exception as e:
        print(f"✗ Erreur: {e}")
        return False


def main():
    """Exécute tous les tests"""
    print("\n" + "=" * 70)
    print("SUITE DE TESTS - SERVEUR AUTOMATION")
    print("=" * 70)
    print(f"URL: {BASE_URL}")
    print(f"Output: {OUTPUT_TEST_DIR}")
    print()
    
    results = {}
    
    # Test 1: Health check
    results['health'] = test_health()
    
    if not results['health']:
        print("\n" + "=" * 70)
        print("ABANDON: Serveur non accessible")
        print("=" * 70)
        return
    
    # Test 2-4: Génération des 3 cas
    for cas in [6, 7, 8]:
        results[f'cas_{cas}'] = test_cas(cas)
        time.sleep(0.5)  # Pause entre les tests
    
    # Test 5-7: Endpoints test
    for cas in [6, 7, 8]:
        results[f'test_endpoint_{cas}'] = test_endpoint_test(cas)
        time.sleep(0.5)
    
    # Test 8: JSON invalide
    results['invalid_json'] = test_invalid_json()
    
    # Résumé
    print("\n" + "=" * 70)
    print("RÉSUMÉ DES TESTS")
    print("=" * 70)
    
    total = len(results)
    passed = sum(1 for r in results.values() if r)
    
    for test_name, result in results.items():
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {test_name}")
    
    print()
    print(f"Score: {passed}/{total} tests réussis ({passed*100//total}%)")
    
    if passed == total:
        print("\n🎉 Tous les tests sont réussis !")
    else:
        print(f"\n⚠️  {total - passed} test(s) échoué(s)")
    
    print("\n" + "=" * 70)
    print(f"Documents générés dans: {OUTPUT_TEST_DIR}")
    print("=" * 70)


if __name__ == '__main__':
    main()
