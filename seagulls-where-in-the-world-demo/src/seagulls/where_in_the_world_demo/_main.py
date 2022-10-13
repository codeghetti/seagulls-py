from functools import lru_cache
from typing import List

import pygame
from pygame import Surface
from pygame.event import Event
from pygame.font import Font

from seagulls.where_in_the_world_demo._executable import executable
from seagulls.where_in_the_world_demo._session_client import GameSessionClient, InitializeGameSessionCommand, \
    RunGameLoopCommand, ShutdownGameSessionCommand
from seagulls.where_in_the_world_demo._session_frame_client import GameSessionFrameClient
from seagulls.where_in_the_world_demo._session_window_client import GameSessionWindowClient
from seagulls.where_in_the_world_demo._session_state_client import GameSessionStateClient


class GameInputClient:

    _session_state_client: GameSessionStateClient
    _frame_events: List[Event]

    def __init__(self, session_state_client: GameSessionStateClient) -> None:
        self._session_state_client = session_state_client
        self._frame_events = []

    def process_input(self) -> None:
        self._frame_events = pygame.event.get()
        for event in self._frame_events:
            if event.type == pygame.QUIT:
                self._session_state_client.set_stopped()

            if self.was_key_pressed(pygame.K_ESCAPE):
                self._session_state_client.set_stopped()

    def was_key_pressed(self, key: int) -> bool:
        for event in self._frame_events:
            if self._is_key_down_event(event, key):
                return True

        return False

    def was_key_released(self, key: int) -> bool:
        for event in self._frame_events:
            if self._is_key_up_event(event, key):
                return True

        return False

    def was_mouse_button_pressed(self) -> bool:
        for event in self._frame_events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                return True

        return False

    def was_mouse_button_released(self) -> bool:
        for event in self._frame_events:
            if event.type == pygame.MOUSEBUTTONUP:
                return True

        return False

    def _is_key_down_event(self, event: Event, key: int) -> bool:
        return event.type == pygame.KEYDOWN and event.key == key

    def _is_key_up_event(self, event: Event, key: int) -> bool:
        return event.type == pygame.KEYUP and event.key == key

class FooScene:

    _session_window_client: GameSessionWindowClient

    def __init__(self, session_window_client: GameSessionWindowClient) -> None:
        self._session_window_client = session_window_client

    def render_scene(self) -> None:
        window = self._window()
        self._window().fill((100, 100, 200))

    @lru_cache()
    def _logo(self) -> Surface:
        pygame.font.init()
        font = Font(
            "/home/zeelot/projects/github/codeghetti/seagulls-py/seagulls-rpg-demo/seagulls_assets/fonts/ubuntu-mono-v10-latin-regular.ttf",
            120,
        )
        return font.render("codeghetti", True, (60, 60, 175))


    def _window(self) -> Surface:
        return self._session_window_client.get_surface()


def main() -> None:
    session_state_client = GameSessionStateClient()
    session_window_client = GameSessionWindowClient()
    game_input_client = GameInputClient(session_state_client=session_state_client)
    scene = FooScene(session_window_client=session_window_client)

    process_input = executable(game_input_client.process_input)
    render_scene = executable(scene.render_scene)

    session_frame_client = GameSessionFrameClient(
        session_state_client=session_state_client,
        frame_stages=tuple([
            process_input,
            render_scene,
        ]),
    )

    initialize = InitializeGameSessionCommand(
        session_state_client=session_state_client,
        session_window_client=session_window_client,
    )
    run_game_loop = RunGameLoopCommand(session_frame_client=session_frame_client)
    shutdown = ShutdownGameSessionCommand(
        session_state_client=session_state_client,
        session_window_client=session_window_client,
    )

    session = GameSessionClient(session_stages=tuple([initialize, run_game_loop, shutdown]))

    session.run()


if __name__ == "__main__":
    main()
