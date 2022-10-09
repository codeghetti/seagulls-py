import logging

import pygame.mouse
from seagulls.pygame import WindowSurface
from seagulls.rendering import Camera, IPrinter, Position
from seagulls.scene import IGameScene, IProvideGameScenes
from seagulls.session import IProvideGameSessions

from seagulls.rpg_demo._sprite_client import SpriteClient, Sprites

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
            camera: Camera,
            sprite_client: SpriteClient):
        self._session = session
        self._printer = printer
        self._window = window
        self._camera = camera
        self._sprite_client = sprite_client

    def tick(self) -> None:
        self._printer.clear()

        self._sprite_client.render_sprite(
            Sprites.island_water,
            Position({"x": 0, "y": 0})
        )

        self._sprite_client.render_sprite(Sprites.island_tree, Position({"x": 200, "y": 50}))
        self._sprite_client.render_sprite(Sprites.island_tree, Position({"x": 100, "y": 50}))
        self._sprite_client.render_sprite(Sprites.island_tree, Position({"x": 400, "y": 50}))
        self._sprite_client.render_sprite(Sprites.island_tree, Position({"x": 200, "y": 150}))

        self._sprite_client.render_sprite(Sprites.island_red_home, Position({"x": 264, "y": 50}))

        self._sprite_client.render_sprite(Sprites.jeffrey_standing, Position({"x": 350, "y": 60}))

        pygame.event.get()

        adjusted_position = self._camera.adjust_position(
            Position(
                {"x": pygame.mouse.get_pos()[0],
                 "y": pygame.mouse.get_pos()[1]}))

        self._sprite_client.render_sprite(
            Sprites.cursor_sword_bronze,
            adjusted_position)

        self._printer.commit()


class SceneProvider(IProvideGameScenes):

    _scene: IGameScene

    def __init__(self, scene: IGameScene):
        self._scene = scene

    def get(self) -> IGameScene:
        return self._scene
