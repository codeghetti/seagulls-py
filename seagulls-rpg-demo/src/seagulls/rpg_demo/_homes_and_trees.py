import random
from functools import lru_cache
from typing import Any, Dict, List, Optional

from pygame.rect import Rect
from seagulls.assets import AssetManager
from seagulls.engine import GameObject, Surface


class Tile:
    pass


class GameBoard:
    _tiles: Dict[Any, Any]

    def __init__(self):
        self._tiles = {}

    def get_tile(self, x: int, y: int) -> Optional[Tile]:
        return self._tiles.get((x, y))

    def set_tile(self, x, y, tile: Tile) -> None:
        self._tiles[(x, y)] = tile

    def get_neighbors(self, x: int, y: int, size: int) -> List[Tile]:
        neighbors = []

        if self.get_tile(x - size, y) is not None:
            neighbors.append(self.get_tile(x - size, y))

        if self.get_tile(x + size, y) is not None:
            neighbors.append(self.get_tile(x + size, y))

        if self.get_tile(x, y - size) is not None:
            neighbors.append(self.get_tile(x, y - size))

        if self.get_tile(x, y + size) is not None:
            neighbors.append(self.get_tile(x, y + size))

        if self.get_tile(x + size, y + size) is not None:
            neighbors.append(self.get_tile(x + size, y + size))

        if self.get_tile(x - size, y - size) is not None:
            neighbors.append(self.get_tile(x - size, y - size))

        if self.get_tile(x - size, y + size) is not None:
            neighbors.append(self.get_tile(x - size, y + size))

        if self.get_tile(x + size, y - size) is not None:
            neighbors.append(self.get_tile(x + size, y - size))

        return [n for n in neighbors if n]


class HomesAndTrees(GameObject):

    _asset_manager: AssetManager
    _game_board: GameBoard
    _world_objects: List[Rect]

    def __init__(self, asset_manager: AssetManager):
        self._asset_manager = asset_manager
        self._game_board = GameBoard()
        self._world_objects = []

    def tick(self) -> None:
        pass

    def render(self, surface: Surface) -> None:
        surface.blit(self._get_cached_homes_and_trees(), (0, 0))

    def get_world_object_rectangles(self) -> List[Rect]:
        self._get_cached_homes_and_trees()
        return self._world_objects

    @lru_cache()
    def _get_cached_homes_and_trees(self) -> Surface:
        surface = Surface((1024, 600))
        color_key = (127, 33, 33)
        surface.fill(color_key)
        surface.set_colorkey(color_key)

        island_red_home = self._asset_manager.load_sprite(
            "environment/rpg-environment/island-red-home").copy()
        island_blue_home = self._asset_manager.load_sprite(
            "environment/rpg-environment/island-blue-home").copy()
        island_tree = self._asset_manager.load_sprite(
            "environment/rpg-environment/island-tree").copy()

        for y in range(int(600 / 16)):
            for x in range(int(1024 / 16)):
                if not (y == 0 or y >= 35 or x == 0 or x >= 63):
                    random_number = random.randint(0, 100)
                    if random_number == 93:
                        if len(self._game_board.get_neighbors(x * 16, y * 16, 16)) == 0:
                            surface.blit(island_red_home, (x * 16, y * 16))
                            self._game_board.set_tile(x * 16, y * 16, Tile())
                            self._world_objects.append(Rect(x * 16, y * 16, 16, 16))
                    elif random_number == 94:
                        if len(self._game_board.get_neighbors(x * 16, y * 16, 16)) == 0:
                            surface.blit(island_blue_home, (x * 16, y * 16))
                            self._game_board.set_tile(x * 16, y * 16, Tile())
                            self._world_objects.append(Rect(x * 16, y * 16, 16, 16))
                    elif random_number > 94:
                        surface.blit(island_tree, (x * 16, y * 16))
                        self._world_objects.append(Rect(x * 16, y * 16, 16, 16))

        return surface
