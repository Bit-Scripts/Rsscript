# Rsscript
## EST TOUJOURS EN COURS DE DEVELOPEMENT !!!

est un project opensource de bot discord qui à pour but de lire les flux RSS
est de les trensmetre dans un salon discord specifique


## Prérequis

- Python
- discord.py
- feedparser
- python-dotenv

## Installation
Expliquez comment installer et configurer le projet sur la machine de l'utilisateur. Utilisez le contenu de votre fichier requirements.txt :

```bash
pip install -r requirements.txt
```

## Configuration
### Configuration du Token Discord :

Créez un fichier nommé token.env à la racine du projet.

Ajoutez votre token Discord au fichier token.env de la manière suivante :


```env
TOKEN=VotreTokenDiscordIci
```

dans commmande/rss.py

à la ligne 7 " news_channel = bot.get_channel(IDCHANEL)  # Remplacer avec l'ID du salon souhaité "
remplacer IDCHANEL par id du channel ou vous souaitez que le flux rss s'affiche


## Utilisation
### Ajout de flux RSS :

Ouvrez le fichier commande/flux.json .

Ajoutez vos flux RSS avec le nom du flux en tant que clé et l'URL du flux en tant que valeur.

```json
{
    "NomDuFlux1": "URLDuFlux1",
    "NomDuFlux2": "URLDuFlux2",
    ...
}
```

exemple

```json
{
    "IT-Connect": "https://www.it-connect.fr/feed/",
    "NomDuFlux2": "URLDuFlux2"
}
```

### Démarrage du Bot :

Exécutez le fichier main.py pour démarrer le bot Discord :

```bash
python main.py
```

## Contributions
Si vous acceptez des contributions, expliquez comment les autres personnes peuvent contribuer au projet.

## Licence
Ce projet est sous licence [MIT].
