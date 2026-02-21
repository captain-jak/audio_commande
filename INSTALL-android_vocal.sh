############################################################################
###     ta voix lance une action Android qui exécute une commande SSH vers ton serveur.
############################################################################

Étapes
Installer Termux (sur Android)
Installer SSH :
pkg update
pkg install openssh
Tester la connexion :
ssh user@ip_du_serveur

Créer une clé SSH (pour éviter le mot de passe) :
ssh-keygen
ssh-copy-id user@ip_du_serveur

Créer un script Android (ex: cmd.sh) :
ssh user@ip_du_serveur "commande_linux"
Rendre exécutable :
chmod +x cmd.sh

Associer à une commande vocale :
Installer Tasker ou MacroDroid
Profil → Commande vocale / Assistant
Action → Exécuter :
/data/data/com.termux/files/home/cmd.sh

👉 Quand tu dis : "Lancer serveur", la commande Linux s’exécute.

############################################################################
#Méthode Webhook (plus propre / distant)
Sur le serveur Linux
Exemple Python (Flask) :
nano server.py

Sur Android
Avec Tasker / MacroDroid
Déclencheur : commande vocale
Action : HTTP GET

http://IP_SERVEUR:5000/cmd


