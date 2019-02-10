import discord
from discord.ext import commands

class Mycog:
    """My custom cog that does stuff!"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def punch(self):
        """Dont Worry Ill Do This!"""

        #Your code will go here
        await self.bot.say("ONE PUNCH AND KNOCKOUT")

def setup(bot):
    bot.add_cog(Mycog(bot))