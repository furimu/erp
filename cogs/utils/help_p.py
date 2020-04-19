import discord

async def default_help(bot, commands, ctx):
    e = discord.Embed(
        title = f'{bot.user.name}のコマンド一覧',
        description = '詳しいコマンドの説明を見たい場合は、e!help <コマンド名>'
    )
    test = []
    for command in commands:
         

    e.add_field(
        name = f'**aa**',
        value = ','.join([f'`{x.name}`' for x in new_cog.get_commands() if not x.hidden]),
        inline = False
    )
       
    await ctx.send(embed = e)


def cog_help(bot, cog: str):
    cog = bot.get_cog(cog)
    if len(cog.get_commands()) != 0:
        e = discord.Embed(
            title = f'{cog}のコマンド一覧',
            description = '詳しいコマンドの説明を見たい場合は、e!help <コマンド名>'
        )
        e.add_field(
            name = f'**{cog}**',
            value = ','.join([f'`{x.name}``' for x in new_cog.get_commands()]),
            inline = False
        )

    else:
        e = discord.Embed(
            description = 'そのカテゴリーには、コマンドは見つかりませんでした。'
        )

    return e