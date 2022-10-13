from enum import Enum, auto


class GameSessionState(Enum):
    STOPPED = auto()
    RUNNING = auto()


class GameSessionStateClient:

    _state: GameSessionState

    def __init__(self) -> None:
        self._state = GameSessionState.STOPPED

    def get_state(self) -> GameSessionState:
        return self._state

    def is_running(self) -> bool:
        return self._state == GameSessionState.RUNNING

    def is_stopped(self) -> bool:
        return self._state == GameSessionState.STOPPED

    def set_running(self) -> None:
        self._state = GameSessionState.RUNNING

    def set_stopped(self) -> None:
        self._state = GameSessionState.STOPPED
