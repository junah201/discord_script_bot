from tkinter import E
import discord
from discord.ext import commands, tasks

import os
import json
import sys
import datetime

from Cogs.대본 import gether_view

with open(f"config.json", "r", encoding="utf-8-sig") as json_file:
    config = json.load(json_file)

with open(f"color.json", "r", encoding="utf-8-sig") as json_file:
    color = json.load(json_file)

Channels = {}
Gather_message = None


class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix=config['PREFIX'],
            intents=discord.Intents.all(),
            sync_command=True,
            application_id=config['APPLICATION_ID']
        )
        self.initial_extension = [
            "Cogs.대본",
            "Cogs.유저",
            "Cogs.유틸",
            "Cogs.단문",
            "Cogs.채널"
        ]

    async def setup_hook(self):
        for ext in self.initial_extension:
            await self.load_extension(ext)

        await bot.tree.sync(guild=discord.Object(id=827801772143017994))

    async def on_ready(self):
        # 기본 역할 채널 세팅
        role_channel = discord.utils.get(
            bot.get_all_channels(), id=config["ROLE_CHANNEL_ID"])

        await role_channel.purge(limit=None)

        role_init_embed = discord.Embed(
            title="환영합니다. REC 서버입니다.", description="📌 ┃ 세 가지 중요한 설문에 참여 하시면 각 설문마다 해당 역할이 추가됩니다.\n\n📛 ┃설문에 응하지 않으시면 서버를 이용하실 수 없습니다.", color=0xffee40)
        await role_channel.send(embed=role_init_embed)

        # 기본 역할 채널 세팅 - 성별
        gender_embed = discord.Embed(
            title=":red_circle: 성별이 어떻게 되시나요?", color=0xffee40)
        gender_view = discord.ui.View(timeout=None)
        man_button = discord.ui.Button(
            emoji="♂️", label="남성 배우", style=discord.ButtonStyle.primary)

        async def man_button_callback(interaction: discord.Interaction):
            man_role = discord.utils.get(
                interaction.guild.roles, name="《 ឵ ឵឵ ឵ ឵឵ ឵남성 배우 ឵ ឵឵ ឵ ឵឵ ឵》")
            woman_role = discord.utils.get(
                interaction.guild.roles, name="《 ឵ ឵឵ ឵ ឵឵ ឵여성 배우 ឵ ឵឵ ឵ ឵឵ ឵》")
            is_man = man_role in interaction.user.roles
            is_woman = woman_role in interaction.user.roles
            if not is_man:
                await interaction.user.add_roles(man_role)
            if is_woman:
                await interaction.user.remove_roles(woman_role)

            await interaction.response.send_message(
                "정상적으로 남성 역할이 부여되었습니다.", ephemeral=True)

        man_button.callback = man_button_callback

        woman_button = discord.ui.Button(
            emoji="♀️", label="여성 배우", style=discord.ButtonStyle.primary)

        async def woman_button_callback(interaction: discord.Interaction):
            man_role = discord.utils.get(
                interaction.guild.roles, name="《 ឵ ឵឵ ឵ ឵឵ ឵남성 배우 ឵ ឵឵ ឵ ឵឵ ឵》")
            woman_role = discord.utils.get(
                interaction.guild.roles, name="《 ឵ ឵឵ ឵ ឵឵ ឵여성 배우 ឵ ឵឵ ឵ ឵឵ ឵》")
            is_man = man_role in interaction.user.roles
            is_woman = woman_role in interaction.user.roles
            if is_man:
                await interaction.user.remove_roles(man_role)
            if not is_woman:
                await interaction.user.add_roles(woman_role)

            await interaction.response.send_message(
                "정상적으로 여성 역할이 부여되었습니다.", ephemeral=True)

        woman_button.callback = woman_button_callback

        gender_view.add_item(man_button)
        gender_view.add_item(woman_button)

        await role_channel.send(embed=gender_embed, view=gender_view)

        # 기본 역할 채널 세팅 - 활동

        activeity_embed = discord.Embed(
            title=":red_circle:  어떤 활동을 원하시나요?", color=0xffee40)
        activeity_view = discord.ui.View(timeout=None)

        acting_button = discord.ui.Button(
            emoji="<:mic:841221542875627571>", label="연기", style=discord.ButtonStyle.primary)

        async def acting_button_callback(interaction: discord.Interaction):
            acting_role = discord.utils.get(
                interaction.guild.roles, name="《 ឵ ឵឵ ឵ ឵឵ ឵Actor ឵ ឵឵ ឵ ឵឵ ឵》")
            writer_role = discord.utils.get(
                interaction.guild.roles, name="《 ឵ ឵឵ ឵ ឵឵ ឵Scenario Writer ឵ ឵឵ ឵ ឵឵ ឵》")
            listener_role = discord.utils.get(
                interaction.guild.roles, name="《 ឵ ឵឵ ឵ ឵឵ ឵Listeners ឵ ឵឵ ឵ ឵឵ ឵》")

            if acting_role not in interaction.user.roles:
                await interaction.user.add_roles(acting_role)
            if writer_role in interaction.user.roles:
                await interaction.user.remove_roles(writer_role)
            if listener_role in interaction.user.roles:
                await interaction.user.remove_roles(listener_role)

            await interaction.response.send_message(
                "정상적으로 연기 역할이 부여되었습니다.", ephemeral=True)

        acting_button.callback = acting_button_callback

        writer_button = discord.ui.Button(
            emoji="✏️", label="작가", style=discord.ButtonStyle.primary)

        async def writer_button_callback(interaction: discord.Interaction):
            acting_role = discord.utils.get(
                interaction.guild.roles, name="《 ឵ ឵឵ ឵ ឵឵ ឵Actor ឵ ឵឵ ឵ ឵឵ ឵》")
            writer_role = discord.utils.get(
                interaction.guild.roles, name="《 ឵ ឵឵ ឵ ឵឵ ឵Scenario Writer ឵ ឵឵ ឵ ឵឵ ឵》")
            listener_role = discord.utils.get(
                interaction.guild.roles, name="《 ឵ ឵឵ ឵ ឵឵ ឵Listeners ឵ ឵឵ ឵ ឵឵ ឵》")

            if acting_role in interaction.user.roles:
                await interaction.user.remove_roles(acting_role)
            if writer_role not in interaction.user.roles:
                await interaction.user.add_roles(writer_role)
            if listener_role in interaction.user.roles:
                await interaction.user.remove_roles(listener_role)

            await interaction.response.send_message(
                "정상적으로 작가 역할이 부여되었습니다.", ephemeral=True)

        writer_button.callback = writer_button_callback

        listener_button = discord.ui.Button(
            emoji="👀", label="청취", style=discord.ButtonStyle.primary)

        async def listener_button_callback(interaction: discord.Interaction):
            acting_role = discord.utils.get(
                interaction.guild.roles, name="《 ឵ ឵឵ ឵ ឵឵ ឵Actor ឵ ឵឵ ឵ ឵឵ ឵》")
            writer_role = discord.utils.get(
                interaction.guild.roles, name="《 ឵ ឵឵ ឵ ឵឵ ឵Scenario Writer ឵ ឵឵ ឵ ឵឵ ឵》")
            listener_role = discord.utils.get(
                interaction.guild.roles, name="《 ឵ ឵឵ ឵ ឵឵ ឵Listeners ឵ ឵឵ ឵ ឵឵ ឵》")

            if acting_role in interaction.user.roles:
                await interaction.user.remove_roles(acting_role)
            if writer_role in interaction.user.roles:
                await interaction.user.remove_roles(writer_role)
            if listener_role not in interaction.user.roles:
                await interaction.user.add_roles(listener_role)

            await interaction.response.send_message(
                "정상적으로 청취 역할이 부여되었습니다.", ephemeral=True)

        listener_button.callback = listener_button_callback

        activeity_view.add_item(acting_button)
        activeity_view.add_item(writer_button)
        activeity_view.add_item(listener_button)

        await role_channel.send(embed=activeity_embed, view=activeity_view)

        # 기본 역할 채널 세팅 - 장르

        preference_embed = discord.Embed(
            title=":red_circle:  어떤 장르를 선호하시나요?", color=0xffee40)
        preference_view = discord.ui.View(timeout=None)

        radio_drama_button = discord.ui.Button(
            emoji="📑", label="라디오 드라마", style=discord.ButtonStyle.primary)

        async def radio_drama_button_callback(interaction: discord.Interaction):
            radio_drama_role = discord.utils.get(
                interaction.guild.roles, name="《 ឵ ឵឵ ឵ ឵឵ ឵Voice drama ឵ ឵឵ ឵ ឵឵ ឵》")

            if radio_drama_role not in interaction.user.roles:
                await interaction.user.add_roles(radio_drama_role)

                await interaction.response.send_message(
                    "정상적으로 라디오 드라마 역할이 부여되었습니다.", ephemeral=True)
            else:
                await interaction.user.remove_roles(radio_drama_role)

                await interaction.response.send_message(
                    "정상적으로 라디오 드라마 역할이 제거되었습니다.", ephemeral=True)

        radio_drama_button.callback = radio_drama_button_callback

        animation_button = discord.ui.Button(
            emoji="🧸", label="애니매이션", style=discord.ButtonStyle.primary)

        async def animation_button_callback(interaction: discord.Interaction):
            animation_role = discord.utils.get(
                interaction.guild.roles, name="《 ឵ ឵឵ ឵ ឵឵ ឵Animation ឵ ឵឵ ឵ ឵឵ ឵》")

            if animation_role not in interaction.user.roles:
                await interaction.user.add_roles(animation_role)

                await interaction.response.send_message(
                    "정상적으로 애니매이션 역할이 부여되었습니다.", ephemeral=True)
            else:
                await interaction.user.remove_roles(animation_role)

                await interaction.response.send_message(
                    "정상적으로 애니매이션 역할이 제거되었습니다.", ephemeral=True)

        animation_button.callback = animation_button_callback

        narration_button = discord.ui.Button(
            emoji="📻", label="독백/내레이션", style=discord.ButtonStyle.primary)

        async def narration_button_callback(interaction: discord.Interaction):
            narration_role = discord.utils.get(
                interaction.guild.roles, name="《 ឵ ឵឵ ឵ ឵឵ ឵Narration ឵ ឵឵ ឵ ឵឵ ឵》")

            if narration_role not in interaction.user.roles:
                await interaction.user.add_roles(narration_role)

                await interaction.response.send_message(
                    "정상적으로 독백/내레이션 역할이 부여되었습니다.", ephemeral=True)
            else:
                await interaction.user.remove_roles(narration_role)

                await interaction.response.send_message(
                    "정상적으로 독백/내레이션 역할이 제거되었습니다.", ephemeral=True)

        narration_button.callback = narration_button_callback

        media_button = discord.ui.Button(
            emoji="📺", label="매체연기", style=discord.ButtonStyle.primary)

        async def media_button_callback(interaction: discord.Interaction):
            media_role = discord.utils.get(
                interaction.guild.roles, name="《 ឵ ឵឵ ឵ ឵឵ ឵Media drama ឵ ឵឵ ឵ ឵឵ ឵》")

            if media_role not in interaction.user.roles:
                await interaction.user.add_roles(media_role)
                # await interaction.response.defer(ephemeral=True)
                await interaction.response.send_message("정상적으로 매체연기 역할이 부여되었습니다.", ephemeral=True)
            else:
                await interaction.user.remove_roles(media_role)

                await interaction.response.send_message(
                    "정상적으로 매체연기 역할이 제거되었습니다.", ephemeral=True)

        media_button.callback = media_button_callback

        preference_view.add_item(radio_drama_button)
        preference_view.add_item(animation_button)
        preference_view.add_item(narration_button)
        preference_view.add_item(media_button)

        await role_channel.send(embed=preference_embed, view=preference_view)

        # 기본 역할 채널 세팅 - 대배우

        grant_actor_embed = discord.Embed(
            description="❤️ 설문에 응해주셔서 감사드립니다.\n 아래 완료 버튼을 누르시면 서버로 입장됩니다.", color=0xff80bf)
        grant_actor_view = discord.ui.View(timeout=None)

        grant_actor_button = discord.ui.Button(
            emoji="<:cst:840538932906950682>", label="완료", style=discord.ButtonStyle.success)

        async def grant_actor_button_callback(interaction: discord.Interaction):
            await interaction.user.add_roles(
                discord.utils.get(interaction.guild.roles, name="《 ឵ ឵឵ ឵ ឵឵ ឵Very Important Person ឵ ឵឵ ឵ ឵឵ ឵》"))
            await interaction.user.add_roles(
                discord.utils.get(interaction.guild.roles, name="《 ឵ ឵឵ ឵⚜️대배우님들께서는 입장해 주십시오.⚜️ ឵ ឵឵ ឵》"))

            await interaction.response.send_message(
                "정상적으로 역할이 부여되었습니다.", ephemeral=True)

        grant_actor_button.callback = grant_actor_button_callback

        grant_actor_view.add_item(grant_actor_button)

        await role_channel.send(embed=grant_actor_embed, view=grant_actor_view)

        # 추가 역할 채널 세팅
        '''
        additional_role_embed = discord.Embed(title="역할샵")
        additional_role_embed.add_field(
            name="<@&827887094307356673>", value="/모여 명령어 사용 시 맨션으로 리딩이 모집되고 있음을 알리는 역할")
        additional_role_embed.add_field("")
        '''

        # 모여 채널 세팅

        # gather_channel = discord.utils.get(
        #     bot.get_all_channels(), id=config["GATHER_CHANNEL_ID"])

        # gather_dashboard_embed = discord.Embed(title="모여 대시보드")
        # gather_dashboard_view = gether_view()

        # await gather_channel.send(embed=gather_dashboard_embed, view=gather_dashboard_view)

        print("=========================")
        print(f"대본 봇 Login 완료")
        print(f"bot name : {self.user.name}")
        print(f"bot id : {self.user.id}")
        print(f"discord.py version : {discord.__version__}")
        print("=========================")
        await self.change_presence(status=discord.Status.online, activity=discord.Game("REC에서 대본 리딩"))

        self.setting_gether_dashboard.start()

    @tasks.loop(seconds=120)
    async def setting_gether_dashboard(self):
        print(123)
        global Gather_message
        try:
            await Gather_message.delete()
        except Exception as e:
            print(e)

        gather_channel = discord.utils.get(
            bot.get_all_channels(), id=config["GATHER_CHANNEL_ID"])
        gather_dashboard_embed = discord.Embed(
            description="아래 버튼을 이용해 배우를 모집할 수 있습니다. ", color=0xffff00)
        gather_dashboard_view = gether_view(timeout=120)
        gather_dashboard_embed.set_thumbnail(
            url="https://i.imgur.com/L1VJKG5.png")
        gather_dashboard_embed.set_image(url = "https://i.imgur.com/kuy5ynB.gif")
        gather_dashboard_embed.set_author(name=f"REC 배우 모집 기능 '모여 대시보드'",
                                          icon_url="https://i.imgur.com/JGSMPZ4.png")
        Gather_message = await gather_channel.send(embed=gather_dashboard_embed, view=gather_dashboard_view)


bot = MyBot()
bot.run(config['TOKEN'])
