import discord
from discord.ext import commands

class Mycog:
    """My custom cog that does stuff!"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def smash(self):
        """This does stuff!"""

        #Your code will go here
        await self.bot.say("I HATE THIS PC https://media.giphy.com/media/9o9dh1JRGThC1qxGTJ/giphy.gif")

def setup(bot):
    bot.add_cog(Mycog(bot))
