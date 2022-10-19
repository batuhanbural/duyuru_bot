import os

import discord
from discord.ext import commands
# from discord.ext import timers
from dotenv import load_dotenv
from keep_alive import keep_alive

intents = discord.Intents().all()
client = commands.Bot(command_prefix=".", intents=intents)


# client.timer_manager = timers.TimerManager(client)


@client.command()
async def load(extension):
    client.load_extension(f"cogs.{extension}")


@client.command()
async def unload(ctx, extension):
    client.unload_extension(f"cogs.{extension}")


@client.command()
async def reload(ctx, extension):
    client.unload_extension(f"cogs.{extension}")
    client.load_extension(f"cogs.{extension}")


for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        client.load_extension(f"cogs.{filename[:-3]}")

keep_alive()
load_dotenv()
client.run(os.getenv("TOKEN"))
