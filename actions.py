from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from engine import Engine
    from Entity import Entity

class Action:
    def perform(self, engine: Engine, entity: Entity) -> None:
        # 'Engine' is the scope where the action is being performed, entity is the object doing the action
        # This method will be overriden by the action subclasses. 
        raise NotImplementedError()

class EscapeAction:
    def perform(self, engine: Engine, entity: Entity) -> None:
        raise SystemExit()

class MovementAction:
    def __init__(self, dx: int, dy: int):
        super().__init__()

        self.dx = dx
        self.dy = dy
    
    def perform(self, engine: Engine, entity: Entity) -> None:
        dest_x = entity.x + self.dx
        dest_y = entity.y + self.dy

        if not engine.game_map.in_bounds(dest_x, dest_y):
            return # Destination out of bounds
        if not engine.game_map.tiles["walkable"][dest_x, dest_y]:
            return # Destination not walkable (wall)
        
        entity.move(self.dx, self.dy)