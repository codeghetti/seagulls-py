from typing import Tuple

from dataclasses import dataclass

from seagulls.cat_demos.engine._input import InputEvent


class QuitGameEvent:
    pass


@dataclass(frozen=True)
class PlayerMoveEvent:
    direction: Tuple[int, int]


class GameInputs:
    QUIT = InputEvent[QuitGameEvent]("quit-game")
    MOVE = InputEvent[PlayerMoveEvent]("player-move")
