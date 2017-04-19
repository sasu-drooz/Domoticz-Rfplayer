Ziblue Rfp1000 plugins for Domoticz


Prérequis :

-Avoir Domoticz et les plugins python fonctionnel (uniquememnt sur la version beta pour le moment)

-Python 3.4 installé (nécessaire pour exécuter les plugins python)


Créer un sous-repertoire dans le répertoire plugins de domoticz et y déposer le fichier plugin.py
Relancer domoticz


Dans Réglages>Matériel, vous trouverez le matériel RfPlayer

Choisir un nom pour le plugin, 
laisser DataTimeout à Disable,
Choisir le port série utilisé (ComX pour Windows, ttyUSBx pour linux),
Choisir une Mac adresse ou laisser par defaut,
Et enfin choisir le mode Debug ou non.


Actuellement, seul les capteurs de pluie et le protocole X2D ne sont pas du tout supportés (en cours d'ajout)

Pour les interrupteurs seuls les fonctions ON et OFF sont supportés, le Dim reste a inclure



ATTENTION : Ce plugin n'est pas totalement fini, des modifications sont encore à venir pour supporter l'ensemble des fonctions du RfPlayer
