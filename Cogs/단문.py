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


def is_reading_channel(channel_id: int) -> bool:
    if channel_id in config["READING_CHANNEL_ID"]:
        return False
    return True


class 단문(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="단문예약", description="예약목록을 만들고, 단문 연기를 시작합니다.")
    async def 단문예약(self, interaction: Interaction):
        if is_reading_channel(interaction.channel.category.id):
            await interaction.response.send_message(f"리딩 채널 밖에선 사용 할 수 없는 명령어 입니다.")
            return
        if short_script.get(str(interaction.channel.id)) == None:
            short_script[str(interaction.channel.id)] = {
                "channel": interaction.channel,
                "last_member": interaction.user.mention,
                "members": [],
                "last_time": datetime.datetime.now()
            }
            embed = discord.Embed(
                title="단문 예약", description=f"< {interaction.user.mention} > 님이 예약목록을 만들고, 연기를 시작하셨습니다.", color=discord.Color(0xFFFF00))
            await interaction.response.send_message(embed=embed)
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

    @app_commands.command(name="단문스킵", description="예약목록에서 해당 유저를 스킵합니다. (유저를 선택하지 않을 경우 본인을 스킵합니다.) (유저 칸에는 유저를 맨션해주세요.)")
    async def 단문스킵(self, interaction: Interaction, 유저: str = None):
        if is_reading_channel(interaction.channel.category.id):
            await interaction.response.send_message(f"리딩 채널 밖에선 사용 할 수 없는 명령어 입니다.")
            return

        if short_script.get(str(interaction.channel.id)) == None:
            await interaction.response.send_message(f"단문예약이 시작하지 않았습니다. `/단문예약`을 사용해주세요.")
            return

        if 유저 == None:
            유저 = interaction.user.mention

        if 유저 in short_script[str(interaction.channel.id)]["members"]:
            short_script[str(interaction.channel.id)]["members"].remove(유저)
        elif 유저 == short_script[str(interaction.channel.id)]["last_member"]:
            short_script[str(interaction.channel.id)]["last_member"] = None
            if not short_script[str(interaction.channel.id)]["members"]:
                short_script.pop(str(interaction.channel.id))
                embed = discord.Embed(
                    title="단문 연기 종료", description="목록에 유저가 없음에 따라 단문 연기가 종료되었습니다.", color=discord.Color(0x00FF00))
                await interaction.response.send_message(embed=embed)
                return
            else:
                short_script[str(interaction.channel.id)]["last_member"] = short_script[str(
                    interaction.channel.id)]["members"][0]
                short_script[str(interaction.channel.id)]["members"].pop(0)
        else:
            embed = discord.Embed(
                title="없는 유저 경고", description=f"< {interaction.user.mention} > 님은 이미 목록에 있습니다.", color=discord.Color(0xFF0000))

            embed.add_field(
                name="현재 인원", value=short_script[str(interaction.channel.id)]["last_member"], inline=False)

            embed.add_field(name="예약목록", value=await get_member_list(short_script[str(interaction.channel.id)]["members"]), inline=False)

            await interaction.response.send_message(embed=embed)
            return

        embed = discord.Embed(
            title="스킵 완료", description=f"< {interaction.user.mention} > 님이 예약목록에서 스킵되었습니다.", color=discord.Color(0x00FF00))
        embed.add_field(
            name="현재 인원", value=short_script[str(interaction.channel.id)]["last_member"], inline=False)
        embed.add_field(name="예약목록", value=await get_member_list(short_script[str(interaction.channel.id)]["members"]), inline=False)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="단문다음", description="현재 연기 중인 유저를 스킵하고 다음 유저를 연기합니다.")
    async def 단문다음(self, interaction: Interaction):
        if is_reading_channel(interaction.channel.category.id):
            await interaction.response.send_message(f"리딩 채널 밖에선 사용 할 수 없는 명령어 입니다.")
            return

        if short_script.get(str(interaction.channel.id)) == None:
            await interaction.response.send_message(f"단문예약이 시작하지 않았습니다. `/단문예약`을 사용해주세요.")
            return

        short_script[str(interaction.channel.id)]["last_member"] = None

        if short_script[str(interaction.channel.id)]["members"] == []:
            short_script.pop(str(interaction.channel.id))
            embed = discord.Embed(
                title="단문 연기 종료", description="목록에 유저가 없음에 따라 단문 연기가 종료되었습니다.", color=discord.Color(0x00FF00))
            await interaction.response.send_message(embed=embed)
            return

        short_script[str(interaction.channel.id)]["last_member"] = short_script[str(
            interaction.channel.id)]["members"].pop(0)

        embed = discord.Embed(
            title="다음 연기자", description=f"다음 연기자는 < {short_script[str(interaction.channel.id)]['last_member']} > 님입니다.", color=discord.Color(0x00FF00))
        embed.add_field(
            name="현재 인원", value=short_script[str(interaction.channel.id)]["last_member"], inline=False)
        embed.add_field(name="예약목록", value=await get_member_list(short_script[str(interaction.channel.id)]["members"]), inline=False)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="단문리스트", description="단문 예약 목록을 보여줍니다.")
    async def 단문리스트(self, interaction: Interaction):
        if is_reading_channel(interaction.channel.category.id):
            await interaction.response.send_message(f"리딩 채널 밖에선 사용 할 수 없는 명령어 입니다.")
            return

        if short_script.get(str(interaction.channel.id)) == None:
            await interaction.response.send_message(f"단문예약이 시작하지 않았습니다. `/단문예약`을 사용해주세요.")
            return

        time_delta = (datetime.datetime.now(
        ) - short_script[str(interaction.channel.id)]["last_time"]).seconds

        embed = discord.Embed(
            title="📑 단문 리스트", description=f"시작시간 : {time_delta // 60}분 {time_delta % 60}초 전", color=0xFFFF00)
        embed.add_field(
            name="현재 연기자", value=short_script[str(interaction.channel.id)]["last_member"], inline=False)
        embed.add_field(name="예약 인원 리스트", value=await get_member_list(short_script[str(interaction.channel.id)]["members"]), inline=False)
        embed.set_thumbnail(
            url="https://cdn.discordapp.com/attachments/827931592932065332/841197513561735168/6979bf056826de22.png")
        embed.set_image(
            url="https://i.imgur.com/IO3jvcq.gif")
        await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(
        단문(bot),
        guilds=[Object(id=config['GUILD_ID'])]
    )
