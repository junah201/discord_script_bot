import discord
from discord import app_commands
from discord.ext import commands
from discord import Interaction
from discord import Object

import json
import os
import datetime
import re

with open(f"config.json", "r", encoding="utf-8-sig") as json_file:
    config = json.load(json_file)


async def 명령어점수(interaction: discord.Interaction, self):
    with open(f"./DB/User/users.json", "r", encoding="utf-8-sig") as json_file:
        users_data = json.load(json_file)

    if users_data.get(str(interaction.user.id)) != None:
        users_data[str(interaction.user.id)]["last_evaluate"] = datetime.datetime.now(
        ).strftime("%Y-%m-%d")

    else:
        users_data[str(interaction.user.id)] = {
            "name": interaction.user.name,
            "grade": 0,
            "command_point": 0,
            "last_evaluate": datetime.datetime.now().strftime("%Y-%m-%d"),
            "review": {},
            "warning": 0
        }

    if users_data.get(str(interaction.user.id)) == None:
        users_data[str(interaction.user.id)] = {
            "name": interaction.user.name,
            "grade": 0,
            "command_point": 0,
            "last_evaluate": "미평가",
            "review": {},
            "warning": 0
        }

    users_data[str(interaction.user.id)]['command_point'] += 1

    with open(f"./DB/User/users.json", "w", encoding="utf-8-sig") as json_file:
        json.dump(users_data, json_file, indent=4)

    if users_data[str(interaction.user.id)]['command_point'] in [1, 10, 50, 100, 150, 200, 300]:
        # member = await interaction.guild.fetch_member(interaction.user.id)
        # for point in [1, 2, 10, 100, 200, 300, 400, 500]:
        #     point_value = users_data[str(interaction.user.id)]['command_point'][str(point)]
        #     if point_value in [1, 2, 10, 100, 200, 300, 400, 500]:

        await interaction.channel.send(f"{interaction.user.mention}님의 노고에 감사드립니다! (하트 수 : `{users_data[str(interaction.user.id)]['command_point'] - 1} -> {users_data[str(interaction.user.id)]['command_point']}`)")

    # 1 : 신인 배우 , 10 : 조연 배우, 20 : 유명 배우, 30 : 대세 배우, 40 : 주연 배우, 50 : 탑배우
    if users_data[str(interaction.user.id)]['command_point'] in [1, 10, 50, 100, 150, 200, 300]:
        member = await interaction.guild.fetch_member(interaction.user.id)
        for grade in [1, 10, 50, 100, 150, 200, 300]:
            role = discord.utils.get(
                member.guild.roles, id=config['ROLE_ID2'][str(grade)])
            if role in member.roles:
                await member.remove_roles(role)
        role = interaction.guild.get_role(config['ROLE_ID2'][str(
            users_data[str(interaction.user.id)]['command_point'])])
        await member.add_roles(role)

    # try:
        channel = await self.bot.fetch_channel(config['LOG_CHANNEL'])
        # print(interaction.user)
        # print(interaction.user.id)
        # print(interaction.channel)
        # print(interaction.channel.id)
        log_embed = discord.Embed(
            title="[유저활동점수]", description=f"""사용자 : `{interaction.user.name}({interaction.user.id}`)\n
            채널 : {interaction.channel.mention} (`{interaction.channel.id}`)\n
            대상 : `{interaction.user.name} ({interaction.user.id}`)\n
            점수 : `{users_data[str(interaction.user.id)]['command_point'] - 1} -> {users_data[str(interaction.user.id)]['command_point']}`\n
            시간 : `({datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')})`""")
        await channel.send(embed=log_embed)
    # except Exception as e:
    #     print("[유저활동점수] error 발생")
    #     print(e)


