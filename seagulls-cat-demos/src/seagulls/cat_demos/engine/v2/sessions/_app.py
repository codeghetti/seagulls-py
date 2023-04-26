from functools import lru_cache
from typing import Any, Callable, NamedTuple, Tuple, TypeAlias

from seagulls.cat_demos.engine.v2.collisions._collider_component import (
    ColliderPrefabIds,
    CollisionPrefab
)
from seagulls.cat_demos.engine.v2.components._component_containers import (
    CachedGameComponentContainer,
    ContextualGameComponentContainer,
    FilteredGameComponentRegistry,
    GameComponentContainer,
    GameComponentFactory,
    GameComponentId,
    GameComponentProvider,
    GameComponentType
)
from seagulls.cat_demos.engine.v2.components._entities import GameSceneId
from seagulls.cat_demos.engine.v2.components._prefabs import (
    GameObjectConfig,
    GameObjectPrefab,
    PrefabClient
)
from seagulls.cat_demos.engine.v2.components._scene_objects import SceneObjects
from seagulls.cat_demos.engine.v2.eventing._event_dispatcher import (
    GameEventDispatcher,
    GameEventId
)
from seagulls.cat_demos.engine.v2.frames._frames_client import (
    FrameClient,
    FrameCollection,
    FrameEvents
)
from seagulls.cat_demos.engine.v2.input._game_clock import GameClock
from seagulls.cat_demos.engine.v2.input._input_toggles import (
    InputTogglesClient
)
from seagulls.cat_demos.engine.v2.input._pygame import (
    PygameEvents,
    PygameKeyboardInputPublisher
)
from seagulls.cat_demos.engine.v2.position._position_prefab import (
    PositionPrefab
)
from seagulls.cat_demos.engine.v2.resources._resources_client import (
    ResourceClient
)
from seagulls.cat_demos.engine.v2.scenes._client import (
    IScene,
    SceneClient,
    SceneComponent,
    SceneContext,
    SceneEvents,
    SceneProvider,
    SceneRegistry
)
from seagulls.cat_demos.engine.v2.sprites._sprite_component import (
    SpriteComponent,
    SpriteSource
)
from seagulls.cat_demos.engine.v2.sprites._sprite_prefab import SpritePrefab
from seagulls.cat_demos.engine.v2.text._text_component import TextComponent
from seagulls.cat_demos.engine.v2.text._text_prefab import TextPrefab
from seagulls.cat_demos.engine.v2.window._window import WindowClient

from ..debugging._debug_hud_prefab import DebugHud, DebugHudPrefab
from ._client import SessionClient
from ._executables import QuitGameExecutable
from ._index import CloseIndexScene, OpenIndexScene

GameEventCallback: TypeAlias = Tuple[GameEventId[Any], Callable[[], None]]


class SessionComponents:
    EVENT_CLIENT = GameComponentId[GameEventDispatcher]("event-client")
    INPUT_TOGGLES_CLIENT = GameComponentId[InputTogglesClient]("input-toggles-client")
    SCENE_OBJECTS = GameComponentId[SceneObjects]("scene-objects")
    PREFAB_CLIENT = GameComponentId[PrefabClient]("prefab-client")
    TEXT_COMPONENT = GameComponentId[TextComponent]("text-component")
    TEXT_PREFAB = GameComponentId[TextPrefab]("prefab.text-component")
    POSITION_PREFAB = GameComponentId[PositionPrefab]("prefab.position-component")
    RESOURCE_CLIENT = GameComponentId[ResourceClient]("resource-client")
    SPRITE_COMPONENT = GameComponentId[SpriteComponent]("sprite-component")
    SPRITE_PREFAB = GameComponentId[SpritePrefab]("prefab.sprite-component")
    OBJECT_PREFAB = GameComponentId[GameObjectConfig]("prefab.game-object")
    OBJECT_COMPONENT = GameComponentId[GameObjectPrefab]("prefab.game-object")
    DEBUG_HUD_PREFAB = GameComponentId[DebugHud]("prefab.debug-hud")
    DEBUG_HUD_COMPONENT = GameComponentId[DebugHudPrefab]("prefab.debug-hud")
    OBJECT_COMPONENT_CONTAINER = GameComponentId[GameComponentContainer](
        "object-component-registry",
    )
    FRAME_COLLECTION = GameComponentId[FrameCollection]("frame-collection")
    INDEX_SCENE = GameComponentId[IScene]("index.scene")
    INDEX_OPEN_EXECUTABLE = GameComponentId[OpenIndexScene](
        "index-scene:open.executable",
    )
    INDEX_CLOSE_EXECUTABLE = GameComponentId[CloseIndexScene](
        "index-scene:close.executable",
    )
    PYGAME_INPUT_CLIENT = GameComponentId[PygameKeyboardInputPublisher](
        "pygame-input-client",
    )
    QUIT_GAME_EXECUTABLE = GameComponentId[QuitGameExecutable]("quit-game-executable")
    SCENE_CONTEXT = GameComponentId[SceneContext]("scene-context")
    SESSION_CLIENT = GameComponentId[SessionClient]("session-client")
    WINDOW_CLIENT = GameComponentId[WindowClient]("window-client")
    SCENE_CLOCK = GameComponentId[GameClock]("scene-clock")

    PLUGIN_EVENT_CALLBACKS = GameComponentId[Tuple[GameEventCallback, ...]](
        "plugin:event-callbacks",
    )
    PLUGIN_SPRITE_SOURCES = GameComponentId[Tuple[SpriteSource, ...]]("sprite-sources")


