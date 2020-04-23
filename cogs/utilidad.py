import os
import sys
import traceback
from datetime import datetime, timezone
from typing import Optional

import discord
from discord.ext import commands

from cogs.utils.embeds import jumbo_embed, simple_embed


def to_upper(argument):
    return argument.upper()


def to_lower(argument):
    return argument.lower()


class Utilidad(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.fmt = "%a %d-%m-%y %H:%M"

    @commands.has_permissions(manage_messages=True)
    @commands.command(aliases=["announce", "quote", "q"])
    async def anunciar(
        self,
        ctx,
        channel: Optional[discord.TextChannel] = None,
        embed: Optional[bool] = False,
        *,
        mensaje: str,
    ):
        """
        **Haz que el bot envie un mensaje por tí**
        `[channel]` Canal en donde se desea enviar el mensaje.
        `[embed]` Si desea enviar el mensaje en un embed (por defecto no)
        `<mensaje>` Texto que el bot enviará.
        """
        if not channel:
            channel = ctx.channel
        if embed:
            await channel.send(embed=simple_embed(mensaje))
        else:
            await channel.send(mensaje)

    @commands.has_any_role("Isleñes", 700566190665367622, 702724565649850508)
    @commands.command()
    async def jumbo(self, ctx, emoji: discord.PartialEmoji):
        """ 
        **Obten un emoji más grande**
        `<emoji>` El emoji a aumentar.
        """
        embed = jumbo_embed(emoji)
        await ctx.send(embed=embed)

    @commands.command()
    async def ping(self, ctx):
        """**Realiza un ping al cliente**"""
        description = f"🏓  |  **Pong!** ({self.bot.latency * 1000:.2f} ms)"
        await ctx.send(embed=simple_embed(description))

    @commands.command()
    async def uptime(self, ctx):
        """**Obtén el tiempo que el bot lleva en linea**"""
        delta = str(datetime.now() - self.bot.uptime).split(".")[0]
        description = f"Online for: **{delta}** {self.bot.omg}"
        await ctx.send(embed=simple_embed(description))

    @commands.is_owner()
    @commands.command(aliases=["r"])
    async def reiniciar(self, ctx):
        """**Reinicia el bot**"""
        for extension in os.listdir("./cogs"):
            if extension.endswith(".py"):
                cog = f"cogs.{extension[:-3]}"
                try:
                    self.bot.reload_extension(cog)
                except Exception:
                    print(f"Failed to load extension {cog}.", file=sys.stderr)
                    traceback.print_exc()
        description = f"{self.bot.omg} {self.bot.user.name} se está reiniciando..."
        await ctx.send(embed=simple_embed(description), delete_after=15)


def setup(bot):
    bot.add_cog(Utilidad(bot))
