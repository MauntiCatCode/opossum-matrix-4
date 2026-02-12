from dataclasses import dataclass

from .movement import MoveState


@dataclass
class VelocityMod:
    coefficients: dict[MoveState, float]