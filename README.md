# ScrapPy

*- English version after the screenshots -*

First python project

TP3 réalisé avec [skoll09](https://github.com/skoll09/ScrapPy)

## Réalisé :
Base requise :
- création de l'environnement virtuel avec virtualenv
- installation des packages requests et BeautifulSoup
- scrap de la page [https://www.frameip.com/liste-des-ports-tcp-udp/]
- scrap des pages liées (listes des ports)
- exports en fichiers json
- publication sur github

## Plus :
- export en fichiers csv
- gestion connecté/déconnecté
- affichage des headers
- affichage des cookies
- création de fonctions
- gestion des exceptions
- transformation en module et appel de celui-ci dans le main.py
- ajout d'une interface graphique (DearPyGui)
- ajout de contrôles :
  - texte
  - checkbox (avec boutons tous/aucun)
  - lignes de séparation
  - boutons radio (csv, json, les 2)
  - boutons (test cnx, scrap, exit) avec tooltip
  - fenêtres (headers, cookies)
  - barre de progression
  - input texte
  - indicateur de chargement
- gestion du layout (avec des groupes et zones fixes)
- modification du thème
- affichage des cookies de n'importe quel site
- vérification (regex) de l'url saisie par l'utilisateur
- ajout d'un easter-egg
- export du projet en exe (avec auto-py-to-exe en mode 1 fichier)
- ajout d'un fichier requirements.txt pour faciliter l'installation de l'environnement
(auto-py-to-exe non inclut)
- ajout de la possibilité d'exporter dans 1 seul fichier si toutes les pages sont sélectionnée

## Captures

![capture exe](/captures/scrappy.png "capture exe") 


![capture exe deco](/captures/scrappy_no_cnx.png "capture exe deco")

 
# English version:

**User interface in french only**

## Done:
The basic requirements:
- requests and BeautifulSoup packages install
- scrap of the page [https://www.frameip.com/liste-des-ports-tcp-udp/]
- scrap of linked pages (ports list)
- export to json files
- publication to github

## More :
- virtualenv initialized
- export to csv files
- connected/disconnected management
- display of headers
- display of cookies
- functions creation
- exception handling
- main code extracted into a module called from main.py
- added a graphical user interface (DearPyGui)
- added controls :
  - text
  - checkbox (with all/no buttons)
  - separator lines
  - radio buttons (csv, json, both)
  - buttons (test cnx, scrap, exit) with tooltip
  - windows (headers, cookies)
  - progress bar
  - text input
  - loading indicator
- layout management (with groups and fixed zones)
- theme modification
- display of cookies from any website
- verification (regex) of the user entered url
- add an easter-egg
- exported project to exe (with auto-py-to-exe in 1 file mode)
- Requirements.txt added for easy dev environment config (auto-py-to-exe not include)
- added ability to export in 1 file if all webpages selected
