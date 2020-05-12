from discord.ext import commands
from config import date
from cogs import help_
import botinfo
import traceback
import discord
import asyncio

prefixes = date.load('prefix')

cogs = [
    'cogs.admin',
    'cogs.anonymous',
    'cogs.auto_channel',
    'cogs.bumper',
    'cogs.counter',
    'cogs.guild_event',
    'cogs.log_server',
    'cogs.join_url',
    'cogs.member_event',
    'cogs.member_check',
    'cogs.mes',
    'cogs.moveer',
    'cogs.music',
    'cogs.reaction_role',
    'cogs.returnname',
    'cogs.setting',
    'cogs.spam'
]

spamer = date.load('spamer')
class ERP(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix = 'e!', description = botinfo.description, help_attrs=dict(hidden=True))

        self.token = botinfo.token

        
    
    async def on_ready(self):
        print('起動が完了しました!')

        for guild in self.guilds:
            if spamer.get(str(guild.id)):
                spamer.pop(str(guild.id))
                date.save(spamer, 'spamer')
        send_error_channel = self.get_channel(695803169678163970)
        await send_error_channel.send('新規エラー')
        for cog in cogs:
            try:
                self.load_extension(cog)
            except commands.ExtensionAlreadyLoaded:
                pass

            except Exception:
                await send_error_channel.send(f'```py\n{traceback.format_exc()}\n```')

    async def default_embed(self, mes: str):
        e = discord.Embed(
            description = mes
        )
        return e
    
    async def on_command_error(self, ctx, error):
        error = getattr(error, 'original', error)

        input_error = (commands.CommandNotFound, commands.UserInputError)
        Authority = (commands.CommandInvokeError, commands.MissingPermissions)

        if isinstance(error, commands.errors.CheckFailure):
            return 
        elif isinstance(error, Authority):
            await ctx.send('ごめん！君の権限が無いから実行できない！')
        elif isinstance(error, commands.NoPrivateMessage):
            await ctx.send('ごめん！このコマンドはプライベートでは使用できない！')
        elif isinstance(error, commands.DisabledCommand):
            await ctx.send('ごめん！このコマンドはメンテナンス中で無効化されてる！')
        elif isinstance(error, discord.errors.Forbidden):
            await ctx.send('ごめん！僕の権限が無いから変更できなかった！')

        

    async def on_message(self, mes):
        if mes.author.bot:
            return
        await self.process_commands(mes)



    async def start(self):
        await super().start(self.token)

    
    def main(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.start())
        loop.close()

if __name__ == '__main__':
    bot = ERP()
    bot.main()
