import logging
from typing import Tuple

from pygame.font import Font

from seagulls.cat_demos.engine.v2.components._color import Color
from seagulls.cat_demos.engine.v2.components._component_containers import GameComponentId
from seagulls.cat_demos.engine.v2.components._game_objects import GameObjectId
from seagulls.cat_demos.engine.v2.components._prefabs import GamePrefabId, PrefabClient
from seagulls.cat_demos.engine.v2.components._scene_objects import SceneObjects
from seagulls.cat_demos.engine.v2.components._size import Size
from seagulls.cat_demos.engine.v2.eventing._client import GameEventDispatcher
from seagulls.cat_demos.engine.v2.position._point import Position
from seagulls.cat_demos.engine.v2.position._prefab import PositionConfig
from seagulls.cat_demos.engine.v2.sessions._app import SeagullsApp, SessionComponents
from seagulls.cat_demos.engine.v2.sessions._executables import IExecutable
from seagulls.cat_demos.engine.v2.sprites._sprite_component import Sprite, SpriteId, SpriteSource
from seagulls.cat_demos.engine.v2.sprites._sprite_prefab import SpritePrefabRequest
from seagulls.cat_demos.engine.v2.text._component import Text
from seagulls.cat_demos.engine.v2.text._prefab import TextConfig
from seagulls.cat_demos.engine.v2.window._window import WindowClient

logger = logging.getLogger(__name__)


class OpenScene(IExecutable):
    _scene_objects: SceneObjects
    _scene_event_client: GameEventDispatcher
    _window_client: WindowClient
    _prefab_client: PrefabClient

    def __init__(
        self,
        scene_objects: SceneObjects,
        scene_event_client: GameEventDispatcher,
        window_client: WindowClient,
        prefab_client: PrefabClient,
    ) -> None:
        self._scene_objects = scene_objects
        self._scene_event_client = scene_event_client
        self._window_client = window_client
        self._prefab_client = prefab_client

    def __call__(self) -> None:
        logger.warning("index scene open")
        hello_world = GameObjectId("hello-world")
        self._scene_objects.add(hello_world)
        self._prefab_client.run(
            prefab_id=GamePrefabId[PositionConfig]("prefab.position-component"),
            config=PositionConfig(
                object_id=hello_world,
                position=Position(20, 400),
            ))

        self._prefab_client.run(
            prefab_id=GamePrefabId[TextConfig]("prefab.text-component"),
            config=TextConfig(
                object_id=hello_world,
                text=Text(
                    value="hello, prefabs!",
                    font=GameComponentId[Font]("font.default"),
                    size=13,
                    color=Color(red=200, green=150, blue=150),
                ),
            ))

        self._prefab_client.run(
            prefab_id=GamePrefabId[SpritePrefabRequest]("prefab.sprite-component"),
            config=SpritePrefabRequest(
                object_id=hello_world,
                sprite=Sprite(sprite_id=SpriteId("player")),
            ))


app = SeagullsApp()

component_factory = app.component_factory()
session_components = app.session_components()
scene_components = app.scene_components()

app.run(
    (SessionComponents.INDEX_OPEN_EXECUTABLE, lambda: OpenScene(
        scene_objects=scene_components.get(SessionComponents.SCENE_OBJECTS),
        scene_event_client=scene_components.get(SessionComponents.EVENT_CLIENT),
        window_client=session_components.get(SessionComponents.WINDOW_CLIENT),
        prefab_client=session_components.get(SessionComponents.PREFAB_CLIENT),
    )),
    (GameComponentId[Tuple[SpriteSource, ...]]("sprite-sources"), lambda: tuple([
        SpriteSource(
            sprite_id=SpriteId("player"),
            image_name="kenney.tiny-dungeon/tilemap-packed",
            coordinates=Position(x=16, y=16*7),
            size=Size(16, 16),
        ),
    ])),
)
