import discord
from discord.ext import commands

import os
import json
import sys
import datetime

with open(f"config.json", "r", encoding="utf-8-sig") as json_file:
    config = json.load(json_file)

with open(f"color.json", "r", encoding="utf-8-sig") as json_file:
    color = json.load(json_file)


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
        ]

    async def setup_hook(self):
        for ext in self.initial_extension:
            await self.load_extension(ext)

        await bot.tree.sync(guild=discord.Object(id=827801772143017994))

    async def on_ready(self):
        # 역할 채널 세팅
        role_channel = discord.utils.get(
            bot.get_all_channels(), id=config["ROLE_CHANNEL_ID"])

        await role_channel.purge(limit=None)

        role_init_embed = discord.Embed(
            title="환영합니다. REC 서버입니다.", description="📌 ┃서버에 입장 하기 전, 3가지 중요한 설문에 참여 하시면 각 설문마다 해당 역할이 추가됩니다.\n\n📛 ┃설문에 응하지 않으시면 서버를 이용하실 수 없습니다.")
        await role_channel.send(embed=role_init_embed)

        # 역할 채널 세팅 - 성별
        gender_embed = discord.Embed(title=":red_circle: 성별이 어떻게 되시나요?")
        gender_view = discord.ui.View(timeout=None)
        man_button = discord.ui.Button(label="남성 배우")

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

        woman_button = discord.ui.Button(label="여성 배우")

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

        # 역할 채널 세팅 - 활동

        activeity_embed = discord.Embed(title=":red_circle:  어떤 활동을 원하시나요?")
        activeity_view = discord.ui.View(timeout=None)

        acting_button = discord.ui.Button(label="연기")

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

        writer_button = discord.ui.Button(label="작가")

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

        listener_button = discord.ui.Button(label="청취")

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

        # 역할 채널 세팅 - 장르

        preference_embed = discord.Embed(
            title=":red_circle:  어떤 장르를 선호하시나요?")
        preference_view = discord.ui.View(timeout=None)

        radio_drama_button = discord.ui.Button(label="라디오 드라마")

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

        animation_button = discord.ui.Button(label="애니매이션")

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

        narration_button = discord.ui.Button(label="독백/내레이션")

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

        media_button = discord.ui.Button(label="매체연기")

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

        # 역할 채널 세팅 - 대배우

        grant_actor_embed = discord.Embed(
            title="", description=": yellow_square: 설문에 응해주셔서 감사드립니다.\n: arrow_down: 아래에서: white_check_mark: 선택해 주시면 서버에 입장됩니다.\n: name_badge: 입장 후에는 현 페이지로 돌아올 수 없습니다.")
        grant_actor_view = discord.ui.View(timeout=None)

        grant_actor_button = discord.ui.Button(label="체크")

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

        print("=========================")
        print(f"대본 봇 Login 완료")
        print(f"bot name : {self.user.name}")
        print(f"bot id : {self.user.id}")
        print(f"discord.py version : {discord.__version__}")
        print("=========================")
        await self.change_presence(status=discord.Status.online, activity=discord.Game("REC에서 대본 리딩"))


bot = MyBot()
bot.run(config['TOKEN'])
