from discord.ext import commands

class Error(commands.Cog):
    def __init__(self, bot):
        self.bot=bot

        async def on_command_error(self, ctx, error):
        error = getattr(error, 'original', error)
 
        input_error = (commands.CommandNotFound, commands.UserInputError
        
        if isinstance(error, commands.CommandNotFound):
            await ctx.send("そのコマンドは存在しないよ！")

        else:
            msg=traceback.format_exc()
            for i in range(0, len(msg), 1092):
                await ctx.channel.send(f'```py\n{msg[i:i+1092]}\n```')