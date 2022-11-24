from dataclasses import dataclass
from pathlib import Path

from ._position import Position
from ._size import Size


@dataclass(frozen=True)
class SpriteSheet:
    file_path: Path
    resolution: Size

    def get_unit_position(self, coordinates: Position) -> Position:
        return coordinates


@dataclass(frozen=True)
class Sprite:
    sprite_grid: SpriteSheet
    coordinates: Position
    size: Size

    def position(self) -> Position:
        return self.sprite_grid.get_unit_position(self.coordinates)

    def resolution(self) -> Size:
        return self.size
