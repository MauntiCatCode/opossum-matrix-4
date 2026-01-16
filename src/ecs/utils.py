import esper

from components.labels import Label 
from components.tags import UnregisteredLabel


def try_remove_components(entity: int, *components: type):
    for c in components:
        if esper.has_component(entity, c):
            esper.remove_component(entity, c)

def untag_all(*tags: type):
    for tag in tags:
        for ent, _ in esper.get_component(tag):
            esper.remove_component(ent, tag)

def add_new_entity(*comps):
    ent = esper.create_entity(*comps)
    
    if esper.has_component(ent, Label):
        esper.add_component(ent, UnregisteredLabel)
