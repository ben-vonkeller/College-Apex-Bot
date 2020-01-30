import discord
from discord.ext import commands

class Countdown(commands.Cog):

    def __init__(self, client):
        self.client = client

    #@commands.command()
    #async def countdownTest(self, ctx):
    #    await ctx.send('Countdown.py Test')

def setup(client):
    client.add_cog(Countdown(client))