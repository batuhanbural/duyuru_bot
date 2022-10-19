import discord
import asyncio
import json
from discord.ext import commands


class Register(commands.Cog):

    def __init__(self, client):
        # assign client
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        # get data from json file
        self.conf_file = open("config/guild_settings.json", "r", encoding="utf-8")
        self.config = json.load(self.conf_file)
        self.conf_file.close()

    @commands.Cog.listener()
    async def on_message(self, message):
        gid = str(message.guild.id)
        mc = self.client.get_channel(self.config[gid]["channel_data"]["main_channel"])
        dc = self.client.get_channel(self.config[gid]["channel_data"]["data_channel"])
        if message.channel == mc and not message.content.startswith("."):
            params: dict = self.config[gid]["sign_up_data"]
            lines = message.content.split("\n")

            index = 0
            user_data = []
            isTrue = 1

            for line in lines:
                data = line.split(":")
                req = data[0].lower().strip().replace("̇l", "l")

                try:
                    get = data[1].lower().strip()
                except IndexError:
                    get = ""

                if req == params[f"{index}"] and (len(get) >= 1):
                    user_data.append(data[1])
                else:
                    isTrue = 0
                index += 1

            br = discord.utils.find(lambda r: r.name == self.config[gid]["role_data"]["bot_role"], message.guild.roles)
            mr = discord.utils.find(lambda r: r.name == self.config[gid]["role_data"]["member_role"],
                                    message.guild.roles)

            if message.author.top_role != br:
                if (len(user_data) == len(params)) and isTrue == 1:
                    ds = f"{message.author.mention} Sunucuya kayıt oldu!\nKullanıcı Bilgileri:\n"
                    for key, val in enumerate(user_data):
                        ds += f"{params[str(key)].capitalize()}: {val.capitalize()}\n"
                    await dc.send(ds)

                    cm = await mc.send("Başarı ile kaydoldunuz. Hoşgeldiniz! "
                                       ":partying_face: ")
                    await message.author.add_roles(mr)

                    await asyncio.sleep(5)
                    await message.delete()
                    await cm.delete()
                else:
                    em = await mc.send("Lütfen bilgilerinizi doğru formatta giriniz! :no_entry_sign: ")
                    await asyncio.sleep(5)
                    await message.delete()
                    await em.delete()
        else:
            pass

    @commands.command(aliases=["sr"])
    async def set_register(self, ctx, fields=None, reg_ch: discord.TextChannel = None,
                           data_ch: discord.TextChannel = None, br: discord.Role = None, mr: discord.Role = None):
        if fields is None:
            fields = ["ad", "soyad", "okul"]
        else:
            fields = fields.split(",")
        if mr is None:
            await ctx.send(f"{ctx.prefix}sr alan1,alan2,alan3,alan4,... #kayıt-kanalı #data-kanalı @bot-rolü "
                           f"@yeni_üye_rolü şeklinde ayarlamanız gerekmektedir.")

        else:
            fields = dict(enumerate(fields))
            self.config[f"{ctx.guild.id}"] = {
                "sign_up_data": fields,
                "channel_data": {
                    "main_channel": reg_ch.id,
                    "data_channel": data_ch.id
                },
                "role_data": {
                    "bot_role": br.name,
                    "member_role": mr.name
                }
            }

            config = open("config/guild_settings.json", "w", encoding="utf-8")
            json.dump(self.config, config, ensure_ascii=False)
            config.close()

            await ctx.send(f"Lütfen '{ctx.prefix}reload register' yazın :)")


def setup(client):
    client.add_cog(Register(client))
# main
