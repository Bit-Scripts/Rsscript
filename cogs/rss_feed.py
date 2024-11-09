from discord.ext import commands, tasks
import discord
from discord import app_commands
import feedparser
import sqlite3
import os
from dotenv import load_dotenv
import html
from bs4 import BeautifulSoup

# Charger les variables d'environnement
load_dotenv()
CHANNEL_ID = int(os.getenv('CHANNEL_ID'))
GUILD_ID = int(os.getenv('GUILD_ID'))
DEFAULT_IMAGE_URL = os.getenv('DEFAULT_IMAGE_URL')  # Nouvelle variable pour l'image par défaut

class RSSFeed(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.conn = sqlite3.connect('rss_links.db')
        self.create_tables()
        self.check_feed.start()

    def create_tables(self):
        cursor = self.conn.cursor()
        # Table pour les liens déjà envoyés
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS links (
                link TEXT PRIMARY KEY
            )
        ''')
        # Table pour les flux RSS suivis
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS feeds (
                url TEXT PRIMARY KEY
            )
        ''')
        self.conn.commit()

    def is_new_link(self, link):
        cursor = self.conn.cursor()
        cursor.execute('SELECT link FROM links WHERE link = ?', (link,))
        result = cursor.fetchone()
        if result:
            return False
        else:
            cursor.execute('INSERT INTO links (link) VALUES (?)', (link,))
            self.conn.commit()
            return True

    def get_feeds(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT url FROM feeds')
        feeds = cursor.fetchall()
        return [feed[0] for feed in feeds]

    def add_feed(self, url):
        cursor = self.conn.cursor()
        try:
            cursor.execute('INSERT INTO feeds (url) VALUES (?)', (url,))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def remove_feed(self, url):
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM feeds WHERE url = ?', (url,))
        self.conn.commit()
        return cursor.rowcount > 0

    @tasks.loop(minutes=5.0)
    async def check_feed(self):
        await self.bot.wait_until_ready()
        channel = self.bot.get_channel(CHANNEL_ID)
        if channel is None:
            print(f"Le salon avec l'ID {CHANNEL_ID} est introuvable.")
            return

        feeds = self.get_feeds()
        if not feeds:
            return

        for feed_url in feeds:
            feed = feedparser.parse(feed_url)
            for entry in reversed(feed.entries):
                if self.is_new_link(entry.link):
                    # Nettoyer le titre
                    title = entry.title if 'title' in entry else 'Sans titre'
                    title = html.unescape(title)

                    # Nettoyer la description
                    if 'summary' in entry:
                        soup = BeautifulSoup(entry.summary, 'html.parser')
                        description = soup.get_text()
                        description = html.unescape(description)
                        # Limiter la longueur de la description
                        max_description_length = 2048  # Limite pour Discord
                        if len(description) > max_description_length:
                            description = description[:max_description_length - 3] + '...'
                    else:
                        description = ''

                    # Créer l'embed avec le contenu nettoyé
                    embed = discord.Embed(
                        title=title,
                        url=entry.link,
                        description=description,
                        color=0x00ff00
                    )

                    # Nettoyer et ajouter l'auteur si présent
                    if 'author' in entry:
                        author = html.unescape(entry.author)
                        embed.set_author(name=author)

                    # Ajouter la date de publication si présente
                    if 'published' in entry:
                        embed.set_footer(text=entry.published)

                    # Essayer de récupérer l'image
                    image_url = None

                    # 1. Vérifier 'media_content'
                    if 'media_content' in entry:
                        media = entry.media_content[0]
                        if 'url' in media:
                            image_url = media['url']

                    # 2. Vérifier 'enclosures'
                    elif 'enclosures' in entry and len(entry.enclosures) > 0:
                        image_url = entry.enclosures[0].get('href', None)

                    # 3. Extraire la première image du contenu HTML dans 'content:encoded'
                    elif 'content' in entry:
                        # 'content' est une liste de dicts avec 'value' clé
                        for content in entry.content:
                            if 'value' in content:
                                soup = BeautifulSoup(content.value, 'html.parser')
                                img_tag = soup.find('img')
                                if img_tag and 'src' in img_tag.attrs:
                                    image_url = img_tag['src']
                                    break  # Utiliser la première image trouvée

                    # 4. Extraire la première image du contenu HTML dans 'summary'
                    elif 'summary' in entry:
                        soup = BeautifulSoup(entry.summary, 'html.parser')
                        img_tag = soup.find('img')
                        if img_tag and 'src' in img_tag.attrs:
                            image_url = img_tag['src']

                    # Si une image a été trouvée, l'ajouter à l'embed
                    if image_url:
                        embed.set_image(url=image_url)
                    elif DEFAULT_IMAGE_URL:
                        embed.set_image(url=DEFAULT_IMAGE_URL)

                    await channel.send(embed=embed)

    @check_feed.before_loop
    async def before_check_feed(self):
        await self.bot.wait_until_ready()

    def cog_unload(self):
        self.conn.close()
        self.check_feed.cancel()

    # Slash Commands

    @app_commands.command(name='add_feed', description='Ajouter un flux RSS.')
    @app_commands.describe(url='URL du flux RSS à ajouter')
    async def add_feed_command(self, interaction: discord.Interaction, url: str):
        if self.add_feed(url):
            await interaction.response.send_message(f'Flux RSS ajouté : {url}', ephemeral=True)
        else:
            await interaction.response.send_message('Ce flux RSS est déjà suivi.', ephemeral=True)

    @app_commands.command(name='remove_feed', description='Supprimer un flux RSS.')
    @app_commands.describe(url='URL du flux RSS à supprimer')
    async def remove_feed_command(self, interaction: discord.Interaction, url: str):
        if self.remove_feed(url):
            await interaction.response.send_message(f'Flux RSS supprimé : {url}', ephemeral=True)
        else:
            await interaction.response.send_message('Ce flux RSS ne fait pas partie des flux suivis.', ephemeral=True)

    @app_commands.command(name='list_feeds', description='Lister les flux RSS suivis.')
    async def list_feeds_command(self, interaction: discord.Interaction):
        feeds = self.get_feeds()
        if feeds:
            message = "**Flux RSS suivis :**\n" + "\n".join(f"- {feed}" for feed in feeds)
        else:
            message = "Aucun flux RSS n'est actuellement suivi."
        await interaction.response.send_message(message, ephemeral=True)

    @app_commands.command(name='force_check', description='Forcer la vérification des flux RSS.')
    async def force_check_command(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)  # Différer la réponse
        try:
            await self.check_feed()
            await interaction.followup.send('Vérification des flux RSS terminée.', ephemeral=True)  # Envoyer le message final
        except Exception as e:
            await interaction.followup.send('Une erreur est survenue lors de la vérification des flux RSS.', ephemeral=True)
            print(f"Erreur lors de la vérification des flux RSS : {e}")

    @commands.Cog.listener()
    async def on_ready(self):
        # Synchroniser les commandes
        guild = discord.Object(id=GUILD_ID)
        self.bot.tree.add_command(self.add_feed_command, guild=guild)
        self.bot.tree.add_command(self.remove_feed_command, guild=guild)
        self.bot.tree.add_command(self.list_feeds_command, guild=guild)
        self.bot.tree.add_command(self.force_check_command, guild=guild)

    async def cog_load(self):
        guild = discord.Object(id=GUILD_ID)
        self.bot.tree.add_command(self.add_feed_command, guild=guild)
        self.bot.tree.add_command(self.remove_feed_command, guild=guild)
        self.bot.tree.add_command(self.list_feeds_command, guild=guild)
        self.bot.tree.add_command(self.force_check_command, guild=guild)

    async def cog_unload(self):
        guild = discord.Object(id=GUILD_ID)
        self.bot.tree.remove_command(self.add_feed_command.name, guild=guild)
        self.bot.tree.remove_command(self.remove_feed_command.name, guild=guild)
        self.bot.tree.remove_command(self.list_feeds_command.name, guild=guild)
        self.bot.tree.remove_command(self.force_check_command.name, guild=guild)

async def setup(bot):
    await bot.add_cog(RSSFeed(bot))
