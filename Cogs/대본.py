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

Scripts = {}


async def 대본목록() -> list:
    db_list = []
    for file in os.listdir("./DB/Script"):
        if file.endswith(".json"):
            db_list.append(file)
    return db_list


async def 대본생성(types: list, man: int, woman: int):
    datas = {}

    for file in await 대본목록():
        if file == "Script.json":
            continue
        if len(file) == 11 and int(file[0]) <= man and int(file[2]) <= woman and int(file[0]) + int(file[2]) + int(file[4]) == man + woman:
            with open(f"./DB/Script/{file}", "r", encoding="utf-8-sig") as json_file:
                tmp = json.load(json_file)
                for type in types:
                    if tmp.get(type):
                        datas.update(tmp.get(type))

    global idx
    global max_idx

    idx = 1

    if len(datas) % 10 == 0:
        max_idx = len(datas) // 10
    else:
        max_idx = len(datas) // 10 + 1

    numbers = [
        "<:A01:854342175226986579>",
        "<:A02:854342175437488138>",
        "<:A03:854342175478775818>",
        "<:A04:854342175487819806>",
        "<:A05:854342175448760361>",
        "<:A06:854342175477989386>",
        "<:A07:854342175507742750>",
        "<:A08:854342175751798834>",
        "<:A09:854342175219384341>",
        "<:A10:854342175496470548>"
    ]

    def 대본내용생성(datas: dict, numbers: list, idx: int, max_idx: int):
        tmp_msg = ""

        if len(datas.keys()) <= 10:
            for key, num in zip(datas.keys(), numbers[:len(datas.keys())]):
                if datas[key]['rating'] == 0:
                    tmp_msg += f"{num} [{datas[key]['name']}]({datas[key]['link']}) (id : {key}) (미평가)\n"
                else:
                    tmp_msg += f"{num} [{datas[key]['name']}]({datas[key]['link']}) (id : {key}) {''.join(['❤️' for i in range(round(datas[key]['rating'] // datas[key]['rating_users']))])}{''.join(['🤍' for i in range(round(5 - (datas[key]['rating'] // datas[key]['rating_users'])))])}\n"
        else:
            for key, num in zip(list(datas.keys())[10*idx - 10:10*idx], numbers):
                if datas[key]['rating'] == 0:
                    tmp_msg += f"{num} [{datas[key]['name']}]({datas[key]['link']}) (id : {key}) (미평가)\n"
                else:
                    tmp_msg += f"{num} [{datas[key]['name']}]({datas[key]['link']}) (id : {key}) {''.join(['❤️' for i in range(round(datas[key]['rating'] // datas[key]['rating_users']))])}{''.join(['🤍' for i in range(round(5 - (datas[key]['rating'] // datas[key]['rating_users'])))])}\n"

        if tmp_msg == "":
            tmp_msg = "없음"

        return tmp_msg

    id = datetime.datetime.today().strftime('%c')

    embed = discord.Embed(title=f"📑대본  [{man}남{woman}녀]  {types}", description=대본내용생성(
        datas, numbers, idx, max_idx), color=0x62c1cc)
    embed.set_footer(text=f"{1} / {max_idx}   {id}")

    global Scripts

    Scripts[id] = {
        "idx": idx,
        "max_idx": max_idx,
        "man": man,
        "woman": woman,
        "add_time": datetime.datetime.now()
    }

    view = discord.ui.View()

    front_back_button = discord.ui.Button(
        emoji="⏪", style=discord.ButtonStyle.primary)
    front_back_button.disabled = True

    async def front_back_button_callback(interaction: discord.Interaction):
        global Scripts
        id = embed.footer.text[-24:]

        Scripts[id]['idx'] = 1

        new_embed = discord.Embed(title=embed.title, description=대본내용생성(
            datas, numbers, Scripts[id]['idx'], Scripts[id]['max_idx']), color=embed.color)
        new_embed.set_footer(
            text=f"{Scripts[id]['idx']} / {Scripts[id]['max_idx']}   {id}")

        if Scripts[id]['idx'] == Scripts[id]['max_idx']:
            next_button.disabled = True
            front_next_button.disabled = True
        else:
            next_button.disabled = False
            front_next_button.disabled = False

        if Scripts[id]['idx'] == 1:
            back_button.disabled = True
            front_back_button.disabled = True
        else:
            back_button.disabled = False
            front_back_button.disabled = False

        await interaction.response.edit_message(embed=new_embed, view=view)

    front_back_button.callback = front_back_button_callback
    view.add_item(front_back_button)

    back_button = discord.ui.Button(
        emoji="◀", style=discord.ButtonStyle.primary)
    back_button.disabled = True

    async def back_button_callback(interaction: discord.Interaction) -> None:
        global Scripts
        id = embed.footer.text[-24:]

        Scripts[id]['idx'] -= 1

        new_embed = discord.Embed(title=embed.title, description=대본내용생성(
            datas, numbers, Scripts[id]['idx'], Scripts[id]['max_idx']), color=embed.color)
        new_embed.set_footer(
            text=f"{Scripts[id]['idx']} / {Scripts[id]['max_idx']}   {id}")

        if Scripts[id]['idx'] == Scripts[id]['max_idx']:
            next_button.disabled = True
            front_next_button.disabled = True
        else:
            next_button.disabled = False
            front_next_button.disabled = False

        if Scripts[id]['idx'] == 1:
            back_button.disabled = True
            front_back_button.disabled = True
        else:
            back_button.disabled = False
            front_back_button.disabled = False

        await interaction.response.edit_message(embed=new_embed, view=view)

    back_button.callback = back_button_callback
    view.add_item(back_button)

    next_button = discord.ui.Button(
        emoji="▶", style=discord.ButtonStyle.primary)
    if max_idx == 1:
        next_button.disabled = True

    delete_button = discord.ui.Button(
        emoji="⬜", style=discord.ButtonStyle.danger)

    async def delete_button_callback(interaction: discord.Interaction) -> None:
        await interaction.message.delete()
        global Scripts
        id = embed.footer.text[-24:]
        Scripts.pop(id)

    delete_button.callback = delete_button_callback

    view.add_item(delete_button)

    async def next_button_callback(interaction: discord.Interaction):
        global Scripts
        id = embed.footer.text[-24:]

        Scripts[id]['idx'] += 1

        new_embed = discord.Embed(title=embed.title, description=대본내용생성(
            datas, numbers, Scripts[id]['idx'], Scripts[id]['max_idx']), color=embed.color)
        new_embed.set_footer(
            text=f"{Scripts[id]['idx']} / {Scripts[id]['max_idx']}   {id}")

        if Scripts[id]['idx'] == Scripts[id]['max_idx']:
            next_button.disabled = True
            front_next_button.disabled = True
        else:
            next_button.disabled = False
            front_next_button.disabled = False

        if Scripts[id]['idx'] == 1:
            back_button.disabled = True
            front_back_button.disabled = True
        else:
            back_button.disabled = False
            front_back_button.disabled = False

        await interaction.response.edit_message(embed=new_embed, view=view)

    next_button.callback = next_button_callback
    view.add_item(next_button)

    front_next_button = discord.ui.Button(
        emoji="⏩", style=discord.ButtonStyle.primary)

    if max_idx == 1:
        front_next_button.disabled = True

    async def front_next_button_callback(interaction: discord.Interaction):
        global Scripts
        id = embed.footer.text[-24:]

        Scripts[id]['idx'] = Scripts[id]['max_idx']

        new_embed = discord.Embed(title=embed.title, description=대본내용생성(
            datas, numbers, Scripts[id]['idx'], Scripts[id]['max_idx']), color=embed.color)
        new_embed.set_footer(
            text=f"{Scripts[id]['idx']} / {Scripts[id]['max_idx']}   {id}")

        if Scripts[id]['idx'] == Scripts[id]['max_idx']:
            next_button.disabled = True
            front_next_button.disabled = True
        else:
            next_button.disabled = False
            front_next_button.disabled = False

        if Scripts[id]['idx'] == 1:
            back_button.disabled = True
            front_back_button.disabled = True
        else:
            back_button.disabled = False
            front_back_button.disabled = False

        await interaction.response.edit_message(embed=new_embed, view=view)

    front_next_button.callback = front_next_button_callback
    view.add_item(front_next_button)

    return embed, view


