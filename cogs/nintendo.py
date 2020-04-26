import json
from datetime import datetime

import discord
from bs4 import BeautifulSoup
from discord.ext import commands

from cogs.utils.embeds import villager_embed
from cogs.utils.paginator import Paginator
from cogs.utils.queries import get_soup
from cogs.utils.acnh import personality_es, species_es, villager_urls


def to_title(argument):
    return argument.title()


def normalize(argument):
    replacements = (
        ("á", "a"),
        ("é", "e"),
        ("í", "i"),
        ("ó", "o"),
        ("ú", "u"),
    )
    for a, b in replacements:
        argument = argument.replace(a, b).replace(a.upper(), b.upper())
    return argument.title()


def get_keys(argument):
    strings = [f"`{k}`" for k, v in argument.items()]
    return ", ".join(strings)


def parse_date(argument):
    months = [
        "Jan",
        "Feb",
        "Mar",
        "Apr",
        "May",
        "Jun",
        "Jul",
        "Aug",
        "Sep",
        "Oct",
        "Nov",
        "Dec",
    ]
    days = reversed(range(1, 32))
    year = datetime.today().year
    month = months.index(next(m for m in months if m in argument)) + 1
    day = next(d for d in days if str(d) in argument)
    return datetime(year, month, day)


class Nintendo(commands.Cog, name="Animal Crossing"):
    def __init__(self, bot):
        self.bot = bot

    @commands.cooldown(rate=1, per=3, type=commands.BucketType.user)
    @commands.command(aliases=["a", "ald"])
    async def aldeano(self, ctx, *, aldeano: normalize):
        """
        **Obtén información de algún aldeano de ACNH**
        <busqueda>: El nombre en **español** del aldeano a buscar.
        """
        async with ctx.typing():
            msg = await ctx.send(f"{self.bot.think} | Se esta buscando a tu aldeano.")
            data = next(
                (x for x in self.bot.villagers if normalize(x["spanish"]) == aldeano),
                None,
            )
            if data:
                embed = villager_embed(data)
                await msg.delete()
                await ctx.send(embed=embed)
            else:
                err = f"{self.bot.omg} | {aldeano.title()} no es un aldeano en ACNH."
                await msg.edit(content=err, delete_after=7)

    @commands.cooldown(rate=1, per=3, type=commands.BucketType.user)
    @commands.command(aliases=["v", "vil"])
    async def villager(self, ctx, *, villager: str):
        """
        **Obtén información de algún aldeano de ACNH**
        <busqueda>: El nombre en **ingles** del aldeano a buscar.
        """
        async with ctx.typing():
            msg = await ctx.send(f"{self.bot.think} | Se esta buscando a tu aldeano.")
            data = next(
                (vil for vil in self.bot.villagers if vil["name"] == villager.title()),
                None,
            )
            if data:
                embed = villager_embed(data)
                await msg.delete()
                await ctx.send(embed=embed)
            else:
                err = f"{self.bot.omg} | {villager.title()} no es un aldeano en ACNH."
                await msg.edit(content=err, delete_after=7)

    @commands.max_concurrency(number=1, per=commands.BucketType.member)
    @commands.command(aliases=["p", "per", "personality"])
    async def personalidad(self, ctx, *, personalidad: to_title):
        """
        **Obtén un listado con todos los aldeanos de una personalidad**
        <personalidad>: La personalidad en **ingles** a buscar.
        """
        # Verificar personalidad
        if personalidad not in personality_es:
            ctx.command.reset_cooldown(ctx)
            content = (
                f"{personalidad} no es una personalidad valida en inglés.\n"
                "Por favor, elija una de las siguientes personalidades: "
                f"{get_keys(personality_es)}"
            )
            await ctx.send(content, delete_after=30)
            return
        # Generar paginas
        pages = []
        filtered = [x for x in self.bot.villagers if x["personality"] == personalidad]
        for idx, villager in enumerate(filtered, start=1):
            embed = villager_embed(villager)
            embed.set_footer(
                text=f"Información obtenida de Nookipedia ({idx}/{len(filtered)})",
                icon_url="https://i.imgur.com/UKmjvyA.png",
            )
            pages.append(embed)
        # Crear paginador por 10 minutos
        msg = f"Aldeanos de personalidad **{personalidad}** ({personality_es[personalidad]})"
        paginator = Paginator(ctx, msg, pages)
        await paginator.run(600)

    @commands.max_concurrency(number=1, per=commands.BucketType.member)
    @commands.command(aliases=["e", "esp", "species"])
    async def especie(self, ctx, *, especie: to_title):
        """
        **Obtén un listado con todos los aldeanos de una especie**
        <especie>: La especie en **ingles** a buscar.
        """
        # Verificar especie
        if especie not in species_es:
            ctx.command.reset_cooldown(ctx)
            content = (
                f"{especie} no es una especie valida en inglés.\n"
                "Por favor, elija una de las siguientes especies: "
                f"{get_keys(species_es)}"
            )
            await ctx.send(content, delete_after=30)
            return
        # Generar paginas
        pages = []
        filtered = [x for x in self.bot.villagers if x["species"] == especie]
        for idx, villager in enumerate(filtered, start=1):
            embed = villager_embed(villager)
            embed.set_footer(
                text=f"Información obtenida de Nookipedia ({idx}/{len(filtered)})",
                icon_url="https://i.imgur.com/UKmjvyA.png",
            )
            pages.append(embed)
        # Crear paginador por 10 minutos
        msg = f"Aldeanos de especie **{especie}** ({species_es[especie]})"
        paginator = Paginator(ctx, msg, pages)
        await paginator.run(600)

    @commands.is_owner()
    @commands.command()
    async def update(self, ctx):
        """
        **Actualiza la base de datos de aldeanos**
        Recordar verificar consola al terminar y modificar aldeanos con asterisco.
        """
        villagers = []
        msg = await ctx.send(f"{self.bot.think} ┆ Actualizando aldeanos...")
        # Generar listado
        for idx, url in enumerate(villager_urls, start=1):
            soup = await get_soup(url)
            try:
                name = soup.find(id="api-villager_name")
                spanish = soup.find("img", alt="Spanish").find_next_sibling("span")
                gender = soup.find(id="api-villager_gender")
                species = soup.find(id="api-villager_species")
                birthday = soup.find(id="api-villager_birthday")
                personality = soup.find(id="api-villager_personality")
                table = name.find_parent("table")
                image_url = table.a.get("href")
                description = table.find_next_sibling("p")
            except:
                print(f"Error actualizando {idx} : {url}")
            else:
                data = {}
                data["name"] = name.text
                data["spanish"] = spanish.text
                data["gender"] = gender.text
                data["species"] = species.text
                data["birthday"] = parse_date(birthday.text)
                data["personality"] = personality.text
                data["image_url"] = image_url
                data["description"] = description.text
                data["url"] = url
                villagers.append(data)
            finally:
                text = f"{self.bot.think} ┆ Descargando aldeanos ({idx}/{len(villager_urls)})"
                await msg.edit(content=text)
        # Escribir JSON
        await msg.edit(content="Guardando información...")
        with open("villagers.json", "w", encoding="utf-8") as fp:
            json.dump(villagers, fp, ensure_ascii=False, default=str)
        await msg.edit(content="Terminado.")


def setup(bot):
    bot.add_cog(Nintendo(bot))
