import discord
from discord.ext import commands

class Mycog:
    """My custom cog that does stuff!"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def roast4(self, user : discord.Member):
        """Roast People"""

        #Your code will go here
        await self.bot.say("I’m sorry, was I meant to be offended? The only thing offending me is your face " + user.mention + " ")

def setup(bot):
    bot.add_cog(Mycog(bot))
