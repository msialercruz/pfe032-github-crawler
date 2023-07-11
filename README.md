# PFE032-GITHUB-CRAWLER

## Description

Ce script permet d'aller récupérer des fichiers Jupyter Notebook depuis Github. Celui-ci nous permet de tester notre outil d'analyse de data leakage avec des données reelles.

Ce script se déroule en plusieurs étapes. Voici chaque étape détaillé suivant un ordre chronologique :
1. On va tout d'abord trouver tous les répertoires Github dont le langage principal est "Jupyter Notebook". Pour les obtenir, nous utilisons le lien de recherche Github https://github.com/search avec les paramètres suivants : ``created:>2023-05-01 created:<2023-05-31 language: "Jupyter Notebook" license:mit machine learning``. Nous indiquons que nous voulons des répertoires datant de mai 2023, avec une licence MIT et contenant "machine" et "learning" dans leur nom ou leur description.
2. Après avoir récupéré chaque répertoire, nous allons obtenir la liste des fichiers ipynb (Jupyter Notebook) en utilisant les paramètres suivants : ``repo :... path:*.ipynb fit``. On remplace ce qui suit "repo:" par le nom du propriétaire suivi d'un / suivi du nom du répertoire (par exemple Azure/MachineLearningNotebooks). Nous indiquons également que nous voulons des fichiers ipynb qui contiennent le terme ``fit``, qui est souvent la fonction utilisée pour entraîner un modèle.
3. Ensuite, une fois que nous avons tous les liens vers les fichiers ipynb dans chaque répertoire, nous les téléchargeons simplement. Comme nous aurons un grand nombre de téléchargements à effectuer, nous utiliserons plusieurs "threads" (fils d'exécution) pour accélérer le processus.
4. Enfin, nous allons séparer les fichiers valides des fichiers invalides. Les fichiers invalides sont ceux qui ne contiennent pas de cellules de code, qui ne sont pas au format JSON et qui utilisent la librairie Tensorflow, qui n'est pas actuellement supportée par notre outil d'analyse. Les fichiers valides sont séparés par catégorie de taille : sm (inférieur ou égal à 10 KB), md (entre 10KB et 100KB) et lg (supérieur à 100KB).

<h2 id="dependencies">Dépendances</h2>

- [python](https://www.python.org/) <=3.10
- [jq](https://jqlang.github.io/jq/)

## Exécution

### Avec docker

1. Construire l'image : ``docker build -t pfe032-github-crawler .``
2. Exécuter l'image : ``docker run -v ./notebooks:/var/www/notebooks/ pfe032-github-crawler``

### Sans docker

1. Installer les [dépendances](#dependencies) sur poste local.
2. Créer le dossier notebooks a la racine
3. Exécuter ``./main.py`` ou ``python main.py``