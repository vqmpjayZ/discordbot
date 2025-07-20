TOKEN = os.environ['DISCORD_TOKEN']
TARGET_CHANNEL_ID = 1270301984897110148  # 1389210900489044048
DELAY_SECONDS = 5

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

recent_boosts = {}
pending_tasks = {}

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

async def send_good_boy_after_delay(user_id, channel):
    await asyncio.sleep(DELAY_SECONDS)
    if user_id in recent_boosts:
        await channel.send(f"<@{user_id}> good boy")
        recent_boosts.pop(user_id, None)
        pending_tasks.pop(user_id, None)

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.channel.id == TARGET_CHANNEL_ID:
        if message.content.startswith("someone just Boosted the server"):
            user_id = message.author.id

            recent_boosts[user_id] = True

            if user_id in pending_tasks:
                pending_tasks[user_id].cancel()

            pending_tasks[user_id] = bot.loop.create_task(send_good_boy_after_delay(user_id, message.channel))

    await bot.process_commands(message)

bot.run(TOKEN)
