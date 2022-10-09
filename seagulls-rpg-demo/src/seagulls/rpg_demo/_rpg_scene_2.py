import logging
from pathlib import Path

import pygame.mouse
from seagulls.pygame import WindowSurface
from seagulls.rendering import (
    Camera,
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
    _camera: Camera

    def __init__(
            self,
            session: IProvideGameSessions,
            printer: IPrinter,
            window: WindowSurface,
            camera: Camera):
        self._session = session
        self._printer = printer
        self._window = window
        self._camera = camera

    def tick(self) -> None:
        self._printer.clear()

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

        pygame.event.get()

        adjusted_position = self._camera.adjust_position(
            Position(
                {"x": pygame.mouse.get_pos()[0],
                 "y": pygame.mouse.get_pos()[1]}))

        cursor_sprite = SpriteComponent(
            sprite=Sprite(
                sprite_grid=SpriteSheet(
                    file_path=Path(
                        "seagulls_assets/sprites/environment/"
                        "rpg-environment/cursor-sword-bronze.png"),
                    resolution=Size({"height": 37, "width": 34}),
                    grid_size=Size({"height": 1, "width": 1}),
                ),
                coordinates=Position({"x": 0, "y": 0}),
            ),
            size=Size({"height": 64, "width": 64}),
            position=adjusted_position,
            printer=self._printer,
        )

        cursor_sprite.render()

        logger.warning(f"{pygame.mouse.get_pos()}")
        logger.warning(f"adjusted position: {adjusted_position.get()}")

        self._printer.commit()


class SceneProvider(IProvideGameScenes):

    _scene: IGameScene

    def __init__(self, scene: IGameScene):
        self._scene = scene

    def get(self) -> IGameScene:
        return self._scene
