import discord
from discord.ext import commands, tasks


class StatusCycler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.status_dict = {
            # ActivityType values; playing = 0, streaming = 1, listening = 2, watching = 3
            "status": [
                {"name": "with my darling", "type": 0},
                {"name": f"{self.bot.command_prefix}help", "type": 0},
                {"name": "with the API", "type": 0},
            ]
        }
        self.status_cycler.start()
        self.status_counter = 0

    def cog_unload(self):
        self.status_cycler.cancel()

    @tasks.loop(minutes=10.0)
    async def status_cycler(self):
        status = self.status_dict["status"][self.status_counter]
        await self.bot.change_presence(
            activity=discord.Activity(name=status["name"], type=status["type"])
        )
        self.status_counter += 1
        if self.status_counter == len(self.status_dict["status"]):
            self.status_counter = 0

    @status_cycler.before_loop
    async def before_status_cycler(self):
        await self.bot.wait_until_ready()


def setup(bot):
    bot.add_cog(StatusCycler(bot))
