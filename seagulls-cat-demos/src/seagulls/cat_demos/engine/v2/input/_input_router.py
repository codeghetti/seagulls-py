from typing import Any, Callable, Dict, Tuple

from ._eventing import EventPayloadType, EventType, InputEvent


class GameInputRouter:

    _subscribers: Dict[InputEvent[Any], Tuple[Callable[[InputEvent[Any], Any], None], ...]]

    def __init__(self, subscribers) -> None:
        self._subscribers = {k: v for k, v in subscribers.get_scenes()}

    def route(self, event: EventType, payload: EventPayloadType) -> None:
        for subscriber in self._subscribers.get(event, []):
            subscriber(event, payload)
