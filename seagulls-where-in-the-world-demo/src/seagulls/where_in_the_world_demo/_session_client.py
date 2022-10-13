from typing import Tuple

from ._executable import IExecutable
from ._session_frame_client import GameSessionFrameClient
from ._session_state_client import GameSessionStateClient
from ._session_window_client import GameSessionWindowClient


class InitializeGameSessionCommand:

    _session_state_client: GameSessionStateClient
    _session_window_client: GameSessionWindowClient

    def __init__(
            self,
            session_state_client: GameSessionStateClient,
            session_window_client: GameSessionWindowClient) -> None:
        self._session_state_client = session_state_client
        self._session_window_client = session_window_client

    def execute(self) -> None:
        self._session_window_client.open()
        self._session_state_client.set_running()


class RunGameLoopCommand:

    session_frame_client: GameSessionFrameClient

    def __init__(self, session_frame_client: GameSessionFrameClient) -> None:
        self._session_frame_client = session_frame_client

    def execute(self) -> None:
        for frame in self._session_frame_client.frames():
            frame.execute()


class ShutdownGameSessionCommand:

    _session_state_client: GameSessionStateClient
    _session_window_client: GameSessionWindowClient

    def __init__(
            self,
            session_state_client: GameSessionStateClient,
            session_window_client: GameSessionWindowClient) -> None:
        self._session_state_client = session_state_client
        self._session_window_client = session_window_client

    def execute(self) -> None:
        self._session_window_client.close()
        self._session_state_client.set_stopped()


class GameSessionClient:

    _session_stages: Tuple[IExecutable, ...]

    def __init__(self, session_stages: Tuple[IExecutable, ...]) -> None:
        self._session_stages = session_stages

    def run(self) -> None:
        for stage in self._session_stages:
            stage.execute()
