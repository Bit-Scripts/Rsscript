import feedparser
import asyncio
import json

async def display_news(bot):
    await bot.wait_until_ready()
    news_channel = bot.get_channel(IDCHANEL)  # Remplacer avec l'ID du salon souhaité

    # Charger la liste des liens des articles déjà affichés depuis le fichier JSON
    try:
        with open('commande/history.json', 'r') as history_file:
            content = history_file.read()
            if content:
                articles_affiches = set(json.loads(content))
            else:
                articles_affiches = set()
    except FileNotFoundError:
        articles_affiches = set()
    except json.JSONDecodeError:
        articles_affiches = set()

    while not bot.is_closed():
        try:
            # Charger la liste des flux RSS depuis le fichier JSON
            with open('commande/flux.json', 'r') as file:
                rss_feeds = json.load(file)

            # Actualiser les flux RSS
            for feed_name, feed_url in rss_feeds.items():
                feed = feedparser.parse(feed_url)
                for entry in feed.entries:
                    # Vérifier si le lien a déjà été affiché
                    article_link = entry.link
                    if article_link not in articles_affiches:
                        # Afficher chaque titre et lien d'article
                        article_title = entry.title
                        await news_channel.send(f"{feed_name}: {article_title}\n{article_link}")
                        # Ajouter le lien à la liste des articles affichés
                        articles_affiches.add(article_link)

            # Sauvegarder la liste des articles affichés dans le fichier JSON
            with open('commande/history.json', 'w') as history_file:
                json.dump(list(articles_affiches), history_file, indent=2)

            # Attendre 5 minutes avant la prochaine actualisation
            await asyncio.sleep(300)  # 300 secondes = 5 minutes
        except Exception as e:
            # Afficher une erreur en cas de problème avec les flux RSS
            print(f"Erreur lors de l'actualisation des flux RSS : {e}")
