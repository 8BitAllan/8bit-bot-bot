import discord
from discord.ext import commands
from utils.dataIO import dataIO
import os
from copy import deepcopy
import asyncio
import json
import random
import datetime 

default_settings = {
                    "TACOS": 0,
                    "BANK-TACOS": 0,
                    "TACO-COINS": 0,
                    }
                    

default_user_settings = {
                    "IN_GAME": False,
                    "IN_QUEUE": False
                    "WINS": 0 
                    "DEATHS": 0,
                    "BET": 0
                    }

default_server_settings = {
                    "IN_GAME": False,
                    "WAITING_FOR_GAME": False,
                    "PLAYERS": 0, 
                    "QUEUE": 0
                    }

class Economy:
    def __init__(self, taco):
        self.taco = taco
        self.settings = dataIO.load_json('data/economy/settings.json')
        self.settings_server = dataIO.load_json('data/economy/russian-roulette/servers.json')
        self.settings_user = dataIO.load_json('data/economy/russian-roulette/users.json')
        self.version = "0.0.1"



    async def save_settings(self):
        dataIO.save_json('data/economy/settings.json', self.settings)
        dataIO.save_json('data/economy/russian-roulette/users.json', self.settings_user)  
        dataIO.save_json('data/economy/russian-roulette/servers.json', self.settings_server)  

    async def _data_check(self, ctx):
        user = ctx.message.author
        server = ctx.message.server
        if user.id not in self.settings:
            self.settings[user.id] = deepcopy(default_settings)
            await self.save_settings()
        if user.id not in self.settings_user:
            self.settings_user[user.id] = deepcopy(default_user_settings)
            await self.save_settings()
        if server.id not in self.settings_server:
            self.settings_server[server.id] = deepcopy(default_server_settings)
            await self.save_settings()        
            
    async def queue_player(self, ctx):
        user = ctx.message.author
        server = ctx.message.server
        if self.settings_user[user.id]["IN_GAME"] == True:
            await self.taco.say("You are already in a game.")
            return
        if self.settings_user[user.id]["IN_QUEUE"] == True:
            await self.taco.say("You are already in a queue.")
            return        
        self.settings_user[user.id]["IN_QUEUE"] = True
        self.settings_server[server.id]["WAITING_FOR_GAME"] = True
        Queue = self.settings_server[server.id]["QUEUE"] 
        New_Queue = Queue + 1
        self.settings_server[server.id]["QUEUE"] = New_Queue
        await self.taco.say("You are now in a queue for a russian roulette game.")
        await self.save_settings()
        

    @commands.command(pass_context=True, aliases=["rr", "russian-roulette", "roulette"])
    async def russian_roulette(self, ctx, arg="help", arg2=None):
        server = ctx.message.server
        user = ctx.message.author
        self._data_check(ctx)
        if arg == "help":
            embed = discord.Embed(color=0x36393e)
            embed.add_field(name=":taco: **Russian Roulette** :taco", value="**taco rr play <bet>** - Play a match on your current server, reminder, your bet is in taco tokens, so be sure to have enough.\n**taco rr start** - Start a Russian Roulette.")
            embed.timestamp = datetime.datetime.utcnow()
            embed.set_footer(text=f"Requested by {ctx.message.author.name}", icon_url=f"{ctx.message.author.avatar_url}")
        if arg != "help":
            if arg == "play" and arg2 != None:
                Tokens = self.settings[ctx.message.author.id]["TACO-COINS"]
                if int(arg2) > Tokens:
                    await self.taco.say("The amount of tokens you are currently betting is more than the amount you have, try to compress some using `taco compress <tacos>`.")
                    return
                New_Token_Bal = Tokens - arg2
                self.settings[ctx.message.author.id]["TACO-COINS"] = New_Token_Bal
                msg = await self.taco.say("Successfully deducted **{arg2} tokens** from your account.")
                self.settings_user[user.id]["BET"] = arg2
                await self.taco.edit_message(msg, "Now searching for a Russian Roulette game...")
                await self.queue_player(ctx)
    
            

            
            
    @commands.command(pass_context=True)
    async def compress(self, ctx, amount: int="None"):
        try:
            await self._data_check(ctx)
            Bal = self.settings[ctx.message.author.id]["TACOS"]
            if amount > Bal:
                await self.taco.say("Your amount that you want to compress into Taco Tokens is bigger than your balance, try withdrawing some in using `taco withdraw`.")
                return
            if amount == "None":
                await self.taco.say("Usage: `taco compress <amount>`")
                return
            Tokens = amount/2
            New_Tokens = self.settings[ctx.message.author.id]["TACO-COINS"] + Tokens
            New_Bal = Bal - amount
            self.settings[ctx.message.author.id]["TACOS"] = New_Bal
            self.settings[ctx.message.author.id]["TACO-COINS"] = New_Tokens
            await self.taco.say(f"You have successfully compressed **{amount} tacos** into **{Tokens} taco tokens.**.")
            await self.save_settings()
        except Exception as e:
            await self.taco.say(e)  
    
    @commands.command(pass_context=True)
    async def uncompress(self, ctx, amount: int="None"):
        try:
            await self._data_check(ctx)
            Tokens = self.settings[ctx.message.author.id]["TACO-COINS"]
            Bal = self.settings[ctx.message.author.id]["TACOS"]
            if amount > Tokens:
                await self.taco.say("Your amount that you wish to compress is more than the amount you have.")
                return
            if amount == "None":
                await self.taco.say("Usage: `taco uncompress <amount>`")
                return
            New_Token_Bal = Tokens - amount 
            self.settings[ctx.message.author.id]["TACO-COINS"] = New_Token_Bal
            New_Bal = amount*2 + Bal
            self.settings[ctx.message.author.id]["TACOS"] = New_Bal
            await self.taco.say(f"Translated **{amount}** tokens into **{New_Bal}** tacos.")
            await self.save_settings()
        except Exception as e:
            await self.taco.say(e)

    @commands.cooldown(1, 86400, commands.BucketType.user)
    @commands.command(pass_context=True)      
    async def daily(self, ctx):
        try:
            await self._data_check(ctx)
            New_Bal = self.settings[ctx.message.author.id]["TACOS"] + 5000
            self.settings[ctx.message.author.id]["TACOS"] = New_Bal
            await self.taco.say("Congrats! You just got **5,000** free tacos for using this command! Check again in 24 hours.")
            await self.save_settings()
        except Exception as e:
            await self.taco.say(e)
            
    @commands.cooldown(1, 3, commands.BucketType.user)            
    @commands.command(pass_context=True)  
    async def work(self, ctx):     
        try:
            await self._data_check(ctx)
            Coins = random.randint(25, 150)
            Updated_Bal = self.settings[ctx.message.author.id]["TACOS"] + Coins
            self.settings[ctx.message.author.id]["TACOS"] = Updated_Bal
            await self.save_settings()
            embed = discord.Embed(color=0x36393e)
            embed.add_field(name=f"{ctx.message.author.name} worked and gained {Coins} tacos. :taco:", value=f"This adds {Coins} to your balance. ({Updated_Bal})") 
            embed.timestamp = datetime.datetime.utcnow()
            await self.taco.say(embed=embed)
        except Exception as e:
            await self.taco.say(e)
            
    @commands.command(pass_context=True, aliases=["balance", "b"])
    async def bal(self, ctx, user: discord.User="None"):
        """Check your taco balance, bank balance, total balance."""        
        await self._data_check(ctx)
        print(f"{ctx.message.author} did a command.")        
        if user == "None":
            YOUR_TACOS = self.settings[ctx.message.author.id]["TACOS"]
            YOUR_BANK_TACOS = self.settings[ctx.message.author.id]["BANK-TACOS"]
            YOUR_TACO_TOKENS = self.settings[ctx.message.author.id]["TACO-COINS"]            
            YOUR_TOTAL_TACOS = YOUR_BANK_TACOS + YOUR_TACOS
            embed = discord.Embed(title=":taco: {}'s Balance".format(ctx.message.author.name), color=0x36393e)
            embed.add_field(name="Balance", value="{:,}".format(YOUR_TACOS))            
            embed.add_field(name="Bank", value="{:,}".format(YOUR_BANK_TACOS))
            embed.add_field(name="Tokens", value="{:,}".format(YOUR_TACO_TOKENS))            
            embed.add_field(name="Total", value="{:,}".format(YOUR_TOTAL_TACOS))
            embed.timestamp = datetime.datetime.utcnow()
            await self.taco.say(embed=embed)           
            return      
        elif user != "None":
            THEIR_TACOS = self.settings[user.id]["TACOS"]
            THEIR_BANK_TACOS = self.settings[user.id]["BANK-TACOS"]
            THEIR_TACO_TOKENS = self.settings[user.id]["TACO-COINS"]            
            THEIR_TOTAL_TACOS = THEIR_TACOS + THEIR_BANK_TACOS
            embed = discord.Embed(title=":taco: {}'s Balance".format(user.name), color=0x36393e)
            embed.add_field(name="Balance", value="{:,}".format(THEIR_TACOS))            
            embed.add_field(name="Bank", value="{:,}".format(THEIR_BANK_TACOS))
            embed.add_field(name="Tokens", value="{:,}".format(THEIR_TACO_TOKENS))            
            embed.add_field(name="Total", value="{:,}".format(THEIR_TOTAL_TACOS))
            embed.timestamp = datetime.datetime.utcnow()
            await self.taco.say(embed=embed)
            return



    @commands.command(pass_context=True, aliases=["c", "felony"])
    async def crime(self, ctx):
        Chance = random.randint(1,9)
        if Chance == 3:
            CRIME_BAL = random.randint(1000, 100000)
            NEW_CRIME_BAL = 1000 + self.settings[ctx.message.author.id]["TACOS"]
            self.settings[ctx.message.author.id]["TACOS"] = NEW_CRIME_BAL
            await self.save_settings()
            await self.taco.say("Success! You successfully did a crime and earned 1,000 tacos. :taco:")
            return
        else:
            NEW_CRIME_BAL = self.settings[ctx.message.author.id]["TACOS"] - 1000
            self.settings[ctx.message.author.id]["TACOS"] = NEW_CRIME_BAL
            await self.save_settings()
            await self.taco.say("Sorry, you tried to do a crime and got fined 1,000 tacos.")
            
    @commands.command(pass_context=True, aliases=["r", "robuser"])
    async def rob(self, ctx, user: discord.User):
        """You have a chance to steal all of someone's balance."""    
        await self._data_check(ctx)
        THEIR_TACOS = self.settings[user.id]["TACOS"]
        if THEIR_TACOS == 0 or THEIR_TACOS < 0:
            await self.taco.say("**{}** does not have any tacos on them, you should maybe try later.".format(user.name))
            return
        elif user == ctx.message.author:
            await self.taco.say("You can't rob yourself.")
            return
        else:
            Chance = random.randint(1,6)
            if Chance == 3:
                ROBBED = self.settings[user.id]["TACOS"] - self.settings[user.id]["TACOS"]
                self.settings[user.id]["TACOS"] = ROBBED
                NEW_CRIME_BAL = self.settings[user.id]["TACOS"] + self.settings[ctx.message.author.id]["TACOS"]
                self.settings[ctx.message.author.id]["TACOS"] = NEW_CRIME_BAL
                await self.save_settings()
                self.taco.send_message(user, "Sorry, **{}** robbed you of your tacos in your balance! (TIP: Prevent this by depositing your tacos)".format(ctx.message.author.name))
                await self.taco.say("Success! You successfully robbed **{}** of all his tacos.".format(user.name))
                return
            else:
                NEW_CRIME_BAL = self.settings[ctx.message.author.id]["TACOS"] - 1000
                self.settings[ctx.message.author.id]["TACOS"] = NEW_CRIME_BAL
                await self.save_settings()
                await self.taco.say("Sorry, you tried to rob **{}** and got fined 1,000 tacos.".format(user.name))                

    @commands.command(pass_context=True, aliases=["depositall", "depoall"])
    async def depall(self, ctx):
        """Deposit all your tacos into your bank."""
        await self._data_check(ctx)        
        print(f"{ctx.message.author} did a command.")        
        YOUR_BAL = self.settings[ctx.message.author.id]["TACOS"]
        if YOUR_BAL == 0 or YOUR_BAL < 0:
            await self.taco.say("You can't deposit in tacos that don't exist.")
            return
        else:
            await self._data_check(ctx)
            YOUR_BAL = self.settings[ctx.message.author.id]["TACOS"]
            NEW_BAL = self.settings[ctx.message.author.id]["TACOS"] - self.settings[ctx.message.author.id]["TACOS"]
            NEW_BANK_BAL = self.settings[ctx.message.author.id]["BANK-TACOS"] + self.settings[ctx.message.author.id]["TACOS"]
            self.settings[ctx.message.author.id]["TACOS"] = NEW_BAL
            self.settings[ctx.message.author.id]["BANK-TACOS"] = NEW_BANK_BAL        
            await self.save_settings()
            await self.taco.say("Added **{:,}** tacos to your taco bank.".format(YOUR_BAL))
            return

    @commands.command(pass_context=True, aliases=["payuser", "p"])
    async def pay(self, ctx, user: discord.User="None", amount: int="None"):
        """Pay a user tacos from your balance."""
        await self._data_check(ctx)
        YOUR_BAL = self.settings[ctx.message.author.id]["TACOS"]
        if user == "None":
            await self.taco.say("Usage: `taco pay <@user> <amount>`")
            return
        if amount == "None":
            await self.taco.say("Usage: `taco pay <@user> <amount>`")
            return
        if amount > YOUR_BAL:
            amount_needed = amount - YOUR_BAL            
            await self.taco.say("You have an insufficient amount [You need **{:,}** taco(s) in your balance to perform that transaction]".format(amount_needed))
        else:
            THEIR_BAL = self.settings[user.id]["TACOS"]
            YOUR_UPDATED_BAL = self.settings[ctx.message.author.id]["TACOS"] - amount            
            THEIR_UPDATED_BAL = self.settings[user.id]["TACOS"] + amount
            self.settings[ctx.message.author.id]["TACOS"] = YOUR_UPDATED_BAL            
            self.settings[user.id]["TACOS"] = THEIR_UPDATED_BAL
            await self.save_settings()
            await self.taco.say("Thanks for being generous, you just paid **{}** {:,} tacos :taco:".format(user.mention, amount))
            return            
            
        
    @commands.command(pass_context=True, aliases=["deposit", "depo"])
    async def dep(self, ctx, amount: int):
        """Deposit some tacos from your balance."""
        await self._data_check(ctx)        
        if ctx.message.author.id not in self.settings:
            await self.taco.say("You're not in the database.")
            
        YOUR_BAL = self.settings[ctx.message.author.id]["TACOS"]
        if YOUR_BAL == 0 or YOUR_BAL < 0:
            await self.taco.say("You can't deposit in tacos that don't exist.")
            return
        if amount > YOUR_BAL:
            amount_needed = amount - YOUR_BAL
            await self.taco.say("You have an insufficient amount [You need **{:,}** taco(s) in your balance to perform that transaction]".format(amount_needed))
            return
        else:
            NEW_BAL = self.settings[ctx.message.author.id]["TACOS"] - amount
            self.settings[ctx.message.author.id]["TACOS"] = NEW_BAL
            NEW_BANK_BAL = self.settings[ctx.message.author.id]["BANK-TACOS"] + amount
            self.settings[ctx.message.author.id]["BANK-TACOS"] = NEW_BANK_BAL
            await self.save_settings()
            await self.taco.say("Added **{:,}** tacos to your taco bank.".format(amount))
            return
    @commands.command(pass_context=True, name="withdraw", aliases=["with"])
    async def _withdraw(self, ctx, amount: int):
        """Withdraw tacos from your bank."""
        await self._data_check(ctx)
        YOUR_BANK_BAL = self.settings[ctx.message.author.id]["BANK-TACOS"]
        YOUR_BAL = self.settings[ctx.message.author.id]["TACOS"]        
        if amount > YOUR_BANK_BAL:
            amount_needed = amount - YOUR_BAL
            await self.taco.say("You have an insufficient amount [You need **{:,}** taco(s) in your bank to perform that transaction]".format(amount_needed))             
        else:
            NEW_BANK_BAL = self.settings[ctx.message.author.id]["BANK-TACOS"] - amount
            self.settings[ctx.message.author.id]["BANK-TACOS"] = NEW_BANK_BAL
            NEW_BAL = self.settings[ctx.message.author.id]["TACOS"] + amount
            self.settings[ctx.message.author.id]["TACOS"] = NEW_BAL
            await self.save_settings()
            await self.taco.say("Added **{:,}** tacos to your balance.".format(amount))
            return
        
    @commands.command(pass_context=True, name="coinflip", aliases=["cf" , "coin"])
    async def coinflip(self, ctx, amount: int="None"):
        await self._data_check(ctx)
        if amount == "None":
            await self.taco.say("Usage: `taco coinflip <amount>`")
            return        
        YOUR_BAL = self.settings[ctx.message.author.id]["TACOS"] 
        if amount > YOUR_BAL:
            amount_needed = amount - YOUR_BAL
            await self.taco.say("You have an insufficient amount [You need **{:,}** taco(s) in your balance to perform that transaction]".format(amount_needed)) 
        else:
            coin = random.randint(1,2)
            if coin == 1:
                YOUR_NEW_BAL = amount*2
                self.settings[ctx.message.author.id]["TACOS"] = YOUR_NEW_BAL
                await self.taco.say("**Heads!** It's a winner! [You have **{}** new tacos awaiting for you.]".format(YOUR_NEW_BAL))
            if coin == 2:
                YOUR_NEW_BAL = YOUR_BAL-amount
                self.settings[ctx.message.author.id]["TACOS"] = YOUR_NEW_BAL
                await self.taco.say("**Tails!** Yikes! You'll, get 'em next time. [You lost your bet.]")            
            
            
            
            
        
def check_folders():
    if not os.path.exists('data/economy/'):
        os.mkdir('data/economy/')


def check_files():
    if not dataIO.is_valid_json('data/economy/settings.json'):
        defaults = {}
        dataIO.save_json('data/economy/settings.json', defaults)
        
def setup(taco):
    check_folders()
    check_files()
    taco.add_cog(Economy(taco))
    print("Economy is loaded")

