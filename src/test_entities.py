import esper

from uuid import uuid1 
from datetime import datetime

from ecs.enums import MoveState
from ecs.components.labels import Label
from ecs.components.discord import DiscordIDLabelMap
from ecs.components.regions import Regions, Node, Length, Links 
from ecs.components.tags import UnregisteredLabel
from ecs.components.movement import AllowedMoveStates, BaseVelocityMap
from ecs.components.time import GlobalTime, DeltaTime
from ecs.components.modifiers import VelocityMod

def new_labels(n: int) -> tuple[Label, ...]:
    return tuple(Label(uuid1()) for i in range(n))

PLAYER, LINK, NODE_A, NODE_B, REGION_A, REGION_B = new_labels(6)

def create_test_entities():
    esper.create_entity(
        DiscordIDLabelMap({}),
        GlobalTime(datetime(1987, 1, 1)),
        DeltaTime(0)
    )

    esper.create_entity(
        PLAYER,
        Node(NODE_B),
        AllowedMoveStates({
            MoveState.WALK,
            MoveState.RUN
        }),
        BaseVelocityMap({
            MoveState.WALK: 1,
            MoveState.RUN: 2
        }),
        UnregisteredLabel()
    )

    esper.create_entity(
        LINK,
        Length(1),
        Regions({REGION_A}),
        UnregisteredLabel()
    )

    esper.create_entity(
        NODE_A,
        Links({NODE_B: LINK}),
        Regions({REGION_B}),
        UnregisteredLabel()
    )
    esper.create_entity(
        NODE_B,
        Links({NODE_A: LINK}),
        Regions({REGION_B}),
        UnregisteredLabel()
    )

    # Regions
    esper.create_entity(
        REGION_A,
        VelocityMod({
            MoveState.WALK: 1,
            MoveState.RUN: 0.5
        })
    )
    esper.create_entity(
        REGION_B,
        VelocityMod({
            MoveState.WALK: 0.5,
            MoveState.RUN: 0.7
        })
    )

if __name__ == "__main__":
    from ecs.api.persistence import save_entities
    create_test_entities()
    save_entities("/home/meow/projects/opossum-matrix-4/data/world.json")