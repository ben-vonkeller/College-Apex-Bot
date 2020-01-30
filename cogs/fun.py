import discord
from discord.ext import commands

class Fun(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    #@commands.command()
    #async def funTest(self, ctx):
    #    await ctx.send('fun.py Test')

    # COMMAND USAGE: .apex
    # Sends a message in the chat for fun that says "College Apex is
    # the best league, no questions asked!"
    @commands.command()
    async def apex(self, ctx):
        await ctx.send('College Apex is the best league, no questions asked')

def setup(client):
    client.add_cog(Fun(client))