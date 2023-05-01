from typing import NamedTuple

from seagulls.cat_demos.engine.v2.components._color import Color
from seagulls.cat_demos.engine.v2.components._component_containers import (
    ObjectDataId
)
from seagulls.cat_demos.engine.v2.components._entities import GameObjectId
from seagulls.cat_demos.engine.v2.components._prefabs import (
    GameComponentConfig,
    GameObjectConfig,
    GameObjectPrefab,
    IPrefab
)
from seagulls.cat_demos.engine.v2.components._scene_objects import SceneObjects
from seagulls.cat_demos.engine.v2.input._game_clock import GameClock
from seagulls.cat_demos.engine.v2.position._point import Position
from seagulls.cat_demos.engine.v2.text._text_component import Text


class DebugHud(NamedTuple):
    show_fps: bool


class DebugHudPrefab(IPrefab[DebugHud]):
    _scene_objects: SceneObjects
    _object_prefab: GameObjectPrefab
    _clock: GameClock

    def __init__(
        self,
        scene_objects: SceneObjects,
        object_prefab: GameObjectPrefab,
        clock: GameClock,
    ) -> None:
        self._scene_objects = scene_objects
        self._object_prefab = object_prefab
        self._clock = clock

    def execute(self, request: DebugHud) -> None:
        self._object_prefab.execute(
            GameObjectConfig(
                object_id=GameObjectId("debug-hud"),
                components=(
                    GameComponentConfig(
                        component_id=ObjectDataId[Position](
                            "object-component::position"
                        ),
                        config=Position(350, 10),
                    ),
                    GameComponentConfig(
                        component_id=ObjectDataId[Text]("object-component::text"),
                        config=Text(
                            value="N/A",
                            font="monospace",
                            size=20,
                            color=Color(red=230, blue=230, green=230),
                        ),
                    ),
                    GameComponentConfig(
                        component_id=ObjectDataId[DebugHud](
                            "object-component::debug-hud"
                        ),
                        config=request,
                    ),
                ),
            )
        )

    def tick(self) -> None:
        component_id = ObjectDataId[DebugHud]("object-component::debug-hud")
        text_component_id = ObjectDataId[Text]("object-component::text")

        for object_id in self._scene_objects.find_by_data_id(component_id):
            text = self._scene_objects.get_data(object_id, text_component_id)
            new_text = Text(
                value=str(self._clock.get_fps()),
                font=text.font,
                size=text.size,
                color=text.color,
            )
            self._scene_objects.set_data(object_id, text_component_id, new_text)
