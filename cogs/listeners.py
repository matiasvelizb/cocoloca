import re

import asyncpg
import discord
from discord.ext import commands

url_regex = (
    "http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
)


class Listeners(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        query = """
        INSERT INTO guilds (guild_id)
        VALUES ($1) ON CONFLICT (guild_id) DO NOTHING;
        """
        await self.bot.db.execute(query, guild.id)
        print("Joined guild:", guild, guild.id)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.id == 701951947644600410 and not message.author.bot:
            urls = re.findall(url_regex, message.content)
            if len(message.attachments) >= 1 or urls:
                pass
            else:
                await message.delete()
                error = (
                    "**Este canal solo admite mensajes con imagenes o links**. "
                    "Todo lo demás será borrado automaticamente."
                )
                await message.channel.send(error, delete_after=5)


def setup(bot):
    bot.add_cog(Listeners(bot))
