import json

from discord.ext import commands

with open("config.json", "r") as f:
    config = json.load(f)


class Example(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


def setup(bot):
    bot.add_cog(Example(bot))
