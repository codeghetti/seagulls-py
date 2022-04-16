import logging
import random
from dataclasses import dataclass
from functools import lru_cache
from typing import Tuple

import pygame

from seagulls.pygame import PygameSquarePrinter, WindowSurface, PygameSurface
from seagulls.rendering import (
    IClearPrinters,
    IGameScreen,
    IPrintSquares,
    IProvideGameScreens
)
from seagulls.rendering._camera import Camera
from seagulls.rendering._color import Color
from seagulls.rendering._position import Position, IUpdatePosition
from seagulls.rendering._renderable_component import (
    IProvideRenderables,
    RenderableComponent
)
from seagulls.rendering._size import Size, SizeDict
from seagulls.scene import IGameScene, IProvideGameScenes
from seagulls.session import (
    BlockingGameSession,
    IGameSession,
    IProvideGameSessions,
    IStopGameSessions,
    NullGameSession
)

logger = logging.getLogger(__name__)


class SolidColorComponent(RenderableComponent):

    _color: Color
    _size: Size
    _position: Position
    _printer: IPrintSquares

    def __init__(self, color: Color, size: Size, position: Position, printer: IPrintSquares):
        self._color = color
        self._size = size
        self._position = position
        self._printer = printer

    def render(self) -> None:
        self._printer.print(self._color, self._size, self._position)


class SceneProvider(IProvideGameScenes):

    _scene: IGameScene

    def __init__(self, scene: IGameScene):
        self._scene = scene

    def get(self) -> IGameScene:
        return self._scene


class PygameScreen:
    _scene: SceneProvider

    def __init__(self, scene: SceneProvider):
        self._scene = scene

    def refresh(self) -> None:
        self._scene.get().tick()


class ScreenProvider(IProvideGameScreens):

    def __init__(self, screen: IGameScreen):
        self._screen = screen

    def get(self) -> IGameScreen:
        return self._screen


class MyRenderables(IProvideRenderables):

    _printer: IPrintSquares
    _scene_size: SizeDict

    def __init__(self, printer: IPrintSquares, scene_size: SizeDict):
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
        ])


class MySessionStopper(IStopGameSessions):

    _session: IStopGameSessions

    def __init__(self, session: IStopGameSessions):
        self._session = session

    def wait_for_completion(self) -> None:
        raise RuntimeError("Can't wait for completion?")

    def stop(self) -> None:
        self._session.stop()


class MyResolutionSettings:
    _window: WindowSurface

    def __init__(self, window: WindowSurface):
        self._window = window


class MyScene(IGameScene):

    _session: IProvideGameSessions
    _printer: IPrintSquares
    _clearer: IClearPrinters
    _renderables: IProvideRenderables
    _resoution_settings: WindowSurface
    _scene_size: SizeDict
    _camera_position: IUpdatePosition

    def __init__(
            self,
            session: IProvideGameSessions,
            printer: IPrintSquares,
            clearer: IClearPrinters,
            renderables: IProvideRenderables,
            resoution_settings: WindowSurface,
            scene_size: SizeDict,
            camera_position: IUpdatePosition):
        self._session = session
        self._printer = printer
        self._clearer = clearer
        self._renderables = renderables
        self._resoution_settings = resoution_settings
        self._scene_size = scene_size
        self._camera_position = camera_position

    def tick(self) -> None:
        # How do we move this logic out of scenes?
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                # How do we stop violating liskov substitution principle here?
                self._session.get().stop()
                return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                self._resoution_settings.set_resolution({
                    "height": random.randint(100, 700),
                    "width": random.randint(100, 700),
                })
                self._resoution_settings.update_window()
            if pygame.key.get_pressed()[pygame.K_LEFT]:
                self._camera_position.move_position((-5, 0))
                self._clearer.clear()
                self._black_background.cache_clear()
            if pygame.key.get_pressed()[pygame.K_RIGHT]:
                self._camera_position.move_position((5, 0))
                self._clearer.clear()
                self._black_background.cache_clear()
            if pygame.key.get_pressed()[pygame.K_UP]:
                self._camera_position.move_position((0, -5))
                self._clearer.clear()
                self._black_background.cache_clear()
            if pygame.key.get_pressed()[pygame.K_DOWN]:
                self._camera_position.move_position((0, 5))
                self._clearer.clear()
                self._black_background.cache_clear()

        self._black_background()
        for component in self._renderables.get():
            component.render()

        self._printer.commit()

    @lru_cache()
    def _black_background(self) -> None:
        self._printer.print(Color({
            "r": 0,
            "g": 0,
            "b": 0}),
            Size(self._scene_size),
            Position({"x": 0, "y": 0}))


class MySessionProvider(IProvideGameSessions):
    _session: IGameSession

    def __init__(self, session: IGameSession):
        self._session = session

    def set(self, session: IGameSession) -> None:
        self._session = session

    def get(self) -> IGameSession:
        return self._session


@dataclass(frozen=True)
class VideoSettings:
    window_size: SizeDict
    scene_size: SizeDict
    camera_size: SizeDict


def _test() -> None:
    video_settings = VideoSettings(
        window_size={"width": 1000, "height": 1000},
        scene_size={"height": 500, "width": 500},
        camera_size={"height": 700, "width": 500},
    )

    # Printers "print" onto surfaces
    surface_provider = WindowSurface(video_settings.window_size, video_settings.camera_size)
    surface_provider.initialize()

    camera_surface_provider = PygameSurface(
        surface_provider,
        video_settings.camera_size,
        (230, 230, 250))
    # These two classes are pygame specific implementations
    printer = PygameSquarePrinter(surface_provider)

    camera_printer = PygameSquarePrinter(camera_surface_provider)

    camera = Camera(
        square_renderer=camera_printer,
        clearer=printer,
        # If camera size does not match scene size, some objects skip rendering
        size=Size(video_settings.camera_size),
        # If the camera does not start at 0, 0, we also skip rendering some objects
        position=Position({"x": 0, "y": 0}),
    )

    # Objects with a render() method are provided by this class
    renderables = MyRenderables(camera, video_settings.scene_size)

    # A session is one execution of the game
    # Sessions run until the game is exited
    session_provider = MySessionProvider(NullGameSession())

    # Scenes are the game's "levels" but could be the main menu scene too
    scene = MyScene(
        session=session_provider,
        printer=camera,
        clearer=camera,
        renderables=renderables,
        resoution_settings=surface_provider,
        scene_size=video_settings.scene_size,
        camera_position=camera,
    )
    # Our scene uses the session provider to exit but we could move that somewhere else
    # This is the reason for the `NullGameSession`
    scene_provider = SceneProvider(scene)

    # Sessions refresh "screens" which typically render a scene
    screen = PygameScreen(scene_provider)
    screen_provider = ScreenProvider(screen)

    # Sessions just need a screen to constantly call refresh() on
    session = BlockingGameSession(screen_provider)
    session_provider.set(session)
    try:
        # Since this is blocking, one of the active scene objects must call stop()
        pygame.init()
        session.start()
    except KeyboardInterrupt:
        session.stop()


_test()
