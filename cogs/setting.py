from discord.ext import commands
from discord import TextChannel
from config import date
from cogs.utils import keys

ID = keys.get_id()
class Setting(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.prefix = date.load('prefix')
        self.notice = date.load('notice')
    
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def add_prefix(self, ctx, new_prefix: str = None):
        """現状使用不要"""
        guild_id = str(ctx.guild.id)
        if prefix is None:
            return await ctx.send('新しいカスタムプレフィックスが指定されていません。')

        elif new_prefix in self.prefix[guild_id]['prefix']:
            return await ctx.send('そのカスタムプレフィックスは既に登録されています。')

        self.prefix[guild_id]['prefix'].append(new_prefix)
        date.save(self.prefix, 'prefix')
        
        await ctx.send(f'{new_prefix}を新しいカスタムプレフィックスに登録しました！')

    
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def remove_prefix(self, ctx, new_prefix: str = None):
        """現状使用不要"""
        guild_id = str(ctx.guild.id)
        if prefix is None:
            return await ctx.send('カスタムプレフィックスが指定されていません。')

        elif new_prefix not in self.prefix[guild_id]['prefix']:
            return await ctx.send('そのカスタムプレフィックスは登録されていません。')

        self.prefix[guild_id]['prefix'].remove(new_prefix)
        date.save(self.prefix, 'prefix')
        
        await ctx.send(f'{new_prefix}を新しいカスタムプレフィックスから解除しました！')



    @commands.command(aliases = ['anc'])
    @commands.has_permissions(administrator=True)
    async def add_news_channel(self, ctx, channel: TextChannel = None):
        """botのお知らせチャンネルを追加する
        
        引数にchannelを指定してBOTの通知が行くチャンネルを登録する


        別名: anc
        """
        guild_id = str(ctx.guild.id)
        if channel is None:
            return await ctx.send('チャンネルが指定されてないよ！')
        
        if self.notice.get(guild_id, None) is None:
            self.notice[guild_id] = {}

        self.notice[guild_id]['サーバーの名前'] = ctx.guild.name
        self.notice[guild_id]['channel_id'] = str(channel.id)
        self.save_date('notice', self.notice)
        
        await ctx.send('設定が完了したよ！')

        target = self.bot.get_channel(ID.update_news_channel)
        e = self.bot.default_embed(f'{ctx.guild.name}- {ctx.guild.id}でお知らせチャンネルを追加しました')
        await target.send(embed = e)

    

    @commands.command(aliases = ['rnc'])
    @commands.has_permissions(administrator=True)
    async def remove_news_channel(self, ctx):
        """botのお知らせチャンネルを削除
        
        引数にchannelを指定してBOTの通知が行くチャンネルを削除する


        別名: rnc
        """
        guild_id = str(ctx.guild.id)
        if self.notice.get(guild_id, None) is None:
            self.notice[guild_id] = {}
            return await ctx.send('チャンネルが登録されていないよ！')

        self.notice.pop(guild_id)
        self.save_date('notice', self.notice)

        await ctx.send('お知らせ送信チャンネルの登録を削除したよ！\nBOTのお知らせは再度登録しない限り来ないよ！')
        
        target = self.bot.get_channel(ID.update_news_channel)
        e = self.bot.default_embed(f'{ctx.guild.name}- {ctx.guild.id}でお知らせチャンネルを削除しました')
        await target.send(embed = e)



def setup(bot):
    bot.add_cog(Setting(bot))