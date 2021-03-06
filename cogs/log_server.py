from discord.ext import commands, tasks
from cogs.utils import keys
import importlib
import discord
import traceback
 
GUILDID, CHANNELID, ACCOUNTID= keys.guild_id(), keys.channel_id(), keys.account_id()


class Log_(commands.Cog, command_attrs=dict(hidden=True)):
    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):
        return ctx.author.id == ACCOUNTID.fulute or ctx.author.id == ACCOUNTID.furimu

    @commands.Cog.listener()
    async def on_message(self, mes):
        
        if mes.channel.id != CHANNELID.entrance:
            return 

        e = discord.Embed(
            description = mes.content
        )

        e.set_author(name=mes.author.name, icon_url=mes.author.avatar_url)

        await self.bot.get_channel(CHANNELID.entrancelog).send(embed=e)


    @commands.Cog.listener()
    async def on_member_join(self, member):

        if member.guild.id != GUILDID:
            return

        join_info = self.bot.get_channel(CHANNELID.joinlog)
        e = discord.Embed(
            description = 'メンバー入出通知'
        )

        e.set_author(name=member.name, icon_url=member.avatar_url)

        await join_info.send(embed =e)



    @commands.Cog.listener()
    async def on_member_remove(self, member):

        if member.guild.id != GUILDID:
            return


        channel = self.bot.get_channel(CHANNELID.entrance)

        async for message in channel.history(limit=None):
            if message.author.mention in message.content:
                await message.delete()

       

        remove_info = self.bot.get_channel(CHANNELID.removelog)
        e = discord.Embed(
            description = 'メンバー退出通知'
        )

        e.set_author(name=member.name, icon_url=member.avatar_url)
        await remove_info.send(embed =e)


    @commands.command()
    async def log_key(self, ctx):
        importlib.reload(keys) 
        await ctx.message.delete()

def setup(bot):
    bot.add_cog(Log_(bot))