import random

from discord.ext import commands


class Quote(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def quote(self, ctx):
        """A random quote from Zero Two."""

        quotes = [
            "Oh, found one.",
            "I'm always alone too, thanks to these horns.",
            "If you don't belong here, just build a place where you do.",
            "Your taste makes my heart race.",
            "Found you, my darling.",
            "Here, this is nice and sweet!",
            "I feel like I'm gonna suffocate in here.",
            "You are just like me.",
            "I like the look in your eyes. It makes my heart race.",
            "I'll let you have him this one time. Go for it!",
            "Once we die, we'll only be a statistic. It won't matter what we're called.",
            "Just look at this lifeless city. There are no skies or oceans here. It's a one-way street to nowhere. A dead end life.",  # noqa
            "Darling, wanna run away with me? I can get you out of here.",
            "Do you think I’m a monster too?",
            "How can I leave after hearing that?",
            "Nobody's ever said such embarrassing things to me before!",
            "You wanna ride me, huh?",
            "Of course you can do this. We can do this!",
            "Weaklings die. Big deal.",
            "Sure, he could. But that'd mean he didn't amount to much.",
            'What is "human" to you people?',
            "Your partner is me, and me alone.",
            "What'll it be? If you want off this ride, now's your chance.",
            "Swimming in the ocean feels so good! And it does taste salty.",
            "You're my wings right? If I'm with you, I can fly anywhere I want... We'll always be together right?",
            "A kiss is something you share with your special someone, is the one you kissed special to you?",
            "Kill more of those monsters and make me human. You're only my fodder, after all!",
            "Give me all your life. I'm going to become a human so I can meet my darling from back then.",
            "The leaving something behind part. My body can't do that. It's wonderful. You're all wonderful. You have the ability to decide your futures with your own hearts.",  # noqa
            "Darling, you pervert.",
            "You're pretty bossy, huh?",
            "Ordering me around again? You really are bossy.",
            "If I'm with you, I can fly anywhere I want.",
            "We'll always be together, right?",
            "Darling... Grab onto me and never let go, okay?",
            "Don't worry. We'll always be together... Until the day we die.",
            "I'll teach you what comes after kissing.",
            "I'll kill many, many and more and become human!",
            "Just quietly be devoured like the fodder you are!",
            "I'm a monster in disguise.",
        ]
        await ctx.send(random.choice(quotes))  # nosec


def setup(bot):
    bot.add_cog(Quote(bot))