class SeagullsAppProvider(NamedTuple):
    id: GameComponentId[Any]
    provider: GameComponentProvider[Any]


class SeagullsApp:
    def run(
        self,
        *providers: Tuple[
            GameComponentId[GameComponentType], GameComponentProvider[GameComponentType]
        ],
    ) -> None:
        component_factory = self._factory()
        # Components built by this class are cached for the duration of the session
        session_components = self.session_components()
        # Components built by this class are cached for the duration of the scene
        scene_components = self.scene_components()

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
                    scene_client=SceneClient(
                        scene_registry=SceneRegistry.with_providers(
                            SceneProvider(
                                GameSceneId("index"),
                                lambda: component_factory.get(
                                    SessionComponents.INDEX_SCENE
                                ),
                            )
                        ),
                        scene_context=session_components.get(
                            SessionComponents.SCENE_CONTEXT
                        ),
                    ),
                    first_scene=lambda: GameSceneId("index"),
                ),
            ),
            (
                SessionComponents.INDEX_SCENE,
                lambda: SceneComponent(
                    frame_collection=scene_components.get(
                        SessionComponents.FRAME_COLLECTION
                    ),
                    event_client=scene_components.get(SessionComponents.EVENT_CLIENT),
                    scene_context=session_components.get(
                        SessionComponents.SCENE_CONTEXT
                    ),
                ),
            ),
            (
                SessionComponents.FRAME_COLLECTION,
                lambda: FrameCollection(
                    lambda: FrameClient(
                        event_client=scene_components.get(
                            SessionComponents.EVENT_CLIENT
                        ),
                        window_client=session_components.get(
                            SessionComponents.WINDOW_CLIENT
                        ),
                        pygame_input_client=scene_components.get(
                            SessionComponents.PYGAME_INPUT_CLIENT
                        ),
                        toggles=scene_components.get(
                            SessionComponents.INPUT_TOGGLES_CLIENT
                        ),
                    )
                ),
            ),
            (SessionComponents.INDEX_OPEN_EXECUTABLE, lambda: OpenIndexScene()),
            (SessionComponents.INDEX_CLOSE_EXECUTABLE, lambda: CloseIndexScene()),
            (
                SessionComponents.PYGAME_INPUT_CLIENT,
                lambda: PygameKeyboardInputPublisher(
                    event_dispatcher=scene_components.get(
                        SessionComponents.EVENT_CLIENT
                    ),
                ),
            ),
            (
                SessionComponents.TEXT_COMPONENT,
                lambda: TextComponent(
                    objects=scene_components.get(SessionComponents.SCENE_OBJECTS),
                    window_client=session_components.get(
                        SessionComponents.WINDOW_CLIENT
                    ),
                ),
            ),
            (
                SessionComponents.SPRITE_COMPONENT,
                lambda: SpriteComponent(
                    objects=scene_components.get(SessionComponents.SCENE_OBJECTS),
                    window_client=session_components.get(
                        SessionComponents.WINDOW_CLIENT
                    ),
                    resource_client=session_components.get(
                        SessionComponents.RESOURCE_CLIENT
                    ),
                    sprite_sources=session_components.get(
                        SessionComponents.PLUGIN_SPRITE_SOURCES
                    ),
                ),
            ),
            (
                SessionComponents.SCENE_OBJECTS,
                lambda: SceneObjects(
                    container=component_factory.get(
                        SessionComponents.OBJECT_COMPONENT_CONTAINER
                    ),
                ),
            ),
            (SessionComponents.WINDOW_CLIENT, lambda: WindowClient()),
            (SessionComponents.SCENE_CONTEXT, lambda: SceneContext()),
            # TODO: add a filter to this container
            (
                SessionComponents.OBJECT_COMPONENT_CONTAINER,
                lambda: FilteredGameComponentRegistry(
                    container=scene_components,
                    context=lambda: [
                        GameComponentId("object-position"),
                    ],
                ),
            ),
            (
                SessionComponents.EVENT_CLIENT,
                lambda: GameEventDispatcher.with_callbacks(
                    (
                        PygameEvents.QUIT,
                        lambda: session_components.get(
                            SessionComponents.QUIT_GAME_EXECUTABLE
                        )(),
                    ),
                    (
                        FrameEvents.OPEN,
                        lambda: scene_components.get(
                            SessionComponents.SCENE_CLOCK
                        ).tick(),
                    ),
                    (
                        FrameEvents.CLOSE,
                        lambda: scene_components.get(
                            SessionComponents.SPRITE_COMPONENT
                        )(),
                    ),
                    (
                        FrameEvents.CLOSE,
                        lambda: scene_components.get(
                            SessionComponents.TEXT_COMPONENT
                        )(),
                    ),
                    (
                        FrameEvents.CLOSE,
                        lambda: scene_components.get(
                            SessionComponents.DEBUG_HUD_COMPONENT
                        ).tick(),
                    ),
                    (
                        SceneEvents.OPEN,
                        lambda: scene_components.get(
                            SessionComponents.INDEX_OPEN_EXECUTABLE
                        )(),
                    ),
                    (
                        SceneEvents.CLOSE,
                        lambda: scene_components.get(
                            SessionComponents.INDEX_CLOSE_EXECUTABLE
                        )(),
                    ),
                    # Append any external event callbacks
                    *session_components.get(SessionComponents.PLUGIN_EVENT_CALLBACKS),
                ),
            ),
            (
                SessionComponents.QUIT_GAME_EXECUTABLE,
                lambda: QuitGameExecutable(
                    stop=scene_components.get(SessionComponents.FRAME_COLLECTION)
                ),
            ),
            (
                SessionComponents.PREFAB_CLIENT,
                lambda: PrefabClient(container=scene_components),
            ),
            (
                SessionComponents.TEXT_PREFAB,
                lambda: TextPrefab(
                    scene_objects=scene_components.get(SessionComponents.SCENE_OBJECTS),
                ),
            ),
            (
                SessionComponents.SPRITE_PREFAB,
                lambda: SpritePrefab(
                    scene_objects=scene_components.get(SessionComponents.SCENE_OBJECTS),
                ),
            ),
            (
                SessionComponents.OBJECT_PREFAB,
                lambda: GameObjectPrefab(
                    scene_objects=scene_components.get(SessionComponents.SCENE_OBJECTS),
                ),
            ),
            (
                SessionComponents.POSITION_PREFAB,
                lambda: PositionPrefab(
                    scene_objects=scene_components.get(SessionComponents.SCENE_OBJECTS),
                ),
            ),
            (
                SessionComponents.DEBUG_HUD_PREFAB,
                lambda: DebugHudPrefab(
                    scene_objects=scene_components.get(SessionComponents.SCENE_OBJECTS),
                    object_prefab=scene_components.get(
                        SessionComponents.OBJECT_COMPONENT
                    ),
                    clock=scene_components.get(SessionComponents.SCENE_CLOCK),
                ),
            ),
            (SessionComponents.RESOURCE_CLIENT, lambda: ResourceClient()),
            (
                SessionComponents.INPUT_TOGGLES_CLIENT,
                lambda: InputTogglesClient(
                    input_client=scene_components.get(SessionComponents.EVENT_CLIENT),
                ),
            ),
            (
                ColliderPrefabIds.PREFAB_COMPONENT,
                lambda: CollisionPrefab(
                    objects=scene_components.get(SessionComponents.SCENE_OBJECTS),
                    event_client=scene_components.get(SessionComponents.EVENT_CLIENT),
                ),
            ),
            (SessionComponents.SCENE_CLOCK, lambda: GameClock()),
        )

        session_components.get(SessionComponents.SESSION_CLIENT).execute()

    @lru_cache()
    def scene_components(self) -> GameComponentContainer:
        return ContextualGameComponentContainer(
            container=self.component_factory(),
            context=lambda: self.session_components().get(
                SessionComponents.SCENE_CONTEXT
            )(),
        )

    @lru_cache()
    def session_components(self) -> GameComponentContainer:
        return CachedGameComponentContainer(
            factory=self.component_factory(),
        )

    def component_factory(self) -> GameComponentContainer:
        return self._factory()

    @lru_cache()
    def _factory(self) -> GameComponentFactory:
        return GameComponentFactory()
