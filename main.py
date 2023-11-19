import discord
from discord.ext import commands
import asyncio
from dotenv import load_dotenv
import os
from commande import rss

# Charger les variables d'environnement à partir du fichier token.env
load_dotenv("token.env")

# Récupérer le token à partir des variables d'environnement
TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.typing = False
intents.presences = False
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f"Connecté en tant que {bot.user.name}")
    bot.loop.create_task(rss.display_news(bot))  # Passer l'objet bot comme paramètre

bot.run(TOKEN)
