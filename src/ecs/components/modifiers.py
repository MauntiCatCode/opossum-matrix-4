from dataclasses import dataclass

from ecs.enums import MoveState


@dataclass
class VelocityMod:
    coefficients: dict[MoveState, float]