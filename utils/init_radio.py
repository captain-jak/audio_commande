#!/usr/bin/env python3
import os
import zipfile
import subprocess
from vosk_conf import MODEL_PATH, MODEL_PATH2, MODEL_URL

# =============================================
#                            Prerequis: 
# =============================================
#     environnement python
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
#      modules python:         vosk - sounddevice - numpy
# ------------------------------------------------------------------------------

def install_package(pkg):
    subprocess.check_call([sys.executable, "-m", "pip", "install", pkg])
# Vosk
try:
    import vosk
except ImportError:
    print("Vosk non trouvé, installation...")
    install_package("vosk")
    import vosk

# Sounddevice
try:
    import sounddevice as sd
except ImportError:
    print("Sounddevice non trouvé, installation...")
    install_package("sounddevice")
    import sounddevice as sd

# NumPy
try:
    import numpy as np
except ImportError:
    print("NumPy non trouvé, installation...")
    install_package("numpy")
    import numpy as np
    
# ------------------------------------------------------------------------------------------------------------
# 2️⃣ Télécharger le modèle français si nécessaire
# ------------------------------------------------------------------------------------------------------------
if not os.path.exists(MODEL_PATH2):
    print("Téléchargement du modèle français...")
    subprocess.check_call(["wget", "-P", MODEL_PATH, MODEL_URL])
    print("Extraction du modèle...")
    
    with zipfile.ZipFile(ZIP_PATH, 'r') as zip_ref:
        zip_ref.extractall(MODEL_PATH)
    os.remove(ZIP_PATH)
    print(f"Modèle installé dans {MODEL_PATH}")
# =============================================
