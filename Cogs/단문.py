import re
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

short_script = {}


async def get_member_list(members: list):
    user_list = ""
    for idx, member in zip(range(1, len(members) + 1), members):
        user_list += f"{idx}. {member}\n"
    if user_list == "":
        user_list = "없음"
    return user_list


class 단문(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="단문예약", description="예약목록을 만들고, 단문 연기를 시작합니다.")
    async def 단문예약(self, interaction: Interaction):
        if short_script.get(str(interaction.channel.id)) == None:
            short_script[str(interaction.channel.id)] = {
                "channel": interaction.channel,
                "last_member": interaction.user.mention,
                "members": [],
                "last_time": datetime.datetime.now()
            }
            await interaction.response.send_message(f"< {interaction.user.mention} > 님이 예약목록을 만들고, 연기를 시작하셨습니다.")
        else:
            if interaction.user.mention in short_script[str(interaction.channel.id)]["members"] or interaction.user.mention in short_script[str(interaction.channel.id)]["last_member"]:
                embed = discord.Embed(
                    title="중복 경고", description=f"< {interaction.user.mention} > 님은 이미 목록에 있습니다.", color=discord.Color(0xFF0000))

                embed.add_field(
                    name="현재 인원", value=short_script[str(interaction.channel.id)]["last_member"], inline=False)

                embed.add_field(name="예약목록", value=await get_member_list(short_script[str(interaction.channel.id)]["members"]), inline=False)

                await interaction.response.send_message(embed=embed)
            else:
                short_script[str(interaction.channel.id)]["members"].append(
                    interaction.user.mention)
                embed = discord.Embed(
                    title="예약 완료", description=f"< {interaction.user.mention} > 님이 예약목록에 추가되었습니다.", color=discord.Color(0x00FF00))
                embed.add_field(
                    name="현재 인원", value=short_script[str(interaction.channel.id)]["last_member"], inline=False)
                embed.add_field(name="예약목록", value=await get_member_list(short_script[str(interaction.channel.id)]["members"]), inline=False)
                await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(
        단문(bot),
        guilds=[Object(id=config['GUILD_ID'])]
    )
