import discord
import os
from discord.ext import commands

class General(commands.Cog):

    def __init__(self, client):
        self.client = client

    def is_owner(self, ctx):
        return ctx.message.author.id == 731286082548924449

    def is_mod(self, member : discord.Member):
        return member.guild_permissions.mute_members or member.guild_permissions.administrator or member.id == 731286082548924449

## On-ready event            
    @commands.Cog.listener()
    async def on_ready(self):
        print('General cog online')

    @commands.command(commands.has_permissions(administrator=True), commands.check(is_owner))
    async def setup(self, ctx):
        if discord.utils.get(ctx.guild.roles, name='Muted'):
            await ctx.send('The bot has already been setup for this server.')
        else:
            member = ctx.author
            guild = member.guild
            perms = discord.Permissions(send_messages=False)

            await guild.create_role(name='Muted', colour=discord.Colour(0x202020))
            role = discord.utils.get(member.guild.roles, anme='Muted')
            await role.edit(name='Muted', permissions=perms)

            for channel in guild.text_channels:
                await channel.set_permissions(role, send_messages=False)

            embed=discord.Embed(description="The bot's role + muted role must have a high hierarchy in the server to work. Follow the gif below if needed. Also, only people with _manage messages_ can use the bots moderation commands", color=0x00ccff)
            embed.set_author(name="Setup complete. Great!", icon_url=f"https://i.imgur.com/HOn2phK.png")
            embed.set_image(url='https://media0.giphy.com/media/mB9vJSEuNXxHAMdfHT/giphy.gif')
            await ctx.send(embed=embed)
            await ctx.message.delete()

    @setup.error
    async def setup_error(self, ctx, error):
        if isinstance(error, commands.TooManyArguments):
            await ctx.send('Too many arguements! Just do !setup')


def setup(client):
    client.add_cog(General(client))