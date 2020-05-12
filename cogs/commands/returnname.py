from discord.ext import commands
from config import date
import asyncio
import traceback
import discord


class Return_Name(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(aliases = ['rn'])
    async def role_(self, ctx, role: discord.Role):
        e = discord.Embed()
        e.add_field(
            name = 'name',
            value = role.name,
            inline = False
        )
        e.add_field(
            name = 'id',
            value = role.id
        )
        await ctx.send(embed =e)


    @commands.command(aliases = ['mn'])
    async def member_(self, ctx, member: discord.Member):
        e = discord.Embed()
        e.add_field(
            name = 'name',
            value = member.name,
            inline = False
        )
        e.add_field(
            name = 'id',
            value = member.id
        )
        await ctx.send(embed =e)


    @commands.command(aliases = ['tn'])
    async def text_channel_(self, ctx, channel: discord.TextChannel):
        e = discord.Embed()
        e.add_field(
            name = 'name',
            value = channel.name,
            inline = False
        )
        e.add_field(
            name = 'id',
            value = channel.id
        )
        await ctx.send(embed =e)

    @commands.command(aliases = ['vn'])
    async def voice_channel_(self, ctx, channel: discord.VoiceChannel):
        e = discord.Embed()
        e.add_field(
            name = 'name',
            value = channel.name,
            inline = False
        )
        e.add_field(
            name = 'id',
            value = channel.id
        )
        await ctx.send(embed =e)

def setup(bot):
    bot.add_cog(Return_Name(bot))