from abc import ABC, abstractmethod

from pygame.time import Clock


class GameTimeUpdater(ABC):
    @abstractmethod
    def update(self) -> None:
        pass


class GameTimeProvider(ABC):
    @abstractmethod
    def get_time(self) -> int:
        pass


class GameClock(GameTimeUpdater, GameTimeProvider):
    _clock: Clock
    _ticks: int
    _delta: int

    def __init__(self):
        self._clock = Clock()
        self._ticks = 0
        self._delta = 0

    def update(self) -> None:
        self._delta = self._clock.tick()

    def get_time(self) -> int:
        return self._delta
