from functools import lru_cache
from typing import Any, Callable, NamedTuple, Tuple, TypeAlias

from seagulls.cat_demos.app.gui._gui_client import GuiClient
from seagulls.cat_demos.engine.v2.collisions._collision_client import (
    CollisionClient,
    CollisionComponent,
)
from seagulls.cat_demos.engine.v2.components._client_containers import (
    CachedGameClientContainer,
    ContextualGameClientContainer,
    FilteredGameComponentContainer,
    GameClientContainer,
    GameClientFactory,
    GameClientProvider,
    Tco_GameClientType,
)
from seagulls.cat_demos.engine.v2.components._entities import GameClientId, GameSceneId
from seagulls.cat_demos.engine.v2.components._scene_objects import SceneObjects
from seagulls.cat_demos.engine.v2.debugging._debug_hud_client import DebugHudClient
from seagulls.cat_demos.engine.v2.eventing._event_dispatcher import (
    GameEventDispatcher,
    GameEventId
)
from seagulls.cat_demos.engine.v2.input._game_clock import GameClock
from seagulls.cat_demos.engine.v2.input._input_toggles import (
    InputTogglesClient
)
from seagulls.cat_demos.engine.v2.input._pygame import (
    PygameEvents,
    PygameKeyboardInputPublisher
)
from seagulls.cat_demos.engine.v2.position._position_client import (
    PositionClient
)
from seagulls.cat_demos.engine.v2.resources._resources_client import (
    ResourceClient
)
from seagulls.cat_demos.engine.v2.scenes._frame_client import (
    FrameClient,
    FrameCollection,
    FrameEvents
)
from seagulls.cat_demos.engine.v2.scenes._scene_client import (
    SceneClient,
    SceneContext,
    SceneEvents, )
from seagulls.cat_demos.engine.v2.sprites._sprite_client import SpriteClient
from seagulls.cat_demos.engine.v2.sprites._sprite_component import (
    SpriteComponent,
    SpriteSource
)
from seagulls.cat_demos.engine.v2.text._text_client import TextClient
from seagulls.cat_demos.engine.v2.text._text_component import TextComponent
from seagulls.cat_demos.engine.v2.window._window import WindowClient
from ._executables import QuitGameExecutable
from ._index import CloseScene, OpenScene
from ._session_client import SessionClient

GameEventCallback: TypeAlias = Tuple[GameEventId[Any], Callable[[], None]]


class SessionComponents:
    EVENT_CLIENT_ID = GameClientId[GameEventDispatcher]("event-client")
    INPUT_TOGGLES_CLIENT_ID = GameClientId[InputTogglesClient]("input-toggles-client")
    SCENE_OBJECTS_CLIENT_ID = GameClientId[SceneObjects]("scene-object-client")
    TEXT_CLIENT_ID = GameClientId[TextComponent]("text-client")
    RESOURCE_CLIENT_ID = GameClientId[ResourceClient]("resource-client")
    SPRITE_CLIENT_ID = GameClientId[SpriteComponent]("sprite-client")
    POSITION_CLIENT_ID = GameClientId[PositionClient]("position-client")
    DEBUG_HUD_CLIENT_ID = GameClientId[DebugHudClient]("debug-hud-client")
    COMPONENT_CONTAINER_CLIENT_ID = GameClientId[GameClientContainer]("client-container")
    FRAME_COLLECTION_CLIENT_ID = GameClientId[FrameCollection]("frame-collection")
    INDEX_OPEN_EXECUTABLE = GameClientId[OpenScene]("index-scene:open.executable")
    INDEX_CLOSE_EXECUTABLE = GameClientId[CloseScene]("index-scene:close.executable")
    PYGAME_INPUT_CLIENT = GameClientId[PygameKeyboardInputPublisher]("pygame-input-client")
    QUIT_GAME_EXECUTABLE = GameClientId[QuitGameExecutable]("quit-game-executable")
    SCENE_CONTEXT = GameClientId[SceneContext]("scene-context")
    SCENE_CLIENT = GameClientId[SceneClient]("scene-client")
    SESSION_CLIENT = GameClientId[SessionClient]("session-client")
    WINDOW_CLIENT = GameClientId[WindowClient]("window-client")
    SCENE_CLOCK = GameClientId[GameClock]("scene-clock")

    PLUGIN_EVENT_CALLBACKS = GameClientId[Tuple[GameEventCallback, ...]]("plugin:event-callbacks")
    PLUGIN_SPRITE_SOURCES = GameClientId[Tuple[SpriteSource, ...]]("sprite-sources")

    GUI_CLIENT = GameClientId[GuiClient]("gui-client")


