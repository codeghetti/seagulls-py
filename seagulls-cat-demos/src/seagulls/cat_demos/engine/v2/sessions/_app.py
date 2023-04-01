from typing import Tuple

from seagulls.cat_demos.engine.v2.components._component_registry import ContextualGameComponentRegistry, \
    GameComponentFactory, GameComponentId, \
    GameComponentProvider, \
    GameComponentRegistry, GameComponentType
from seagulls.cat_demos.engine.v2.components._entities import GameSceneId
from seagulls.cat_demos.engine.v2.components._object_components import ObjectComponentRegistry
from seagulls.cat_demos.engine.v2.components._scene_objects import SceneObjects
from seagulls.cat_demos.engine.v2.eventing._client import GameEventDispatcher
from seagulls.cat_demos.engine.v2.frames._client import FrameClient, FrameCollection
from seagulls.cat_demos.engine.v2.input._pygame import PygameEvents, PygameKeyboardInputPublisher
from seagulls.cat_demos.engine.v2.scenes._client import IScene, SceneClient, SceneComponent, SceneContext, \
    SceneProvider, SceneRegistry
from seagulls.cat_demos.engine.v2.window._window import WindowClient
from ._client import SessionClient
from ._executables import QuitGameExecutable
from ._index import CloseIndexScene, OpenIndexScene


class SessionComponents:
    EVENT_CLIENT = GameComponentId[GameEventDispatcher]("event-client")

    FRAME_COLLECTION = GameComponentId[FrameCollection]("frame-collection")

    INDEX_SCENE = GameComponentId[IScene]("index.scene")
    INDEX_OPEN_EXECUTABLE = GameComponentId[OpenIndexScene]("index-scene:open.executable")
    INDEX_CLOSE_EXECUTABLE = GameComponentId[OpenIndexScene]("index-scene:close.executable")

    OBJECT_COMPONENT_REGISTRY = GameComponentId[ObjectComponentRegistry]("object-component-registry")

    PYGAME_INPUT_CLIENT = GameComponentId[PygameKeyboardInputPublisher]("pygame-input-client")

    QUIT_GAME_EXECUTABLE = GameComponentId[QuitGameExecutable]("quit-game-executable")

    SCENE_CONTEXT = GameComponentId[SceneContext]("scene-context")
    SCENE_OBJECTS = GameComponentId[SceneObjects]("scene-objects")

    SESSION_CLIENT = GameComponentId[SessionClient]("session-client")
    SESSION_OBJECTS = GameComponentId[SceneObjects]("scene-objects")

    WINDOW_CLIENT = GameComponentId[WindowClient]("window-client")


class SeagullsApp:

    def run(
        self,
        *providers: Tuple[GameComponentId[GameComponentType], GameComponentProvider[GameComponentType]],
    ) -> None:
        component_factory = GameComponentFactory.with_providers(*providers)

        # Components built by this class are cached for the duration of the session
        session_components = GameComponentRegistry(
            factory=component_factory,
        )
        # Components built by this class are cached for the duration of the scene
        scene_components = ContextualGameComponentRegistry(
            factory=component_factory,
            context_provider=lambda: session_components.get(SessionComponents.SCENE_CONTEXT)(),
        )

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
                scene_objects=scene_components.get(SessionComponents.SESSION_OBJECTS),
                scene_event_client=scene_components.get(SessionComponents.EVENT_CLIENT),
                window_client=session_components.get(SessionComponents.WINDOW_CLIENT),
            )),
            (SessionComponents.INDEX_CLOSE_EXECUTABLE, lambda: CloseIndexScene()),
            (SessionComponents.PYGAME_INPUT_CLIENT, lambda: PygameKeyboardInputPublisher(
                event_dispatcher=component_factory.get(SessionComponents.EVENT_CLIENT),
            )),
            (SessionComponents.SESSION_OBJECTS, lambda: SceneObjects(
                object_component_registry=component_factory.get(
                    SessionComponents.OBJECT_COMPONENT_REGISTRY),
            )),
            (SessionComponents.WINDOW_CLIENT, lambda: WindowClient()),
            (SessionComponents.SCENE_CONTEXT, lambda: SceneContext()),
            (SessionComponents.OBJECT_COMPONENT_REGISTRY, lambda: ObjectComponentRegistry(
                registry=GameComponentFactory(),
            )),
            (SessionComponents.EVENT_CLIENT, lambda: GameEventDispatcher.with_callbacks(
                (PygameEvents.QUIT, session_components.get(SessionComponents.QUIT_GAME_EXECUTABLE)),
            )),
            (SessionComponents.QUIT_GAME_EXECUTABLE, lambda: QuitGameExecutable(
                stop=scene_components.get(SessionComponents.FRAME_COLLECTION)
            )),
        )

        session_components.get(SessionComponents.SESSION_CLIENT).execute()
