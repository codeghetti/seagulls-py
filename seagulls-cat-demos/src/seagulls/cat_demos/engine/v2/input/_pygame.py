from typing import NamedTuple

import pygame

from ._eventing import InputEvent
from ._input_client import GameInputClient


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
                    event=PygameEvents.KEYBOARD,
                    payload=PygameInputEvent(type=event.type, key=event.key),
                )
