from argparse import ArgumentParser
from typing import Tuple

from seagulls.cat_demos.app._index_scene import IndexScene
from seagulls.cat_demos.app.environment._world_elements import WorldElementIds, WorldElementPrefab
from seagulls.cat_demos.app.player._mouse_controls import MouseControlIds, MouseControlsPrefab
from seagulls.cat_demos.app.player._player_controls import PlayerControlIds, PlayerControlsPrefab
from seagulls.cat_demos.engine.v2.colliders._collider_component import ColliderPrefabIds
from seagulls.cat_demos.engine.v2.components._entities import GameSceneId
from seagulls.cat_demos.engine.v2.components._size import Size
from seagulls.cat_demos.engine.v2.position._point import Position
from seagulls.cat_demos.engine.v2.scenes._client import SceneEvents
from seagulls.cat_demos.engine.v2.sessions._app import SeagullsApp, SessionComponents
from seagulls.cat_demos.engine.v2.sprites._sprite_component import SpriteId, SpriteSource
from seagulls.cli import ICliCommand


class GameCliCommand(ICliCommand):

    _app: SeagullsApp

    def __init__(self, app: SeagullsApp) -> None:
        self._app = app

    def configure_parser(self, parser: ArgumentParser) -> None:
        pass

    def execute(self) -> None:
        try:
            self._run()
        except KeyboardInterrupt:
            pass

    def _run(self) -> None:
        component_factory = self._app.component_factory()
        session_components = self._app.session_components()
        scene_components = self._app.scene_components()

        self._app.run(
            (PlayerControlIds.PREFAB_COMPONENT, lambda: PlayerControlsPrefab(
                scene_objects=scene_components.get(SessionComponents.SCENE_OBJECTS),
                event_client=scene_components.get(SessionComponents.EVENT_CLIENT),
                toggles=scene_components.get(SessionComponents.INPUT_TOGGLES_CLIENT),
                clock=scene_components.get(SessionComponents.SCENE_CLOCK),
                collisions=scene_components.get(ColliderPrefabIds.PREFAB_COMPONENT),
            )),
            (MouseControlIds.PREFAB_COMPONENT, lambda: MouseControlsPrefab(
                scene_objects=scene_components.get(SessionComponents.SCENE_OBJECTS),
                event_client=scene_components.get(SessionComponents.EVENT_CLIENT),
            )),
            (WorldElementIds.PREFAB_COMPONENT, lambda: WorldElementPrefab(
                object_prefab=scene_components.get(SessionComponents.OBJECT_PREFAB),
            )),
            (SessionComponents.PLUGIN_EVENT_CALLBACKS, lambda: tuple([
                (SceneEvents.open_scene(GameSceneId("index")), lambda: IndexScene(
                    prefab_client=session_components.get(SessionComponents.PREFAB_CLIENT),
                    event_client=scene_components.get(SessionComponents.EVENT_CLIENT),
                )()),
            ])),
            (SessionComponents.PLUGIN_SPRITE_SOURCES, self._sprites),
        )

    def _sprites(self) -> Tuple[SpriteSource, ...]:
        return tuple([
            SpriteSource(
                sprite_id=SpriteId("player"),
                image_name="kenney.tiny-dungeon/tilemap-packed",
                coordinates=Position(x=16, y=16 * 7),
                size=Size(16, 16),
            ),
            SpriteSource(
                sprite_id=SpriteId("mouse"),
                image_name="kenney.ui-pack-rpg-expansion/tilemap",
                coordinates=Position(x=30, y=482),
                size=Size(width=30, height=30),
            ),
            SpriteSource(
                sprite_id=SpriteId("menu-button"),
                image_name="kenney.ui-pack-rpg-expansion/tilemap",
                coordinates=Position(x=0, y=188),
                size=Size(height=49, width=190),
            ),
            SpriteSource(
                sprite_id=SpriteId("barrel"),
                image_name="kenney.tiny-dungeon/tilemap-packed",
                coordinates=Position(x=16 * 10, y=16 * 6),
                size=Size(height=16, width=16),
            ),
        ])
