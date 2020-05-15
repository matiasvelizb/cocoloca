import random

import discord
from discord.ext import commands

from cogs.utils.embeds import horoscope_embed
from cogs.utils.queries import get_bytes, get_json, get_text
from config import cat_api


def to_lower(argument):
    return argument.lower()


class Fun(commands.Cog, name="Diversión"):
    def __init__(self, bot):
        self.bot = bot

    @commands.cooldown(rate=1, per=3, type=commands.cooldowns.BucketType.member)
    @commands.command(aliases=["gatito", "meow"])
    async def catpic(self, ctx):
        """**Obtén una tierna imagen de un gato**"""
        async with ctx.typing():
            choice = random.choices(["jpg", "gif"], [0.7, 0.3], k=1)[0]
            url = f"https://api.thecatapi.com/v1/images/search?mime_types={choice}"
            response = await get_json(url, {"X-API-KEY": cat_api})
            data = await get_bytes(response[0]["url"])
            await ctx.send(file=discord.File(data, f"{response[0]['id']}.{choice}"))

    @commands.cooldown(rate=1, per=3, type=commands.cooldowns.BucketType.member)
    @commands.command(aliases=["perrito", "woof"])
    async def dogpic(self, ctx):
        """**Obtén una tierna imagen de un perro**"""
        async with ctx.typing():
            response = await get_json("https://random.dog/woof.json")
            url = response["url"]
            filename = url.split("https://random.dog/")[1]
            filesize = ctx.guild.filesize_limit if ctx.guild else 8388608
            if response["fileSizeBytes"] >= filesize:
                await ctx.send(f"Este perrito está muy pesado {self.bot.omg}\n{url}")
            else:
                data = await get_bytes(url)
                await ctx.send(file=discord.File(data, filename=filename))

    @commands.cooldown(rate=1, per=3, type=commands.cooldowns.BucketType.member)
    @commands.command(aliases=["h", "horoscope"])
    async def horoscopo(self, ctx, signo: to_lower):
        async with ctx.typing():
            response = await get_json("https://api.adderou.cl/tyaas/")
            if signo in response["horoscopo"]:
                embed = horoscope_embed(response["horoscopo"][signo])
                await ctx.send(embed=embed)
            else:
                error = f"{signo.title()} no es un signo valido {self.bot.omg}"
                await ctx.send(error, delete_after=7)

    @commands.cooldown(rate=1, per=3, type=commands.cooldowns.BucketType.member)
    @commands.command(aliases=["shiba", "shibe"])
    async def shibapic(self, ctx):
        """**Obtén una tierna imagen de un shiba inu**"""
        async with ctx.typing():
            response = await get_json("http://shibe.online/api/shibes")
            filename = response[0].split("https://cdn.shibe.online/shibes/")[1]
            data = await get_bytes(response[0])
            await ctx.send(file=discord.File(data, filename=filename))


def setup(bot):
    bot.add_cog(Fun(bot))
