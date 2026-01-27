import esper

from .exceptions import SingletonError

def try_remove_components(entity: int, *components: type):
    for c in components:
        if esper.has_component(entity, c):
            esper.remove_component(entity, c)

def untag_all(*tags: type):
    for tag in tags:
        for ent, _ in esper.get_component(tag):
            esper.remove_component(ent, tag)


def get_singleton_component(component_type: type):
    for ent, c in esper.get_component(component_type):
        return c
    raise SingletonError(f"Singleton component of type {component_type} not present in the ECS")