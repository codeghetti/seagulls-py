from abc import abstractmethod

import pygame

from typing import Any, Callable, Dict, Generic, List, NamedTuple, Protocol, Tuple, TypeAlias, \
    TypeVar

from seagulls.cat_demos.engine.v2.components._identity import EntityId


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
        self._subscribers = {k: v for k, v in subscribers.get_scenes()}

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


class IProcessInputEvents(Protocol):
    @abstractmethod
    def tick(self) -> None:
        pass


class PygameKeyboardInputPublisher(IProcessInputEvents):

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
