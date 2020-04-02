import discord
from discord.ext import commands


class Moderation(commands.Cog):
    """Commands for server moderation"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="kick")
    @commands.guild_only()
    @commands.has_permissions(kick_members=True)
    @commands.bot_has_permissions(kick_members=True)
    async def _kick(self, ctx, member: discord.Member, *, reason: str = None):
        """Kicks the given member.
        If the member has spaces in their name, the name must be put in quotes. You can also mention the member.
        Reason is optional."""

        # Add a default reason if none is given.
        if reason:
            reason = f"Kicked by {ctx.author} [ID: {ctx.author.id}] - {reason}"
        else:
            reason = f"Kicked by {ctx.author} [ID: {ctx.author.id}]"

        # Reason must be 512 characters or less.
        if len(reason) > 512:
            await ctx.send(
                f":no_entry_sign: Reason must be 512 (currently: {len(reason)}) or fewer characters in length."
            )
        else:

            try:
                await member.kick(reason=reason)
            except discord.HTTPException:
                await ctx.send(f":no_entry_sign: Kicking failed.")
            else:
                await ctx.message.add_reaction("\u2705")

    @commands.command(name="ban")
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def _ban(self, ctx, member: discord.Member, *, reason: str = None):
        """Bans the given member.
        If the member has spaces in their name, the name must be put in quotes.
        You can also mention the member.
        Reason is optional."""

        if reason:
            reason = f"Invoked by {ctx.author} [ID: {ctx.author.id}] - {reason}"
        else:
            reason = f"Invoked by {ctx.author} [ID: {ctx.author.id}]"

        # Reason must be 512 characters or fewer.
        if len(reason) > 512:
            await ctx.send(
                f":no_entry_sign: Reason must be 512 (currently: {len(reason)}) or fewer characters in length."
            )
        else:

            try:
                await member.ban(delete_message_days=0, reason=reason)
            except discord.HTTPException:
                await ctx.send(f":no_entry_sign: Banning failed.")
            else:
                await ctx.message.add_reaction("\u2705")


def setup(bot):
    bot.add_cog(Moderation(bot))
