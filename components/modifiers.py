from dataclasses import dataclass

from enums import MoveState


@dataclass
class VelocityMod:
    coefficients: dict[MoveState, float]