from ast import Await, Delete
from cgi import print_directory
from email import message
from multiprocessing import Manager, managers
from tkinter.font import names
from tokenize import Name
import discord
from discord import app_commands
from discord.ext import commands, tasks
from discord import Interaction
from discord import Object
import asyncio

import json
import os
import datetime
import random

from Cogs.대본 import 대본목록, 대본생성, 대본평가, gether_view

Channels = {}

redh = {}

with open(f"config.json", "r", encoding="utf-8-sig") as json_file:
    config = json.load(json_file)


class 대본모달(discord.ui.Modal, title='대본'):
    남 = discord.ui.TextInput(
        label='남', style=discord.TextStyle.short, max_length=2)
    여 = discord.ui.TextInput(
        label='여', style=discord.TextStyle.short, max_length=2)

    async def on_submit(self, interaction: discord.Interaction):
        self.남 = int(self.남.value)
        self.여 = int(self.여.value)

        datas = {}

        for file in await 대본목록():
            if file == "Script.json":
                continue
            if len(file) == 11 and int(file[0]) <= self.남 and int(file[2]) <= self.여 and int(file[0]) + int(file[2]) + int(file[4]) == self.남 + self.여:
                with open(f"./DB/Script/{file}", "r", encoding="utf-8-sig") as json_file:
                    datas.update(json.load(json_file))

        selects = discord.ui.Select()

        if not datas.keys():
            return await interaction.response.send_message(f"존재하는 대본이 없습니다. ({self.남}남{self.여}여)", ephemeral=True)

        for type in datas.keys():
            selects.add_option(label=type)

        async def select_callback(interaction: interaction) -> None:
            script_type = selects.values[0]
            script_embed, script_view = await 대본생성(script_type, self.남, self.여)

            await interaction.response.send_message(embed=script_embed, view=script_view)

        selects.callback = select_callback

        delete_button = discord.ui.Button(
            emoji="⬜", style=discord.ButtonStyle.danger)

        async def delete_button_callback(interaction: discord.Interaction) -> None:
            if embed.author.name == interaction.user.name:
                await interaction.message.delete()
                await interaction.response.send_message("삭제되었습니다.", ephemeral=True)
            else:
                await interaction.response.send_message("대본 생성자만 삭제할 수 있습니다.", ephemeral=True)

        delete_button.callback = delete_button_callback

        embed = discord.Embed(
            title="대본 선택", description="대본을 선택해주세요.", color=0xd6e2ff)
        embed.set_footer(text=f"[ {self.남}남 ] | [ {self.여}여 ]")
        embed.set_author(name=f'{interaction.user.name}')
        embed.set_image(url="https://i.imgur.com/rLaOoQn.png")
        view = discord.ui.View(timeout=1200)
        view.add_item(selects)
        view.add_item(delete_button)

        await interaction.response.send_message(embed=embed, view=view)


