import logging
import random
from dataclasses import dataclass
from functools import cache
from typing import Tuple

import pygame

from seagulls.pygame import PygameSquarePrinter, WindowSurface
from seagulls.rendering import (
    IClearPrinters,
    IGameScreen,
    IPrintSquares,
    IProvideGameScreens
)
from seagulls.rendering._camera import Camera
from seagulls.rendering._color import Color
from seagulls.rendering._position import Position
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
        self._printer.render(self._color, self._size, self._position)


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
        self._set_caption()
        self._scene.get().tick()
        pygame.display.flip()

    @cache
    def _set_caption(self) -> None:
        pygame.display.set_caption("Our Game")


class ScreenProvider(IProvideGameScreens):

    def __init__(self, screen: IGameScreen):
        self._screen = screen

    def get(self) -> IGameScreen:
        return self._screen


class MyRenderables(IProvideRenderables):

    _printer: IPrintSquares

    def __init__(self, printer: IPrintSquares):
        self._printer = printer

    def get(self) -> Tuple[RenderableComponent, ...]:
        color = Color({
            "r": random.randint(0, 255),
            "g": random.randint(0, 255),
            "b": random.randint(0, 255),
        })
        size = Size({
            "height": 1,
            "width": 1,
        })
        position = Position({
            "x": random.randint(100, 400),
            "y": random.randint(100, 400),
        })
        return tuple([
            SolidColorComponent(
                color=color,
                size=size,
                position=position,
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

    def __init__(
            self,
            session: IProvideGameSessions,
            printer: IPrintSquares,
            clearer: IClearPrinters,
            renderables: IProvideRenderables,
            resoution_settings: WindowSurface):
        self._session = session
        self._printer = printer
        self._clearer = clearer
        self._renderables = renderables
        self._resoution_settings = resoution_settings

    def tick(self) -> None:
        # self._clearer.clear()

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

        for component in self._renderables.get():
            component.render()


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
        window_size={"height": 500, "width": 500},
        scene_size={"height": 500, "width": 500},
        camera_size={"height": 500, "width": 500},
    )

    # Printers "print" onto surfaces
    surface_provider = WindowSurface(video_settings.window_size)
    surface_provider.initialize()
    # These two classes are pygame specific implementations
    printer = PygameSquarePrinter(surface_provider)

    camera = Camera(
        square_renderer=printer,
        clearer=printer,
        # If camera size does not match scene size, some objects skip rendering
        size=Size(video_settings.camera_size),
        # If the camera does not start at 0, 0, we also skip rendering some objects
        position=Position({"x": 0, "y": 0}),
    )

    # Objects with a render() method are provided by this class
    renderables = MyRenderables(camera)

    # A session is one execution of the game
    # Sessions run until the game is exited
    session_provider = MySessionProvider(NullGameSession())

    # Scenes are the game's "levels" but could be the main menu scene too
    scene = MyScene(
        session=session_provider,
        printer=camera,
        clearer=camera,
        renderables=renderables,
        resoution_settings=surface_provider)
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
