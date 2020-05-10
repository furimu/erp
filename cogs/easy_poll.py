from discord.ext import commands
from utils import date
import discord

class Easy_Poll(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        self.load = date.load("poll_channel")
    @commands.command(aliases=['yn'])
    async def yneasy_poll(self, ctx, *, question=None):
        if question is None:
            return await ctx.send("質問が渡されていません")

        e = discord.Embed(
            title= question,
            description= "**1**:はい, **2**:いいえ")

        if self.load[str(ctx.guild.id)].get("yn") is None:
            channel= ctx.channel

        else:
            channel= self.bot.get_channel(int(self.load[str(ctx.guild.id)]["yn"])

        await channel.send(embed=e)

        

    @commands.command(aliases=['pc'])
    async def poll_channel(self, ctx, channel: discord.TextChannel, opt= None):
        if opt is None:
            opt= "global"

        if opt not in ["global", "yn", "custom"]:
            return

        if self.load[str(ctx.guild.id)].get(opt) is None:
            self.load[str(ctx.guild.id)][opt]= None

        self.load[str(ctx.guild.id)][opt]=str(channel.id)

        date.save(self.load, "poll_channel")

        await ctx.send(f"{channel.mention}をアンケートチャンネルに設定しました")

def setup(bot):
    bot.add_cog(Easy_Poll(bot))