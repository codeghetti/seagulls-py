import logging
from typing import Tuple

from pygame.font import Font

from seagulls.cat_demos.engine.v2.components._color import Color
from seagulls.cat_demos.engine.v2.components._component_containers import GameComponentId
from seagulls.cat_demos.engine.v2.components._game_objects import GameObjectId
from seagulls.cat_demos.engine.v2.components._prefabs import GameComponentConfig, GameObjectConfig, PrefabClient
from seagulls.cat_demos.engine.v2.components._size import Size
from seagulls.cat_demos.engine.v2.position._point import Position
from seagulls.cat_demos.engine.v2.sessions._app import SeagullsApp, SessionComponents
from seagulls.cat_demos.engine.v2.sessions._executables import IExecutable
from seagulls.cat_demos.engine.v2.sprites._sprite_component import Sprite, SpriteId, SpriteSource
from seagulls.cat_demos.engine.v2.text._component import Text

logger = logging.getLogger(__name__)


class OpenScene(IExecutable):
    _prefab_client: PrefabClient

    def __init__(self, prefab_client: PrefabClient) -> None:
        self._prefab_client = prefab_client

    def __call__(self) -> None:
        self._prefab_client.run(SessionComponents.OBJECT_PREFAB, GameObjectConfig(
            object_id=GameObjectId("hello-world"),
            components=(
                GameComponentConfig(
                    component_id=GameComponentId[Position]("object-component::position"),
                    config=Position(10, 600),
                ),
                GameComponentConfig(
                    component_id=GameComponentId[Text]("object-component::text"),
                    config=Text(
                        value="hello, prefabs!",
                        font=GameComponentId[Font]("font.default"),
                        size=13,
                        color=Color(red=200, green=150, blue=150),
                    ),
                ),
                GameComponentConfig(
                    component_id=GameComponentId[Sprite]("object-component::sprite"),
                    config=Sprite(sprite_id=SpriteId("player")),
                ),
            ),
        ))


app = SeagullsApp()

component_factory = app.component_factory()
session_components = app.session_components()
scene_components = app.scene_components()

app.run(
    (SessionComponents.INDEX_OPEN_EXECUTABLE, lambda: OpenScene(
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
