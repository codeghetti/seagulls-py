from typing import List

import pygame
from pygame.event import Event

from ._game_object import GameObject
from ._pyagme import Surface


class GameControls(GameObject):

    _events: List[Event]

    def __init__(self):
        self._events = []

    def tick(self):
        self._events = pygame.event.get()

    def should_quit(self) -> bool:
        for event in self._events:
            if event.type == pygame.QUIT:
                return True

            if self._is_key_down_event(event, pygame.K_ESCAPE):
                return True

        return False

    def should_fire(self) -> bool:
        for event in self._events:
            if self._is_key_down_event(event, pygame.K_SPACE):
                return True

        return False

    def is_left_moving(self) -> bool:
        return pygame.key.get_pressed()[pygame.K_LEFT]

    def is_right_moving(self) -> bool:
        return pygame.key.get_pressed()[pygame.K_RIGHT]

    def is_up_moving(self) -> bool:
        return pygame.key.get_pressed()[pygame.K_UP]

    def is_down_moving(self) -> bool:
        return pygame.key.get_pressed()[pygame.K_DOWN]

    def should_toggle_debug_hud(self) -> bool:
        for event in self._events:
            if self._is_key_down_event(event, pygame.K_BACKQUOTE):
                return True

        return False

    def is_click_initialized(self) -> bool:
        for event in self._events:
            if not event.type == pygame.MOUSEBUTTONDOWN:
                continue

            return pygame.mouse.get_pressed(num_buttons=3)[0]

        return False

    def is_mouse_down(self) -> bool:
        return pygame.mouse.get_pressed(num_buttons=3)[0]

    def _is_key_down_event(self, event: Event, key: int) -> bool:
        return event.type == pygame.KEYDOWN and event.key == key

    def _is_key_up_event(self, event: Event, key: int) -> bool:
        return event.type == pygame.KEYUP and event.key == key

    def render(self, surface: Surface) -> None:
        pass
