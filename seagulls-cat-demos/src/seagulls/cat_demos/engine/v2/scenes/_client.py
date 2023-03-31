from __future__ import annotations

import logging
from abc import abstractmethod
from queue import Empty, Queue
from typing import Dict, Iterable, NamedTuple, Optional, Protocol

from seagulls.cat_demos.engine.v2.components._entities import GameSceneId
from seagulls.cat_demos.engine.v2.components._service_provider import ServiceProvider
from seagulls.cat_demos.engine.v2.frames._client import IFrameCollection
from seagulls.cat_demos.engine.v2.sessions._executables import IExecutable

logger = logging.getLogger(__name__)


class IScene(Protocol):

    @abstractmethod
    def open_scene(self) -> None:
        pass

    @abstractmethod
    def run_scene(self) -> None:
        pass

    @abstractmethod
    def close_scene(self) -> None:
        pass


class IProvideScenes(Protocol):

    @abstractmethod
    def get_scenes(self) -> Iterable[IScene]:
        pass

    @abstractmethod
    def load_scene(self, scene_id: GameSceneId) -> None:
        pass


class IProvideSessionState(Protocol):
    @abstractmethod
    def is_open(self) -> bool:
        pass


class SceneContext:

    _current: Optional[GameSceneId]

    def __init__(self) -> None:
        self._current = None

    def __call__(self) -> GameSceneId:
        return self.get()

    def set(self, scene_id: GameSceneId) -> None:
        self._current = scene_id

    def get(self) -> GameSceneId:
        if self._current is None:
            raise RuntimeError("No active scene found")

        return self._current


class SceneComponent(IScene):

    _open_callback: IExecutable
    _close_callback: IExecutable
    _frame_collection: IFrameCollection

    def __init__(
        self,
        open_callback: IExecutable,
        close_callback: IExecutable,
        frame_collection: IFrameCollection,
    ) -> None:
        self._open_callback = open_callback
        self._close_callback = close_callback
        self._frame_collection = frame_collection

    def open_scene(self) -> None:
        self._open_callback()

    def run_scene(self) -> None:
        for frame in self._frame_collection.items():
            frame.process()

    def close_scene(self) -> None:
        self._close_callback()


class IManageScenes(Protocol):

    @abstractmethod
    def register(self, scene_id: GameSceneId, provider: ServiceProvider[IScene]) -> None:
        pass

    @abstractmethod
    def get(self, scene_id: GameSceneId) -> IScene:
        pass


class SceneRegistry(IManageScenes):

    _providers: Dict[GameSceneId, ServiceProvider[IScene]]

    def __init__(self) -> None:
        self._providers = {}

    @staticmethod
    def with_providers(*providers: SceneProvider) -> SceneRegistry:
        client = SceneRegistry()
        for p in providers:
            client.register(scene_id=p.scene_id, provider=p.provider)

        return client

    def register(self, scene_id: GameSceneId, provider: ServiceProvider[IScene]) -> None:
        self._providers[scene_id] = provider

    def get(self, scene_id: GameSceneId) -> IScene:
        return self._providers[scene_id]()


class SceneProvider(NamedTuple):
    scene_id: GameSceneId
    provider: ServiceProvider[IScene]


class SceneClient(IProvideScenes):

    _next_scene: Queue[GameSceneId]
    _scene_registry: IManageScenes
    _scene_context: SceneContext

    def __init__(self, scene_registry: IManageScenes, scene_context: SceneContext) -> None:
        self._next_scene = Queue(maxsize=1)
        self._scene_registry = scene_registry
        self._scene_context = scene_context

    def load_scene(self, scene_id: GameSceneId) -> None:
        self._next_scene.put_nowait(scene_id)

    def get_scenes(self) -> Iterable[IScene]:
        try:
            while True:
                scene_id = self._next_scene.get_nowait()
                self._scene_context.set(scene_id)
                yield self._scene_registry.get(scene_id)
        except Empty:
            pass


class GameSceneObjects:
    pass
