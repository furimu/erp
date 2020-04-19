from discord.ext import commands, tasks
import discord


class Check_member(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.check_member.start()


    def cog_unload(self):
        self.check_member.cancel()


    @tasks.loop(hours = 6)
    async def check_member(self):
        channel = self.bot.get_channel(699031258201718846)
        e = discord.Embed(
            title = '定期チェック',
            description = '定期でプロフィール未記入者に通知します'
        )
        await channel.send(embed = e)
        for guild in self.bot.guilds:
            role = discord.utils.get(guild.roles, name = 'not profile')
            if guild.id == 695801973127118899:
                for member in guild.members:
                    if any(r.name == role.name for r in member.roles):
                        
                        
                        await channel.send(f'{member.mention}さんプロフィールをお書きください。')


    @check_member.before_loop
    async def check_before_loop(self):
        await self.bot.wait_until_ready()


def setup(bot):
    bot.add_cog(Check_member(bot))