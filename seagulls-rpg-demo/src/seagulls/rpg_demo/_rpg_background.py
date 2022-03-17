from functools import lru_cache

from seagulls.assets import AssetManager
from seagulls.engine import GameObject, Surface


class SimpleRpgBackground(GameObject):

    def __init__(self, asset_manager: AssetManager):
        self._asset_manager = asset_manager

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
                    surface.blit(island_grass, (x * 16, y * 16))

        return surface
