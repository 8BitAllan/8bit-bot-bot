import dbl
import discord
from discord.ext import commands
import os
import aiohttp
import asyncio
import logging
import socket
import io
from .utils.dbl import DBL
            
class DiscordBotsOrgAPI:
    """Handles interactions with the discordbots.org API"""

    def __init__(self, taco):
        self.taco = taco
        self.token = ""
        self.dblpy = dbl.Client(self.taco, self.token)
        self.taco.loop.create_task(self.update_stats())
        
    async def update_stats(self):
        """This function runs every 30 minutes to automatically update your server count"""

        while True:
            logger.info('attempting to post server count')
            try:
                await self.dblpy.post_server_count()
                logger.info('Posted server count: ({})'.format(len(self.taco.servers)))
            except Exception as e:
                logger.exception('Failed to post server count\n{}: {}'.format(type(e).__name__, e))
                
            await asyncio.sleep(1800)


        

def setup(taco):
    global logger
    logger = logging.getLogger('taco')
    taco.add_cog(DiscordBotsOrgAPI(taco))
