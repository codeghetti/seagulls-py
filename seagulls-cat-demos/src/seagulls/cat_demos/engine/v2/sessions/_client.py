import logging
from abc import abstractmethod
from typing import Protocol, Tuple

import pygame

from seagulls.cat_demos.engine import IExecutable
from seagulls.cat_demos.engine.v2.components._component_registry import ContextualGameComponentRegistry, \
    GameComponentFactory, GameComponentId, \
    GameComponentProvider, GameComponentRegistry, GameComponentType
from seagulls.cat_demos.engine.v2.components._entities import GameSceneId
from seagulls.cat_demos.engine.v2.components._game_objects import GameObjectId
from seagulls.cat_demos.engine.v2.components._object_components import ObjectComponentRegistry
from seagulls.cat_demos.engine.v2.components._scene_objects import SceneObjects
from seagulls.cat_demos.engine.v2.eventing._client import GameEventDispatcher
from seagulls.cat_demos.engine.v2.frames._client import FrameClient, FrameCollection, FrameEvents, IStopScenes
from seagulls.cat_demos.engine.v2.input._pygame import PygameEvents, PygameKeyboardInputPublisher
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
    def run(self) -> None:
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

    def run(self) -> None:
        self._window_client.open()
        self._scene_client.load_scene(GameSceneId("index"))

        for scene in self._scene_client.get_scenes():
            scene.open_scene()
            scene.run_scene()
            scene.close_scene()

        self._window_client.close()


class OpenIndexScene(IExecutable):

    _scene_objects: SceneObjects
    _scene_event_client: GameEventDispatcher
    _window_client: WindowClient

    def __init__(
        self,
        scene_objects: SceneObjects,
        scene_event_client: GameEventDispatcher,
        window_client: WindowClient,
    ) -> None:
        self._scene_objects = scene_objects
        self._scene_event_client = scene_event_client
        self._window_client = window_client

    def __call__(self) -> None:
        logger.debug("index scene open")
        self._scene_event_client.register(FrameEvents.EXECUTE, self._tick)
        self._scene_objects.add(GameObjectId("hello-world"))
        # self._scene_objects.attach_component(
        #     GameObjectId("hello-world"),
        #     GameComponentId("text.scene-component"),
        # )

    def _tick(self) -> None:
        f = pygame.font.SysFont("monospace", 75)
        text = f.render("Hello, World!", True, (0, 0, 0))
        surface = self._window_client.get_surface()
        surface.fill((20, 120, 20))
        surface.blit(text, (20, 20))


class CloseIndexScene(IExecutable):

    def __call__(self) -> None:
        print("Goodbye!")


class QuitGameExecutable(IExecutable):

    _stop: IStopScenes

    def __init__(self, stop: IStopScenes) -> None:
        self._stop = stop

    def __call__(self) -> None:
        self._stop.stop()


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
                open_callback=session_components.get(GameComponentId[OpenIndexScene]("index-scene:open.executable")),
                close_callback=session_components.get(GameComponentId[OpenIndexScene]("index-scene:close.executable")),
                frame_collection=scene_components.get(GameComponentId[FrameCollection]("frame-collection")),
            )),
            (GameComponentId(name="frame-collection"), lambda: FrameCollection(lambda: FrameClient(
                event_client=scene_components.get(GameComponentId[GameEventDispatcher]("event-client")),
                window_client=session_components.get(GameComponentId[WindowClient]("window-client")),
                pygame_input_client=component_factory.get(
                    GameComponentId[PygameKeyboardInputPublisher]("pygame-input-client"),
                ),
            ))),
            (GameComponentId(name="index-scene:open.executable"), lambda: OpenIndexScene(
                scene_objects=scene_components.get(GameComponentId[SceneObjects]("scene-objects")),
                scene_event_client=scene_components.get(GameComponentId[GameEventDispatcher]("event-client")),
                window_client=session_components.get(GameComponentId[WindowClient]("window-client")),
            )),
            (GameComponentId(name="index-scene:close.executable"), lambda: CloseIndexScene()),
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
            (GameComponentId(name='event-client'), lambda: GameEventDispatcher.with_callbacks(
                (PygameEvents.QUIT, session_components.get(GameComponentId[QuitGameExecutable]("quit-game-executable"))),
            )),
            (GameComponentId(name='quit-game-executable'), lambda: QuitGameExecutable(
                stop=scene_components.get(GameComponentId[FrameCollection]("frame-collection"))
            )),
        )

        session_components.get(GameComponentId[SessionClient]("session-client")).run()
