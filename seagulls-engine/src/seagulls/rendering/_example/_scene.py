import random

import pygame

from seagulls.pygame import WindowSurface
from seagulls.rendering import SizeDict, Color, Size, Position
from seagulls.rendering._camera import Camera
from seagulls.rendering._position import IUpdatePosition
from seagulls.rendering._renderable_component import IProvideRenderables
from seagulls.scene import IGameScene, IProvideGameScenes
from seagulls.session import IProvideGameSessions


class MyScene(IGameScene):

    _session: IProvideGameSessions
    _camera: Camera
    _renderables: IProvideRenderables
    _resoution_settings: WindowSurface
    _scene_size: SizeDict
    _camera_position: IUpdatePosition

    def __init__(
            self,
            session: IProvideGameSessions,
            camera: Camera,
            renderables: IProvideRenderables,
            window: WindowSurface,
            scene_size: SizeDict,
            camera_position: IUpdatePosition):
        self._session = session
        self._camera = camera
        self._renderables = renderables
        self._window = window
        self._scene_size = scene_size
        self._camera_position = camera_position

    def tick(self) -> None:
        self._camera.clear()

        # How do we move this logic out of scenes?
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                # How do we stop violating liskov substitution principle here?
                self._session.get().stop()
                return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                self._window.set_resolution({
                    "height": random.randint(100, 1200),
                    "width": random.randint(100, 1200),
                })
                self._window.update_window()
            if pygame.key.get_pressed()[pygame.K_LEFT]:
                self._camera_position.move_position((-5, 0))
            if pygame.key.get_pressed()[pygame.K_RIGHT]:
                self._camera_position.move_position((5, 0))
            if pygame.key.get_pressed()[pygame.K_UP]:
                self._camera_position.move_position((0, -5))
            if pygame.key.get_pressed()[pygame.K_DOWN]:
                self._camera_position.move_position((0, 5))

        self._set_scene_background()
        for component in self._renderables.get():
            component.render()

        self._camera.commit()

    def _set_scene_background(self) -> None:
        self._camera.print_square(Color({
            "r": 50,
            "g": 0,
            "b": 0}),
            Size(self._scene_size),
            Position({"x": 0, "y": 0}))


class SceneProvider(IProvideGameScenes):

    _scene: IGameScene

    def __init__(self, scene: IGameScene):
        self._scene = scene

    def get(self) -> IGameScene:
        return self._scene
