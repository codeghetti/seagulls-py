from argparse import ArgumentParser

import pygame
from seagulls.cli import ICliCommand
from seagulls.pygame import WindowSurface
from seagulls.scene import IGameScene
from seagulls.session import BlockingGameSession, NullGameSessionError


class GameCliCommand(ICliCommand):

    _game_session: BlockingGameSession
    _scene: IGameScene
    _window: WindowSurface

    def __init__(
            self,
            game_session: BlockingGameSession,
            scene: IGameScene,
            window: WindowSurface):
        self._game_session = game_session
        self._scene = scene
        self._window = window

    def configure_parser(self, parser: ArgumentParser) -> None:
        pass

    def execute(self) -> None:
        pygame.init()
        pygame.mouse.set_visible(False)

        self._window.initialize()
        try:
            self._game_session.start()
        except KeyboardInterrupt:
            self._game_session.stop()
        except NullGameSessionError:
            pass
