from pathlib import Path

from seagulls.engine import Surface
from pygame.image import load


class AssetManager:
    _assets_path: Path

    def __init__(self, assets_path: Path):
        self._assets_path = assets_path

    def load_sprite(self, name: str) -> Surface:
        path = self._assets_path / f"sprites/{name}.png"
        loaded_sprite = load(path.resolve())
        if loaded_sprite.get_alpha() is None:
            return loaded_sprite.convert()
        else:
            return loaded_sprite.convert_alpha()
