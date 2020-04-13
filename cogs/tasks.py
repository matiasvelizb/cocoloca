import discord
from discord.ext import commands, tasks

delay = 600  # 10 minutos


class Tasks(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.status.start()

    def cog_unload(self):
        self.status.cancel()

    @tasks.loop(seconds=delay)
    async def status(self):
        guild = self.bot.get_guild(699100559726215208)
        members = [member for member in guild.members if not member.bot]
        game = f"Animal Crossing con {len(members)} amigos."
        activity = discord.Activity(type=discord.ActivityType.playing, name=game)
        await self.bot.change_presence(activity=activity)

    @status.before_loop
    async def before_status(self):
        await self.bot.wait_until_ready()


def setup(bot):
    bot.add_cog(Tasks(bot))
