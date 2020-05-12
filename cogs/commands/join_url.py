from discord.ext import commands

class join(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    @commands.command(aliases=['invite'])
    async def join(self, ctx):
        """サーバーに参加させるための招待URLを発行
        
        別名: invite
        """
        perms = Permissions.none()
        perms.read_message_history = True
        perms.read_messages = True
        perms.send_messages = True
        perms.send_tts_messages = True

        perms.manage_roles = True
        perms.manage_channels = True

        perms.embed_links = True

        perms.add_reactions = True

        perms.kick_members = True
        
        perms.connect = True
        perms.speak = True
        perms.move_members = True
        
        await ctx.send(f'<{utils.oauth_url(botinfo.client_id, perms)}>')


    @join.error
    async def join_error(self, ctx, error):
        await ctx.send(f'```py\n{traceback.format_exc()}\n```')


def setup(bot):
    bot.add_cog(join(bot))