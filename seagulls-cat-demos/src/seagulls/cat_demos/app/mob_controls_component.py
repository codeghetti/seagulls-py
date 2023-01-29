from __future__ import annotations

import logging

from functools import lru_cache

from seagulls.cat_demos.engine.v2._entities import GameComponent, GameObject
from seagulls.cat_demos.engine.v2._game_clock import GameClock
from seagulls.cat_demos.engine.v2._movement import MovementClient
from seagulls.cat_demos.engine.v2._position_component import PositionComponent, \
    PositionComponentClient
from seagulls.cat_demos.engine.v2._scene import IProvideGameObjectComponent

logger = logging.getLogger(__name__)


class MobControlsComponent:

    _position_component: PositionComponent
    _target_position_component: PositionComponent
    _clock: GameClock
    _object: GameObject

    def __init__(
        self,
        position_component: PositionComponent,
        target_position_component: PositionComponent,
        clock: GameClock,
        game_object: GameObject,
    ) -> None:
        self._position_component = position_component
        self._target_position_component = target_position_component
        self._clock = clock
        self._object = game_object

    def tick(self) -> None:
        delta = self._clock.get_delta()
        # normalized = Vector(vector.x * delta / 10, vector.y * delta / 10)
        # if vector != Vector.zero():
        #     logger.debug(f"move: {self._object} + {normalized} delta={delta}")
        # self._position_component.update(
        #     self._position_component.get() + normalized,
        # )
        # self._movement_client.reset()


MobControlsComponentId = GameComponent[MobControlsComponent]("mob-controls")


class MobControlsComponentClient(IProvideGameObjectComponent[MobControlsComponent]):

    _clock: GameClock
    _position_client: PositionComponentClient

    def __init__(
        self,
        clock: GameClock,
        position_client: PositionComponentClient,
    ) -> None:
        self._clock = clock
        self._position_client = position_client

    def tick(self, game_object: GameObject) -> None:
        self.get(game_object).tick()

    @lru_cache()
    def get(self, game_object: GameObject) -> MobControlsComponent:
        return MobControlsComponent(
            position_component=self._position_client.get(game_object),
            # TODO: make this settable when attaching the component
            target_position_component=self._position_client.get(GameObject("player")),
            clock=self._clock,
            game_object=game_object
        )
