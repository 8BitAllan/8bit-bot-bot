import discord
import asyncio
from discord.ext import commands

class Status:
    def __init__(self, taco):
        self.taco = taco
            
    async def on_ready(self, taco):
        await self.taco.change_presence(game=discord.Game(name='taco help | {} servers'.format(str(len(self.taco.servers))), type=1, url="https://twitch.tv/#"))            


def setup(taco):
    taco.add_cog(Status(taco))
    print("Status is loaded")
