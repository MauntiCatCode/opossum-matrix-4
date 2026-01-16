import esper

from uuid import uuid1, uuid4
from datetime import datetime

from enums import MoveState
from components.labels import Label
from components.regions import Regions, Node, Length, Links 
from components.tags import UnregisteredLabel
from components.movement import AllowedMoveStates, BaseVelocityMap
from components.time import GlobalTime, DeltaTime
from components.modifiers import VelocityMod

def new_labels(n: int) -> tuple[Label, ...]:
    return tuple(Label(uuid1()) for i in range(n))

PLAYER, LINK, NODE_A, NODE_B, REGION_A, REGION_B = new_labels(6)

def create_test_entities():
    esper.create_entity(
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