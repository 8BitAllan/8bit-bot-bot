import discord
from discord.ext import commands

class Mycog:
    """My custom cog that does stuff!"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def dog(self):
        """This does stuff!"""

        #Your code will go here
        await self.bot.say("RUFF RUFF WHAT? https://tenor.com/MqlY.gif ")

def setup(bot):
    bot.add_cog(Mycog(bot))
