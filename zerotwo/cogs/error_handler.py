import sys
import traceback

from discord.ext import commands

from .utils import embed_builder as builder


class CommandErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):

        if hasattr(ctx.command, "on_error"):
            return

        ignored = (commands.CommandNotFound, commands.NotOwner)
        error = getattr(error, "original", error)

        if isinstance(error, ignored):
            return

        elif isinstance(error, commands.DisabledCommand):
            await ctx.send(
                content=None,
                embed=await builder.build_error_embed(
                    "This command has been disabled."
                ),
            )

        elif isinstance(error, commands.NoPrivateMessage):
            await ctx.author.send(
                content=None,
                embed=await builder.build_error_embed(
                    "This command can't be used in private messages."
                ),
            )

        elif isinstance(error, commands.BadArgument):
            await ctx.send(
                content=None,
                embed=await builder.build_error_embed(
                    "I couldn't find that member. Please try again"
                ),
            )

        elif isinstance(error, commands.MissingPermissions):
            await ctx.send(
                content=None,
                embed=await builder.build_error_embed(
                    "You don't have the permission to do that."
                ),
            )

        elif isinstance(error, commands.BotMissingPermissions):
            await ctx.send(
                content=None,
                embed=await builder.build_error_embed(
                    "I don't have the permission to do that."
                ),
            )

        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(
                content=None,
                embed=await builder.build_error_embed(
                    "Missing one or more required arguments."
                ),
            )

        elif isinstance(error, commands.TooManyArguments):
            await ctx.send(
                content=None,
                embed=await builder.build_error_embed(
                    "Too many arguments were passed."
                ),
            )

        else:
            print(f"Ignoring exception in command {ctx.command}:", file=sys.stderr)
            traceback.print_exception(
                type(error), error, error.__traceback__, file=sys.stderr
            )


def setup(bot):
    bot.add_cog(CommandErrorHandler(bot))
