from typing import (
    Any,
    Callable,
    Dict,
    Generic,
    List,
    Optional,
    Tuple,
    TypeAlias,
    TypeVar
)

from typing_extensions import NamedTuple

from seagulls.cat_demos.engine.v2.components._entities import TypedEntityId

GameEventType = TypeVar("GameEventType", bound=NamedTuple)


GameEventId: TypeAlias = TypedEntityId[GameEventType]


class GameEvent(NamedTuple, Generic[GameEventType]):
    id: GameEventId[GameEventType]
    payload: GameEventType


class GameEventDispatcher:
    _active_event: Optional[GameEvent]
    _callbacks: Dict[GameEventId, List[Callable[[], None]]]

    def __init__(self) -> None:
        self._active_event = None
        self._callbacks = {}

    @staticmethod
    def with_callbacks(
        *callback: Tuple[GameEventId[Any], Callable[[], None]]
    ) -> "GameEventDispatcher":
        inst = GameEventDispatcher()
        for cb in callback:
            inst.register(cb[0], cb[1])

        return inst

    def register(self, event: GameEventId[Any], callback: Callable[[], None]) -> None:
        if event not in self._callbacks:
            self._callbacks[event] = []

        self._callbacks[event].append(callback)

    def trigger(self, event: GameEvent[Any]) -> None:
        prev = self._active_event
        self._active_event = event

        for callback in self._callbacks.get(event.id, []):
            callback()

        self._active_event = prev

    def event(self) -> GameEvent[Any]:
        if not self._active_event:
            raise RuntimeError("No active event found")

        return self._active_event
