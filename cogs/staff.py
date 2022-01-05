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
        
        msg = await ctx.send("<a:loader:928387309538279484> Please wait...")
        
        sheet = SheetData.from_id(PLANNING_DOC_ID)
        chap_data = sheet.get_chapter_data(chap)
        if not chap_data:
            emb = make_error_embed(f"Le chapitre {chap} n'existe pas sur le google doc.")
            await msg.edit(content=None, embed=emb)
            return
        
        emb = Embed(color=Color.dark_green())
        emb.set_author(name=f"Chapitre {chap}")
        for tsk in chap_data.tasks:
            state_emote = chap_state_to_emote(tsk.state)
            worker = tsk.worker.capitalize() if tsk.worker else 'non réservé(e)'
            val = f"{state_emote} **{worker}**"
            emb.add_field(name=tsk.type.capitalize(), value=val, inline=False)

        await msg.edit(content=None, embed=emb)
   

def setup(client):
    client.add_cog(Staff(client))
