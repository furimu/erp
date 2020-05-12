from discord.ext import commands, tasks
from cogs.utils import keys
import discord

GUILDID, CHANNELID = keys.guild_id(), keys.channel_id()


class Check_member(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.pro_count= {}
        self.check_member.start()


    def cog_unload(self):
        self.check_member.cancel()


    @tasks.loop(hours = 6)
    async def check_member(self):
        channel = self.bot.get_channel(CHANNELID.profile)
        e = discord.Embed(
            title = '定期チェック',
            description = '定期でプロフィール未記入者に通知します'
        )
        await channel.send(embed = e)
        guild = self.bot.get_guild(GUILDID.mainguild)
        role =discord.utils.get(guild.roles, name = 'not profile')
        for member in guild.members:
            self.pro_count[str(member.id)]=0
            if any(r.name == role.name for r in member.roles):
                await channel.send(f'{member.mention}さんプロフィールをお書きください。')
        try:
            async for message in channel.history(limit=None):
                if len(message.mentions) ==0:
                    return

                for user in message.mentions:
                    self.pro_count[str(user.id)] += 1

                    if self.pro_count[str(user.id)] <= 3:
                        await user.klck()

                        kick = self.bot.get_channel(CHANNELID.kick)
                        await kick.send(f"{user.name}{user. discriminator}さんがプロフィールを書かないためキックしました")

        except:
            error = self.bot.get_channel(CHANNELID.error)
            msg= list(traceback.TracebackException.from_exception(error).format())
            for i in range(0, len(msg), 1092):
                await errorsend(f'```py\n{msg[i:i+1092]}\n```')
        


    @check_member.before_loop
    async def check_before_loop(self):
        await self.bot.wait_until_ready()


def setup(bot):
    bot.add_cog(Check_member(bot))