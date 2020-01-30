import discord
from discord.ext import commands

class Tracker(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    #@commands.command()
    #async def trackerTest(self, ctx):
    #    await ctx.send('Tracker.py Test')


def setup(client):
    client.add_cog(Tracker(client))