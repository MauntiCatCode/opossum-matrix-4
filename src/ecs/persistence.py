import esper

import jsonpickle as jp

from components.tags import NonPersistent
from utils import add_new_entity

def get_all_persistent_components():
    component_lists = []
    for ent in esper._entities.values():
        if NonPersistent in ent.keys():
            continue
        
        component_lists.append(
            [c for ct, c in ent.items()
             if not issubclass(ct, NonPersistent)]
        )
    
    return component_lists

def save_entities(path):
    with open(path, 'w') as f:
        f.write(str(jp.encode(get_all_persistent_components(), keys=True, indent=2)))

def load_entities(path):
    with open(path, 'r') as f:
        complists = jp.decode(f.read(), keys=True)

    for comps in complists:
        add_new_entity(*comps)
        



    