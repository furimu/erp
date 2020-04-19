from discord.ext import commands
import discord
class Anonymous(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(hidden = True)
    async def admin_anony(self, ctx, *, contents: str):
        """BOT開発者兼サポートサーバー管理者に匿名でメッセージが行くようにします。
        """
        if not isinstance(ctx.channel, discord.DMChannel):
            return

        now = datetime.utcnow() + timedelta(hours=9)

        e = discord.Embed(
            description = contents
        )
        e.set_footer(
            text = now.strftime('%m月%d月%H時%M分')
        )
        await ctx.send(embed = e)


    @commands.command()
    async def que(self, ctx, *, contents):
        """サポートサーバーに匿名でメッセージが行くようにします。
        """
        if not isinstance(ctx.channel, discord.DMChannel):
            return

        now = datetime.utcnow() + timedelta(hours=9)

        e = discord.Embed(
            description = contents
        )
        e.set_footer(
            text = now.strftime('%m月%d月%H時%M分')
        )
        channel = self.bot.get_channel(698085469388406794)
        await channel.send(embed = e)


def setup(bot):
    bot.add_cog(Anonymous(bot))