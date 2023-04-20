from enum import Enum, auto
from typing import NamedTuple, Tuple

from seagulls.cat_demos.app._cli_command import ComponentProviderCollection
from seagulls.cat_demos.app._index_scene import IndexScene
from seagulls.cat_demos.app.dev._client_window_scene import ClientWindowScene
from seagulls.cat_demos.app.dev._server_prefab import DefaultExecutable, GameServerIds, GameServerPrefab, \
    GameServerProcessManager, ServerEventForwarder
from seagulls.cat_demos.app.environment._world_elements import WorldElementIds, WorldElementPrefab
from seagulls.cat_demos.app.player._mouse_controls import MouseControlIds, MouseControlsPrefab
from seagulls.cat_demos.app.player._player_controls import PlayerControlIds, PlayerControlsPrefab
from seagulls.cat_demos.engine.v2.colliders._collider_component import ColliderPrefabIds
from seagulls.cat_demos.engine.v2.components._color import Color
from seagulls.cat_demos.engine.v2.components._entities import GameSceneId
from seagulls.cat_demos.engine.v2.components._service_provider import ServiceProvider
from seagulls.cat_demos.engine.v2.components._size import Size
from seagulls.cat_demos.engine.v2.frames._frames_client import FrameEvents
from seagulls.cat_demos.engine.v2.position._point import Position
from seagulls.cat_demos.engine.v2.scenes._client import SceneEvents
from seagulls.cat_demos.engine.v2.sessions._app import SeagullsApp, SessionComponents
from seagulls.cat_demos.engine.v2.sprites._sprite_component import SpriteId, SpriteSource
from seagulls.cat_demos.engine.v2.window._window import ServerWindowClient, WindowClient


class ProcessType(Enum):
    STANDALONE = auto()
    CLIENT = auto()
    SERVER = auto()


class CatDemosAppSettings(NamedTuple):
    process_type: ProcessType


class CatDemosComponentProviders:

    _app: SeagullsApp
    _settings: ServiceProvider[CatDemosAppSettings]

    def __init__(self, app: SeagullsApp, settings: ServiceProvider[CatDemosAppSettings]) -> None:
        self._app = app
        self._settings = settings

    def __call__(self):
        session_components = self._app.session_components()
        scene_components = self._app.scene_components()
        settings = self._settings()

        print(f"settings: {settings}")

        components_by_type = {
            ProcessType.STANDALONE: lambda: (
                (SessionComponents.WINDOW_CLIENT, lambda: WindowClient()),
            ),
            ProcessType.CLIENT: lambda: (
                (SessionComponents.WINDOW_CLIENT, lambda: WindowClient()),
            ),
            ProcessType.SERVER: lambda: (
                (SessionComponents.WINDOW_CLIENT, lambda: ServerWindowClient(
                    connection=lambda: scene_components.get(GameServerIds.SERVER_PROCESS_CONNECTION),
                )),
                (GameServerIds.SERVER_MSG_HANDLER, lambda: ServerEventForwarder(
                    connection=scene_components.get(GameServerIds.SERVER_PROCESS_CONNECTION),
                    event_client=scene_components.get(SessionComponents.EVENT_CLIENT),
                )),
            ),
        }

        def _set_background() -> None:
            # Just a quick hack until this moves somewhere permanent
            scene_components.get(SessionComponents.WINDOW_CLIENT).get_surface().fill(Color(20, 20, 20))

        events_by_type = {
            ProcessType.STANDALONE: lambda: (
                (SceneEvents.open_scene(GameSceneId("index")), lambda: IndexScene(
                    prefab_client=session_components.get(SessionComponents.PREFAB_CLIENT),
                    event_client=scene_components.get(SessionComponents.EVENT_CLIENT),
                    window_client=scene_components.get(SessionComponents.WINDOW_CLIENT),
                )()),
            ),
            ProcessType.CLIENT: lambda: (
                (SceneEvents.open_scene(GameSceneId("index")), lambda: ClientWindowScene(
                    prefab_client=session_components.get(SessionComponents.PREFAB_CLIENT),
                    event_client=scene_components.get(SessionComponents.EVENT_CLIENT),
                )()),
                (FrameEvents.CLOSE, lambda: scene_components.get(GameServerIds.PREFAB_COMPONENT).on_frame_close()),
                (SceneEvents.OPEN, lambda: scene_components.get(GameServerIds.PREFAB_COMPONENT).on_scene_open()),
            ),
            ProcessType.SERVER: lambda: (
                (SceneEvents.open_scene(GameSceneId("index")), lambda: IndexScene(
                    prefab_client=session_components.get(SessionComponents.PREFAB_CLIENT),
                    event_client=scene_components.get(SessionComponents.EVENT_CLIENT),
                    window_client=scene_components.get(SessionComponents.WINDOW_CLIENT),
                )()),
                (FrameEvents.OPEN, lambda: scene_components.get(GameServerIds.SERVER_MSG_HANDLER).tick()),
                (FrameEvents.OPEN, lambda: _set_background()),
            ),
        }

        return (
            *components_by_type[settings.process_type](),
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
                *events_by_type[settings.process_type](),
            ])),
            (SessionComponents.PLUGIN_SPRITE_SOURCES, self._sprites),
            (GameServerIds.PREFAB_COMPONENT, lambda: GameServerPrefab(
                scene_objects=scene_components.get(SessionComponents.SCENE_OBJECTS),
                object_prefab=scene_components.get(SessionComponents.OBJECT_PREFAB),
                window_client=scene_components.get(SessionComponents.WINDOW_CLIENT),
                event_client=scene_components.get(SessionComponents.EVENT_CLIENT),
                executable=scene_components.get(GameServerIds.SUBPROCESS_EXECUTABLE),
                process_manager=GameServerProcessManager(),
            )),
            (GameServerIds.SUBPROCESS_EXECUTABLE, lambda: DefaultExecutable(
                app_factory=create_server,
            )),
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


def create_server() -> Tuple[SeagullsApp, ServiceProvider[ComponentProviderCollection]]:
    app = SeagullsApp()
    return app, CatDemosComponentProviders(
        app=app,
        settings=lambda: CatDemosAppSettings(process_type=ProcessType.SERVER)
    )
