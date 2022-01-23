import random
from functools import lru_cache
from typing import Any, Dict, List, Optional

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


class SimpleRpgBackground(GameObject):

    _asset_manager: AssetManager
    _game_board: GameBoard

    def __init__(self, asset_manager: AssetManager):
        self._asset_manager = asset_manager
        self._game_board = GameBoard()

    def tick(self) -> None:
        pass

    def render(self, surface: Surface) -> None:
        background = self._get_cached_background()
        surface.blit(background, (0, 0))

    @lru_cache()
    def _get_cached_background(self) -> Surface:
        surface = Surface((1024, 600))

        top_left_corner = self._asset_manager.load_sprite(
            "environment/rpg-environment/island-top-left-corner").copy()
        top_island_edge = self._asset_manager.load_sprite(
            "environment/rpg-environment/island-top-edge").copy()
        top_right_corner = self._asset_manager.load_sprite(
            "environment/rpg-environment/island-top-right-corner").copy()
        island_water = self._asset_manager.load_sprite(
            "environment/rpg-environment/island-water").copy()
        bottom_left_corner = self._asset_manager.load_sprite(
            "environment/rpg-environment/island-bottom-left-corner").copy()
        bottom_island_edge = self._asset_manager.load_sprite(
            "environment/rpg-environment/island-bottom-edge").copy()
        bottom_right_corner = self._asset_manager.load_sprite(
            "environment/rpg-environment/island-bottom-right-corner").copy()
        island_left_edge = self._asset_manager.load_sprite(
            "environment/rpg-environment/island-left-edge").copy()
        island_right_edge = self._asset_manager.load_sprite(
            "environment/rpg-environment/island-right-edge").copy()
        island_grass = self._asset_manager.load_sprite(
            "environment/rpg-environment/island-grass").copy()
        island_red_home = self._asset_manager.load_sprite(
            "environment/rpg-environment/island-red-home").copy()
        island_blue_home = self._asset_manager.load_sprite(
            "environment/rpg-environment/island-blue-home").copy()
        island_tree = self._asset_manager.load_sprite(
            "environment/rpg-environment/island-tree").copy()

        for y in range(int(600 / 16)):
            for x in range(int(1024 / 16)):
                if y == 0:
                    if x == 0:
                        surface.blit(top_left_corner, (x * 16, y * 16))
                    elif x == 63:
                        surface.blit(top_right_corner, (x * 16, y * 16))
                    else:
                        surface.blit(top_island_edge, (x * 16, y * 16))
                elif y == 35:
                    if x == 0:
                        surface.blit(bottom_left_corner, (x * 16, y * 16))
                    elif x == 63:
                        surface.blit(bottom_right_corner, (x * 16, y * 16))
                    else:
                        surface.blit(bottom_island_edge, (x * 16, y * 16))
                elif y == 36:
                    surface.blit(island_water, (x * 16, y * 16))

                elif x == 0:
                    surface.blit(island_left_edge, (x * 16, y * 16))

                elif x == 63:
                    surface.blit(island_right_edge, (x * 16, y * 16))

                else:
                    random_number = random.randint(0, 100)
                    if random_number < 92:
                        surface.blit(island_grass, (x * 16, y * 16))
                    elif random_number < 93:
                        if len(self._game_board.get_neighbors(x * 16, y * 16, 16)) == 0:
                            surface.blit(island_red_home, (x * 16, y * 16))
                            self._game_board.set_tile(x * 16, y * 16, Tile())
                        else:
                            surface.blit(island_grass, (x * 16, y * 16))
                    elif random_number < 94:
                        if len(self._game_board.get_neighbors(x * 16, y * 16, 16)) == 0:
                            surface.blit(island_blue_home, (x * 16, y * 16))
                            self._game_board.set_tile(x * 16, y * 16, Tile())
                        else:
                            surface.blit(island_grass, (x * 16, y * 16))
                    else:
                        surface.blit(island_tree, (x * 16, y * 16))
        return surface
