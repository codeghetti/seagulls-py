from functools import lru_cache

from seagulls.seagulls_cli import SeagullsCliApplication

from seagulls.cat_demos.engine.v2.components._entities import GameSceneId
from seagulls.cat_demos.engine.v2.components._object_components import ObjectComponentRegistry
from seagulls.cat_demos.engine.v2.components._scene_objects import SceneObjects
from seagulls.cat_demos.engine.v2.components._service_provider import ServiceProvider
from seagulls.cat_demos.engine.v2.debugging._component import DebugComponent, DebugComponentId
from seagulls.cat_demos.engine.v2.eventing._client import GameEventDispatcher
from seagulls.cat_demos.engine.v2.frames._client import FrameClient, FrameCollection, FrameEvents
from seagulls.cat_demos.engine.v2.input._pygame import PygameKeyboardInputPublisher
from seagulls.cat_demos.engine.v2.position._position_component import PositionComponent, PositionComponentId, \
    PositionObjectComponentId
from seagulls.cat_demos.engine.v2.scenes._client import SceneClient, SceneComponent, SceneProvider, SceneRegistry
from seagulls.cat_demos.engine.v2.sessions._client import SessionClient
from seagulls.cat_demos.engine.v2.window._window import WindowClient
from ._cli_command import GameCliCommand
from ._cli_plugin import CatDemosCliPlugin
from ._main_menu import CloseMainMenuScene, OpenMainMenuScene
from ..engine.v2.components._component_registry import GameComponentFactory


class CatDemosDiContainer:
    _application: SeagullsCliApplication

    def __init__(self, application: SeagullsCliApplication):
        self._application = application

    @lru_cache()
    def plugin(self) -> CatDemosCliPlugin:
        return CatDemosCliPlugin(
            application=self._application,
            command=self._command(),
        )

    @lru_cache()
    def _command(self) -> GameCliCommand:
        return GameCliCommand(
            session_client=self._session_client(),
            scene_client=self._scene_client(),
            frames_provider=self._frames_provider(),
            event_dispatcher=self._event_dispatcher(),
        )

    @lru_cache()
    def _session_client(self) -> SessionClient:
        return SessionClient(
            window_client=self._window_client(),
            scene_client=self._scene_client(),
        )

    @lru_cache()
    def _scene_client(self) -> SceneClient:
        return SceneClient(self._scene_registry())

    @lru_cache()
    def _scene_registry(self) -> SceneRegistry:
        return SceneRegistry.with_providers(
            SceneProvider(
                scene_id=GameSceneId("main-menu"),
                provider=ServiceProvider(
                    lambda: SceneComponent(
                        open_callback=OpenMainMenuScene(
                            scene_components=self._scene_components(),
                            scene_objects=self._scene_objects(),
                        ),
                        close_callback=CloseMainMenuScene(),
                        frame_collection=self._frames_provider(),
                    ),
                ),
            ),
        )

    @lru_cache()
    def _frames_provider(self) -> FrameCollection:
        return FrameCollection(frame_factory=self._frame_client_factory())

    @lru_cache()
    def _frame_client_factory(self) -> ServiceProvider[FrameClient]:
        return ServiceProvider[FrameClient](lambda: FrameClient(event_client=self._event_dispatcher()))

    @lru_cache()
    def _event_dispatcher(self) -> GameEventDispatcher:
        def open_frame() -> None:
            self._pygame_input().tick()

        def execute_frame() -> None:
            self._window_client().get_surface().fill((20, 20, 20))
            self._debug_component().tick()

        def close_frame() -> None:
            self._window_client().commit()

        return GameEventDispatcher.with_callbacks(
            (FrameEvents.OPEN, open_frame),
            (FrameEvents.EXECUTE, execute_frame),
            (FrameEvents.CLOSE, close_frame),
        )

    @lru_cache()
    def _pygame_input(self) -> PygameKeyboardInputPublisher:
        return PygameKeyboardInputPublisher(
            event_dispatcher=self._event_dispatcher(),
        )

    @lru_cache()
    def _scene_objects(self) -> SceneObjects:
        return SceneObjects(self._object_component_registry())

    @lru_cache()
    def _object_component_registry(self) -> ObjectComponentRegistry:
        registry = ObjectComponentRegistry(self._component_registry())
        registry.register(PositionObjectComponentId, PositionComponentId)
        return registry

    @lru_cache()
    def _component_registry(self) -> GameComponentFactory:
        return GameComponentFactory.with_providers(
            (PositionComponentId, self._position_component),
            (DebugComponentId, self._debug_component),
        )

    @lru_cache()
    def _debug_component(self) -> DebugComponent:
        return DebugComponent(window_client=self._window_client())

    @lru_cache()
    def _position_component(self) -> PositionComponent:
        return PositionComponent()

    @lru_cache()
    def _window_client(self) -> WindowClient:
        return WindowClient()
