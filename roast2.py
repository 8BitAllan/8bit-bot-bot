import discord
from discord.ext import commands

class Mycog:
    """My custom cog that does stuff!"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def roast2(self, user : discord.Member):
        """Roast People"""

        #Your code will go here
        await self.bot.say("I’d smack " + user.mention + " but that would be animal abuse")

def setup(bot):
    bot.add_cog(Mycog(bot))
