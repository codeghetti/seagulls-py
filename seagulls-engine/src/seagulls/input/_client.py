from abc import abstractmethod
from typing import Protocol, List

import pygame
from pygame.event import Event


class IUpdateInputState(Protocol):
    @abstractmethod
    def update(self) -> None:
        pass


class IProvideInputState(Protocol):
    pass


class IManageInputState(IUpdateInputState, IProvideInputState, Protocol):
    pass


class GameInputClient(IManageInputState):

    _events: List[Event]

    def __init__(self) -> None:
        self._events = []

    def update(self) -> None:
        self._events = pygame.event.get()
