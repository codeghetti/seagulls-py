from abc import abstractmethod
from typing import Callable, Protocol, Type, TypeVar

EventType = TypeVar("EventType")
EventCallbackType = Callable[[EventType], None]


class IDispatchEvents(Protocol):

    @abstractmethod
    def register_callback(
            self,
            event_type: Type[EventType],
            callback: EventCallbackType) -> None:
        """Register to be notified of a certain type of events"""

    def trigger_event(self, event: EventType) -> None:
        """Trigger an event, calling any registered callbacks"""
