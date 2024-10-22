# Eval à la carte

Version 0.5.1 du 22-10-2024

L’ensemble des fichiers est distribué sous la licence CC BY SA  https://creativecommons.org/licenses/by-sa/4.0/deed.fr

Auteur : Matthieu DEVILLERS

Ce projet s’inspire librement de celui de Rémi ANGOT : http://revue.sesamath.net/spip.php?article535



### Cloner le dépot ou télécharger l'ensemble des fichiers 

### Installer streamlit 

[https://docs.streamlit.io/library/get-started/installation](https://docs.streamlit.io/library/get-started/installation)

### Lancer l'application localement

```bash
$ cd chemin/vers/ALaCarte
$ pipenv shell
$ streamlit run Accueil.py

```

### TODO

* [ ] Possibilité de ranger les fichiers tex des exercices dans des sous-répertoires (un par referentiel) et possibilité de choisir le référentiel utilisé lors de la création de l'évaluation.
* [ ] interface pour ajouter des référentiels / ajouter des exercices.
* [ ] Possibilité de télécharger des fichiers exemples pour demandes.csv, facultatif.tex, commun.tex et tableaux items correspondants. 
* [ ] Factoriser le code (OuiNON....)
* [ ] Commenter le code
* [ ] Améliorer (nom des variables...)
* [ ] Ouvrir le projet à des contributions extérieures
