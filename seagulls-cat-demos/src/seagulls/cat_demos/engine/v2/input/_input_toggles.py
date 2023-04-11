from collections import defaultdict
from typing import Dict

from seagulls.cat_demos.engine.v2.eventing._event_dispatcher import GameEvent, GameEventDispatcher


class InputTogglesClient:

    _input_client: GameEventDispatcher
    _events: Dict[GameEvent, int]

    def __init__(self, input_client: GameEventDispatcher) -> None:
        self._input_client = input_client
        self._events = defaultdict(int)

    def tick(self) -> None:
        rm = []
        for event, count in self._events.items():
            if count < 0:
                raise RuntimeError(f"weird count found for event toggle: {event} :: {count}")
            elif count == 0:
                rm.append(event)
            else:
                self._input_client.trigger(event)

        for event in rm:
            del self._events[event]

    def on(self, event: GameEvent) -> None:
        self._events[event] += 1

    def off(self, event: GameEvent) -> None:
        self._events[event] -= 1
