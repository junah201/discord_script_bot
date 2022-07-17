import discord
from discord import app_commands
from discord.ext import commands
from discord import Interaction
from discord import Object

import json
import os
import datetime

with open(f"config.json", "r", encoding="utf-8-sig") as json_file:
    config = json.load(json_file)


class 유저(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="유저평가")
    async def 유저평가(self, interaction: Interaction, 유저: str):
        with open(f"./DB/User/users.json", "r", encoding="utf-8-sig") as json_file:
            users_data = json.load(json_file)

        if users_data.get(str(interaction.user.id)) != None:
            if users_data[str(interaction.user.id)]['last_evaluate'] == datetime.datetime.now().strftime("%Y-%m-%d"):
                await interaction.response.send_message(f"{interaction.user.mention} 오늘은 이미 평가하셨습니다.", ephemeral=True)
                return
            users_data[str(interaction.user.id)]["last_evaluate"] = datetime.datetime.now(
            ).strftime("%Y-%m-%d")
        else:
            users_data[str(interaction.user.id)] = {
                "name": interaction.user.name,
                "grade": 0,
                "last_evaluate": datetime.datetime.now().strftime("%Y-%m-%d"),
                "review": {},
                "warning": 0
            }

        user = await self.bot.fetch_user(유저[3:-1])
        if users_data.get(str(user.id)) == None:
            users_data[str(user.id)] = {
                "name": interaction.user.name,
                "grade": 0,
                "last_evaluate": "미평가",
                "review": {},
                "warning": 0
            }

        users_data[str(user.id)]['grade'] += 1

        with open(f"./DB/User/users.json", "w", encoding="utf-8-sig") as json_file:
            json.dump(users_data, json_file, indent=4)

        await interaction.response.send_message(f"{user.mention}님의 평가가 완료되었습니다.", ephemeral=True)

        try:
            channel = await self.bot.fetch_channel(config['LOG_CHANNEL'])
            await channel.send(f"`{interaction.user.name}({interaction.user.id})`님이 `{user.name}({user.id})`님을 평가하여 점수가 `{users_data[str(user.id)]['grade']}`로 변화하였습니다. `({datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')})`")
        except Exception as e:
            print("error 발생")
            print(e)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(
        유저(bot),
        guilds=[Object(id=config['GUILD_ID'])]
    )
