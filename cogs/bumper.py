from discord.ext import commands, tasks
from datetime import datetime, timedelta
from config import date
import discord
import traceback
class Bumper(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bump_time = date.load('bump_time')
        self.check_bump_time.start()


    def cog_unload(self):
        self.check_bump_time.cancel()


    @tasks.loop(minutes = 1)
    async def check_bump_time(self):
        try:
            now = datetime.utcnow() + timedelta(hours=9)
            
            for guild in self.bot.guilds:
                guild_id = str(guild.id)

                if not self.bump_time.get(guild_id):
                    return

                if not self.bump_time[guild_id].get('bump_role'):
                    target = guild.default_role

                elif now.strftime('%H') in ['23', '00', '01', '02', '03']:
                    
                    if not self.bump_time[guild_id].get('bump_role_night'):
                        target = guild.get_role(int(self.bump_time[guild_id]['bump_role']))

                    else:
                        target = guild.get_role(int(self.bump_time[guild_id]['bump_role_night']))

                else:
                    target = guild.get_role(int(self.bump_time[guild_id]['bump_role']))

                admin = self.bot.get_channel(696591762042650644)
               
                if self.bump_time[guild_id]['latest_time_h'] != str(f'{now:%H}'):
                    return


                
                await admin.send("a")
                if int(self.bump_time[guild_id]['latest_time_m']) - int(now.strftime('%M')) != 1:
                    return

                elif self.bump_time[guild_id]['enable_nihun'] == 'on':
                    return

                await admin.send("w")
                channel = self.bot.get_channel(int(self.bump_time[guild_id]['message_channel']))

                new_embed = discord.Embed(
                    title = f'bump一分前だよ！',
                    url = f'https://disboard.org/ja/server/{guild.id}'
                )

                

                if not self.bump_time[guild_id].get('enable_mention'):
                    await channel.send(embed = new_embed)

                elif self.bump_time[guild_id]['enable_mention'] == 'off':
                    await channel.send(embed = new_embed)    
                    

                elif self.bump_time[guild_id]['enable_mention'] == 'on':
                    await channel.send(target.mention, embed = new_embed)

                self.bump_time[guild_id]['enable_nihun'] = 'on'
                date.save(self.bump_time, 'bump_time')

        except Exception:
            error = self.bot.get_channel(695803169678163970)
            await error.send(f'```py\n{traceback.format_exc()}\n```')



    @check_bump_time.before_loop
    async def before_check_bump_time(self):
        await self.bot.wait_until_ready()


    @commands.command(aliases = ['sbp'])
    @commands.has_permissions(manage_roles=True)
    async def set_bumper(self, ctx, role: discord.Role):
        """
        引数に指定した役職に通知が飛ぶように設定するコマンドだよ！
        
        role: 名前・ID・メンション

        別名: sbp
        """
        guild_id = str(ctx.guild.id)
        if not self.bump_time.get(guild_id):
            self.bump_time[guild_id] = {}

        self.bump_time[guild_id]['bump_role'] = str(role.id)
        date.save(self.bump_time, 'bump_time')
        await ctx.send(f'**{role.name}**に通知が行くように設定したよ！')


    @commands.command(aliases= ['snb'])
    @commands.has_permissions(manage_roles=True)
    async def set_night_bumper(self, ctx, role: discord.Role):
        """
        引数に指定した役職に深夜帯に通知が飛ぶように設定するコマンドだよ！
        
        role: 名前・ID・メンション

        別名: snb
        """
        guild_id = str(ctx.guild.id)
        if not self.bump_time.get(guild_id):
            self.bump_time[guild_id] = {}

        self.bump_time[guild_id]['bump_role_night'] = str(role.id)
        date.save(self.bump_time, 'bump_time')
        await ctx.send(f'**{role.name}**に深夜帯に通知が行くように設定したよ！')

    @commands.command(aliases = ['sen'])
    @commands.has_permissions(manage_roles=True)
    async def set_enable(self, ctx, enable: str = 'on'):
        """
        引数にon(有効)/off(無効)を渡すことにより、bumpの通知時にメンションのオン・オフを切り替えます。

        enable: on/off

        別名: sen
        """

        guild_id = str(ctx.guild.id)
        if not self.bump_time.get(guild_id):
            self.bump_time[guild_id] = {}

        if enable == 'on':
            self.bump_time[guild_id]['enable_mention'] = 'on'

        elif enable == 'off':
            self.bump_time[guild_id]['enable_mention'] = 'off'

        date.save(self.bump_time, 'bump_time')

        mention_enable = '有効化' if enable == 'on' else '無効化'

        await ctx.send(f'メンションを{mention_enable}したよ！')


    @commands.Cog.listener()
    async def  on_message(self, mes):
        if isinstance(mes.channel, discord.DMChannel):
            return

        if mes.author.id != 302050872383242240:
            return

        admin = self.bot.get_channel(696591762042650644)
        
        
        guild_id = str(mes.guild.id)
        if embed := mes.embeds:
            for e in embed:
                if '表示順をアップしたよ' in e.description:
                    now = datetime.utcnow() + timedelta(hours=11)

                    new_embed = discord.Embed(
                        title = f'bumpを検知したよ！',
                        url = f'https://disboard.org/ja/server/{mes.guild.id}',
                        description = f"次回は{now.strftime('%m月%d月%H時%M分')}に出来るよ！"
                    )
                    await mes.channel.send(embed = new_embed)

                    if not self.bump_time.get(guild_id):
                        self.bump_time[guild_id] = {}

                    self.bump_time[guild_id]['latest_time_h'] = str(f'{now:%H}')
                    self.bump_time[guild_id]['latest_time_m'] = str(f'{now:%M}')
                    self.bump_time[guild_id]['message_channel'] = str(mes.channel.id)
                    self.bump_time[guild_id]['enable_mention'] = 'on'
                    self.bump_time[guild_id]['enable_nihun'] = 'off'
                    date.save(self.bump_time, 'bump_time')


                    
def setup(bot):
    bot.add_cog(Bumper(bot))