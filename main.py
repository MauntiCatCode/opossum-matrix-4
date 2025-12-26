import esper

from pathlib import Path
from time import sleep

from api.movement import start_route, change_movestate
from systems import LabelEntityMapSystem, TimeSystem, MovementSystem, VelocitySystem, RegionsSystem
from persistence import save_entities, load_entities

from components.labels import Label
from enums import MoveState

from test_entities import create_test_entities

create_test_entities()
#load_entities(Path(__name__).parent / "world.json")
save_entities(Path(__name__).parent / "world.json")

esper.add_processor(LabelEntityMapSystem(1), priority=5)
esper.add_processor(TimeSystem(1), priority=4)
esper.add_processor(RegionsSystem(1), priority=3)
esper.add_processor(VelocitySystem(1), priority=2)
esper.add_processor(MovementSystem(1), priority=1)

change_movestate(2, MoveState.WALK)
start_route(2, Label(5))

from rich import print

for i in range(10):
    esper.process()
    print(esper.components_for_entity(2))
    sleep(0.2)