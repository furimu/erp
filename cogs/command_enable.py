from discord.ext import commands
from config import date
import discord
import traceback


class Commands_Enable(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cmd_ena = date.load('cmd_ena')
        self.mcmd_ena = date.load('mcmd_ena')


    @commands.command(aliases=  ['cde'])
    async def cmde(self, ctx, command_name: str, enable: str = None):
        role_flag = False
        
        if self.mcmd_ena.get(str(ctx.guild.id), None) is None:
            await ctx.send(self.mcmd_ena)
            self.mcmd_ena[str(ctx.guild.id)] = {}
            date.save(self.mcmd_ena, 'mcmd_ena')
            return
        
        if (manage_users := self.mcmd_ena[str(ctx.guild.id)].get('manage_users')):
            if str(ctx.author.id) not in self.mcmd_ena[str(ctx.guild.id)]['manage_users']:    
                return

        if (manage_roles := self.mcmd_ena[str(ctx.guild.id)].get('manage_roles')):
            for role in ctx.author.roles:
                if str(role.id) in self.mcmd_ena[str(ctx.guild.id)]['manage_roles']:
                    role_flag = True
            else:
                if role_flag == False:
                    return

        if (not manage_roles) and (not manage_users):
            return await ctx.send('これは**非常に危険**な状態です。今のままでは、誰でもコマンドの**オン・オフ**を設定できてしまいます。設定を変更できる**ユーザー・役職**を追加して下さい。')


        cmd = self.bot.get_command(command_name)
        if cmd is None:
            return await ctx.send(f'{command_name}はこのBOTのコマンドに存在しないよ!')

        if enable is None:
            return await ctx.send('on/offが指定されていないよ!')

        if not self.cmd_ena.get(str(ctx.guild.id)):
            self.cmd_ena[str(ctx.guild.id)] = {}

        enable_bool = True if enable in ['on', 'ON'] else False if enable in ['off', 'OFF'] else '不正な値'

        if enable_bool == '不正な値':
            return await ctx.send('不正な値が入力されました。 on/off 又は off/OFFを入力してね!')

        self.cmd_ena[str(ctx.guild.id)][command_name] = enable_bool
        date.save(self.cmd_ena, 'cmd_ena')
        await ctx.send(command_name + 'を有効化しました!' if enable_bool == True else command_name + 'を無効化しました!')


    @commands.command(aliases= ['mucmd'])
    @commands.has_permissions(administrator = True)
    async def manage_ucmde(self, ctx, user: discord.Member = None):
        if user is None:
            return await ctx.send('ユーザーが指定されていないよ!')


        if not self.mcmd_ena.get(str(ctx.guild.id)):
            self.mcmd_ena[str(ctx.guild.id)] = {}

        if not self.mcmd_ena[str(ctx.guild.id)].get('manage_users'):
            self.mcmd_ena[str(ctx.guild.id)]['manage_users'] = []

        self.mcmd_ena[str(ctx.guild.id)]['manage_users'].append(str(user.id))
        date.save(self.mcmd_ena, 'mcmd_ena')

        await ctx.send(f'{user}にコマンド管理権限を付与したよ!')

    @manage_ucmde.error
    async def manage_ucmde_error(self, ctx, error):
        await ctx.send(f'```py\n{traceback.format_exc()}\n```')


    @commands.command(aliases= ['mrcmd'])
    @commands.has_permissions(administrator = True)
    async def manage_rcmde(self, ctx, role: discord.Role = None):
        if role is None:
            return await ctx.send('役職が指定されていないよ!')

        if not self.mcmd_ena.get(str(ctx.guild.id)):
            self.mcmd_ena[str(ctx.guild.id)] = {}

        if not self.mcmd_ena[str(ctx.guild.id)].get('manage_roles'):
            self.mcmd_ena[str(ctx.guild.id)]['manage_roles'] = []

        self.mcmd_ena[str(ctx.guild.id)]['manage_roles'].append(str(role.id))
        date.save(self.mcmd_ena, 'mcmd_ena')

        await ctx.send(f'{role}にコマンド管理権限を付与したよ!')


    @commands.command(aliases= ['rmucmd'])
    @commands.has_permissions(administrator = True)
    async def remove_manage_ucmde(self, ctx, user: discord.Member = None):
        if user is None:
            return await ctx.send('ユーザーが指定されていないよ!')

        if not self.mcmd_ena.get(str(ctx.guild.id)):
            self.mcmd_ena[str(ctx.guild.id)] = {}
            return

        if not self.mcmd_ena[str(ctx.guild.id)].get('manage_users'):
            self.mcmd_ena[str(ctx.guild.id)]['manage_users'] = []
            return

        self.mcmd_ena[str(ctx.guild.id)]['manage_users'].remove(str(user.id))
        date.save(self.mcmd_ena, 'mcmd_ena')

        await ctx.send(f'{user}のコマンド管理権限を剥奪したよ!')


    @commands.command(aliases= ['rmrcmd'])
    @commands.has_permissions(administrator = True)
    async def remove_manage_rcmde(self, ctx, role: discord.Role = None):
        if role is None:
            return await ctx.send('役職が指定されていないよ!')

        if not self.mcmd_ena.get(str(ctx.guild.id)):
            self.mcmd_ena[str(ctx.guild.id)] = {}
            return

        if not self.mcmd_ena[str(ctx.guild.id)].get('manage_roles'):
            self.mcmd_ena[str(ctx.guild.id)]['manage_roles'] = []
            return

        self.mcmd_ena[str(ctx.guild.id)]['manage_roles'].remove(str(role.id))
        date.save(self.mcmd_ena, 'mcmd_ena')

        await ctx.send(f'{role}のコマンド管理権限を剥奪したよ!')


    @commands.command(aliases= ['wmu'])
    @commands.has_permissions(administrator = True)
    async def watch_manage_user(self, ctx):
        if not self.mcmd_ena.get(str(ctx.guild.id)):
            self.mcmd_ena[str(ctx.guild.id)] = {}
            return

        if not self.mcmd_ena[str(ctx.guild.id)].get('manage_users'):
            self.mcmd_ena[str(ctx.guild.id)]['manage_users'] = []
            return

        e = discord.Embed(
            title = 'コマンド管理権限を持っている人々',
            description = ',\n'.join(ctx.guild.get_member(int(x)).mention for x in self.mcmd_ena[str(ctx.guild.id)]['manage_users'])
        )

        await ctx.send(embed = e)

    @watch_manage_user.error
    async def wmu_error(self, ctx, error):
        await ctx.send(f'```py\n{traceback.format_exc()}\n```')


    @commands.command(aliases= ['wmr'])
    @commands.has_permissions(administrator = True)
    async def watch_manage_role(self, ctx):
        if not self.mcmd_ena.get(str(ctx.guild.id)):
            self.mcmd_ena[str(ctx.guild.id)] = {}
            return

        if not self.mcmd_ena[str(ctx.guild.id)].get('manage_roles'):
            self.mcmd_ena[str(ctx.guild.id)]['manage_roles'] = []
            return

        e = discord.Embed(
            title = 'コマンド管理権限を持っている役職群',
            description = ',\n'.join(ctx.guild.get_member(int(x.id)).mention for x in self.mcmd_ena[str(ctx.guild.id)]['manage_roles'])
        )

        await ctx.send(embed = e)


def setup(bot):
    bot.add_cog(Commands_Enable(bot))