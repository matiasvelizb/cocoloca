import json
from datetime import datetime

import discord
from bs4 import BeautifulSoup
from discord.ext import commands

from cogs.utils.embeds import villager_embed
from cogs.utils.paginator import Paginator
from cogs.utils.queries import get_soup
from cogs.utils.translations import personality_es, species_es

urls = [
    "https://nookipedia.com/wiki/Admiral",
    "https://nookipedia.com/wiki/Agent%20S",
    "https://nookipedia.com/wiki/Agnes",
    "https://nookipedia.com/wiki/Al",
    "https://nookipedia.com/wiki/Alfonso",
    "https://nookipedia.com/wiki/Alice",
    "https://nookipedia.com/wiki/Alli",
    "https://nookipedia.com/wiki/Amelia",
    "https://nookipedia.com/wiki/Anabelle",
    "https://nookipedia.com/wiki/Anchovy",
    "https://nookipedia.com/wiki/Ankha",
    "https://nookipedia.com/wiki/Angus",
    "https://nookipedia.com/wiki/Anicotti",
    "https://nookipedia.com/wiki/Annalisa",
    "https://nookipedia.com/wiki/Annalise",
    "https://nookipedia.com/wiki/Antonio",
    "https://nookipedia.com/wiki/Apollo",
    "https://nookipedia.com/wiki/Apple",
    "https://nookipedia.com/wiki/Astrid",
    "https://nookipedia.com/wiki/Audie",
    "https://nookipedia.com/wiki/Aurora",
    "https://nookipedia.com/wiki/Ava",
    "https://nookipedia.com/wiki/Avery",
    "https://nookipedia.com/wiki/Axel",
    "https://nookipedia.com/wiki/Baabara",
    "https://nookipedia.com/wiki/Bam",
    "https://nookipedia.com/wiki/Bangle",
    "https://nookipedia.com/wiki/Barold",
    "https://nookipedia.com/wiki/Beau",
    "https://nookipedia.com/wiki/Bea",
    "https://nookipedia.com/wiki/Beardo",
    "https://nookipedia.com/wiki/Becky",
    "https://nookipedia.com/wiki/Bella",
    "https://nookipedia.com/wiki/Benedict",
    "https://nookipedia.com/wiki/Benjamin",
    "https://nookipedia.com/wiki/Bertha",
    "https://nookipedia.com/wiki/Bettina",
    "https://nookipedia.com/wiki/Bianca",
    "https://nookipedia.com/wiki/Biff",
    "https://nookipedia.com/wiki/Big%20Top",
    "https://nookipedia.com/wiki/Bill",
    "https://nookipedia.com/wiki/Billy",
    "https://nookipedia.com/wiki/Biskit",
    "https://nookipedia.com/wiki/Bitty",
    "https://nookipedia.com/wiki/Blaire",
    "https://nookipedia.com/wiki/Blanche",
    "https://nookipedia.com/wiki/Bluebear",
    "https://nookipedia.com/wiki/Bob",
    "https://nookipedia.com/wiki/Bonbon",
    "https://nookipedia.com/wiki/Bones",
    "https://nookipedia.com/wiki/Boomer",
    "https://nookipedia.com/wiki/Boone",
    "https://nookipedia.com/wiki/Boots",
    "https://nookipedia.com/wiki/Boris",
    "https://nookipedia.com/wiki/Boyd",
    "https://nookipedia.com/wiki/Bree",
    "https://nookipedia.com/wiki/Broccolo",
    "https://nookipedia.com/wiki/Bruce",
    "https://nookipedia.com/wiki/Broffina",
    "https://nookipedia.com/wiki/Bubbles",
    "https://nookipedia.com/wiki/Buck",
    "https://nookipedia.com/wiki/Bud",
    "https://nookipedia.com/wiki/Bunnie",
    "https://nookipedia.com/wiki/Butch",
    "https://nookipedia.com/wiki/Buzz",
    "https://nookipedia.com/wiki/Cally",
    "https://nookipedia.com/wiki/Camofrog",
    "https://nookipedia.com/wiki/Canberra",
    "https://nookipedia.com/wiki/Candi",
    "https://nookipedia.com/wiki/Carmen%20(rabbit)",
    "https://nookipedia.com/wiki/Caroline",
    "https://nookipedia.com/wiki/Carrie",
    "https://nookipedia.com/wiki/Cashmere",
    "https://nookipedia.com/wiki/Celia",
    "https://nookipedia.com/wiki/Cesar",
    "https://nookipedia.com/wiki/Chadder",
    "https://nookipedia.com/wiki/Charlise",
    "https://nookipedia.com/wiki/Cheri",
    "https://nookipedia.com/wiki/Cherry",
    "https://nookipedia.com/wiki/Chester",
    "https://nookipedia.com/wiki/Chevre",
    "https://nookipedia.com/wiki/Chief",
    "https://nookipedia.com/wiki/Chops",
    "https://nookipedia.com/wiki/Chow",
    "https://nookipedia.com/wiki/Chrissy",
    "https://nookipedia.com/wiki/Claude",
    "https://nookipedia.com/wiki/Claudia",
    "https://nookipedia.com/wiki/Clay",
    "https://nookipedia.com/wiki/Cleo",
    "https://nookipedia.com/wiki/Clyde",
    "https://nookipedia.com/wiki/Coach",
    "https://nookipedia.com/wiki/Cobb",
    "https://nookipedia.com/wiki/Coco",
    "https://nookipedia.com/wiki/Cole",
    "https://nookipedia.com/wiki/Colton",
    "https://nookipedia.com/wiki/Cookie",
    "https://nookipedia.com/wiki/Cousteau",
    "https://nookipedia.com/wiki/Cranston",
    "https://nookipedia.com/wiki/Croque",
    "https://nookipedia.com/wiki/Cube",
    "https://nookipedia.com/wiki/Curlos",
    "https://nookipedia.com/wiki/Curly",
    "https://nookipedia.com/wiki/Curt",
    "https://nookipedia.com/wiki/Cyd",
    "https://nookipedia.com/wiki/Cyrano",
    "https://nookipedia.com/wiki/Daisy",
    "https://nookipedia.com/wiki/Deena",
    "https://nookipedia.com/wiki/Deirdre",
    "https://nookipedia.com/wiki/Del",
    "https://nookipedia.com/wiki/Deli",
    "https://nookipedia.com/wiki/Derwin",
    "https://nookipedia.com/wiki/Diana",
    "https://nookipedia.com/wiki/Diva",
    "https://nookipedia.com/wiki/Dizzy",
    "https://nookipedia.com/wiki/Dobie",
    "https://nookipedia.com/wiki/Doc",
    "https://nookipedia.com/wiki/Dom",
    "https://nookipedia.com/wiki/Dora",
    "https://nookipedia.com/wiki/Dotty",
    "https://nookipedia.com/wiki/Drago",
    "https://nookipedia.com/wiki/Drake",
    "https://nookipedia.com/wiki/Drift",
    "https://nookipedia.com/wiki/Ed",
    "https://nookipedia.com/wiki/Egbert",
    "https://nookipedia.com/wiki/Elise",
    "https://nookipedia.com/wiki/Ellie",
    "https://nookipedia.com/wiki/Elmer",
    "https://nookipedia.com/wiki/Eloise",
    "https://nookipedia.com/wiki/Elvis",
    "https://nookipedia.com/wiki/Erik",
    "https://nookipedia.com/wiki/Eunice",
    "https://nookipedia.com/wiki/Eugene",
    "https://nookipedia.com/wiki/Fang",
    "https://nookipedia.com/wiki/Fauna",
    "https://nookipedia.com/wiki/Felicity",
    "https://nookipedia.com/wiki/Filbert",
    "https://nookipedia.com/wiki/Flip",
    "https://nookipedia.com/wiki/Flo",
    "https://nookipedia.com/wiki/Flora%20(villager)",
    "https://nookipedia.com/wiki/Flurry",
    "https://nookipedia.com/wiki/Francine",
    "https://nookipedia.com/wiki/Frank",
    "https://nookipedia.com/wiki/Freckles",
    "https://nookipedia.com/wiki/Freya",
    "https://nookipedia.com/wiki/Friga",
    "https://nookipedia.com/wiki/Frita",
    "https://nookipedia.com/wiki/Frobert",
    "https://nookipedia.com/wiki/Fuchsia",
    "https://nookipedia.com/wiki/Gabi",
    "https://nookipedia.com/wiki/Gala",
    "https://nookipedia.com/wiki/Gaston",
    "https://nookipedia.com/wiki/Gayle",
    "https://nookipedia.com/wiki/Genji",
    "https://nookipedia.com/wiki/Gigi",
    "https://nookipedia.com/wiki/Gladys",
    "https://nookipedia.com/wiki/Gloria",
    "https://nookipedia.com/wiki/Goldie",
    "https://nookipedia.com/wiki/Gonzo",
    "https://nookipedia.com/wiki/Goose",
    "https://nookipedia.com/wiki/Graham",
    "https://nookipedia.com/wiki/Greta",
    "https://nookipedia.com/wiki/Grizzly",
    "https://nookipedia.com/wiki/Groucho",
    "https://nookipedia.com/wiki/Gruff",
    "https://nookipedia.com/wiki/Gwen",
    "https://nookipedia.com/wiki/Hamlet",
    "https://nookipedia.com/wiki/Hamphrey",
    "https://nookipedia.com/wiki/Hans",
    "https://nookipedia.com/wiki/Harry",
    "https://nookipedia.com/wiki/Hazel",
    "https://nookipedia.com/wiki/Henry",
    "https://nookipedia.com/wiki/Hippeux",
    "https://nookipedia.com/wiki/Hopkins",
    "https://nookipedia.com/wiki/Hopper",
    "https://nookipedia.com/wiki/Hornsby",
    "https://nookipedia.com/wiki/Huck",
    "https://nookipedia.com/wiki/Hugh",
    "https://nookipedia.com/wiki/Iggly",
    "https://nookipedia.com/wiki/Ike",
    "https://nookipedia.com/wiki/Jacob",
    "https://nookipedia.com/wiki/Jacques",
    "https://nookipedia.com/wiki/Jambette",
    "https://nookipedia.com/wiki/Jay",
    "https://nookipedia.com/wiki/Jeremiah",
    "https://nookipedia.com/wiki/Jitters",
    "https://nookipedia.com/wiki/Joey",
    "https://nookipedia.com/wiki/Judy",
    "https://nookipedia.com/wiki/Julia",
    "https://nookipedia.com/wiki/Julian",
    "https://nookipedia.com/wiki/June%20(villager)",
    "https://nookipedia.com/wiki/Kabuki",
    "https://nookipedia.com/wiki/Katt",
    "https://nookipedia.com/wiki/Keaton",
    "https://nookipedia.com/wiki/Ken",
    "https://nookipedia.com/wiki/Ketchup",
    "https://nookipedia.com/wiki/Kevin",
    "https://nookipedia.com/wiki/Kid%20Cat",
    "https://nookipedia.com/wiki/Kidd",
    "https://nookipedia.com/wiki/Kiki",
    "https://nookipedia.com/wiki/Kitt",
    "https://nookipedia.com/wiki/Kitty",
    "https://nookipedia.com/wiki/Klaus",
    "https://nookipedia.com/wiki/Knox",
    "https://nookipedia.com/wiki/Kody",
    "https://nookipedia.com/wiki/Kyle",
    "https://nookipedia.com/wiki/Leonardo",
    "https://nookipedia.com/wiki/Leopold",
    "https://nookipedia.com/wiki/Lily",
    "https://nookipedia.com/wiki/Limberg",
    "https://nookipedia.com/wiki/Lionel",
    "https://nookipedia.com/wiki/Lobo",
    "https://nookipedia.com/wiki/Lolly",
    "https://nookipedia.com/wiki/Lopez",
    "https://nookipedia.com/wiki/Louie",
    "https://nookipedia.com/wiki/Lucha",
    "https://nookipedia.com/wiki/Lucky",
    "https://nookipedia.com/wiki/Lucy",
    "https://nookipedia.com/wiki/Lyman",
    "https://nookipedia.com/wiki/Mac",
    "https://nookipedia.com/wiki/Maddie",
    "https://nookipedia.com/wiki/Maelle",
    "https://nookipedia.com/wiki/Maggie",
    "https://nookipedia.com/wiki/Mallary",
    "https://nookipedia.com/wiki/Maple",
    "https://nookipedia.com/wiki/Margie",
    "https://nookipedia.com/wiki/Marcel",
    "https://nookipedia.com/wiki/Marcie",
    "https://nookipedia.com/wiki/Marina",
    "https://nookipedia.com/wiki/Marshal",
    "https://nookipedia.com/wiki/Mathilda",
    "https://nookipedia.com/wiki/Megan",
    "https://nookipedia.com/wiki/Melba",
    "https://nookipedia.com/wiki/Merengue",
    "https://nookipedia.com/wiki/Merry",
    "https://nookipedia.com/wiki/Midge",
    "https://nookipedia.com/wiki/Mint",
    "https://nookipedia.com/wiki/Mira",
    "https://nookipedia.com/wiki/Miranda",
    "https://nookipedia.com/wiki/Mitzi",
    "https://nookipedia.com/wiki/Moe",
    "https://nookipedia.com/wiki/Molly",
    "https://nookipedia.com/wiki/Monique",
    "https://nookipedia.com/wiki/Monty",
    "https://nookipedia.com/wiki/Moose",
    "https://nookipedia.com/wiki/Mott",
    "https://nookipedia.com/wiki/Muffy",
    "https://nookipedia.com/wiki/Murphy",
    "https://nookipedia.com/wiki/Nan",
    "https://nookipedia.com/wiki/Nana",
    "https://nookipedia.com/wiki/Naomi",
    "https://nookipedia.com/wiki/Nate",
    "https://nookipedia.com/wiki/Nibbles",
    "https://nookipedia.com/wiki/Norma",
    "https://nookipedia.com/wiki/Octavian",
    "https://nookipedia.com/wiki/O'Hare",
    "https://nookipedia.com/wiki/Olaf",
    "https://nookipedia.com/wiki/Olive",
    "https://nookipedia.com/wiki/Olivia",
    "https://nookipedia.com/wiki/Opal",
    "https://nookipedia.com/wiki/Ozzie",
    "https://nookipedia.com/wiki/Pancetti",
    "https://nookipedia.com/wiki/Pango",
    "https://nookipedia.com/wiki/Papi",
    "https://nookipedia.com/wiki/Paolo",
    "https://nookipedia.com/wiki/Pashmina",
    "https://nookipedia.com/wiki/Pate",
    "https://nookipedia.com/wiki/Patty",
    "https://nookipedia.com/wiki/Paula",
    "https://nookipedia.com/wiki/Peaches",
    "https://nookipedia.com/wiki/Peanut",
    "https://nookipedia.com/wiki/Pecan",
    "https://nookipedia.com/wiki/Peck",
    "https://nookipedia.com/wiki/Peewee",
    "https://nookipedia.com/wiki/Peggy",
    "https://nookipedia.com/wiki/Pekoe",
    "https://nookipedia.com/wiki/Penelope",
    "https://nookipedia.com/wiki/Phil",
    "https://nookipedia.com/wiki/Phoebe",
    "https://nookipedia.com/wiki/Pierce",
    "https://nookipedia.com/wiki/Pietro",
    "https://nookipedia.com/wiki/Pinky",
    "https://nookipedia.com/wiki/Piper",
    "https://nookipedia.com/wiki/Pippy",
    "https://nookipedia.com/wiki/Plucky",
    "https://nookipedia.com/wiki/Pompom",
    "https://nookipedia.com/wiki/Poncho",
    "https://nookipedia.com/wiki/Poppy",
    "https://nookipedia.com/wiki/Portia",
    "https://nookipedia.com/wiki/Prince",
    "https://nookipedia.com/wiki/Puck",
    "https://nookipedia.com/wiki/Puddles",
    "https://nookipedia.com/wiki/Pudge",
    "https://nookipedia.com/wiki/Punchy",
    "https://nookipedia.com/wiki/Purrl",
    "https://nookipedia.com/wiki/Queenie",
    "https://nookipedia.com/wiki/Quillson",
    "https://nookipedia.com/wiki/Raddle",
    "https://nookipedia.com/wiki/Rasher",
    "https://nookipedia.com/wiki/Raymond",
    "https://nookipedia.com/wiki/Renée",
    "https://nookipedia.com/wiki/Reneigh",
    "https://nookipedia.com/wiki/Rex",
    "https://nookipedia.com/wiki/Rhonda",
    "https://nookipedia.com/wiki/Ribbot",
    "https://nookipedia.com/wiki/Ricky",
    "https://nookipedia.com/wiki/Rizzo",
    "https://nookipedia.com/wiki/Roald",
    "https://nookipedia.com/wiki/Robin",
    "https://nookipedia.com/wiki/Rocco",
    "https://nookipedia.com/wiki/Rocket",
    "https://nookipedia.com/wiki/Rod",
    "https://nookipedia.com/wiki/Rodeo",
    "https://nookipedia.com/wiki/Rodney",
    "https://nookipedia.com/wiki/Rolf",
    "https://nookipedia.com/wiki/Rooney",
    "https://nookipedia.com/wiki/Rory",
    "https://nookipedia.com/wiki/Roscoe",
    "https://nookipedia.com/wiki/Rosie",
    "https://nookipedia.com/wiki/Rowan",
    "https://nookipedia.com/wiki/Ruby",
    "https://nookipedia.com/wiki/Rudy",
    "https://nookipedia.com/wiki/Sally",
    "https://nookipedia.com/wiki/Samson",
    "https://nookipedia.com/wiki/Sandy",
    "https://nookipedia.com/wiki/Savannah",
    "https://nookipedia.com/wiki/Scoot",
    "https://nookipedia.com/wiki/Shari",
    "https://nookipedia.com/wiki/Sheldon",
    "https://nookipedia.com/wiki/Shep",
    "https://nookipedia.com/wiki/Sherb",
    "https://nookipedia.com/wiki/Simon",
    "https://nookipedia.com/wiki/Skye",
    "https://nookipedia.com/wiki/Sly",
    "https://nookipedia.com/wiki/Snake",
    "https://nookipedia.com/wiki/Snooty%20(villager)",
    "https://nookipedia.com/wiki/Soleil",
    "https://nookipedia.com/wiki/Sparro",
    "https://nookipedia.com/wiki/Spike",
    "https://nookipedia.com/wiki/Spork",
    "https://nookipedia.com/wiki/Sprinkle",
    "https://nookipedia.com/wiki/Sprocket",
    "https://nookipedia.com/wiki/Static",
    "https://nookipedia.com/wiki/Stella",
    "https://nookipedia.com/wiki/Sterling",
    "https://nookipedia.com/wiki/Stinky",
    "https://nookipedia.com/wiki/Stitches",
    "https://nookipedia.com/wiki/Stu",
    "https://nookipedia.com/wiki/Sydney",
    "https://nookipedia.com/wiki/Sylvana",
    "https://nookipedia.com/wiki/Sylvia",
    "https://nookipedia.com/wiki/Tabby",
    "https://nookipedia.com/wiki/Tad",
    "https://nookipedia.com/wiki/Tammi",
    "https://nookipedia.com/wiki/Tammy",
    "https://nookipedia.com/wiki/Tangy",
    "https://nookipedia.com/wiki/Tank",
    "https://nookipedia.com/wiki/T-Bone",
    "https://nookipedia.com/wiki/Tasha",
    "https://nookipedia.com/wiki/Teddy",
    "https://nookipedia.com/wiki/Tex",
    "https://nookipedia.com/wiki/Tia",
    "https://nookipedia.com/wiki/Tiffany",
    "https://nookipedia.com/wiki/Timbra",
    "https://nookipedia.com/wiki/Tipper",
    "https://nookipedia.com/wiki/Tom",
    "https://nookipedia.com/wiki/Truffles",
    "https://nookipedia.com/wiki/Tucker",
    "https://nookipedia.com/wiki/Tutu",
    "https://nookipedia.com/wiki/Twiggy",
    "https://nookipedia.com/wiki/Tybalt",
    "https://nookipedia.com/wiki/Ursala",
    "https://nookipedia.com/wiki/Velma",
    "https://nookipedia.com/wiki/Vesta",
    "https://nookipedia.com/wiki/Vic",
    "https://nookipedia.com/wiki/Victoria",
    "https://nookipedia.com/wiki/Violet",
    "https://nookipedia.com/wiki/Vivian",
    "https://nookipedia.com/wiki/Vladimir",
    "https://nookipedia.com/wiki/Wade",
    "https://nookipedia.com/wiki/Walker",
    "https://nookipedia.com/wiki/Walt",
    "https://nookipedia.com/wiki/Wart%20Jr.",
    "https://nookipedia.com/wiki/Weber",
    "https://nookipedia.com/wiki/Wendy",
    "https://nookipedia.com/wiki/Winnie",
    "https://nookipedia.com/wiki/Whitney",
    "https://nookipedia.com/wiki/Willow",
    "https://nookipedia.com/wiki/Wolfgang",
    "https://nookipedia.com/wiki/Yuka",
    "https://nookipedia.com/wiki/Zell",
    "https://nookipedia.com/wiki/Zucker",
]


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

    @commands.cooldown(rate=1, per=240, type=commands.BucketType.user)
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

    @commands.cooldown(rate=1, per=240, type=commands.BucketType.user)
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
        for idx, url in enumerate(urls, start=1):
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
                update = f"{self.bot.think} ┆ Descargando aldeanos ({idx}/{len(urls)})"
                await msg.edit(content=update)
        # Escribir JSON
        await msg.edit(content="Guardando información...")
        with open("villagers.json", "w", encoding="utf-8") as fp:
            json.dump(villagers, fp, ensure_ascii=False, default=str)
        await msg.edit(content="Terminado.")


def setup(bot):
    bot.add_cog(Nintendo(bot))