class SeagullsAppProvider(NamedTuple):
    id: GameClientId[Any]
    provider: GameClientProvider[Any]


"""

"""


class SeagullsApp:

    def run(
        self,
        *providers: Tuple[
            GameClientId[Tco_GameClientType], GameClientProvider[Tco_GameClientType]
        ],
    ) -> None:
        component_factory = self._factory()
        # Components built by this class are cached for the duration of the session
        session_components = self.session_components()

        for p in providers:
            component_factory.set(p[0], p[1])

        # TODO: why do I need to type-ignore this?
        component_factory.set_missing(  # type: ignore
            (
                SessionComponents.SESSION_CLIENT,
                lambda: SessionClient(
                    window_client=session_components.get(
                        SessionComponents.WINDOW_CLIENT
                    ),
                    scene_client=session_components.get(SessionComponents.SCENE_CLIENT),
                    first_scene=lambda: GameSceneId("index"),
                ),
            ),
            (
                SessionComponents.SCENE_CLIENT,
                lambda: SceneClient(
                    scene_context=session_components.get(SessionComponents.SCENE_CONTEXT),
                    frame_collection=session_components.get(
                        SessionComponents.FRAME_COLLECTION_CLIENT_ID,
                    ),
                    event_client=session_components.get(SessionComponents.EVENT_CLIENT_ID),
                    # scene_registry=SceneRegistry.with_providers(
                    #     SceneProvider(
                    #         scene_id=GameSceneId("index"),
                    #         provider=lambda: session_components.get(
                    #         SessionComponents.INDEX_SCENE),
                    #     ),
                    #     *session_components.get(SessionComponents.SCENE_PROVIDERS),
                    # ),
                ),
            ),
            (
                SessionComponents.FRAME_COLLECTION_CLIENT_ID,
                lambda: FrameCollection(
                    frame_factory=lambda: FrameClient(
                        event_client=session_components.get(
                            SessionComponents.EVENT_CLIENT_ID
                        ),
                        window_client=session_components.get(
                            SessionComponents.WINDOW_CLIENT
                        ),
                        pygame_input_client=session_components.get(
                            SessionComponents.PYGAME_INPUT_CLIENT
                        ),
                        toggles=session_components.get(
                            SessionComponents.INPUT_TOGGLES_CLIENT_ID
                        ),
                    ),
                    scene_context=session_components.get(SessionComponents.SCENE_CONTEXT),
                ),
            ),
            (SessionComponents.INDEX_OPEN_EXECUTABLE, lambda: OpenScene(
                scene=session_components.get(SessionComponents.SCENE_CONTEXT),
            )),
            (SessionComponents.INDEX_CLOSE_EXECUTABLE, lambda: CloseScene(
                scene=session_components.get(SessionComponents.SCENE_CONTEXT),
            )),
            (
                SessionComponents.PYGAME_INPUT_CLIENT,
                lambda: PygameKeyboardInputPublisher(
                    event_dispatcher=session_components.get(
                        SessionComponents.EVENT_CLIENT_ID
                    ),
                    scene_context=session_components.get(SessionComponents.SCENE_CONTEXT),
                ),
            ),
            (
                SessionComponents.TEXT_CLIENT_ID,
                lambda: TextComponent(
                    objects=session_components.get(SessionComponents.SCENE_OBJECTS_CLIENT_ID),
                    window_client=session_components.get(
                        SessionComponents.WINDOW_CLIENT
                    ),
                ),
            ),
            (
                SessionComponents.SPRITE_CLIENT_ID,
                lambda: SpriteComponent(
                    objects=session_components.get(SessionComponents.SCENE_OBJECTS_CLIENT_ID),
                    window_client=session_components.get(
                        SessionComponents.WINDOW_CLIENT
                    ),
                    resource_client=session_components.get(
                        SessionComponents.RESOURCE_CLIENT_ID
                    ),
                    sprite_sources=session_components.get(
                        SessionComponents.PLUGIN_SPRITE_SOURCES
                    ),
                ),
            ),
            (
                SessionComponents.SCENE_OBJECTS_CLIENT_ID,
                lambda: SceneObjects(
                    scene_context=session_components.get(SessionComponents.SCENE_CONTEXT),
                ),
            ),
            # (SessionComponents.WINDOW_CLIENT, lambda: WindowClient()),
            (SessionComponents.SCENE_CONTEXT, lambda: SceneContext()),
            # TODO: add a filter to this container
            (
                SessionComponents.COMPONENT_CONTAINER_CLIENT_ID,
                lambda: FilteredGameComponentContainer(
                    container=session_components,
                    context=lambda: [
                        GameClientId("object-position"),
                    ],
                ),
            ),
            (
                SessionComponents.EVENT_CLIENT_ID,
                lambda: GameEventDispatcher.with_callbacks(
                    (
                        PygameEvents.QUIT,
                        lambda: session_components.get(
                            SessionComponents.QUIT_GAME_EXECUTABLE
                        ).execute(),
                    ),
                    (
                        FrameEvents.OPEN,
                        lambda: session_components.get(SessionComponents.SCENE_CLOCK).tick(),
                    ),
                    (
                        FrameEvents.OPEN,
                        lambda: session_components.get(
                            SessionComponents.PYGAME_INPUT_CLIENT,
                        ).tick(),
                    ),
                    (
                        FrameEvents.OPEN,
                        lambda: session_components.get(
                            SessionComponents.INPUT_TOGGLES_CLIENT_ID,
                        ).tick(),
                    ),
                    (
                        FrameEvents.CLOSE,
                        lambda: session_components.get(
                            SessionComponents.SPRITE_CLIENT_ID
                        ).execute(),
                    ),
                    (
                        FrameEvents.CLOSE,
                        lambda: session_components.get(SessionComponents.TEXT_CLIENT_ID).execute(),
                    ),
                    (
                        FrameEvents.CLOSE,
                        lambda: session_components.get(
                            SessionComponents.DEBUG_HUD_CLIENT_ID
                        ).tick(),
                    ),
                    (
                        FrameEvents.CLOSE,
                        lambda: session_components.get(SessionComponents.WINDOW_CLIENT).commit(),
                    ),
                    (
                        SceneEvents.OPEN,
                        lambda: session_components.get(
                            SessionComponents.INDEX_OPEN_EXECUTABLE
                        ).execute(),
                    ),
                    (
                        SceneEvents.CLOSE,
                        lambda: session_components.get(
                            SessionComponents.INDEX_CLOSE_EXECUTABLE
                        ).execute(),
                    ),
                    # Append any external event callbacks
                    *session_components.get(SessionComponents.PLUGIN_EVENT_CALLBACKS),
                ),
            ),
            (
                SessionComponents.QUIT_GAME_EXECUTABLE,
                lambda: QuitGameExecutable(
                    stop=session_components.get(SessionComponents.FRAME_COLLECTION_CLIENT_ID)
                ),
            ),
            (
                SessionComponents.TEXT_CLIENT_ID,
                lambda: TextClient(
                    scene_objects=session_components.get(SessionComponents.SCENE_OBJECTS_CLIENT_ID),
                ),
            ),
            (
                SessionComponents.SPRITE_CLIENT_ID,
                lambda: SpriteClient(
                    scene_objects=session_components.get(SessionComponents.SCENE_OBJECTS_CLIENT_ID),
                ),
            ),
            (
                SessionComponents.POSITION_CLIENT_ID,
                lambda: PositionClient(
                    scene_objects=session_components.get(SessionComponents.SCENE_OBJECTS_CLIENT_ID),
                ),
            ),
            (
                SessionComponents.DEBUG_HUD_CLIENT_ID,
                lambda: DebugHudClient(
                    scene_objects=session_components.get(SessionComponents.SCENE_OBJECTS_CLIENT_ID),
                    clock=session_components.get(SessionComponents.SCENE_CLOCK),
                ),
            ),
            (SessionComponents.RESOURCE_CLIENT_ID, lambda: ResourceClient()),
            (
                SessionComponents.INPUT_TOGGLES_CLIENT_ID,
                lambda: InputTogglesClient(
                    input_client=session_components.get(SessionComponents.EVENT_CLIENT_ID),
                ),
            ),
            (
                CollisionComponent.CLIENT_ID,
                lambda: CollisionClient(
                    objects=session_components.get(SessionComponents.SCENE_OBJECTS_CLIENT_ID),
                    event_client=session_components.get(SessionComponents.EVENT_CLIENT_ID),
                ),
            ),
            (SessionComponents.SCENE_CLOCK, lambda: GameClock()),
        )

        session_components.get(SessionComponents.SESSION_CLIENT).execute()

    @lru_cache()
    def scene_components(self) -> GameClientContainer:
        return ContextualGameClientContainer(
            container=self.component_factory(),
            context=lambda: self.session_components().get(SessionComponents.SCENE_CONTEXT).get(),
        )

    @lru_cache()
    def session_components(self) -> GameClientContainer:
        return CachedGameClientContainer(
            container=self.component_factory(),
        )

    def component_factory(self) -> GameClientContainer:
        return self._factory()

    @lru_cache()
    def _factory(self) -> GameClientFactory:
        return GameClientFactory()


def seagulls_app() -> SeagullsApp:
    app = SeagullsApp()
    return app
