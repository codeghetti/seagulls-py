import random
from functools import lru_cache
from pathlib import Path
from typing import Tuple

import pygame
from pygame.rect import Rect

from seagulls.pygame import PygameCameraPrinter
from seagulls.rendering import Color, Position, Size, SizeDict, Camera
from seagulls.rendering._example._components import (
    BoxComponent,
    SolidColorComponent,
    SpriteComponent
)
from seagulls.rendering._renderable_component import (
    IProvideRenderables,
    RenderableComponent
)
from seagulls.rendering._sprite import Sprite, SpriteSheet


class MyRenderables(IProvideRenderables):

    _printer: PygameCameraPrinter
    _camera: Camera
    _scene_size: SizeDict

    def __init__(
            self,
            printer: PygameCameraPrinter,
            camera: Camera,
            scene_size: SizeDict):
        self._printer = printer
        self._camera = camera
        self._scene_size = scene_size

    def get(self) -> Tuple[RenderableComponent, ...]:
        color = Color({
            "r": random.randint(0, 255),
            "g": random.randint(0, 255),
            "b": random.randint(0, 255),
        })
        size = Size({
            "height": random.randint(1, 3),
            "width": random.randint(1, 3),
        })
        position1 = Position({
            "x": random.randint(0, 50),
            "y": random.randint(0, 50),
        })
        position2 = Position({
            "x": random.randint(self._scene_size["width"] - 50 - 60,
                                self._scene_size["width"] - 60),

            "y": random.randint(self._scene_size["height"] - 50 - 60,
                                self._scene_size["height"] - 60),
        })
        items = [
            SolidColorComponent(
                color=color,
                size=size,
                position=position1,
                printer=self._printer,
            ),
            BoxComponent(
                color=color,
                size=Size({
                    "height": random.randint(30, 60),
                    "width": random.randint(30, 60),
                }),
                border_size=2,
                position=position2,
                printer=self._printer,
            ),
            SpriteComponent(
                sprite=Sprite(
                    sprite_grid=SpriteSheet(
                        file_path=Path(
                            "../../../../../seagulls-rpg-demo/seagulls_assets/sprites/environment/"
                            "rpg-environment-options/tile_0060.png"),
                        resolution=Size({"height": 16, "width": 16}),
                        grid_size=Size({"height": 1, "width": 1}),
                    ),
                    coordinates=Position({"x": 0, "y": 0}),
                ),
                size=Size({"height": 16, "width": 16}),
                position=Position({"x": 200, "y": 50}),
                printer=self._printer,
            ),
            SpriteComponent(
                sprite=Sprite(
                    sprite_grid=SpriteSheet(
                        file_path=Path(
                            "../../../../../seagulls-rpg-demo/seagulls_assets/sprites/environment/"
                            "rpg-environment-options/tile_0026.png"),
                        resolution=Size({"height": 16, "width": 16}),
                        grid_size=Size({"height": 1, "width": 1}),
                    ),
                    coordinates=Position({"x": 0, "y": 0}),
                ),
                size=Size({"height": 16*4, "width": 16*4}),
                position=Position({"x": 100, "y": 50}),
                printer=self._printer,
            ),
            SpriteComponent(
                sprite=Sprite(
                    sprite_grid=SpriteSheet(
                        file_path=Path(
                            "../../../../../seagulls-rpg-demo/seagulls_assets/sprites/"
                            "rpg/rpg-urban-tilemap.packed.png"),
                        resolution=Size({"height": 288, "width": 432}),
                        grid_size=Size({"height": 18, "width": 27}),
                    ),
                    coordinates=Position({"x": 26, "y": random.randint(15, 17)}),
                ),
                size=Size({"height": 16*4, "width": 16*4}),
                position=Position({"x": 200, "y": 400}),
                printer=self._printer,
            ),
            SpriteComponent(
                sprite=Sprite(
                    sprite_grid=SpriteSheet(
                        file_path=Path(
                            "../../../../../seagulls-rpg-demo/seagulls_assets/sprites/"
                            "rpg/rpg-urban-tilemap.packed.png"),
                        resolution=Size({"height": 288, "width": 432}),
                        grid_size=Size({"height": 18, "width": 27}),
                    ),
                    coordinates=Position({"x": 21, "y": 13}),
                ),
                size=Size({"height": 16*4, "width": 16*4}),
                position=Position({"x": 20, "y": 400}),
                printer=self._printer,
            ),
            SpriteComponent(
                sprite=Sprite(
                    sprite_grid=SpriteSheet(
                        file_path=Path(
                            "../../../../../seagulls-rpg-demo/seagulls_assets/sprites/"
                            "rpg/rpg-urban-tilemap.packed.png"),
                        resolution=Size({"height": 288, "width": 432}),
                        grid_size=Size({"height": 1, "width": 1}),
                    ),
                    coordinates=Position({"x": 0, "y": 0}),
                ),
                size=Size({"height": 288, "width": 432}),
                position=Position({"x": 0, "y": 50}),
                printer=self._printer,
            ),
        ]

        for rect, coordinates in self._get_sprite_sheet_rects():
            if rect.collidepoint(pygame.mouse.get_pos()):
                coords_pos = coordinates.get()
                print(f"Highlighted Cell: {coords_pos}")
                items.append(
                    BoxComponent(
                        color=Color({"r": 1, "g": 0, "b": 0}),
                        size=Size({
                            "height": 16,
                            "width": 16,
                        }),
                        border_size=2,
                        position=Position(
                            {"x": coords_pos["x"] * 16, "y": 50 + coords_pos["y"] * 16}),
                        printer=self._printer,
                    ),
                )

        return tuple(items)

    @lru_cache()
    def _get_sprite_sheet_rects(self) -> Tuple[Tuple[Rect, Position], ...]:
        items = []

        for x in range(27):
            for y in range(18):
                rect_position = self._camera.adjust_position(
                    Position({"x": 16 * x, "y": 50 + (16 * y)})).get()

                items.append((
                    Rect((rect_position["x"], rect_position["y"]), (16, 16)),
                    Position({"x": x, "y": y}),
                ))

        return tuple(items)
