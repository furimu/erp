from discord.ext import commands

class Ready(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('起動が完了しました!')

        for guild in self.guilds:
            if spamer.get(str(guild.id)):
                spamer.pop(str(guild.id))
                date.save(spamer, 'spamer')
        send_error_channel = self.get_channel(695803169678163970)
        await send_error_channel.send('新規エラ
        for cog in cogs:
            try:
                self.load_extension(cog)
            except commands.ExtensionAlreadyLoaded:
                pass

            except Exception:
                pass