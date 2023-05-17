import pygame
from typing import NamedTuple
from uuid import uuid4

from seagulls.cat_demos.engine.v2.collisions._collision_client import (CollisionClient,
                                                                       CollisionComponent,
                                                                       CollisionEvent)
from seagulls.cat_demos.engine.v2.components._entities import GameClientId, GameObjectId
from seagulls.cat_demos.engine.v2.components._object_data import ObjectDataId
from seagulls.cat_demos.engine.v2.components._scene_objects import SceneObjects
from seagulls.cat_demos.engine.v2.eventing._event_dispatcher import (
    GameEvent,
    GameEventDispatcher,
    GameEventId
)
from seagulls.cat_demos.engine.v2.input._game_clock import GameClock
from seagulls.cat_demos.engine.v2.input._input_toggles import (
    InputTogglesClient
)
from seagulls.cat_demos.engine.v2.input._pygame import PygameEvents
from seagulls.cat_demos.engine.v2.position._point import Position
from seagulls.cat_demos.engine.v2.scenes._scene_client import SceneContext
from seagulls.cat_demos.engine.v2.sprites._sprite_component import Sprite, SpriteId


class PlayerControls(NamedTuple):
    object_id: GameObjectId
    left_key: int
    right_key: int
    up_key: int
    down_key: int
    fire_key: int


class PlayerMoveEvent(NamedTuple):
    object_id: GameObjectId
    direction: Position


class PlayerControlClient:
    _scene_objects: SceneObjects
    _scene_context: SceneContext
    _event_client: GameEventDispatcher
    _toggles: InputTogglesClient
    _clock: GameClock
    _collisions: CollisionClient

    def __init__(
        self,
        scene_objects: SceneObjects,
        scene_context: SceneContext,
        event_client: GameEventDispatcher,
        toggles: InputTogglesClient,
        clock: GameClock,
        collisions: CollisionClient,
    ) -> None:
        self._scene_objects = scene_objects
        self._scene_context = scene_context
        self._event_client = event_client
        self._toggles = toggles
        self._clock = clock
        self._collisions = collisions

    def _spawn_laser(self, player_id: GameObjectId) -> None:
        object_id = GameObjectId(str(uuid4()))
        self._scene_objects.add(object_id)
        current_position = self._scene_objects.get_data(
            object_id=player_id,
            data_id=ObjectDataId[Position]("position"),
        )
        self._scene_objects.set_data(
            object_id=object_id,
            data_id=ObjectDataId[Position]("position"),
            config=current_position,
        )

        self._scene_objects.set_data(
            object_id=object_id,
            data_id=ObjectDataId[Sprite]("sprite"),
            config=Sprite(sprite_id=SpriteId("laser"), layer="units"),
        )

    def attach(self, request: PlayerControls) -> None:
        movement_mapping = {
            request.left_key: Position(-1, 0),
            request.down_key: Position(0, 1),
            request.right_key: Position(1, 0),
            request.up_key: Position(0, -1),
        }

        def on_movement_key() -> None:
            event = self._event_client.event()
            game_event = GameEvent(
                event_id=PlayerControlComponent.MOVE_EVENT,
                payload=PlayerMoveEvent(
                    object_id=request.object_id,
                    direction=movement_mapping[event.payload.key],
                ),
            )

            if event.payload.type == pygame.KEYDOWN:
                self._toggles.on(game_event)
            elif event.payload.type == pygame.KEYUP:
                self._toggles.off(game_event)

        def on_fire_key() -> None:
            event = self._event_client.event()
            if event.payload.type == pygame.KEYDOWN:
                self._spawn_laser(request.object_id)

        self._event_client.register(
            PygameEvents.key(request.left_key).namespace(self._scene_context.get().name),
            on_movement_key,
        )
        self._event_client.register(
            PygameEvents.key(request.right_key).namespace(self._scene_context.get().name),
            on_movement_key,
        )
        self._event_client.register(
            PygameEvents.key(request.up_key).namespace(self._scene_context.get().name),
            on_movement_key,
        )
        self._event_client.register(
            PygameEvents.key(request.down_key).namespace(self._scene_context.get().name),
            on_movement_key,
        )
        self._event_client.register(
            PygameEvents.key(request.fire_key).namespace(self._scene_context.get().name),
            on_fire_key,
        )

        self._event_client.register(PlayerControlComponent.MOVE_EVENT, self._move_player)
        self._event_client.register(CollisionComponent.COLLISION_EVENT, self._undo_move)

    def _move_player(self) -> None:
        delta = self._clock.get_delta()
        event = self._event_client.event()
        payload: PlayerMoveEvent = event.payload
        current_position = self._scene_objects.get_data(
            object_id=payload.object_id,
            data_id=ObjectDataId[Position]("position"),
        )
        adjusted_direction = Position(
            x=payload.direction.x * delta / 10, y=payload.direction.y * delta / 10
        )
        self._scene_objects.set_data(
            object_id=payload.object_id,
            data_id=ObjectDataId[Position]("position"),
            config=current_position + adjusted_direction,
        )
        self._previous_position = current_position
        self._collisions.check_collisions(payload.object_id)

    def _undo_move(self) -> None:
        event = self._event_client.event()
        payload: CollisionEvent = event.payload
        self._scene_objects.set_data(
            object_id=payload.source_id,
            data_id=ObjectDataId[Position]("position"),
            config=self._previous_position,
        )


class PlayerControlComponent:
    CLIENT_ID = GameClientId[PlayerControlClient]("player-control-client")
    MOVE_EVENT = GameEventId[PlayerMoveEvent]("player-controls.move")
