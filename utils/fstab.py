#!/usr/bin/env python3

# ----------------------    prerequis:   --------------------------------------------
# # sur le serveur local (lenovo 192.168.198) installer cifs-utils
# sudo apt install cifs-utils
#sudo nano /etc/samba/smb.conf
# [Data]
   # path = /media/enjoy/Data/musique
   # read only = no
   # browsable = yes
   # guest ok = yes
#sudo systemctl restart smbd
# # sur le serveur local (gen 192.168.1.80) installer cifs-utils
# sudo apt install cifs-utils
# Créer le point de montage
# sudo mkdir -p /mnt/Data/musique
#Monter via Python
#Demonter via Python
# os.system("sudo umount /mnt/Data")
#=================================================
# sudo mount -t cifs //192.168.1.98/Data /mnt/Data/musique  -o enjoy=user,enjoy=pass,uid=1000,gid=1000,iocharset=utf8
#=================================================
import os
import subprocess

# -------------------------------
# Configuration
# -------------------------------
REMOTE_SHARE = "//192.168.1.98/Data"
MOUNT_POINT = "/mnt/Data/musique"
CRED_FILE = "/root/.smbcred"   # doit contenir username/password
USER = "enjoy"                 # utilisateur local pour les fichiers montés
GROUP = "enjoy"                # groupe local
SMB_VERSION = "3.0"            # SMB2/3 moderne

# -------------------------------
# Fonctions
# -------------------------------

def check_ping(host):
    """Vérifie si l'hôte distant répond au ping"""
    result = subprocess.run(["ping", "-c", "1", "-W", "1", host],stdout=subprocess.DEVNULL)
    return result.returncode == 0

def ensure_mount_point(path):
    """Crée le répertoire de montage si nécessaire"""
    if not os.path.exists(path):
        print(f"Création du point de montage : {path}")
        os.makedirs(path, exist_ok=True)
    os.chown(path, uid=os.getuid(), gid=os.getgid())

def is_mounted(path):
    """Vérifie si le chemin est déjà monté"""
    return subprocess.run(["mountpoint", "-q", path]).returncode == 0


def mount_share():
    """Monte le partage distant"""
    if is_mounted(MOUNT_POINT):
        print(f"✅ {MOUNT_POINT} est déjà monté")
        return

    ensure_mount_point(MOUNT_POINT)

    cmd = [
        "sudo", "mount", "-t", "cifs",
        REMOTE_SHARE,
        MOUNT_POINT,
        "-o", f"credentials={CRED_FILE},uid={os.getuid()},gid={os.getgid()},iocharset=utf8,vers={SMB_VERSION}"
    ]
    print("Montage du partage...")
    result = subprocess.run(cmd)
    if result.returncode == 0:
        print(f"✅ Montage réussi : {MOUNT_POINT}")
    else:
        print(f"❌ Montage échoué, vérifiez Samba et firewall")

def unmount_share():
    """Démonte le partage"""
    if is_mounted(MOUNT_POINT):
        print(f"Démontage de {MOUNT_POINT}")
        subprocess.run(["sudo", "umount", MOUNT_POINT])
    else:
        print(f"{MOUNT_POINT} n’est pas monté")

# -------------------------------
# Script principal
# -------------------------------
if __name__ == "__main__":
    host = REMOTE_SHARE.split("/")[2].split(":")[0]
    if not check_ping(host):
        print(f"❌ Impossible de joindre {host}")
    else:
        mount_share()
        # --- Décommenter pour démonter automatiquement ---
        # unmount_share()


