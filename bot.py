import asyncio
import json
import locale
import os
import sys
import traceback
from datetime import datetime

import asyncpg
import discord
from discord.ext import commands

import config


async def run():
    db = await asyncpg.create_pool(**config.credentials)
    bot = Bot(db=db, allowed=config.allowed_channels)
    try:
        await bot.start(config.discord_token)
    except KeyboardInterrupt:
        await bot.logout()


class Bot(commands.Bot):
    def __init__(self, **kwargs):
        super().__init__(command_prefix=config.prefix, case_insersitive=True)
        self.db = kwargs.pop("db")
        self.allowed = kwargs.pop("allowed")
        # Cargar extensiones
        for extension in os.listdir("./cogs"):
            if extension.endswith(".py"):
                cog = f"cogs.{extension[:-3]}"
                try:
                    self.load_extension(cog)
                except Exception:
                    print(f"Failed to load extension {cog}.", file=sys.stderr)
                    traceback.print_exc()

    async def on_ready(self):
        locale.setlocale(locale.LC_ALL, "es_CL.utf8")
        # Emojis
        self.omg = self.get_emoji(699124939965333585)
        self.question = self.get_emoji(699124939676057661)
        # Informacion de las guias
        with open("data.json", encoding='utf-8') as data:
            self.guias = json.load(data)
        # Uptime
        if not hasattr(self, "uptime"):
            self.uptime = datetime.now()
        print(f"Ready: {self.user} ID: {self.user.id}")

    async def on_message(self, message):
        # Ignorar bots y DMs
        if message.author.bot or not message.guild:
            return
        # Solo aceptar comandos en los canales admitidos
        if message.channel.id not in self.allowed:
            return
        await self.process_commands(message)

    async def on_command_error(self, ctx, e):
        # Hints
        hint, name = None, ctx.author.name
        if isinstance(e, commands.CommandOnCooldown):
            hint = f"No tan rapido {name}, Intenta de nuevo en {e.retry_after:.1f} segundos."
        elif isinstance(e, commands.MissingPermissions):
            hint = f"No tienes permisos para usar este comando {name}."
        elif isinstance(e, commands.BadArgument):
            hint = "Uno de tus parametros no es valido."
        elif isinstance(e, commands.MissingRequiredArgument):
            hint = f"Te falta un parametro obligatorio {name}."
        if hint:
            await ctx.send(hint)
            await ctx.send_help(ctx.command)
        # Traceback
        error = f"In {ctx.command.qualified_name}: {e.original.__class__.__name__}: {e.original}"
        if isinstance(e, commands.CommandInvokeError):
            print(error, file=sys.stderr)
            traceback.print_tb(e.original.__traceback__)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
