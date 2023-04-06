from functools import lru_cache
from typing import Any, NamedTuple, Tuple

from seagulls.cat_demos.engine.v2.components._component_containers import ContextualGameComponentRegistry, \
    FilteredGameComponentRegistry, GameComponentContainer, GameComponentFactory, GameComponentId, \
    GameComponentProvider, \
    GameComponentRegistry, GameComponentType
from seagulls.cat_demos.engine.v2.components._entities import GameSceneId
from seagulls.cat_demos.engine.v2.components._scene_objects import SceneObjects
from seagulls.cat_demos.engine.v2.eventing._client import GameEventDispatcher
from seagulls.cat_demos.engine.v2.frames._client import FrameClient, FrameCollection, FrameEvents
from seagulls.cat_demos.engine.v2.input._pygame import PygameEvents, PygameKeyboardInputPublisher
from seagulls.cat_demos.engine.v2.scenes._client import IScene, SceneClient, SceneComponent, SceneContext, \
    SceneProvider, SceneRegistry
from seagulls.cat_demos.engine.v2.window._window import WindowClient
from ._client import SessionClient
from ._executables import QuitGameExecutable
from ._index import CloseIndexScene, OpenIndexScene
from ..components._prefabs import PrefabClient
from ..position._prefab import PositionPrefab
from ..sprites._component import SpriteComponent
from ..sprites._sprite_prefab import SpritePrefab
from ..text._component import TextComponent
from ..text._prefab import TextPrefab


class SessionComponents:
    EVENT_CLIENT = GameComponentId[GameEventDispatcher]("event-client")

    FRAME_COLLECTION = GameComponentId[FrameCollection]("frame-collection")

    INDEX_SCENE = GameComponentId[IScene]("index.scene")
    INDEX_OPEN_EXECUTABLE = GameComponentId[OpenIndexScene]("index-scene:open.executable")
    INDEX_CLOSE_EXECUTABLE = GameComponentId[OpenIndexScene]("index-scene:close.executable")

    OBJECT_COMPONENT_CONTAINER = GameComponentId[GameComponentContainer]("object-component-registry")

    PYGAME_INPUT_CLIENT = GameComponentId[PygameKeyboardInputPublisher]("pygame-input-client")

    QUIT_GAME_EXECUTABLE = GameComponentId[QuitGameExecutable]("quit-game-executable")

    SCENE_CONTEXT = GameComponentId[SceneContext]("scene-context")
    SCENE_OBJECTS = GameComponentId[SceneObjects]("scene-objects")

    SESSION_CLIENT = GameComponentId[SessionClient]("session-client")

    WINDOW_CLIENT = GameComponentId[WindowClient]("window-client")
    PREFAB_CLIENT = GameComponentId[PrefabClient]("prefab-client")

    TEXT_COMPONENT = GameComponentId[TextComponent]("text-component")
    TEXT_PREFAB = GameComponentId[TextPrefab]("prefab.text-component")
    POSITION_PREFAB = GameComponentId[PositionPrefab]("prefab.position-component")
    SPRITE_COMPONENT = GameComponentId[SpriteComponent]("sprite-component")
    SPRITE_PREFAB = GameComponentId[SpritePrefab]("prefab.sprite-component")


class SeagullsAppProvider(NamedTuple):
    id: GameComponentId[Any]
    provider: GameComponentProvider[Any]


