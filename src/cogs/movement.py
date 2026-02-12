import esper
import discord

from ecs.components.labels import Label, Name
from ecs.components.tags import LocationTag
from ecs.components.movement import MoveState

from ecs.exceptions import PathfindingError

from ecs.api.labels import entities_by_name
from ecs.api.discord import get_user_entity
from ecs.api.movement import pathfind, move, get_node_entity


class Movement(discord.Cog):
    @discord.slash_command()
    async def goto(self, ctx: discord.ApplicationContext, location_name, movestate = "walk"): # pyright: ignore[reportGeneralTypeIssues]
        location_name, movestate = Name(location_name), MoveState.from_str(movestate)
        user_ent = get_user_entity(ctx.user.id)
        locs = {loc for loc in entities_by_name(location_name) if esper.has_component(loc, LocationTag)}
        
        if len(locs) == 0:
            await ctx.respond(f"No locations found with name {location_name}")
            return
        
        try:
            dest, = locs
        except ValueError:
            dest = await self.choose_destination(ctx, locs)
        
        pos = get_node_entity(user_ent)
        
        try:
            path = pathfind(pos, dest)
        except PathfindingError as e:
            await ctx.respond(e)
            return

        move(user_ent, movestate, *(esper.component_for_entity(loc, Label) for loc in path))
            
    @staticmethod
    async def choose_destination(ctx: discord.ApplicationContext, locations: set[int]) -> int:
        # TODO: Implement a followup where user selects its desired destination from locations
        await ctx.respond("Go fuck yourself")
        return 228
        ...
