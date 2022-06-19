from pathlib import Path
from typing import Generic, TypeVar, Type, Dict

from ._sprites_client import (
    SpriteConfig,
    SpriteEnum,
    SpriteSheetConfig,
    SpriteSheetEnum, SpriteClient
)
from ..rendering import SpriteComponent, Sprite, SpriteSheet


class PixelShmupSpriteSheets(SpriteSheetEnum):
    TILES = SpriteSheetConfig(
        file_path=Path("seagulls_assets/kenney/pixelshmup/tiles.png"),
        width=192,
        height=160,
        rows=10,
        columns=12,
    )
    SHIPS = SpriteSheetConfig(
        file_path=Path("seagulls_assets/kenney/pixelshmup/ships.png"),
        width=128,
        height=192,
        rows=6,
        columns=4,
    )


class PixelShmupTileSprites(SpriteEnum):
    TREE_GRASS_1 = SpriteConfig(x=0, y=4)
    TREE_GRASS_2 = SpriteConfig(x=0, y=5)

    TREE_DIRT_1 = SpriteConfig(x=7, y=4)
    TREE_DIRT_2 = SpriteConfig(x=7, y=5)

    HOME_RED_GRASS_1 = SpriteConfig(x=0, y=6)
    HOME_RED_GRASS_AFRAME = SpriteConfig(x=0, y=7)

    FLAG_RED_GRASS = SpriteConfig(x=0, y=8)

    GRASS_1 = SpriteConfig(x=2, y=4)
    GRASS_2 = SpriteConfig(x=2, y=9)


# class PixelShmupShipSprites(SpriteEnum):
#     MODEL_1_LARGE_BLUE = SpriteConfig(x=0, y=0)
#     MODEL_1_MEDIUM_BLUE = SpriteConfig(x=0, y=1)
#     MODEL_1_SMALL_BLUE = SpriteConfig(x=0, y=2)
#
#     MODEL_1_LARGE_GREY = SpriteConfig(x=0, y=3)
#     MODEL_1_MEDIUM_GREY = SpriteConfig(x=0, y=4)
#     MODEL_1_SMALL_GREY = SpriteConfig(x=0, y=5)
#
#     MODEL_2_LARGE_ORANGE = SpriteConfig(x=1, y=0)
#     MODEL_2_MEDIUM_ORANGE = SpriteConfig(x=1, y=1)
#     MODEL_2_SMALL_ORANGE = SpriteConfig(x=1, y=2)
#
#     MODEL_2_LARGE_GREY = SpriteConfig(x=1, y=3)
#     MODEL_2_MEDIUM_GREY = SpriteConfig(x=1, y=4)
#     MODEL_2_SMALL_GREY = SpriteConfig(x=1, y=5)
#
#     MODEL_3_LARGE_GREEN = SpriteConfig(x=2, y=0)
#     MODEL_3_MEDIUM_GREEN = SpriteConfig(x=2, y=1)
#     MODEL_3_SMALL_GREEN = SpriteConfig(x=2, y=2)
#
#     MODEL_3_LARGE_GREY = SpriteConfig(x=2, y=3)
#     MODEL_3_MEDIUM_GREY = SpriteConfig(x=2, y=4)
#     MODEL_3_SMALL_GREY = SpriteConfig(x=2, y=5)
#
#     MODEL_4_LARGE_YELLOW = SpriteConfig(x=3, y=0)
#     MODEL_4_MEDIUM_YELLOW = SpriteConfig(x=3, y=1)
#     MODEL_4_SMALL_YELLOW = SpriteConfig(x=3, y=2)
#
#     MODEL_4_LARGE_GREY = SpriteConfig(x=3, y=3)
#     MODEL_4_MEDIUM_GREY = SpriteConfig(x=3, y=4)
#     MODEL_4_SMALL_GREY = SpriteConfig(x=3, y=5)


T = TypeVar("T")


class SpriteSheetRegistry(Generic[T]):

    _providers: Dict[Type[T], T]

    def __init__(self):
        self._providers = {}

    def register_provider(self, ref: Type[T], provider: T) -> None:
        self._providers[ref] = provider

    def get_provider(self, ref: Type[T]) -> T:
        return self._providers[ref]


class PixelShmupShipSprites:
    def model_1_large_blue(self) -> SpriteClient:
        return
        SpriteConfig(x=0, y=0)
    MODEL_1_MEDIUM_BLUE = SpriteConfig(x=0, y=1)
    MODEL_1_SMALL_BLUE = SpriteConfig(x=0, y=2)

    @lru_cache()
    def _sprite(self) -> Sprite:
        return Sprite(
            sprite_grid=self._sprite_sheet(),
            coordinates=Position({
                "x": self._sprite_id.value.x,
                "y": self._sprite_id.value.y,
            }),
        )

    def _sprite_sheet(self) -> SpriteSheet:
        return SpriteSheet(
            file_path=self._sprite_sheet_id.value.file_path,
            resolution=Size({
                "height": self._sprite_sheet_id.value.height,
                "width": self._sprite_sheet_id.value.width,
            }),
            grid_size=Size({
                "height": self._sprite_sheet_id.value.rows,
                "width": self._sprite_sheet_id.value.columns,
            }),
        )


class PixelShmupShipSpritesPlugin:

    _registry: SpriteSheetRegistry

    def __init__(self, registry: SpriteSheetRegistry):
        self._registry = registry

    def register_sheets(self) -> None:
        self._registry.register_provider(PixelShmupShipSprites, PixelShmupShipSprites())
