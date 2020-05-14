import asyncio

import discord


class Paginator:
    """
    Implements a paginator with a list of embeds.
    
    Parameters
    ------------
    ctx: Context
        The context where the command was invoked.
    content: str
        An opening note to the paginator.
    pages: list
        List of discord.Embed with the content to show.
    """

    def __init__(self, ctx, content, pages):
        self.ctx = ctx
        self.content = content
        self.pages = pages
        self.message = None
        self.curr = 0

    async def run(self, time: int):
        self.message = await self.ctx.send(content=self.content, embed=self.pages[self.curr])
        self.ctx.bot.add_listener(self.on_reaction_add)
        for reaction in self.handlers:
            await self.message.add_reaction(reaction)
        await self.timer(time)

    async def timer(self, time: int):
        def check(reaction, user):
            return user == self.ctx.author and str(reaction.emoji) == "⏹"

        await self.ctx.bot.wait_for("reaction_add", check=check, timeout=time)

    async def on_reaction_add(self, reaction, user):
        if reaction.message.id != self.message.id:
            return

        if user.id != self.ctx.bot.user.id:
            try:
                await self.message.remove_reaction(reaction, user)
            except discord.Forbidden:
                pass

        if user.id != self.ctx.author.id:
            return

        handler = self.handlers.get(str(reaction.emoji))
        if handler is not None:
            await handler(self)

    async def update(self):
        await self.message.edit(embed=self.pages[self.curr])

    async def first(self):
        self.curr = 0
        await self.update()

    async def next(self):
        if self.curr == len(self.pages) - 1:
            return
        self.curr += 1
        await self.update()

    async def back(self):
        if self.curr == 0:
            return
        self.curr -= 1
        await self.update()

    async def last(self):
        self.curr = len(self.pages) - 1
        await self.update()

    async def stop(self):
        if self.ctx.command.is_on_cooldown(self.ctx):
            self.ctx.command.reset_cooldown(self.ctx)
        self.ctx.bot.remove_listener(self.on_reaction_add)
        try:
            await self.message.clear_reactions()
        except discord.Forbidden:
            for emoji in self.handlers:
                await self.message.remove_reaction(emoji, self.ctx.me)

    handlers = {"⏮": first, "◀": back, "⏹": stop, "▶": next, "⏭": last}


class TextPaginator(Paginator):
    """
    Implements a paginator with a list of strings instead.
    
    Parameters
    ------------
    ctx: Context
        The context where the command was invoked.
    pages: list
        List of strings with the content to show.
    """

    def __init__(self, ctx, pages):
        super().__init__(ctx, None, pages)

    async def run(self, time: int):
        self.message = await self.ctx.send(content=self.pages[self.curr])
        self.ctx.bot.add_listener(self.on_reaction_add)
        for reaction in self.handlers:
            await self.message.add_reaction(reaction)
        await super().timer(time)

    async def update(self):
        await self.message.edit(content=self.pages[self.curr])
