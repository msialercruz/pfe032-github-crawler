# pfe032-github-crawler

## Script download.py

### Description

Ce script permet de trouver et de télécharger des fichiers Jupyter Notebook depuis Github. Cela nous permet de tester notre outil d'analyse avec des données réelles.

Ce script se déroule en plusieurs étapes. Voici chaque étape détaillé en ordre chronologique:

1. On va tout d'abord trouver tous les répertoires Github dont le langage principal est "Jupyter Notebook". Pour les obtenir, nous utilisons le lien de recherche Github https://github.com/search avec les paramètres suivants : `created:>2023-05-01 created:<2023-05-31 language: "Jupyter Notebook" license:mit machine learning`. Nous indiquons que nous voulons des répertoires datant du mois de mai 2023, avec une licence MIT et contenant "machine" et "learning" dans leur nom ou leur description.
2. Après avoir récupéré chaque répertoire, nous allons obtenir la liste des fichiers ipynb (Jupyter Notebook) en utilisant les paramètres suivants : `repo :... path:*.ipynb fit`. On remplace ce qui suit "repo:" par le nom du propriétaire suivi d'un / suivi du nom du répertoire (par exemple Azure/MachineLearningNotebooks). Nous indiquons également que nous voulons des fichiers ipynb qui contiennent le terme `fit`, qui correspond à la fonction utilisée pour entraîner des modèles.
3. Ensuite, une fois que nous avons tous les liens vers les fichiers ipynb dans chaque répertoire, nous les téléchargeons. Les fichiers ne contenant aucune cellule de type "code", n'étant pas au format JSON ou utilisant la librairie Tensorflow, qui n'est pas actuellement supportée par notre outil d'analyse, ne sont pas sauvegardés. Les autres fichiers sont considérés valides et sont séparés par taille. On génère également un fichier JSON qui fait la correspondance entre chaque fichier téléchargé et son URL source.

### Exécution

1. Créer le fichier ``cookies.txt`` et ajouter le contenu d'un cookie Github (requiert d'être connecter avec un compte)
2. Installer les dépendances `pip -r requirements.txt`
3. Exécuter `./download.py` ou `python download.py`

## Script report.py

### Description

Ce script envoie simplement chaque fichier à notre serveur pour les faire évaluer. On évalue le temps de l'analyse, le statut de l'analyse et on obtient les différents type de fuites de données trouvées lors de l'analyse. On note également la taille en octets, le nombre de cellules et le nombre de lignes de code de chaque fichier évalué. On enregistre le tout dans un fichier CSV.

### Exécution

1. Installer les dépendances `pip -r requirements.txt`
2. Exécuter `./report.py` ou `python report.py`
