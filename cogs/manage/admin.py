from discord.ext import commands
from cogs.utils import check
from config import date
import discord
import traceback
import os
import subprocess
import importlib

black_list= date.load("black_list") 

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
        msg=traceback.format_exc()
        for i in range(0, len(msg), 1092):
            await ctx.channel.send(f'```py\n{msg[i:i+1092]}\n```')


    @commands.command()
    async def mr(self, ctx):
        importlib.reload(check)
        
    @commands.command()
    async def gs(self, ctx):
        e=discord.Embed(
            title="サーバー一覧")
        for s in self.bot.guilds:
            e.add_field(
                name=s.name,
                value=s.id,
                inline=False)
        await ctx.send(embed=e)


    @commands.command()
    async def add_black_server(self, ctx, guild:discord.Guild, opt: None):
        if opt is None:
            opt= "red"
        
        black_list[str(guild.id)]= opt

        date.save(black_list, "black_list")

        for server in self.bot.guilds:
            if server.id == guild.id:
                await guild.leave()

        await ctx.send(f"{guild.name}をブラックリストに登録しました")


        
    @commands.command()
    async def restart(self, ctx):
        os.system('cals')
        subprocess.run("launc.py", shell=True)

    @commands.command(aliases=["sn"])
    async def  send_embed(self, ctx, channel = discord.TextChannel, opt, *, mes):
        if opt == 'y':
            await ctx.send('@everyone', embed=self.bot.default_embed(mes))

        elif opt == 'n':
            await ctx.send(embed=self.bot.default_embed(mes))


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