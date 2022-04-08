import logging
import random
from abc import abstractmethod
from functools import cache
from typing import Protocol, Tuple

import pygame
from pygame import Surface

from seagulls.rendering import IGameScreen, IProvideGameScreens
from seagulls.rendering._color import Color
from seagulls.rendering._position import Position
from seagulls.rendering._printer import Printer
from seagulls.rendering._renderable_component import (
    IProvideRenderables,
    RenderableComponent
)
from seagulls.rendering._size import Size
from seagulls.scene import IGameScene, IProvideGameScenes
from seagulls.session import (
    BlockingGameSession,
    IGameSession,
    IProvideGameSessions,
    IStopGameSessions,
    NullGameSession
)

logger = logging.getLogger(__name__)


class GameObject:
    pass


class GameComponent:
    pass


class IProvideSurfaces(Protocol):
    """Move this into seagulls.pygame?"""

    @abstractmethod
    def get(self) -> Surface:
        """"""


class WindowSurfaceProvider(IProvideSurfaces):

    def get(self) -> Surface:
        return self._get_window()

    @cache
    def _get_window(self) -> Surface:
        return pygame.display.set_mode((0, 0), pygame.FULLSCREEN)


class PygamePrinter(Printer):
    """Move this into seagulls.pygame?"""

    _surface: IProvideSurfaces

    def __init__(self, surface: IProvideSurfaces):
        self._surface = surface

    def render(self, color: Color, size: Size, position: Position):
        c = color.get()
        s = size.get()
        p = position.get()

        square = Surface((s["width"], s["height"]))
        square.fill((c["r"], c["g"], c["b"]))
        self._surface.get().blit(square, (p["x"], p["y"]))

    def clear(self) -> None:
        self._surface.get().fill((0, 0, 0))


class SolidColorComponent(RenderableComponent):

    _color: Color
    _size: Size
    _position: Position
    _printer: Printer

    def __init__(self, color: Color, size: Size, position: Position, printer: Printer):
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

    _printer: Printer

    def __init__(self, printer: Printer):
        self._printer = printer

    def get(self) -> Tuple[RenderableComponent, ...]:
        color = Color({
            "r": random.randint(0, 255),
            "g": random.randint(0, 255),
            "b": random.randint(0, 255),
        })
        size = Size({
            "height": random.randint(1, 500),
            "width": random.randint(1, 500),
        })
        position = Position({
            "x": random.randint(0, 500),
            "y": random.randint(0, 500),
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


class MyScene(IGameScene):

    _session: IProvideGameSessions
    _printer: Printer
    _renderables: IProvideRenderables

    def __init__(
            self, session: IProvideGameSessions, printer: Printer, renderables: IProvideRenderables):
        self._session = session
        self._printer = printer
        self._renderables = renderables

    def tick(self) -> None:
        self._printer.clear()

        # How do we move this logic out of scenes?
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                # How do we stop violating liskov substitution principle here?
                self._session.get().stop()
                return

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


def _test() -> None:
    # Printers "print" onto surfaces
    surface_provider = WindowSurfaceProvider()
    # These two classes are pygame specific implementations
    printer = PygamePrinter(surface_provider)

    # Objects with a render() method are provided by this class
    renderables = MyRenderables(printer)

    # A session is one execution of the game
    # Sessions run until the game is exited
    session_provider = MySessionProvider(NullGameSession())

    # Scenes are the game's "levels" but could be the main menu scene too
    scene = MyScene(session_provider, printer, renderables)
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
        session.start()
    except KeyboardInterrupt:
        session.stop()


_test()