class 대본하트모달(discord.ui.Modal, title='대본하트'):
    대본아이디 = discord.ui.TextInput(
        label='대본아이디', style=discord.TextStyle.short, max_length=4)

    async def on_submit(self, interaction: discord.Interaction):
        self.대본아이디 = self.대본아이디.value

        with open(f"./DB/Script/Script.json", "r", encoding="utf-8-sig") as json_file:
            script_list = json.load(json_file)

        if str(self.대본아이디) not in script_list.keys():
            return await interaction.response.send_message("존재하지 않는 대본입니다.", ephemeral=True)

        heart_embed = discord.Embed(title="대본 평가하기")
        heart_embed.add_field(
            name="제목", value=f"[{script_list[self.대본아이디]['name']}]({script_list[self.대본아이디]['link']})")
        heart_embed.add_field(
            name="성비", value=f"{script_list[self.대본아이디]['gender']}")

        with open(f"./DB/Script/{script_list[self.대본아이디]['gender']}.json", "r", encoding="utf-8-sig") as json_file:
            script_data = json.load(json_file)

        data = script_data[script_list[self.대본아이디]['type']][self.대본아이디]

        if data['rating'] == 0:
            heart_embed.add_field(
                name="하트", value=f"미평가 (0명)")
        else:
            heart_embed.add_field(
                name="하트", value=f"{''.join(['❤️' for i in range(round(data['rating'] // data['rating_users']))])}{''.join(['🤍' for i in range(round(5 - (data['rating'] // data['rating_users'])))])} ({data['rating_users']}명)")

        heart_view = discord.ui.View(timeout=1200)

        one_button = discord.ui.Button(label="1점")

        async def one_button_callback(interaction: discord.Interaction):
            await 대본평가(interaction, self.대본아이디, 1, heart_embed)
            with open(f"./DB/Script/{script_list[self.대본아이디]['gender']}.json", "r", encoding="utf-8-sig") as json_file:
                script_data = json.load(json_file)
                data = script_data[script_list[self.대본아이디]['type']][self.대본아이디]
            heart_embed.set_field_at(
                index=2, name="하트", value=f"{''.join(['❤️' for i in range(round(data['rating'] // data['rating_users']))])}{''.join(['🤍' for i in range(round(5 - (data['rating'] // data['rating_users'])))])} ({data['rating_users']}명)")
            await interaction.response.edit_message(embed=heart_embed)
        one_button.callback = one_button_callback

        two_button = discord.ui.Button(label="2점")

        async def two_button_callback(interaction: discord.Interaction):
            await 대본평가(interaction, self.대본아이디, 2, heart_embed)
            with open(f"./DB/Script/{script_list[self.대본아이디]['gender']}.json", "r", encoding="utf-8-sig") as json_file:
                script_data = json.load(json_file)
                data = script_data[script_list[self.대본아이디]['type']][self.대본아이디]
            heart_embed.set_field_at(
                index=2, name="하트", value=f"{''.join(['❤️' for i in range(round(data['rating'] // data['rating_users']))])}{''.join(['🤍' for i in range(round(5 - (data['rating'] // data['rating_users'])))])} ({data['rating_users']}명)")
            await interaction.response.edit_message(embed=heart_embed)
        two_button.callback = two_button_callback

        three_button = discord.ui.Button(label="3점")

        async def three_button_callback(interaction: discord.Interaction):
            await 대본평가(interaction, self.대본아이디, 3, heart_embed)
            with open(f"./DB/Script/{script_list[self.대본아이디]['gender']}.json", "r", encoding="utf-8-sig") as json_file:
                script_data = json.load(json_file)
                data = script_data[script_list[self.대본아이디]['type']][self.대본아이디]
            heart_embed.set_field_at(
                index=2, name="하트", value=f"{''.join(['❤️' for i in range(round(data['rating'] // data['rating_users']))])}{''.join(['🤍' for i in range(round(5 - (data['rating'] // data['rating_users'])))])} ({data['rating_users']}명)")
            await interaction.response.edit_message(embed=heart_embed)
        three_button.callback = three_button_callback

        four_button = discord.ui.Button(label="4점")

        async def four_button_callback(interaction: discord.Interaction):
            await 대본평가(interaction, self.대본아이디, 4, heart_embed)
            with open(f"./DB/Script/{script_list[self.대본아이디]['gender']}.json", "r", encoding="utf-8-sig") as json_file:
                script_data = json.load(json_file)
                data = script_data[script_list[self.대본아이디]['type']][self.대본아이디]
            heart_embed.set_field_at(
                index=2, name="하트", value=f"{''.join(['❤️' for i in range(round(data['rating'] // data['rating_users']))])}{''.join(['🤍' for i in range(round(5 - (data['rating'] // data['rating_users'])))])} ({data['rating_users']}명)")
            await interaction.response.edit_message(embed=heart_embed)
        four_button.callback = four_button_callback

        five_button = discord.ui.Button(label="5점")

        async def five_button_callback(interaction: discord.Interaction):
            await 대본평가(interaction, self.대본아이디, 5, heart_embed)
            with open(f"./DB/Script/{script_list[self.대본아이디]['gender']}.json", "r", encoding="utf-8-sig") as json_file:
                script_data = json.load(json_file)
                data = script_data[script_list[self.대본아이디]['type']][self.대본아이디]
            heart_embed.set_field_at(
                index=2, name="하트", value=f"{''.join(['❤️' for i in range(round(data['rating'] // data['rating_users']))])}{''.join(['🤍' for i in range(round(5 - (data['rating'] // data['rating_users'])))])} ({data['rating_users']}명)")
            await interaction.response.edit_message(embed=heart_embed)
        five_button.callback = five_button_callback

        heart_view.add_item(one_button)
        heart_view.add_item(two_button)
        heart_view.add_item(three_button)
        heart_view.add_item(four_button)
        heart_view.add_item(five_button)

        await interaction.response.send_message(embed=heart_embed, view=heart_view)


