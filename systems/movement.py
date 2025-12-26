import esper

from components.movement import Route, MovementState, Velocity, LinkProgress
from components.regions import Regions, Node, NextNode, Link, Length
from components.tags import AdvanceRoute, EndRoute, VelocityDue, LinkDue, NodeRegionsDue, LinkRegionsDue
from components.labels import LabelEntityMap
from components.time import DeltaTime

from utils import untag_all, try_remove_components


class MovementSystem(esper.Processor):
    OWNED_COMPONENTS = {
        Route,
        NextNode,
        MovementState,
        Velocity,
        Link,
        LinkProgress,
        # Tags
        EndRoute,
        AdvanceRoute,
        VelocityDue,
        LinkDue,
        LinkRegionsDue
    }

# --- Processor implementation ---
    def __init__(self, singleton_entity: int = 1):
        self._delta_time = esper.component_for_entity(singleton_entity, DeltaTime)
        self._label_map = esper.component_for_entity(singleton_entity, LabelEntityMap).map

    def process(self):
        self._end_routes()
        self._update_link_progress()
        self._advance_routes()
        untag_all(AdvanceRoute)

    def _end_routes(self):
        for ent, _ in esper.get_component(EndRoute):
            try_remove_components(ent, *self.OWNED_COMPONENTS)
            # Signal to RegionsSystem
            esper.add_component(ent, NodeRegionsDue())

    def _update_link_progress(self):
        dt = self._delta_time.dt
        for ent, (v, link, prog) in esper.get_components(Velocity, Link, LinkProgress):
            if link.length > 0:
                dp = v.magnitude * dt / link.length
                prog.percent += dp
            else:
                prog.percent = 1
                
            if prog.percent >= 1:
                prog.percent = 0
                # Signal to self._advance_routes()
                esper.add_component(ent, AdvanceRoute())

    def _advance_routes(self):
        for ent, (route, node, nxt, _) in esper.get_components(Route, Node, NextNode, AdvanceRoute):
            try:
                route.nodes.popleft()
                node.label = nxt.label
                nxt.label = route.nodes[0]

            except IndexError:
                esper.add_component(ent, EndRoute())
                continue

            # Signal to RegionsSystem
            esper.add_component(ent, LinkDue())
            esper.add_component(ent, LinkRegionsDue())
            
            # Signal to VelocitySystem
            esper.add_component(ent, VelocityDue())

            # Clean up stale data
            esper.remove_component(ent, Link)
            esper.remove_component(ent, Regions)
            esper.remove_component(ent, Velocity)

    
    