async def 취향저격추가(유저: discord.Member, interaction: discord.Interaction, self):
    if 유저.id == interaction.user.id:
        # ↓↓↓ 연가람이 메시지 적음
        await interaction.response.send_message(f"{interaction.user.mention} 님 ^^ 자기 자신을 추천할 수는 없는거랍니다 ㅎㅎ", ephemeral=False)
        return

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
            "command_point": 0,
            "last_evaluate": datetime.datetime.now().strftime("%Y-%m-%d"),
            "review": {},
            "warning": 0
        }

    user = 유저
    if users_data.get(str(user.id)) == None:
        users_data[str(user.id)] = {
            "name": interaction.user.name,
            "grade": 0,
            "command_point": 0,
            "last_evaluate": "미평가",
            "review": {},
            "warning": 0
        }

    users_data[str(user.id)]['grade'] += 1

    with open(f"./DB/User/users.json", "w", encoding="utf-8-sig") as json_file:
        json.dump(users_data, json_file, indent=4)

    await interaction.response.send_message(f"{user.mention}님의 평가가 완료되었습니다.", ephemeral=True)
    await 명령어점수(interaction, self)

    try:
        await user.send(f"알 수 없는 누군가가 당신에게 __취향저격__ 하트를 보냈습니다. (하트 수 : `{users_data[str(user.id)]['grade'] - 1} -> {users_data[str(user.id)]['grade']}`)")

    except:
        await interaction.channel.send(f"""```{user.name}님께서 개인 멘션을 닫아 두셨기 때문에 이곳으로 채팅이 도착했습니다.```\n
        알 수 없는 누군가가 {user.mention}님에게 취향저격 하트를 보냈습니다. (하트 수 : `{users_data[str(user.id)]['grade'] - 1} -> {users_data[str(user.id)]['grade']}`)""")

    # 1 : 신인 배우 , 10 : 조연 배우, 20 : 유명 배우, 30 : 대세 배우, 40 : 주연 배우, 50 : 탑배우
    if users_data[str(user.id)]['grade'] in [1, 10, 20, 30, 40, 50]:
        member = await interaction.guild.fetch_member(user.id)
        for grade in [1, 10, 20, 30, 40, 50]:
            role = discord.utils.get(
                member.guild.roles, id=config['ROLE_ID'][str(grade)])
            if role in member.roles:
                await member.remove_roles(role)
        role = interaction.guild.get_role(
            config['ROLE_ID'][str(users_data[str(user.id)]['grade'])])
        await member.add_roles(role)

    try:
        channel = await self.bot.fetch_channel(config['LOG_CHANNEL'])
        log_embed = discord.Embed(
            title="[유저평가]", description=f"사용자 : `{interaction.user.name}({interaction.user.id})`\n채널 :{interaction.channel.mention} (`{interaction.channel.id}`)\n대상 : `{user.name} ({user.id})`\n점수 : `{users_data[str(user.id)]['grade'] - 1} -> {users_data[str(user.id)]['grade']}`\n시간 : `({datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')})`")
        await channel.send(embed=log_embed)
    except Exception as e:
        print("[유저평가] error 발생")
        print(e)


