#!/usr/bin/env python3

from pathlib import Path
current_directory = Path.cwd()

# --------------   configuration vosk ----------------------------------------------------
SAMPLE_RATE = 16000
MODEL_PATH = f"{current_directory}/model_vosk/"
MODEL_PATH2 = f"{current_directory}/model_vosk/vosk-model-fr-0.22"
#MODEL_PATH2 = f"{current_directory}/model_vosk/vosk-model-small-fr-0.22"
ZIP_PATH = f"{current_directory}model_vosk/vosk-model-fr-0.22.zip"
MODEL_URL= "https://alphacephei.com/vosk/models/vosk-model-fr-0.22.zip"
# ---------------------------------------------------------------------------------------------

