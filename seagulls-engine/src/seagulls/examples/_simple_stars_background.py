from functools import lru_cache

from seagulls.assets import AssetManager
from seagulls.engine import GameObject, Surface


class SimpleStarsBackground(GameObject):

    _asset_manager: AssetManager

    def __init__(self, asset_manager: AssetManager):
        self._asset_manager = asset_manager

    def tick(self) -> None:
        pass

    def render(self, surface: Surface) -> None:
        background = self._get_cached_background()
        surface.blit(background, (0, 0))

    @lru_cache()
    def _get_cached_background(self) -> Surface:
        return self._asset_manager.load_sprite("environment/environment-stars").copy()
