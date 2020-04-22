import itertools

import discord
from discord.ext import commands

from cogs.utils.embeds import bot_colour


class HelpCommand(commands.MinimalHelpCommand):
    def __init__(self, **options):
        super().__init__(**options)

    def get_opening_note(self):
        return (
            f"Use `{self.clean_prefix}help [comando]` para mayor información de un comando.\n"
            "_Los argumentos con <> son obligatorios y los con [] son opcionales._"
        )

    def get_command_signature(self, command):
        if command.signature:
            return f"`{self.clean_prefix}{command.qualified_name} {command.signature}`"
        else:
            return f"`{self.clean_prefix}{command.qualified_name}`"

    def add_aliases_formatting(self, aliases):
        if aliases:
            return "`" + "`\u2002`".join(x for x in aliases) + "`"

    def add_bot_commands_formatting(self, commands, heading, embed):
        if commands:
            joined = "`" + "`\u2002`".join(c.name for c in commands) + "`"
            embed.add_field(name=heading, value=joined, inline=False)

    async def send_embed(self, embed):
        destination = self.get_destination()
        await destination.send(embed=embed)

    async def send_bot_help(self, mapping):
        # Embed
        bot = self.context.bot
        title = f"Comandos de {bot.user.name}"
        embed = discord.Embed(description=self.get_opening_note(), colour=bot_colour)
        embed.set_author(name=title, icon_url=bot.user.avatar_url)
        embed.set_thumbnail(url=bot.user.avatar_url_as(format="png"))
        embed.set_footer(text="Desarrollado por Foosen#3357")

        def get_category(command):
            cog = command.cog
            return cog.qualified_name

        # Get command for each category
        filtered = await self.filter_commands(bot.commands, sort=True, key=get_category)
        to_iterate = itertools.groupby(filtered, key=get_category)
        for category, commands in to_iterate:
            commands = (
                sorted(commands, key=lambda c: c.name)
                if self.sort_commands
                else list(commands)
            )
            self.add_bot_commands_formatting(commands, category, embed)

        await self.send_embed(embed)

    async def send_cog_help(self, cog):
        return None

    async def send_command_help(self, command):
        bot = self.context.bot.user
        title = f"Comandos de {bot.name} ({command.name})"
        embed = discord.Embed(description=command.help, color=bot_colour)
        embed.set_author(name=title, icon_url=bot.avatar_url)
        # Signature
        signature = self.get_command_signature(command)
        embed.add_field(name="Formula", value=signature, inline=False)
        # Aliases
        aliases = self.add_aliases_formatting(command.aliases)
        if aliases:
            embed.add_field(name="Aliases", value=aliases, inline=False)
        embed.set_footer(text="<> - Obligatorio, [] - Opcional")
        await self.send_embed(embed)


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        bot.help_command = HelpCommand(command_attrs={"hidden": True})
        self._original_help_command = bot.help_command
        bot.help_command.cog = self

    def cog_unload(self):
        self.bot.help_command = self._original_help_command


def setup(bot):
    bot.add_cog(Help(bot))
