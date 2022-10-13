from enum import Enum, auto


class GameState(Enum):
    MENU = auto()
    LEVEL = auto()
    LEVEL_END = auto()
    GAME_END = auto()
