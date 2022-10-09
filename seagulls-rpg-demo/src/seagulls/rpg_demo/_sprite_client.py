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


class Sprites(Enum):
    island_tree = "island-tree"
    island_red_home = "island-red-home"
    jeffrey_standing = "jeffrey-standing"
    cursor_sword_bronze = "cursor-sword-bronze"
    island_water = "island-water"


class SpriteInfo(NamedTuple):
    path: str
    resolution: Tuple[int, int]
    size: Tuple[int, int]
    grid_size: Tuple[int, int]
    coordinates: Tuple[int, int]


class SpriteClient:
    def __init__(self, printer: IPrinter):
        self._printer = printer
        self._sprite_mapping: Dict[Sprites, SpriteInfo] = {
            Sprites.island_tree: SpriteInfo(
                path="seagulls_assets/sprites/environment/rpg-environment/island-tree.png",
                resolution=(16, 16),
                size=(64, 64),
                grid_size=(1, 1),
                coordinates=(0, 0),
            ),
            Sprites.island_red_home: SpriteInfo(
                path="seagulls_assets/sprites/environment/rpg-environment/island-red-home.png",
                resolution=(16, 16),
                size=(64, 64),
                grid_size=(1, 1),
                coordinates=(0, 0),
            ),
            Sprites.cursor_sword_bronze: SpriteInfo(
                path="seagulls_assets/sprites/environment/rpg-environment/cursor-sword-bronze.png",
                resolution=(37, 34),
                size=(64, 64),
                grid_size=(1, 1),
                coordinates=(0, 0),
            ),
            Sprites.island_water: SpriteInfo(
                path="seagulls_assets/sprites/environment/rpg-environment/island-water.png",
                resolution=(16, 16),
                size=(500, 500),
                grid_size=(1, 1),
                coordinates=(0, 0),
            ),
            Sprites.jeffrey_standing: SpriteInfo(
                path="seagulls_assets/sprites/rpg/rpg-urban-tilemap.packed.png",
                resolution=(288, 432),
                size=(32, 32),
                grid_size=(18, 27),
                coordinates=(24, 0),
            )
        }

    def render_sprite(self, sprite_name: Sprites, position: Position) -> None:
        sprite_info = self._sprite_mapping[sprite_name]

        sprite = SpriteComponent(
            sprite=Sprite(
                sprite_grid=SpriteSheet(
                    file_path=Path(sprite_info.path),
                    resolution=Size(
                        {"height": sprite_info.resolution[0], "width": sprite_info.resolution[1]}),
                    grid_size=Size(
                        {"height": sprite_info.grid_size[0], "width": sprite_info.grid_size[1]}),
                ),
                coordinates=Position(
                    {"x": sprite_info.coordinates[0], "y": sprite_info.coordinates[1]}),
            ),
            size=Size({"height": sprite_info.size[0], "width": sprite_info.size[1]}),
            position=position,
            printer=self._printer,
        )

        sprite.render()
