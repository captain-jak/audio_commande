#!/usr/bin/env python3

# sudo apt install python3.13-venv
# environnement python
#python3 -m venv venv_clean
#source venv_clean/bin/activate

import sys
import queue
import sounddevice as sd
import json
import os
import time
import subprocess
import tempfile
import threading
from vosk import Model, KaldiRecognizer, SetLogLevel
from utils import dir_playlist
from radios_conf import lesradios, laplaylist_locale, laplaylist_distant
import ssh_gen

# ----------------- Configuration -----------------
MODEL_PATH = "/home/enjoy/dev/Reconnaissance_vocale/audio_commande/model_vosk/vosk-model-small-fr-0.22"
PIPER_MODEL = "/home/enjoy/dev/Reconnaissance_vocale/model_piper/piper-fr_FR-medium/piper_model.onnx"
WAKE_WORD = "ordinateur"
EXIT_WORDS = ["quitter", "quit"]
TTS_FILE = "tts.wav"
mic_enabled = True
q = queue.Queue()
# -------------------------------------------------

# Serveur audio
leserveur = sys.argv[1] if len(sys.argv) > 1 else None
if leserveur == "local":
    SERV_LOCAL = True
elif leserveur == "distant":
    SERV_LOCAL = False
else:
    print("Syntaxe: local | distant")
    exit()
print("Serveur audio:", leserveur)

# ----------------- Audio callback -----------------
def callback(indata, frames, time_info, status):
    if mic_enabled:
        q.put(bytes(indata))

# ----------------- TTS -----------------
def speak(text: str):
    """Parle via Piper en thread séparé, sans echo"""
    def tts_thread(text_inner):
        global mic_enabled
        mic_enabled = False
        os.system('pactl set-source-mute @DEFAULT_SOURCE@ 1')

        # Écriture dans un fichier temporaire pour Piper
        with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix='.txt') as tmpfile:
            tmpfile.write(text_inner)
            tmpfile_path = tmpfile.name

        # Génération TTS
        subprocess.run([
            "piper",
            "--model", PIPER_MODEL,
            "--input_file", tmpfile_path,
            "--output_file", TTS_FILE
        ], check=True)

        # Lecture audio
        subprocess.run(["aplay", TTS_FILE], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        # Suppression du fichier temporaire
        os.remove(tmpfile_path)
        time.sleep(0.3)
        mic_enabled = True
        os.system('pactl set-source-mute @DEFAULT_SOURCE@ 0')  # unmute

    threading.Thread(target=tts_thread, args=(text,), daemon=True).start()

# ----------------- Commandes -----------------
def traiter_commande(text: str):
    """Traite uniquement les commandes de lecture (radio, playlist, titre)"""
    text = text.lower()
    if "station" in text and "disponible" in text:
        print("France inter | France musique | France culture | Fip | Fip cultes | Radio 50")
    elif "playlist" in text:
        joue(text, "playlist")
    elif "radio" in text:
        joue(text, "radio")
    elif "titre" in text:
        joue(text, "letitre")
    elif "instruction" in text:
        # ici, commande() sera appelée directement, mais ne pas réappeler traiter_commande
        commande(text)
    else:
        print("🤷 Instruction inconnue:", text)

def joue(text: str, media: str):
    """Joue radio, playlist ou titre dans un thread pour ne pas bloquer l'écoute"""
    def player_thread(valeur_inner):
        if SERV_LOCAL:
            print("❌ lecteur local ligne 102:")
            subprocess.run(["pkill", "mpv"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            subprocess.Popen(["mpv", "--shuffle", "--no-video", "--audio-display=no", valeur_inner])
        else:
            #print("❌ lecteur distant ligne 106")
            ssh_gen.laconnexion(valeur_inner)

    cle, valeur = None, None
    if media == "playlist":
        source = laplaylist_locale if SERV_LOCAL else laplaylist_distant
        for k, v in source.items():
            if k in text:
                cle, valeur = k, v
                break
    elif media == "radio":
        for k, v in lesradios.items():
            if k in text:
                cle, valeur = k, v
                break
    elif media == "letitre":
        recherche = text.replace("titre ", "")
        print(f"🔍 Recherche titre: {recherche}")
        valeur = dir_playlist.chercher(recherche)

    if not valeur:
        print("❌ Aucun média trouvé pour:", text)
        return

    print("🎙️ Lecture:", cle or valeur)
    threading.Thread(target=player_thread, args=(valeur,), daemon=True).start()

def commande(text: str):
    text = text.lower()
    lordre = None
    if "augmente" in text and "le volume" in text:
        lordre = "pactl set-sink-volume @DEFAULT_SINK@ +20%"
    elif "baisse" in text and "le volume" in text:
        lordre = "pactl set-sink-volume @DEFAULT_SINK@ -20%"
    elif "arrêt" in text or "stop" in text:
        lordre = "pkill mpv"
    else:
        print("🤷 Instruction inconnue:", text)
        speak(f"{text} est une instruction inconnue")
        return
    if SERV_LOCAL:
        print("🤷 threading: - ligne 147", lordre)
        threading.Thread(target=os.system, args=(lordre,), daemon=True).start()
    else:
        ssh_gen.lestop(lordre)

# ----------------- Initialisation -----------------
SetLogLevel(-1)
model = Model(MODEL_PATH)
rec = KaldiRecognizer(model, 16000)

speak(f"Assistant prêt, le mot clé est {WAKE_WORD}")
print("🎤 Assistant prêt  Mot clé:", WAKE_WORD)

# ----------------- Boucle principale -----------------
with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype="int16", channels=1, callback=callback):
    while True:
        data = q.get()
        if rec.AcceptWaveform(data):
            text = json.loads(rec.Result()).get("text", "").lower()
            if text:
                print("🗣️", text)
            if WAKE_WORD in text:
                speak("Oui je vous écoute?")
                print(f"🟢 Mode conversation activé (dites {EXIT_WORDS})")
                while True:
                    data = q.get()
                    if rec.AcceptWaveform(data):
                        cmd = json.loads(rec.Result()).get("text", "").lower()
                        if not cmd:
                            continue
                        print("Commande:", cmd)
                        if any(word in cmd for word in EXIT_WORDS):
                            print("🔴 Fin de la conversation")
                            #speak(f"Fin de la conversation. Mode écoute avec le mot clé {WAKE_WORD}")
                            break
                        elif "heure" in cmd:
                            speak(time.strftime("Il est %H heures %M"))
                        elif any(vol in cmd for vol in ["baisse le volume", "augmente le volume", "stop", "arrêt"]):
                            commande(cmd)  # traité une seule fois
                        else:
                            traiter_commande(cmd)


