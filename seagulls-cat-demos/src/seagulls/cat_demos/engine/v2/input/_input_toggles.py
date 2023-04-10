from typing import Set

from seagulls.cat_demos.engine.v2.eventing._event_dispatcher import GameEvent, GameEventDispatcher


class InputTogglesClient:

    _input_client: GameEventDispatcher
    _events: Set[GameEvent]

    def __init__(self, input_client: GameEventDispatcher) -> None:
        self._input_client = input_client
        self._events = set()

    def tick(self) -> None:
        for event in self._events:
            self._input_client.trigger(event)

    def on(self, event: GameEvent) -> None:
        self._events.add(event)

    def off(self, event: GameEvent) -> None:
        self._events.remove(event)
