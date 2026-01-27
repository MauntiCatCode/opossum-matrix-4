import discord
import esper

from ecs.components.labels import Name
from ecs.api.discord import get_user_entity, create_user_entity

class Characters(discord.Cog):
    @discord.slash_command()
    async def create_character(self, ctx: discord.ApplicationContext, name: str):
        ent, label = create_user_entity(ctx.user.id)
        esper.add_component(ent, Name(name))
        await ctx.respond(f"Character {name} created successfully as Entity {ent} with label: {label}")

    @discord.slash_command()
    async def whoami(self, ctx):
        ent = get_user_entity(ctx.user.id)
        name = esper.component_for_entity(ent, Name).value
        await ctx.respond(name)