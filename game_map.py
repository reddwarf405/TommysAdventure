from __future__ import annotations

from typing import Iterable, TYPE_CHECKING, Optional, Iterator

import numpy as np
from tcod.console import Console

from Entity import Actor
import tile_types

if TYPE_CHECKING:
    from engine import Engine
    from Entity import Entity

class GameMap:
    def __init__(
        self, engine: Engine, width: int, height: int, entities: Iterable[Entity] = ()
    ):
        self.engine = engine
        self.width, self.height = width, height
        self.entities = set(entities)
        self.tiles = np.full((width, height), fill_value=tile_types.wall, order="F")

        self.visible = np.full(
            (width, height), fill_value=False, order="F"
        )  # Tiles the player can currently see
        self.explored = np.full(
            (width, height), fill_value=False, order="F"
        )  # Tiles the player has seen before

    @property
    def actors(self) -> Iterator[Actor]:
        #Iterate over this maps living actors.
        yield from (
            entity
            for entity in self.entities
            if isinstance(entity, Actor) and entity.is_alive
        )

    def get_blocking_entity_at(
        self, location_x: int, location_y: int,
    ) -> Optional[Entity]:
        for entity in self.entities:
            if (
                entity.blocks_movement
                and entity.x == location_x
                and entity.y == location_y
            ):
                return entity
        
        return None
    
    def get_actor_at(self, x: int, y: int) -> Optional[Actor]:
        for actor in self.actors:
            if actor.x == x and actor.y == y:
                return actor
        return None

    def in_bounds(self, x: int, y: int) -> bool:
        # Checks if something is in the bounds of the map & returns true if so
        return 0 <= x < self.width and 0 <= y < self.height

    def render(self, console: Console) -> None:
        # Renders the map.
        # If a tile is 'visible', it will be drawn with light colors
        # If it isn't, but it has been explored, draw it with 'dark' colors
        # Otherwise it will default to SHROUD
        console.tiles_rgb[0 : self.width, 0 : self.height] = np.select(
            condlist=[self.visible, self.explored],
            choicelist=[self.tiles["light"], self.tiles["dark"]],
            default=tile_types.SHROUD,
        )

        entities_sorted_for_rendering = sorted(
            self.entities, key=lambda x: x.render_order.value
        )

        for entity in entities_sorted_for_rendering:
          # Only print entities in FOV
          if self.visible[entity.x, entity.y]:
             console.print(x=entity.x, y=entity.y, string=entity.char, fg=entity.color)
