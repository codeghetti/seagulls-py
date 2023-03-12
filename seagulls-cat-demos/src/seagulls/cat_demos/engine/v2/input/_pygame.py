from typing import NamedTuple

import pygame

from seagulls.cat_demos.engine.v2.eventing._client import GameEvent, GameEventDispatcher, GameEventId


class PygameInputEvent(NamedTuple):
    type: int
    key: int


class PygameEvents:
    KEYBOARD = GameEventId[PygameInputEvent](name='seagulls:pygame-input.keyboard')
    QUIT = GameEventId[None](name='seagulls:pygame-input.quit')


class PygameKeyboardInputPublisher:

    _event_dispatcher: GameEventDispatcher

    def __init__(self, event_dispatcher: GameEventDispatcher) -> None:
        self._event_dispatcher = event_dispatcher

    def tick(self) -> None:
        events = pygame.event.get()
        for event in events:
            if event.type in [pygame.KEYDOWN, pygame.KEYUP]:
                self._event_dispatcher.trigger(GameEvent(
                    PygameEvents.KEYBOARD,
                    PygameInputEvent(type=event.type, key=event.key),
                ))
            if event.type == pygame.QUIT:
                self._event_dispatcher.trigger(GameEvent(PygameEvents.QUIT, None))
            else:
                print(f"unknown: {event}")
