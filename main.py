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
            "Cogs.대본"
        ]

    async def setup_hook(self):
        for ext in self.initial_extension:
            await self.load_extension(ext)

        await bot.tree.sync(guild=discord.Object(id=827801772143017994))

    async def on_ready(self):
        print("=========================")
        print(f"대본 봇 Login 완료")
        print(f"bot name : {self.user.name}")
        print(f"bot id : {self.user.id}")
        print(f"discord.py version : {discord.__version__}")
        print("=========================")
        await self.change_presence(status=discord.Status.online, activity=discord.Game("REC에서 대본 리딩"))


bot = MyBot()
bot.run(config['TOKEN'])
