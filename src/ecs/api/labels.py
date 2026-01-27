import esper

from uuid import uuid1

from ..components.labels import Label, EntityRegistry
from ..components.tags import Unregistered

from utils import get_singleton_component

def label_exists(label: Label):
    return label in get_singleton_component(EntityRegistry).maps[Label]

def create_labeled_entity(*comps) -> tuple[int, Label]:
    label = Label(uuid1())
    ent = esper.create_entity(*comps, label)
    esper.add_component(ent, Unregistered())

    return ent, label


    