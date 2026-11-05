#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
═══════════════════════════════════════════════════════════════════════════════
    CAS 10 - ROUTEUR INTELLIGENT
    Détection automatique et routage des types d'étapes de mission
═══════════════════════════════════════════════════════════════════════════════

Description:
    Module de routage intelligent qui analyse les données JSON et détermine
    automatiquement vers quel cas (5, 6, 7, 8) router chaque élément.

Auteur: Expert Python & Automation
Date: 5 novembre 2026
Version: 1.0.0
"""

from typing import Dict, List, Optional, Tuple
import json

# ═══════════════════════════════════════════════════════════════════════════
# MAPPING ÉTAPES → CAS
# ═══════════════════════════════════════════════════════════════════════════

ETAPE_MAPPING = {
    # CAS 2 - Procédures d'audit
    2: [
        "Procédure",
        "Procédures",
        "Procédure d'audit",
        "Procédures d'audit",
        "Audit procedure",
    ],
    
    # CAS 3 - Manuels d'audit
    3: [
        "Manuel",
        "Manuels",
        "Manuel d'audit",
        "Manuels d'audit",
        "Manuel méthodologique",
        "Guide d'audit",
    ],
    
    # CAS 5 - FRAP et Recommandations
    5: [
        "Frap",
        "FRAP",
        "Feuille de Révélation et d'Analyse de Problème",
        "Recos contrôle des comptes",
        "Recos contrôle interne comptable",
        "Recommandations contrôle",
        "Plan de recommendation",
    ],
    
    # CAS 6 - Feuilles de révision
    6: [
        "Feuille revision",
        "Feuille révision",
        "Feuille de révision",
        "Révision des comptes",
        "Test de révision",
    ],
    
    # CAS 7 - Feuilles de couverture
    7: [
        "Feuille couverture",
        "Couverture",
        "Feuille de couverture",
        "Test de couverture",
    ],
    
    # CAS 8 - Modèles standard
    8: [
        "Programme de travail",
        "Cartographie des risques",
        "Modélisation",
        "Plan de recommendation de surveillance permanente",
        "Matrice de surveillance permanente",
        "Programme d'audit",
        "Matrice des risques",
    ],
}

# Créer un mapping inversé pour une recherche rapide
ETAPE_TO_CAS = {}
for cas_num, etapes in ETAPE_MAPPING.items():
    for etape in etapes:
        ETAPE_TO_CAS[etape.lower()] = cas_num

# ═══════════════════════════════════════════════════════════════════════════
# MOTS-CLÉS PAR CAS
# ═══════════════════════════════════════════════════════════════════════════

KEYWORDS_BY_CAS = {
    2: [
        "procédure", "étape méthodologique", "acteur audit", "traitement",
        "diligence", "document probant", "norme iia", "cripp"
    ],
    3: [
        "manuel", "méthodologie", "guide", "acteur audit",
        "norme iia", "cripp", "référentiel"
    ],
    5: [
        "frap", "problème", "constat", "cause", "conséquence",
        "recommandation", "plan d'action", "échéance", "responsable",
        "déficience", "anomalie", "non-conformité"
    ],
    6: [
        "révision", "test", "échantillon", "pointage", "vérification",
        "contrôle", "assertion", "validité", "exhaustivité",
        "exactitude", "réalité", "droits", "évaluation"
    ],
    7: [
        "couverture", "étendue", "nature", "calendrier", "budget",
        "ressources", "objectifs", "périmètre", "méthodologie"
    ],
    8: [
        "programme", "cartographie", "risque", "processus",
        "contrôle interne", "surveillance", "matrice", "criticité",
        "impact", "probabilité", "dispositif de maîtrise"
    ],
}

# ═══════════════════════════════════════════════════════════════════════════
# FONCTIONS DE DÉTECTION
# ═══════════════════════════════════════════════════════════════════════════

def detect_by_etape_field(data_item: Dict) -> Optional[int]:
    """
    Détecte le cas via le champ "Etape de mission" de table 1
    OU via le champ source du webhook N8N.
    
    Args:
        data_item: Élément de Data_integrale
        
    Returns:
        Numéro du cas ou None
    """
    # Méthode 1 : Chercher dans le champ source (DATA_COLLECTION)
    if "source" in data_item:
        source = str(data_item["source"]).upper()
        if "PROCEDURE" in source:
            return 2
        elif "MANUEL" in source:
            return 3
        elif "FRAP" in source or "RECO" in source:
            return 5
        elif "REVISION" in source or "FEUILLE_REVISION" in source:
            return 6
        elif "COUVERTURE" in source:
            return 7
        elif "PROGRAMME" in source or "CARTO" in source or "MATRICE" in source:
            return 8
    
    # Méthode 2 : Chercher table 1
    table1 = None
    for key in ["table 1", "table1", "Table 1", "Table1"]:
        if key in data_item:
            table1 = data_item[key]
            break
    
    if not table1 or not isinstance(table1, dict):
        return None
    
    # Extraire l'étape de mission
    etape = None
    for key in ["Etape de mission", "Étape de mission", "etape_de_mission"]:
        if key in table1:
            etape = table1[key]
            break
    
    if not etape:
        return None
    
    # Rechercher dans le mapping
    etape_lower = str(etape).lower()
    
    # Recherche exacte d'abord
    if etape_lower in ETAPE_TO_CAS:
        return ETAPE_TO_CAS[etape_lower]
    
    # Recherche partielle
    for key, cas_num in ETAPE_TO_CAS.items():
        if key in etape_lower or etape_lower in key:
            return cas_num
    
    return None

def detect_by_keywords(data_item: Dict) -> Optional[int]:
    """
    Détecte le cas via l'analyse des mots-clés dans le contenu.
    
    Args:
        data_item: Élément de Data_integrale
        
    Returns:
        Numéro du cas ou None
    """
    # Convertir en texte pour analyse
    data_str = json.dumps(data_item, ensure_ascii=False).lower()
    
    # Compter les occurrences de mots-clés par cas
    scores = {}
    for cas_num, keywords in KEYWORDS_BY_CAS.items():
        score = sum(1 for kw in keywords if kw in data_str)
        if score > 0:
            scores[cas_num] = score
    
    # Retourner le cas avec le score le plus élevé
    if scores:
        return max(scores, key=scores.get)
    
    return None

def detect_by_structure(data_item: Dict) -> Optional[int]:
    """
    Détecte le cas via l'analyse de la structure des données.
    
    Args:
        data_item: Élément de Data_integrale
        
    Returns:
        Numéro du cas ou None
    """
    # Cas 5: Contient des champs FRAP spécifiques
    if any(key in str(data_item).lower() for key in ["problème", "constat", "cause", "conséquence"]):
        return 5
    
    # Cas 6: Contient des colonnes de test de révision
    if any(key in str(data_item).lower() for key in ["assertion", "échantillon", "pointage"]):
        return 6
    
    # Cas 7: Contient des informations de couverture
    if any(key in str(data_item).lower() for key in ["couverture", "étendue", "périmètre"]):
        return 7
    
    # Cas 8: Contient des matrices ou cartographies
    if any(key in str(data_item).lower() for key in ["matrice", "cartographie", "criticité"]):
        return 8
    
    return None

def detect_cas(data_item: Dict) -> Tuple[Optional[int], str]:
    """
    Détecte le numéro de cas pour un élément de Data_integrale.
    Utilise plusieurs méthodes de détection en cascade.
    
    Args:
        data_item: Élément de Data_integrale
        
    Returns:
        Tuple (numéro_cas, méthode_utilisée)
    """
    # Méthode 1: Champ "Etape de mission"
    cas = detect_by_etape_field(data_item)
    if cas:
        return cas, "etape_field"
    
    # Méthode 2: Analyse des mots-clés
    cas = detect_by_keywords(data_item)
    if cas:
        return cas, "keywords"
    
    # Méthode 3: Structure des données
    cas = detect_by_structure(data_item)
    if cas:
        return cas, "structure"
    
    return None, "not_detected"

def group_by_cas(data_integrale: List[Dict]) -> Dict[int, List[Dict]]:
    """
    Groupe les éléments de Data_integrale par numéro de cas.
    
    Args:
        data_integrale: Liste des éléments
        
    Returns:
        Dict avec numéro de cas comme clé et liste d'éléments comme valeur
    """
    grouped = {}
    undetected = []
    
    for idx, item in enumerate(data_integrale):
        cas_num, method = detect_cas(item)
        
        if cas_num:
            if cas_num not in grouped:
                grouped[cas_num] = []
            grouped[cas_num].append({
                "index": idx,
                "data": item,
                "detection_method": method
            })
        else:
            undetected.append({
                "index": idx,
                "data": item
            })
    
    # Ajouter les non-détectés si présents
    if undetected:
        grouped[0] = undetected
    
    return grouped

def get_cas_info(cas_num: int) -> Dict[str, str]:
    """
    Retourne les informations sur un cas donné.
    
    Args:
        cas_num: Numéro du cas
        
    Returns:
        Dict avec les informations
    """
    info = {
        5: {
            "name": "FRAP et Recommandations",
            "description": "Feuilles de Révélation et d'Analyse de Problème",
            "script": "json2word_frap_recos.py",
            "columns": ["Problème", "Constat", "Cause", "Conséquence", "Recommandation"]
        },
        6: {
            "name": "Feuilles de Révision",
            "description": "Tests de révision des comptes",
            "script": "json2word_feuilles_revision.py",
            "columns": ["Test", "Objectif", "Nature", "Procédure", "Échantillon", "Résultat", "Écart", "Conclusion", "Action"]
        },
        7: {
            "name": "Feuilles de Couverture",
            "description": "Feuilles de couverture des tests",
            "script": "json2word_feuille_couverture.py",
            "columns": ["Processus", "Contrôle", "Modèle de test", "Résultats"]
        },
        8: {
            "name": "Modèles Standard",
            "description": "Programme de travail, Cartographie, Matrices",
            "script": "json2word_modele_standard.py",
            "columns": ["Variable selon le modèle"]
        },
    }
    
    return info.get(cas_num, {
        "name": "Non détecté",
        "description": "Type d'étape non identifié",
        "script": None,
        "columns": []
    })

# ═══════════════════════════════════════════════════════════════════════════
# TESTS UNITAIRES
# ═══════════════════════════════════════════════════════════════════════════

def test_router():
    """Tests de base du routeur"""
    print("═" * 80)
    print("TESTS DU ROUTEUR CAS 10")
    print("═" * 80)
    
    # Test 1: Détection Cas 5
    test_cas5 = {
        "table 1": {
            "Etape de mission": "FRAP"
        }
    }
    cas, method = detect_cas(test_cas5)
    print(f"\nTest 1 - Cas 5 (FRAP): {cas} via {method}")
    assert cas == 5, f"Attendu: 5, Obtenu: {cas}"
    
    # Test 2: Détection Cas 6
    test_cas6 = {
        "table 1": {
            "Etape de mission": "Feuille de révision"
        }
    }
    cas, method = detect_cas(test_cas6)
    print(f"Test 2 - Cas 6 (Révision): {cas} via {method}")
    assert cas == 6, f"Attendu: 6, Obtenu: {cas}"
    
    # Test 3: Détection Cas 7
    test_cas7 = {
        "table 1": {
            "Etape de mission": "Feuille couverture"
        }
    }
    cas, method = detect_cas(test_cas7)
    print(f"Test 3 - Cas 7 (Couverture): {cas} via {method}")
    assert cas == 7, f"Attendu: 7, Obtenu: {cas}"
    
    # Test 4: Détection Cas 8
    test_cas8 = {
        "table 1": {
            "Etape de mission": "Cartographie des risques"
        }
    }
    cas, method = detect_cas(test_cas8)
    print(f"Test 4 - Cas 8 (Cartographie): {cas} via {method}")
    assert cas == 8, f"Attendu: 8, Obtenu: {cas}"
    
    # Test 5: Groupement
    data_test = [test_cas5, test_cas6, test_cas7, test_cas8]
    grouped = group_by_cas(data_test)
    print(f"\nTest 5 - Groupement: {len(grouped)} cas détectés")
    print(f"  Cas 5: {len(grouped.get(5, []))} éléments")
    print(f"  Cas 6: {len(grouped.get(6, []))} éléments")
    print(f"  Cas 7: {len(grouped.get(7, []))} éléments")
    print(f"  Cas 8: {len(grouped.get(8, []))} éléments")
    
    print("\n✅ Tous les tests passés!")

if __name__ == "__main__":
    test_router()


# ═══════════════════════════════════════════════════════════════════════════
# CLASSE ROUTEUR (pour compatibilité avec l'orchestrateur)
# ═══════════════════════════════════════════════════════════════════════════

class Cas10Router:
    """
    Classe wrapper pour le routeur intelligent Cas 10
    Permet une utilisation orientée objet dans l'orchestrateur
    """
    
    def __init__(self):
        """Initialise le routeur"""
        self.etape_mapping = ETAPE_MAPPING
        self.etape_to_cas = ETAPE_TO_CAS
        self.keywords = KEYWORDS_BY_CAS
    
    def detect_cas(self, data_item: Dict) -> Optional[int]:
        """
        Détecte le numéro de cas pour un élément
        
        Args:
            data_item: Élément de Data_integrale
            
        Returns:
            Numéro du cas (2-8) ou None
        """
        # Utiliser la fonction globale
        cas, method = detect_cas(data_item)
        return cas
    
    def detect_with_method(self, data_item: Dict) -> Tuple[Optional[int], str]:
        """
        Détecte le cas avec la méthode utilisée
        
        Args:
            data_item: Élément de Data_integrale
            
        Returns:
            Tuple (numéro_cas, méthode)
        """
        return detect_cas(data_item)
    
    def group_by_cas(self, data_integrale: List[Dict]) -> Dict[int, List[Dict]]:
        """
        Groupe les éléments par cas
        
        Args:
            data_integrale: Liste des éléments
            
        Returns:
            Dict {cas_number: [list of items]}
        """
        return group_by_cas(data_integrale)
    
    def get_cas_info(self, cas_num: int) -> Dict[str, str]:
        """
        Obtient les informations sur un cas
        
        Args:
            cas_num: Numéro du cas
            
        Returns:
            Dict avec les informations
        """
        return get_cas_info(cas_num)
