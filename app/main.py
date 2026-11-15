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
g = game.Game(db="./players.db", playerCount=20)
g.import_resources()
g.setup_player_positions()

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
@app_commands.describe(direction="Direction UP, DOWN, LEFT, RIGHT")
async def move(interaction, direction: str) -> None:
    result = g.cursor.execute("SELECT current_x, current_y FROM playerlist WHERE discord_uid = ?;", (interaction.user.id,))
    start_pos = result.fetchone()
    pos = g.update_position(start_pos, direction)
    if not pos == None:
        g.cursor.execute("UPDATE playerlist SET current_x = ?, current_y = ? WHERE discord_uid = ?;", pos+(interaction.user.id,))
        embed = discord.Embed()
        embed.colour = discord.Colour.blue()
        embed.title = f"Move '{direction}' made!"
        await interaction.response.send_message(embed=embed, ephemeral=True)
    else:
        embed = discord.Embed()
        embed.colour = discord.Colour.red()
        embed.title = f"Move '{direction}' invalid!"
        await interaction.response.send_message(embed=embed, ephemeral=True)


load_dotenv()
token = getenv("DISCORD_TOKEN")
client.run(token)

