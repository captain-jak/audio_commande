#!/bin/bash

# 1. Définition du chemin correct (Chemin absolu)
APP_DIR="/home/enjoy/dev/Reconnaissance_vocale/audio_commande"
VENV_PATH="$APP_DIR/venv_clean"

## 1. Mode verbeux pour voir tout ce qui se passe
#set -x  # Affiche chaque commande avant de l'exécuter
#echo "--- Démarrage du diagnostic ---"
## 2. Vérification du répertoire de travail
## On force le script à se situer dans son propre dossier pour éviter les erreurs de chemin relatif
#cd "$(dirname "$0")"
#echo "Répertoire actuel : $(pwd)"

## 3. Activation de l'environnement virtuel
#if [ -f "$VENV_PATH/bin/activate" ]; then
    #echo "[OK] Activation de l'environnement virtuel..."
    #source "$VENV_PATH/bin/activate"
#else
    #echo "[ERREUR] Environnement virtuel introuvable dans : $VENV_PATH"
    #exit 1
#fi

## 4. Vérification de l'environnement (ex: Python ou binaire)
## Remplacez 'python3' par votre moteur de reconnaissance si différent
#if ! command -v python3 >/dev/null; then
    #echo "[ERREUR] Python n'est pas installé."
    #exit 1
#fi
# 5. Lancement de l'application avec capture d'erreur
#echo "--- Lancement de la reconnaissance vocale ---"
# Remplacez la ligne ci-dessous par votre commande réelle
# python3 main.py 2>&1 | tee debug_session.log
#python3 /home/enjoy/dev/Reconnaissance_vocale/audio_commande/main.py distant 2>&1 | tee debug_session.log
#xfce4-terminal -e "bash -c 'flock -n /tmp/commande_vocale.lock /usr/bin/python3 /home/enjoy/dev/Reconnaissance_vocale/audio_commande/main.py distant'" &
bash -c 'flock -n /tmp/commande_vocale.lock /usr/bin/python3 /home/enjoy/dev/Reconnaissance_vocale/audio_commande/main.py distant' &
## On garde la main à la fin pour lire les messages si --hold n'est pas utilisé
read -n 1

##=>exec 2> /tmp/debug_commande.log # Envoie les erreurs dans un fichier log

## ... à la fin de votre script lancer_commande_.sh ...
#echo "Traitement terminé. Fermeture..."
#exit 0

