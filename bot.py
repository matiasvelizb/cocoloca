import asyncio
import json
import locale
import logging
import os
import sys
import traceback
from datetime import datetime

import asyncpg
import discord
from discord.ext import commands

import config


async def run():
    locale.setlocale(locale.LC_TIME, "es_CL")
    logging.basicConfig(
        filename="bot.log",
        filemode="w",
        level=logging.INFO,
        format="%(asctime)s:%(levelname)s:%(message)s",
        datefmt="%d-%m-%Y %H:%M:%S",
    )
    db = await asyncpg.create_pool(**config.credentials)
    bot = Bot(db=db)
    try:
        await bot.start(config.discord_token)
    except KeyboardInterrupt:
        await bot.logout()


class Bot(commands.Bot):
    def __init__(self, **kwargs):
        super().__init__(command_prefix=config.prefix, case_insersitive=True)
        self.db = kwargs.pop("db")
        # Cargar extensiones
        for extension in os.listdir("./cogs"):
            if extension.endswith(".py"):
                cog = f"cogs.{extension[:-3]}"
                try:
                    self.load_extension(cog)
                except Exception as e:
                    logging.error(e)

    async def on_ready(self):
        # Emojis
        self.think = self.get_emoji(702729662413013102)
        self.omg = self.get_emoji(702729661997645834)
        self.love = self.get_emoji(702729661385539667)
        # Cargar informacion de aldeanos
        with open("villagers.json", encoding="utf-8") as data:
            self.villagers = json.load(data)
        # Uptime
        if not hasattr(self, "uptime"):
            self.uptime = datetime.now()
        info = f"Ready: {self.user} ID: {self.user.id} Guilds: {len(self.guilds)}"
        logging.info(info)

    async def on_message(self, message):
        # Ignorar bots y DMs
        if message.author.bot or not message.guild:
            return
        await self.process_commands(message)

    async def on_command_error(self, ctx, error):
        name, hint = ctx.author.name, None
        if isinstance(error, commands.CommandOnCooldown):
            hint = f"No tan rapido {name}, Intenta de nuevo en {error.retry_after:.1f} segundos."
        elif isinstance(error, commands.MaxConcurrencyReached):
            hint = f"Si quieres ver una lista nueva, cierra la lista anterior con ⏹."
        elif isinstance(error, commands.MissingAnyRole):
            hint = f"Disculpa {name}, este comando valido solo para nuestros Isleñes."
        elif isinstance(error, commands.MissingPermissions):
            hint = f"No tienes permisos para usar este comando {name}."
        elif isinstance(error, commands.BadArgument):
            hint = "Uno de tus parametros no es valido."
        elif isinstance(error, commands.MissingRequiredArgument):
            hint = f"Te falta un parametro obligatorio {name}."

        if hint:
            await ctx.send(hint, delete_after=10)
        else:
            logging.error(error)

        if isinstance(error, commands.CommandInvokeError):
            text = f"In {ctx.command.qualified_name}: {error.original.__class__.__name__}: {error.original}\n"
            etype = type(error)
            trace = error.__traceback__
            verbosity = 4
            lines = traceback.format_exception(etype, error, trace, verbosity)
            text += "".join(lines)
            logging.error(text)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
