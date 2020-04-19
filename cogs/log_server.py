from discord.ext import commands, tasks
import discord
import traceback
class Log_(commands.Cog, command_attrs=dict(hidden=True)):
    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):
        return ctx.author.id == 650249780072677378 or ctx.author.id == 386289367955537930

    @commands.command(aliases = ['cc'])
    async def copy_c(self, ctx, trype: str, channel: str):
        """ログ鯖にバックアップ用のチャンネルを作成
        
        引数にtypeを指定\n チャンネル名を指定

        trype: str
        channel: str
         別名: cc
        """
        log_guild = self.bot.get_guild(696702035399147521)

        if trype == 'category':
            await log_guild.create_category_channel(name = channel)

        elif trype == 'text':
            for category in log_guild.categories:
                if category.name == ctx.channel.category.name:
                    await category.create_text_channel(name = channel)


    @copy_c.error
    async def copy_c_error(self, ctx, error):
        await ctx.send(f'```py\n{traceback.format_exc()}\n```')

    @commands.Cog.listener()
    async def on_message(self, mes):
        log_guild = self.bot.get_guild(696702035399147521)
        if isinstance(mes.channel, discord.DMChannel):
            return
        if mes.guild.id != 695801973127118899:
            return

        log_guild_mes_channel = discord.utils.get(log_guild.text_channels, name = mes.channel.name)

        if log_guild_mes_channel is None:
            return

        e = discord.Embed(
            description = mes.content
        )

        e.set_author(name=mes.author.name, icon_url=mes.author.avatar_url)
 

        await log_guild_mes_channel.send(embed =e)


    @commands.Cog.listener()
    async def on_member_join(self, member):
        log_guild = self.bot.get_guild(696702035399147521)

        if member.guild.id != 695801973127118899:
            return

        join_info = self.bot.get_channel(696704172841500692)
        e = discord.Embed(
            description = 'メンバー入出通知'
        )

        e.set_author(name=member.name, icon_url=member.avatar_url)

        await join_info.send(embed =e)



    @commands.Cog.listener()
    async def on_member_remove(self, member):
        log_guild = self.bot.get_guild(696702035399147521)

        if member.guild.id != 695801973127118899:
            return

        join_info = self.bot.get_channel(696704201119498330)
        e = discord.Embed(
            description = 'メンバー退出通知'
        )

        e.set_author(name=member.name, icon_url=member.avatar_url)
        await join_info.send(embed =e)


def setup(bot):
    bot.add_cog(Log_(bot))