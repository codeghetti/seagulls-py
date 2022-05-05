import logging
from pathlib import Path

from seagulls.pygame import WindowSurface
from seagulls.rendering import (
    Color,
    IPrinter,
    Position,
    Size,
    Sprite,
    SpriteComponent,
    SpriteSheet
)
from seagulls.scene import IGameScene, IProvideGameScenes
from seagulls.session import IProvideGameSessions

logger = logging.getLogger(__name__)


class RpgScene2(IGameScene):

    _session: IProvideGameSessions
    _printer: IPrinter

    def __init__(
            self,
            session: IProvideGameSessions,
            printer: IPrinter,
            window: WindowSurface):
        self._session = session
        self._printer = printer
        self._window = window
        pass

    def tick(self) -> None:
        tree_sprite = SpriteComponent(
            sprite=Sprite(
                sprite_grid=SpriteSheet(
                    file_path=Path(
                        "seagulls_assets/sprites/environment/"
                        "rpg-environment/island-tree.png"),
                    resolution=Size({"height": 16, "width": 16}),
                    grid_size=Size({"height": 1, "width": 1}),
                ),
                coordinates=Position({"x": 0, "y": 0}),
            ),
            size=Size({"height": 64, "width": 64}),
            position=Position({"x": 200, "y": 50}),
            printer=self._printer,
        )

        tree_sprite.render()

        red_house_sprite = SpriteComponent(
            sprite=Sprite(
                sprite_grid=SpriteSheet(
                    file_path=Path(
                        "seagulls_assets/sprites/environment/"
                        "rpg-environment/island-red-home.png"),
                    resolution=Size({"height": 16, "width": 16}),
                    grid_size=Size({"height": 1, "width": 1}),
                ),
                coordinates=Position({"x": 0, "y": 0}),
            ),
            size=Size({"height": 64, "width": 64}),
            position=Position({"x": 264, "y": 50}),
            printer=self._printer,
        )

        red_house_sprite.render()

        self._printer.print_square(
            Color({"r": 155, "g": 155, "b": 155}),
            Size({"height": 100, "width": 100}),
            Position({"x": 10, "y": 10})
        )

        self._printer.commit()


class SceneProvider(IProvideGameScenes):

    _scene: IGameScene

    def __init__(self, scene: IGameScene):
        self._scene = scene

    def get(self) -> IGameScene:
        return self._scene
