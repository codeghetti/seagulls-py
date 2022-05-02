import logging
from threading import Event

from seagulls.rendering import IProvideGameScreens

from ._game_session import IGameSession

logger = logging.getLogger(__name__)


class BlockingGameSession(IGameSession):
    _screen_provider: IProvideGameScreens
    _should_quit: Event

    def __init__(self, screen_provider: IProvideGameScreens) -> None:
        self._screen_provider = screen_provider
        self._should_quit = Event()

    def start(self) -> None:
        logger.debug("starting game session")
        screen = self._screen_provider.get()

        while not self._should_quit.is_set():
            screen.refresh()
        logger.debug("exiting game session")

    def wait_for_completion(self) -> None:
        """not sure if this belongs"""
        pass

    def stop(self) -> None:
        self._should_quit.set()
