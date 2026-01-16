from dataclasses import dataclass, field

from .labels import Label


@dataclass
class Node:
    """
    A given entity's location (ID of a node entity) when it is at rest
    """
    label: Label 

@dataclass
class NextNode:
    """
    A moving entity's next Node id
    """
    label: Label

@dataclass
class Link:
    """
    A given moving entity's location (ID of a link entity)
    """
    label: Label
    length: int

@dataclass
class Length:
    length: int

@dataclass
class Links:
    # Map of nodes and links connected to them
    map: dict[Label, Label]

@dataclass
class Regions:
    regions: set[Label] = field(default_factory=set)