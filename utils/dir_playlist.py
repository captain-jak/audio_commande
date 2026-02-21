#!/usr/bin/env python3
import os
from pathlib import Path
import mpv
import subprocess

# Chemin du dossier à parcourir
chemin = Path("/media/enjoy/Data/musique/")
nom="titre tango marina"

# Extensions de fichiers audio que tu veux lister
extensions_audio = [".mp3", ".wav", ".ogg", ".flac"]

# def chercher(nom) :
    # print("Fonction chercher", nom)
    # # Parcours récursif du dossier
    # for fichier in chemin.rglob("*"):  # '*' = tous les fichiers et dossiers
        # if fichier.is_file() and fichier.suffix.lower() in extensions_audio:
                # print(f"Fichier audio trouvé : {fichier}")
                # jecherche= fichier.name.lower()
                # if nom in str(fichier):
                    # print(f"Fichier audio trouvé : {fichier}")
                    # return fichier.name
                # else:
                    # return "pas trouve"

# chaine=nom
# mot_a_supprimer="titre"
# nouvelle_chaine = chaine.replace(mot_a_supprimer + " ", "")
# print (f"5️⃣  je cherche {nouvelle_chaine}")
# jejoue=chercher(nouvelle_chaine)
# print (f"5️⃣  jai trouve  {jejoue}")

# Extensions de fichiers audio que tu veux lister
extensions_audio = [".mp3", ".wav", ".ogg", ".flac"]

def chercher(nom) :
    # Parcours récursif du dossier
    for fichier in chemin.rglob("*"):  # '*' = tous les fichiers et dossiers
        if fichier.is_file() and fichier.suffix.lower() in extensions_audio:
             jecherche= fichier.name.lower()
             #print(f"{nom} Fichier audio trouvé : {jecherche}")
             if nom in str(jecherche):
                #print(f"{nom} Fichier audio trouvé : {str(fichier)}")
                return str(fichier)
             
# Pour tester:           
# try:
    # player = mpv.MPV()
# except Exception as e:
    # print("Erreur lors de l'initialisation de MPV :", e)
    # sys.exit(1)
    
# ajouer=chercher("azulidad")
# nouvelle_chaine = ajouer.replace(" ", "\\")
# print(f"Lecture du fichier : {ajouer}")
# #player.play(ajouer)
# process = subprocess.Popen(["mpv","--shuffle","--no-video","--audio-display=no",ajouer])

                