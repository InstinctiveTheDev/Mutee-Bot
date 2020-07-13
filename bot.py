import discord
import os
from discord.ext import commands

client = commands.Bot(command_prefix = '.')

def is_owner(ctx):
    return ctx.message.author.id == 731286082548924449

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{sum(len(guild.members) for guild in client.guilds)} users"))
    print('Bot is online.')

@client.command()
@commands.check(is_owner)
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')

@client.command()
@commands.check(is_owner)
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

client.run('NzMyMDExMjk2Mjg2OTY1ODIx.XwuZ2g.IHrkv9dQzdOzKIVwLm5wP-_qVSg')
