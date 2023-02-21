# FIRST Team 3996 - 2020

## Installation
Télécharger et extraire ce projet (ou encore mieu le cloner avec git)

### Sur Windows
installer [python 3.10](https://www.python.org/downloads/)
Ouvrez un terminal powershell exécutez
`python -V` pour valider que votre version de python est bonne
`python -m pip install --upgrade pip` pour mettre à jours le gestionnaire des dépendances
`python -m pip install -U poetry` pour installer un outil de gestion des dépendances

Ouvrez un terminal et naviguez jusqu'au dossier du projet. Exécutez
`poetry install`

### Sur Linux (Ubuntu 2022.04 ou plus)
python 3.10 est installé par défaut
Ouvrez un terminal et exécutez
`python3 -V` pour valider que votre version de python est bonne
`sudo apt update && sudo apt install -y python3-pip` pour installer le gestionnaire des dépendances
`python3 -m pip install --upgrade pip` pour mettre à jours le gestionnaire des dépendances
`python3 -m pip install -U poetry` pour installer un outil de gestion des dépendances

Ouvrez un terminal et naviguez jusqu'au dossier du projet. Exécutez
`poetry install`


## Utilisation
NOTE: Remplacez `python3` par `python` selon votre plateforme

Ouvrir un terminal et naviguez jusqu'au dossier du projet. Depuis cet emplacement, vous pouvez exécuter les commandes suivantes

`poetry run robotpy-installer download-python` pour télécharger python pour le roborio sur votre ordinateur
`poetry run robotpy-installer install-python` pour installer python sur le roborio
`poetry run robotpy-installer download robotpy-navx robotpy-rev robotpy-ctre robotpy-wpilib-utilities` pour télécharger les dépendances pour robotrio
`poetry run robotpy-installer install robotpy-navx robotpy-rev robotpy-ctre robotpy-wpilib-utilities` pour installer les dépendances sur le robotio

`poetry run python ./robot-code/robot.py` pour voir l'ensemble des actions possibles
`poetry run python ./robot-code/robot.py deploy --nc` pour déployer le code avec un suivi sur le terminal
`poetry run python ./robot-code/robot.py deploy` pour déployer le code de façon finale


## Ajouter une nouvelle dépendance
Exécuter le fichier poetry_shell.ps1 (Windows) ou poetry_shell.sh (Linux)
`poetry add <nom_de_la_dependance>` pour ajouter une nouvelle dépendance (Ex.: robotpy-navx ou robotpy-ctre)
`poetry robotpy-installer download <nom_de_la_dependance>` pour télécharger la dépendance pour le robotrio
`poetry robotpy-installer install <nom_de_la_dependance>` pour installer la dépendance sur le robotio

`poetry update <nom_de_la_dependance>` pour mettre à jours une dépendance