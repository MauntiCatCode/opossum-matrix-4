import esper
import jsonpickle as jp

from ..components.labels import Label
from ..components.tags import NonPersistent, UnregisteredLabel

def _get_all_persistent_components():
    component_lists = []
    for ent in esper._entities.values():
        if NonPersistent in ent.keys():
            continue
        
        component_lists.append(
            [c for ct, c in ent.items()
             if not issubclass(ct, NonPersistent)]
        )
    
    return component_lists

def save_entities(path) -> int:
    complists = _get_all_persistent_components()
    
    with open(path, 'w') as f:
        f.write(str(jp.encode(complists, keys=True, indent=2)))

    return len(complists)

def load_entities(path) -> int:
    with open(path, 'r') as f:
        complists = jp.decode(f.read(), keys=True)

    for comps in complists:
        ent = esper.create_entity(*comps)
        if esper.has_component(ent, Label):
            esper.add_component(ent, UnregisteredLabel)
        
    return len(complists)
        



    