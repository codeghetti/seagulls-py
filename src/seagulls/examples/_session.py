import logging
import time
from threading import Thread, Event

import pygame
from seagulls.engine import IGameSession, IProvideGameScenes

logger = logging.getLogger(__name__)


class AsyncGameSession(IGameSession):
    _scene_manager: IProvideGameScenes
    _thread: Thread
    _stopped: Event

    def __init__(self, scene_manager: IProvideGameScenes) -> None:
        self._scene_manager = scene_manager

        self._thread = Thread(target=self._thread_target)
        self._stopped = Event()

    def start(self) -> None:
        logger.debug(f"starting game session")
        self._thread.start()

    def wait_for_completion(self) -> None:
        logger.debug(f"waiting for completion")
        while not self._stopped.is_set():
            time.sleep(0.1)
        logger.debug(f"done waiting for completion")

    def stop(self) -> None:
        logger.debug(f"stopping game session")
        self._stopped.set()
        self._thread.join()

    def _thread_target(self) -> None:
        pygame.display.set_caption("Our Game")
        scene = self._scene_manager.get_scene()
        scene.start()

        while not self._stopped.is_set() and not scene.should_quit():
            scene.tick()
        logger.debug("exiting game session")
        self._stopped.set()
