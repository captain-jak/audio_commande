#!/usr/bin/env python3

import tkinter as tk
from tkinter import messagebox

def lancer_commande():
    # Ici tu mets le code de ta commande vocale
    messagebox.showinfo("Commande vocale", "Commande vocale lancée !")

# Création de la fenêtre principale
root = tk.Tk()
root.title("Commande vocale")
root.geometry("300x150")  # largeur x hauteur

# Bouton pour lancer la commande
btn = tk.Button(root, text="Lancer la commande", command=lancer_commande)
btn.pack(expand=True)

# Lancement de la boucle principale Tkinter
root.mainloop()
