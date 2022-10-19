import json

import discord
from discord.ext import commands, tasks
from itertools import cycle


class Basics(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.status = cycle(["Madem", "Yad Eller", "Yapma N'olursun", "Filozof", "Odamda Hayalin Saklı"])

    @commands.Cog.listener()
    async def on_ready(self):
        self.change_status.start()
        print(f"Bot is online! {self.client.user}")

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        config = open("config/guild_settings.json", "r", encoding="utf-8")
        json_conf = json.load(config)
        config.close()

        try:
            json_conf[guild.id]
        except KeyError:
            json_conf[guild.id] = {
                "sign_up_data": {
                },
                "channel_data": {
                    "main_channel": "",
                    "data_channel": ""
                },
                "role_data": {
                    "bot_role": "",
                    "member_role": ""
                }
            }

            config = open("config/guild_settings.json", "w", encoding="utf-8")
            json.dump(json_conf, config)
            config.close()

    @tasks.loop(minutes=3)
    async def change_status(self):
        await self.client.change_presence(
            activity=discord.Activity(type=discord.ActivityType.listening, name=next(self.status)))

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f"Pong! {round(self.client.latency * 1000)} ms")

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount: int = 10):
        await ctx.channel.purge(limit=amount)

    @clear.error
    async def clear_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please specify amount of messages to delete!")


def setup(client):
    client.add_cog(Basics(client))
