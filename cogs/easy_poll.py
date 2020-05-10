from discord.ext import commands

import discord

class Easy_Poll(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command(aliases=['ep']
    async def easy_poll(self, ctx, *, question=None):
        if question is None:
            return await ctx.send("質問が渡されていません")