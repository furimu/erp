from discord.ext import commands
import discord
import traceback
class Multi_Eroype_Server(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):
        return ctx.guild.id == 695801973127118899


    @commands.command()
    @commands.has_permissions(manage_messages = True)
    async def purge(self, ctx, channel: discord.TextChannel, limit: int = None):
        """指定されたチャンネルのメッセージを一括削除
        引数に指定されたチャンネルを作成\n limitに指定された数を削除

        channel: 名前・ID・メンション
        limit: int = None 
        """
        if channel is None:
            channel= ctx.channel

        await channel.purge(limit = limit)


    
    @commands.Cog.listener()
    async def on_message(self, message):
        channel = self.bot.get_channel(696611907712319488)

        if message.channel.id in [696064895107465389, 696064931375611924]:
            counter = 0
            async for mes in message.channel.history(limit=None):
                if mes.author == message.author:
                    counter += 1

            if counter != 1:
                return

            await channel.send(f'{message.author}さんがプロフィールを新規に記入しました。下のURLをクリックすると実際のメッセージに移動する事が出来ます。\n{message.jump_url}')
            boy_profile = discord.utils.get(message.guild.roles, name='男性')
            girl_profile = discord.utils.get(message.guild.roles, name='女性')
            boy_mention = discord.utils.get(message.guild.roles, name='男性宛')
            girl_mention = discord.utils.get(message.guild.roles, name='女性宛')
            not_profile = discord.utils.get(message.guild.roles, name='not profile')
            
            if message.channel.id == 696064895107465389:
                await message.author.add_roles(boy_profile)
                await message.author.add_roles(boy_mention)
                await message.author.remove_roles(not_profile)

            elif message.channel.id == 696064931375611924:
                await message.author.add_roles(girl_profile)
                await message.author.add_roles(girl_mention)
                await message.author.remove_roles(not_profile)
                
    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        channel = self.bot.get_channel(696611907712319488)
        if before.channel.id not in [696064895107465389, 696064931375611924]:
            return

        elif before.content == after.content:
            return

        await channel.send(f'{message.author}さんがプロフィールを更新しました。下のURLをクリックすると実際のメッセージに移動する事が出来ます。\n{message.jump_url}')


def setup(bot):
    bot.add_cog(Multi_Eroype_Server(bot))