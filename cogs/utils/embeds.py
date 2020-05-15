import random
from datetime import datetime

from discord import Colour, Embed, Member, PartialEmoji

from cogs.utils.acnh import horoscope_urls, personality_es, species_es

bot_colour = 0x89D9BA


def random_colour() -> Colour:
    """ Returna un Colour aleatoreo """
    return Colour.from_hsv(random.random(), 1, 1)


def jumbo_embed(emoji: PartialEmoji) -> Embed:
    """ Returns an embed with an emoji on it's original size """
    embed = Embed(title=str(emoji.name), url=str(emoji.url), colour=random_colour())
    embed.set_image(url=emoji.url)
    return embed


def simple_embed(description: str) -> Embed:
    """ Returns a text only Embed  """
    return Embed(description=description, colour=bot_colour)


def horoscope_embed(data: dict) -> Embed:
    """ Returns a horoscope Embed  """
    embed = Embed(
        title=data["nombre"], description=f"_{data['fechaSigno']}_", colour=0xC18DD6
    )
    embed.add_field(name="Amor", value=data["amor"])
    embed.add_field(name="Salud", value=data["salud"])
    embed.add_field(name="Dinero", value=data["dinero"])
    embed.add_field(name="Color", value=data["color"])
    embed.add_field(name="Número", value=data["numero"])
    embed.set_author(name="Celeste Sultana", icon_url="https://i.imgur.com/pdXckc0.png")
    today = datetime.today().strftime("%#d de %B")
    embed.set_footer(text=f"Horóscopo para el {today}.")
    embed.set_thumbnail(url=horoscope_urls[data["nombre"]])
    return embed


def villager_embed(data: dict) -> Embed:
    """ Retorns an Embed for a ACNH Villager """
    # Color embed
    if data["personality"] == "Cranky":
        colour = 0xFF9292
    elif data["personality"] == "Jock":
        colour = 0x6EB5FF
    elif data["personality"] == "Lazy":
        colour = 0xF8E081
    elif data["personality"] == "Normal":
        colour = 0xBDECB6
    elif data["personality"] == "Peppy":
        colour = 0xFFCCF9
    elif data["personality"] == "Smug":
        colour = 0x97A2FF
    elif data["personality"] == "Snooty":
        colour = 0xD5AAFF
    elif data["personality"] == "Sisterly":
        colour = 0xFFBD61
    else:
        colour = 0x000000

    # Translations
    species = data["species"] + f" ({species_es[data['species']]})"
    personality = data["personality"] + f" ({personality_es[data['personality']]})"
    birthday = datetime.strptime(data["birthday"], "%Y-%m-%d %H:%M:%S")
    birthday = birthday.strftime("%#d de %B").title().replace("De", "de")

    # Embed
    title = f"{data['name']} ({data['spanish']})"
    title += " ♀️" if data["gender"] == "Female" else " ♂️"
    embed = Embed(title=title, colour=colour, timestamp=datetime.utcnow())
    embed.set_thumbnail(url=data["image_url"])
    embed.add_field(name="Especie", value=species)
    embed.add_field(name="Personalidad", value=personality)
    embed.add_field(name="Cumpleaños", value=birthday)
    embed.set_author(
        name="Ver en Nookipedia",
        icon_url="https://i.imgur.com/UKmjvyA.png",
        url=data["url"],
    )
    return embed
