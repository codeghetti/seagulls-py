import logging

import pygame
from ._game_session import IGameSession
from ._game_scene_manager import IProvideGameScenes

logger = logging.getLogger(__name__)


class BlockingGameSession(IGameSession):
    _scene_manager: IProvideGameScenes

    def __init__(self, scene_manager: IProvideGameScenes) -> None:
        self._scene_manager = scene_manager

    def start(self) -> None:
        logger.debug("starting game session")
        pygame.display.set_caption("Our Game")
        scene = self._scene_manager.get_scene()
        scene.start()

        while not scene.should_quit():
            scene.tick()
        logger.debug("exiting game session")

    def wait_for_completion(self) -> None:
        pass

    def stop(self) -> None:
        pass
