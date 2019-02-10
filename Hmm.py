import discord
from discord.ext import commands

class Mycog:
    """My custom cog that does stuff!"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def hmm(self):
        """HMM INTRESTING???"""

        #Your code will go here
        await self.bot.say("Hmm... https://tenor.com/YtvI.gif ")

def setup(bot):
    bot.add_cog(Mycog(bot))
