from typing import NamedTuple

import pygame

from seagulls.cat_demos.engine.v2.collisions._collider_component import ColliderPrefabIds, CollisionEvent, \
    CollisionPrefab
from seagulls.cat_demos.engine.v2.components._component_containers import GameComponentId
from seagulls.cat_demos.engine.v2.components._entities import GameObjectId
from seagulls.cat_demos.engine.v2.components._prefabs import GamePrefabId, IExecutablePrefab
from seagulls.cat_demos.engine.v2.components._scene_objects import SceneObjects
from seagulls.cat_demos.engine.v2.eventing._event_dispatcher import GameEvent, GameEventDispatcher, GameEventId
from seagulls.cat_demos.engine.v2.input._game_clock import GameClock
from seagulls.cat_demos.engine.v2.input._input_toggles import InputTogglesClient
from seagulls.cat_demos.engine.v2.input._pygame import PygameEvents
from seagulls.cat_demos.engine.v2.position._point import Position


class PlayerControls(NamedTuple):
    object_id: GameObjectId
    left_key: int
    right_key: int
    up_key: int
    down_key: int


class PlayerMoveEvent(NamedTuple):
    object_id: GameObjectId
    direction: Position


class PlayerControlsPrefab(IExecutablePrefab[PlayerControls]):

    _scene_objects: SceneObjects
    _event_client: GameEventDispatcher
    _toggles: InputTogglesClient
    _clock: GameClock
    _collisions: CollisionPrefab

    def __init__(
        self,
        scene_objects: SceneObjects,
        event_client: GameEventDispatcher,
        toggles: InputTogglesClient,
        clock: GameClock,
        collisions: CollisionPrefab,
    ) -> None:
        self._scene_objects = scene_objects
        self._event_client = event_client
        self._toggles = toggles
        self._clock = clock
        self._collisions = collisions

    def __call__(self, config: PlayerControls) -> None:
        mapping = {
            config.left_key: Position(-1, 0),
            config.down_key: Position(0, 1),
            config.right_key: Position(1, 0),
            config.up_key: Position(0, -1),
        }

        def on_keyboard() -> None:
            event = self._event_client.event()
            game_event = GameEvent(
                id=PlayerControlIds.MOVE_EVENT,
                payload=PlayerMoveEvent(
                    object_id=config.object_id,
                    direction=mapping[event.payload.key],
                ),
            )

            if event.payload.type == pygame.KEYDOWN:
                self._toggles.on(game_event)
            elif event.payload.type == pygame.KEYUP:
                self._toggles.off(game_event)

        self._event_client.register(PygameEvents.key(config.left_key), on_keyboard)
        self._event_client.register(PygameEvents.key(config.right_key), on_keyboard)
        self._event_client.register(PygameEvents.key(config.up_key), on_keyboard)
        self._event_client.register(PygameEvents.key(config.down_key), on_keyboard)

        self._event_client.register(PlayerControlIds.MOVE_EVENT, self._move_player)
        self._event_client.register(ColliderPrefabIds.COLLISION_EVENT, self._undo_move)

    def _move_player(self) -> None:
        delta = self._clock.get_delta()
        event = self._event_client.event()
        payload: PlayerMoveEvent = event.payload
        current_position = self._scene_objects.get_component(
            entity_id=payload.object_id,
            component_id=GameComponentId[Position]("object-component::position"),
        )
        adjusted_direction = Position(x=payload.direction.x * delta / 10, y=payload.direction.y * delta / 10)
        self._scene_objects.set_component(
            entity_id=payload.object_id,
            component_id=GameComponentId[Position]("object-component::position"),
            config=current_position + adjusted_direction,
        )
        self._previous_position = current_position
        self._collisions(payload.object_id)

    def _undo_move(self) -> None:
        event = self._event_client.event()
        payload: CollisionEvent = event.payload
        self._scene_objects.set_component(
            entity_id=payload.source_id,
            component_id=GameComponentId[Position]("object-component::position"),
            config=self._previous_position,
        )


class PlayerControlIds:
    MOVE_EVENT = GameEventId[PlayerMoveEvent]("player-controls.move")
    PREFAB = GamePrefabId[PlayerControls]("prefab::player-controls")
    PREFAB_COMPONENT = GameComponentId[PlayerControlsPrefab]("prefab::player-controls")
