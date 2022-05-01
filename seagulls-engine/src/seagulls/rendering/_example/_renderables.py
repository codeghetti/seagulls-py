import random
from pathlib import Path
from typing import Tuple

from seagulls.rendering import Color, IPrinter, Position, Size, SizeDict
from seagulls.rendering._example._components import (
    SolidColorComponent,
    SpriteComponent
)
from seagulls.rendering._renderable_component import (
    IProvideRenderables,
    RenderableComponent
)
from seagulls.rendering._sprite import Sprite, SpriteGrid


class MyRenderables(IProvideRenderables):

    _printer: IPrinter
    _scene_size: SizeDict

    def __init__(
            self,
            printer: IPrinter,
            scene_size: SizeDict):
        self._printer = printer
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
            "x": random.randint(self._scene_size["width"] - 50,
                                self._scene_size["width"]),

            "y": random.randint(self._scene_size["height"] - 50,
                                self._scene_size["height"]),
        })
        return tuple([
            SolidColorComponent(
                color=color,
                size=size,
                position=position1,
                printer=self._printer,
            ),
            SolidColorComponent(
                color=color,
                size=size,
                position=position2,
                printer=self._printer,
            ),
            SpriteComponent(
                sprite=Sprite(
                    sprite_grid=SpriteGrid(
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
                    sprite_grid=SpriteGrid(
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
                    sprite_grid=SpriteGrid(
                        file_path=Path(
                            "../../../../../seagulls-rpg-demo/seagulls_assets/sprites/"
                            "rpg/rpg-urban-tilemap.packed.png"),
                        resolution=Size({"height": 288, "width": 432}),
                        grid_size=Size({"height": 18, "width": 27}),
                    ),
                    coordinates=Position({"x": 26, "y": 17}),
                ),
                size=Size({"height": 16*4, "width": 16*4}),
                position=Position({"x": 200, "y": 250}),
                printer=self._printer,
            ),
        ])
