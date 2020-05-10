from discord.ext import commands

import discord

class Easy_Poll(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

   @commands.command(aliases=['yn'])
    async def yneasy_poll(self, ctx, *, question=None):
        if question is None:
            return await ctx.send("質問が渡されていません")

        e = discord.Embed(
            title= question,
            description= "**1**:はい, **2**:いいえ")

        

    @commands.command(aliases=['pc'])
    async def poll_channel(self, ctx, channel: discord.TextChannel=None):
        if channel is None:
            channel = ctx.channel

        
