from discord.ext import commands
from discord import Embed, Game, Activity, ActivityType, utils, TextChannel, VoiceChannel, CategoryChannel, Member, Role, Permissions
from config import date
import json
import asyncio
import traceback
import botinfo


class Moveer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.admin_channel = date.load('admin_channel')


    @commands.command()
    @commands.has_permissions(manage_channels = True)
    async def changema(self, ctx, channel: TextChannel = None):
        """引数指定されたTCでコマンドの送信が可能にする

        channel: 名前・ID・メンション
        """
        if channel is None:
            return await ctx.send('チャンネルが指定されていません')
        if ctx.channel.name != 'moveeradmin':
            return await ctx.send(f'これは管理コマンドです。"moveeradmin"というテキストチャンネルで最初に実行してください。{ctx.author.mention}')

        if not self.admin_channel.get(str(ctx.guild.id)):
            self.admin_channel[str(ctx.guild.id)] = {}
        
        self.admin_channel[str(ctx.guild.id)]['サーバーの名前'] = ctx.guild.name
        self.admin_channel[str(ctx.guild.id)]['テキストチャンネルの名前'] = channel.name
        self.admin_channel[str(ctx.guild.id)]['テキストチャンネルのID'] = str(channel.id)

        date.save(self.admin_channel, 'admin_channel')
        await ctx.send(f'{channel.name}で管理コマンドを送信できるようにしました')


    @commands.command()
    async def move(self, ctx, users: commands.Greedy[Member] = None):
        """指定されたユーザーをMoveerVCに移動する
        引数に指定されたメンバーをMoveerというボイスチャンネルに移動します

        users: 名前・ID・メンション
        """
        if users is None:
            return await ctx.send('メンバーが指定されていません')

        vc = utils.get(guild.voice_channels, name='Moveer') 
        if vc is None:
            return await ctx.send('**Moveer**というボイスチャンネルが見つかりませんでした')

        elif ctx.channel.name != 'moveeradmin' or ctx.channel.id != self.admin_channel[str(ctx.guild.id)]['テキストチャンネルのID']:
            return await ctx.send(f'これは管理コマンドです。"moveeradmin"というテキストチャンネルで最初に実行するか、！changema＃<変更先のチャンネル名> で設定してください。(最初はmoveeradminチャンネルで実行する必要があります){ctx.author.mention}')



        for member in users:
            if member.voice.channel is None:
                return await ctx.send(f'{member.name}はVCにいない為処理が停止しました')

            await member.move_to(vc)

        await ctx.send(f'{ctx.author.name}のリクエストにより{len(users)}人のユーザーを移動させました')
        


    @commands.command()
    async def cmove(self, ctx, channel: VoiceChannel, users: commands.Greedy[Member] = None):
        """指定されたユーザーを指定されたVCに移動する
        引数に指定されたメンバーを移動します。

        users: 名前・ID・メンション
        """
        if users is None:
            return await ctx.send('メンバーが指定されていません')

        if ctx.channel.name != 'moveeradmin' or ctx.channel.id != self.admin_channel[str(ctx.guild.id)]['テキストチャンネルのID']:
            return await ctx.send(f'これは管理コマンドです。"moveeradmin"というテキストチャンネルで最初に実行するか、！changema＃<変更先のチャンネル名> で設定してください。(最初はmoveeradminチャンネルで実行する必要があります){ctx.author.mention}')

        elif ctx.channel.name != 'moveeradmin' or ctx.channel.id != self.admin_channel[str(ctx.guild.id)]['テキストチャンネルのID']:
            return await ctx.send(f'これは管理コマンドです。"moveeradmin"というテキストチャンネルで最初に実行するか、！changema＃<変更先のチャンネル名> で設定してください。(最初はmoveeradminチャンネルで実行する必要があります){ctx.author.mention}')

        for user in users:
            await user.move_to(channel)
        
        await ctx.send(f'{ctx.author.name}のリクエストにより{len(users)}人のユーザーを移動させました')


    @commands.command()
    async def fmove(self, ctx, channel: VoiceChannel, after_channel: VoiceChannel = None):
        """指定されたVCから他のVCに移動する
        引数に指定されたボイスチャンネルに居るメンバー全員を次の引数に指定されたボイスチャンネルに移動します。

        channel: 名前・ID
        after_channel: 名前・ID
        """
        if after_channel is None:
            return await ctx.send('チャンネルが指定されていません')

        elif ctx.channel.name != 'moveeradmin' or ctx.channel.id != self.admin_channel[str(ctx.guild.id)]['テキストチャンネルのID']:
            return await ctx.send(f'これは管理コマンドです。"moveeradmin"というテキストチャンネルで最初に実行するか、！changema＃<変更先のチャンネル名> で設定してください。(最初はmoveeradminチャンネルで実行する必要があります){ctx.author.mention}')

        for member in channel.members:
            await member.move_to(after_channel)

        await ctx.send(f'{ctx.author.name}のリクエストにより{len(users)}人のユーザーを移動させました')


    @commands.command()
    async def rmove(self, ctx, role: Role):
        """指定された役職がついてる人を特定のVCに移動する
        引数に指定された役職がついてる人をコマンド送信者が居るボイスチャンネルに移動させます。

        role: 名前・ID・メンション
        """
        if ctx.author.voice.channel is None:
            return await ctx.send('貴方がボイスチャンネルに接続していない為このコマンドを実行できません')

        elif ctx.channel.name != 'moveeradmin' or ctx.channel.id != self.admin_channel[str(ctx.guild.id)]['テキストチャンネルのID']:
            return await ctx.send(f'これは管理コマンドです。"moveeradmin"というテキストチャンネルで最初に実行するか、！changema＃<変更先のチャンネル名> で設定してください。(最初はmoveeradminチャンネルで実行する必要があります){ctx.author.mention}')

        for member in ctx.guild.members:
            if role in member.roles:
                if member.voice.channel is None:
                    continue
                await member.move_to(ctx.author.voice.channel)


    @commands.command()
    async def tmove(self, ctx, channel: VoiceChannel, role: Role):
        """指定された役職がついてる人を特定のVCに移動する
        引数に指定された役職がついてる人を指定されたボイスチャンネルに移動させます。

        channel: 名前・ID
        role: 名前・ID・メンション
        """
        if ctx.channel.name != 'moveeradmin' or ctx.channel.id != self.admin_channel[str(ctx.guild.id)]['テキストチャンネルのID']:
            return await ctx.send(f'これは管理コマンドです。"moveeradmin"というテキストチャンネルで最初に実行するか、！changema＃<変更先のチャンネル名> で設定してください。(最初はmoveeradminチャンネルで実行する必要があります){ctx.author.mention}')


        for member in ctx.guild.members:
            if role in member.roles:
                if member.voice.channel is None:
                    continue
                await member.move_to(channel)



    @commands.command()
    async def faq(self, ctx):
        """
        Moveer機能に対するよくある質問
        """
        e = Embed(
            title = 'FAQ'
        )

        e.add_field(
            name = 'どうして実装されてないコマンドがあるのか。',
            value = 'helpを翻訳したところゲーム関係の機能だったので不要だと判断し、除去しました',
            inline= False
        )

        await ctx.send(embed = e)


    

def setup(bot):
    bot.add_cog(Moveer(bot))