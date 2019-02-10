import discord
from discord.ext import commands

class Mycog:
    """My custom cog that does stuff!"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def nuke(self):
        """I Wonder What This Big Red Button Does"""

        #Your code will go here
        await self.bot.say("INCOMING!!! https://tenor.com/sTFz.gif ")

def setup(bot):
    bot.add_cog(Mycog(bot))
