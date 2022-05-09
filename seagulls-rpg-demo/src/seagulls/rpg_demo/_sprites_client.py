from dataclasses import dataclass
from enum import Enum
from functools import lru_cache
from pathlib import Path
from typing import TypeVar, Generic

from seagulls.rendering import (
    IPrinter,
    Position,
    SpriteComponent,
    Sprite,
    Size,
    SpriteSheet
)


@dataclass(frozen=True)
class SpriteSheetConfig:
    file_path: Path
    height: int
    width: int
    rows: int
    columns: int

    @property
    def sprite_height(self) -> int:
        return int(self.height / self.rows)

    @property
    def sprite_width(self) -> int:
        return int(self.width / self.columns)


@dataclass(frozen=True)
class SpriteConfig:
    x: int
    y: int


class SpriteSheetEnum(Enum):
    pass


class SpriteEnum(Enum):
    pass


SpriteSheetEnumType = TypeVar("SpriteSheetEnumType", bound=SpriteSheetEnum)
SpriteEnumType = TypeVar("SpriteEnumType", bound=SpriteEnum)


class SpriteClient(Generic[SpriteSheetEnumType, SpriteEnumType]):

    _printer: IPrinter
    _sprite_sheet_id: SpriteSheetEnumType
    _sprite_id: SpriteEnumType

    def __init__(
            self,
            printer: IPrinter,
            sprite_sheet_id: SpriteSheetEnumType,
            sprite_id: SpriteEnumType):
        self._printer = printer
        self._sprite_sheet_id = sprite_sheet_id
        self._sprite_id = sprite_id

    def render_sprite(self, position: Position, scale: float = 1.0) -> None:
        sprite_component = SpriteComponent(
            sprite=self._sprite(),
            size=Size({
                "height": int(self._sprite_sheet_id.value.sprite_height * scale),
                "width": int(self._sprite_sheet_id.value.sprite_width * scale),
            }),
            position=position,
            printer=self._printer,
        )

        sprite_component.render()

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


class SpriteSheetClient(Generic[SpriteEnumType]):

    _printer: IPrinter
    _sprite_sheet_id: SpriteSheetEnum

    def __init__(
            self,
            printer: IPrinter,
            sprite_sheet_id: SpriteSheetEnum):
        self._printer = printer
        self._sprite_sheet_id = sprite_sheet_id

    @lru_cache()
    def get_sprite(self, sprite_id: SpriteEnumType) -> SpriteClient:
        return SpriteClient(
            printer=self._printer,
            sprite_sheet_id=self._sprite_sheet_id,
            sprite_id=sprite_id,
        )


class SpriteSheetLocator:

    _printer: IPrinter

    def __init__(self, printer: IPrinter):
        self._printer = printer

    def get_sprite_sheet(
            self,
            sprite_sheet_id: SpriteSheetEnumType
    ) -> SpriteSheetClient[SpriteSheetEnumType]:
        return SpriteSheetClient[SpriteSheetEnumType](
            printer=self._printer,
            sprite_sheet_id=sprite_sheet_id,
        )