class 유저(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="취향저격", description="리딩에서 감명 깊은 연기를 선보여준 배우에게 하트를 보냅니다. (유저 칸에는 원하는 유저를 맨션해주세요.) (하루에 1회 사용 가능)")
    async def 취향저격(self, interaction: Interaction, 유저: discord.Member):
        await 취향저격추가(유저, interaction, self)

    @app_commands.command(name="유저정보", description="유저의 상태정보를 열람합니다. (유저 칸에는 원하는 유저를 맨션해주세요.)")
    async def 유저정보(self, interaction: Interaction, 유저: str):
        user = await self.bot.fetch_user(re.sub(r'[^0-9]', '', 유저))
        member = await interaction.guild.fetch_member(user.id)

        with open(f"./DB/User/users.json", "r", encoding="utf-8-sig") as json_file:
            users_data = json.load(json_file)

        if users_data.get(str(user.id)) == None:
            await interaction.response.send_message(f"`{user.name}({user.id})`님은 유저 데이터에 없습니다.\n(`{user.name}({user.id})`이 대본이나 유저를 평가하지 않아 유저 데이터에 등록되지 않은 것 같습니다.)", ephemeral=True)
            return

        embed = discord.Embed(
            title=f"{user.display_name}",
            description=f"**REC 서버회원 {user.mention}님의 정보입니다. (유저 인포메이션)**",
            color=discord.Color(0xFFFF00),
            timestamp=datetime.datetime.now()
        )

        embed.add_field(name="**유저 평점**",
                        value=f"{users_data[str(user.id)]['grade']}")
        embed.add_field(name="**유저 경고**",
                        value=f"{users_data[str(user.id)]['warning']}")
        embed.add_field(name="**대본 평가**",
                        value=f"{len(users_data[str(user.id)]['review'].keys())}개의 대본을 평가했습니다.")

        '''
        embed.add_field(name="**계정생성일**",
                        value=member.created_at.strftime("%Y/%m/%d/%H"))
        embed.add_field(name="**서버입장일**",
                        value=member.joined_at.strftime("%Y/%m/%d일/%H"))
        '''

        embed.add_field(name="**서버 직업**", value=member.top_role.mention)
        roles = [role.mention for role in member.roles if not role.is_default()]
        embed.add_field(
            name=f"역할 [{len(roles)}]",
            value=" **\n** ".join(roles),
            inline=False
        )
        embed.set_thumbnail(url=user.avatar.url)
        embed.set_footer(icon_url=interaction.user.avatar.url,
                         text=f"요청자 : {interaction.user}")
        await interaction.response.send_message(embed=embed)

        try:
            channel = await self.bot.fetch_channel(config['LOG_CHANNEL'])
            log_embed = discord.Embed(
                title="[유저정보]", description=f"사용자 : `{interaction.user.name}({interaction.user.id})`\n채널 : {interaction.channel.mention} (`{interaction.channel.id}`)\n대상 : `{user.name} ({user.id})`\n시간 : `({datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')})`")
            await channel.send(embed=log_embed)
        except Exception as e:
            print("[유저정보] error 발생")
            print(e)

    @app_commands.command(name="유저경고", description="유저를 경고합니다. (유저 칸에는 원하는 유저를 맨션해주세요.)")
    async def 유저경고(self, interaction: discord.Interaction, 유저: str):
        with open(f"./DB/User/users.json", "r", encoding="utf-8-sig") as json_file:
            users_data = json.load(json_file)

        user = await self.bot.fetch_user(re.sub(r'[^0-9]', '', 유저))

        if users_data.get(str(user.id)) == None:
            users_data[str(user.id)] = {
                "name": user.name,
                "grade": 0,
                "last_evaluate": "미평가",
                "review": {},
                "warning": 0
            }

        users_data[str(user.id)]['warning'] += 1

        with open(f"./DB/User/users.json", "w", encoding="utf-8-sig") as json_file:
            json.dump(users_data, json_file, indent=4)

        await interaction.response.send_message(f"{user.mention}님의 대한 경고가 완료되어 총 경고 수가 `{users_data[str(user.id)]['warning']}`으로 변화하였습니다.", ephemeral=True)

        try:
            channel = await self.bot.fetch_channel(config['LOG_CHANNEL'])
            log_embed = discord.Embed(
                title="[유저경고]", description=f"사용자 : `{interaction.user.name}({interaction.user.id})`\n채널 : {interaction.channel.mention} (`{interaction.channel.id}`)\n대상 : `{user.name} ({user.id})`\n경고 : `{users_data[str(user.id)]['warning'] - 1} -> {users_data[str(user.id)]['warning']}`\n시간 : `({datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')})`")
            await channel.send(embed=log_embed)
        except Exception as e:
            print("[유저경고] error 발생")
            print(e)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(
        유저(bot),
        guilds=[Object(id=config['GUILD_ID'])]
    )
