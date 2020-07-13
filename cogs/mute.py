import discord
import os
from discord.ext import commands

class Mute(commands.Cog):

    def __init__(self, client):
        self.client = client

    def is_owner(self, ctx):
        return ctx.message.author.id == 731286082548924449

    def is_mod(self, member : discord.Member):
        return member.guild_permissions.mute_members or member.guild_permissions.administrator or member.id == 731286082548924449

## On-ready event            
    @commands.Cog.listener()
    async def on_ready(self):
        print('Mute cog online')

## Mute command 
    @commands.command()
    @commands.check_any(commands.has_permissions(administrator=True), commands.has_permissions(mute_members=True), commands.check(is_owner))
    async def mute(self, ctx, member : discord.Member, *, reason=None):
        if discord.utils.get(ctx.guild.roles, name='Muted'):
            if member.is_mod(member):
                await ctx.send('Oops. You can\'t mute that person.')
            else:
                if member.nick.startswith('[Muted]'):
                    await ctx.send('That user is already muted.')
                else:
                    role = discord.utils.get(member.guild.roles, name='Muted')
                    await member.add_role(role)
                    nick = f'[Muted] {member}'
                    await member.edit(nick=nick[:-5])
                    embed=discord.Embed(description=f"**Reason :** {reason}", color=0x00ccff)
                    embed.set_author(name=f"{member} was muted", icon_url=f"{member.avatar_url}")
                    await ctx.send(embed=embed)
        else:
            await ctx.send('The bot hasn\'t been setup correctly. Use `.setup` to set up the bot.')
        await ctx.message.delete()

    @mute.error
    async def mute_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Oops. Please make sure to specify which use to mute.')

## Unmute command
    @commands.command()
    @commands.check_any(commands.has_permissions(administrator=True), commands.has_permissions(mute_members=True), commands.check(is_owner))
    async def unmute(self, ctx, member : discord.Member):
        if discord.utils.get(ctx.guild.roles, name='Muted'):
            if member.is_mod(member):
                await ctx.send('Oops. You can\'t mute that person.')
            else:
                if member.nick.startswith('[Muted]'):
                    role = discord.utils.get(member.guild.roles, name='Muted')
                    await member.remove_role(role)
                    await member.edit(nick=None)
                    await ctx.send(f'{member.mention} was unmuted.')
                else:
                    await ctx.send('That user is not muted.')
        else:
            await ctx.send('The bot hasn\'t been setup correctly. Use `.setup` to set up the bot.')
        await ctx.message.delete()

    @unmute.error
    async def unmute_error(self, ctx, error):

        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Please specify a user to unmute.')
            
        elif isinstance(error, commands.TooManyArguments):
            await ctx.send('Too many arguements! I just need to know who to unmute.')
        
def setup(client):
    client.add_cog(Mute(client))