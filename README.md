# Rsscript
## EST TOUJOURS EN COURS DE DEVELOPEMENT !!!

est un project opensource de bot discord qui à pour but de lire les flux RSS
est de les trensmetre dans un salon discord specifique


## Fonctionnalités

- **Ajouter** des flux RSS à suivre.
- **Supprimer** des flux RSS suivis.
- **Lister** tous les flux RSS suivis.
- **Forcer** la vérification des flux RSS pour les nouveaux articles.
- Envoi automatique des nouveaux articles dans un salon Discord spécifique.

## Prérequis

- **Python 3.8** ou supérieur.
- Un compte Discord avec les permissions pour créer un bot.
- Un serveur Discord où vous avez les permissions d'administrateur.

## Installation

### 1. Cloner le dépôt

```bash
git clone https://github.com/votre-utilisateur/votre-repo.git
cd votre-repo
```

# 2. Créer un environnement virtuel
Il est recommandé d'utiliser un environnement virtuel pour isoler les dépendances du projet.

# Sous Windows
```bash
python -m venv venv
venv\Scripts\activate
```

# Sous macOS/Linux
```bash
python3 -m venv venv
source venv/bin/activate
```

# 3. Installer les dépendances
Assurez-vous que l'environnement virtuel est activé, puis exécutez :

```bash
pip install -r requirements.txt
```

# 4. Configuration
Créez un fichier `.env` à la racine du projet avec les variables suivantes :
```env
DISCORD_TOKEN=VotreTokenDiscord
GUILD_ID=VotreGuildID
CHANNEL_ID=VotreChannelID
DEFAULT_IMAGE_URL=URLDeLImageParDéfaut (optionnel)
```

- **DISCORD_TOKEN :** Le token de votre bot Discord.
- **GUILD_ID :** L'ID du serveur Discord où le bot sera utilisé.
- **CHANNEL_ID :** L'ID du salon Discord où les articles seront envoyés.
- **DEFAULT_IMAGE_URL :** (Optionnel) URL d'une image par défaut si aucun média n'est trouvé dans l'article.

# 5. Démarrer le bot
Assurez-vous que votre environnement virtuel est activé et lancez le bot :
```bash
python main.py
```
## Utilisation

### Commandes Slash disponibles

Le bot utilise des commandes slash pour interagir. Voici la liste des commandes disponibles et comment les utiliser :

#### 1. `/add_feed`

- **Description** : Ajouter un flux RSS à suivre. - **Paramètres** : - `url` : L'URL du flux RSS à ajouter. - **Exemple** :

``` /add_feed url=https://exemple.com/rss ```

#### 2. `/remove_feed`

- **Description** : Supprimer un flux RSS suivi. - **Paramètres** : - `url` : L'URL du flux RSS à supprimer. - **Exemple** :

``` /remove_feed url=https://exemple.com/rss ```

#### 3. `/list_feeds`

- **Description** : Lister tous les flux RSS actuellement suivis. - **Exemple** :

``` /list_feeds ```

#### 4. `/force_check`

- **Description** : Forcer la vérification immédiate des flux RSS pour de nouveaux articles. - **Exemple** :

``` /force_check ```

### Notes Importantes

- Les commandes sont généralement accessibles aux utilisateurs ayant les permissions nécessaires (administrateur recommandé). - Les nouveaux articles sont vérifiés toutes les 5 minutes automatiquement. - Le bot évite d'envoyer des doublons grâce à une base de données SQLite qui stocke les liens déjà envoyés.

## Exemple de Flux RSS

Pour tester le bot, vous pouvez utiliser des flux RSS publics tels que :

- `https://www.lemonde.fr/rss/une.xml\` - `https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml\`

## Contribution

Les contributions sont les bienvenues ! Si vous trouvez un bug ou souhaitez proposer une amélioration, n'hésitez pas à ouvrir une issue ou une pull request.

## Licence
Ce projet est sous licence [MIT].
