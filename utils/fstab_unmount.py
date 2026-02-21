#!/usr/bin/env python3

import os

mount_point = "/mnt/Data/musique"
os.system(f"sudo umount {mount_point}")

# Vérifier
if os.path.ismount(mount_point):
    print("❌  Démontage échoué :", mount_point)
else:
    print("✅  Démontage réussi")