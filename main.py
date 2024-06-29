import discord
import discord.ext.commands as commands
import os
from dotenv import load_dotenv
import asyncio
import schedule
from datetime import datetime

intents = discord.Intents(messages=True, message_content=True)

bot = commands.Bot(command_prefix="//", intents=discord.Intents.all())

load_dotenv()


@bot.event
async def on_ready():
    print("listoooooooooooooo")
    try:
        synced = await bot.tree.sync()
        print(f"Sincronizado {len(synced)} comand(s)")
    except Exception as e:
        print(e)
    bot.loop.create_task(time_check())


@bot.tree.command(name="birthday", description="Register the date of your birthday")
async def birthday(interaction: discord.Interaction, *, day: str, month: str) -> None:
    if int(day) > 31 or int(month) > 12:
        await interaction.response.send_message("Invalid date")
    elif len(day) != 2:
        await interaction.response.send_message("Invalid day, please use the format DD (02, 12, ...)")
    else:
        try:
            with open("database.txt", "a") as db:
                db.write(f"{interaction.user.id}/{day}/{month}\n")
            await interaction.response.send_message("Birthday registered!")
        except Exception as e:
            print(e)


@bot.tree.command(name="channel_config", description="Set the channel where the bot will send the birthday message")
async def channel_config(interaction: discord.Interaction, channel: discord.TextChannel) -> None:
    try:
        with open("channel.txt", "a") as db:
            db.write(f"{channel.id}\n")
        await interaction.response.send_message("Channel setted!")
    except Exception as e:
        print(e)


async def birthday_check():
    now = datetime.now().strftime("%d/%m")
    with open("database.txt", "r") as db:
        for line in db:
            user_id, day, month = line.strip().split('/')
            if day == now.split('/')[0] and month == now.split('/')[1]:
                user = await bot.fetch_user(int(user_id))
                await user.send(f"Happy Birthday! 🎉🎉 <@{user_id}>")
                with open("channel.txt", "r") as channeldb:
                    for channel_id in channeldb:
                        channel = bot.get_channel(int(channel_id.strip()))
                        await channel.send(f"Happy Birthday! 🎉🎉 <@{user_id}>")


async def time_check():
    while True:
        schedule.run_pending()
        await asyncio.sleep(60)


schedule.every().day.at("00:00").do(lambda: asyncio.create_task(birthday_check()))

bot.run(os.getenv("TOKEN"))
