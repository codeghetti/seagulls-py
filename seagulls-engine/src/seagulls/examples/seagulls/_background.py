from functools import lru_cache

from seagulls.assets import AssetManager
from seagulls.engine import GameObject, Surface


class SeagullsBackground(GameObject):

    _asset_manager: AssetManager

    def __init__(
            self,
            asset_manager: AssetManager):
        self._asset_manager = asset_manager

    def tick(self) -> None:
        pass

    def render(self, surface: Surface) -> None:
        background = self._get_cached_background()
        surface.blit(background, (0, 0))

    @lru_cache()
    def _get_cached_background(self) -> Surface:
        background = self._asset_manager.load_sprite("environment/environment-sky").copy()

        things = [
            # These need to be in the order they should be rendered on top of the sky
            self._asset_manager.load_sprite("environment/environment-stars"),
            self._asset_manager.load_sprite("environment/environment-wall"),
            self._asset_manager.load_sprite("environment/environment-bookshelves"),
            self._asset_manager.load_sprite("environment/environment-ladders"),
            self._asset_manager.load_sprite("environment/environment-floor"),
            self._asset_manager.load_sprite("environment/environment-rampart"),
            self._asset_manager.load_sprite("environment/environment-perch"),
            self._asset_manager.load_sprite("environment/environment-scrolls"),
            self._asset_manager.load_sprite("environment/environment-spider"),
        ]

        for thing in things:
            background.blit(thing, (0, 0))

        return background
