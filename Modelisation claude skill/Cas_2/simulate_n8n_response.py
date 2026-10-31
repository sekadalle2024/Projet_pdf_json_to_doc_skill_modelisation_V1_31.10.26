#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script : simulate_n8n_response.py
Description : Simule la réponse du webhook N8N pour tester le workflow
Auteur : Expert Python & Automation
Date : 31 octobre 2026
"""

import json
from pathlib import Path

# Simuler une réponse du webhook N8N avec 2 procédures de test
simulated_response = [
    {
        "Data_integrale": [
            {
                "Etape mission - Manuel des procedures": [
                    {
                        "table 1": {
                            "Etape de mission": "Test Manuel audit interne",
                            "Document": "Manuel de test - Procédure 1",
                            "Processus": "Test de simulation API",
                            "Cycle d'activité": "Cycle de test",
                            "Secteur d'activité": "Banque Test",
                            "Norme": {
                                "Norme 1": "Norme 1.1 Test",
                                "Norme 2": "Norme 1.2 Test"
                            },
                            "Reference": "TEST-001",
                            "Version": "V1.0 Test",
                            "Etablissement": "Banque de Test",
                            "Approbation": "Direction Test"
                        }
                    },
                    {
                        "table 2": [
                            {
                                "Étape méthodologique": "Étape de test 1",
                                "Acteur audit": "Auditeur Test",
                                "Traitement et diligences d'audit": "Test des diligences d'audit",
                                "Document probant": "Document de test",
                                "Norme IIA / CRIPP": "Norme de test",
                                "Extrait de la norme": "Extrait de test"
                            }
                        ]
                    }
                ]
            },
            {
                "Etape mission - Manuel des procedures": [
                    {
                        "table 1": {
                            "Etape de mission": "Test Phase de préparation",
                            "Document": "Manuel de test - Procédure 2",
                            "Processus": "Test de simulation API",
                            "Cycle d'activité": "Cycle de test",
                            "Secteur d'activité": "Banque Test",
                            "Norme": {
                                "Norme 1": "Norme 2.1 Test"
                            },
                            "Reference": "TEST-002",
                            "Version": "V1.0 Test",
                            "Etablissement": "Banque de Test",
                            "Approbation": "Direction Test"
                        }
                    },
                    {
                        "table 2": [
                            {
                                "Étape méthodologique": "Étape de test 2",
                                "Acteur audit": "Auditeur Test",
                                "Traitement et diligences d'audit": "Test des diligences d'audit",
                                "Document probant": "Document de test",
                                "Norme IIA / CRIPP": "Norme de test",
                                "Extrait de la norme": "Extrait de test"
                            }
                        ]
                    }
                ]
            }
        ]
    }
]

def main():
    """Crée un fichier JSON de simulation"""
    output_dir = Path("./data_json_from_n8n")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    filepath = output_dir / "data_integrale_simulation.json"
    
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(simulated_response, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Fichier de simulation créé : {filepath}")
    print(f"📊 Nombre de procédures : {len(simulated_response[0]['Data_integrale'])}")
    
    return str(filepath)

if __name__ == "__main__":
    main()
