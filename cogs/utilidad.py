from datetime import datetime, timezone

import discord
from discord.ext import commands

from cogs.utils.embeds import simple_embed, jumbo_embed


def to_upper(argument):
    return argument.upper()


def to_lower(argument):
    return argument.lower()


class Utilidad(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.fmt = "%a %d-%m-%y %H:%M"

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
        description = f"Online for: **{delta}** {self.bot.emoji}"
        await ctx.send(embed=simple_embed(description))


def setup(bot):
    bot.add_cog(Utilidad(bot))
