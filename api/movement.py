import esper

from collections import deque

from components.movement import MovementState, AllowedMoveStates, Route, Velocity, LinkProgress
from components.regions import NextNode, Link
from components.tags import VelocityDue, LinkDue, LinkRegionsDue, EndRoute
from components.labels import Label

from enums import MoveState
from .labels import label_exists

def movestate_valid(entity: int, movestate: MoveState) -> bool:
    allowed = esper.try_component(entity, AllowedMoveStates) or False
    return allowed and movestate in allowed.states

def set_movestate(ent: int, state: MoveState):
    if state_inst := esper.try_component(ent, MovementState):
        state_inst.state = state
    else:
        esper.add_component(ent, MovementState(state))

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
    if (esper.has_component(ent, Route)
        or esper.has_component(ent, NextNode)
        or esper.has_component(ent, LinkProgress)):
        return False
    
    set_route(ent, *route)
    return True

def end_route(ent: int):
    esper.add_component(ent, EndRoute())