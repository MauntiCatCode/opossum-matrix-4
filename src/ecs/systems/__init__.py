import esper as _esper

from .label_entity_map import LabelEntityMapSystem
from .movement import MovementSystem
from .time import TimeSystem
from .velocity import VelocitySystem
from .regions import RegionsSystem

ALL_SYSTEMS: list[type[_esper.Processor]] = [
    LabelEntityMapSystem,
    TimeSystem,
    RegionsSystem,
    VelocitySystem,
    MovementSystem
]

def init_systems(systems: list[type[_esper.Processor]], *args, **kwargs):
    for i, sys in enumerate(systems):
        _esper.add_processor(
            sys(*args, **kwargs),
            priority=len(systems)-i
            )