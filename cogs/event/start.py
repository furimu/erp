from discord.ext import commands
import traceback

cogs = [
    'manage.admin',
    'event.auto_channel',
    'event.bumper',
    'event.counter',
    'event.err',
    'commands.easy_poll',
    'event.guild_event',
    'log_server',
    'commands.join_url',
    'event.member_event',
    'event.member_check',
    'event.mes',
    'commands.moveer',
    'commands.music',
    'event.reaction_role',
    'commands.returnname',
    'spam'
]

class Ready(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('起動が完了しました!')

        send_error_channel = self.bot.get_channel(695803169678163970)

        for cog in cogs:
            try:
                self.bot.load_extension(f"cogs.{cog}")
            except commands.ExtensionAlreadyLoaded:
                pass

            except Exception:
                msg=traceback.format_exc()
                for i in range(0, len(msg), 1092):
                    await send_error_channel.send(f'```py\n{msg[i:i+1092]}\n```')

def setup(bot):
    bot.add_cog(Ready(bot))