class SeagullsApp:

    def run(
        self,
        *providers: Tuple[GameComponentId[GameComponentType], GameComponentProvider[GameComponentType]],
    ) -> None:
        component_factory = self._factory()
        # Components built by this class are cached for the duration of the session
        session_components = self.session_components()
        # Components built by this class are cached for the duration of the scene
        scene_components = self.scene_components()

        for p in providers:
            component_factory.set(p[0], p[1])

        component_factory.set_missing(
            (SessionComponents.SESSION_CLIENT, lambda: SessionClient(
                window_client=session_components.get(SessionComponents.WINDOW_CLIENT),
                scene_client=SceneClient(
                    scene_registry=SceneRegistry.with_providers(SceneProvider(
                        GameSceneId("index"),
                        lambda: component_factory.get(SessionComponents.INDEX_SCENE),
                    )),
                    scene_context=session_components.get(SessionComponents.SCENE_CONTEXT),
                ),
                first_scene=lambda: GameSceneId("index"),
            )),
            (SessionComponents.INDEX_SCENE, lambda: SceneComponent(
                open_callback=session_components.get(SessionComponents.INDEX_OPEN_EXECUTABLE),
                close_callback=session_components.get(SessionComponents.INDEX_CLOSE_EXECUTABLE),
                frame_collection=scene_components.get(SessionComponents.FRAME_COLLECTION),
            )),
            (SessionComponents.FRAME_COLLECTION, lambda: FrameCollection(lambda: FrameClient(
                event_client=scene_components.get(SessionComponents.EVENT_CLIENT),
                window_client=session_components.get(SessionComponents.WINDOW_CLIENT),
                pygame_input_client=component_factory.get(SessionComponents.PYGAME_INPUT_CLIENT),
            ))),
            (SessionComponents.INDEX_OPEN_EXECUTABLE, lambda: OpenIndexScene(
                scene_objects=scene_components.get(SessionComponents.SCENE_OBJECTS),
                scene_event_client=scene_components.get(SessionComponents.EVENT_CLIENT),
                window_client=session_components.get(SessionComponents.WINDOW_CLIENT),
            )),
            (SessionComponents.INDEX_CLOSE_EXECUTABLE, lambda: CloseIndexScene()),
            (SessionComponents.PYGAME_INPUT_CLIENT, lambda: PygameKeyboardInputPublisher(
                event_dispatcher=component_factory.get(SessionComponents.EVENT_CLIENT),
            )),
            (SessionComponents.TEXT_COMPONENT, lambda: TextComponent(
                objects=scene_components.get(SessionComponents.SCENE_OBJECTS),
                window_client=session_components.get(SessionComponents.WINDOW_CLIENT),
            )),
            (SessionComponents.SPRITE_COMPONENT, lambda: SpriteComponent(
                objects=scene_components.get(SessionComponents.SCENE_OBJECTS),
                container=session_components,
                window_client=session_components.get(SessionComponents.WINDOW_CLIENT),
            )),
            (SessionComponents.SCENE_OBJECTS, lambda: SceneObjects(
                container=component_factory.get(
                    SessionComponents.OBJECT_COMPONENT_CONTAINER),
            )),
            (SessionComponents.WINDOW_CLIENT, lambda: WindowClient()),
            (SessionComponents.SCENE_CONTEXT, lambda: SceneContext()),
            # TODO: add a filter to this container
            (SessionComponents.OBJECT_COMPONENT_CONTAINER, lambda: FilteredGameComponentRegistry(
                container=scene_components,
                context=lambda: [
                    GameComponentId("object-position"),
                ],
            )),
            (SessionComponents.EVENT_CLIENT, lambda: GameEventDispatcher.with_callbacks(
                (PygameEvents.QUIT, session_components.get(SessionComponents.QUIT_GAME_EXECUTABLE)),
                (FrameEvents.CLOSE, scene_components.get(SessionComponents.TEXT_COMPONENT).render_objects),
                (FrameEvents.CLOSE, scene_components.get(SessionComponents.SPRITE_COMPONENT).render_objects),
            )),
            (SessionComponents.QUIT_GAME_EXECUTABLE, lambda: QuitGameExecutable(
                stop=scene_components.get(SessionComponents.FRAME_COLLECTION)
            )),
            (SessionComponents.PREFAB_CLIENT, lambda: PrefabClient(container=scene_components)),
            (SessionComponents.TEXT_PREFAB, lambda: TextPrefab(
                scene_objects=scene_components.get(SessionComponents.SCENE_OBJECTS),
            )),
            (SessionComponents.SPRITE_PREFAB, lambda: SpritePrefab(
                scene_objects=scene_components.get(SessionComponents.SCENE_OBJECTS),
            )),
            (SessionComponents.POSITION_PREFAB, lambda: PositionPrefab(
                scene_objects=scene_components.get(SessionComponents.SCENE_OBJECTS),
            )),
        )

        session_components.get(SessionComponents.SESSION_CLIENT).execute()

    @lru_cache()
    def scene_components(self) -> GameComponentContainer:
        return ContextualGameComponentRegistry(
            container=self.component_factory(),
            context=lambda: self.session_components().get(SessionComponents.SCENE_CONTEXT)(),
        )

    @lru_cache()
    def session_components(self) -> GameComponentContainer:
        return GameComponentRegistry(
            factory=self.component_factory(),
        )

    def component_factory(self) -> GameComponentContainer:
        return self._factory()

    @lru_cache()
    def _factory(self) -> GameComponentFactory:
        return GameComponentFactory()
