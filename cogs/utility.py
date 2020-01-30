import discord
from discord.ext import commands

class Utility(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    #@commands.command()
    #async def utilityTest(self, ctx):
    #    await ctx.send('utility.py Test')

    # COMMAND USAGE: .clear
    # Clears a text channel
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def clear(self, ctx):
        await ctx.channel.purge()

def setup(client):
    client.add_cog(Utility(client))