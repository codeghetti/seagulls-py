from seagulls.cat_demos.engine.v2.components._component_containers import (
    GameComponentId
)
from seagulls.cat_demos.engine.v2.components._entities import GameObjectId
from seagulls.cat_demos.engine.v2.components._scene_objects import SceneObjects
from seagulls.cat_demos.engine.v2.input._game_clock import GameClock
from seagulls.cat_demos.engine.v2.position._point import Position


class RockManager:
    _scene_objects: SceneObjects
    _clock: GameClock

    def __init__(
        self,
        scene_objects: SceneObjects,
        clock: GameClock,
    ) -> None:
        self._scene_objects = scene_objects
        self._clock = clock

    def tick(self):
        delta = self._clock.get_delta()
        current_position = self._scene_objects.get_component(
            entity_id=GameObjectId("rock-large"),
            component_id=GameComponentId[Position]("object-component::position"),
        )
        adjusted_direction = Position(x=0, y=1 * delta / 10)
        self._scene_objects.set_component(
            entity_id=GameObjectId("rock-large"),
            component_id=GameComponentId[Position]("object-component::position"),
            config=current_position + adjusted_direction,
        )
