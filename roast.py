import discord
from discord.ext import commands

class Mycog:
    """My custom cog that does stuff!"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def roast(self, user : discord.Member):
        """This does stuff!"""

        #Your code will go here
        await self.bot.say("It’s a shame " + user.mention + " you can't Photoshop your personality")

def setup(bot):
    bot.add_cog(Mycog(bot))
