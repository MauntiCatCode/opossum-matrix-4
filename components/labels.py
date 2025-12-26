from bidict import bidict
from typing import Hashable
from dataclasses import dataclass

from .tags import NonPersistent


@dataclass(frozen=True)
class Label:
    label: Hashable

@dataclass
class LabelEntityMap(NonPersistent):
    map: bidict[Label, int]

@dataclass
class Name:
    name: str

@dataclass
class Description:
    text: str


