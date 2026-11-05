# [Modélisation design] - contenu intégral du prompt source (verbatim)

Fait foi en cas de doute. Orthographe d'origine conservée.

```text
- [Modélisation design]
    - Description
        - [Modélisation design] correspond a la modelisation d’un groupe de colonnes qui partage des designation ou attribut qiu converge
        - elle peut etre definir de maniere litteraire ou par la modelisation des colonnes dans sa definition
        - Elle consiste a ajouter des entete horizontale Aux entete de base. Certaines colonnes de [Étape de mission] peuvent être regrouper selon une dénomination. Le dénomination susceptible d être appliquer peuvent être ajouter au dessus des colonnes concernées et juxtaposée l”une après l autre
        - Si les colonnes de base existent dans [Modele] alors juste ajoute les colonnes lies aux niveau
        - Si les colonnes de base n existent pas dans [Modélisation design], alors tu dois ajouter les colonnes de base qui manquent, les remplir selon le contexte du document, ensuite mettre en oeuvre [Modélisation design
    - Objectif
        - Permet de designer et de rendre plus pro les colonnes de l étape de mission en ajoutant des entetes horizontale Aux entetes de base
    - [Rubrique audit]
        - Description
            - [Modele]  et [Modélisation design] sont constituees de [Rubrique audit]
            - Les [Rubrique audit] sont les rubrique elabore ou collecte ou diffuse durant les activités d’audit, risque et controle ou qui integre les colonnes des activites ( mission d’audit interne, plan d’audit, cartographie des risques, surevillance permanente, suivi des recos et ) , phase de mission ou etape de mission
            - exemple de Rubrique audit] : cycle, processus, sous processus, tache, tache cle, controle cle, controle , niveau 1, controle niveau 2n causes, consequences, probabilité, impact, criticite, operationnel, plan d’action, delais, document, preuve, dispositif de maiytise des risques, operation, docmaines, transactions, donnees  etc
    - Designation
        - Designation = [Rubrique audit] de niveau 1 +  [Rubrique audit] de niveau 2/3/4
        - Exemple
            - [Cycle par sous processus]
                - [Cycle par sous processus] = 3 [Niveau ]
                    - [Niveau 1] = Cycle
                    - [Niveau 2] = Processus
                    - [Niveau 3] = taches, opérationnel, document
    - variable complementaire de [Modélisation design]
        - Nb de [Modélisation design] =  le nombre de  [Modélisation design] a integrer dans [User_message] par  [Etape de mission] ou [Document]
        - Nb de colonne de [Modélisation design] =  le nombre de  colonne total à integrer dans [Modélisation design] et a integrer dans [User_message] par  [Etape de mission] ou [Document]
        - [Max] de [Modélisation design] = le nombre maximal de  [Modélisation design] a integrer dans [User_message] par  [Etape de mission] ou [Document]
        - [Min] de  [Modélisation design] = le nombre mainimal de  [Modélisation design] a integrer dans [User_message] par  [Etape de mission] ou [Document]
        - [Modélisation design] = [Mode auto] te donne le choix de modeliser  et integrer les  [Modélisation design] de ton choix par  [Etape de mission] ou [Document]
        - Conception de [Modélisation design] = [Mode auto] cette variable te donne l autorisation de designer tes [Modélisation design]  selon le contexte, sans suivre uniquement Exemples de [Modélisation design]
        Nombre de [Modélisation design]
    - Instruction
        - Lorsqu’une [Modélisation design] est ajoute dans une [User_message], alors les colonnes et entetes de colonnes definies doivent apparaitre dans le design de  [Etape de mission] ou [Document], en plus des colonnes definies dans [Modele]
        - [Modele]  et [Modélisation design] sont complementaires, tout en evitant les doublons
        - si [Modélisation design] est definies pour  une [Etape de mission] ou [Document], alors la variable est egament integre dans la [User_message], afin que l agent charger d elaborer ne [Etape de mission] ou [Document] puissent en tenir compte dans la modelisation en document word ou excel du document
    - Exemples de [Modélisation design]
        - [Cycle par opérations]
            - [Cycle par opérations] = 2 [Niveau ]
                - [Niveau 1] = Cycle
                - [Niveau 2] = opérations financière, opérations administrative,  opérations operationnelles
                    - [Niveau 2] = taches, opérationnel, document
        - [Evaluation des risques par criticité]
            - [Evaluation des risques par criticité] = 2 [Niveau ]
                - [Niveau 1] = Evaluation des risques
                - [Niveau 2] = probabilite, impact, criticite
                    - [Niveau 2] = taches, opérationnel, document
        - [Plan d’action]
            - [Plan d’action]= 2 [Niveau ]
                - [Niveau 1] = Plan d’action
                - [Niveau 2] = Niveau 1, niveau 2, Niveau 3
                    - [Niveau 2] = taches, opérationnel, document
                - [Niveau 2] = point de contrôle, contrôle a realiser, document
        - [Dispositif de controle interne par echellon]
            -
            | **DISPOSITIF DE CONTRÔLE INTERNE** |  |
            | --- | --- |
            | **1er échelon**
            **Auto-contrôle / contrôle hiérarchique** | **2e échelon**
            **Contrôle permanent / audit interne** |
            -
        - [Risque inherent par impact]
            -
            |  | **RISQUE INHÉRENT** |  |
            | --- | --- | --- |
            | Prob | impact | Amplitude |
    - Exemples de [User_message]
        - "[Command] = /cartographie des risques"
        - [Processus] = Gestion des comptes inactifs et dépôts sous mandat de justice",
        - [Modélisation design] = [Cycle par sous processus], [Evaluation des risques par criticité]
        - [Cycle par sous processus]= 3 [Niveau]
            - [Niveau 1] = Cycle
            - [Niveau 2] = Processus
            - Niveau 3] = taches, opérationnel, document
        - [Evaluation des risques par criticité]
            - [Niveau 1] = Evaluation des risques
            - [Niveau 2] =  Probabilite, impact, criticite
        - [Modele] = no, Sous-processus, Tâche clé, Risque identifié, Cause racine, Impact, Probabilité, Criticité brute, Dispositif de maîtrise des risques, Criticité nette",
        - [Nb de lignes] = 20
        - [Demo] = Activate"
```
