from os import listdir
from datetime import datetime
from json import load

import discord
import colorama
from discord.ext import commands
from colorama import Fore

from utils import *
from constants import TOKEN_FILE, unauthorized_embed

colorama.init()
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="fc!", intents=intents)
bot.remove_command("help")

@bot.check
def is_command_allowed(ctx):
    return is_command_authorized(ctx.author, ctx.command)

async def on_command_error(ctx, exc):
    await ctx.send(embed=unauthorized_embed)
bot.on_command_error = on_command_error

@bot.event
async def on_ready():
    print(f'{datetime.now()} - Connected as {bot.user}')

@bot.command(name="help", description="Envoie ce message", usage="help", aliases=[])
async def help_(ctx):
    embed = discord.Embed(title="Commandes",
                          description="Liste des commandes disponibles",
                          colour=discord.Colour.green())
    embed.set_footer(text=f"{bot.user.name} | Requested by {ctx.author.name}")

    for cmd in bot.commands:
        if not is_command_authorized(ctx.author, cmd) : continue

        name = f"{cmd.name.capitalize()} (``{bot.command_prefix + cmd.name}``)"
        aliases = ", ".join(cmd.aliases)
        content = f"{cmd.description}\n**Usage :**  {bot.command_prefix + cmd.usage}"
        if aliases : content += f"\n**Aliases :**  {aliases}"

        embed.add_field(name=name,
                        value=content,
                        inline=False)

    await ctx.send(embed=embed)




for filename in listdir('./cogs'):
    if filename.endswith('.py'):
        try:
            bot.load_extension(f'cogs.{filename[:-3]}')
            print(f'{Fore.GREEN}   [{filename[:-3]}] successfully loaded {Fore.WHITE}')

        except Exception as e:
            print(f'{Fore.RED}   [{filename[:-3]}] failed to load : {e}{Fore.WHITE}')


def init(botInit, token):
    token = token.strip()
    botInit.run(token)

with open(TOKEN_FILE, 'r') as f:
    tkn = load(f)['token']
    init(bot, tkn)