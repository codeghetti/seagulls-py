import pygame
from typing import Dict, Tuple

from dataclasses import dataclass

from argparse import ArgumentParser
from pygame import Surface

from seagulls.cat_demos._object_position import Position
from seagulls.cat_demos.app._events import GameInputs, QuitGameEvent, PlayerMoveEvent
from seagulls.cat_demos.engine import (
    executable,
    GameSession,
    GameSessionStages,
    GameSessionStateClient,
    GameSessionWindowClient,
)
from seagulls.cat_demos.engine._input import GameSessionInputClient
from seagulls.cat_demos.engine._rendering import RenderSceneObjects, IProvideGameObjects, \
    IProvideObjectSprites, IProvideObjectPositions, GameObject, IProvideSurfaces, IProvidePositions
from seagulls.cat_demos.player._sprite import PlayerSprite
from seagulls.cli import ICliCommand


class SceneObjects(IProvideGameObjects, IProvideObjectSprites, IProvideObjectPositions):

    _surface_providers: Dict[GameObject, IProvideSurfaces]
    _position_providers: Dict[GameObject, IProvidePositions]

    def __init__(
            self,
            # TODO: make this input immutable
            surface_providers: Dict[GameObject, IProvideSurfaces],
            position_providers: Dict[GameObject, IProvidePositions]) -> None:
        self._surface_providers = surface_providers.copy()
        self._position_providers = position_providers.copy()

    def get_game_objects(self) -> Tuple[GameObject, ...]:
        return tuple(self._surface_providers.keys())

    def get_sprite(self, game_object: GameObject) -> Surface:
        return self._surface_providers[game_object].get_surface()

    def get_position(self, game_object: GameObject) -> Position:
        return self._position_providers[game_object].get_position()


class SceneObjectContext:
    pass


class GameCliCommand(ICliCommand):

    _session_state_client: GameSessionStateClient
    _session_window_client: GameSessionWindowClient
    _session_input_client: GameSessionInputClient
    _window: Surface

    def configure_parser(self, parser: ArgumentParser) -> None:
        pass

    def execute(self) -> None:
        session = GameSession(session_stages=GameSessionStages(tuple([
            executable(self._init_session),
            executable(self._run_session),
            executable(self._end_session),
        ])))
        session.run()

    def _init_session(self) -> None:
        print("init")
        self._session_state_client = GameSessionStateClient()
        self._session_window_client = GameSessionWindowClient()
        self._session_input_client = GameSessionInputClient()
        self._session_window_client.open()
        self._window = self._session_window_client.get_surface()
        self._session_input_client.publisher(executable(self._check_quit))
        self._session_input_client.publisher(executable(self._check_move))
        self._session_input_client.subscribe(GameInputs.QUIT, self._on_quit)
        self._session_input_client.subscribe(GameInputs.MOVE, self._on_move)
        self._player_sprite = PlayerSprite()
        self._scene_objects_client = SceneObjects(
            surface_providers={GameObject("player-character"): self._player_sprite},
            position_providers={GameObject("player-character"): self._player_sprite},
        )
        self._render_objects = RenderSceneObjects(
            surface_client=self._session_window_client,
            game_objects_client=self._scene_objects_client,
            object_sprites_client=self._scene_objects_client,
            object_positions_client=self._scene_objects_client,
        )

    def _check_quit(self) -> None:
        if self._session_input_client.was_key_pressed(pygame.K_ESCAPE):
            self._session_input_client.publish(GameInputs.QUIT, QuitGameEvent())

    def _check_move(self) -> None:
        if self._session_input_client.was_key_pressed(pygame.K_LEFT):
            self._session_input_client.publish(GameInputs.MOVE, PlayerMoveEvent(
                direction=(-1, 0),
            ))

    def _on_move(self, event: PlayerMoveEvent) -> None:
        print(event)

    def _on_quit(self, event: QuitGameEvent) -> None:
        exit()

    def _run_session(self) -> None:
        try:
            while True:
                self._tick()
                self._session_window_client.commit()
        finally:
            pass

    def _tick(self) -> None:
        self._window.fill((100, 120, 20))
        self._session_input_client.tick()
        self._render_character()
        self._render_objects.execute()

    def _render_character(self) -> None:
        character = Surface(size=(100, 100))
        self._window.blit(character, (10, 10))

    def _end_session(self) -> None:
        self._session_window_client.close()
