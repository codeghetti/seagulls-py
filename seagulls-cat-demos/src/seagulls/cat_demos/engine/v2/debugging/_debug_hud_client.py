from typing import NamedTuple

from seagulls.cat_demos.engine.v2.components._color import Color
from seagulls.cat_demos.engine.v2.components._entities import GameObjectId
from seagulls.cat_demos.engine.v2.components._object_data import ObjectDataId
from seagulls.cat_demos.engine.v2.components._scene_objects import SceneObjects
from seagulls.cat_demos.engine.v2.input._game_clock import GameClock
from seagulls.cat_demos.engine.v2.position._point import Position
from seagulls.cat_demos.engine.v2.text._text_component import Text


class DebugHud(NamedTuple):
    show_fps: bool


class DebugHudClient:
    _scene_objects: SceneObjects
    _clock: GameClock

    def __init__(
        self,
        scene_objects: SceneObjects,
        clock: GameClock,
    ) -> None:
        self._scene_objects = scene_objects
        self._clock = clock

    def execute(self, request: DebugHud) -> None:
        object_id = GameObjectId("debug-hud")
        self._scene_objects.add(object_id)
        self._scene_objects.set_data(
            object_id=object_id,
            data_id=ObjectDataId[Position]("position"),
            config=Position(350, 10),
        )
        self._scene_objects.set_data(
            object_id=object_id,
            data_id=ObjectDataId[Text]("text"),
            config=Text(
                value="N/A",
                font="monospace",
                size=20,
                color=Color(red=230, blue=230, green=230),
            ),
        )
        self._scene_objects.set_data(
            object_id=object_id,
            data_id=ObjectDataId[DebugHud]("debug-hud"),
            config=request,
        )

    def tick(self) -> None:
        component_id = ObjectDataId[DebugHud]("debug-hud")
        text_component_id = ObjectDataId[Text]("text")

        for object_id in self._scene_objects.find_by_data_id(component_id):
            text = self._scene_objects.get_data(object_id, text_component_id)
            new_text = Text(
                value=str(self._clock.get_fps()),
                font=text.font,
                size=text.size,
                color=text.color,
            )
            self._scene_objects.set_data(object_id, text_component_id, new_text)
