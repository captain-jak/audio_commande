#!/usr/bin/env python3

# ----------------------    prerequis:   --------------------------------------------
# # sur le serveur local (lenovo 192.168.1.98) installer cifs-utils
# sudo apt install sshfs
# #=>sudo nano /root.smbcred
	# #=>username=enjoy
	# #=>password=enjoy
#=================================================
# Beaucoup + simple avec sshfs
#mount
# enjoy@gen:~/Musique$ echo "enjoy" | sshfs enjoy@192.168.1.98:/media/enjoy/Data/musique /home/enjoy/Musique/enjoy -o password_stdin
# umount 
#fusermount -u  /home/enjoy/Musique/enjoy
# enjoy@gen | fusermount -u  /home/enjoy/Musique/enjoy
#=================================================
import os
from fabric import Connection
import subprocess

import ssh_gen # connexion au serveur player

# -------------------------------
# Configuration
# -------------------------------
REMOTE_SHARE = "enjoy@192.168.1.98:/media/enjoy/Data/musique"
    # host = REMOTE_SHARE.split("/")[2].split("@")[0]
    
# REMOTE_SHARE = "enjoy@192.168.1.98:/media/enjoy/Data/musique"
    # host = REMOTE_SHARE.split("/")[2].split(":")[0]

MOUNT_POINT = "/home/enjoy/Musique/enjoy"
CRED_FILE = "/root/.smbcred"   # doit contenir username/password
USER = "enjoy"                 # utilisateur local pour les fichiers montés
GROUP = "enjoy"                # groupe local
SCRIPT_VERSION = "1.0"            # ma version du script

# -------------------------------
# Fonctions
# -------------------------------


def check_ping(host):
    """Vérifie si l'hôte distant répond au ping"""
    result = subprocess.run(["ping", "-c", "1", "-W", "1", host],stdout=subprocess.DEVNULL)
    print ("je ping")
    return result.returncode == 0

def ensure_mount_point(path):
    ssh_gen.jemonte(lordre)

def is_mounted(path):
    """Vérifie si le chemin est déjà monté"""
    return subprocess.run(["mountpoint", "-q", path]).returncode == 0


def mount_share():
    """Monte le partage distant"""
    if is_mounted(MOUNT_POINT):
        print(f"✅ {MOUNT_POINT} est déjà monté")
        return

    ensure_mount_point(MOUNT_POINT)
   # sudo mount -t cifs //192.168.1.98/Data /mnt/Data/musique  -o enjoy=user,enjoy=pass,uid=1000,gid=1000,iocharset=utf8
        cmd = [
        "sudo", "mount", "-t", "cifs",
        REMOTE_SHARE,
        MOUNT_POINT,
        "-o", f"credentials={CRED_FILE},uid={os.getuid()},gid={os.getgid()},iocharset=utf8,vers={SMB_VERSION}"
    ]
    
# enjoy@gen:~/Musique | sshfs enjoy@192.168.1.98:/media/enjoy/Data/musique /home/enjoy/Musique/enjoy
    cmd = [
        "enjoy@gen:~/Musique$ echo ", "-t", "cifs",
        REMOTE_SHARE,
        MOUNT_POINT,
        "-o", f"credentials={CRED_FILE},uid={os.getuid()},gid={os.getgid()},iocharset=utf8,vers={SMB_VERSION}"
    ]
    lordre="sshfs enjoy@192.168.1.98:/media/enjoy/Data/musique /home/enjoy/Musique/enjoy"
    print("Montage du partage...")
    result = ssh_gen.jemonte(lordre)
    if result.returncode == 0:
        print(f"✅ Montage réussi : {MOUNT_POINT}")
    else:
        print(f"❌ Montage échoué, vérifiez sshfs et firewall")

def unmount_share():
    lordre="sshfs enjoy@192.168.1.98:/media/enjoy/Data/musique /home/enjoy/Musique/enjoy"
    """Démonte le partage"""
    if is_mounted(MOUNT_POINT):
        print(f"Démontage de {MOUNT_POINT}")
        result = ssh_gen.jedemonte(lordre)
    else:
        print(f"{MOUNT_POINT} n’est pas monté")

# -------------------------------
# Script principal
# -------------------------------
c = Connection(
    "gen",
    connect_kwargs={
        "key_filename": KEY_FILENAME,
        "passphrase": PASSPHRASE,          # ← ici
        "allow_agent": False,              # optionnel : désactive agent si conflit
        "look_for_keys": False
    }
)

c.run("pactl set-sink-volume @DEFAULT_SINK@ 50%", hide=False)
c.close()

if __name__ == "__main__":
    # REMOTE_SHARE = "enjoy@192.168.1.98:/media/enjoy/Data/musique"
    leuser = REMOTE_SHARE.split("/")[2].split(":")[0]
    host = REMOTE_SHARE.split("@")[1].split(":")[0]
    print ("serveur", host, " - user: ",leuser)
    if not check_ping(host):
        print(f"❌ Impossible de joindre {host}")
    else:
        mount_share()
        # --- Décommenter pour démonter automatiquement ---
        # unmount_share()


