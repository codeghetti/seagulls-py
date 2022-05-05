from dataclasses import dataclass
from pathlib import Path

from ._position import Position
from ._size import Size


@dataclass(frozen=True)
class SpriteSheet:
    file_path: Path
    resolution: Size
    grid_size: Size

    def get_unit_position(self, coordinates: Position) -> Position:
        coords = coordinates.get()
        unit_rez = self.unit_resolution().get()

        x = unit_rez["width"] * coords["x"]
        y = unit_rez["height"] * coords["y"]
        return Position({"x": x, "y": y})

    def num_units(self) -> int:
        grid = self.grid_size.get()
        return grid["height"] * grid["width"]

    def unit_resolution(self) -> Size:
        rez = self.resolution.get()
        grid = self.grid_size.get()

        return Size({
            "height": int(rez["height"] / grid["height"]),
            "width": int(rez["width"] / grid["width"]),
        })


@dataclass(frozen=True)
class Sprite:
    sprite_grid: SpriteSheet
    coordinates: Position

    def position(self) -> Position:
        return self.sprite_grid.get_unit_position(self.coordinates)

    def resolution(self) -> Size:
        return self.sprite_grid.unit_resolution()
