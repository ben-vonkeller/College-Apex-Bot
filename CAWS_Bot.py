import discord
import os, sys
from discord.ext import commands
from discord.utils import get
import youtube_dl

# Discord Token required to use the bot
TOKEN = 'NjcwMTE5NDc2MDMyODMxNDg4.XloMVA.Pux5281oGzx6gE39kjZtpaZQpMM'

# Prefix for all commands
client = commands.Bot(command_prefix = '.')

# Global dictionary that is used to invoke the .champs command and list the lobbies
champDictionary = {}

playerDictionary = {}

# This event handler checks to see if a message is sent in the champs channel.
# If it is, it reads in the message, stores it in the dictionary, and makes the value
# associated with the key equal to whatever it was before plus one. Otherwise, it
# proceeds on as though the message was sent somewhere else
@client.event
async def on_message(message):
    if message.channel.name == 'champs':
        if message.content != '.clear':
            if message.content.lower() in champDictionary:
                temp = champDictionary.get(message.content.lower())
                temp = temp + 1
                champDictionary[message.content.lower()] = temp
            else:
                champDictionary[message.content.lower()] = 1
            if message.author.mention not in playerDictionary:
                playerDictionary[message.author.mention] = message.content.lower()
    await client.process_commands(message)

# Simple event handler that tells the command prompt that the bot is up and ready to be used.
@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.idle, activity=discord.Game('CAWS Starts Feb. 1st! Sign Up Now!'))
    print ('Bot is ready!')

# COMMAND USAGE: .load {extension name}
# Loads extensions that have different commands in them. Not implemented fully yet
@client.command()
@commands.has_permissions(ban_members=True)
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')

# COMMAND USAGE: .join
# When this command is invoked by a user, the bot will join the channel that the user is currently in.
# If the user is not in a channel, the command will not work properly
@client.command()
@commands.has_permissions(ban_members=True)
async def join(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
    
    await voice.disconnect()

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
        print(f'The bot has connected to {channel}\n')
    
    await ctx.send(f'Joined {channel}')

# COMMAND USAGE: .leave
# This command makes the bot leave whatever voice channel it is currently in.
@client.command()
@commands.has_permissions(ban_members=True)
async def leave(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.disconnect()
        print(f'The bot has left {channel}')
        await ctx.send(f'Left {channel}')
    else:
        print('Bot was told to leave voice channel, but was not in one')
        await ctx.send(f'Don\'t think I am in a voice channel')

# COMMAND USAGE: .countdown
# This command plays a countdown for scrims
@client.command()
@commands.has_permissions(ban_members=True)
async def countdown(ctx):
    countdownLink = str("https://www.youtube.com/watch?v=mT96R4JEtus")
    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
            print("Removed old song file")
    except PermissionError:
        print("Trying to delete song file, but it's being played")
        await ctx.send("Error: Currently Playing")
        return
    
    await ctx.send("Getting everything ready now")

    voice = get(client.voice_clients, guild=ctx.guild)

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        print("Downloading audio now\n")
        ydl.download([countdownLink])
    
    for file in os.listdir('./'):
        if file.endswith('.mp3'):
            name = file
            print(f'renamed file: {file}\n')
            os.rename(file, "song.mp3")

    voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: print(f'{name} has finished playing'))
    voice.source = discord.PCMVolumeTransformer(voice.source)
    voice.source.volume = .7

    
    await ctx.send('Countdown Starting Now')
    print('playing\n')

# COMMAND USAGE: .champs {Game Number}
# This command will take the global dictionary that counts how many times each message in
# a certain chat is said, and print it out, showing the number of players in each lobby
@client.command()
@commands.has_permissions(ban_members=True)
async def match(ctx, game):
    await ctx.send(f'Game {game} matches Below\n--------------------------------')
    for key in sorted(champDictionary, key=champDictionary.get, reverse=True):
        if key != '.clear':
            formatted = "{} - {}"
            await ctx.send(formatted.format(key, champDictionary[key]))
    champDictionary.clear()

    await ctx.send(f'--------------------------------\nGame {game} lobby info Below\n--------------------------------')
    for key in sorted(playerDictionary, key=playerDictionary.get, reverse=True):
        formatted = "{} - {}"
        await ctx.send(formatted.format(key, playerDictionary[key]))
    playerDictionary.clear()

# COMMAND USAGE: .unload {Extension Name}
# This command unloads a specific extension. Not currently used
@client.command()
@commands.has_permissions(ban_members=True)
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')


client.run(TOKEN)