from discord.ext import commands
from config import date
import discord
import asyncio
import traceback
class Reaction_Role(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.reaction_role = date.load('reaction_role')
        self.reactions_ = ['\u0031\u20e3', '\u0032\u20e3', '\u0033\u20e3', '\u0034\u20e3', '\u0035\u20e3', '\u0036\u20e3', "\u0037\u20e3", '\u0038\u20e3', '\u0039\u20e3']
        self.count_ = [1, 2, 3, 4, 5, 6, 7, 8, 9]


            

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.member.bot:
            return
        guild = payload.member.guild
        channel = self.bot.get_channel(payload.channel_id)
        mes = await channel.fetch_message(payload.message_id)
        member = payload.member

        if not self.reaction_role.get(str(guild.id)):
            return

        if embeds := mes.embeds:
            for e in embeds:
                for group in self.reaction_role[str(guild.id)].keys():

                    if e.title != group:
                        continue
                    

                    if str(payload.emoji) == '\u0031\u20e3':
                        role = guild.get_role(int(self.reaction_role[str(guild.id)][group]['1']))

                        if any(r.name == role.name for r in member.roles):
                            await member.remove_roles(role)

                        elif not any(r.name == role.name for r in member.roles):
                            await member.add_roles(role)

                    elif str(payload.emoji) == '\u0032\u20e3':
                        role = guild.get_role(int(self.reaction_role[str(guild.id)][group]['2']))

                        if any(r.name == role.name for r in member.roles):
                            await member.remove_roles(role)

                        elif not any(r.name == role.name for r in member.roles):
                            await member.add_roles(role)

                    elif str(payload.emoji) == '\u0033\u20e3':
                        role = guild.get_role(int(self.reaction_role[str(guild.id)][group]['3']))

                        if any(r.name == role.name for r in member.roles):
                            await member.remove_roles(role)

                        elif not any(r.name == role.name for r in member.roles):
                            await member.add_roles(role)

                    elif str(payload.emoji) == '\u0034\u20e3':
                        role = guild.get_role(int(self.reaction_role[str(guild.id)][group]['4']))

                        if any(r.name == role.name for r in member.roles):
                            await member.remove_roles(role)

                        elif not any(r.name == role.name for r in member.roles):
                            await member.add_roles(role)

                    elif str(payload.emoji) == '\u0035\u20e3':
                        role = guild.get_role(int(self.reaction_role[str(guild.id)][group]['5']))

                        if any(r.name == role.name for r in member.roles):
                            await member.remove_roles(role)

                        elif not any(r.name == role.name for r in member.roles):
                            await member.add_roles(role)

                    elif str(payload.emoji) == '\u0036\u20e3':
                        role = guild.get_role(int(self.reaction_role[str(guild.id)][group]['6']))

                        if any(r.name == role.name for r in member.roles):
                            await member.remove_roles(role)

                        elif not any(r.name == role.name for r in member.roles):
                            await member.add_roles(role)

                    elif str(payload.emoji) == '\u0037\u20e3':
                        role = guild.get_role(int(self.reaction_role[str(guild.id)][group]['7']))

                        if any(r.name == role.name for r in member.roles):
                            await member.remove_roles(role)

                        elif not any(r.name == role.name for r in member.roles):
                            await member.add_roles(role)

                    elif str(payload.emoji) == '\u0038\u20e3':
                        role = guild.get_role(int(self.reaction_role[str(guild.id)][group]['8']))

                        if any(r.name == role.name for r in member.roles):
                            await member.remove_roles(role)

                        elif not any(r.name == role.name for r in member.roles):
                            await member.add_roles(role)

                    elif str(payload.emoji) == '\u0039\u20e3':
                        role = guild.get_role(int(self.reaction_role[str(guild.id)][group]['9']))

                        if any(r.name == role.name for r in member.roles):
                            await member.remove_roles(role)

                        elif not any(r.name == role.name for r in member.roles):
                            await member.add_roles(role)
                            
                    await mes.remove_reaction(str(payload.emoji), member)


                            

    @commands.command(aliases= ['cr'])
    @commands.has_permissions(manage_messages = True)
    async def create_react(self, ctx, group: str, channel: discord.TextChannel, roles: commands.Greedy[discord.Role] = None):
        """リアクションで役職を付けれるように設定します

        引数にgroupを渡す。これはどのようなジャンルの役職なのか大雑把に説明する為の物。あまり長い名前は推奨しない。
        次の引数にchannelを渡す。これはどこのチャンネルでリアクションロールを動かすか。
        最後の引数にリアクションで付ける役職を指定。最大9個

        group: str
        channel: 名前・ID・メンション
        roles: 名前・ID・メンション

        別名: cr
        """

        if roles is None:
            return await ctx.send('roleが指定されていません')

        if not self.reaction_role.get(str(ctx.guild.id)):
            self.reaction_role[str(ctx.guild.id)] = {}

        counter = 0
        self.reaction_role[str(ctx.guild.id)][group] = {}
        date.save(self.reaction_role, 'reaction_role')
        for role in roles:
            counter = counter + 1
            self.reaction_role[str(ctx.guild.id)][group]['channel'] = str(channel.id)
            self.reaction_role[str(ctx.guild.id)][group][str(counter)] = str(role.id)
            date.save(self.reaction_role, 'reaction_role')

            if counter == 9:
                await ctx.send(f'上限9個を超えました。{role}までの保存が完了しました')
                break


        e = discord.Embed(
            title = group,
            description = '下のリアクションを押すと対象の役職がつきます'
        )
        
        counter = 1
        for role in roles:
            
            e.add_field(
                name = str(counter),
                value = role.name,
                inline = False
            )

            counter = counter + 1


        react_mes = await channel.send(embed = e)

        self.reaction_role[str(ctx.guild.id)][group]['message_id'] = str(react_mes.id)
        date.save(self.reaction_role, 'reaction_role')


        count = 1
        while True:
   
            if not self.reaction_role[str(ctx.guild.id)][group].get(str(count)):
                break

            for k in self.reaction_role[str(ctx.guild.id)][group].keys():
                if k == '1':
                    await react_mes.add_reaction('\u0031\u20e3')

                elif k == '2':
                    await react_mes.add_reaction('\u0032\u20e3')

                elif k == '3':
                    await react_mes.add_reaction('\u0033\u20e3')

                elif k == '4':
                    await react_mes.add_reaction('\u0034\u20e3')

                elif k == '5':
                    await react_mes.add_reaction('\u0035\u20e3')

                elif k == '6':
                    await react_mes.add_reaction('\u0036\u20e3')

                elif k == '7':
                    await react_mes.add_reaction('\u0037\u20e3')

                elif k == '8':
                    await react_mes.add_reaction('\u0038\u20e3')

                elif k == '9':
                    await react_mes.add_reaction('\u0039\u20e3')

            count = count + 1

    @create_react.error
    async def add_react_error(self, ctx, error):
        await ctx.send(f'```py\n{traceback.format_exc()}\n```')

    @commands.command(aliases = ['ar'])
    @commands.has_permissions(manage_messages = True)
    async def add_react(self, ctx, group: str, roles: commands.Greedy[discord.Role]):
        """リアクションで付けれる役職を増やす

        引数にgroupを渡す。
        最後の引数にリアクションで付ける役職を指定。合計の最大9個

        group: str
        roles: 名前・ID・メンション

        別名: ar
        """

        if roles is None:
            return await ctx.send('roleが指定されていません')

        if (not self.reaction_role.get(str(ctx.guild.id))) or (not self.reaction_role[str(ctx.guild.id)].get(group)):
            return await ctx.send('データが見つかりません')

        counter = 1
        while True:
            if self.reaction_role[str(ctx.guild.id)][group].get(str(counter)):
                counter = counter + 1
                continue
            
            if not self.reaction_role[str(ctx.guild.id)][group].get(str(counter)):
                if counter >= 10:
                    await ctx.send(f'上限9個を超えたよ')
                break

        channel = self.bot.get_channel(int(self.reaction_role[str(ctx.guild.id)][group]['channel']))
        react_mes = await channel.fetch_message(int(self.reaction_role[str(ctx.guild.id)][group]['message_id']))

        async for mes in channel.history(limit = None):
            if embeds := mes.embeds:
                for e in embeds:
                    if e.title != group:
                        continue
                        

                    for role in roles:
                        e.add_field(
                            name = str(counter),
                            value = role.name,
                            inline = False
                        )
                        self.reaction_role[str(ctx.guild.id)][group][str(counter)] = str(role.id)
                        date.save(self.reaction_role, 'reaction_role')
                        if counter == 1:
                            await react_mes.add_reaction('\u0031\u20e3')

                        elif counter == 2:
                            await react_mes.add_reaction('\u0032\u20e3')

                        elif counter == 3:
                            await react_mes.add_reaction('\u0033\u20e3')

                        elif counter == 4:
                            await react_mes.add_reaction('\u0034\u20e3')

                        elif counter == 5:
                            await react_mes.add_reaction('\u0035\u20e3')

                        elif counter == 6:
                            await react_mes.add_reaction('\u0036\u20e3')

                        elif counter == 7:
                            await react_mes.add_reaction('\u0037\u20e3')

                        elif counter == 8:
                            await react_mes.add_reaction('\u0038\u20e3')

                        elif counter == 9:
                            await react_mes.add_reaction('\u0039\u20e3')
                        counter = counter + 1

                    await mes.edit(embed = e)


    @add_react.error
    async def edit_react_error(self, ctx, error):
        await ctx.send(f'```py\n{traceback.format_exc()}\n```')


        
    @commands.command(aliases = ['dr'])
    @commands.has_permissions(manage_messages = True)
    async def del_react(self, ctx, group: str):
        """グループのリアクションロールの設定を削除

        引数にgroupを渡す。ここに指定されたグループのリアクションロール関連の物を全て削除する

        group: str


        別名: dr
        """
        
        mes = await ctx.send('このコマンドを実行すると指定されたグループに関する情報を全て削除します。それでも良ければ下のリアクションを押してください。')
        await mes.add_reaction('\U0001f44c')
        
        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) == '\U0001f44c'

        try:
        
            reaction, user = await self.bot.wait_for('reaction_add', check = check, timeout = 60.0)
        except asyncio.TimeoutError:
            return

        counter = 1

        async for mes in channel.history(limit = None):
            if embed := mes.embeds:
                for e in embed:
                    if embed.title != group:
                        continue
                    
                    await mes.delete()

        self.reaction_role[str(ctx.guild.id)].pop(group)
        date.save(self.reaction_role, 'reaction_role')

        await ctx.send('処理が正常に終了しました')

    @del_react.error
    async def del_react_error(self, ctx, error):
        await ctx.send(f'```py\n{traceback.format_exc()}\n```')


    


def setup(bot):
    bot.add_cog(Reaction_Role(bot))