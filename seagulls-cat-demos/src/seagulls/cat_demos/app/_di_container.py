from typing import Iterable

from functools import lru_cache

from seagulls.seagulls_cli import SeagullsCliApplication

from ._cli_command import GameCliCommand
from ._cli_plugin import CatDemosCliPlugin
from seagulls.cat_demos.engine.v2._input_client import (
    EventPayloadType,
    InputEvent,
)
from seagulls.cat_demos.engine.v2._interactors import IFrame, \
    IProvideFrames, \
    IProvideScenes, IScene
from seagulls.cat_demos.engine.v2.window._window import WindowClient
from ..engine.v2._service_provider import ServiceProvider
from ..engine.v2.components._identity import GameSceneId
from ..engine.v2.frames._client import FrameClient, FrameCollection
from ..engine.v2.scenes._client import SceneClient, SceneCollection, SceneProvider
from ..engine.v2.sessions._client import SessionClient


class StubbyScenes(IProvideScenes):

    def items(self) -> Iterable[IScene]:
        return []


class StubbyFrames(IProvideFrames):

    def items(self) -> Iterable[IFrame]:
        return []


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
            scene_collection=self._scene_collection(),
        )

    @lru_cache()
    def _session_client(self) -> SessionClient:
        return SessionClient(
            window_client=self._window_client(),
            scenes_collection=self._scene_collection(),
        )

    @lru_cache()
    def _scene_collection(self) -> SceneCollection:
        return SceneCollection((
            SceneProvider(
                scene_id=GameSceneId("main-menu"),
                provider=ServiceProvider(lambda: SceneClient(
                    frame_collection=self._frame_collection())
                )
            ),
        ))

    @lru_cache()
    def _frame_collection(self) -> FrameCollection:
        return FrameCollection(frame_factory=self._frame_client_factory())

    @lru_cache()
    def _frame_client_factory(self) -> ServiceProvider[FrameClient]:
        return ServiceProvider[FrameClient](lambda: FrameClient(self._window_client()))

    @lru_cache()
    def _window_client(self) -> WindowClient:
        return WindowClient()

    def _on_input_v2(self, event: InputEvent[EventPayloadType], payload: EventPayloadType) -> None:
        # self._input_v2_routing.route(event, payload)
        # self._event_dispatcher.trigger(event, payload)
        pass
