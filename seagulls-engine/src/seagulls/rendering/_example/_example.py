import logging

import pygame

from seagulls.pygame import PygamePrinter, PygameSurface, WindowSurface
from seagulls.pygame._printer import PygameCameraPrinter
from seagulls.rendering._camera import Camera
from seagulls.rendering._example._pygame_screen import PygameScreen
from seagulls.rendering._example._renderables import MyRenderables
from seagulls.rendering._example._scene import MyScene, SceneProvider
from seagulls.rendering._example._screen_provider import ScreenProvider
from seagulls.rendering._example._session import MySessionProvider
from seagulls.rendering._example._settings import VideoSettings
from seagulls.rendering._position import Position
from seagulls.rendering._size import Size
from seagulls.session import BlockingGameSession, NullGameSession

logger = logging.getLogger(__name__)


def _test() -> None:
    video_settings = VideoSettings(
        window_size={"height": 800, "width": 1200},
        scene_size={"height": 500, "width": 500},
        camera_size={"height": 500, "width": 500},
    )

    # Printers "print" onto surfaces
    surface_provider = WindowSurface(video_settings.window_size, video_settings.camera_size)
    surface_provider.initialize()

    camera_surface_provider = PygameSurface(
        surface_provider,
        video_settings.camera_size,
        (70, 70, 150))

    printer = PygamePrinter(camera_surface_provider)

    camera = Camera(
        printer=printer,
        # If camera size does not match scene size, some objects skip rendering
        size=Size(video_settings.camera_size),
        # If the camera does not start at 0, 0, we also skip rendering some objects
        position=Position({"x": 0, "y": 0}),
    )

    camera_printer = PygameCameraPrinter(
        surface=camera_surface_provider,
        camera=camera,
    )

    # Objects with a render() method are provided by this class
    renderables = MyRenderables(
        camera_printer,
        video_settings.scene_size)

    # A session is one execution of the game
    # Sessions run until the game is exited
    session_provider = MySessionProvider(NullGameSession())

    # Scenes are the game's "levels" but could be the main menu scene too
    scene = MyScene(
        session=session_provider,
        camera=camera,
        renderables=renderables,
        window=surface_provider,
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
