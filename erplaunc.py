from discord.ext import commands
from config import date
from cogs import help_
import botinfo
import traceback
import discord
import asyncio

prefixes = date.load('prefix')
spamer = date.load('spamer')

class ERP(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix = 'e!', description = botinfo.description, help_attrs=dict(hidden=True))

        self.token = botinfo.token
        self.load_extension(f"cogs.event.start")


    async def default_embed(self, mes: str):
        e = discord.Embed(
            description = mes
        )
        return e
        

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
