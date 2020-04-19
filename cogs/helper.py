from discord.ext import commands

class JapaneseHelpCommand(commands.DefaultHelpCommand):
    def __init__(self):
        super().__init__()
        self.commands_heading = "コマンド:"
        self.no_category = "その他"
        self.command_attrs["help"] = "コマンド一覧と簡単な説明"

    def get_ending_note(self):
        return ("コマンドの説明が見づらい？それなら、e!help <コマンド名>\n"
                "カテゴリーの説明は、 e!help <カテゴリ名>\n")