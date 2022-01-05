from discord.ext import commands, tasks
from discord import Embed, Color, Game, Status

from utils import *

class Info(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_ready(self):
        self.update_activity.start()

    @commands.command(name='read',
                      usage='read <numéro du chapitre>',
                      description="Obtenez le lien du chapitre demandé.",
                      aliases=['chapter', 'rd'],
                      permission_level='member')
    async def read(self, ctx, number:int):
        last_chapter_number = get_last_chapter_data()['attributes']['chapter']
        if number > int(last_chapter_number):
            emb = Embed(title="Numéro incorrect",
                        description="Ce chapitre n'est pas encore sorti en VF sur Mangadex.",
                        color=Color.red())
            await ctx.send(embed=emb)
            return

        urls = {"japscan" : f"https://www.japscan.ws/lecture-en-ligne/domestic-na-kanojo/{number}/"}
        emb_desc = "Achetez la version physique chez [Delcourt Tonkam](https://www.editions-delcourt.fr/mangas/series/serie-love-x-dilemma)"
        if number >= 155:
            mangadex_id = get_mangadex_id(str(number))
            urls = {
                'japanread' : f"https://www.japanread.cc/manga/domestic-na-kanojo/{number}",
                'mangadex' : f"https://mangadex.org/chapter/{mangadex_id}"
            }
        else :
            emb_desc += "\nLes chapitres précédant le 155 sont traduits par la [PervTeam](https://pervteam.wordpress.com)"

        emb = Embed(title=f"Scan VF chapitre {number}",
                    description=emb_desc,
                    color=Color.dark_magenta())
        emb.set_footer(text=f"{self.client.user.name} | Requested by {ctx.author.name}")

        for site, url in urls.items():
            emb.add_field(name=site.capitalize(), value=f"[Lire le chapitre]({url})", inline=False)

        await ctx.send(embed=emb)

    @commands.command(name='lastchapter',
                      usage='lastchapter',
                      description="Obtenez le lien vers le dernier chapitre publié.",
                      aliases=['lc', 'lastchap'],
                      permission_level='member')
    async def last_chapter(self, ctx):
        data = get_last_chapter_data()
        chapter_number = data['attributes']['chapter']
        chapter_title = data['attributes']['title']
        urls = {
            "mangadex" : f"https://mangadex.org/chapter/{data['id']}",
            "japanread" : f"https://www.japanread.cc/manga/domestic-na-kanojo/{chapter_number}"
        }
        emb = Embed(title=f"Chapitre {chapter_number}",
                            description=f"Ch. {chapter_number} : {chapter_title}",
                            color=Color.gold())
        emb.set_footer(text=f"{self.client.user.name} | Requested by {ctx.author.name}")

        for site, url in urls.items():
            emb.add_field(name=site.capitalize(), value=f"[Lire le chapitre]({url})", inline=False)

        await ctx.send(embed=emb)
    
    @tasks.loop(hours=1.0)
    async def update_activity(self):
        last_chap = get_last_chapter_data()['attributes']['chapter']
        act = Game(name=f"Lisez le chapitre {last_chap} de DNK sur Mangadex et Japanread !")
        await self.client.change_presence(status=Status.idle, activity=act)

def setup(client):
    client.add_cog(Info(client))


# add someone to the team