from dataclasses import dataclass

from .labels import Label

@dataclass
class DiscordIDLabelMap:
    map: dict[int, Label]


