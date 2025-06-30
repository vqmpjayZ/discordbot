import discord
from discord.ext import commands
from collections import defaultdict
from datetime import datetime
import os

TOKEN = os.environ['DISCORD_TOKEN']
TARGET_CHANNEL_ID = 1389210900489044048
MESSAGE_WINDOW = 5

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)
recent_boosts = defaultdict(float)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.channel.id == TARGET_CHANNEL_ID:
        now = datetime.utcnow().timestamp()
        if now - recent_boosts[message.author.id] > MESSAGE_WINDOW:
            recent_boosts[message.author.id] = now
            await message.channel.send(f"{message.author.mention} good boy")

    await bot.process_commands(message)

bot.run(TOKEN)
