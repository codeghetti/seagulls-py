from abc import abstractmethod
from typing import Protocol, TypeVar, Callable, Type

EventType = TypeVar("EventType")
EventCallbackType = Callable[[EventType], None]


class IDispatchEvents(Protocol):

    @abstractmethod
    def register_callback(
            self,
            event_type: Type[EventType],
            callback: EventCallbackType) -> None: ...

    def trigger_event(self, event: EventType) -> None: ...
