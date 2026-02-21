#!/bin/bash

# 1. Installer les plugins
sudo apt install geany-plugins
# 2. Activer le plugin : 
#Allez dans le menu Outils > Gestionnaire de plugins. 
#Cochez GitChangeBar (pour voir les modifs en direct) et Addons (pour le terminal).
#3. Utiliser Git : Une fois activé, 
#vous verrez des indicateurs de couleur dans la marge de Geany pour les lignes modifiées.

#---------------------------------------------------------------------------
### Installatio depôt audio_commande sur github
#---------------------------------------------------------------------------
# apres avoit créer une cle de connexion sur github.com voir procedure sur le site)
# sur le client:
cd ~/dev/Reconnaissance_vocale/audio_commande
# Initialiser le dépôt local
git init
# Ajouter tous les fichiers au suivi Git
git add .
# Créer le premier commit
git commit -m "Initial commit : projet reconnaissance vocale"
# Créer la branche principale (main)
git branch -M main
Lier votre dossier local au dépôt GitHub
# Remplacez "VOTRE_NOM_UTILISATEUR" par votre vrai pseudo GitHub
git remote add origin https://github.com/VOTRE_NOM_UTILISATEUR/audio_commande.git
# Envoyer le code vers GitHub
git push -u origin main