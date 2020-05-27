from discord.ext import commands
from config import date
from datetime import datetime
import discord
import typing
class Spam(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.spamer = date.load('spamer')
        self.black_user = date.load('black_user')
        self.not_mention = date.load('not_mention')

    @commands.Cog.listener()
    async def on_message(self, mes):
        admin = self.bot.get_channel(696591762042650644)
        guild_id = str(mes.guild.id)

        if mes.author.id == 693839038200938547:
            return

        if mes.mention_everyone:
   
            channel = self.bot.get_channel(696409125403230238)
  
            if not self.spamer.get(str(mes.guild.id)):
                self.spamer[str(mes.guild.id)] = {}
   

            if not self.spamer[str(mes.guild.id)].get(str(mes.author.id)):
                self.spamer[str(mes.guild.id)][str(mes.author.id)] = {}


            if not self.spamer[str(mes.guild.id)][str(mes.author.id)].get('開始時刻'):
                self.spamer[str(mes.guild.id)][str(mes.author.id)]['開始時刻'] = str(datetime.now().second)

            self.spamer[str(mes.guild.id)][str(mes.author.id)]['終了時刻'] = str(datetime.now().second)

            if self.spamer[str(mes.guild.id)][str(mes.author.id)].get('回数'):
                self.spamer[str(mes.guild.id)][str(mes.author.id)]['回数'] = str(int(self.spamer[str(mes.guild.id)][str(mes.author.id)]['回数']) + 1)

            elif not self.spamer[str(mes.guild.id)][str(mes.author.id)].get('回数'):
                self.spamer[str(mes.guild.id)][str(mes.author.id)]['回数'] = str(1)

            

            date.save(self.spamer, 'spamer')

            e = discord.Embed(
                title = 'メンションスパム'
            )
            e.add_field(
                name = '名前',
                value = str(mes.author),
                inline=False
            )
            e.add_field(
                name = 'ID',
                value = mes.author.id,
                inline=False
            )
     


            if int(self.spamer[str(mes.guild.id)][str(mes.author.id)]['回数']) >= 5:
                if int(self.spamer[str(mes.guild.id)][str(mes.author.id)]['終了時刻']) - int(self.spamer[str(mes.guild.id)][str(mes.author.id)]['開始時刻']) <- 10:
                    await mes.author.ban(delete_message_days=7, reason='メンションスパム')
                    if mes.guild.id == 695801973127118899:
                        await channel.send(embed =e)
                    

                elif (self.spamer[str(mes.guild.id)][str(mes.author.id)]['開始時刻'] == 59) and (self.spamer[str(mes.guild.id)][str(mes.author.id)]['終了時刻'] == 4):
                    await mes.author.ban(delete_message_days=7, reason='メンションスパム')
                    if mes.guild.id == 695801973127118899:
                        await channel.send(embed =e)

                elif (self.spamer[str(mes.guild.id)][str(mes.author.id)]['開始時刻'] == 58) and (self.spamer[str(mes.guild.id)][str(mes.author.id)]['終了時刻'] == 3):
                    await mes.author.ban(delete_message_days=7, reason='メンションスパム')
                    if mes.guild.id == 695801973127118899:
                        await channel.send(embed =e)

                elif (self.spamer[str(mes.guild.id)][str(mes.author.id)]['開始時刻'] == 57) and (self.spamer[str(mes.guild.id)][str(mes.author.id)]['終了時刻'] == 2):
                    await mes.author.ban(delete_message_days=7, reason='メンションスパム')
                    if mes.guild.id == 695801973127118899:
                        await channel.send(embed =e)

                elif (self.spamer[str(mes.guild.id)][str(mes.author.id)]['開始時刻'] == 56) and (self.spamer[str(mes.guild.id)][str(mes.author.id)]['終了時刻'] == 2):
                    await mes.author.ban(delete_message_days=7, reason='メンションスパム')
                    if mes.guild.id == 695801973127118899:
                        await channel.send(embed =e)

                elif (self.spamer[str(mes.guild.id)][str(mes.author.id)]['開始時刻'] == 55) and (self.spamer[str(mes.guild.id)][str(mes.author.id)]['終了時刻'] == 00):
                    await mes.author.ban(delete_message_days=7, reason='メンションスパム')
                    if mes.guild.id == 695801973127118899:
                        await channel.send(embed =e)


        elif mes.mentions:
            if str(mes.channel.id) in self.not_mention[guild_id]['channel_id']:
                if not self.not_mention[guild_id].get('custom_message'):
                    await admin.send(f'{mes.author.mention}さん此処のチャンネルではメンション禁止だよ。')

                elif self.not_mention[guild_id].get('custom_message'):
                    await mes.channel.send(self.not_mention[guild_id]['custom_message'])

                


    @commands.command(aliases = ['anm'])
    @commands.has_permissions(manage_roles = True)
    async def add_not_mention(self, ctx, channel: discord.TextChannel):
        guild_id = str(ctx.guild.id)
        if not self.not_mention.get(guild_id):
            self.not_mention[guild_id] = {}

        if not self.not_mention[guild_id].get('channel_id'):
            self.not_mention[guild_id]['channel_id'] = []

        self.not_mention[guild_id]['channel_id'].append(str(channel.id))
        date.save(self.not_mention, 'not_mention')

        await ctx.send(f'{channel.mention}を指定しました')


    @commands.command(aliases = ['anmcm'])
    @commands.has_permissions(manage_roles = True)
    async def add_not_mention_custom_message(self, ctx, *, custom_message: str):
        guild_id = str(ctx.guild.id)
        if not self.not_mention.get(guild_id):
            self.not_mention[guild_id] = {}

        self.not_mention[guild_id]['custom_message'] = custom_message
        date.save(self.not_mention, 'not_mention')
        await ctx.send('カスタムメッセージを指定しました')


    @commands.command(aliases = ['rnm'])
    @commands.has_permissions(manage_roles = True)
    async def remove_not_mention(self, ctx, channel: discord.TextChannel):
        guild_id = str(ctx.guild.id)
        if not self.not_mention.get(guild_id):
            self.not_mention[guild_id] = {}

        if not self.not_mention[guild_id].get('channel_id'):
            self.not_mention[guild_id]['channel_id'] = []

        self.not_mention[guild_id]['channel_id'].remove(str(channel.id))
        date.save(self.not_mention, 'not_mention')
        await ctx.send(f'{channel.mention}を除外しました')


    @commands.command(aliases = ['rnmcm'])
    @commands.has_permissions(manage_roles = True)
    async def remove_not_mention_custom_message(self, ctx, *, custom_message: str):
        guild_id = str(ctx.guild.id)
        if not self.not_mention.get(guild_id):
            self.not_mention[guild_id] = {}

        self.not_mention[guild_id].pop('custom_message')
        date.save(self.not_mention, 'not_mention')
        await ctx.send('カスタムメッセージを除外しました')

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, members: commands.Greedy[discord.Member], delete_days: typing.Optional[int] = 0, *, reason: str = None):
        """userをbanする
        引数にメンバーを指定する。
        次の引数に過去何日間のメッセージを削除するか。
        最後に理由
        
        """

        channel = self.bot.get_channel(696409125403230238)

        for member in members:
            await member.ban(delete_message_days=delete_days, reason=reason)

            e = discord.Embed(
                title = reason
            )
            e.add_field(
                name = '名前',
                value = str(member),
                inline=False
            )
            e.add_field(
                name = 'ID',
                value = member.id,
                inline=False
            )
 
            await channel.send(embed = e)



    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, members: commands.Greedy[discord.Member], *, reason: str = None):
        """userをkickする
        引数にメンバーを指定する。
        最後に理由
        
        """
        channel = self.bot.get_channel(696415419157970986)

        

        for member in members:
            await member.kick(reason=reason)

            e = discord.Embed(
                title = reason
            )
            e.add_field(
                name = '名前',
                value = str(member),
                inline=False
            )
            e.add_field(
                name = 'ID',
                value = member.id,
                inline=False
            )
     
            await channel.send(embed = e)

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def akick(self, ctx, *, reason: str = None):
        """userをkickする
        引数にメンバーを指定する。
        最後に理由
        
        """
        channel = self.bot.get_channel(696415419157970986)

        

        for member in ctx.guild.members:
            if member.guild_permissions.administrator:
                continue
            try:
                await member.send(reason)
            except:
                print(f"{str(member)}にメッセージを送信できませんでした")

            await member.kick(reason=reason)

           
    

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def softban(self, ctx, members: commands.Greedy[discord.Member], delete_days: typing.Optional[int] = 0, *, reason: str = None):
        """userをbanしてunbanする
        引数にメンバーを指定する。
        次の引数に過去何日間のメッセージを削除するか。
        最後に理由
        
        """

        for member in members:
            await member.ban(delete_message_days=delete_days, reason=reason)
            await member.unban()

        await ctx.message.add_reaction('\U0001f44c')

    
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, members: commands.Greedy[discord.Member], *, reason: str = None):
        """userをunbanする
        引数にメンバーを指定する。
        最後に理由
        
        """
        channel = self.bot.get_channel(696415396991074327)

        for member in members:
            await member.unban(reason=reason)

            e = discord.Embed(
                title = reason
            )
            e.add_field(
                name = '名前',
                value = str(member),
                inline=False
            )
            e.add_field(
                name = 'ID',
                value = member.id,
                inline=False
            )
           
            await channel.send(embed = e)

    
    @commands.command(hidden =True)
    async def spu(self, ctx, server: str, member: str, reason: str = None):
        """現在改良中
        """
        if not isinstance(ctx.channel, discord.DMChannel):
            return
            
        if reason is None:
            return await ctx.send('理由が指定されていません')


        if not self.black_user.get(server):
            self.black_user[server] = {}

        if not self.black_user[server].get(member):

            self.black_user[server][member]['回数'] = str(1)
            date.save(self.black_user, 'black_user')
        
        else:
            self.black_user[server][member]['回数'] = int(self.black_user[server][member]['回数']) + 1

        self.black_user[server]['理由'] = []
        self.black_user[server]['理由'].append(reason)
        date.save(self.black_user, 'black_user')

        await ctx.send('ブラックリストに登録しました。')

    

def setup(bot):
    bot.add_cog(Spam(bot))