import logging
from functools import lru_cache
from typing import NamedTuple

import pygame

from seagulls.cat_demos.engine.v2.eventing._event_dispatcher import GameEvent, GameEventDispatcher, GameEventId
from seagulls.cat_demos.engine.v2.position._point import Point, Position

logger = logging.getLogger(__name__)


class PygameKeyboardEvent(NamedTuple):
    type: int
    key: int


class PygameMouseMotionEvent(NamedTuple):
    position: Position
    previous_position: Position

    @lru_cache()
    def movement(self) -> Point:
        return self.position - self.previous_position


class PygameEvents:
    KEYBOARD = GameEventId[PygameKeyboardEvent](name='seagulls:pygame-input.keyboard')
    MOUSE_MOTION = GameEventId[PygameMouseMotionEvent](name='seagulls:pygame-input.mouse-motion')
    QUIT = GameEventId[None](name='seagulls:pygame-input.quit')

    @staticmethod
    def key(x: int) -> GameEventId[PygameKeyboardEvent]:
        return GameEventId[PygameKeyboardEvent](name=f'seagulls:pygame-input.keyboard:{x}')

    @staticmethod
    def key_pressed(x: int) -> GameEventId[PygameKeyboardEvent]:
        return GameEventId[PygameKeyboardEvent](name=f'seagulls:pygame-input.keyboard:{x}:pressed')

    @staticmethod
    def key_released(x: int) -> GameEventId[PygameKeyboardEvent]:
        return GameEventId[PygameKeyboardEvent](name=f'seagulls:pygame-input.keyboard:{x}:released')


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
                    PygameKeyboardEvent(type=event.type, key=event.key),
                ))
                self._event_dispatcher.trigger(GameEvent(
                    PygameEvents.key(event.key),
                    PygameKeyboardEvent(type=event.type, key=event.key),
                ))
            if event.type == pygame.KEYDOWN:
                self._event_dispatcher.trigger(GameEvent(
                    PygameEvents.key_pressed(event.key),
                    PygameKeyboardEvent(type=event.type, key=event.key),
                ))
            if event.type == pygame.KEYUP:
                self._event_dispatcher.trigger(GameEvent(
                    PygameEvents.key_released(event.key),
                    PygameKeyboardEvent(type=event.type, key=event.key),
                ))
            if event.type == pygame.QUIT:
                self._event_dispatcher.trigger(GameEvent(PygameEvents.QUIT, None))
            if event.type == pygame.MOUSEMOTION:
                self._event_dispatcher.trigger(
                    GameEvent(PygameEvents.MOUSE_MOTION, PygameMouseMotionEvent(
                        position=Position(*event.pos),
                        previous_position=Position(event.pos[0] + event.rel[0], event.pos[1] + event.rel[1])
                    ))
                )
            else:
                logger.debug(f"unknown pygame event detected: {event}")
