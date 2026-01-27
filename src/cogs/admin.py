import discord

from pathlib import Path

from ecs.api.persistence import save_entities, load_entities

class Admin(discord.Cog):
    def __init__(self, data_path: Path) -> None:
        self.data_path = data_path
        self.world_file = data_path / "world.json"

    @discord.slash_command()
    async def save(self, ctx):
        save_entities(self.world_file)
        await ctx.respond(f"All entities saved to {self.world_file}")
    
    @discord.slash_command()
    async def load(self, ctx):
        quantity = load_entities(self.world_file)
        await ctx.respond(f"{quantity} Entities loaded from {self.world_file}")