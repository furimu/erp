from discord.ext import commands
from config import date
import discord

black_list= date.load("black_list")

class Guild_Event(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.notice = date.load('notice')
    
    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        if guild.id != 695801973127118899:
            return

        if black_list.get(str(guild.id)) is not None:
            if black_list[str(guild.id)]== "red":
                return await guild.leave()
        


def setup(bot):
    bot.add_cog(Guild_Event(bot))