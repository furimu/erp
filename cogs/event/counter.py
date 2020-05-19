from discord.ext import commands, tasks
from config import date
import discord
import traceback

class Counter(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.counter = date.load('member_counter')
        self.role_counter = date.load('role_counter')
        self.member_count.start()
        self.role_count.start()


    def cog_unload(self):
        self.member_count.cancel()
        self.role_count.cancel()

    @tasks.loop(minutes = 1)
    async def member_count(self):
        admin = self.bot.get_channel(696591762042650644)
        for guild in self.bot.guilds:
            guild_id = str(guild.id)

            if not self.counter.get(guild_id):
                return

            if not self.counter[guild_id].get('bot_role_id'):
                return

            voice = self.bot.get_channel(int(self.counter[guild_id]['voice_id']))
            bot_role = guild.get_role(int(self.counter[guild_id]['bot_role_id']))

            await voice.edit(name = f'サーバー人数: {guild.member_count}')
            for member in guild.members:
                try:
                    if member.id == 693839038200938547:
                        await voice.set_permissions(bot_role, manage_channels=True)
                    else:
                        await voice.set_permissions(member, connect=False)
                    
                except discord.errors.Forbidden:
                    pass
            

    @member_count.before_loop
    async def before_member_count(self):
        await self.bot.wait_until_ready()



    @tasks.loop(minutes = 1)
    async def role_count(self):
        admin = self.bot.get_channel(696591762042650644)
        for guild in self.bot.guilds:
            guild_id = str(guild.id)
            if not self.role_counter.get(guild_id):
                return

            if not self.counter[guild_id].get('bot_role_id'):
                return

            counter = 0
            while True:
                
                if not self.role_counter[guild_id].get(str(counter)):
                    break

                voice = self.bot.get_channel(int(self.role_counter[guild_id][str(counter)]['voice_channel']))
                role = guild.get_role(int(self.role_counter[guild_id][str(counter)]['role_id']))
                bot_role = guild.get_role(int(self.counter[guild_id]['bot_role_id']))

                await voice.edit(name = f'{role.name}人数: {len(role.members)}')
                for member in guild.members:
                    try:
                        if member.id == 693839038200938547:
                            await voice.set_permissions(bot_role, manage_channels=True)

                        else:
                            await voice.set_permissions(member, connect=False)
                    except discord.errors.Forbidden:
                        continue

                counter = counter + 1
                


    @role_count.before_loop
    async def before_role_count(self):
        await self.bot.wait_until_ready()


    async def say_permissions(self, ctx, member):
        permissions = member.guild_permissions
        e = discord.Embed(colour=member.colour)
        avatar = member.avatar_url_as(static_format='png')
        e.set_author(name=str(member), url=avatar)
        allowed, denied = [], []
        for name, value in permissions:
            name = name.replace('_', ' ').replace('guild', 'server').title()
            if value:
                allowed.append(name)
            else:
                denied.append(name)

        e.add_field(name='Allowed', value='\n'.join(allowed))
        e.add_field(name='Denied', value='\n'.join(denied))
        await ctx.send(embed=e)

    @commands.command(hidden = True)
    async def cp(self, ctx, channel: discord.VoiceChannel):
        """Shows a member's permissions in a specific channel.
        If no channel is given then it uses the current one.
        You cannot use this in private messages. If no member is given then
        the info returned will be yours.
        """

        member = ctx.guild.me

        await self.say_permissions(ctx, member)

    @cp.error
    async def load_error(self, ctx, error):
        await ctx.send(f'```py\n{traceback.format_exc()}\n```')


    @commands.command()
    async def ch(self, ctx):
        await ctx.send(f'このサーバーのチャンネル数: {len(ctx.guild.channels)}')

    
    @commands.command(aliases = ['gm'])
    async def guild_member(self, ctx):
        await ctx.send(f'サーバーの人数: {ctx.guild.member_count}')

    @commands.command()
    async def sm(self, ctx):
        e = discord.Embed(
            title = str(ctx.guild.member_count),
            description= ',/n'.join(member.mention for member in ctx.guild.members)
        )
        await ctx.send(embed=e)
    
    @commands.command(aliases = ['rml'])
    @commands.has_permissions(manage_channels = True)
    async def role_members(self, ctx, role: discord.Role):
        """指定された役職を持ってるユーザーを表示します
        
        role: 名前・ID・メンション

        別名: rml
        """
        e = discord.Embed(
            description = ",\n ".join(x.name for x in role.members)
        )
        await ctx.send(embed = e)

    
    @commands.command(aliases = ['vm'])
    async def voice_member(self, ctx):
        voice_member_ = 0
        for voice in ctx.guild.voice_channels:
            voice_member_ = voice_member_ + len(voice.members)

        await ctx.send(f'現在VCに上がってる人の人数: {voice_member_}')

    @commands.command(aliases= ['svb'])
    @commands.has_permissions(manage_roles = True)
    async def set_vc_bot(self, ctx, role: discord.Role):
        """チャンネルを管理するBOTの役職を設定

        BOTに統一して付いてる役職を設定して下さい。

        別名: svm
        """
        guild_id = str(ctx.guild.id)
        if not self.counter.get(guild_id):
            self.counter[guild_id] = {}

        self.counter[guild_id]['bot_role_id'] = str(role.id)
        date.save(self.counter, 'member_counter')

        await ctx.send(f'BOTの役職を{role.name}に設定しました')


    @commands.command(aliases= ['svm'])
    @commands.has_permissions(manage_channels = True)
    async def set_vc_member(self, ctx):
        """サーバーの人数を表示するVCを作成


        別名: svm
        """
        guild_id = str(ctx.guild.id)
        if not self.counter.get(guild_id):
            self.counter[guild_id] = {}

        new_voice = await ctx.guild.create_voice_channel(name = f"サーバー人数{ctx.guild.member_count}")

        for member in ctx.guild.members:
            try:
                if member.id == 693839038200938547:
                    bot_role = ctx.guild.get_role(int(self.counter[guild_id]['bot_role_id']))
                    await new_voice.set_permissions(bot_role, manage_channels=True)
                else:
                    await new_voice.set_permissions(member, connect=False)
            except discord.errors.Forbidden:

                pass

        bot_role = ctx.guild.get_role(int(self.counter[guild_id]['bot_role_id']))
        await new_voice.set_permissions(bot_role, manage_channels=True)

        self.counter[guild_id]['voice_id'] = str(new_voice.id)

        date.save(self.counter, 'member_counter')

        await ctx.send(f'サーバー人数: {ctx.guild.member_count}を作成しました')


    @set_vc_member.error
    async def set_vc_member_error(self, ctx, error):
 
        await ctx.send(f'```py\n{traceback.format_exc()}\n```')


    @commands.command(aliases= ['svr'])
    @commands.has_permissions(manage_channels = True)
    async def set_vc_role(self, ctx, roles: commands.Greedy[discord.Role]):
        """指定された役職を持つ人数を表示するVCを作成
        引数には複数の役職を指定可能
        roles: 名前・ID・メンション
        別名: svm
        """
        guild_id = str(ctx.guild.id)
        if not self.role_counter.get(guild_id):
            self.role_counter[guild_id] = {}


        for role in roles:
            new_voice = await ctx.guild.create_voice_channel(name = f"{role.name}人数: {len(role.members)}")
            for member in ctx.guild.members:
                try:
                    if member.id == 693839038200938547:
                        bot_role = ctx.guild.get_role(int(self.counter[guild_id]['bot_role_id']))
                        await new_voice.set_permissions(bot_role, manage_channels=True)
                    else:
                        await new_voice.set_permissions(member, connect=False)

                except discord.errors.Forbidden:
                    pass

            await ctx.send(f'{role.name}人数: {len(role.members)}を作成しました')

            
        counter = 0
        while True:
            if self.role_counter[guild_id].get(str(counter)):
                counter = counter + 1
                continue
            
            elif not self.role_counter[guild_id].get(str(counter)):
                self.role_counter[guild_id][str(counter)] = {}

            self.role_counter[guild_id][str(counter)]['voice_channel'] = str(new_voice.id)
            self.role_counter[guild_id][str(counter)]['role_id'] = str(role.id)
            date.save(self.role_counter, 'role_counter')
            break
        

    @set_vc_role.error
    async def set_vc_role_error(self, ctx, error):
 
        await ctx.send(f'```py\n{traceback.format_exc()}\n```')


    @commands.command(aliases= ['rer'])
    @commands.has_permissions(manage_channels = True)
    async def reset_role(self, ctx):
        """指定された役職を持つ人数を表示するVCを作成
        引数には複数の役職を指定可能
        roles: 名前・ID・メンション
        別名: svm
        """
        guild_id = str(ctx.guild.id)
        if not self.role_counter.get(guild_id):
            self.role_counter[guild_id] = {}
            return

        self.role_counter.pop(guild_id)
        date.save(self.role_counter, 'role_counter')

        await ctx.send(f'{ctx.guild.name}: roleVCの設定を削除しました')

    @commands.command(aliases = ['vv'])
    async def vc_view(self, ctx, opt: str, voice: discord.VoiceChannel = None):
        guild_id = str(ctx.guild.id)
        if not self.counter.get(guild_id):
            return

        if voice is None:

            if opt == 'guild':
                voice = self.bot.get_channel(int(self.counter[guild_id]['voice_id']))
                for member in ctx.guild.members:
                    try:
                        if member.id == 693839038200938547:
                            bot_role = ctx.guild.get_role(int(self.counter[guild_id]['bot_role_id']))
                            await new_voice.set_permissions(bot_role, manage_channels=True)
                        else:
                            await new_voice.set_permissions(member, connect=False)

                    except discord.errors.Forbidden:
                        pass

            elif opt == 'role':
                while True:
                    counter = 0
                    if not self.role_counter[guild_id].get(str(counter)):
                        break

                    voice = self.bot.get_channel(int(self.role_counter[guild_id][str(counter)]['voice_channel']))
                    role = ctx.guild.get_role(int(self.role_counter[guild_id][str(counter)]['role_id']))
                    for member in ctx.guild.members:
                        try:
                            if member.id == 693839038200938547:
                                bot_role = ctx.guild.get_role(int(self.counter[guild_id]['bot_role_id']))
                                await new_voice.set_permissions(bot_role, manage_channels=True)
                            else:
                                await new_voice.set_permissions(member, connect=False)

                        except discord.errors.Forbidden:
                            pass

                    counter = counter + 1

            else:
                return await ctx.send('不正な値が渡されました')

        else:
            if opt == 'guild':
                for member in ctx.guild.members:
                    try:
                        if member.id == 693839038200938547:
                            bot_role = ctx.guild.get_role(int(self.counter[guild_id]['bot_role_id']))
                            await new_voice.set_permissions(bot_role, manage_channels=True)
                        else:
                            await new_voice.set_permissions(member, connect=False)

                    except discord.errors.Forbidden:
                        pass

            elif opt == 'role':
                for member in ctx.guild.members:
                    try:
                        if member.id == 693839038200938547:
                            bot_role = ctx.guild.get_role(int(self.counter[guild_id]['bot_role_id']))
                            await new_voice.set_permissions(bot_role, manage_channels=True)
                        else:
                            await new_voice.set_permissions(member, connect=False)

                    except discord.errors.Forbidden:
                        pass

            else:
                return await ctx.send('不正な値が渡されました')


    
    @commands.Cog.listener()
    async def on_member_join(self, member):
        guild_id = str(member.guild.id)
        if not self.counter.get(guild_id):
            return

        if not self.counter[guild_id].get('bot_role_id'):
            return

        voice = self.bot.get_channel(int(self.counter[guild_id]['voice_id']))
         
        await voice.edit(name = f'サーバー人数{member.guild.member_count}')



    @commands.Cog.listener()
    async def on_member_remove(self, member):
        guild_id = str(member.guild.id)
        if not self.counter.get(guild_id):
            return

        if not self.counter[guild_id].get('bot_role_id'):
            return

        voice = self.bot.get_channel(int(self.counter[guild_id]['voice_id']))
         
        await voice.edit(name = f'サーバー人数{guild.member_count}')
            

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        guild_id = str(before.guild.id)
        if before.roles != after.roles:
            for role in before.roles:
                if role.name == '男性':
                    pass

                elif role.name == '女性':
                    pass
            else:
                while True:
                    counter = 0
                    if not self.role_counter[guild_id].get(str(counter)):
                        break

                    voice = self.bot.get_channel(int(self.role_counter[guild_id][str(counter)]['voice_channel']))
                    role = guild.get_role(int(self.role_counter[guild_id][str(counter)]['role_id']))
                    await voice.edit(name = f'{role.name}人数: {len(role.members)}')
                    counter = counter + 1

                    
def setup(bot):
    bot.add_cog(Counter(bot))