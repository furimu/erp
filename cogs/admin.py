from discord.ext import commands
from cogs.utils import check
import discord
import traceback
import os
import subprocess
import importlib

class Admin(commands.Cog, command_attrs=dict(hidden=True)):
    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):
        return ctx.author.id == 650249780072677378 or ctx.author.id == 386289367955537930


    @commands.command()
    async def load(self, ctx, module: str, opt = None):
        module = f'cogs.{module}'
        if opt is None:
            self.bot.load_extension(module)

        elif opt == 'un':
            self.bot.unload_extension(module)

        elif opt == 're':
            self.bot.reload_extension(module)

        else:
            return await ctx.message.add_reaction('\N{BLACK QUESTION MARK ORNAMENT}')
        
        await ctx.message.add_reaction('\N{WHITE HEAVY CHECK MARK}')

    @load.error
    async def load_error(self, ctx, error):
        await ctx.send(f'```py\n{traceback.format_exc()}\n```')


    @commands.command()
    async def cc(self, ctx, category: discord.CategoryChannel, name: str):
        await category.create_text_channel(name=name)
        await ctx.send("ok")
    @commands.command()
    async def ctx_repeat(self, ctx):
        if await check.original_command_permissions(ctx) == False:
            return
            
        await ctx.send(ctx.command)

    @commands.command()
    async def mr(self, ctx):
        importlib.reload(check)
        

        
    @commands.command()
    async def restart(self, ctx):
        os.system('cals')
        subprocess.run("launc.py", shell=True)

    
    @commands.command(aliases = ['sn'])
    async def send_notice(self, ctx, channel: discord.TextChannel, *, contents: str):
        
        e = discord.Embed(
            description = contents
        )
        await channel.send('@everyone\n', embed = e)

    @send_notice.error
    async def sn_error(self, ctx, error):
 
        await ctx.send(f'```py\n{traceback.format_exc()}\n```')

    @commands.command(aliases = ['ne'])
    async def nomal_embed(self, ctx, channel: discord.TextChannel, *, contents: str):
        
        e = discord.Embed(
            description = contents
        )
        await channel.send(embed = e)

    @commands.command(aliases = ['nm'])
    async def nomal_mes(self, ctx, channel: discord.TextChannel, *, contents: str):
        
        await channel.send(contents)

    @commands.command(aliases = ['onemes'])
    async def one_message(self, ctx, member: discord.Member, channel: discord.TextChannel, *, contents: str):
        
        e = discord.Embed(
            description = contents
        )
        await channel.send(f"{member.mention}\n", embed = e)


def setup(bot):
    bot.add_cog(Admin(bot))