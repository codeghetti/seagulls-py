from enum import Enum, auto
from typing import NamedTuple, Tuple

from seagulls.cat_demos.app._cli_command import ComponentProviderCollection
from seagulls.cat_demos.app._index_scene import IndexScene
from seagulls.cat_demos.app.dev._client_window_scene import ClientWindowScene
from seagulls.cat_demos.app.dev._game_server import (DefaultExecutable, FilesystemMonitor,
                                                     GameServerClient, GameServerComponent,
                                                     GameServerProcessManager,
                                                     ServerEventForwarder)
from seagulls.cat_demos.app.environment._world_elements import (WorldElementClient,
                                                                WorldElementComponent)
from seagulls.cat_demos.app.player._mouse_controls import (MouseControlClient,
                                                           MouseControlComponent)
from seagulls.cat_demos.app.player._player_controls import (PlayerControlClient,
                                                            PlayerControlComponent)
from seagulls.cat_demos.app.space_shooter._mob_controls_client import RockManager
from seagulls.cat_demos.engine.v2.collisions._collision_client import (
    ColliderComponent
)
from seagulls.cat_demos.engine.v2.components._client_containers import GameClientProvider
from seagulls.cat_demos.engine.v2.components._color import Color
from seagulls.cat_demos.engine.v2.components._entities import GameClientId, GameSceneId
from seagulls.cat_demos.engine.v2.components._size import Size
from seagulls.cat_demos.engine.v2.frames._frames_client import FrameEvents
from seagulls.cat_demos.engine.v2.position._point import Position
from seagulls.cat_demos.engine.v2.scenes._client import SceneEvents
from seagulls.cat_demos.engine.v2.sessions._app import (
    SeagullsApp,
    SessionComponents
)
from seagulls.cat_demos.engine.v2.sprites._sprite_component import (
    SpriteId,
    SpriteSource
)
from seagulls.cat_demos.engine.v2.window._window import (
    ServerWindowClient,
    WindowClient
)


class ProcessType(Enum):
    STANDALONE = auto()
    CLIENT = auto()
    SERVER = auto()


class CatDemosAppSettings(NamedTuple):
    process_type: ProcessType


