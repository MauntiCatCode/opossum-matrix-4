import esper

from collections import deque

from ..components.movement import MoveState, AllowedMoveStates, Route, LinkProgress
from ..components.regions import Node, NextNode, Links
from ..components.tags import VelocityDue, LinkDue, LinkRegionsDue, EndRoute
from ..components.labels import Label, EntityRegistry

from ..utils import get_singleton_component
from ..exceptions import PathfindingError

from .labels import entity_by_label, label_exists

def move(entity: int, movestate: MoveState, *route: Label) -> bool:
    return change_movestate(entity, movestate) and start_route(entity, *route)

def pathfind(pos: int, dest: int, max_depth=8) -> list[int]:
    visited = set()
    queue = deque([(pos, [])])

    while queue:
        node, path = queue.pop()
        if node == dest:
            return path
        
        if len(path) > max_depth:
            raise PathfindingError(f"Max pathfinding depth of {max_depth} exceeded on {path}")
        if node in visited:
            continue
        visited.add(node)
        
        neighbors = esper.component_for_entity(node, Links).map
        
        for loc in neighbors.keys():
            loc = entity_by_label(loc)
            path_to_loc = path.copy()
            path_to_loc.append(loc)
            queue.append((loc, path_to_loc))
    
    raise PathfindingError(f"No path found from {pos} to {dest}")

def get_node_entity(ent: int) -> int:
    registry = get_singleton_component(EntityRegistry).map[Label]
    node = esper.component_for_entity(ent, Node).label
    return registry[node]

def movestate_valid(entity: int, movestate: MoveState) -> bool:
    allowed = esper.try_component(entity, AllowedMoveStates) or False
    return allowed and movestate in allowed.states

def set_movestate(ent: int, state: MoveState):
    esper.add_component(ent, state)

    # Signal to VelocitySystem
    esper.add_component(ent, VelocityDue())

def change_movestate(ent: int, state: MoveState) -> bool:
    if not movestate_valid(ent, state):
        return False
    
    set_movestate(ent, state)
    return True

def set_route(ent: int, *route: Label):    
    esper.add_component(ent, Route(deque(route)))
    esper.add_component(ent, NextNode(route[0]))
    esper.add_component(ent, LinkProgress(0.0))
    
    # Signal to RegionsSystem
    esper.add_component(ent, LinkDue())
    esper.add_component(ent, LinkRegionsDue())

def route_exists(*route: Label) -> bool:
    return all(label_exists(r) for r in route)

def start_route(ent: int, *route: Label) -> bool:
    if not route_exists():
        return False 
    
    if any((
        esper.has_component(ent, Route),
        esper.has_component(ent, NextNode),
        esper.has_component(ent, LinkProgress)
        )):
        return False
    
    set_route(ent, *route)
    return True

def end_route(ent: int):
    esper.add_component(ent, EndRoute())