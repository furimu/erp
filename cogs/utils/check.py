from config import date
cmd_ena = date.load('cmd_ena')

async def original_command_permissions(ctx):
    command = ctx.command
    guild_id = str(ctx.guild.id)
    if not cmd_ena.get(guild_id):
        return await ctx.message.add_reaction('\U00002757')

    elif cmd_ena[guild_id].get(command.name):
        server_key = cmd_ena[guild_id]
        run = True if server_key[command.name] == True else False if server_key[command.name] == False else '不正な値'
        await ctx.send(run)
        if run == True:
            return True

        elif run == False:
            return False
