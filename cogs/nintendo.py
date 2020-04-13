import aiohttp
import discord
from bs4 import BeautifulSoup
from discord.ext import commands

from cogs.utils.embeds import villager_embed


class Nintendo(commands.Cog, name="Animal Crossing"):
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    async def get_soup(url: str) -> BeautifulSoup:
        """ Retorna una pagina web con BeautifulSoup """
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as r:
                data = await r.text()
                return BeautifulSoup(data, "lxml") if r.status == 200 else None

    @commands.bot_has_permissions(manage_messages=True)
    @commands.cooldown(rate=1, per=3, type=commands.BucketType.user)
    @commands.command(aliases=["a", "char", "vil", "villager", "wiki"])
    async def aldeano(self, ctx, *, aldeano: str):
        """
        Obtén información de algún aldeano de ACNH
        <aldeano>: Nombre en **inglés** del aldeano a buscar.
        """
        url = "https://nookipedia.com/wiki/" + aldeano.title()
        content = f"{self.bot.question} ┆ Buscando información de {aldeano.title()}."
        info_msg = await ctx.send(content)

        async with ctx.typing():
            soup = await self.get_soup(url)
            if soup:
                embed = villager_embed(soup)
                try:
                    await ctx.send(embed=embed)
                except discord.HTTPException:
                    aux = f"{self.bot.omg} ┆ {aldeano.title()} no es un aldeano valido."
                    await info_msg.edit(content=aux)
                else:
                    await info_msg.delete()
            else:
                aux = f"{self.bot.omg} ┆ Error al obtener los datos desde la Wiki."
                await info_msg.edit(content=aux)

    @commands.command(aliases=["repup", "up", "uprep"])
    async def upvote(self, ctx, member: discord.Member):
        """ Subir la reputación de algún miembro """
        if member.id == ctx.author.id:
            await ctx.send("{self.bot.emoji} | No puedes votar a favor de ti mismo.")
            return
        # Aumentar reputación
        query = """
        INSERT INTO members(member_id) VALUES ($1)
        ON CONFLICT (member_id) DO
        UPDATE SET reputation = members.reputation + 1;
        """
        await self.bot.db.execute(query, member.id)
        await ctx.send(f"Se ha votado a favor de {member.name}.")

    @commands.bot_has_permissions(manage_messages=True)
    @commands.command(aliases=["repdown", "down", "downrep"])
    async def downvote(self, ctx, member: discord.Member):
        """ Bajar la reputación de algún miembro """
        await ctx.message.delete()
        if member.id == ctx.author.id:
            await ctx.send("{self.bot.emoji} | No puedes votar en contra de ti mismo.")
            return
        # Disminuir reputación
        query = """
        INSERT INTO members(member_id) VALUES ($1)
        ON CONFLICT (member_id) DO
        UPDATE SET reputation = members.reputation - 1;
        """
        await self.bot.db.execute(query, member.id)
        await ctx.send(f"Se ha votado en contra de {member.name}.")


def setup(bot):
    bot.add_cog(Nintendo(bot))
