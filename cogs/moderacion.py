import os
import sys
import traceback
from typing import Optional

import discord
from discord.ext import commands

from cogs.utils.embeds import simple_embed


class Moderacion(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

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

    @commands.is_owner()
    @commands.command(aliases=["r"], hidden=True)
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
        description = f"{self.bot.user.name} is restarting..."
        await ctx.send(embed=simple_embed(description), delete_after=15)


def setup(bot):
    bot.add_cog(Moderacion(bot))
