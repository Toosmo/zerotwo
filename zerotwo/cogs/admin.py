import aiohttp
import discord
from discord.ext import commands


class Admin(commands.Cog):
    """Commands for controlling the bot.
    Mostly owner only."""

    def __init__(self, bot):
        self.bot = bot
        self._last_result = None
        self.session = aiohttp.ClientSession(loop=bot.loop)

    async def cog_check(self, ctx):
        """Checks whether the command was invoked by the owner of the bot."""

        return await self.bot.is_owner(ctx.author)

    def cog_unload(self):
        """Cleanup is called whenever the cog is removed."""

        self.bot.loop.create_task(self.session.close())

    @commands.group(hidden=True)
    async def status(self, ctx):
        """Changes the bot's status."""

    @commands.command(hidden=True)
    async def shutdown(self, ctx):
        """Shuts down the bot."""

        await ctx.message.add_reaction("\U0001F44B")
        await self.bot.logout()

    @status.command(aliases=["listen", "watch"], hidden=True)
    async def play(self, ctx, *, media_title: str):
        """Change's the bot's presence between playing, listening or watching."""

        p_types = {"play": 0, "listen": 2, "watch": 3}
        my_media = discord.Activity(name=media_title, type=p_types[ctx.invoked_with])
        await self.bot.change_presence(activity=my_media)
        await ctx.message.add_reaction("\u2705")

    @commands.command(hidden=True)
    async def avatar(self, ctx):
        """Changes the bot's avatar.
        Any image uploaded with your message will be used as the avatar."""

        async with ctx.typing():
            try:
                avatar_url = ctx.message.attachments[0].url
                async with self.session.get(avatar_url) as response:
                    avatar_bytes = await response.read()
                try:
                    await self.bot.user.edit(avatar=avatar_bytes)
                except discord.InvalidArgument:
                    await ctx.send(":no_entry_sign: You must upload an image file.")
                except discord.HTTPException:
                    await ctx.send("Changing the avatar failed.")
                else:
                    await ctx.send("Do I look prettier now, darling?")
            except IndexError:
                await ctx.send(":no_entry_sign: You didn't upload a file.")


def setup(bot):
    bot.add_cog(Admin(bot))
