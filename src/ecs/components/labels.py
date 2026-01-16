from bidict import bidict
from uuid import UUID
from dataclasses import dataclass

from .tags import NonPersistent

@dataclass(frozen=True)
class Label:
    id: UUID

@dataclass
class LabelEntityMap(NonPersistent):
    map: bidict[Label, int]

@dataclass
class Name:
    value: str

@dataclass
class Description:
    value: str


