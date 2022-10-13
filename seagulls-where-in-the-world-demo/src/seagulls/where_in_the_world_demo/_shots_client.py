from typing import List, Tuple, NamedTuple

from ._position import Position


class Shot(NamedTuple):
    player: int
    level: int
    position: Position


class ShotsClient:
    _shots: List[Shot]

    def __init__(self) -> None:
        self._shots = []

    def add(self, shot: Shot) -> None:
        self._shots.append(shot)

    def get_player_level_shot(self, player: int, level: int) -> Shot:
        for shot in self.get_level_shots(level):
            if shot.player == player:
                return shot

        raise RuntimeError(f"Player[{player}] / Level[{level}] shot not found.")

    def get_level_shots(self, level: int) -> Tuple[Shot, ...]:
        result = [shot for shot in self._shots if shot.level == level]
        return tuple(result)

    def get_player_shots(self, player: int) -> Tuple[Shot, ...]:
        result = [shot for shot in self._shots if shot.player == player]
        return tuple(result)
