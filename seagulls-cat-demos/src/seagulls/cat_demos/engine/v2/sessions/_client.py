import logging
from abc import abstractmethod
from typing import Protocol, Tuple

from seagulls.cat_demos.engine import IExecutable
from seagulls.cat_demos.engine.v2._service_provider import provider
from seagulls.cat_demos.engine.v2.components._component_registry import ContextualGameComponentRegistry, \
    GameComponentFactory, GameComponentId, \
    GameComponentProvider, GameComponentRegistry, GameComponentType
from seagulls.cat_demos.engine.v2.components._entities import GameSceneId
from seagulls.cat_demos.engine.v2.components._game_objects import GameObjectId
from seagulls.cat_demos.engine.v2.components._object_components import ObjectComponentRegistry
from seagulls.cat_demos.engine.v2.components._scene_objects import SceneObjects
from seagulls.cat_demos.engine.v2.eventing._client import GameEventDispatcher
from seagulls.cat_demos.engine.v2.frames._client import FrameClient, FrameCollection
from seagulls.cat_demos.engine.v2.input._pygame import PygameKeyboardInputPublisher
from seagulls.cat_demos.engine.v2.scenes._client import (
    IProvideScenes,
    IScene,
    SceneClient,
    SceneComponent, SceneContext, SceneProvider,
    SceneRegistry,
)
from seagulls.cat_demos.engine.v2.window._window import WindowClient

logger = logging.getLogger(__name__)


class ISession(Protocol):

    @abstractmethod
    def open_session(self) -> None:
        pass

    @abstractmethod
    def run_session(self) -> None:
        pass

    @abstractmethod
    def close_session(self) -> None:
        pass


class SessionClient(ISession):

    _window_client: WindowClient
    _scene_client: IProvideScenes

    def __init__(
        self,
        window_client: WindowClient,
        scene_client: IProvideScenes,
    ) -> None:
        self._window_client = window_client
        self._scene_client = scene_client

    def open_session(self) -> None:
        self._window_client.open()
        self._scene_client.load_scene(GameSceneId("index"))

    def run_session(self) -> None:
        logger.warning(f"running session")
        for scene in self._scene_client.get_scenes():
            logger.warning(f"processing scene: {scene}")
            scene.open_scene()
            scene.run_scene()
            scene.close_scene()

    def close_session(self) -> None:
        self._window_client.close()


class Game:

    _config: GameComponentFactory

    def __init__(self, config: GameComponentFactory) -> None:
        self._config = config

    def run(self) -> None:
        session = self._config.get(GameComponentId[SessionClient]("session-client"))
        session.open_session()
        session.run_session()
        session.close_session()


class OpenIndexScene(IExecutable):

    _scene_objects: SceneObjects

    def __init__(self, scene_objects: SceneObjects) -> None:
        self._scene_objects = scene_objects

    def __call__(self) -> None:
        logger.warning("index scene open")
        self._scene_objects.add(GameObjectId("hello-world"))
        self._scene_objects.attach_component(
            GameObjectId("hello-world"),
            GameComponentId("text.scene-component"),
        )


class Seagulls:

    def create(
        self,
        *providers: Tuple[GameComponentId[GameComponentType], GameComponentProvider[GameComponentType]],
    ) -> Game:
        component_factory = GameComponentFactory.with_providers(*providers)

        # Components built by this class are cached for the duration of the session
        session_components = GameComponentRegistry(
            factory=component_factory,
        )
        # Components built by this class are cached for the duration of the scene
        scene_components = ContextualGameComponentRegistry(
            factory=component_factory,
            context_provider=lambda: session_components.get(GameComponentId[SceneContext]("scene-context"))(),
        )

        component_factory.set_missing(
            (GameComponentId[SessionClient]("session-client"), lambda: SessionClient(
                window_client=session_components.get(GameComponentId[WindowClient]("window-client")),
                scene_client=SceneClient(
                    scene_registry=SceneRegistry.with_providers(SceneProvider(
                        GameSceneId("index"),
                        lambda: component_factory.get(GameComponentId[IScene]("index.scene")),
                    )),
                    scene_context=session_components.get(GameComponentId[SceneContext]("scene-context")),
                ),
            )),
            (GameComponentId(name='index.scene'), lambda: SceneComponent(
                open_callback=session_components.get(GameComponentId[OpenIndexScene]("index-scene.executable")),
                close_callback=lambda: logger.warning("index scene close"),
                frame_collection=FrameCollection(
                    provider(lambda: FrameClient(
                        event_client=component_factory.get(GameComponentId[GameEventDispatcher]("event-client")),
                        window_client=session_components.get(GameComponentId[WindowClient]("window-client")),
                        pygame_input_client=component_factory.get(GameComponentId[PygameKeyboardInputPublisher]("pygame-input-client")),
                    ))
                ),
            )),
            (GameComponentId(name='event-client'), lambda: GameEventDispatcher.with_callbacks(
                # (FrameEvents.OPEN, config.get(GameComponentId[IExecutable]("frame.open"))),
                # (FrameEvents.EXECUTE, config.get(GameComponentId[IExecutable]("frame.execute"))),
                # (FrameEvents.CLOSE, config.get(GameComponentId[IExecutable]("frame.close"))),
            )),
            # (GameComponentId(name='frame.open'), lambda: open_frame),
            # (GameComponentId(name='frame.execute'), lambda: execute_frame),
            # (GameComponentId(name='frame.close'), lambda: close_frame),
            (GameComponentId(name="index-scene.executable"), lambda: OpenIndexScene(
                scene_objects=scene_components.get(GameComponentId[SceneObjects]("scene-objects")),
            )),
            (GameComponentId(name='pygame-input-client'), lambda: PygameKeyboardInputPublisher(
                event_dispatcher=component_factory.get(GameComponentId[GameEventDispatcher]("event-client")),
            )),
            (GameComponentId(name='scene-objects'), lambda: SceneObjects(
                object_component_registry=component_factory.get(
                    GameComponentId[ObjectComponentRegistry]("object-component-registry")),
            )),
            (GameComponentId(name='window-client'), lambda: WindowClient()),
            (GameComponentId(name='scene-context'), lambda: SceneContext()),
            (GameComponentId(name='object-component-registry'), lambda: ObjectComponentRegistry(
                registry=GameComponentFactory(),
            )),
        )

        return Game(component_factory)
