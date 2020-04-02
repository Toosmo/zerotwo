import discord
from discord.ext import commands

from .utils import embed_builder as builder


class NoSpotify(commands.CheckFailure):
    pass


def is_spotify():
    async def predicate(ctx):
        spotify = False

        for activity in ctx.author.activities:
            if isinstance(activity, discord.Spotify):
                spotify = True

        if spotify is not True:
            raise NoSpotify("User is not currently listening to Spotify.")
        return True

    return commands.check(predicate)


class Spotify(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.guild_only()
    @is_spotify()
    async def spotify(self, ctx):
        """Share what you're currently listening to in Spotify."""

        await ctx.send(content=None, embed=await builder.build_spotify_embed(ctx))

    @spotify.error
    async def spotify_error(self, ctx, error):
        error = getattr(error, "original", error)

        if isinstance(error, NoSpotify):
            await ctx.send(
                content=None,
                embed=await builder.build_error_embed(
                    "You're not listening to Spotify."
                ),
            )


def setup(bot):
    bot.add_cog(Spotify(bot))
