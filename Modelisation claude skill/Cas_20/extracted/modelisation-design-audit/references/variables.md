# Variables d'entrée (user_message)


| Variable | Rôle | Valeur par défaut |
|---|---|---|
| `[Command]` | Étape de mission visée (`/cartographie des risques`, `/programme de travail`, `/feuille couverture`, `/Frap`, `/modélisation`...) | obligatoire |
| `[Processus]` | Processus audité | obligatoire |
| `[Modélisation design]` | Liste des designs à activer, ou `[Mode auto]` | absente : ne rien regrouper (mais proposer 1 design si `[Mode auto]`) |
| `[Cycle par sous processus]`, `[Evaluation des risques par criticité]`, `[Plan d'action]`, ... | Définition d'un design : nombre de `[Niveau]` et contenu de chaque niveau | voir annexe A |
| `[Modele]` | Colonnes de base (rubriques d'audit) | colonnes standard de l'étape |
| `[Nb de lignes]` | Nombre de lignes de données | selon l'étape ; `[Mode auto]` = libre |
| `[Nb de colonnes]`, `[Max]`/`[Min]` de `[Nb de colonnes]` | Bornes de colonnes | libre |
| `Nb de [Modélisation design]` | Nombre de designs par étape ou document | selon `[Mode auto]` |
| `Nb de colonne de [Modélisation design]` | Total de colonnes à intégrer via les designs | libre |
| `[Max]`/`[Min]` de `[Modélisation design]` | Bornes du nombre de designs | libre |
| `Conception de [Modélisation design]` | `[Mode auto]` = liberté de concevoir les designs | non auto : suivre uniquement les designs définis |
| `[Demo]` | `Activate` : remplir toutes les cellules avec des données de démonstration réalistes | inactif |
| `[Contenu]` | `Activate` : produire le JSON de l'étape (voir [Formatage data]) | inactif |
| `[Format sortie]` | `docx` / `json` / `pdf` / `xlsx` (ou liste) | **docx** |
| `[Template source]` | Chemin d'un modèle `.docx` / `.dotx` / `.xlsx` à reproduire (styles, largeurs, en-têtes) | modèle Word par défaut (section 6.1) |
| `[Json source]` | Chemin ou contenu d'un JSON déjà élaboré à convertir | aucun |
| `[Nom logiciel]` | Nom du logiciel pour l'en-tête de page et le nom de fichier | `Logiciel automatisé E-audit pro 2.0` |
| `[Valeur alphanumerique]` | Référence du fichier (1 ou 2 lettres + 2 ou 3 chiffres, ex. BB040) | générée automatiquement si vide |
| `[Directive]` | Instruction libre à respecter | aucune |
| `[Correlation [Colonne X]]` | La colonne X doit avoir le même contenu dans plusieurs étapes/documents | aucune |
| `[Source]` | Élément (par ex. une cartographie) dont il faut reprendre les paramètres | aucune |

Règle de lecture : une variable absente prend sa valeur par défaut ; une variable `= [Mode auto]` signifie liberté de choix du LLM (section 5).
