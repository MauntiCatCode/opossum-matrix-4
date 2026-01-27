from ..components.labels import Label, DiscordID, EntityRegistry
from ..utils import get_singleton_component

from .labels import create_labeled_entity

def get_user_entity(discord_id: int) -> int:
    return get_singleton_component(EntityRegistry).maps[DiscordID][discord_id]

def create_user_entity(discord_id: int, *comps) -> tuple[int, Label]:
    ent, label = create_labeled_entity(*comps)
    return ent, label

    
