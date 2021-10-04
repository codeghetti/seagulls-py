import time
from threading import Thread, Event
import logging

import pygame
from seagulls.engine import IGameSession, IProvideGameScenes
from ._game_scene_manager import SeagullsGameSceneManager

logger = logging.getLogger(__name__)


class AsyncGameSession(IGameSession):

    _name: str
    _game_scene_manager: IProvideGameScenes
    _thread: Thread
    _stopped: Event

    def __init__(self, name: str) -> None:
        self._name = name
        self._game_scene_manager = SeagullsGameSceneManager()
        self._thread = Thread(target=self._thread_target)
        self._stopped = Event()

    def start(self) -> None:
        logger.debug(f"starting game session {self._name}")
        self._thread.start()

    def wait_for_completion(self) -> None:
        logger.debug(f"waiting for completion {self._name}")
        while not self._stopped.is_set():
            time.sleep(0.2)
        logger.debug(f"done waiting for completion {self._name}")

    def stop(self) -> None:
        logger.debug(f"stopping game session {self._name}")
        self._stopped.set()
        self._thread.join()

    def _thread_target(self) -> None:
        pygame.display.set_caption("Our Game")
        scene = self._game_scene_manager.get_scene(self._name)
        scene.start()

        while not self._stopped.is_set() and not scene.should_quit():
            scene.tick()
        logger.debug("exiting game session")
        self._stopped.set()
