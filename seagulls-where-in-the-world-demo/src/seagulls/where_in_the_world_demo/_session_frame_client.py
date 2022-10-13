from typing import Tuple, Iterator

import pygame

from ._executable import IExecutable, executable
from ._session_state_client import GameSessionStateClient


class GameSessionFrameClient:

    _session_state_client: GameSessionStateClient
    _frame_stages: Tuple[IExecutable, ...]

    def __init__(
            self,
            session_state_client: GameSessionStateClient,
            frame_stages: Tuple[IExecutable, ...]) -> None:
        self._session_state_client = session_state_client
        self._frame_stages = frame_stages

    def frames(self) -> Iterator[IExecutable]:
        while self._session_state_client.is_running():
            yield executable(self._tick)

    def _tick(self) -> None:
        for stage in self._frame_stages:
            stage.execute()
        pygame.display.flip()
