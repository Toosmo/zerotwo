import random
from typing import Union

import discord
from discord.ext import commands


class Generic(commands.Cog):
    """Generic commands."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        """Pong."""

        resp = await ctx.send("Pong! Loading...")
        diff = resp.created_at - ctx.message.created_at
        await resp.edit(content=f"Pong! That took {1000*diff.total_seconds():.1f}ms.")

    @commands.command()
    async def echo(self, ctx, *, message: str):
        """Echoes the given input."""

        await ctx.send(message)

    @commands.command()
    async def slap(self, ctx, *, member: Union[discord.Member, discord.User] = None):
        """Slap another user."""

        weapons = ["a large trout", "a dried baguette"]

        if not member:
            member = ctx.author
            await ctx.send(
                f"*slaps {member.mention} around a bit with {random.choice(weapons)}.*"  # nosec
            )

        elif member == self.bot.user:
            await ctx.send(
                f"*slaps {ctx.author.mention} around a bit with {random.choice(weapons)}.*"  # nosec
            )

        else:
            await ctx.send(
                f"_**{ctx.author.display_name}** slaps {member.mention} around a bit with {random.choice(weapons)}._"  # nosec
            )

    @commands.command()
    async def ding(self, ctx):
        await ctx.send(
            f"{'🌸 ✌ <a:Dingdingdingding:742622269985128471> DING DING ' * 7 }"
        )


def setup(bot):
    bot.add_cog(Generic(bot))
