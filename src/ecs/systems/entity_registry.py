import esper

from collections import defaultdict

from ..components.labels import Label, Name, DiscordID, EntityRegistry
from ..components.tags import Registrable, Unregistered
from ..utils import untag_all


class EntityRegistrySystem(esper.Processor):
    def __init__(self):
        self._dead_entities: set[int] = set()
        self._maps = {Label: {}, DiscordID: {}, Name: defaultdict(set)}

        esper.set_handler("kill_entity", self.kill_entity)
        esper.add_component(1, EntityRegistry(self._maps))
        # Build maps at init to allow references at first tick
        self.process()
    
    def process(self):
        self._add_new_entities()
        self._remove_dead_entities()
        untag_all(Unregistered)

    def kill_entity(self, ent: int):
        self._dead_entities.add(ent)

    def _add_new_entities(self):
        for ent, (lb, _) in esper.get_components(Label, Unregistered):
            if lb in self._maps[Label]:
                # Should we add events/logging here?
                continue
            self._maps[Label][lb] = ent
        
        for ent, (user, _) in esper.get_components(DiscordID, Unregistered):
            if user in self._maps[DiscordID]:
                continue
            self._maps[DiscordID][user] = ent
        
        for ent, (nm, _) in esper.get_components(Name, Unregistered):
            self._maps[Name][nm].add(ent)
        
    def _remove_dead_entities(self):
        for ent in self._dead_entities:
            self._try_delete_entries(ent, Label, DiscordID, Name)
        self._dead_entities = set()
    
    def _try_delete_entries(self, ent: int, *component_types: type[Registrable]):
        for ct in component_types:
            try:
                c = esper.component_for_entity(ent, ct)
                del self._maps[ct][c]
            
            except KeyError:
                continue
