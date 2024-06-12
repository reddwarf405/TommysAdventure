from __future__ import annotations

from typing import TYPE_CHECKING, Tuple, Optional

if TYPE_CHECKING:
    from engine import Engine
    from Entity import Entity


class Action:
    def __init__(self, entity: Entity) -> None:
        super().__init__()
        self.entity = entity

    @property
    def engine(self) -> Engine:
        """Return the engine this action belongs to."""
        return self.entity.gamemap.engine
    
    def perform(self)-> None:
        # 'Engine' is the scope where the action is being performed, entity is the object doing the action
        # This method will be overriden by the action subclasses. 
        raise NotImplementedError()

class EscapeAction:
    def perform(self) -> None:
        raise SystemExit()

class ActionWithDirection(Action):
    def __init__(self, entity: Entity, dx: int, dy: int):
        super().__init__(entity)

        self.dx = dx
        self.dy = dy

    @property
    def dest_xy(self) -> Tuple[int, int]:
        """Returns this actions destination."""
        return self.entity.x + self.dx, self.entity.y + self.dy

    @property
    def blocking_entity(self) -> Optional[Entity]:
        """Return the blocking entity at this actions destination.."""
        return self.engine.game_map.get_blocking_entity_at(*self.dest_xy)

    def perform(self) -> None:
        raise NotImplementedError()

class MeleeAttack(ActionWithDirection):
     def perform(self) -> None:
        target = self.blocking_entity
        if not target:
            return # No entity to attack
        
        print(f"You kick the {target.name}, much to its annoyance!")

class MovementAction(ActionWithDirection):
    def perform(self) -> None:
        dest_x, dest_y = self.dest_xy

        if not self.engine.game_map.in_bounds(dest_x, dest_y):
            return # Destination out of bounds
        if not self.engine.game_map.tiles["walkable"][dest_x, dest_y]:
            return # Destination not walkable (wall)
        if self.engine.game_map.get_blocking_entity_at(dest_x, dest_y):
            return # Destination is blocked by an entity (not walkable)
        
        self.entity.move(self.dx, self.dy)

class BumpAction(ActionWithDirection):
    def perform(self) -> None:
        if self.blocking_entity:
            return MeleeAttack(self.entity, self.dx, self.dy).perform()
    
        else:
            return MovementAction(self.entity, self.dx, self.dy).perform()