import pygame

from typing import Any, Callable, Dict, Generic, List, NamedTuple, Tuple, TypeAlias, TypeVar

from seagulls.cat_demos.engine.v2._entities import _IdentityObject


EventPayloadType = TypeVar("EventPayloadType")


class InputEvent(_IdentityObject, Generic[EventPayloadType]):
    pass


EventType: TypeAlias = InputEvent[EventPayloadType]
EventCallbackType: TypeAlias = Callable[[EventType, EventPayloadType], None]


class GameInputClient:
    _handlers: Tuple[EventCallbackType, ...]

    def __init__(self, handlers: Tuple[EventCallbackType, ...]) -> None:
        self._handlers = handlers

    def trigger(self, event: EventType, payload: EventPayloadType) -> None:
        for handler in self._handlers:
            handler(event, payload)


class GameInputRouter:

    _subscribers: Dict[InputEvent[Any], Tuple[Callable[[InputEvent[Any], Any], None], ...]]

    def __init__(self, subscribers) -> None:
        self._subscribers = {k: v for k, v in subscribers.items()}

    def route(self, event: EventType, payload: EventPayloadType) -> None:
        for subscriber in self._subscribers.get(event, []):
            subscriber(event, payload)


class PygameInputMapper:
    pass


class PygameInputEvent(NamedTuple):
    type: int
    key: int


class PygameEvents:
    KEYBOARD = InputEvent[PygameInputEvent](name='seagulls.pygame-input.keyboard')


class PygameKeyboardInputPublisher:

    _game_input_client: GameInputClient

    def __init__(self, game_input_client: GameInputClient) -> None:
        self._game_input_client = game_input_client

    def tick(self) -> None:
        events = pygame.event.get()
        for event in events:
            if event.type in [pygame.KEYDOWN, pygame.KEYUP]:
                self._game_input_client.trigger(
                    event=InputEvent[PygameInputEvent]("seagulls.pygame-input.keyboard"),
                    payload=PygameInputEvent(type=event.type, key=event.key),
                )


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


class EventTogglesClient:

    _input_client: GameInputClient
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
