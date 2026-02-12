import esper

from ..components.movement import Velocity, MoveState, BaseVelocityMap
from ..components.modifiers import VelocityMod
from ..components.regions import Regions
from ..components.tags import VelocityDue
from ..api.labels import entity_by_label
from ..utils import untag_all
from ..exceptions import MovementError


class VelocitySystem(esper.Processor):
    def process(self):
        self._set_base_velocities()
        self._apply_regional_mods()
        untag_all(VelocityDue)

    def _apply_regional_mods(self):
        for ent, (v, rg, state, _) in esper.get_components(Velocity, Regions, MoveState, VelocityDue):
            for r in rg.regions:
                try:
                    mod = esper.component_for_entity(entity_by_label(r), VelocityMod)
                    v.magnitude *= mod.coefficients[state]
                
                except KeyError:
                    continue
                
    def _set_base_velocities(self):
        for ent, (state, v_map, _) in esper.get_components(MoveState, BaseVelocityMap, VelocityDue):
            try:
                v = v_map.magnitude_map[state]
            
            except KeyError:
                raise MovementError(f"Entity {ent}: {state} not in {v_map}")
            
            else:
                esper.add_component(ent, Velocity(v))