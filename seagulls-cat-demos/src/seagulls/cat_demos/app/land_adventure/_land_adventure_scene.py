from seagulls.cat_demos.app.environment._world_elements import (
    WorldElement,
    WorldElementClient, WorldElementId
)
from seagulls.cat_demos.app.player._mouse_controls import (
    MouseControlClient, MouseControls
)
from seagulls.cat_demos.app.player._player_controls import (
    PlayerControlClient
)
from seagulls.cat_demos.engine.v2.collisions._collision_client import (
    RectCollider
)
from seagulls.cat_demos.engine.v2.components._color import Color
from seagulls.cat_demos.engine.v2.components._entities import GameObjectId
from seagulls.cat_demos.engine.v2.components._object_data import ObjectDataId
from seagulls.cat_demos.engine.v2.components._scene_objects import SceneObjects
from seagulls.cat_demos.engine.v2.components._size import Size
from seagulls.cat_demos.engine.v2.debugging._debug_hud_client import DebugHud, DebugHudClient
from seagulls.cat_demos.engine.v2.eventing._event_dispatcher import (
    GameEventDispatcher
)
from seagulls.cat_demos.engine.v2.position._point import Position
from seagulls.cat_demos.engine.v2.sessions._executables import IExecutable
from seagulls.cat_demos.engine.v2.sprites._sprite_component import (
    Sprite,
    SpriteId
)
from seagulls.cat_demos.engine.v2.text._text_component import Text
from seagulls.cat_demos.engine.v2.window._window import WindowClient


class LandAdventureScene(IExecutable):
    _scene_objects: SceneObjects
    _event_client: GameEventDispatcher
    _window_client: WindowClient
    _world_elements: WorldElementClient
    _mouse_controls: MouseControlClient
    _player_controls: PlayerControlClient
    _debug_hud: DebugHudClient

    def __init__(
        self,
        scene_objects: SceneObjects,
        event_client: GameEventDispatcher,
        window_client: WindowClient,
        world_elements: WorldElementClient,
        mouse_controls: MouseControlClient,
        player_controls: PlayerControlClient,
        debug_hud: DebugHudClient,
    ) -> None:
        self._scene_objects = scene_objects
        self._event_client = event_client
        self._window_client = window_client
        self._world_elements = world_elements
        self._mouse_controls = mouse_controls
        self._player_controls = player_controls
        self._debug_hud = debug_hud

    def __call__(self) -> None:
        self._spawn_environment()
        self._spawn_player()
        self._spawn_menu()
        self._spawn_mouse()
        self._spawn_debug_hud()

    def _spawn_environment(self):
        for x in range(15):
            for y in range(15):
                self._world_elements.spawn(WorldElement(
                    object_id=GameObjectId(f"barrel::{x}.{y}"),
                    sprite_id=WorldElementId.BARREL,
                    position=Position(x=50 + (x * 32), y=50 + (y * 32)),
                ))

    def _spawn_player(self) -> None:
        object_id = GameObjectId("player")
        self._scene_objects.add(object_id)
        self._scene_objects.set_data(
            entity_id=object_id,
            data_id=ObjectDataId[Position]("position"),
            config=Position(200, 700),
        )
        self._scene_objects.set_data(
            entity_id=object_id,
            data_id=ObjectDataId[Sprite]("sprite"),
            config=Sprite(sprite_id=SpriteId("player"), layer="units"),
        )
        self._scene_objects.set_data(
            entity_id=object_id,
            data_id=ObjectDataId[RectCollider]("rect-collider"),
            config=RectCollider(size=Size(width=16, height=16)),
        )

    def _spawn_mouse(self) -> None:
        object_id = GameObjectId("mouse")
        self._scene_objects.add(object_id)
        self._scene_objects.set_data(
            entity_id=object_id,
            data_id=ObjectDataId[Position]("position"),
            config=Position(0, 0),
        )
        self._scene_objects.set_data(
            entity_id=object_id,
            data_id=ObjectDataId[Sprite]("sprite"),
            config=Sprite(sprite_id=SpriteId("mouse"), layer="mouse"),
        )

        self._mouse_controls.attach_mouse(MouseControls(object_id=GameObjectId("mouse")))

    def _spawn_menu(self) -> None:
        object_id = GameObjectId("menu:quit")
        self._scene_objects.add(object_id)
        self._scene_objects.set_data(
            entity_id=object_id,
            data_id=ObjectDataId[Position]("position"),
            config=Position(600, 10),
        )
        self._scene_objects.set_data(
            entity_id=object_id,
            data_id=ObjectDataId[Sprite]("sprite"),
            config=Sprite(sprite_id=SpriteId("menu-button"), layer="ui"),
        )
        self._scene_objects.set_data(
            entity_id=object_id,
            data_id=ObjectDataId[Text]("text"),
            config=Text(
                value="Quit!",
                font="monospace",
                size=40,
                color=Color(red=30, blue=30, green=30),
            ),
        )

    def _spawn_debug_hud(self) -> None:
        self._debug_hud.execute(DebugHud(show_fps=True))
