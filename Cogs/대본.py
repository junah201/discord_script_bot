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

    @app_commands.command(name="모여", description="특정 역할을 가지고 있는 모두를 멘션한 후, 대본 리딩에 필요한 배우를 모집할 수 있습니다.")
    async def 모여(self, interaction: Interaction):
        embed = discord.Embed(color=0x62c1cc)
        embed.title = "💌 캐스팅 시작"
        # .\n[<:cst:840538932906950682> : 참여 <:RED:841252822795550751> : 참여취소 <:can:841253094674399243> : 완료]"
        embed.description = "무대 참여 의사를 확인합니다"
        embed.add_field(name="🍺⠀남배우", value=" 《⠀공 석⠀》")
        embed.add_field(name="💋⠀여배우", value=" 《⠀공 석⠀》")
        embed.set_image(
            url="https://media.discordapp.net/attachments/424831572861124619/549533764880171018/da41590cda439e68.gif")
        embed.set_author(name=f'{interaction.user.name}',
                         icon_url="https://cdn.discordapp.com/attachments/827931592932065332/841197513561735168/6979bf056826de22.png")
        embed.set_thumbnail(url=str(interaction.user.display_avatar))

        view = discord.ui.View()

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
                    return await interaction.response.send_message("이미 등록되어있습니다.")

                man_users.append(interaction.user.name)

                embed.set_field_at(
                    0, name=f"🍺⠀남배우 {len(man_users)}분", value='\n'.join(man_users))
            elif is_woman:
                if embed.fields[1].value == " 《⠀공 석⠀》":
                    woman_users = []
                else:
                    woman_users = embed.fields[1].value.split('\n')

                if interaction.user.name in woman_users:
                    return await interaction.response.send_message("이미 등록되어있습니다.")

                woman_users.append(interaction.user.name)

                embed.set_field_at(
                    1, name=f"💋⠀여배우 {len(woman_users)}분", value='\n'.join(woman_users))

            await interaction.channel.send(f"{interaction.user.mention}님이 참여하셨습니다")
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
                        embed.set_field_at(0, name=f"🍺⠀남배우", value=" 《⠀공 석⠀》")
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
                        embed.set_field_at(1, name=f"💋⠀여배우", value=" 《⠀공 석⠀》")
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
                    title="캐스팅 완료", description=f"총 {len(man_users)}남{len(woman_users)}여", color=0x62c1cc)

                ending_view = discord.ui.View()

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

                selects = discord.ui.Select()

                if not datas.keys():
                    selects.add_option(label="해당 인원의 대본이 없음")

                for type in datas.keys():
                    selects.add_option(label=type)

                async def select_callback(interaction: interaction) -> None:
                    script_type = selects.values
                    script_embed, script_view = await 대본생성(script_type, 남, 여)

                    await interaction.response.send_message(embed=script_embed, view=script_view)

                selects.callback = select_callback

                ending_view = discord.ui.View()
                ending_view.add_item(selects)

                await interaction.channel.send(embed=ending_embed, view=ending_view)
            else:
                await interaction.response.send_message(f"마무리 버튼은 개설자인 {embed.author.name} 님만 사용할 수 있습니다.", ephemeral=True)

        ending_button.callback = ending_button_callback
        view.add_item(ending_button)

        await interaction.response.send_message(content=f"{interaction.user.mention}님께서 새로운 무대를 여셨습니다. <@&827887094307356673>", embed=embed, view=view)

    @app_commands.command(name="대본", description="인원을 설정 후 대본 목록을 보여줍니다.")
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

    @app_commands.command(name="대본추가", description="따로 등록하고 싶은 대본을 추가합니다.")
    async def 대본추가(self, interaction: Interaction, 대본명: str, 링크: str, 남: int, 여: int, 공: int, 대본종류: str):
        with open(f"./DB/Script/Script.json", "r", encoding="utf-8-sig") as json_file:
            Scripts = json.load(json_file)

        is_exist = None

        for key in Scripts.keys():
            if Scripts[key]['link'] == 링크:
                is_exist = key
                break

        async def regist_script():
            filename = f"{남}남{여}여{공}공.json"

            if filename in await 대본목록():
                with open(f"./DB/Script/{filename}", "r", encoding="utf-8-sig") as json_file:
                    datas = json.load(json_file)

                if 대본종류 not in datas.keys():
                    datas[대본종류] = {}

                datas[대본종류][str(config["NEW_IDX"])] = {
                    "name": 대본명,
                    "link": 링크,
                    "type": {
                        "name": f"{남}남{여}여{공}공",
                        "남": 남,
                        "여": 여,
                        "공": 공
                    },
                    "rating": 0,
                    "rating_users": 0,
                    "adder": interaction.user.name,
                    "adder_id": interaction.user.id,
                    "time": datetime.datetime.today().strftime('%c')
                }

            else:
                datas = {}

                datas[대본종류] = {}

                datas[대본종류][str(config["NEW_IDX"])] = {
                    "name": 대본명,
                    "link": 링크,
                    "type": 대본종류,
                    "gender": {
                        "name": f"{남}남{여}여{공}공",
                        "남": 남,
                        "여": 여,
                        "공": 공
                    },
                    "rating": 0,
                    "rating_users": 0,
                    "adder": interaction.user.name,
                    "adder_id": interaction.user.id,
                    "time": datetime.datetime.today().strftime('%c')
                }

            with open(f"./DB/Script/{filename}", "w", encoding="utf-8-sig") as json_file:
                json.dump(datas, json_file, ensure_ascii=False, indent=4)

            with open(f"./DB/Script/Script.json", "r", encoding="utf-8-sig") as json_file:
                Scripts = json.load(json_file)

            Scripts[str(config["NEW_IDX"])] = {
                "name": 대본명,
                "type": 대본종류,
                "gender": f"{남}남{여}여{공}공",
                "link": 링크
            }

            with open(f"./DB/Script/Script.json", "w", encoding="utf-8-sig") as json_file:
                json.dump(Scripts, json_file, ensure_ascii=False, indent=4)

            embed = discord.Embed(
                title=f"{대본명}", description=f"성공적으로 대본이 추가되었습니다.\n\n대본명 : {대본명}\n대본종류 : {대본종류}\n성비 : {남}남{여}여{공}공\n추가자 : {interaction.user.name}\n추가시간 : {datetime.datetime.today().strftime('%c')}\n아이디 : {config['NEW_IDX']}\n링크 : {링크}", color=0x62c1cc)

            config["NEW_IDX"] += 1

            with open(f"config.json", "w", encoding="utf-8-sig") as json_file:
                json.dump(config, json_file, ensure_ascii=False, indent=4)

            return embed

        if is_exist == None:
            await interaction.response.send_message(embed=await regist_script())
        else:
            embed = discord.Embed(
                title="중복 경고", description=f"`{is_exist}`\n원본 : {Scripts[is_exist]['link']}\n추가 : {링크}", color=0xFF0000)
            add_button = discord.ui.Button(label="계속 추가하기")

            async def add_button_callback(interaction: Interaction):
                await interaction.response.send_message(embed=await regist_script())

            add_button.callback = add_button_callback

            view = discord.ui.View()
            view.add_item(add_button)

            await interaction.response.send_message(embed=embed, view=view)

    @app_commands.command(name="대본삭제", description="등록 되어 있는 대본의 ID를 이용해, 선택한 대본을 삭제할 수 있습니다.")
    async def 대본삭제(self, interaction: Interaction, 대본아이디: str):
        with open(f"./DB/Script/Script.json", "r", encoding="utf-8-sig") as json_file:
            script_list = json.load(json_file)

        if str(대본아이디) not in script_list.keys():
            return await interaction.response.send_message("존재하지 않는 대본입니다.", ephemeral=True)

        with open(f"./DB/Script/{script_list[str(대본아이디)]['gender']}.json", "r", encoding="utf-8-sig") as json_file:
            script_data = json.load(json_file)
        try:
            tmp = script_list.pop(str(대본아이디))
        except:
            pass
        try:
            tmp.update(script_data[tmp['type']][str(대본아이디)])
            script_data[tmp['type']].pop(str(대본아이디))
        except:
            pass

        with open(f"./DB/Script/Script.json", "w", encoding="utf-8-sig") as json_file:
            json.dump(script_list, json_file, ensure_ascii=False, indent=4)

        with open(f"./DB/Script/{tmp['gender']}.json", "w", encoding="utf-8-sig") as json_file:
            json.dump(script_data, json_file, ensure_ascii=False, indent=4)

        embed = discord.Embed(
            title="삭제 완료", description=f"정상적으로 삭제 완료 하였습니다.\n```대본명 : {tmp['name']}\n대본종류 : {tmp['type']['name']}\n대본아이디 : {대본아이디}\n추가자 : {tmp['adder']}```")
        embed.set_author(name=interaction.user.name)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="대본평가", description="리딩에서 감명 깊은 연기를 선보여준 배우에게 1점을 부여합니다. (하루에 1회 사용 가능)")
    async def 대본평가(self, interaction: Interaction, 대본아이디: str, 점수: int):
        with open(f"./DB/User/users.json", "r", encoding="utf-8-sig") as json_file:
            user_data = json.load(json_file)

        with open(f"./DB/Script/Script.json", "r", encoding="utf-8-sig") as json_file:
            script_data = json.load(json_file)

        if 점수 not in [1, 2, 3, 4, 5]:
            return await interaction.response.send_message("점수는 1점에서 5점 사이여야 합니다.", ephemeral=True)

        if str(interaction.user.id) not in user_data.keys():
            user_data[str(interaction.user.id)] = {
                "name": interaction.user.name,
                "grade": 0,
                "last_evaluate": "미평가",
                "review": {},
                "warning": 0
            }

        with open(f"./DB/Script/Script.json", "r", encoding="utf-8-sig") as json_file:
            script_list = json.load(json_file)

        if str(대본아이디) not in script_list.keys():
            return await interaction.response.send_message("존재하지 않는 대본입니다.", ephemeral=True)

        with open(f"./DB/Script/{script_list[str(대본아이디)]['gender']}.json", "r", encoding="utf-8-sig") as json_file:
            script_data = json.load(json_file)

        if 대본아이디 in user_data[str(interaction.user.id)]["review"].keys():
            await interaction.response.send_message(f"이미 평가한 대본이므로 평가를 수정하였습니다.\n({user_data[str(interaction.user.id)]['review'][대본아이디]}점 -> {점수}점)", ephemeral=True)
            script_data[script_list[대본아이디]["type"]
                        ][대본아이디]["rating"] -= user_data[str(interaction.user.id)]['review'][대본아이디]
            script_data[script_list[대본아이디]["type"]][대본아이디]["rating"] += 점수
        else:
            script_data[script_list[대본아이디]["type"]][대본아이디]["rating"] += 점수
            script_data[script_list[대본아이디]["type"]][대본아이디]["rating_users"] += 1
            user_data[str(interaction.user.id)]['review'][대본아이디] = 점수
            await interaction.response.send_message(f"{점수}점으로 평가하였습니다.", ephemeral=True)

        with open(f"./DB/User/users.json", "w", encoding="utf-8-sig") as json_file:
            json.dump(user_data, json_file, ensure_ascii=False, indent=4)

        with open(f"./DB/Script/{script_list[str(대본아이디)]['gender']}.json", "w", encoding="utf-8-sig") as json_file:
            json.dump(script_data, json_file, ensure_ascii=False, indent=4)

    @app_commands.command(name="대본검색", description="등록 되어 있는 대본을 제목 또는 링크를 통해 찾아 볼 수 있습니다.")
    async def 대본검색(self, interaction: Interaction, 검색: str):
        with open(f"./DB/Script/Script.json", "r", encoding="utf-8-sig") as json_file:
            script_list = json.load(json_file)

        result = []

        for key in script_list.keys():
            if 검색 in script_list[key]["name"]:
                result.append((key, script_list[key]))
            elif 검색 in script_list[key]["link"]:
                result.append((key, script_list[key]))

        if len(result) == 0:
            return await interaction.response.send_message("검색 결과가 없습니다.", ephemeral=True)

        embed = discord.Embed(
            title=f"{검색} 검색 결과", description=f"총 {len(result)}개의 결과가 있습니다.\n\n", color=0x62c1cc
        )

        for key, data in result:
            embed.add_field(name=f"{data['name']}",
                            value=f">>> {data['type']}   {data['gender']} ({key})\n{data['link']}", inline=False)

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="대본상세정보", description="등록된 대본의 ID를 통해, 대본의 상세한 정보를 열람할 수 있습니다.")
    async def 대본상세정보(self, interaction: Interaction, id: int):
        with open(f"./DB/Script/Script.json", "r", encoding="utf-8-sig") as json_file:
            script_list = json.load(json_file)

        if str(id) not in script_list.keys():
            return await interaction.response.send_message("존재하지 않는 대본입니다.", ephemeral=True)

        with open(f"./DB/Script/{script_list[str(id)]['gender']}.json", "r", encoding="utf-8-sig") as json_file:
            script_data = json.load(json_file)

        script = script_data[script_list[str(id)]['type']][str(id)]

        if script['rating'] == 0:
            embed = discord.Embed(
                title=f"{script_list[str(id)]['name']}", description=f"종류 : {script_list[str(id)]['type']}\n성별 : {script_list[str(id)]['gender']}\n링크 : {script['link']}\n평점 : {script['rating']}점 ({script['rating_users']}명)\n추가자 : {script['adder']} ({script['adder_id']})\n추가 시간 : {script['time']}", color=0x62c1cc)
        else:
            embed = discord.Embed(
                title=f"{script_list[str(id)]['name']}", description=f"종류 : {script_list[str(id)]['type']}\n성별 : {script_list[str(id)]['gender']}\n링크 : {script['link']}\n평점 : {round(script['rating']/script['rating_users'], 1)}점 ({script['rating_users']}명)\n추가자 : {script['adder']} ({script['adder_id']})\n추가 시간 : {script['time']}", color=0x62c1cc)

        await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(
        대본(bot),
        guilds=[Object(id=config['GUILD_ID'])]
    )
