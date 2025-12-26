--- Responsibilities ---

LabelMapSystem:
1. Tie labels and entities
2. Be valid and clean at the start of each tick

TimeSystem:
1. Keep track of global time
2. Keep track of delta time

MovementSystem:
1. Physically move entities from node to node
2. End movement
3. Keep track of the progress of an entity along its current route segment

VelocitySystem:
1. Dig up an entity's base velocity from its movement state
2. Apply velocity modifiers to the entity

RegionsSystem:
1. Assign node regions to entities at rest
2. Assign link regions to entities en route
3. Infer the current link from an entity's current Node and NextNode


