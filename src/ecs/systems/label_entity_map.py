import esper
from bidict import bidict

from ..components.labels import Label, LabelEntityMap
from ..components.tags import UnregisteredLabel
from ..utils import untag_all


class LabelEntityMapSystem(esper.Processor):
    def __init__(self, singleton_entity: int):
        self._label_map: bidict[Label, int] = bidict()
        self._dead_entities: set[int] = set()
        esper.add_component(singleton_entity, LabelEntityMap(self._label_map))
        esper.set_handler("kill_entity", self.kill_entity)
        # Build map at init to allow references at first tick
        self.process()
    
    def process(self):
        self._add_new_entities()
        self._remove_dead_entities()
        untag_all(UnregisteredLabel)

    def kill_entity(self, ent: int):
        self._dead_entities.add(ent)
    
    def _add_new_entities(self):
        for ent, (lb, _) in esper.get_components(Label, UnregisteredLabel):
            if lb in self._label_map.keys():
                raise KeyError(f"Label {lb} already present in the LabelEntityMap.")
            self._label_map[lb] = ent

    def _remove_dead_entities(self):
        for ent in self._dead_entities:
            try:
                del self._label_map.inv[ent]
            except KeyError:
                continue
        
        self._dead_entities = set()
