from discord.ext import commands
from discord import VoiceChannel, PermissionOverwrite, Embed, errors, utils, Role
from config import date
import asyncio
import traceback


class Auto_Create_Setting(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.create_voice = date.load('voice')
        self.create_text = date.load('text')
        self.new_text = date.load('new_channel')

    @commands.command(aliases = ['sv'])
    @commands.has_permissions(manage_channels = True)
    async def set_create_voice(self, ctx, voice: str , user_limit: int = 99):
        """特定のカテゴリー内に固定するボイスチャンネルを作成
        
        引数にボイスチャンネルの名前を指定することにより、固定のボイスチャンネルを作成\n ユーザーリミットを指定することにより、そのボイスチャンネルに入れる人数を制限する

        voice: 文字列
        user_limit: int (デフォルト値: 99)

        別名: sv
        """
        if not self.create_voice.get(str(ctx.guild.id)):
            self.create_voice[str(ctx.guild.id)] = {}

        self.create_voice[str(ctx.guild.id)]['ボイスチャンネルカウント'] = str(1)
        date.save(self.create_voice, 'voice')
        
        new_voice = await ctx.channel.category.create_voice_channel(name = f"{voice}", user_limit = user_limit)
        
        self.create_voice[str(ctx.guild.id)][str(new_voice.id)] = {}
        date.save(self.create_voice, 'voice')

        await ctx.send(f'{user_limit}人制限で{new_voice.name}を作成しました')

    @commands.command(aliases = ['rv'])
    @commands.has_permissions(manage_channels = True)
    async def remove_voice(self, ctx, voice: VoiceChannel = None):
        """指定されたボイスチャンネルを固定ボイスチャンネルから除外
        
     
        voice: 名前・ID

        別名: rv
        """
        if voice is None:
            return await ctx.send('voiceが指定されていません')
        
        if not self.create_voice.get(str(ctx.guild.id)):
            self.create_voice[str(ctx.guild.id)] = {}
            return

        for k in self.create_voice[str(ctx.guild.id)].keys():
            if k == str(voice.id):
                self.create_voice[str(ctx.guild.id)].pop(str(voice.id))
                date.save(self.create_voice, 'voice')
                await ctx.send(f'ボイスチャンネル一覧から{voice.name}を除外したよ！')


    @remove_voice.error
    async def remove_voice_error(self, ctx, error):
        await ctx.send(f'```py\n{traceback.format_exc()}\n```')


    @commands.command(aliases = ['rgv'])
    @commands.has_permissions(manage_channels = True)
    async def remove_guild_voice(self, ctx):
        """指定されたボイスチャンネルを固定ボイスチャンネルから除外

        別名: rgv
        """
 
        
        if not self.create_voice.get(str(ctx.guild.id)):
            self.create_voice[str(ctx.guild.id)] = {}
            return
        
        self.create_voice.pop(str(ctx.guild.id))
        date.save(self.create_voice, 'voice')
        await ctx.send(f'サーバーに関するすべての情報を除外したよ！')
    


    @commands.command(aliases = ['rc'])
    @commands.has_permissions(manage_channels=True)
    async def reset_count(self, ctx):
        """ボイスチャンネルのカウントをリセットします。

        別名: rc
        """
        self.create_voice[str(ctx.guild.id)]['ボイスチャンネルカウント']= str(1)
        date.save(self.create_voice, 'voice')


    @commands.command(aliases = ['sbr'])
    @commands.has_permissions(manage_roles=True)
    async def set_bot_role(self, ctx, role: Role):
        """チャンネルの管理権限を与える役職をセットします。

        引数に指定された役職を設定します。これはBOTに統一で付けられてる役職でなければなりません。

        別名: sbr
        
        """

        self.create_voice[str(ctx.guild.id)]['bot_role'] = str(role.id)
        date.save(self.create_voice, 'voice')
        await ctx.send(f'bot役職を{role.mention}に設定しました')


    @set_bot_role.error
    async def set_bot_role_error(self, ctx, error):
        await ctx.send(f'```py\n{traceback.format_exc()}\n```')


    @commands.command(aliases = ['st'])
    @commands.has_permissions(manage_channels = True)
    async def set_create_text(self, ctx, text: str = 'チャンネルの名前を変更してね'):
        """特定のカテゴリー内に固定するテキストチャンネルを作成
        
        引数にボイスチャンネルの名前を指定することにより、固定のテキストチャンネルを作成

        text: 文字列
         別名: st
        """
        new_text = await ctx.channel.category.create_text_channel(name = text)
        if not self.create_text.get(str(ctx.guild.id)):
            self.create_text[str(ctx.guild.id)] = {}

        self.create_text[str(ctx.guild.id)]['サーバー名'] = ctx.guild.name
        self.create_text[str(ctx.guild.id)]['テキストチャンネルID'] = []
        self.create_text[str(ctx.guild.id)]['テキストチャンネルID'].append(str(new_text.id))
        date.save(self.create_text, 'text')
        await ctx.send(f'自動作成チャンネル{new_text.mention}を作成しました')


    @commands.command(hidden = True)
    async def sdel(self, ctx, text: str):
        if text == 'text':
            self.create_text.pop(str(ctx.guild.id))
            date.save(self.create_text, 'text')

        elif text == 'new':
            self.new_text.pop(str(ctx.guild.id))
            date.save(self.new_text, 'new_channel')

        else:
            return await ctx.send('不正な値が渡されました')

        await ctx.send(f'{text}を全削除しました')



    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        
        if before.channel is None:

            if not self.create_voice.get(str(member.guild.id)):
                return

            elif not self.create_voice[str(member.guild.id)].get('bot_role'):
                return

            if len(after.channel.members) == 1:

                if str(after.channel.id) in self.create_voice[str(member.guild.id)].keys():
                    
                    new_voice = await after.channel.clone()
                    await new_voice.edit(name = f"{after.channel.name}-{self.create_voice[str(member.guild.id)]['ボイスチャンネルカウント']}")
                    await member.move_to(new_voice)
                    self.create_voice[str(member.guild.id)][str(new_voice.id)] = {}
                    self.create_voice[str(member.guild.id)]['ボイスチャンネルカウント'] = str(int(self.create_voice[str(member.guild.id)]['ボイスチャンネルカウント']) + 1)
                    date.save(self.create_voice, 'voice')

            elif len(after.channel.members) >= 2:
                if str(after.channel.id) in self.create_voice[str(member.guild.id)].keys():
                    new_text = self.bot.get_channel(int(self.create_voice[str(member.guild.id)][str(after.channel.id)]['new_channel']))
                    return await new_text.set_permissions(member, read_messages=True)
                    
                    

        if (before.channel  is not None) and (after.channel is not None):
            new_text = await after.channel.category.create_text_channel(name = f"{after.channel.name}")
            for member_ in member.guild.members:
                try:
                    if member_ == member:
                        await new_text.set_permissions(member, manage_channels=True)
                        continue
                    
                    elif member_.id == 693839038200938547:
                        role = member.guild.get_role(int(self.create_voice[str(member.guild.id)]['bot_role']))
                        await new_text.set_permissions(role, manage_channels=True)
                        continue


                    await new_text.set_permissions(member_, read_messages=False)
                except errors.Forbidden:
                    pass

        
            e = Embed(
                title = f'OWNER: {member}'
            )
            e.add_field(
                name = 'チャンネルの管理権限',
                value = 'オン'
            )
            await new_text.send(embed = e)
            self.create_voice[str(member.guild.id)][str(after.channel.id)]['new_channel'] = str(new_text.id)
            self.create_voice[str(member.guild.id)][str(before.channel.id)]['creater'] = str(member.id)
            date.save(self.create_voice, 'voice')

  

        if after.channel is None:
            if self.create_voice[str(member.guild.id)].get(str(before.channel.id)):

                new_text = self.bot.get_channel(int(self.create_voice[str(member.guild.id)][str(before.channel.id)]['new_channel']))
                
                if str(before.channel.id) not in self.create_voice[str(member.guild.id)].keys():
                    return


                elif len(before.channel.members) == 0:
                    await new_text.delete()
                    await before.channel.delete()
                    self.create_voice[str(member.guild.id)].pop(str(before.channel.id))
                    date.save(self.create_voice, 'voice')

                else:
                    await new_text.set_permissions(member, read_messages=False)

                if len(before.channel.category.voice_channels) == 1:

                    self.create_voice[str(member.guild.id)]['ボイスチャンネルカウント']= str(1)
                    date.save(self.create_voice, 'voice')
                
            
        

    @commands.Cog.listener()
    async def on_message(self, mes):
        if mes.author.bot:
            return

        if mes.content.startswith('e!'):
            return

        if mes.embeds:
            return

        if not self.create_text.get(str(mes.guild.id)):
            return

        if not self.create_text[str(mes.guild.id)].get('テキストチャンネルID'):
            return

        test_channel = self.bot.get_channel(699274063142715484)
       
        if str(mes.channel.id) in self.create_text[str(mes.guild.id)]['テキストチャンネルID']:

            if len(mes.content) >= 30:
                return await mes.channel.send('メッセージが30文字を超えてるため、エラーが発生しました。30文字以内に抑えて新規作成してください。')
            
            await mes.delete()

            overwrites = {
                mes.author: PermissionOverwrite(manage_channels=True)
            }

            new_channel = await mes.channel.category.create_text_channel(name = mes.content, overwrites=overwrites)
            get_new_channel = utils.get(mes.channel.category.text_channels, name = mes.content)

            e = Embed(
                description = f'新規チャンネル{get_new_channel.mention}を作成しました'
            )
            e.add_field(
                name = '対象ユーザー',
                value = mes.author.mention
            )
            await mes.channel.send(embed = e)
            

            if not self.new_text.get(str(mes.guild.id)):
                self.new_text[str(mes.guild.id)] = {}

            if not self.new_text[str(mes.guild.id)].get(str(mes.author.id)):
                self.new_text[str(mes.guild.id)][str(mes.author.id)] = {}

            if not self.new_text[str(mes.guild.id)][str(mes.author.id)].get('new_channel'):
                self.new_text[str(mes.guild.id)][str(mes.author.id)]['new_channel'] = []

            if str(new_channel.id) not in self.new_text[str(mes.guild.id)][str(mes.author.id)]['new_channel']:
                self.new_text[str(mes.guild.id)][str(mes.author.id)]['new_channel'].append(str(new_channel.id))


            date.save(self.new_text, 'new_channel')

            
            e = Embed(
                description = f'{mes.author.mention}\n{mes.content}'
            )
            
            await new_channel.send(embed=e)

        if str(mes.channel.id) in self.new_text[str(mes.guild.id)][str(mes.author.id)]['new_channel']:
            await mes.add_reaction('\U0001f5d1')

    
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if self.new_text.get(str(payload.member.guild.id)) is None:
            return

        if self.new_text[str(payload.member.guild.id)][str(payload.member.id)].get('new_channel') is None:
            return

        if payload.member.bot:
            return


        channel = self.bot.get_channel(payload.channel_id)
        if str(payload.channel_id) in self.new_text[str(payload.member.guild.id)][str(payload.member.id)]['new_channel']:

            for k in self.new_text[str(payload.member.guild.id)].keys():
                if k != str(payload.member.id):
                    return

                elif str(payload.emoji) == '\U0001f5d1':
                    await channel.delete()
                    self.new_text[str(mes.guild.id)][str(mes.author.id)]['new_channel'].remove(str(channel.id))
                    date.save(self.new_text, 'new_channel')


def setup(bot):
    bot.add_cog(Auto_Create_Setting(bot))