class 이름변경모달(discord.ui.Modal, title='이름변경'):
    이름 = discord.ui.TextInput(
        label='이름변경', style=discord.TextStyle.long)

    async def on_submit(self, interaction: discord.Interaction):
        self.이름 = self.이름.value

        변경이름 = str(self.이름)

        voice_state = None if not interaction.user.voice else interaction.user.voice.channel
        if voice_state:
            await interaction.user.voice.channel.edit(name=변경이름)
            await interaction.channel.edit(name=변경이름)
            await interaction.response.send_message(f"음성채널의 이름이 ``{변경이름}``으로 이름이 변경 되었습니다.")
        else:
            await interaction.response.send_message("음성 채널에 들어가 있지 않습니다.")


class 인원설정모달(discord.ui.Modal, title='인원설정'):
    인원 = discord.ui.TextInput(
        label='인원설정', style=discord.TextStyle.long)

    async def on_submit(self, interaction: discord.Interaction):
        self.인원 = self.인원.value

        설정인원 = self.인원

        user_limit = interaction.user.voice.channel.user_limit
        await interaction.user.voice.channel.edit(user_limit=설정인원)
        await interaction.response.send_message(f"최대 배우님의 정원이 {설정인원} 명으로 설정되었습니다.")


class 뽑기모달(discord.ui.Modal, title='뽑기'):
    뽑기 = discord.ui.TextInput(
        label='뽑기', style=discord.TextStyle.long)

    async def on_submit(self, interaction: discord.Interaction):
        self.뽑기 = self.뽑기.value

        embed = discord.Embed(
            title='⠀⠀⠀⠀〔⠀⠀⠀🥇 제비 뽑기⠀⠀⠀〕',
            description='연기자에게 랜덤하게 번호를 부여합니다.',
            color=discord.Color(0xFFFF00)
        )

        embed.set_thumbnail(
            url="https://cdn.discordapp.com/attachments/827931592932065332/841197513561735168/6979bf056826de22.png")
        embed.set_image(
            url="https://i.imgur.com/xLNYJF0.png")

        users = self.뽑기.split()

        random_num = [i for i in range(1, len(users) + 1, 1)]
        random.shuffle(random_num)

        for user, num in zip(users, random_num):
            embed.add_field(name=f"\t\t\t\t**⠀⠀⠀⠀⠀⠀《⠀⠀⠀⠀⠀{user}⠀⠀⠀⠀⠀》**",
                            value=f"*{user}* 님은 : ||[⠀⠀⠀⠀⠀{num}⠀⠀⠀⠀⠀]||     번 입니다.", inline=False)

        await interaction.response.send_message(embed=embed)


