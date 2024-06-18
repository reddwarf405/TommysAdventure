from __future__ import annotations

from typing import Tuple, Iterator, List, TYPE_CHECKING
import random

import tcod

import entity_factories
from game_map import GameMap
import tile_types

if TYPE_CHECKING:
    from engine import Engine

class RectangularRoom:
    def __init__(self, x: int, y: int, width: int, height:int):
        self.x1 = x
        self.y1 = y
        self.x2 = x + width
        self.y2 = y + height
    
    @property
    def center(self) -> Tuple[int, int]:
        center_x = int((self.x1 + self.x2) / 2)
        center_y = int((self.y1 + self.y2) / 2)

        return center_x, center_y
    
    @property
    def inner(self) -> Tuple[slice, slice]:
        # Returns the inner area of this room as a 2d array index
        return slice(self.x1 + 1, self.x2), slice(self.y1 + 1, self.y2)
    
    def intersects(self, other: RectangularRoom) -> bool:
        # Returns true if this room overlaps with another room
        return(
            self.x1 <= other.x2
            and self.x2 >= other.x1
            and self.y1 <= other.y2
            and self.y2 >= other.y1
        )
    
def place_entities(
            room: RectangularRoom, dungeon: GameMap, maximum_monsters: int, maximum_items: int,
    ) -> None:
            number_of_monsters = random.randint(0, maximum_monsters)
            number_of_items = random.randint(0, maximum_items)

            for i in range(number_of_monsters):
                x = random.randint(room.x1 + 1, room.x2 - 1)
                y = random.randint(room.y1 + 1, room.y2 - 1)

                if not any (entity.x == x and entity.y == y for entity in dungeon.entities):
                    if random.random() < 0.8:
                        entity_factories.bot.spawn(dungeon, x, y)
                    else:
                        entity_factories.employee.spawn(dungeon, x, y)

            for i in range(number_of_items):
                x = random.randint(room.x1 + 1, room.x2 - 1)
                y = random.randint(room.y1 + 1, room.y2 - 1)

                if not any(entity.x == x and entity.y == y for entity in dungeon.entities):
                    item_chance = random.random()

                    if item_chance < 0.7:
                        entity_factories.bandage.spawn(dungeon, x, y)
                    elif item_chance < 0.8:
                        entity_factories.bomb.spawn(dungeon, x, y)
                    elif item_chance < 0.9:
                        entity_factories.emp.spawn(dungeon, x, y)
                    else:
                        entity_factories.onetimehack.spawn(dungeon, x, y)
    
def tunnel_between(start: Tuple[int, int], end: Tuple[int, int]) -> Iterator[Tuple[int, int]]:
    # Return an L-shaped tunnel between two rooms
    x1, y1 = start
    x2, y2 = end
    if random.random() < 0.5:
        # Moves horizontally, then vertically
        corner_x, corner_y = x2, y1
    else:
        # Moves vertically then horizontally
        corner_x, corner_y = x1, y2

    # Generate the coordinates for this tunnel.
    for x, y in tcod.los.bresenham((x1, y1), (corner_x, corner_y)).tolist():
        yield x, y
    for x, y in tcod.los.bresenham((corner_x, corner_y), (x2, y2)).tolist():
        yield x, y

def generate_dungeon(max_rooms: int, room_min_size: int, room_max_size: int, map_width: int, map_height: int, max_monsters_per_room: int, max_items_per_room: int, engine: Engine) -> GameMap:
    #Generate a new dungeon map
    player = engine.player
    dungeon = GameMap(engine, map_width, map_height, entities=[player])

    rooms: List[RectangularRoom] = []

    center_of_last_room = (0,0)

    for r in range(max_rooms):
        room_width = random.randint(room_min_size, room_max_size)
        room_height = random.randint(room_min_size, room_max_size)

        x = random.randint(0, dungeon.width - room_width - 1)
        y = random.randint(0, dungeon.height - room_height - 1)

        # "RectangularRoom" class makes rectangles easier to work with
        new_room = RectangularRoom(x, y, room_width, room_height)

        # Run through the other rooms and see if they intersect with this one
        if any(new_room.intersects(other_room) for other_room in rooms):
            continue  # Intersects, so we try again

        # Dig out this rooms inner area
        dungeon.tiles[new_room.inner] = tile_types.floor

        if len(rooms) == 0:
            # The first room, where the player starts
            player.place(*new_room.center, dungeon)
        else:  # All rooms after the first.
            # Dig out a tunnel between this room and the previous one.
            for x, y in tunnel_between(rooms[-1].center, new_room.center):
                dungeon.tiles[x, y] = tile_types.floor

            center_of_last_room = new_room.center

        place_entities(new_room, dungeon, max_monsters_per_room, max_items_per_room)

        dungeon.tiles[center_of_last_room] = tile_types.up_stairs
        dungeon.upstairs_location = center_of_last_room
 
        # Finally, append the new room to the list
        rooms.append(new_room)

    return dungeon