import discord
from discord.ext import commands
from copy import deepcopy
import time

from utils.dataIO import dataIO
from utils import permissions


user_settings = {
                 "XP": 0,
                 "LEVEL": 0
                 }


server_settings = {
                   "LEVELING": False
                   }

class Leveling:
    def __init__(self, taco):
        self.taco = taco
        self.server_settings = dataIO.load_json('data/leveling/settings.json')
        
    async def _data_check(self, ctx):
        user = ctx.message.author
        server = ctx.message.server
        if not dataIO.is_valid_json(f'data/leveling/server_data/{server.id}.json'):
            defaults = {}
            dataIO.save_json(f'data/leveling/server_data/{server.id}.json', defaults)        
        settings = dataIO.load_json(f'data/leveling/server_data/{server.id}.json')
        if user.id not in settings:
            settings[user.id] = deepcopy(user_settings)
            dataIO.save_json(f'data/leveling/server_data/{server.id}.json', settings)

            
    @commands.command(pass_context=True)
    @permissions.has_permissions(manage_server=True)
    async def leveling(self, ctx):
        try:
            if ctx.message.server.id not in self.server_settings:
                self.server_settings[ctx.message.server.id] = deepcopy(server_settings)
                dataIO.save_json('data/leveling/settings.json', self.server_settings)        
            if self.server_settings["LEVELING"] == False:
                self.server_settings["LEVELING"] = True
                await self.taco.say("Leveling has been enabled in this guild.")
                dataIO.save_json('data/leveling/settings.json', self.server_settings)
            if self.server_settings["LEVELING"] == True:
                self.server_settings["LEVELING"] = False
                dataIO.save_json('data/leveling/settings.json', self.server_settings)
                await self.taco.say("Leveling has been disabled in this guild.")
        except Exception as e:
            fmt = 'Failed to execute command: ' + str(e)
            await self.taco.say(fmt)
            print(fmt)
        
    
def check_files():
    if not dataIO.is_valid_json('data/leveling/settings.json'):
        defaults = {}
        dataIO.save_json('data/leveling/settings.json', defaults)    
    
def setup(taco):
    taco.add_cog(Leveling(taco))
    check_files()
    print("Leveling is loaded")
