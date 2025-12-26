from dataclasses import dataclass
from collections import deque

from enums import MoveState
from .labels import Label


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
class MovementState:
    state: MoveState

@dataclass
class AllowedMoveStates:
    states: set[MoveState]

@dataclass
class BaseVelocityMap:
    magnitude_map: dict[MoveState, float]