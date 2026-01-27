from uuid import UUID
from dataclasses import dataclass

from .tags import NonPersistent, Registrable

@dataclass(frozen=True)
class Label(Registrable):
    id: UUID

@dataclass
class Name(Registrable):
    value: str

@dataclass
class DiscordID(Registrable):
    id: int

@dataclass
class EntityRegistry(NonPersistent):
    maps: dict[type[Registrable], dict[Registrable, int]]

@dataclass
class Description:
    value: str


