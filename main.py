import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

# Charger les variables d'environnement
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD_ID = os.getenv('GUILD_ID')  # Conserver comme chaîne pour flexibilité

# Vérifier que le jeton est chargé
if TOKEN is None:
    print("Le jeton Discord n'a pas été chargé. Vérifiez votre fichier .env.")
    exit(1)

# Configurer les intentions
intents = discord.Intents.default()
intents.message_content = True  # Activer l'intent du contenu des messages si nécessaire

# Initialiser le bot
bot = commands.Bot(command_prefix='!', intents=intents)
tree = bot.tree  # Pour les slash commandes

# Charger les cogs
async def load_extensions():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            try:
                await bot.load_extension(f'cogs.{filename[:-3]}')
            except Exception as e:
                print(f"Erreur lors du chargement de l'extension {filename}: {e}")

@bot.event
async def on_ready():
    await load_extensions()
    # Synchroniser les slash commandes avec le serveur
    try:
        guild = discord.Object(id=int(GUILD_ID))
        synced = await tree.sync(guild=guild)
        print(f"Commandes synchronisées : {len(synced)}")
    except Exception as e:
        print(f"Erreur lors de la synchronisation des commandes : {e}")
    print(f'Connecté en tant que {bot.user}')

if __name__ == '__main__':
    bot.run(TOKEN)
