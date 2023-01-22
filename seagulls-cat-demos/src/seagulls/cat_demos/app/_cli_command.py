import pygame
from typing import Dict, Tuple

from argparse import ArgumentParser
from pygame import Surface

from seagulls.cat_demos.app._events import GameInputs, QuitGameEvent, PlayerMoveEvent
from seagulls.cat_demos.app._scene import MainScene
from seagulls.cat_demos.engine import (
    executable,
    GameSession,
    GameSessionStages,
    GameSessionStateClient,
)
from seagulls.cat_demos.engine._input import GameSessionInputClient
from seagulls.cat_demos.engine._rendering import (
    IProvideGameObjects,
    IProvideObjectSprites,
    IProvideObjectPositions,
    IProvideSurfaces,
    IProvidePositions
)
from seagulls.cat_demos.engine.v2._components import MobControlsComponent, Position, \
    PositionComponent, \
    Size, SpriteComponent
from seagulls.cat_demos.engine.v2._entities import GameComponent, GameSprite
from seagulls.cat_demos.engine.v2._resources import ResourceClient
from seagulls.cat_demos.engine.v2._scene import GameSceneObjects
from seagulls.cat_demos.engine.v2._window import GameWindowClient
from seagulls.cli import ICliCommand


class SceneObjects(IProvideGameObjects, IProvideObjectSprites, IProvideObjectPositions):

    # _surface_providers: Dict[GameObject, IProvideSurfaces]
    # _position_providers: Dict[GameObject, IProvidePositions]

    def __init__(self) -> None:
        pass

    # def get_game_objects(self) -> Tuple[GameObject, ...]:
    #     return tuple(self._surface_providers.keys())

    # def get_sprite(self, game_object: GameObject) -> Surface:
    #     return self._surface_providers[game_object].get_surface()

    # def get_position(self, game_object: GameObject) -> Position:
    #     return self._position_providers[game_object].get_position()


class SceneObjectContext:
    pass


class GameCliCommand(ICliCommand):

    _session_state_client: GameSessionStateClient
    _session_window_client: GameWindowClient
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
        self._session_window_client = GameWindowClient()
        self._session_input_client = GameSessionInputClient()
        self._session_window_client.open()
        self._window = self._session_window_client.get_surface()

        self._session_input_client.publisher(executable(self._check_quit))
        self._session_input_client.publisher(executable(self._check_move))
        self._session_input_client.subscribe(GameInputs.QUIT, self._on_quit)
        self._session_input_client.subscribe(GameInputs.MOVE, self._on_move)

        resource_client = ResourceClient()
        positionizer = PositionComponent()
        mob_controls = MobControlsComponent(positionizer)
        sprites = SpriteComponent(self._session_window_client, resource_client, positionizer)
        sprites.register_sprite(
            sprite=GameSprite("player.idle"),
            resource="/kenney.tiny-dungeon/tilemap-packed.png",
            position=Position(x=0, y=0),
            size=Size(height=50, width=50),
        )
        sprites.register_sprite(
            sprite=GameSprite("enemy.idle"),
            resource="/kenney.tiny-dungeon/tilemap-packed.png",
            position=Position(x=16, y=145),
            size=Size(height=16, width=16),
        )

        self._scene_objects = GameSceneObjects(window=self._session_window_client)

        self._scene_objects.create_component(
            GameComponent[PositionComponent]("position"), positionizer)
        self._scene_objects.create_component(
            GameComponent[MobControlsComponent]("mob-controls"), mob_controls)
        self._scene_objects.create_component(
            GameComponent[SpriteComponent]("sprites"), sprites)

        self._scene = MainScene(
            scene_objects=self._scene_objects,
            sprites=sprites,
        )

    def _check_quit(self) -> None:
        if self._session_input_client.was_key_pressed(pygame.K_ESCAPE):
            self._session_input_client.publish(GameInputs.QUIT, QuitGameEvent())

    def _check_move(self) -> None:
        if self._session_input_client.was_key_pressed(pygame.K_LEFT):
            self._session_input_client.publish(GameInputs.MOVE, PlayerMoveEvent(
                direction=(-1, 0),
            ))
        if self._session_input_client.was_key_pressed(pygame.K_RIGHT):
            self._session_input_client.publish(GameInputs.MOVE, PlayerMoveEvent(
                direction=(1, 0),
            ))

    def _on_move(self, event: PlayerMoveEvent) -> None:
        print(event)

    def _on_quit(self, event: QuitGameEvent) -> None:
        exit()

    def _run_session(self) -> None:
        try:
            self._scene.load_scene()
            while True:
                self._tick()
        finally:
            pass

    def _tick(self) -> None:
        self._window.fill((100, 120, 20))
        self._session_input_client.tick()
        self._scene_objects.tick()
        self._scene.tick()
        self._session_window_client.commit()

    def _end_session(self) -> None:
        self._session_window_client.close()
