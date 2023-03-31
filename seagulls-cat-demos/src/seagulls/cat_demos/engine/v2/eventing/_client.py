from abc import abstractmethod
from typing import Any, Callable, Dict, List, NamedTuple, Optional, Protocol, Tuple

from seagulls.cat_demos.engine.v2.components._entities import EntityType, TypedEntityId


class GameEventId(TypedEntityId[EntityType]):
    pass


class GameEvent(NamedTuple):
    id: GameEventId[EntityType]
    payload: EntityType


class IGameEventDispatcher(Protocol):
    @abstractmethod
    def register(self, event: GameEventId[Any], callback: Callable[[], None]) -> None:
        pass

    @abstractmethod
    def trigger(self, event: GameEvent[Any]) -> None:
        pass

    @abstractmethod
    def event(self) -> EntityType:
        pass


class GameEventDispatcher(IGameEventDispatcher):

    _active_event: Optional[GameEvent[Any]]
    """
    If we switched to using identity objects for the callbacks, we could easily add/remove listeners.
    We just need a registry of callable identities.
    We could also ensure that all callables can be configured after the listener is registered.
    We can think of that as being able to say "someone has to handle this event, but I don't know who."
    Example: register(GameEventId("input.move-left"), CallableId("input.move-left"))
    Is this better than a 1:1 mapping of event to callable?
    1:1 mapping could mean requiring a callback for all events
    A callable that allows registering proxy listeners allows for all the same functionality
    I'm not sure if I prefer making event callbacks optional or not.
    """
    _callbacks: Dict[GameEventId, List[Callable[[], None]]]

    def __init__(self) -> None:
        self._active_event = None
        self._callbacks = {}

    @staticmethod
    def with_callbacks(*callback: Tuple[GameEventId[Any], Callable[[], None]]) -> "GameEventDispatcher":
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

    def event(self) -> EntityType:
        if not self._active_event:
            raise RuntimeError("No active event found")

        return self._active_event
