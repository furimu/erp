from discord.ext import commands

class Error(commands.Cog):
    def __init__(self, bot):
        self.bot=bot

        async def on_command_error(self, ctx, error):
        error = getattr(error, 'original', error)
 
        input_error = (commands.CommandNotFound, commands.UserInputError
        
        if isinstance(error, commands.CommandNotFound):
            await ctx.send("そ
          そのコマンドは存在しないよ！)