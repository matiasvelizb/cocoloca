import aiohttp
import discord
from bs4 import BeautifulSoup
from discord.ext import commands
import json

from cogs.utils.embeds import page_embed, villager_embed
from cogs.utils.queries import get_soup, get_bytes
from cogs.utils.paginator import Paginator


class Nintendo(commands.Cog, name="Animal Crossing"):
    def __init__(self, bot):
        self.bot = bot

    @commands.bot_has_permissions(manage_messages=True)
    @commands.cooldown(rate=1, per=7, type=commands.BucketType.user)
    @commands.command(aliases=["a", "char", "vil", "villager", "wiki"])
    async def aldeano(self, ctx, *, aldeano: str):
        """
        **Obtén información de algún aldeano de ACNH**
        <aldeano>: Nombre en **inglés** del aldeano a buscar.
        """
        url = "https://nookipedia.com/wiki/" + aldeano.title()
        content = f"{self.bot.question} ┆ Buscando información de {aldeano.title()}."
        info_msg = await ctx.send(content)

        async with ctx.typing():
            # Descargar wiki
            soup = await get_soup(url)
            if not soup:
                aux = f"{self.bot.omg} ┆ Error al obtener los datos desde la Wiki."
                await info_msg.edit(content=aux)
            # Enviar embed
            embed = villager_embed(soup)
            try:
                await ctx.send(embed=embed)
            except discord.HTTPException:
                aux = f"{self.bot.omg} ┆ {aldeano.title()} no es un aldeano valido."
                await info_msg.edit(content=aux)
            else:
                await info_msg.delete()

    @commands.command()
    async def patrones(self, ctx):
        """**Obtén información de como plantar tus flores**"""
        pages = [
            page_embed(p["title"], p["description"], p["image_url"], p["footer"])
            for p in self.bot.guias["flores"]["patrones"]
        ]
        patrones = Paginator(ctx, None, pages)
        await patrones.run(600)


def setup(bot):
    bot.add_cog(Nintendo(bot))
