import discord
from discord import app_commands
from discord.ext import commands
from discord import Interaction
from discord import Object

import json
import os
import datetime
import random

with open(f"config.json", "r", encoding="utf-8-sig") as json_file:
    config = json.load(json_file)


class 유틸(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="뽑기", description="배역을 뽑아줍니다. (유저 칸에는 인물들의 이름을 띄어쓰기로 나누어서 넣어주세요.)")
    async def 뽑기(self, interaction: Interaction, 유저: str):
        embed = discord.Embed(
            title='⠀⠀⠀⠀〔⠀⠀⠀🥇 제비 뽑기⠀⠀⠀〕',
            description='연기자에게 랜덤하게 번호를 부여합니다.',
            color=discord.Color(0xFFFF00)

        )
        embed.set_thumbnail(
            url="https://cdn.discordapp.com/attachments/827931592932065332/841197513561735168/6979bf056826de22.png")
        embed.set_image(
            url="https://media.discordapp.net/attachments/424831572861124619/549533764880171018/da41590cda439e68.gif")

        users = 유저.split()

        random_num = [i for i in range(1, len(users) + 1, 1)]
        random.shuffle(random_num)

        for user, num in zip(users, random_num):
            embed.add_field(name=f"\t\t\t\t**⠀⠀⠀⠀⠀⠀《⠀⠀⠀⠀⠀{user}⠀⠀⠀⠀⠀》**",
                            value=f"*{user}* 님은 : ||[⠀⠀⠀⠀⠀{num}⠀⠀⠀⠀⠀]||      번 입니다.", inline=False)

        await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(
        유틸(bot),
        guilds=[Object(id=config['GUILD_ID'])]
    )
