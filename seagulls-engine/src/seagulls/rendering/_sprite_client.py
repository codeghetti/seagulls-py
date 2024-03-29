from enum import Enum
from pathlib import Path
from typing import Dict, NamedTuple, Tuple

from seagulls.rendering import (
    IPrinter,
    Position,
    Size,
    Sprite,
    SpriteComponent,
    SpriteSheet
)


class SpritesType(Enum):
    pass


class SpriteInfo(NamedTuple):
    path: str
    resolution: Tuple[int, int]
    coordinates: Tuple[int, int]
    size: Tuple[int, int]
    game_size: Tuple[int, int]


class SpriteClient:
    def __init__(self,
                 printer: IPrinter,
                 sprite_mapping: Dict[SpritesType, SpriteInfo]):
        self._printer = printer
        self._sprite_mapping = sprite_mapping

    def render_sprite(self, sprite_name: SpritesType, position: Position) -> None:
        sprite_info = self._sprite_mapping[sprite_name]

        sprite = SpriteComponent(
            sprite=Sprite(
                sprite_grid=SpriteSheet(
                    file_path=Path(sprite_info.path),
                    resolution=Size(
                        {"width": sprite_info.resolution[0], "height": sprite_info.resolution[1]}),
                ),
                coordinates=Position(
                    {"x": sprite_info.coordinates[0], "y": sprite_info.coordinates[1]}),
                size=Size({"width": sprite_info.size[0], "height": sprite_info.size[1]})
            ),
            size=Size({"width": sprite_info.game_size[0], "height": sprite_info.game_size[1]}),
            position=position,
            printer=self._printer,
        )

        sprite.render()
