from dataclasses import dataclass
from collections import deque
from enum import Enum

from .labels import Label

class MoveState(Enum):
    IDLE = 0
    WALK = 1
    RUN = 2

    @classmethod
    def from_str(cls, data: str):
        return cls[data.strip().upper()]

@dataclass
class Route:
    """
    Deque of future entity's nodes, starting with the next node
    """
    nodes: deque[Label]

@dataclass
class LinkProgress:
    percent: float

@dataclass
class Velocity:
    magnitude: float

@dataclass
class AllowedMoveStates:
    states: set[MoveState]

@dataclass
class BaseVelocityMap:
    magnitude_map: dict[MoveState, float]