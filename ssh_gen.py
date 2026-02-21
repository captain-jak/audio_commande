#!/usr/bin/env python3
# release 3.1.2 - 16-02-2026

# Prérequis : pip install fabric paramiko

from fabric import Connection
from invoke.exceptions import UnexpectedExit
import subprocess
import socket

# ----------------- Configuration SSH -----------------
KEY_FILENAME = "/home/enjoy/.ssh/gen.selfmicro.com"
PASSPHRASE = "bonjourselfmicro"
SERV_LOCAL = True
REMOTE_USER = "gen"
IP_SERVEUR='192.168.1.80'
# ------------------------------------------------------

# Connexion SSH réutilisable
def get_connection(user: str = REMOTE_USER) -> Connection:
    return Connection(
        host=user,
        connect_kwargs={
            "key_filename": KEY_FILENAME,
            "passphrase": PASSPHRASE,
            "allow_agent": False,
            "look_for_keys": False
        }
    )

# Vérifie la connexion SSH
def connexion_ok(host: str, user: str = None, timeout: int = 5) -> bool:
    try:
        conn = get_connection(user or host)
        conn.open()
        conn.close()
        return True
    except (socket.error, UnexpectedExit, Exception):
        return False

# #=>if connexion_ok(IP_SERVEUR, "tester"):
    # #=>print("Connexion OK")
# #=>else:
    # #=>print(f"Connexion impossible ip {IP_SERVEUR}")

# ----------------- Fonctions -----------------

def ssh_connect(action: str) -> str:
    try:
        conn = get_connection()
        if "disconnect" in action:
            conn.close()
        # ici on pourrait ajouter d'autres actions si besoin
    except Exception as e:
        return f"Erreur SSH : {e}"
    return f"SSH action '{action}' effectuée !"

def laconnexion(nom: str) -> str:
    """Lance la radio sur le serveur distant"""
    try:
        conn = get_connection()
        # Arrête les mpv existants
        conn.run("nohup pkill mpv > fichier_sortie.log 2>&1 &", hide=False)
        # Volume par défaut
        conn.run("pactl set-sink-volume @DEFAULT_SINK@ 50%", hide=False)
        # Lance mpv en arrière-plan
        cmd = f"nohup mpv --shuffle {nom} > fichier_sortie.log 2>&1 &"
        conn.run(cmd, hide=False)
    except Exception as e:
        return f"Erreur lancement radio : {e}"
    return f"Vous écoutez {nom} !"

def leson(step: str, nom: str) -> str:
    """Régle le volume ou lance la lecture locale"""
    try:
        if SERV_LOCAL:
            cmd = f"amixer set Master {step}"
            conn = get_connection()
            conn.run(cmd, hide=False)
        else:
            subprocess.Popen(["mpv", "--no-video", "--audio-display=no", nom])
        print(f"🗣️ Volume réglé sur {step} avec {nom}")
    except Exception as e:
        return f"Erreur lecture/volume : {e}"
    return f"Le niveau sonore est {step} !"

def lestop(action: str):
    """Stoppe mpv ou ajuste le volume"""
    try:
        conn = get_connection()
        if "pkill" in action:
            conn.run("pkill mpv", hide=False)
        elif any(ch.isdigit() for ch in action):
            conn.run(action, hide=False)
    except Exception as e:
        print(f"Erreur stop : {e}")

def jemonte() -> str:
    """Monte le partage distant"""
    try:
        if SERV_LOCAL:
            cmd = "sshfs enjoy@192.168.1.98:/media/enjoy/Data/musique /home/enjoy/Musique/enjoy"
            conn = get_connection()
            conn.run(cmd, hide=False)
    except Exception as e:
        return f"Erreur montage : {e}"
    return "Monté"

def jedemonte() -> str:
    """Démonte le partage distant"""
    try:
        if SERV_LOCAL:
            cmd = "fusermount -u /home/enjoy/Musique/enjoy"
            conn = get_connection()
            conn.run(cmd, hide=False)
    except Exception as e:
        return f"Erreur démontage : {e}"
    return "Démonté"
