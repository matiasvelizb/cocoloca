import random

import discord
from discord.ext import commands

from cogs.utils.queries import get_bytes, get_json
from config import cat_api, dog_api


class Fun(commands.Cog, name="Diversión"):
    def __init__(self, bot):
        self.bot = bot

    @commands.cooldown(rate=1, per=3, type=commands.cooldowns.BucketType.member)
    @commands.command(aliases=["perrito"])
    async def dogpic(self, ctx):
        """**Obtén un tierna imagen de un perro**"""
        async with ctx.typing():
            choice = random.choices(["jpg", "gif"], [0.7, 0.3], k=1)[0]
            url = f"https://api.thedogapi.com/v1/images/search?mime_types={choice}"
            response = await get_json(url, {"X-API-KEY": dog_api})
            data = await get_bytes(response[0]["url"])
            await ctx.send(file=discord.File(data, f"{response[0]['id']}.{choice}"))

    @commands.cooldown(rate=1, per=3, type=commands.cooldowns.BucketType.member)
    @commands.command(aliases=["gatito"])
    async def catpic(self, ctx):
        """**Obtén un tierna imagen de un gato**"""
        async with ctx.typing():
            choice = random.choices(["jpg", "gif"], [0.7, 0.3], k=1)[0]
            url = f"https://api.thecatapi.com/v1/images/search?mime_types={choice}"
            response = await get_json(url, {"X-API-KEY": cat_api})
            data = await get_bytes(response[0]["url"])
            await ctx.send(file=discord.File(data, f"{response[0]['id']}.{choice}"))

    @commands.bot_has_permissions(manage_messages=True, add_reactions=True)
    @commands.has_any_role(700566190665367622, 702724565649850508, 715302998464790618)
    @commands.command(aliases=["funar"])
    async def funa(self, ctx, message: discord.Message):
        """
        **Funa el mensaje de alguien**
        <message>: El mensaje a ser funado.
        """
        await ctx.message.delete()
        reactions = ["🇫", "🇺", "🇳", "🇦", "🇩", "🇴"]
        for emoji in reactions:
            await message.add_reaction(emoji)


def setup(bot):
    bot.add_cog(Fun(bot))
