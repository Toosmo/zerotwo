import platform

import discord
from discord.ext import commands

from ..utils import bot_stats, user_utils

BOT_COLOUR = discord.Colour(0x00A597)
ERROR_COLOUR = discord.Colour(0xDD2E44)


async def build_about_embed(bot: commands.Bot):
    owner = bot.get_user(bot.owner_id)

    embed = discord.Embed(title=f"About {bot.user.name}", colour=BOT_COLOUR)
    embed.set_thumbnail(url=bot.user.avatar_url_as(static_format="png"))
    embed.set_footer(text=f"{bot.command_prefix}help for more commands.")

    embed.add_field(name="Owner:", value=owner.mention)
    embed.add_field(name="Memory usage:", value=await bot_stats.memory_usage())
    embed.add_field(name="WebSocket latency", value=f"{1000*bot.latency:.1f}ms")
    embed.add_field(
        name="Powered by:",
        value=f"Python {platform.python_version()} & discord.py {discord.__version__}",
        inline=False,
    )
    embed.add_field(name="Uptime:", value=await bot_stats.uptime())

    return embed


async def build_error_embed(error_text: str):
    embed = discord.Embed(colour=ERROR_COLOUR)
    embed.description = f":no_entry_sign: {error_text}"

    return embed


async def build_server_embed(ctx: commands.Context):
    embed = discord.Embed(title=f"About {ctx.guild.name}", colour=BOT_COLOUR)
    embed.set_thumbnail(url=ctx.guild.icon_url_as(static_format="png"))
    embed.set_footer(text="A community since:")
    embed.timestamp = ctx.guild.created_at

    embed.add_field(name="Server owner:", value=ctx.guild.owner.mention)
    embed.add_field(name="Voice region:", value=ctx.guild.region)
    embed.add_field(name="Server ID:", value=ctx.guild.id, inline=False)

    return embed


async def build_spotify_embed(ctx: commands.Context):
    activity = ctx.author.activity

    if len(ctx.author.activities) > 1:
        for n in ctx.author.activities:
            if isinstance(n, discord.Spotify):
                activity = n

    embed = discord.Embed(
        title=f"{ctx.author.display_name} is currently listening to",
        colour=discord.Colour(0x1DB954),
    )
    embed.set_thumbnail(url=activity.album_cover_url)

    embed.add_field(name="Title:", value=activity.title, inline=False)

    if len(activity.artists) > 1:
        embed.add_field(
            name="Artists:", value=", ".join(activity.artists), inline=False
        )
    else:
        embed.add_field(name="Artist:", value=activity.artists[0], inline=False)

    embed.add_field(name="Album:", value=activity.album, inline=False)
    embed.add_field(
        name="Song link:",
        value=f"https://open.spotify.com/track/{activity.track_id}",
        inline=False,
    )

    return embed


async def build_user_embed(member: discord.Member):
    if member.colour == discord.Colour.default():
        colour = BOT_COLOUR
    else:
        colour = member.colour

    embed = discord.Embed(title=f"About {member}", colour=colour)

    embed.set_thumbnail(url=member.avatar_url_as(static_format="png"))
    embed.set_footer(text="A member since:")
    embed.timestamp = member.joined_at

    if hasattr(member, "status"):
        embed.add_field(
            name="Status:", value=await user_utils.get_status(member.status)
        )

    if member.activity is not None:
        embed.add_field(
            name="Activity:", value=await user_utils.get_activity(member.activity)
        )

    embed.add_field(name="Highest role:", value=member.top_role.mention, inline=False)
    embed.add_field(name="User ID:", value=member.id)

    return embed
