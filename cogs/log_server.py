from discord.ext import commands, tasks
import discord
import traceback
class Log_(commands.Cog, command_attrs=dict(hidden=True)):
    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):
        return ctx.author.id == 650249780072677378 or ctx.author.id == 386289367955537930

    @commands.Cog.listener()
    async def on_message(self, mes):
        
        if mes.channel.id != 709831686627655742:
            return 

        e = discord.Embed(
            description = mes.content
        )

        e.set_author(name=mes.author.name, icon_url=mes.author.avatar_url)

        await self.bot.get_channel(709831686627655742).send(embed=e)


    @commands.Cog.listener()
    async def on_member_join(self, member):

        if member.guild.id != 695801973127118899:
            return

        join_info = self.bot.get_channel(709833551935307817)
        e = discord.Embed(
            description = 'メンバー入出通知'
        )

        e.set_author(name=member.name, icon_url=member.avatar_url)

        await join_info.send(embed =e)



    @commands.Cog.listener()
    async def on_member_remove(self, member):

        channel = self.bot.get_channel(696059891256656003)

        async for message in channel.history(limit=None):
            if message.author.mention in message.content:
                await message.delete()

        if member.guild.id != 695801973127118899:
            return

        join_info = self.bot.get_channel(709834081495679077)
        e = discord.Embed(
            description = 'メンバー退出通知'
        )

        e.set_author(name=member.name, icon_url=member.avatar_url)
        await join_info.send(embed =e)


def setup(bot):
    bot.add_cog(Log_(bot))