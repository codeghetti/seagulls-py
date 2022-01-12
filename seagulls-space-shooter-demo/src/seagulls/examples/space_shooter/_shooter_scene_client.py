from enum import Enum, auto


class ShooterSceneState(Enum):
    RUNNING = auto()
    WON = auto()
    LOST = auto()


class ShooterSceneStateClient:
    _current_state: ShooterSceneState

    def __init__(self):
        self._current_state = ShooterSceneState.RUNNING

    def update_state(self, state: ShooterSceneState) -> None:
        self._current_state = state

    def get_state(self) -> ShooterSceneState:
        return self._current_state
