from pygame.time import Clock

from ._game_object import GameObject
from ._pyagme import Surface


class GameClock(GameObject):
    _clock: Clock
    _ticks: int
    _delta: int

    def __init__(self):
        self._clock = Clock()
        self._ticks = 0
        self._delta = 0

    def tick(self) -> None:
        self._delta = self._clock.tick()

    def render(self, surface: Surface) -> None:
        pass

    def get_time(self) -> int:
        return self._delta

    def get_fps(self) -> float:
        return self._clock.get_fps()
