from functools import lru_cache
from pathlib import Path

from pygame.image import load

from seagulls.engine import Surface


class AssetManager:

    """Provides basic functionality for loading assets from disk."""

    _assets_path: Path

    def __init__(self, assets_path: Path):
        self._assets_path = assets_path

    @lru_cache()
    def load_sprite(self, name: str) -> Surface:
        return self.load_png(f"sprites/{name}")

    def load_jpg(self, name: str) -> Surface:
        path = self.get_path(f"{name}.jpg")
        loaded_sprite = load(path.resolve())
        return loaded_sprite.convert()

    def load_png(self, name: str) -> Surface:
        path = self.get_path(f"{name}.png")
        loaded_sprite = load(path.resolve())
        if loaded_sprite.get_alpha() is None:
            return loaded_sprite.convert()
        else:
            return loaded_sprite.convert_alpha()

    def get_path(self, name: str) -> Path:
        p = self._assets_path / name
        if not p.exists():
            raise RuntimeError(f"no path found for asset: {name}")

        return p
