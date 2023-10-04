Ce script permet d'exporter les matchs de son club depuis le site [FBI](https://extranet.ffbb.com/fbi/) de la Fédération Française de Basketball et de les importer dans le logiciel [Kalisport](https://www.kalisport.com).

Ce script Python utilise Selenium pour piloter le navigateur Chromium et simuler les actions de l'utilisateur pour réaliser les opérations d'export/import automatiquement.

Le fichier Dockerfile permet de générer une image Docker avec toutes les dépendances nécessaires pour lancer le script.
Il est nécessaire de passer en argument du script/conteneur Docker les identifiants de connexion FBI et Kalisport.

Exemple :
```
# Génération de l'image Docker
docker build -t basket .
# Lancement d'un conteneur Docker pour réaliser l'export FBI et l'import Kalisport
docker run -it --rm basket username_fbi password_fbi url_kali username_kali password_kali
```

Le compte FBI nécessite un profil du type 'Association - Engagement', 'Association' ou 'Association - Compétitions' pour accéder au fichier.
Le compte Kalisport nécessite un profil permettant d'accéder à l'interface d'administration pour importer des matchs.
Le paramètre "url_kali" est l'adresse du type https://mon-club.kalisport.com
