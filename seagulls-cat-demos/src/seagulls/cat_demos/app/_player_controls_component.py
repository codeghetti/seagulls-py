from __future__ import annotations

import logging
from functools import lru_cache

from seagulls.cat_demos.engine.v2._scene import IProvideGameObjectComponent
from seagulls.cat_demos.engine.v2.input._eventing import EventType, InputEventDispatcher

from seagulls.cat_demos.app._events import GameInputs, PlayerMoveEvent
from seagulls.cat_demos.engine.v2._game_clock import GameClock
from seagulls.cat_demos.engine.v2._movement import MovementClient
from seagulls.cat_demos.engine.v2.components._entities import EntityType
from seagulls.cat_demos.engine.v2.components._object_components import GameComponentId
from seagulls.cat_demos.engine.v2.components._scene_objects import GameObjectId
from seagulls.cat_demos.engine.v2.position._position_component import (
    PositionComponent,
    PositionComponentClient,
    Vector,
)

logger = logging.getLogger(__name__)


class PlayerControlsComponent:

    _position_component: PositionComponent
    _movement_client: MovementClient
    _clock: GameClock
    _object: GameObjectId

    def __init__(
        self,
        position_component: PositionComponent,
        movement_client: MovementClient,
        clock: GameClock,
        game_object: GameObjectId,
    ) -> None:
        self._position_component = position_component
        self._movement_client = movement_client
        self._clock = clock
        self._object = game_object

    def tick(self) -> None:
        vector = self._movement_client.get_vector()
        delta = self._clock.get_delta()
        normalized = Vector(vector.x * delta / 10, vector.y * delta / 10)
        if vector != Vector.zero():
            logger.debug(f"move: {self._object} + {normalized} delta={delta}")
        self._position_component.update(
            self._position_component.get() + normalized,
        )
        self._movement_client.reset()


PlayerControlsComponentId = GameComponentId[PlayerControlsComponent]("player-controls")


class PlayerControlsComponentClient(IProvideGameObjectComponent[PlayerControlsComponent]):

    _input_event_dispatcher: InputEventDispatcher
    _clock: GameClock
    _position_client: PositionComponentClient

    def __init__(
        self,
        input_event_dispatcher: InputEventDispatcher,
        clock: GameClock,
        position_client: PositionComponentClient,
    ) -> None:
        self._input_event_dispatcher = input_event_dispatcher
        self._clock = clock
        self._position_client = position_client

    def tick(self, game_object: GameObjectId) -> None:
        self.get(game_object).tick()

    @lru_cache()
    def get(self, game_object: GameObjectId) -> EntityType:
        movement_client = MovementClient()

        def _on_move(event: EventType, payload: PlayerMoveEvent) -> None:
            movement_client.move(payload.direction)

        self._input_event_dispatcher.subscribe(
            event=GameInputs.MOVE_UP,
            callback=_on_move,
        )
        self._input_event_dispatcher.subscribe(
            event=GameInputs.MOVE_DOWN,
            callback=_on_move,
        )
        self._input_event_dispatcher.subscribe(
            event=GameInputs.MOVE_LEFT,
            callback=_on_move,
        )
        self._input_event_dispatcher.subscribe(
            event=GameInputs.MOVE_RIGHT,
            callback=_on_move,
        )
        return PlayerControlsComponent(
            position_component=self._position_client.create(game_object),
            movement_client=movement_client,
            clock=self._clock,
            game_object=game_object
        )
