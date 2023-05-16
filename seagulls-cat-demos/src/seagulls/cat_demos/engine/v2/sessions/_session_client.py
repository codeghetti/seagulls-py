import logging
from abc import abstractmethod
from typing import Protocol

from seagulls.cat_demos.engine.v2.components._client_containers import GameClientProvider
from seagulls.cat_demos.engine.v2.components._entities import GameSceneId
from seagulls.cat_demos.engine.v2.scenes._scene_client import SceneClient
from seagulls.cat_demos.engine.v2.window._window import WindowClient

logger = logging.getLogger(__name__)


class ISession(Protocol):
    @abstractmethod
    def execute(self) -> None:
        pass


class SessionClient(ISession):
    _window_client: WindowClient
    _scene_client: SceneClient
    _first_scene: GameClientProvider[GameSceneId]

    def __init__(
        self,
        window_client: WindowClient,
        scene_client: SceneClient,
        first_scene: GameClientProvider[GameSceneId],
    ) -> None:
        self._window_client = window_client
        self._scene_client = scene_client
        self._first_scene = first_scene

    def execute(self) -> None:
        self._window_client.open()
        self._scene_client.load_scene(self._first_scene())

        for scene in self._scene_client.get_scenes():
            self._scene_client.process(scene)

        self._window_client.close()
