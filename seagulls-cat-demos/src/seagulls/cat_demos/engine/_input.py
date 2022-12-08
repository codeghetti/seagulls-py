import pygame
from dataclasses import dataclass

from typing import List, Dict, TypeVar, Generic, Callable
from pygame.event import Event

from ._executables import IExecutable

InputEventType = TypeVar("InputEventType")


@dataclass(frozen=True)
class InputEvent(Generic[InputEventType]):
    name: str


class GameSessionInputClient:

    _pubs: List[IExecutable]
    _subs: Dict[InputEvent[InputEventType], List[Callable[[InputEventType], None]]]
    _events: List[Event]

    def __init__(self) -> None:
        self._pubs = []
        self._subs = {}
        self._events = []

    def publisher(self, exe: IExecutable) -> None:
        self._pubs.append(exe)

    def publish(self, event: InputEvent[InputEventType], payload: InputEventType) -> None:
        for x in self._subs.get(event, []):
            x(payload)

    def subscribe(
            self,
            event: InputEvent[InputEventType],
            cb: Callable[[InputEventType], None]) -> None:
        if event not in self._subs:
            self._subs[event] = []

        self._subs[event].append(cb)

    def tick(self) -> None:
        self._events = pygame.event.get()
        for x in self._pubs:
            x.execute()

    def was_key_pressed(self, key: int) -> bool:
        for event in self._events:
            if self._is_key_down_event(event, key):
                return True

        return False

    def was_key_released(self, key: int) -> bool:
        for event in self._events:
            if self._is_key_up_event(event, key):
                return True

        return False

    def was_mouse_button_pressed(self) -> bool:
        for event in self._events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                return True

        return False

    def was_mouse_button_released(self) -> bool:
        for event in self._events:
            if event.type == pygame.MOUSEBUTTONUP:
                return True

        return False

    def _is_key_down_event(self, event: Event, key: int) -> bool:
        return event.type == pygame.KEYDOWN and event.key == key

    def _is_key_up_event(self, event: Event, key: int) -> bool:
        return event.type == pygame.KEYUP and event.key == key
