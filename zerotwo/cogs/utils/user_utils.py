import discord


async def get_status(status):
    switch = {
        discord.Status.online: "Currently online",
        discord.Status.offline: "Currently offline",
        discord.Status.idle: "Currently idle",
        discord.Status.dnd: "Do not Disturb",
    }
    return switch.get(status, None)


async def get_activity(activity):
    switch = {
        discord.ActivityType.playing: f"Playing {activity.name}",
        discord.ActivityType.streaming: f"Streaming {activity.name}",
        discord.ActivityType.listening: f"Listening to {activity.name}",
        discord.ActivityType.watching: f"Watching {activity.name}",
        discord.ActivityType.custom: f"{activity.name}",
    }
    return switch.get(activity.type, None)
