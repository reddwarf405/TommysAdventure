import numpy as np
from tcod.console import Console

import tile_types

class GameMap:
    def __init__(self, width: int, height: int):
        self.width, self.height = width, height
        self.tiles = np.full((width, height), fill_value=tile_types.wall, order="F")

        self.visible=np.full((width, height), fill_value=False, order="F") # Tiles the player can see currently
        self.explored=np.full((width, height), fill_value=False, order="F") # Tiles the player has seen before


    def in_bounds(self, x: int, y: int) -> bool:
        # Checks if something is in the bounds of the map & returns true if so
        return 0 <= x < self.width and 0 <= y < self.height

    def render(self, console: Console) -> None:
        # Renders the map.
        # If a tile is 'visible', it will be drawn with light colors
        # If it isn't, but it has been explored, draw it with 'dark' colors
        # Otherwise it will default to SHROUD
        console.tiles_rgb[0:self.width, 0:self.height] = np.select(
            condlist=[self.visible, self.explored],
            choicelist=[self.tiles["light"], self.tiles["dark"]],
            default=tile_types.SHROUD
        )