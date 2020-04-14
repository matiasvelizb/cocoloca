import io

import aiohttp
from bs4 import BeautifulSoup


async def get_soup(url: str) -> BeautifulSoup:
    """ Retorna una pagina web con BeautifulSoup """
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as r:
            data = await r.text()
            return BeautifulSoup(data, "lxml") if r.status == 200 else None


async def get_bytes(url: str) -> io.BytesIO:
    """ Retorna la descarga en bytes de una url """
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as r:
            if r.status != 200:
                return None
            return io.BytesIO(await r.read())
