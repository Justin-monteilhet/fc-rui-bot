from discord.ext import commands
from discord import Embed, Color

from utils import *
from constants import PLANNING_DOC_ID, PLANNING_DOC_URL
from sheets import ChapterData, SheetData

class Staff(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name='planning',
                      usage='planning (chapitre)',
                      description="Obtenez le lien du planning ou l'avancée sur un chapitre.",
                      aliases=['doc', 'gdoc'],
                      permission_level='fcrui')
    async def planning(self, ctx, chap:str=None):
        if not chap :
            emb = Embed(title = "FCRui - Planning",
                        description = f"[Google doc]({PLANNING_DOC_URL})",
                        color = Color.green())
            await ctx.send(embed=emb)
            return
        
        chap_data = SheetData.from_id(PLANNING_DOC_ID).get_chapter_data(chap)
        if not chap_data:
            emb = make_error_embed(f"Le chapitre {chap} n'existe pas sur le google doc.")
            await ctx.send(embed=emb)
            return
        
        print(chap_data)
        # send loading message to update when data found
        # format embed of the chapter's tasks
        



def setup(client):
    client.add_cog(Staff(client))
