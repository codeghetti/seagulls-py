from typing import NamedTuple

from seagulls.cat_demos.app.player._mouse_controls import MouseControlClient, MouseControlComponent, \
    MouseControls
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
    down_sprite_id: SpriteId
    text: str


class GuiClient:
    _scene_objects: SceneObjects
    _mouse_controls: MouseControlClient
    _event_client: GameEventDispatcher

    def __init__(
            self,
            scene_objects: SceneObjects,
            mouse_controls: MouseControlClient,
            event_client: GameEventDispatcher,

    ) -> None:
        self._scene_objects = scene_objects
        self._mouse_controls = mouse_controls
        self._event_client = event_client

    def create_mouse(self) -> None:
        object_id = GameObjectId("mouse")
        self._scene_objects.add(object_id)
        self._scene_objects.set_data(
            object_id=object_id,
            data_id=ObjectDataId[Position]("position"),
            config=Position(0, 0),
        )
        self._scene_objects.set_data(
            object_id=object_id,
            data_id=ObjectDataId[Sprite]("sprite"),
            config=Sprite(sprite_id=SpriteId("mouse"), layer="mouse"),
        )
        self._scene_objects.set_data(
            object_id=object_id,
            data_id=ObjectDataId[RectCollider]("rect-collider"),
            config=RectCollider(
                size=Size(height=49, width=190),
                layers=SelectionLayers(
                    appears_in=frozenset({SelectionLayerId("mouse")}),
                    searches_in=frozenset({SelectionLayerId("buttons")}),
                ),
            ),
        )

        self._mouse_controls.attach_mouse(MouseControls(object_id=GameObjectId("mouse")))

    def create_button(self, button: ButtonConfig) -> None:
        self._scene_objects.add(button.object_id)
        self._scene_objects.set_data(
            object_id=button.object_id,
            data_id=ObjectDataId[Position]("position"),
            config=button.position,
        )
        self._scene_objects.set_data(
            object_id=button.object_id,
            data_id=ObjectDataId[Sprite]("sprite"),
            config=Sprite(sprite_id=button.sprite_id, layer="ui"),
        )
        self._scene_objects.set_data(
            object_id=button.object_id,
            data_id=ObjectDataId[Text]("text"),
            config=Text(
                value=button.text,
                font="monospace",
                size=40,
                color=Color(red=30, blue=30, green=30),
            ),
        )
        self._scene_objects.set_data(
            object_id=button.object_id,
            data_id=ObjectDataId[RectCollider]("rect-collider"),
            config=RectCollider(
                size=button.size,
                layers=SelectionLayers(
                    appears_in=frozenset({SelectionLayerId("buttons")}),
                    searches_in=frozenset({}),
                ),
            ),
        )

        def on_enter() -> None:
            self._scene_objects.set_data(
                object_id=button.object_id,
                data_id=ObjectDataId[Sprite]("sprite"),
                config=Sprite(sprite_id=button.hover_sprite_id, layer="ui"),
            )

        def on_exit() -> None:
            self._scene_objects.set_data(
                object_id=button.object_id,
                data_id=ObjectDataId[Sprite]("sprite"),
                config=Sprite(sprite_id=button.sprite_id, layer="ui"),
            )

        def on_click() -> None:
            self._scene_objects.set_data(
                object_id=button.object_id,
                data_id=ObjectDataId[Sprite]("sprite"),
                config=Sprite(sprite_id=button.hover_sprite_id, layer="ui"),
            )

        def on_active() -> None:
            self._scene_objects.set_data(
                object_id=button.object_id,
                data_id=ObjectDataId[Sprite]("sprite"),
                config=Sprite(sprite_id=button.down_sprite_id, layer="ui"),
            )

        self._event_client.register(
            event=MouseControlComponent.target_mouse_enter_event(button.object_id),
            callback=on_enter,
        )
        self._event_client.register(
            event=MouseControlComponent.target_mouse_exit_event(button.object_id),
            callback=on_exit,
        )
        self._event_client.register(
            event=MouseControlComponent.target_click_event(button.object_id),
            callback=on_click,
        )
        self._event_client.register(
            event=MouseControlComponent.target_active_event(button.object_id),
            callback=on_active,
        )
