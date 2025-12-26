import esper
from bidict import bidict


from components.labels import Label, LabelEntityMap
from components.tags import NewEntity


class LabelEntityMapSystem(esper.Processor):
    def __init__(self, singleton_entity: int = 1):
        self._label_map = bidict()
        esper.add_component(singleton_entity, LabelEntityMap(self._label_map))
        # Build map at init to allow label references at first tick
        self._add_new_entities()
    
    def process(self):
        self._add_new_entities()
        self._remove_dead_entities()

    def _add_new_entities(self):
        for ent, (lb, _) in esper.get_components(Label, NewEntity):
            self._label_map[lb] = ent
            esper.remove_component(ent, NewEntity)

    def _remove_dead_entities(self):
        for ent in esper._dead_entities:
            try:
                del self._label_map.inv[ent]
            except KeyError:
                continue