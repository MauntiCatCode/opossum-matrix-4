import discord

from pathlib import Path

class Bot(discord.Bot):
    def __init__(self, data_path: str | Path, description=None, *args, **options):
        super().__init__(description, *args, **options)
        self.data_path = Path(data_path).expanduser()
