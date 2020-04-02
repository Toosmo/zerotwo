from discord.ext import commands

import extensions

from .utils import embed_builder as builder


class ExtensionHandler(commands.Cog, command_attrs={"hidden": True}):
    """Handles loading and unloading of extensions."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="load")
    @commands.is_owner()
    async def extension_load(self, ctx, *, cog: str):
        """Loads an extension."""

        self.bot.load_extension("cogs." + cog)
        await ctx.message.add_reaction("\u2705")

    @extension_load.error
    async def extension_load_error(self, ctx, error):
        # Errors invoked by commands are wrapped by CommandInvokeError,
        # so we must get the original error with the 'original' attribute.
        error = getattr(error, "original", error)

        if isinstance(error, commands.ExtensionNotFound):
            await ctx.send(
                content=None,
                embed=await builder.build_error_embed("Extension not found."),
            )
        elif isinstance(error, commands.ExtensionAlreadyLoaded):
            await ctx.send(
                content=None,
                embed=await builder.build_error_embed("Extension is already loaded."),
            )
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(
                content=None,
                embed=await builder.build_error_embed("No extension given."),
            )
        elif isinstance(error, commands.NoEntryPointError):
            await ctx.send(
                content=None,
                embed=await builder.build_error_embed(
                    "Extension doesn't have a setup function."
                ),
            )
        elif isinstance(error, commands.ExtensionFailed):
            await ctx.send(
                content=None,
                embed=await builder.build_error_embed(
                    "Extension setup function had an execution error."
                ),
            )

    @commands.command(name="unload")
    @commands.is_owner()
    async def extension_unload(self, ctx, *, cog: str):
        """Unloads an extension."""

        self.bot.unload_extension("cogs." + cog)
        await ctx.message.add_reaction("\u2705")

    @extension_unload.error
    async def extension_unload_error(self, ctx, error):
        error = getattr(error, "original", error)

        if isinstance(error, commands.ExtensionNotLoaded):
            await ctx.send(
                content=None,
                embed=await builder.build_error_embed("Extension not loaded."),
            )
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(
                content=None,
                embed=await builder.build_error_embed("No extension given."),
            )

    @commands.command(name="reload")
    @commands.is_owner()
    async def extension_reload(self, ctx, *, cog: str):
        """Reloads all extensions or a given extension."""

        if cog == "all":
            for cog in extensions.initial_extensions:
                if cog != "cogs.extension_handler":
                    self.bot.reload_extension(cog)
            await ctx.message.add_reaction("\u2705")
        else:
            self.bot.reload_extension("cogs." + cog)
            await ctx.message.add_reaction("\u2705")

    @extension_reload.error
    async def extension_reload_error(self, ctx, error):
        error = getattr(error, "original", error)

        if isinstance(error, commands.ExtensionNotLoaded):
            await ctx.send(
                content=None,
                embed=await builder.build_error_embed("Extension not loaded."),
            )
        elif isinstance(error, commands.ExtensionNotFound):
            await ctx.send(
                content=None,
                embed=await builder.build_error_embed("Extension not found."),
            )
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(
                content=None,
                embed=await builder.build_error_embed("No extension given."),
            )
        elif isinstance(error, commands.NoEntryPointError):
            await ctx.send(
                content=None,
                embed=await builder.build_error_embed(
                    "Extension doesn't have a setup function."
                ),
            )
        elif isinstance(error, commands.ExtensionFailed):
            await ctx.send(
                content=None,
                embed=await builder.build_error_embed(
                    "Extension setup function had an execution error."
                ),
            )


def setup(bot):
    bot.add_cog(ExtensionHandler(bot))
