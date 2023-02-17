# FIRST Team 3996 - 2020

## Installation
Télécharger et extraire ce projet (ou encore mieu le cloner avec git)
Installer [python 3.10](https://www.python.org/downloads/)
Ouvrez un terminal (powershell sur windows ou bash sur Linux) et exécuter `python3 -m pip install --upgrade pip`
Exécuter par la suite `python3 -m pip install poetry`
NOTE: Si `python3` est inconnu par le terminal, réessayer les commandes avec `python`. Vous pouvez faire `python -V` pour valider que vous avez la bonne version

Ouvrir un terminal et naviguez jusqu'au dossier du projet
Exécuter `poetry install`

## Utilisation
Ouvrir un terminal et naviguez jusqu'au dossier du projet. Depuis cet emplacement, vous pouvez exécuter les commandes suivantes

`poetry udpate` pour mettre les dépendances à jours

`robotpy-installer download-python` pour télécharger python pour le roborio sur votre ordinateur
`robotpy-installer install-python` pour installer python sur le roborio
`robotpy-installer download robotpy-navx robotpy-rev robotpy-ctre robotpy-wpilib-utilities` pour télécharger les dépendances pour robotrio
`robotpy-installer install robotpy-navx robotpy-rev robotpy-ctre robotpy-wpilib-utilities` pour installer les dépendances sur le robotio

`python ./robot-code/robot.py` pour voir l'ensemble des actions possibles
`python ./robot-code/robot.py deploy --nc` pour déployer le code avec un suivi sur le terminal
`python ./robot-code/robot.py deploy` pour déployer le code de façon finale


## Ajouter une nouvelle dépendance
Exécuter le fichier poetry_shell.ps1 (Windows) ou poetry_shell.sh (Linux)
`poetry add <nom_de_la_dependance>` pour ajouter une nouvelle dépendance (Ex.: robotpy-navx ou robotpy-ctre)
`robotpy-installer download <nom_de_la_dependance>` pour télécharger la dépendance pour le robotrio
`robotpy-installer install <nom_de_la_dependance>` pour installer la dépendance sur le robotio
