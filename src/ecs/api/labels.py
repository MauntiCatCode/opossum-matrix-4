import esper

from uuid import uuid1

from ..components.labels import Label, LabelEntityMap
from ..components.tags import UnregisteredLabel

def label_exists(label: Label, singleton: int = 1):
    label_map = esper.component_for_entity(singleton, LabelEntityMap).map
    return label in label_map.keys()

def create_labeled_entity(*comps) -> tuple[int, Label]:
    label = Label(uuid1())
    ent = esper.create_entity(*comps, label)
    esper.add_component(ent, UnregisteredLabel())

    return ent, label


    