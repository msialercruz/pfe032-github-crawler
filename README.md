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

*Ce script requiert d'avoir exécuté le script download*

Pour faire ce rapport de performance, on a utilisé un script python. Ce script envoie évaluer chaque fichier qu'on avait collecté depuis Github à l'outil d'analyse et ensuite généré des statistiques avec les résultats obtenus sous forme de diagrammes.

Un premier fichier CSV contenant les résultats d'analyse est d'abord généré. Ce fichier indique combien de chaque type de fuites ont été trouvées, le temps d'analyse et le statut de l'analyse. On va également calculer le nombre de lignes et le nombre de cellules contenues dans chaque fichier.

Ensuite, les diagrammes permettant d'illustrer les statistiques suivantes vont être générés :
- un nuage de points pour illustrer le temps d'exécution selon nombre de lignes d'un Jupyter Notebook
- un diagramme en point de tartes pour illustrer le pourcentage de chaque statut d'analyse
- un diagramme en point de tartes pour illustrer le pourcentage de chaque type de fuites de donnée
- un diagramme à barres pour illustrer le nombre de fichiers Jupyter Notebook par quantité de fuites de donnée

Une première analyse a été faite après avoir réussi a modifier notre outil pour recevoir les données d'analyse sous format JSON ou lieu de HTML.



Voici les statistiques qui avaient été générées en fonction des résultats obtenus sur 476 fichiers Jupyter Notebook :

Dans le premier diagramme, on peut voir que le temps d'exécution n'est pas du tout impacté pas le nombre de lignes contenues dans un fichier. On voit également que le temps maximal est de 300 secondes, ce qui correspond en réalité a un statut d'analyse "timeout". Cela est dû au fait qu'après un certain temps d'exécution, l'analyse est arrêtée et on ne reçoit aucune donnée d'analyse.

Dans le deuxième diagramme, on voit que 87.8 % d'analyses sont des succès, 2.9 % sont des "timeout" et 9.2 % ne produisent aucune donnée d'analyses, car lors de l'analyse a produit de(s) erreur(s) et on ne reçoit aucune donnée d'analyse comme pour le cas des "timeout".

Dans le troisième diagramme, on voit que parmi 79 fichiers dont l'analyse a détecté des fuites de donnés, 34.8 % correspondent à des cas de fuite de type "overlap leakage", 32.6 % à des cas de fuite de type "pre-processing" et 32.6 % à des cas de fuite de type "multi-test". On voit que la quantité pour chaque type de fuites de données est presque égale.

Dans le quatrième diagramme, on voit que parmi 79 fichiers dont l'analyse a détecté des fuites de donnés, la majorité de ses fichiers contiennent une seule fuite de données. On remarque également que le nombre maximal de fuites données est de 8.


### Exécution

1. Installer les dépendances `pip -r requirements.txt`
2. Exécuter `./report.py` ou `python report.py`
