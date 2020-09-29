import json
import logging

try:
    import discord
    from discord.ext import commands
except ModuleNotFoundError:
    print("discord.py not found.")

try:
    import extensions
except ModuleNotFoundError:
    print("extensions.py not found.")

try:
    import uvloop
except ModuleNotFoundError:
    print("uvloop not found, using default event loop instead.")
else:
    uvloop.install()

with open("config/config.json", "r") as f:
    config = json.load(f)

logger = logging.getLogger("discord")
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename="zerotwo.log", encoding="utf-8", mode="w")
handler.setFormatter(
    logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s")
)
logger.addHandler(handler)

intents = discord.Intents.default()
intents.presences = True
intents.members = True
intents.typing = False

prefix = config["BOT"]["PREFIX"]
owner_id = config["BOT"]["OWNER_ID"]


class ZeroTwo(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix=prefix, intents=intents, owner_id=owner_id, dm_help=None
        )

        for extension in extensions.initial_extensions:
            try:
                self.load_extension(extension)
            except (
                commands.ExtensionNotFound,
                commands.ExtensionAlreadyLoaded,
                commands.NoEntryPointError,
                commands.ExtensionFailed,
            ) as e:
                print(f"Failed to load an extension: {e}")

    async def on_ready(self):
        print(f"We have logged in as {self.user}")
        print(f"Running discord.py version: {discord.__version__}")


bot = ZeroTwo()
bot.run(config["BOT"]["TOKEN"])
