"""
The MIT License (MIT)

Copyright (c) 2018 PapyrusThePlant

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""

from discord.ext import commands
from config import date
import json
import discord
import youtube_dl
import os
import random
import asyncio
import pathlib
import functools
import traceback






class MusicError(commands.UserInputError):
    pass


def duration_to_str(duration):
    # Extract minutes, hours and days
    minutes, seconds = divmod(duration, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)

    # Create a fancy string
    duration = []
    if days > 0: duration.append(f'{days}日')
    if hours > 0: duration.append(f'{hours}時間')
    if minutes > 0: duration.append(f'{minutes}分')
    if seconds > 0 or len(duration) == 0: duration.append(f'{seconds}秒')

    return ', '.join(duration)


class Song(discord.PCMVolumeTransformer):
    def __init__(self, song_info):
        self.info = song_info.info
        self.requester = song_info.requester
        self.channel = song_info.channel
        self.filename = song_info.filename
        super().__init__(discord.FFmpegPCMAudio(self.filename, before_options='-nostdin', options='-vn'))


class SongInfo:
    ytdl_opts = {
        'default_search': 'auto',
        'format': 'bestaudio/best',
        'ignoreerrors': True,
        'source_address': '0.0.0.0', # Make all connections via IPv4
        'nocheckcertificate': True,
        'restrictfilenames': True,
        'logtostderr': False,
        'no_warnings': True,
        'quiet': True,
        'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
        'noplaylist': True
    }
    ytdl = youtube_dl.YoutubeDL(ytdl_opts)

    def __init__(self, info, requester, channel):
        self.info = info
        self.requester = requester
        self.channel = channel
        self.filename = info.get('_filename', self.ytdl.prepare_filename(self.info))
        self.downloaded = asyncio.Event()
        self.local_file = '_filename' in info
        

    @classmethod
    async def create(cls, query, requester, channel, loop=None):
        try:
            # Path.is_file() can throw a OSError on syntactically incorrect paths, like urls.
            if pathlib.Path(query).is_file():
                return cls.from_file(query, requester, channel)
        except OSError:
            pass

        return await cls.from_ytdl(query, requester, channel, loop=loop)

    @classmethod
    def from_file(cls, file, requester, channel):
        path = pathlib.Path(file)
        if not path.exists():
            raise MusicError(f'File {file} not found.')

        info = {
            '_filename': file,
            'title': path.stem,
            'creator': 'local file',
        }
        return cls(info, requester, channel)

    @classmethod
    async def from_ytdl(cls, request, requester, channel, loop=None):
        loop = loop or asyncio.get_event_loop()

        # Get sparse info about our query
        partial = functools.partial(cls.ytdl.extract_info, request, download=False, process=False)
        sparse_info = await loop.run_in_executor(None, partial)

        if sparse_info is None:
            raise MusicError(f'情報の取得に失敗しました。 : {request}')

        # If we get a playlist, select its first valid entry
        if "entries" not in sparse_info:
            info_to_process = sparse_info
        else:
            info_to_process = None
            for entry in sparse_info['entries']:
                if entry is not None:
                    info_to_process = entry
                    break
            if info_to_process is None:
                raise MusicError(f'情報の取得に失敗しました。 : {request}')

        # Process full video info
        url = info_to_process.get('url', info_to_process.get('webpage_url', info_to_process.get('id')))
        partial = functools.partial(cls.ytdl.extract_info, url, download=False)
        processed_info = await loop.run_in_executor(None, partial)

        if processed_info is None:
            raise MusicError(f'情報の取得に失敗しました。 : {request}')

        # Select the first search result if any
        if "entries" not in processed_info:
            info = processed_info
        else:
            info = None
            while info is None:
                try:
                    info = processed_info['entries'].pop(0)
                except IndexError:
                    raise MusicError(f'情報の取得に失敗しました。 : {info_to_process["url"]}')

        return cls(info, requester, channel)

    async def download(self, loop):
        if not pathlib.Path(self.filename).exists():
            partial = functools.partial(self.ytdl.extract_info, self.info['webpage_url'], download=True)
            self.info = await loop.run_in_executor(None, partial)
        self.downloaded.set()

    async def wait_until_downloaded(self):
        await self.downloaded.wait()

    def to_embed(self) -> discord.Embed:
        title = f"[{self.info['title']}](https://www.youtube.com/watch?v={self.info['id']})"
        uploader = f"{self.info['uploader']}"
        creator = f"{self.info.get('creator')}"
        duration = f"{duration_to_str(self.info['duration'])}" if 'duration' in self.info else ''

        embed = discord.Embed()
        embed.set_thumbnail(url=f"http://i.ytimg.com/vi/{self.info['id']}/default.jpg")
        embed.description = title
        embed.add_field(name='チャンネル', value=uploader)
        if self.info.get('creator') is not None:
            embed.add_field(name='クリエイター', value=creator)
        embed.add_field(name='曲の長さ', value=duration)
        return embed

    def __str__(self):
        title = f"**{self.info['title']}**"
        creator = f"**{self.info.get('creator') or self.info['uploader']}**"
        duration = f" (duration: {duration_to_str(self.info['duration'])})" if 'duration' in self.info else ''
        return f'{title} from {creator}{duration}'


class Playlist(list):
    def __iter__(self):
        return super().__iter__()

    def __init__(self, maxsize):
        super().__init__()
        self.maxsize = maxsize
        self._qsize = 0

    def clear(self):
        for song in self:
            try:
                os.remove(song.filename)
            except:
                pass
        super().clear()

    def get_song(self):
        self._qsize -= 1
        return super().pop(0)

    def add_song(self, item):
        if len(self) < self.maxsize:
            self.append(item)
            self._qsize += 1
      

    def remove_song(self, index):
        if index < len(self):
            del self[index]
            self._qsize -= 1
        else:
            raise IndexError('その番号はプレイリストに登録されていません。')

    def remove(self, value):
        if self._qsize > 0:
            self._qsize -= 1
        self.remove(value)

    def shuffle(self):
        random.shuffle(self)

    def empty(self):
        return not self

    def qsize(self):
        return self._qsize

    def to_embed(self) -> discord.Embed:
        embed = discord.Embed()
        embed.set_author(name='現在のプレイリスト')
        if self:
            count = 1
            for song in self:
                embed.add_field(
                    name=f'**#{count}** {song.info["title"]}',
                    value=(f'投稿者: {song.info["uploader"]}\n'
                    f'曲の長さ: {duration_to_str(song.info["duration"])}\n'
                    f'[リンク]({song.info["url"]})'
                    )
                )
                count += 1
        else:
            embed.description = 'プレイリストは空です。'

        return embed

class GuildMusicState:
    def __init__(self, loop):
        self.playlist = Playlist(maxsize=50)
        self.voice_client = None
        self.loop = loop
        self.player_volume = 0.5
        self.skips = set()
        self.min_skips = 5
        self.is_repeat = False
        self.previous_song = None
        
        
    @property
    def current_song(self):
        return self.voice_client.source

    @property
    def volume(self):
        return self.player_volume

    @volume.setter
    def volume(self, value):
        self.player_volume = value
        if self.voice_client:
            self.voice_client.source.volume = value

    async def stop(self):
        self.playlist.clear()
        if self.voice_client:
            await self.voice_client.disconnect()
            self.previous_song = None
            self.voice_client = None

    def is_playing(self):
        return self.voice_client and self.voice_client.is_playing()

    async def play_next_song(self, song=None, error=None):
        if error:
            await self.current_song.channel.send(f'{self.current_song}を再生中にエラーが発生しました: {error}')

        if self.previous_song is not None and self.is_repeat:
            self.playlist.add_song(self.previous_song)

        if song and not song.local_file and song.filename not in [s.filename for s in self.playlist]:
            os.remove(song.filename)

        if self.playlist.empty():
            await self.stop()
        
        else:
            next_song_info = self.playlist.get_song()
            self.previous_song = next_song_info
            await next_song_info.wait_until_downloaded()

            try:
                source = Song(next_song_info)
            except Exception as error:
                print(type(error).__name__, str(error))

            source.volume = self.player_volume
            
            self.voice_client.play(source, after=lambda e: asyncio.run_coroutine_threadsafe(self.play_next_song(next_song_info, e), self.loop).result())
            
            embed: discord.Embed = next_song_info.to_embed()
            embed.set_author(name='この曲を再生しています', icon_url=next_song_info.requester.avatar_url)
            await next_song_info.channel.send(embed=embed)
            


class Music(commands.Cog):
    """音楽関係のコマンド群。"""
    def __init__(self, bot):
        self.bot = bot
        self.music_states = {}
        self.lj = date.load
        self.sj = date.save
        self.volume = self.lj('volume')
        self.manage = self.lj('manage')
     
     
    
    


    def __unload(self):
        for state in self.music_states.values():
            self.bot.loop.create_task(state.stop())

    async def cog_check(self, ctx):
        server_id = str(ctx.guild.id)
        try:
            if self.manage[server_id]['role_id']  not in [y.id for y in author.roles]:
                await ctx.send('貴方はこのコマンドを実行する権限がありません。')
        except KeyError:
            pass
        except AttributeError:
            pass

        if not ctx.guild:
            raise commands.NoPrivateMessage('このコマンドはDMでは使用できません。')
        return True

    async def cog_before_invoke(self, ctx):
        guild_id = ctx.guild.id
        ctx.music_state = self.get_music_state(guild_id)
        try:
            ctx.music_state.volume = int(self.mj[str(guild_id)]['volume']) / 100
        except:
            pass
    async def __error(self, ctx, error):
        if not isinstance(error, commands.UserInputError):
            raise error

        try:
            await ctx.send(error)
        except discord.Forbidden:
            pass # /shrug

    def get_music_state(self, guild_id):
        return self.music_states.setdefault(guild_id, GuildMusicState(self.bot.loop))

    @commands.command(aliases =["sta"])
    async def status(self, ctx):
        """現在再生中の曲を表示します。"""
        if ctx.music_state.is_playing():
            song = ctx.music_state.current_song
            await ctx.send(f'{ctx.voice_client.channel.mention}で{song.name}を再生中。 音量は{song.volume * 100}%です。')
        else:
            await ctx.send('再生中の曲はありません。')

    @commands.group(invoke_without_command = True)
    async def playlist(self, ctx):
        """
        プレイリストの操作に関するコマンド群。
        サブコマンドの指定が必要です。
        """
        member = ctx.author
        e = discord.Embed(
            title = 'サブコマンドが見つかりません。',
            color = member.color,
            timestamp = ctx.message.created_at
        )
        
        e.set_author(
            name = member.name, 
            icon_url = ctx.author.avatar_url
        )
        e.add_field(
            name = f'エラー名',
            value = 'サブコマンドが足りません。',
            inline = True
        )
        e.add_field(
            name = '入力方法',
            value = 'afp:(Prefix)コマンド　サブコマンド',
            inline = True
        )
        await ctx.send(embed = e)
            

    @playlist.command(aliases = ["sh"])
    async def show(self, ctx):
        """現在のプレイリストを表示します。
        
        別名: sh
        """
        await ctx.send(embed=ctx.music_state.playlist.to_embed())

    @playlist.command(aliases =["sf"])
    async def shuffle(self, ctx):
        """プレイリストをシャッフルします。
        
        別名: sf
        """
        ctx.music_state.playlist.shuffle_queue()

    @playlist.command(aliases = ["ir"])
    async def remove(self, ctx, index: int):
        """指定されたインデックスの曲を削除します。
        
        別名: ir
        """
        ctx.music_state.playlist.remove_song(index)

    @playlist.command(aliases = ["rp"])
    async def repeat(self, ctx, enable: bool):
        "プレイリスト内の音楽をリピート再生します。"
        if enable:
            await ctx.send('リピート再生を有効にしました。')
        else:
            await ctx.send('リピート再生を無効にしました。')
        ctx.music_state.is_repeat = enable

    @commands.command(aliases = ["j"])
    async def joinvc(self, ctx, *, channel: discord.VoiceChannel = None):
        """ボイスチャンネルにBotを呼び出します。
        チャンネルが指定されていない場合、実行者が現在いるチャンネルに参加します。

        別名: j
        """
        if channel is None and not ctx.author.voice:
            raise MusicError('貴方がボイスチャンネルに接続していないため、接続できません。')

        destination = channel or ctx.author.voice.channel

        if ctx.voice_client:
            await ctx.voice_client.move_to(destination)
        else:
            ctx.music_state.voice_client = await destination.connect()


    @commands.command(aliases = ["p"])
    async def play(self, ctx, *, request: str = None):
        """プレイリストに曲を追加し、再生します。
        このBOTがボイスチャンネルに居なくても実行可能
        youtube_dlにより自動検索が可能です。
        サポートしているサイトは[こちら](https://github.com/rg3/youtube-dl/blob/1b6712ab2378b2e8eb59f372fb51193f8d3bdc97/docs/supportedsites.md)で確認できます。

        別名: p
        """
        await ctx.message.add_reaction('\N{HOURGLASS}')
    
        if request is None:
            await ctx.send("再生する曲が指定されていません。")
        # Create the SongInfo
        song = await SongInfo.create(request, ctx.author, ctx.channel, loop=ctx.bot.loop)

        # Connect to the voice channel if needed
        if ctx.voice_client is None or not ctx.voice_client.is_connected():
            await ctx.invoke(self.join)

        # Add the info to the playlist
        try:
            ctx.music_state.playlist.add_song(song)
        except asyncio.QueueFull:
            raise MusicError('再生リストがいっぱいです。しばらくしてからもう一度お試しください。')

        if not ctx.music_state.is_playing():
            # Download the song and play it
            await song.download(ctx.bot.loop)
            await ctx.music_state.play_next_song()
        else:
            # Schedule the song's download
            ctx.bot.loop.create_task(song.download(ctx.bot.loop))
            embed = song.to_embed()
            embed.add_field(name='プレイリスト', value=f'#{ctx.music_state.playlist.qsize()}')
            embed.set_author(name='プレイリストに追加しました', icon_url=song.requester.avatar_url)
            await ctx.send(embed=embed)
            

        await ctx.message.remove_reaction('\N{HOURGLASS}', ctx.me)
        await ctx.message.add_reaction('\N{WHITE HEAVY CHECK MARK}')

    @play.error
    async def play_error(self, ctx, error):
        print(type(error).__name__, str(error))
        await ctx.message.remove_reaction('\N{HOURGLASS}', ctx.me)
        await ctx.message.add_reaction('\N{CROSS MARK}')
        await ctx.send(f'```py\n{traceback.format_exc()}\n```')

    @commands.command(aliases =["pa"])
    async def pause(self, ctx):
        """曲の再生を一時停止します。
        
        別名: pa
        """
        if ctx.voice_client:
            ctx.voice_client.pause()

    @commands.command(aliases =["rs"])
    async def resume(self, ctx):
        """曲の再生を再開します。
        
        別名: rs
        """
        if ctx.voice_client:
            ctx.voice_client.resume()

    @commands.command(aliases=["s"])
    async def stop(self, ctx):
        """曲の再生を停止し、ボイスチャンネルから退出します。
        また、同時にプレイリストの中身が削除されます。
        
        別名: s
        """
        await ctx.music_state.stop()

    @commands.command(aliases=["v"])
    async def set_volume(self, ctx, volume: int = None):
        """ボリュームを設定します。
        
        別名: v
        """
        if volume is None:
            await ctx.send('ボリュームを入力して下さい。')
            return
            
        if volume < 0 or volume > 200:
            #await ctx.send()に変更
            raise MusicError('設定できるボリュームの範囲は1~200です。')
        
        ctx.music_state.volume = volume / 100
        guild_id = str(ctx.guild.id)
        
        try:
            self.volume[guild_id] = {}
            self.volume[guild_id]['server_name'] = ctx.guild.name
            self.volume[guild_id]['volume'] = str(volume)
        except TypeError:
            await ctx.send('設定に失敗しました。もう一度お試しください。')
        else:
            await ctx.send('設定が完了しました。')

        self.sj(self.volume, 'volume')
        
        
    @commands.command(aliases=["cl"])
    async def clear(self, ctx):
        """プレイリストをクリアします。
        
        別名: cl
        """
        ctx.music_state.playlist.clear()

    @commands.command(aliases=["sk"])
    async def skip(self, ctx):
        """現在再生中の曲をスキップする投票を行います。
        `minskips`コマンドで、スキップに必要な最低投票数を設定できます。

        別名: sk
        """
      
        # Check if the song has to be skipped
        ctx.music_state.skips.clear()
        ctx.voice_client.stop()
        
            


def setup(bot):
    bot.add_cog(Music(bot))
