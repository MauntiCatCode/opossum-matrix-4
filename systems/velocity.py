import esper

from components.movement import Velocity, MovementState, BaseVelocityMap
from components.modifiers import VelocityMod
from components.labels import LabelEntityMap
from components.regions import Regions
from components.tags import VelocityDue

from utils import untag_all
from exceptions import MovementError


class VelocitySystem(esper.Processor):
    def __init__(self, singleton_entity: int = 1):
        self._label_map = esper.component_for_entity(singleton_entity, LabelEntityMap).map
    
    def process(self):
        self._set_base_velocities()
        self._apply_regional_mods()
        untag_all(VelocityDue)

    def _apply_regional_mods(self):
        for ent, (v, rg, move, _) in esper.get_components(Velocity, Regions, MovementState, VelocityDue):
            for r in rg.regions:
                try:
                    mod = esper.component_for_entity(self._label_map[r], VelocityMod)
                    v.magnitude *= mod.coefficients[move.state]
                
                except KeyError:
                    continue
                
    def _set_base_velocities(self):
        for ent, (move, v_map, _) in esper.get_components(MovementState, BaseVelocityMap, VelocityDue):
            try:
                v = v_map.magnitude_map[move.state]
            
            except KeyError:
                raise MovementError(f"Entity {ent}: {move.state} not in {v_map}")
            
            else:
                esper.add_component(ent, Velocity(v))