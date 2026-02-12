import esper

from uuid import uuid1

from ..components.labels import Label, Name, EntityRegistry
from ..components.tags import Unregistered
from ..utils import get_singleton_component

def entities_by_name(name: Name) -> set[int]:
    try:
        return get_singleton_component(EntityRegistry).maps[Name][name]
    except KeyError:
        return set()

def entity_by_label(label: Label) -> int:
    return get_singleton_component(EntityRegistry).maps[Label][label]

def label_exists(label: Label) -> bool:
    return label in get_singleton_component(EntityRegistry).maps[Label]

def create_labeled_entity(*comps) -> tuple[int, Label]:
    label = Label(uuid1())
    ent = esper.create_entity(*comps, label)
    esper.add_component(ent, Unregistered())

    return ent, label


    