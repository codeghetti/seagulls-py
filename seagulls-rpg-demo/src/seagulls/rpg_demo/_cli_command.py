from argparse import ArgumentParser

import pygame
from seagulls.cli import ICliCommand
from seagulls.engine import IGameScene, IGameSession, ISetActiveScene


class GameCliCommand(ICliCommand):

    _game_session: IGameSession
    _active_scene_manager: ISetActiveScene
    _scene: IGameScene

    def __init__(
            self,
            game_session: IGameSession,
            active_scene_manager: ISetActiveScene,
            scene: IGameScene):
        self._game_session = game_session
        self._active_scene_manager = active_scene_manager
        self._scene = scene

    def configure_parser(self, parser: ArgumentParser) -> None:
        pass

    def execute(self) -> None:
        pygame.init()
        self._active_scene_manager.set_active_scene(self._scene)
        try:
            self._game_session.start()
            self._game_session.wait_for_completion()
        except KeyboardInterrupt:
            self._game_session.stop()
