import discord
from discord.ext import commands

from .utils import bot_stats
from .utils import embed_builder as builder


class Info(commands.Cog):
    """Informational commands."""

    def __init__(self, bot):
        self.bot = bot

    @commands.group(case_insensitive=True)
    async def info(self, ctx):
        """Informational commands."""

    @info.command()
    @commands.guild_only()
    async def server(self, ctx):
        """Displays information of the current server."""

        await ctx.send(content=None, embed=await builder.build_server_embed(ctx))

    @info.command()
    @commands.guild_only()
    async def user(self, ctx, *, member: discord.Member = None):
        """Displays information of the given user."""

        # If there's no given user, will display information of the message author.
        if not member:
            member = ctx.author

        await ctx.send(content=None, embed=await builder.build_user_embed(member))

    @user.error
    async def user_error(self, ctx, error):
        error = getattr(error, "original", error)

        if isinstance(error, commands.BadArgument):
            await ctx.send(
                content=None, embed=await builder.build_error_embed("User not found.")
            )

    @commands.command()
    async def about(self, ctx):
        """Displays information of the bot."""

        await ctx.send(content=None, embed=await builder.build_about_embed(self.bot))

    @commands.command()
    async def uptime(self, ctx):
        """Shows the bot uptime."""

        await ctx.send(await bot_stats.uptime())

    @staticmethod
    def permissions():
        """Permissions for the invite link."""

        bot_perms = discord.Permissions.none()
        bot_perms.embed_links = True
        bot_perms.read_message_history = True
        bot_perms.add_reactions = True
        bot_perms.send_messages = True
        bot_perms.ban_members = True
        bot_perms.kick_members = True
        return bot_perms


def setup(bot):
    bot.add_cog(Info(bot))
