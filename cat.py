import discord
from discord.ext import commands

class Mycog:
    """My custom cog that does stuff!"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def cat(self):
        """MEOW MEOW MEOW"""

        #Your code will go here
        await self.bot.say("MEOW MEOW https://tenor.com/tzmM.gif ")

def setup(bot):
    bot.add_cog(Mycog(bot))
