# Cas 7 - Feuilles de Couverture (API N8N)

## Description
Génération de feuilles de couverture d'audit avec schéma de calcul.

## Skill à Développer
- **Skill Natif** : À générer depuis Claude Opus
- **Skill Standard** : `audit-etap_mission_feuille_couverture.skill`

## Étape de Mission
- **Feuille couverture** : Feuilles de couverture avec schéma de calcul

## Workflow N8N
- **Webhook URL** : À définir
- **Méthode** : POST/GET
- **Champ de sortie** : `Data_integrale`

## Caractéristiques Spéciales
- ⏳ **Mode** : API N8N (à configurer)
- ⏳ **Schéma de calcul** : Insertion entre table 5 et table 4
- ⏳ **Format** : (A), (B), (C) = (A) - (D)
- ⏳ **Largeurs colonnes** : Ajustement automatique
- ⏳ **Horodatage** : Format standard V1

## Contraintes Spécifiques
- Insertion automatique du schéma de calcul
- Retrait de la mention "Schéma de calcul : C = A + B ; Écart = C − D"
- Cellules avec formules sur une seule ligne
- Synchronisation largeurs colonnes tables liées

## Statut
⏳ **À DÉVELOPPER** - Skill natif Claude Opus à générer
