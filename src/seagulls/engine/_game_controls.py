from typing import List

import pygame
from pygame.event import Event


class GameControls:

    _events: List[Event]

    def __init__(self):
        self._events = []

    def update(self):
        self._events = pygame.event.get()

    def should_quit(self) -> bool:
        for event in self._events:
            if event.type == pygame.QUIT:
                return True

            if self._is_key_event(event, pygame.K_ESCAPE):
                return True

        return False

    def should_fire(self) -> bool:
        for event in self._events:
            if self._is_key_event(event, pygame.K_SPACE):
                return True

        return False

    def should_toggle_debug_hud(self) -> bool:
        for event in self._events:
            if self._is_key_event(event, pygame.K_BACKQUOTE):
                return True

        return False

    def _is_key_event(self, event: Event, key: int) -> bool:
        return event.type == pygame.KEYDOWN and event.key == key
