from pathlib import Path

from pygame.surface import Surface
from pygame.image import load


class AssetManager:
    _assets_path: Path

    def __init__(self, assets_path: Path):
        self._assets_path = assets_path

    def load_sprite(self, name: str, with_alpha: bool = True) -> Surface:
        path = self._assets_path / f"sprites/{name}.png"
        loaded_sprite = load(path.resolve())
        loaded_sprite.get_alpha()

        if with_alpha:
            return loaded_sprite.convert_alpha()
        else:
            return loaded_sprite.convert()
