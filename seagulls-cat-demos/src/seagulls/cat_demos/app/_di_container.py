from functools import lru_cache

from seagulls.cat_demos.engine.v2._service_provider import ServiceProvider
from seagulls.cat_demos.engine.v2.components._entities import GameSceneId
from seagulls.cat_demos.engine.v2.frames._client import FrameClient, FrameCollection
from seagulls.cat_demos.engine.v2.input._eventing import EventPayloadType, InputEvent
from seagulls.cat_demos.engine.v2.input._input_client import GameInputClient
from seagulls.cat_demos.engine.v2.scenes._client import SceneClient, SceneComponent, SceneProvider, SceneRegistry
from seagulls.cat_demos.engine.v2.sessions._client import SessionClient
from seagulls.cat_demos.engine.v2.window._window import WindowClient
from seagulls.seagulls_cli import SeagullsCliApplication
from ._cli_command import GameCliCommand
from ._cli_plugin import CatDemosCliPlugin
from ._main_menu import CloseMainMenuScene, OpenMainMenuScene
from ..engine.v2.components._game_components import GameComponentRegistry, ObjectComponentRegistry
from ..engine.v2.components._scene_objects import SceneObjects
from ..engine.v2.position._position_component import PositionComponent, PositionComponentId, PositionObjectComponentId


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
            scene_collection=self._scene_client(),
        )

    @lru_cache()
    def _session_client(self) -> SessionClient:
        return SessionClient(
            window_client=self._window_client(),
            scenes_collection=self._scene_client(),
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
                        open_callback=OpenMainMenuScene(self._scene_objects()),
                        close_callback=CloseMainMenuScene(),
                        frame_collection=self._frame_collection(),
                    ),
                ),
            ),
        )

    @lru_cache()
    def _frame_collection(self) -> FrameCollection:
        return FrameCollection(frame_factory=self._frame_client_factory())

    @lru_cache()
    def _frame_client_factory(self) -> ServiceProvider[FrameClient]:
        return ServiceProvider[FrameClient](lambda: FrameClient(
            window_client=self._window_client(),
        ))

    @lru_cache()
    def _game_input_client(self) -> GameInputClient:
        return GameInputClient(handlers=tuple([
            self._on_input_v2,
        ]))

    @lru_cache()
    def _window_client(self) -> WindowClient:
        return WindowClient()

    def _on_input_v2(self, event: InputEvent[EventPayloadType], payload: EventPayloadType) -> None:
        # self._input_v2_routing.route(event, payload)
        # self._event_dispatcher.trigger(event, payload)
        pass

    @lru_cache()
    def _scene_objects(self) -> SceneObjects:
        return SceneObjects(self._object_component_registry())

    @lru_cache()
    def _object_component_registry(self) -> ObjectComponentRegistry:
        registry = ObjectComponentRegistry(self._component_registry())
        registry.register(PositionObjectComponentId, PositionComponentId)
        return registry

    @lru_cache()
    def _component_registry(self) -> GameComponentRegistry:
        registry = GameComponentRegistry()
        registry.register(PositionComponentId, self._position_component)
        return registry

    @lru_cache()
    def _position_component(self) -> PositionComponent:
        return PositionComponent()
