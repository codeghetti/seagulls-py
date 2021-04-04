from abc import ABC, abstractmethod
from typing import Optional

from pygame.time import Clock


class GameTimeUpdater(ABC):
    @abstractmethod
    def update(self, framerate: int = 0) -> None:
        pass


class GameTimeProvider(ABC):
    @abstractmethod
    def get_time(self) -> int:
        pass

    @abstractmethod
    def get_fps(self) -> float:
        pass


class GameClock(GameTimeUpdater, GameTimeProvider):
    _clock: Clock
    _ticks: int
    _delta: int

    def __init__(self):
        self._clock = Clock()
        self._ticks = 0
        self._delta = 0

    def update(self, framerate: int = 0) -> None:
        self._delta = self._clock.tick(framerate)

    def get_time(self) -> int:
        return self._delta

    def get_fps(self) -> float:
        return self._clock.get_fps()
