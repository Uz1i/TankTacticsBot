import discord
from discord import app_commands
from dotenv import load_dotenv
from os import getenv
import game

GUILD = discord.Object(id=1571176494397657108)

class Bot(discord.Client):
    def __init__(self) -> None:
        intents = discord.Intents.default()
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)
    
    async def setup_hook(self) -> None:
        self.tree.copy_global_to(guild=GUILD)
        await self.tree.sync(guild=GUILD)

client = Bot()
g = game.Game(db="", playerCount=20)
g.import_resources()

@client.event
async def on_ready() -> None:
    print("Bot is ready.")

@client.tree.command()
async def ping(interaction) -> None:
    embed = discord.Embed()
    embed.colour = discord.Colour.green()
    embed.title = "Ping stats."
    embed.description = f"Bot latency: `{round(client.latency * 1000, 1)}ms`"
    await interaction.response.send_message(embed=embed)
    print("Running ping command.")

@client.tree.command()
async def showmaptest(interaction) -> None: 
    print("Running map test...", end="\r")
    g.render_grid()
    embed = discord.Embed()
    file = discord.File("./map.png", filename="map.png")
    embed.set_image(url="attachment://map.png")
    await interaction.response.send_message(file=file, embed=embed)
    print("Map test has run successfully!")

@client.tree.command()
async def move(interaction) -> None:
    print("Move being made.")
    embed = discord.Embed()
    embed.colour = discord.Colour.blue()
    embed.title = "Move: cool embed"
    embed.description = "Pretty cool embed huh, wish it actually worked, maybe tmrw or smth\nin sha allah"
    await interaction.response.send_message(embed=embed)

load_dotenv()
token = getenv("DISCORD_TOKEN")
client.run(token)