class CatDemosComponentProviders:
    _app: SeagullsApp
    _settings: GameClientProvider[CatDemosAppSettings]

    def __init__(
        self, app: SeagullsApp, settings: GameClientProvider[CatDemosAppSettings]
    ) -> None:
        self._app = app
        self._settings = settings

    def __call__(self):
        session_components = self._app.session_components()
        scene_components = self._app.scene_components()
        settings = self._settings()

        print(f"settings: {settings}")
        layers = (
            "background",
            "environment",
            "units",
            "ui",
            "mouse",
        )

        components_by_type = {
            ProcessType.STANDALONE: lambda: (
                (SessionComponents.WINDOW_CLIENT, lambda: WindowClient(layers=layers)),
            ),
            ProcessType.CLIENT: lambda: (
                (SessionComponents.WINDOW_CLIENT, lambda: WindowClient(layers=layers)),
            ),
            ProcessType.SERVER: lambda: (
                (
                    SessionComponents.WINDOW_CLIENT,
                    lambda: ServerWindowClient(
                        layers=layers,
                        connection=lambda: session_components.get(
                            GameServerComponent.SERVER_PROCESS_CONNECTION
                        ),
                    ),
                ),
                (
                    GameServerComponent.SERVER_MSG_HANDLER,
                    lambda: ServerEventForwarder(
                        connection=session_components.get(
                            GameServerComponent.SERVER_PROCESS_CONNECTION
                        ),
                        event_client=scene_components.get(
                            SessionComponents.EVENT_CLIENT_ID
                        ),
                    ),
                ),
            ),
        }

        def _set_background() -> None:
            # Just a quick hack until this moves somewhere permanent
            session_components.get(SessionComponents.WINDOW_CLIENT).get_surface().fill(
                Color(20, 20, 20)
            )

        events_by_type = {
            ProcessType.STANDALONE: lambda: (
                (
                    SceneEvents.open_scene(GameSceneId("index")),
                    lambda: IndexScene(
                        scene_objects=scene_components.get(
                            SessionComponents.SCENE_OBJECTS_CLIENT_ID,
                        ),
                        event_client=scene_components.get(
                            SessionComponents.EVENT_CLIENT_ID
                        ),
                        window_client=session_components.get(
                            SessionComponents.WINDOW_CLIENT
                        ),
                        world_elements=scene_components.get(
                            WorldElementComponent.CLIENT_ID
                        ),
                        mouse_controls=session_components.get(
                            MouseControlComponent.CLIENT_ID,
                        ),
                        player_controls=session_components.get(
                            PlayerControlComponent.CLIENT_ID,
                        ),
                        debug_hud=session_components.get(
                            SessionComponents.DEBUG_HUD_CLIENT_ID,
                        ),
                    )(),
                ),
                (FrameEvents.OPEN, lambda: _set_background()),
                # TODO: move this to only be registered when we are running the space shooter
                # (
                #     FrameEvents.OPEN,
                #     lambda: scene_components.get(GameClientId("RockManager")).tick(),
                # ),
            ),
            ProcessType.CLIENT: lambda: (
                (
                    SceneEvents.open_scene(GameSceneId("index")),
                    lambda: ClientWindowScene(
                        event_client=scene_components.get(
                            SessionComponents.EVENT_CLIENT_ID
                        ),
                        server=scene_components.get(
                            GameServerComponent.CLIENT_ID,
                        ),
                    )(),
                ),
                (
                    FrameEvents.CLOSE,
                    lambda: scene_components.get(
                        GameServerComponent.CLIENT_ID
                    ).on_frame_close(),
                ),
                (
                    SceneEvents.OPEN,
                    lambda: scene_components.get(
                        GameServerComponent.CLIENT_ID
                    ).on_scene_open(),
                ),
            ),
            ProcessType.SERVER: lambda: (
                (
                    SceneEvents.open_scene(GameSceneId("index")),
                    lambda: IndexScene(
                        scene_objects=scene_components.get(
                            SessionComponents.SCENE_OBJECTS_CLIENT_ID,
                        ),
                        event_client=scene_components.get(
                            SessionComponents.EVENT_CLIENT_ID
                        ),
                        window_client=session_components.get(
                            SessionComponents.WINDOW_CLIENT
                        ),
                        world_elements=scene_components.get(
                            WorldElementComponent.CLIENT_ID
                        ),
                        mouse_controls=session_components.get(
                            MouseControlComponent.CLIENT_ID,
                        ),
                        player_controls=session_components.get(
                            PlayerControlComponent.CLIENT_ID,
                        ),
                        debug_hud=session_components.get(
                            SessionComponents.DEBUG_HUD_CLIENT_ID,
                        ),
                    )(),
                ),
                (
                    FrameEvents.OPEN,
                    lambda: scene_components.get(
                        GameServerComponent.SERVER_MSG_HANDLER
                    ).tick(),
                ),
                (FrameEvents.OPEN, lambda: _set_background()),
                # (
                #     FrameEvents.OPEN,
                #     lambda: scene_components.get(GameClientId("RockManager")).tick(),
                # ),
            ),
        }

        return (
            *components_by_type[settings.process_type](),
            (
                PlayerControlComponent.CLIENT_ID,
                lambda: PlayerControlClient(
                    scene_objects=scene_components.get(SessionComponents.SCENE_OBJECTS_CLIENT_ID),
                    event_client=scene_components.get(SessionComponents.EVENT_CLIENT_ID),
                    toggles=scene_components.get(
                        SessionComponents.INPUT_TOGGLES_CLIENT_ID
                    ),
                    clock=scene_components.get(SessionComponents.SCENE_CLOCK),
                    collisions=scene_components.get(ColliderComponent.CLIENT_ID),
                ),
            ),
            (
                GameClientId("RockManager"),
                lambda: RockManager(
                    scene_objects=scene_components.get(SessionComponents.SCENE_OBJECTS_CLIENT_ID),
                    clock=scene_components.get(SessionComponents.SCENE_CLOCK),
                ),
            ),
            (
                MouseControlComponent.CLIENT_ID,
                lambda: MouseControlClient(
                    scene_objects=scene_components.get(SessionComponents.SCENE_OBJECTS_CLIENT_ID),
                    event_client=scene_components.get(SessionComponents.EVENT_CLIENT_ID),
                    collisions=scene_components.get(ColliderComponent.CLIENT_ID),
                ),
            ),
            (
                WorldElementComponent.CLIENT_ID,
                lambda: WorldElementClient(
                    scene_objects=scene_components.get(SessionComponents.SCENE_OBJECTS_CLIENT_ID),
                ),
            ),
            (
                SessionComponents.PLUGIN_EVENT_CALLBACKS,
                lambda: tuple(
                    [
                        *events_by_type[settings.process_type](),
                    ]
                ),
            ),
            (SessionComponents.PLUGIN_SPRITE_SOURCES, self._sprites),
            (
                GameServerComponent.CLIENT_ID,
                lambda: GameServerClient(
                    scene_objects=scene_components.get(SessionComponents.SCENE_OBJECTS_CLIENT_ID),
                    window_client=session_components.get(SessionComponents.WINDOW_CLIENT),
                    event_client=scene_components.get(SessionComponents.EVENT_CLIENT_ID),
                    executable=scene_components.get(
                        GameServerComponent.SUBPROCESS_EXECUTABLE
                    ),
                    process_manager=GameServerProcessManager(),
                    filesystem_monitor=FilesystemMonitor(),
                ),
            ),
            (
                GameServerComponent.SUBPROCESS_EXECUTABLE,
                lambda: DefaultExecutable(
                    app_factory=create_server,
                ),
            ),
        )

    def _sprites(self) -> Tuple[SpriteSource, ...]:
        return tuple(
            [
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
                SpriteSource(
                    sprite_id=SpriteId("chest.closed"),
                    image_name="kenney.tiny-dungeon/tilemap-packed",
                    coordinates=Position(x=16 * 5, y=16 * 7),
                    size=Size(height=16, width=16),
                ),
                SpriteSource(
                    sprite_id=SpriteId("star_background"),
                    image_name="space-shooter/environment-stars",
                    coordinates=Position(x=0, y=0),
                    size=Size(height=600, width=1024),
                ),
                SpriteSource(
                    sprite_id=SpriteId("spaceship"),
                    image_name="space-shooter/ship-orange",
                    coordinates=Position(x=0, y=0),
                    size=Size(112, 75),
                ),
                SpriteSource(
                    sprite_id=SpriteId("rock-large"),
                    image_name="space-shooter/rock-large",
                    coordinates=Position(x=0, y=0),
                    size=Size(height=120, width=98),
                ),
            ]
        )


def create_server() -> Tuple[SeagullsApp, GameClientProvider[ComponentProviderCollection]]:
    app = SeagullsApp()
    return app, CatDemosComponentProviders(
        app=app, settings=lambda: CatDemosAppSettings(process_type=ProcessType.SERVER)
    )
