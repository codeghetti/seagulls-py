from typing import NamedTuple

from seagulls.cat_demos.engine.v2.collisions._collision_client import RectCollider, \
    SelectionLayerId, SelectionLayers
from seagulls.cat_demos.engine.v2.components._color import Color
from seagulls.cat_demos.engine.v2.components._entities import GameObjectId
from seagulls.cat_demos.engine.v2.components._object_data import ObjectDataId
from seagulls.cat_demos.engine.v2.components._scene_objects import SceneObjects
from seagulls.cat_demos.engine.v2.components._size import Size
from seagulls.cat_demos.engine.v2.eventing._event_dispatcher import GameEventDispatcher
from seagulls.cat_demos.engine.v2.position._point import Position
from seagulls.cat_demos.engine.v2.sprites._sprite_component import Sprite, SpriteId
from seagulls.cat_demos.engine.v2.text._text_component import Text


class ButtonConfig(NamedTuple):
    object_id: GameObjectId
    position: Position
    size: Size
    sprite_id: SpriteId
    hover_sprite_id: SpriteId
    text: str


class GuiClient:
    _scene_objects: SceneObjects
    _event_client: GameEventDispatcher

    def __init__(
            self,
            scene_objects: SceneObjects,
            event_client: GameEventDispatcher,
    ) -> None:
        self._scene_objects = scene_objects
        self._event_client = event_client

    def create_button(self, request: ButtonConfig) -> None:
        self._scene_objects.add(request.object_id)
        self._scene_objects.set_data(
            entity_id=request.object_id,
            data_id=ObjectDataId[Position]("position"),
            config=request.position,
        )
        self._scene_objects.set_data(
            entity_id=request.object_id,
            data_id=ObjectDataId[Sprite]("sprite"),
            config=Sprite(sprite_id=request.sprite_id, layer="ui"),
        )
        self._scene_objects.set_data(
            entity_id=request.object_id,
            data_id=ObjectDataId[Text]("text"),
            config=Text(
                value="Pew Pew!",
                font="monospace",
                size=40,
                color=Color(red=30, blue=30, green=30),
            ),
        )
        self._scene_objects.set_data(
            entity_id=request.object_id,
            data_id=ObjectDataId[RectCollider]("rect-collider"),
            config=RectCollider(
                size=request.size,
                layers=SelectionLayers(
                    appears_in=frozenset({SelectionLayerId("buttons")}),
                    searches_in=frozenset({}),
                ),
            ),
        )
