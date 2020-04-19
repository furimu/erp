from discord.ext import commands
from config import date
import discord
import traceback

class Member_Event(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.member_is_bot = date.load('member_is_bot')
        self.member_not_is_bot = date.load('member_not_is_bot')
        self.global_ban = date.load('global_ban')
        self.black_user = date.load('black_user')


    @commands.command(aliases = ['sb'])
    @commands.has_permissions(manage_roles = True)
    async def set_bot(self, ctx, role: discord.Role):
        """BOTが入ってきた時に付与する役職を指定
        
        引数にBOTに付与する役職を指定する。BOTが入ってきたらその役職を付与

        role: 名前・ID・メンション
         別名: sb
        """
        if not self.member_is_bot.get(str(ctx.guild.id)):
            self.member_is_bot[str(ctx.guild.id)] = {}

        self.member_is_bot[str(ctx.guild.id)]['bot_role_id'] = str(role.id)
        date.save(self.member_is_bot, 'member_is_bot')

    @commands.command(aliases = ['su'])
    @commands.has_permissions(manage_roles = True)
    async def set_user(self, ctx, role: discord.Role):
        """Userが入ってきた時に付与する役職を指定
        
        引数にUserに付与する役職を指定する。Userが入ってきたらその役職を付与

        role: 名前・ID・メンション
         別名: su
        """
        if not self.member_not_is_bot.get(str(ctx.guild.id)):
            self.member_not_is_bot[str(ctx.guild.id)] = {}

        self.member_not_is_bot[str(ctx.guild.id)]['member_role_id'] = str(role.id)
        date.save(self.member_not_is_bot, 'member_not_is_bot')


    @commands.Cog.listener()
    async def on_member_join(self, member):

        channel = self.bot.get_channel(696059891256656003)
        
        if self.global_ban.get('global_ban_users'):
            if not self.global_ban['global_ban_users'].get('name'):
                if self.global_ban['global_ban_users'].get('id'):
                    counter = 0
                    for user in int(self.global_ban['global_ban_users']['id']):
                        if user.id == member.id:
                            counter = counter +1
                        if counter == 5:
                            await member.ban()


            elif not self.global_ban['global_ban_users'].get('id'):
                if self.global_ban['global_ban_users'].get('name'):
                    for user in int(self.global_ban['global_ban_users']['name']):
                        if user == member:
                            counter = counter +1
                        if counter == 5:
                            await member.ban()

        elif self.black_user.get(member.guild.name):
            if int(self.black_user[member.guild.name][member]['回数']) >= 5:
                await member.ban(delete_message_days=7, reason='ブラックリストユーザー')


        print(channel)
        if member.bot:
            if not self.member_is_bot.get(str(member.guild.id)):
                return

            role = member.guild.get_role(int(self.member_is_bot[str(member.guild.id)]['bot_role_id']))
            return await member.add_roles(role)

        else:
            if not self.member_not_is_bot.get(str(member.guild.id)):
                pass
            else:
                for role in int(self.member_not_is_bot[str(member.guild.id)]['member_role_id']):

                    role = member.guild.get_role(role)
                    await member.add_roles(role)
        

        if member.guild.id != 695801973127118899:
            return
        first_mes = await channel.send(f'{member.mention}貴方の年齢を数字のみで教えてください。例:) 25')

        def cehck(mes):
            return mes.author.id == member.id and channel.id == mes.channel.id

        message = await self.bot.wait_for('message', check=cehck)


        boy_channel = self.bot.get_channel(696064895107465389)
        girl_channel = self.bot.get_channel(696064931375611924)
        boy_profile = discord.utils.get(member.guild.roles, name='男性')
        girl_profile = discord.utils.get(member.guild.roles, name='女性')
        boy_mention = discord.utils.get(member.guild.roles, name='男性宛')
        girl_mention = discord.utils.get(member.guild.roles, name='女性宛')

        not_profile = discord.utils.get(message.guild.roles, name='not profile')

        try:
            if int(message.content) >= 20:
                two_mes = await channel.send(f'{member.mention}二つ目の質問です。貴方の性別を**男性**もしくは、**女性**で教えてください。')
                def role_check(mes):
                    return mes.author.id == member.id and channel.id == mes.channel.id

                profile_channel = await self.bot.wait_for('message', check=role_check)

                if profile_channel.content in ['男性', '女性']:
                    await member.add_roles(not_profile)

                else:
                    await member.kick()
                try:
                    await message.delete()
                    await profile_channel.delete()
                    await first_mes.delete()
                    await two_mes.delete()
       
                    async for mes in boy_channel.history(limit = None):
                        if mes.author == member:
                            await member.remove_roles(not_profile)
                            await member.add_roles(boy_profile)
                            await member.add_roles(boy_mention)

                    async for mes in girl_channel.history(limit = None):
                        if mes.author == member:
                            await member.remove_roles(not_profile)
                            await member.add_roles(girl_profile)
                            await member.add_roles(girl_mention)



                except:
                    channel = self.bot.get_channel(695803169678163970)
                    await channel.send(f'```py\n{traceback.format_exc()}\n```')

                    
        except ValueError:
            try:
                await channel.send(f'{member.mention}もう一度質問です。貴方の年齢を数字のみで教えてください。例:) 25')
                def ne_cehck(mes):
                    return mes.author.id == member.id and channel.id == mes.channel.id

                message = await self.bot.wait_for('message', check=ne_cehck)
                if int(message.content) >= 20:
                    two_mes = await channel.send(f'{member.mention}二つ目の質問です。貴方の性別を**男性**もしくは、**女性**で教えてください。')
                    def role_check(mes):
                        return mes.author.id == member.id and channel.id == mes.channel.id

                    profile_channel = await self.bot.wait_for('message', check=role_check)

                    if profile_channel.content in ['男性','男', '女性', '女']:
                        await member.add_roles(not_profile)

                    else:
                        await member.kick()

                    try:
                        await message.delete()
                        await profile_channel.delete()
                        await first_mes.delete()
                        await two_mes.delete()

                        async for mes in boy_channel.history(limit = None):
                            if mes.author == member:
                                await member.remove_roles(not_profile)
                                await member.add_roles(boy_profile)
                                await member.add_roles(boy_mention)

                        async for mes in girl_channel.history(limit = None):
                            if mes.author == member:
                                await member.remove_roles(not_profile)
                                await member.add_roles(girl_profile)
                                await member.add_roles(girl_mention)
                    except:
                        channel = self.bot.get_channel(695803169678163970)
                        await channel.send(f'```py\n{traceback.format_exc()}\n```')

                else:
                    await member.ban()

            except ValueError:
                await member.ban()
        

def setup(bot):
    bot.add_cog(Member_Event(bot))