class 채널(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        global Channels
        channel_id = config["GENERATOR_CHANNEL_ID"]
        category_id = config["GENERATOR_CATEGORY_ID"]
        if after.channel != None and after.channel.id == channel_id:
            voice_channel = await after.channel.guild.create_voice_channel(name=f"{member.name} 님의 대본방", category=after.channel.category, overwrites={
                member: discord.PermissionOverwrite(manage_channels=True, connect=True, mute_members=True, kick_members=True, deafen_members=True),
            })
            await member.move_to(voice_channel)
            text_channel = await after.channel.guild.create_text_channel(name=f"🌽 ឵ {(member.name).replace('-', '')} ឵ 님의 ឵ 대본방", category=after.channel.category, overwrites={
                member: discord.PermissionOverwrite(manage_channels=True, view_channel=True),
                member.guild.default_role: discord.PermissionOverwrite(
                    view_channel=False)
            })

            embed = discord.Embed(
                description="다음과 같은 서비스를 이용하실 수 있습니다.", color=0xFFFF00)
            # embed.add_field(
            #     name="모여", value="대배우 역할을 가진 유저들을 맨션하여 리딩을 시작", inline=False)
            # embed.add_field(
            #     name="대본", value="남녀 성비를 입력 시, 그에 맞는 대본 목록을 제공", inline=False)
            # embed.add_field(
            #     name="대본하트", value="대본의 ID를 이용해 대본을 평가", inline=False)
            # embed.add_field(
            #     name="뽑기", value="각각의 유저들에게 랜덤한 번호를 부여", inline=False)
            # embed.set_author(
            #     name="REC 대시보드", icon_url="https://i.imgur.com/JGSMPZ4.png")
            embed.set_image(url="https://i.imgur.com/yLhV9oF.png")
            embed.set_footer(text="위 설명을 보시고 아래 버튼을 사용해 주세요")
            view = discord.ui.View(timeout=None)

            gather_button = discord.ui.Button(
                emoji="<:JOIN:1006084189172547664>")  # , label="모여")

            async def gather_button_callback(interaction: discord.Interaction):
                embed = discord.Embed(color=0xFFFF00)
                embed.title = "💌 캐스팅 시작"
                # .\n[<:cst:840538932906950682> : 참여 <:RED:841252822795550751> : 참여취소 <:can:841253094674399243> : 완료]"
                embed.description = "무대 참여 의사를 확인합니다"
                embed.add_field(name="🍺⠀남배우", value=" 《⠀공 석⠀》")
                embed.add_field(name="💋⠀여배우", value=" 《⠀공 석⠀》")
                # embed.set_image(
                #     url="https://media.discordapp.net/attachments/424831572861124619/549533764880171018/da41590cda439e68.gif")
                embed.set_author(name=f'{interaction.user.name}',
                                 icon_url="https://cdn.discordapp.com/attachments/827931592932065332/841197513561735168/6979bf056826de22.png")
                embed.set_thumbnail(url=str(interaction.user.display_avatar))
                embed.set_image(
                    url="https://c.tenor.com/mc9-3cypZEYAAAAC/rainbow-line.gif")

                view = discord.ui.View(timeout=1200)

                join_button = discord.ui.Button(label="참여",
                                                emoji="<:cst:840538932906950682>", style=discord.ButtonStyle.green)

                async def join_button_callback(interaction: discord.Interaction):
                    is_man = "《 ឵ ឵឵ ឵ ឵឵ ឵남성 배우 ឵ ឵឵ ឵ ឵឵ ឵》" in [
                        x.name for x in interaction.user.roles]
                    is_woman = "《 ឵ ឵឵ ឵ ឵឵ ឵여성 배우 ឵ ឵឵ ឵ ឵឵ ឵》" in [
                        x.name for x in interaction.user.roles]

                    if is_man:
                        if embed.fields[0].value == " 《⠀공 석⠀》":
                            man_users = []
                        else:
                            man_users = embed.fields[0].value.split('\n')

                        if interaction.user.name in man_users:
                            return await interaction.response.send_message("이미 등록되어있습니다.", ephemeral=True)

                        man_users.append(interaction.user.name)

                        embed.set_field_at(
                            0, name=f"🍺⠀남배우 {len(man_users)}분", value='\n'.join(man_users))

                        await interaction.channel.send(f"<:cst:840538932906950682> | {open_actor}님이 개설하신 무대에 {interaction.user.mention}님이 캐스팅 되었습니다. [🍺 현재 남성 배우 : {len(man_users)}명]")

                    elif is_woman:
                        if embed.fields[1].value == " 《⠀공 석⠀》":
                            woman_users = []
                        else:
                            woman_users = embed.fields[1].value.split('\n')

                        if interaction.user.name in woman_users:
                            return await interaction.response.send_message("이미 등록되어있습니다.", ephemeral=True)

                        woman_users.append(interaction.user.name)

                        embed.set_field_at(
                            1, name=f"💋⠀여배우 {len(woman_users)}분", value='\n'.join(woman_users))

                        await interaction.channel.send(f"<:cst:840538932906950682> | {open_actor}님이 개설하신 무대에 {interaction.user.mention}님이 캐스팅 되었습니다. [💋 현재 여성 배우 : {len(woman_users)}명]")

                    # await interaction.channel.send(f"{interaction.user.mention}님이 참여하셨습니다")
                    await interaction.response.edit_message(embed=embed, view=view)

                join_button.callback = join_button_callback
                view.add_item(join_button)

                cancel_button = discord.ui.Button(label="취소",
                                                  emoji="<:RED:841252822795550751>", style=discord.ButtonStyle.danger)

                async def cancel_button_callback(interaction: discord.Interaction):
                    is_man = "《 ឵ ឵឵ ឵ ឵឵ ឵남성 배우 ឵ ឵឵ ឵ ឵឵ ឵》" in [
                        x.name for x in interaction.user.roles]
                    is_woman = "《 ឵ ឵឵ ឵ ឵឵ ឵여성 배우 ឵ ឵឵ ឵ ឵឵ ឵》" in [
                        x.name for x in interaction.user.roles]

                    if is_man:
                        if embed.fields[0].value == " 《⠀공 석⠀》":
                            man_users = []
                        else:
                            man_users = embed.fields[0].value.split('\n')
                        if interaction.user.name in man_users:
                            man_users.remove(interaction.user.name)
                            if not man_users:
                                embed.set_field_at(
                                    0, name=f"🍺⠀남배우", value=" 《⠀공 석⠀》")
                            else:
                                embed.set_field_at(
                                    0, name=f"🍺⠀남배우 {len(man_users)}분", value='\n'.join(man_users))

                            await interaction.channel.send(content=f"<:RED:841252822795550751> - < {interaction.user.mention} > 님께서 사정이 생기셨습니다.")
                    elif is_woman:
                        if embed.fields[1].value == " 《⠀공 석⠀》":
                            woman_users = []
                        else:
                            woman_users = embed.fields[1].value.split('\n')
                        if interaction.user.name in woman_users:
                            woman_users.remove(interaction.user.name)
                            if not woman_users:
                                embed.set_field_at(
                                    1, name=f"💋⠀여배우", value=" 《⠀공 석⠀》")
                            else:
                                embed.set_field_at(
                                    1, name=f"💋⠀여배우 {len(woman_users)}분", value='\n'.join(woman_users))
                            await interaction.channel.send(content=f"<:RED:841252822795550751> - < {interaction.user.mention} > 님께서 사정이 생기셨습니다.")

                    await interaction.response.edit_message(embed=embed, view=view)

                cancel_button.callback = cancel_button_callback
                view.add_item(cancel_button)

                ending_button = discord.ui.Button(label="완료",
                                                  emoji="<:can:841253094674399243>", style=discord.ButtonStyle.primary)

                async def ending_button_callback(interaction: discord.Interaction):
                    if interaction.user.name == embed.author.name:
                        if embed.fields[0].value == " 《⠀공 석⠀》":
                            man_users = []
                        else:
                            man_users = embed.fields[0].value.split('\n')

                        if embed.fields[1].value == " 《⠀공 석⠀》":
                            woman_users = []
                        else:
                            woman_users = embed.fields[1].value.split('\n')

                        join_button.disabled = True
                        cancel_button.disabled = True
                        ending_button.disabled = True

                        await interaction.response.edit_message(embed=embed, view=view)

                        ending_embed = discord.Embed(
                            title="《⠀ 🎉 캐스팅 완료 🎉 ⠀》", description=f"총 {len(man_users)}남{len(woman_users)}여", color=0xff2eb6)

                        ending_view = discord.ui.View(timeout=1200)

                        tmp = '\n'.join(man_users)
                        if tmp == "":
                            tmp = " 《⠀공 석⠀》"
                        ending_embed.add_field(name="🍺 남배우", value=f"{tmp} ")

                        tmp = '\n'.join(woman_users)
                        if tmp == "":
                            tmp = " 《⠀공 석⠀》"
                        ending_embed.add_field(name="💋 여배우", value=f"{tmp} ")

                        datas = {}
                        남 = len(man_users)
                        여 = len(woman_users)

                        for file in await 대본목록():
                            if file == "Script.json":
                                continue
                            if len(file) == 11 and int(file[0]) <= 남 and int(file[2]) <= 여 and int(file[0]) + int(file[2]) + int(file[4]) == 남 + 여:
                                with open(f"./DB/Script/{file}", "r", encoding="utf-8-sig") as json_file:
                                    datas.update(json.load(json_file))

                        ending_embed.set_image(
                            url="https://i.imgur.com/4M7IWwP.gif")

                        selects = discord.ui.Select()

                        if not datas.keys():
                            selects.add_option(label="해당 인원의 대본이 없음")

                        for type in datas.keys():
                            selects.add_option(label=type)

                        async def select_callback(interaction: discord.Interaction) -> None:
                            script_type = selects.values[0]
                            script_embed, script_view = await 대본생성(script_type, 남, 여)

                            await interaction.response.send_message(embed=script_embed, view=script_view)

                        selects.callback = select_callback

                        ending_view = discord.ui.View(timeout=1200)
                        ending_view.add_item(selects)

                        await interaction.channel.send(embed=ending_embed, view=ending_view)
                    else:
                        await interaction.response.send_message(f"마무리 버튼은 개설자인 {embed.author.name} 님만 사용할 수 있습니다.", ephemeral=True)

                ending_button.callback = ending_button_callback
                view.add_item(ending_button)

                open_actor = f"{interaction.user.mention}"
                await interaction.response.send_message(f"{interaction.user.mention}님께서 새로운 무대를 여셨습니다. <@&{config['ACTOR_ROLE_ID']}>", embed=embed, view=view, allowed_mentions=discord.AllowedMentions())

            gather_button.callback = gather_button_callback

            script_button = discord.ui.Button(
                emoji="<:SCR:1006084170004574248>")  # ,label="대본")

            async def script_button_callback(interaction: discord.Interaction):
                await interaction.response.send_modal(대본모달())
            script_button.callback = script_button_callback

            script_heart_button = discord.ui.Button(
                emoji="<:SCRH:1006084172433072170>")  # , label="대본하트")

            async def script_heart_button_callback(interaction: discord.Interaction):
                await interaction.response.send_modal(대본하트모달())
            script_heart_button.callback = script_heart_button_callback

            pick_button = discord.ui.Button(
                emoji="<:tiket:1006084174110806118>")  # ,label="뽑기")

            async def pick_button_callback(interaction: discord.Interaction):
                await interaction.response.send_modal(뽑기모달())
            pick_button.callback = pick_button_callback

            rename_button = discord.ui.Button(
                emoji="<:CHNA:1006084175599771709>")  # ,label="이름변경")

            async def rename_button_callback(interaction: discord.Interaction):
                if member.id == interaction.user.id:
                    await interaction.response.send_modal(이름변경모달())
                else:
                    await interaction.response.send_message(
                        f"이름 변경은 개설자인 {member.name} 님만 사용할 수 있습니다.", ephemeral=True)
            rename_button.callback = rename_button_callback

            lock_button = discord.ui.Button(
                emoji="<:LOCKON:1006084192246976572>")  # , label="잠금")

            async def lock_button_callback(interaction: discord.Interaction):
                if member.id == interaction.user.id:
                    channel = interaction.user.voice.channel
                    overwrite = channel.overwrites_for(
                        interaction.guild.default_role)
                    overwrite.connect = False
                    await channel.set_permissions(interaction.guild.default_role, overwrite=overwrite)
                    await interaction.response.send_message(f"<:ro1:935564780163440751> | {channel}을 ``잠금``했습니다.", ephemeral=True)
                else:
                    await interaction.response.send_message(
                        f"잠금 버튼은 개설자인 {member.name} 님만 사용할 수 있습니다.", ephemeral=True)
            lock_button.callback = lock_button_callback

            unlock_button = discord.ui.Button(
                emoji="<:LOCKOFF:1006084190737010769>")  # , label="해제")

            async def unlock_button_callback(interaction: discord.Interaction):
                if member.id == interaction.user.id:
                    channel = interaction.user.voice.channel
                    overwrite = channel.overwrites_for(
                        interaction.guild.default_role)
                    overwrite.connect = True
                    await channel.set_permissions(interaction.guild.default_role, overwrite=overwrite)
                    await interaction.response.send_message(f"{channel}을 ``잠금해제``했습니다.", ephemeral=True)
                else:
                    await interaction.response.send_message(
                        f"잠금 해제버튼은 개설자인 {member.name} 님만 사용할 수 있습니다.", ephemeral=True)
            unlock_button.callback = unlock_button_callback

            hide_button = discord.ui.Button(
                emoji="<:EYEOFF:1006084181014614057>")  # , label="숨김")

            async def hide_button_callback(interaction: discord.Interaction):
                if member.id == interaction.user.id:
                    channel = interaction.user.voice.channel
                    overwrite = channel.overwrites_for(
                        interaction.guild.default_role)
                    overwrite.view_channel = False
                    await channel.set_permissions(interaction.guild.default_role, overwrite=overwrite)
                    await interaction.response.send_message(f"{channel}을 ``숨김``기능을 활성화 했습니다.", ephemeral=True)
                else:
                    await interaction.response.send_message(
                        f"숨김 버튼은 개설자인 {member.name} 님만 사용할 수 있습니다.", ephemeral=True)
            hide_button.callback = hide_button_callback

            unhide_button = discord.ui.Button(
                emoji="<:EYEON:1006084183849959464>")  # , label="숨김해제")

            async def unhide_button_callback(interaction: discord.Interaction):
                if member.id == interaction.user.id:
                    channel = interaction.user.voice.channel
                    overwrite = channel.overwrites_for(
                        interaction.guild.default_role)
                    overwrite.view_channel = True
                    await channel.set_permissions(interaction.guild.default_role, overwrite=overwrite)
                    await interaction.response.send_message(f"{channel}을 ``숨김``기능을 비활성화 했습니다.", ephemeral=True)
                else:
                    await interaction.response.send_message(
                        f"숨김 해제버튼은 개설자인 {member.name} 님만 사용할 수 있습니다.", ephemeral=True)
            unhide_button.callback = unhide_button_callback

            increase_limit_button = discord.ui.Button(
                emoji="<:INCR:1006084185821290497>")  # , label="증가")

            async def increase_limit_button_callback(interaction: discord.Interaction):
                user_limit = interaction.user.voice.channel.user_limit
                await interaction.user.voice.channel.edit(user_limit=user_limit + 1)
                await interaction.response.send_message(f"인원이 최대 인원이 증가 했습니다.", ephemeral=True)
            increase_limit_button.callback = increase_limit_button_callback

            decrease_limit_button = discord.ui.Button(
                emoji="<:DECR:1006084177403326514>")  # , label="감소")

            async def decrease_limit_button_callback(interaction: discord.Interaction):
                user_limit = interaction.user.voice.channel.user_limit
                if user_limit > 0:
                    await interaction.user.voice.channel.edit(user_limit=user_limit - 1)
                await interaction.response.send_message(f"인원이 최대 인원이 감소 했습니다.", ephemeral=True)
            decrease_limit_button.callback = decrease_limit_button_callback

            set_limit_button = discord.ui.Button(
                emoji="<:member:1006109383538790451>")

            async def set_limit_button_callback(interaction: discord.Interaction):
                if member.id == interaction.user.id:
                    await interaction.response.send_modal(인원설정모달())
                else:
                    await interaction.response.send_message(
                        f"인원설정은 개설자인 {member.name} 님만 할 수 있습니다.", ephemeral=True)
            set_limit_button.callback = set_limit_button_callback

            google_button = discord.ui.Button(
                emoji="<:google:1006104727743889438>", url="https://www.google.com/")
            naver_button = discord.ui.Button(
                emoji="<:naver:1006104729195122708>", url="https://www.naver.com/")
            youtube_button = discord.ui.Button(
                emoji="<:youtube:1006104730717651044>", url="https://www.youtube.com/")

            start_SC_button = discord.ui.Button(
                emoji='<:START:1006113303816314951>')
            end_SC_button = discord.ui.Button(
                emoji='<:END:1006113302453157908>')

            view.add_item(gather_button)
            view.add_item(script_button)
            view.add_item(script_heart_button)
            view.add_item(pick_button)
            view.add_item(google_button)

            view.add_item(lock_button)
            view.add_item(unlock_button)
            view.add_item(hide_button)
            view.add_item(unhide_button)
            view.add_item(naver_button)

            view.add_item(set_limit_button)
            view.add_item(rename_button)
            view.add_item(start_SC_button)
            view.add_item(end_SC_button)
            view.add_item(youtube_button)

            # view.add_item(increase_limit_button)
            # view.add_item(decrease_limit_button)

            await text_channel.send(f"<#{voice_channel.id}> 전용의 채팅 채널로 <@&{config['ACTOR_ROLE_ID']}>")

            embed_si = discord.Embed(
                title="《 ឵ ឵឵ ឵ ឵឵음성채널 권한 부여 ឵ ឵឵ ឵ ឵឵ ឵》", description=f"{member.mention} 님이 사용한 음성채널 권한 ឵ ឵឵ ឵ ឵឵ ឵\n>>> 채널 관리 : ``채널명``, ``비트레이트``, ``인원``\n인원 관리 : ``사용자 음소거``, ``사용자 추방``, ``사용자 연결 끊기``", color=0xffff00)
            embed_si.set_author(name=f"REC 음성채널 권한 안내'",
                                icon_url="https://i.imgur.com/JGSMPZ4.png")
            embed_si.set_thumbnail(url="https://i.imgur.com/L1VJKG5.png")
            await member.send(embed=embed_si)
            await member.send(f"😸 소유하신 채팅 채널로 바로가기 -> <#{text_channel.id}>")

            last_message = await text_channel.send(embed=embed, view=view)

            Channels[voice_channel.id] = {
                "text_channel": text_channel, "last_message": last_message}

            while True:
                try:
                    await Channels[voice_channel.id]["last_message"].delete()
                except:
                    Channels[voice_channel.id]["last_message"] = await text_channel.send(embed=embed, view=view)
                    await asyncio.sleep(120)

        if before.channel != None and before.channel.category.id == category_id and before.channel.members == [] and not before.channel.id == channel_id:
            await before.channel.delete()

        if after.channel != None and after.channel.category.id == category_id:
            await Channels[after.channel.id]["text_channel"].set_permissions(
                member, view_channel=True)

        if before.channel != None and before.channel.category.id == category_id:
            await Channels[before.channel.id]["text_channel"].set_permissions(
                member, view_channel=False)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(
        채널(bot),
        guilds=[Object(id=568688402904645642)]
    )
