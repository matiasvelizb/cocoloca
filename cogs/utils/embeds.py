import random
from datetime import datetime

from bs4 import BeautifulSoup
from discord import Colour, Embed, Member, PartialEmoji

bot_colour = 0x89D9BA


def random_colour() -> Colour:
    """ Returna un Colour aleatoreo """
    return Colour.from_hsv(random.random(), 1, 1)


def soup_markdown(url: str, tag: str) -> str:
    """ Returns a hyperlink markdown for a BeautifulSoup tag """
    return f"[{tag.text}]({url}{tag.a.get('href')})" if tag.a else tag.text


def jumbo_embed(emoji: PartialEmoji) -> Embed:
    """ Returns an embed with an emoji on it's original size """
    embed = Embed(title=str(emoji.name), url=str(emoji.url), colour=random_colour())
    embed.set_image(url=emoji.url)
    return embed


def simple_embed(description: str) -> Embed:
    """ Returns a text only Embed  """
    return Embed(description=description, colour=bot_colour)


def villager_embed(soup: BeautifulSoup) -> Embed:
    """ Retorns an Embed for a ACNH Villager """
    # Data
    nombre = soup.find("img", alt="Spanish").find_next_sibling("span")
    name = soup.find(id="api-villager_name")
    gender = soup.find(id="api-villager_gender").text
    species = soup.find(id="api-villager_species")
    personality = soup.find(id="api-villager_personality")
    birthday = soup.find(id="api-villager_birthday")
    table = name.find_parent("table")
    image_url = table.a.get("href")
    description = table.find_next_sibling("p")

    # Color embed
    if personality.text == "Cranky":
        colour = 0xFF9292
    elif personality.text == "Jock":
        colour = 0x6EB5FF
    elif personality.text == "Lazy":
        colour = 0xF8E081
    elif personality.text == "Normal":
        colour = 0xBDECB6
    elif personality.text == "Peppy":
        colour = 0xFFCCF9
    elif personality.text == "Smug":
        colour = 0x97A2FF
    elif personality.text == "Snooty":
        colour = 0xD5AAFF
    elif personality.text == "Uchi":
        colour = 0xFFBD61
    else:
        colour = bot_colour

    # Embed
    url = "https://nookipedia.com"
    title = (
        f"{name.text} ({nombre.text}) ♀️"
        if gender == "Female"
        else f"{name.text} ({nombre.text}) ♂️"
    )
    embed = Embed(
        title=title,
        description=f"{description.text}[Read More]({url}/wiki/{name.text})",
        colour=Colour(colour),
        timestamp=datetime.utcnow(),
    )
    embed.set_image(url=image_url)
    embed.add_field(name="Especie", value=soup_markdown(url, species))
    embed.add_field(name="Personalidad", value=soup_markdown(url, personality))
    embed.add_field(name="Cumpleaños", value=soup_markdown(url, birthday))
    embed.set_footer(
        text="Información obtenida de Nookipedia.",
        icon_url="https://i.imgur.com/UKmjvyA.png",
    )
    return embed