class 대본(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="대본")
    async def 대본(self, interaction: Interaction, 남: int, 여: int) -> None:
        datas = {}

        for file in await 대본목록():
            if file == "Script.json":
                continue
            if len(file) == 11 and int(file[0]) <= 남 and int(file[2]) <= 여 and int(file[0]) + int(file[2]) + int(file[4]) == 남 + 여:
                with open(f"./DB/Script/{file}", "r", encoding="utf-8-sig") as json_file:
                    datas.update(json.load(json_file))

        selects = discord.ui.Select()

        if not datas.keys():
            return await interaction.response.send_message(f"존재하는 대본이 없습니다. ({남}남{여}여)", ephemeral=True)

        for type in datas.keys():
            selects.add_option(label=type)

        async def select_callback(interaction: interaction) -> None:
            script_type = selects.values
            script_embed, script_view = await 대본생성(script_type, 남, 여)

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
            title="대본 선택", description="대본을 선택해주세요.", color=0x62c1cc)
        embed.set_footer(text=f"{남}남{여}여")
        embed.set_author(name=f'{interaction.user.name}')
        view = discord.ui.View()
        view.add_item(selects)
        view.add_item(delete_button)
        await interaction.response.send_message(embed=embed, view=view)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(
        대본(bot),
        guilds=[Object(id=config['GUILD_ID'])]
    )
