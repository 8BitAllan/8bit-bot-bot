import discord
from discord.ext import commands

class Mycog:
    """My custom cog that does stuff!"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def roast1(self, user : discord.Member):
        """Roast People"""

        #Your code will go here
        await self.bot.say("Is there an app I can download to make " + user.mention + " disappear?")

def setup(bot):
    bot.add_cog(Mycog(bot))
