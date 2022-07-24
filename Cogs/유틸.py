import discord
from discord import app_commands
from discord.ext import commands
from discord import Interaction
from discord import Object
import asyncio

import json
import os
import datetime
import random


with open(f"config.json", "r", encoding="utf-8-sig") as json_file:
    config = json.load(json_file)


def is_reading_channel(channel_id: int) -> bool:
    if channel_id in config["READING_CHANNEL_ID"]:
        return False
    return True


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
            url="https://i.imgur.com/xLNYJF0.png")

        users = 유저.split()

        random_num = [i for i in range(1, len(users) + 1, 1)]
        random.shuffle(random_num)

        for user, num in zip(users, random_num):
            embed.add_field(name=f"\t\t\t\t**⠀⠀⠀⠀⠀⠀《⠀⠀⠀⠀⠀{user}⠀⠀⠀⠀⠀》**",
                            value=f"*{user}* 님은 : ||[⠀⠀⠀⠀⠀{num}⠀⠀⠀⠀⠀]||     번 입니다.", inline=False)

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="준비", description="예약된 시간 후에 모두에게 멘션을 줍니다.")
    async def 준비(self, interaction: Interaction, 초: int, 맨션: str = ""):
        if is_reading_channel(interaction.channel.category.id):
            await interaction.response.send_message(f"리딩 채널 밖에선 사용 할 수 없는 명령어 입니다.")
            return

        embed = discord.Embed(
            title='⠀⠀⠀⠀〔⠀⠀⠀🥇 준비⠀⠀⠀〕',
            description='정한 시간을 정했습니다..',
            color=discord.Color(0xFFFF00)
        )

        embed.set_thumbnail(
            url="https://cdn.discordapp.com/attachments/827931592932065332/841197513561735168/6979bf056826de22.png")
        embed.set_image(
            url="https://i.imgur.com/xLNYJF0.png")

        embed = discord.Embed(
            title="리딩이 예약 되었습니다.", description=f"{초}초 후에 대본 리딩이 시작됩니다.", timestamp=datetime.datetime.now(), color=0xFFFF00)

        embed_time = discord.Embed(
            title="< 예약된 알림 >", description=f"잠시 후 대본 리딩이 시작 됩니다.", timestamp=datetime.datetime.now(), color=0xFFFF00)
        embed_time.add_field(
            name="< 리딩 에티켓 >", value="```1. 과한 애드립은 삼가주세요.``````2. 자기 차례를 필히 준수해 주세요.``````3. 역할 찾기 : F3 또는 컨트롤+F```", inline=False)
        embed_time.set_thumbnail(
            url="https://cdn.discordapp.com/attachments/827931592932065332/841197513561735168/6979bf056826de22.png")
        embed_time.set_image(
            url="https://i.imgur.com/IO3jvcq.gif")

        await interaction.response.send_message(embed=embed)

        await asyncio.sleep(초)
        if not 맨션:
            await interaction.channel.send(f"> {초}초가 경과 했습니다. <@&{config['ACTOR_ROLE_ID']}>", embed=embed_time)
        else:
            await interaction.channel.send(f"> {초}초가 경과 했습니다.", embed=embed_time)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(
        유틸(bot),
        guilds=[Object(id=config['GUILD_ID'])]
    )
