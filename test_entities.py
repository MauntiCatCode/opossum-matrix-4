import esper

from datetime import datetime

from enums import MoveState
from components.labels import Label
from components.regions import Regions, Node, Length, Links 
from components.tags import NewEntity
from components.movement import AllowedMoveStates, BaseVelocityMap
from components.time import GlobalTime, DeltaTime
from components.modifiers import VelocityMod

def create_test_entities():
    esper.create_entity(
        GlobalTime(datetime(1987, 1, 1)),
        DeltaTime(0)
    )

    esper.create_entity(
        Label(2),
        Node(Label(4)),
        AllowedMoveStates({
            MoveState.WALK,
            MoveState.RUN
        }),
        BaseVelocityMap({
            MoveState.WALK: 1,
            MoveState.RUN: 2
        }),
        NewEntity()
    )

    # Link
    esper.create_entity(
        Label(3),
        Length(1),
        Regions({Label(6)}),
        NewEntity()
    )

    # Nodes
    esper.create_entity(
        Label(4),
        Links({Label(5): Label(3)}),
        Regions({Label(7)}),
        NewEntity()
    )
    esper.create_entity(
        Label(5),
        Links({Label(4): Label(3)}),
        Regions({Label(7)}),
        NewEntity()
    )

    # Regions
    esper.create_entity(
        Label(6),
        VelocityMod({
            MoveState.WALK: 1,
            MoveState.RUN: 0.5
        })
    )
    esper.create_entity(
        Label(7),
        VelocityMod({
            MoveState.WALK: 0.5,
            MoveState.RUN: 0.7
        })
    )