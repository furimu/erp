from discord.ext import commands
from config import date
import discord
class Guild_Event(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.notice = date.load('notice')
    
    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        if guild.id != 695801973127118899:
            return

        e = self.bot.default_embed('当BOTのご利用ありがとうございます。')
        e.add_field(
            name = '当BOTの注意',
            value = 'チャンネルの作成権限を必須としています。一部機能でユーザーの情報を保存します(第三者が閲覧する事・開発者がバグ修正以外に見る事は絶対にありません)',
            inline = False
        )

        e.add_field(
            name = '以上の事に同意できますか？',
            value = '同意できる場合は〇 | 出来ない場合は✖のリアクションを教えてください。'
        )

        first_mes = await guild.owner.send(embed = e)

        await first_mes.add_reaction('\N{HEAVY LARGE CIRCLE}')
        await first_mes.add_reaction('\N{CROSS MARK}')


        def reaction_check(reaction, user):
            return user == guild.owner

        reaction, user = self.bot.wait_for('raw_reaction_add', check = check)

        if str(reaction.emoji) == '\N{HEAVY LARGE CIRCLE}':
            try:
                news_channel = await guild.create_text_channel('erp-news-channel')
            except discord.errors.Forbidden:
                await guild.owner.send('チャンネルを作成する権限が無かったため自動退出します。再度呼ぶ場合はもう一度リンクをクリックしてください。')
                await guild.leave()
            else:
                if self.notice.get(guild_id, None) is None:
                    self.notice[guild_id] = {}

                    self.notice[guild_id]['サーバーの名前'] = ctx.guild.name
                    self.notice[guild_id]['channel_id'] = str(news_channel.id)
                    self.save_date('notice', self.notice)
                    await news_channel.send('今後このチャンネルにBOTの最新の情報が通知されます。又、ここに送信されたメッセージは全てサポートサーバーに送信されます。ヘルプなどにご利用ください。')


        elif str(reaction.emoji) == '\N{CROSS MARK}':
            await guild.owner.send('自動退出します。')
            await guild.leave()


    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        target = self.bot.get_channel(695802376212316192)
        e = self.bot.default_embed('退出info')
        e.add_field(
            name = 'サーバー名 - サーバーID',
            value = f'{guild.name} - {guild.id}'
        )
        await target.send(embed = e)


def setup(bot):
    bot.add_cog(Guild_Event(bot))