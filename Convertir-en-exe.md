# Convertir le projet ScrapPy en .exe

Nous avons utilisé le module [auto-py-to-exe](https://pypi.org/project/auto-py-to-exe/) pour créer un exécutable.

Cependant, il semble que certains antivirus détectent cet exe et rapportent une alerte bloquant le programme.

Pour éviter toute alerte, il suffit de faire la conversion sur votre machine.

La procédure est simple, il suffit de suivre les quelques instructions ci-dessous.

### 1 - Préparation

Pour ne pas polluer l'environnement global, il est *fortement recommandé* d'avoir au préalable
créé un environnement virtuel pour le projet (pyCharm le fait automatiquement quand on charge le projet
et qu'on lui crée ou affecte une configuration).

Donc, pour créer l'environnement virtuel et s'y connecter, si ce n'est pas déjà fait, dans un terminal à la racine du projet :
```
virtualenv venv
venv\Scripts\activate.bat
```
Le prompt du terminal doit monter (venv) en début de ligne.

- Importer le module easy-py-to-exe dans le projet

Pour cela une simple commande à passer dans le terminal :
```
pip install auto-py-to-exe
```
Valider les éventuelles demandes et exécuter :
```
auto-py-to-exe
```
La fenêtre de l'outil s'ouvre. 

### 2 - Configuration

*Vous pouvez mettre l'interface en français en haut à droite.*

Commencer par charger les options spécifiques au projet en cliquant **"Paramètres"** en bas de la fenêtre. 
Dans la section qui se déplie, sous "Paramétrage", cliquer le bouton Importation [...] JSON et sélectionner 
le fichier `config_exe.json` dans le dossier du projet. 

Il ne reste plus qu'à adapter cette configuration à votre environnement :

- Tout en haut de la fenêtre, à "Emplacement des scripts", sélectionner le fichier ``main.py`` du projet
avec le bouton "Navigateur".
- Conserver l'option "Un fichier".
- Conserver l'option "Basé sur windows (la console n'est pas visible"
- À la section **"Icone"**, indiquer le fichier d'icône ``scrappy.ico`` se trouvant 
dans le sous-dossier ``img`` du projet en cliquant sur le bouton "Navigateur".

La configuration est terminée !

### 3 - Conversion

Il ne reste plus qu'à cliquer sur le bouton tout en bas de la fenêtre
nommé ``CONVERT. .PY VERS .EXE`` pour démarrer l'opération. Si tout se déroule sans erreurs, 
un fichier ``ScrapPy.exe`` doit maintenant se trouver dans le sous-dossier ``output`` du projet accessible via le bouton 
``OUVRIR LE DOSSIER DE SORTIE``.

### 4 - Un peu plus ?

Pour obtenir une version affichant la console à l'exécution, 2 étapes :
- Choisir "Présence de la console" à la section **"Console Windows"**
- Changer l'option "name" à la section **"Paramètres avancées"** (oui, il y a une faute dans l'interface !).
Par example ``SCRAPpY_console``.
Cliquer le bouton ``EFFACER LA CONSOLE`` puis ``CONVERT. .PY VERS .EXE`` pour lancer une nouvelle conversion.

Il est aussi possible de spécifier un dossier de sortie à "Repertoire de sortie" sous la section **"Paramètres"**.

Enjoy !