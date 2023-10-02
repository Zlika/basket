Ce script permet d'exporter les matchs de son club depuis le site FBI de la Fédération Française de Basketball
et de les importer dans le logiciel Kalisport.

Ce script Python utilise Selenium pour piloter le navigateur Chrome/Chromium et simuler les actions de l'utilisateur
pour réaliser les opérations d'export/import automatiquement.

Le fichier Dockerfile permet de générer une image Docker avec toutes les dépendances nécessaires pour lancer le script.
Il est nécessaire de passer en argument du script/conteneur Docker les identifiants de connexion FBI et Kalisport.

Exemple :
```
# Génération de l'image Docker
docker build -t basket .
# Lancement d'un conteneur Docker pour réaliser l'export FBI et l'import Kalisport
docker run -it --rm basket username_fbi password_fbi username_kali password_kali
```

