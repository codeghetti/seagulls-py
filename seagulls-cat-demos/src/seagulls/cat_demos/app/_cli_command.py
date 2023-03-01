from argparse import ArgumentParser

import pygame

from seagulls.cat_demos.app._events import GameInputs, PlayerMoveEvent, QuitGameEvent
from seagulls.cat_demos.app._mob_controls_component import MobControlsComponentClient, \
    MobControlsComponentId
from seagulls.cat_demos.app._player_controls_component import (
    PlayerControlsComponentClient,
    PlayerControlsComponentId,
)
from seagulls.cat_demos.app._scene import MainScene
from seagulls.cat_demos.engine.v2._game_clock import GameClock
from seagulls.cat_demos.engine.v2._resources import ResourceClient
from seagulls.cat_demos.engine.v2._scene import GameSceneObjects
from seagulls.cat_demos.engine.v2._size import Size
from seagulls.cat_demos.engine.v2._sprite_component import (
    GameSprite,
    SpriteComponentClient,
    SpriteComponentId,
)
from seagulls.cat_demos.engine.v2.animation._animation_component import SpriteAnimationComponentClient, \
    SpriteAnimationComponentId
from seagulls.cat_demos.engine.v2.components._entities import GameSceneId
from seagulls.cat_demos.engine.v2.input._eventing import EventPayloadType, InputEvent, \
    InputEventDispatcher
from seagulls.cat_demos.engine.v2.input._input_client import GameInputClient
from seagulls.cat_demos.engine.v2.input._input_router import GameInputRouter
from seagulls.cat_demos.engine.v2.input._input_toggles import InputTogglesClient
from seagulls.cat_demos.engine.v2.input._pygame import PygameEvents, PygameInputEvent, \
    PygameKeyboardInputPublisher
from seagulls.cat_demos.engine.v2.position._position_component import (
    Position, PositionComponentClient,
    PositionComponentId, Vector,
)
from seagulls.cat_demos.engine.v2.scenes._client import SceneClient
from seagulls.cat_demos.engine.v2.sessions._client import SessionClient
from seagulls.cat_demos.engine.v2.window._window import WindowClient
from seagulls.cli import ICliCommand


class GameCliCommand(ICliCommand):

    _session_client: SessionClient
    _scene_collection: SceneClient

    def __init__(self, session_client: SessionClient, scene_collection: SceneClient) -> None:
        self._session_client = session_client
        self._scene_collection = scene_collection

    def configure_parser(self, parser: ArgumentParser) -> None:
        pass

    def execute(self) -> None:
        print("hello")
        self._scene_collection.load_scene(GameSceneId("main-menu"))
        self._session_client.open_session()
        self._session_client.run_session()
        self._session_client.close_session()

    def _init_session(self) -> None:
        self._session_window_client = WindowClient()
        self._session_window_client.open()
        self._window = self._session_window_client.get_surface()
        self._clock = GameClock()

        self._scene_client = GameSceneObjects(window=self._session_window_client)

        self._input_v2 = GameInputClient(handlers=tuple([
            self._on_input_v2,
        ]))
        self._pygame_input_v2 = PygameKeyboardInputPublisher(self._input_v2)
        self._input_v2_routing = GameInputRouter({
            PygameEvents.KEYBOARD: tuple([self._on_keyboard]),
            GameInputs.QUIT: tuple([self._on_quit]),
        })
        self._event_dispatcher = InputEventDispatcher()
        self._event_toggles = InputTogglesClient(self._input_v2)

        resource_client = ResourceClient()
        position_client = PositionComponentClient()
        player_controls_client = PlayerControlsComponentClient(
            self._event_dispatcher,
            self._clock,
            position_client,
        )
        mob_controls_client = MobControlsComponentClient(
            self._clock,
            position_client,
        )
        sprite_client = SpriteComponentClient(
            window_client=self._session_window_client,
            resources_client=resource_client,
            position_client=position_client,
        )
        animation_client = SpriteAnimationComponentClient(sprite_client)

        self._scene_client.create_component(PositionComponentId, position_client)
        self._scene_client.create_component(PlayerControlsComponentId, player_controls_client)
        self._scene_client.create_component(MobControlsComponentId, mob_controls_client)
        self._scene_client.create_component(SpriteComponentId, sprite_client)
        self._scene_client.create_component(SpriteAnimationComponentId, animation_client)

        sprite_client.register_sprite(
            sprite=GameSprite("player.idle.1"),
            resource="/kenney.tiny-dungeon/tilemap-packed.png",
            position=Position(x=16, y=16 * 7),
            size=Size(height=16, width=16),
        )
        sprite_client.register_sprite(
            sprite=GameSprite("player.idle.2"),
            resource="/kenney.tiny-dungeon/tilemap-packed.png",
            position=Position(x=16 * 2, y=16 * 7),
            size=Size(height=16, width=16),
        )
        sprite_client.register_sprite(
            sprite=GameSprite("enemy.idle"),
            resource="/kenney.tiny-dungeon/tilemap-packed.png",
            position=Position(x=16, y=16*9),
            size=Size(height=16, width=16),
        )

        self._scene = MainScene(
            scene_objects=self._scene_client,
        )

    def _on_input_v2(self, event: InputEvent[EventPayloadType], payload: EventPayloadType) -> None:
        self._input_v2_routing.route(event, payload)
        self._event_dispatcher.trigger(event, payload)

    def _on_keyboard(self, event: InputEvent[PygameInputEvent], payload: PygameInputEvent) -> None:
        if payload.type == pygame.KEYDOWN:
            if payload.key == pygame.K_a:
                self._event_toggles.on(GameInputs.MOVE_LEFT, PlayerMoveEvent(Vector(-1, 0)))
            if payload.key == pygame.K_d:
                self._event_toggles.on(GameInputs.MOVE_RIGHT, PlayerMoveEvent(Vector(1, 0)))
            if payload.key == pygame.K_w:
                self._event_toggles.on(GameInputs.MOVE_UP, PlayerMoveEvent(Vector(0, -1)))
            if payload.key == pygame.K_s:
                self._event_toggles.on(GameInputs.MOVE_DOWN, PlayerMoveEvent(Vector(0, 1)))
            if payload.key == pygame.K_ESCAPE:
                self._input_v2.trigger(GameInputs.QUIT, QuitGameEvent())
        if payload.type == pygame.KEYUP:
            if payload.key == pygame.K_a:
                self._event_toggles.off(GameInputs.MOVE_LEFT)
            if payload.key == pygame.K_d:
                self._event_toggles.off(GameInputs.MOVE_RIGHT)
            if payload.key == pygame.K_w:
                self._event_toggles.off(GameInputs.MOVE_UP)
            if payload.key == pygame.K_s:
                self._event_toggles.off(GameInputs.MOVE_DOWN)

    def _on_quit(self, event: GameInputs.QUIT, payload: QuitGameEvent) -> None:
        quit()

    def _run_session(self) -> None:
        try:
            self._scene.load_scene()
            while True:
                self._tick()
        finally:
            pass

    def _tick(self) -> None:
        self._clock.tick()
        self._window.fill((100, 120, 20))
        self._pygame_input_v2.tick()
        self._event_toggles.tick()
        self._scene_client.tick()
        self._scene.tick()
        self._session_window_client.commit()

    def _end_session(self) -> None:
        self._session_window_client.close()
