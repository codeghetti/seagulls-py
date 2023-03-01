from typing import Tuple

from ._eventing import EventCallbackType, EventPayloadType, EventType


class GameInputClient:
    _handlers: Tuple[EventCallbackType, ...]

    def __init__(self, handlers: Tuple[EventCallbackType, ...]) -> None:
        self._handlers = handlers

    def trigger(self, event: EventType, payload: EventPayloadType) -> None:
        for handler in self._handlers:
            handler(event, payload)
