import discord
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio
import random
from random import randint
import datetime

bot=commands.Bot(command_prefix = '+g')

class Start():
    """Start a giveaway faster!"""

    @bot.command(pass_context = True)
    async def start(ctx, duration = None, winners = None, prize = None):
        """Create a giveaway but faster!"""
        winners = int(winners)
        if duration == None:
            await ctx.bot.say(":x: | No `Duration` Was Inputted!")
        if winners == None:
            await ctx.bot.say(":x: | No Amount Of Winners` Were Inputted!")
        if prize == None:
            await ctx.bot.say(":x: | No `Prize` Was Inputted!")
        else:
            unit = duration[-1]
            if unit == 's':
                time = int(duration[:-1])
                longunit = 'seconds'
            elif unit == 'm':
                time = int(duration[:-1]) * 60
                longunit = 'minutes'
            elif unit == 'h':
                time = int(duration[:-1]) * 60 * 60
                longunit = 'hours'
            else:
                await ctx.bot.say('Invalid Unit! Use `s`, `m`, or `h`.')
            color = ''.join([random.choice('0123456789ABCDEF') for x in range(6)])
            color = int(color, 16)
            embed=discord.Embed(title=":tada: __**{} Giveaway!**__ :tada:".format(prize), colour = discord.Colour(value=color), timestamp = datetime.datetime.utcnow())
            embed.add_field(name = "Prize: ",value = "{}".format(prize))
            embed.add_field(name = "Winners: ", value = "{} Winner(s)".format(winners))
            embed.add_field(name = "Time: ", value = "{}".format(duration), inline = True)
            embed.set_footer(text = "Add The Reaction to join! Started @ ")
            give_away = await ctx.bot.say(embed = embed)
            ga_message = await ctx.bot.add_reaction(give_away, "\U0001f389")
            await asyncio.sleep(time)#Sleep for the duration

            ga_message = await ctx.bot.get_message(give_away.channel, give_away.id)
            ga_users=[]
            for user in await ctx.bot.get_reaction_users(ga_message.reactions[0]):
                ga_users.append(user.mention)
            ga_bot = ctx.message.server.get_member('396464677032427530') #giveaways id 396464677032427530
            ga_users.remove(ga_bot.mention)
            if len(ga_users) == 0:
                error = discord.Embed(title=":warning: Error!",description="The giveaway ended with no participants, could not chose a winner",color=0xff0000)
                await ctx.bot.say(embed=error)
            else:
                winner_list=[]
                for loop in range(winners):
                    winner = random.choice(ga_users)
                    ga_users.remove(winner)
                    winner_list.append(winner)
                    msg = ""
            
            color = ''.join([random.choice('0123456789ABCDEF') for x in range(6)])#Winning Embed
            color = int(color, 16)
            embed=discord.Embed(title=":tada: __**Giveaway Ended!**__ :tada:", colour = discord.Colour(value=color), timestamp = datetime.datetime.utcnow())
            embed.add_field(name = "Winners: ", value = "{} Winner(s)".format(winners))
            embed.add_field(name = "Winner(s): ", value = ",\n".join(winner_list))
            embed.add_field(name = "Prize: ", value = "{}".format(prize))
            embed.set_footer(text = "Better Luck Next Time! Ended @ ")
            await ctx.bot.edit_message(give_away, embed = embed)
            for winner in winner_list:
                msg += ", " + winner
            await ctx.bot.say(":tada: " + ", ".join(winner_list) + " won **{}**".format(prize))

def setup(bot):
    bot.add_cog(Start)
