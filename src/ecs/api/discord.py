from ..components.labels import Label, LabelEntityMap
from ..components.discord import DiscordIDLabelMap
from ..utils import get_singleton_component

from ..api.labels import create_labeled_entity

def get_user_label(discord_id: int):
    label_map = get_singleton_component(DiscordIDLabelMap).map
    return label_map[discord_id]

def get_user_entity(discord_id: int) -> int:
    label = get_user_label(discord_id)
    entity_map = get_singleton_component(LabelEntityMap).map
    return entity_map[label]

def create_user_entity(discord_id: int, *comps) -> tuple[int, Label]:
    ent, label = create_labeled_entity(*comps)
    label_map = get_singleton_component(DiscordIDLabelMap).map
    label_map[discord_id] = label
    return ent, label

    
