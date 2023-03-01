from typing import Dict

from ._eventing import EventPayloadType, EventType
from ._input_client import GameInputClient


class InputTogglesClient:

    _input_client: GameInputClient
    # I'm not sure yet if EventType is unique enough as a toggle
    # Do we ever want to fire the same event with different payloads?
    _events: Dict[EventType, EventPayloadType]

    def __init__(self, input_client: GameInputClient) -> None:
        self._input_client = input_client
        self._events = {}

    def tick(self) -> None:
        for event, payload in self._events.items():
            self._input_client.trigger(event, payload)

    def on(self, event: EventType, payload: EventPayloadType) -> None:
        self._events[event] = payload

    def off(self, event: EventType) -> None:
        self._events.pop(event)
