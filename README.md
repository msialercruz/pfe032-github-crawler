# PFE032-GITHUB-CRAWLER

## Description

Ce script permet d'aller récupérer des fichiers Jupyter Notebook depuis Github. Celui-ci nous permet de tester notre outil d'analyse de data leakage avec des données réelles.

Ce script se déroule en plusieurs étapes. Voici chaque étape détaillé suivant un ordre chronologique :
1. On va tout d'abord trouver tous les répertoires Github dont le langage principal est "Jupyter Notebook". Pour les obtenir, nous utilisons le lien de recherche Github https://github.com/search avec les paramètres suivants : ``created:>2023-05-01 created:<2023-05-31 language: "Jupyter Notebook" license:mit machine learning``. Nous indiquons que nous voulons des répertoires datant de mai 2023, avec une licence MIT et contenant "machine" et "learning" dans leur nom ou leur description.
2. Après avoir récupéré chaque répertoire, nous allons obtenir la liste des fichiers ipynb (Jupyter Notebook) en utilisant les paramètres suivants : ``repo :... path:*.ipynb fit``. On remplace ce qui suit "repo:" par le nom du propriétaire suivi d'un / suivi du nom du répertoire (par exemple Azure/MachineLearningNotebooks). Nous indiquons également que nous voulons des fichiers ipynb qui contiennent le terme ``fit``, qui correponds a la fonction utilisée pour entraîner des modèles.
3. Ensuite, une fois que nous avons tous les liens vers les fichiers ipynb dans chaque répertoire, nous les téléchargeons. Les fichiers ne contenant aucune cellule de type "code", n'étant pas au format JSON ou utilisant la librairie Tensorflow, qui n'est pas actuellement supportée par notre outil d'analyse, ne seront pas sauvegarder. Les autres fichiers considérés comme valides sont séparés par taille pour voir comment le temps d'analyse de notre outil dépend de la taille du fichier.

## Exécution

1. Installer les dépendances ``pip -r requirements.txt``
2. Exécuter ``./main.py`` ou ``python main.py``
