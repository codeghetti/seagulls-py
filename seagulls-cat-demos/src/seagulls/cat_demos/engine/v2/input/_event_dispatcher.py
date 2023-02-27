from typing import Callable, Dict, Generic, List, TypeAlias, TypeVar

from seagulls.cat_demos.engine.v2.components._identity import EntityId

EventPayloadType = TypeVar("EventPayloadType")


class InputEvent(EntityId, Generic[EventPayloadType]):
    pass


EventType: TypeAlias = InputEvent[EventPayloadType]
EventCallbackType: TypeAlias = Callable[[EventType, EventPayloadType], None]


class InputEventDispatcher:
    _subscribers: Dict[EventType, List[EventCallbackType]]

    def __init__(self) -> None:
        self._subscribers = {}

    def subscribe(self, event: EventType, callback: EventCallbackType) -> None:
        if event not in self._subscribers:
            self._subscribers[event] = []

        self._subscribers[event].append(callback)

    def trigger(self, event: EventType, payload: EventPayloadType) -> None:
        for callback in self._subscribers.get(event, []):
            callback(event, payload)
