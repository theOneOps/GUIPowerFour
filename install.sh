#!/bin/bash

# Vérifier si Python est installé
if ! command -v python &> /dev/null
then
    echo "Python n'est pas installé. Installation de Python."
    # Ajoutez ici la commande d'installation de Python pour votre
    # distribution spécifique
    # Par exemple, pour Debian/Ubuntu :
    sudo apt-get install python3
fi

# Vérifier si pip est installé
if ! command -v pip &> /dev/null
then
    echo "pip n'est pas installé. Installation de pip."
    # Pour Python 2.x : sudo apt-get install python-pip (ou python2-pip)
    # Pour Python 3.x :
    sudo apt-get install python3-pip
    sudo apt-get install python3-tk
fi

# Installer les dépendances du projet
pip install -r requirements.txt

# Exécuter le script Python principal
python3 main.py
