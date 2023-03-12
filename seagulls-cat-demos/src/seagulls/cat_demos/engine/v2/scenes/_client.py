from __future__ import annotations

from abc import abstractmethod
from queue import Empty, Queue
from typing import Dict, Iterable, NamedTuple, Protocol

from seagulls.cat_demos.engine import IExecutable
from seagulls.cat_demos.engine.v2._service_provider import ServiceProvider
from seagulls.cat_demos.engine.v2.components._entities import GameSceneId
from seagulls.cat_demos.engine.v2.frames._client import IProvideFrames


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


class IProvideSessionState(Protocol):
    @abstractmethod
    def is_open(self) -> bool:
        pass


class SceneComponent(IScene):

    _open_callback: IExecutable
    _close_callback: IExecutable
    _frames_provider: IProvideFrames

    def __init__(
        self,
        open_callback: IExecutable,
        close_callback: IExecutable,
        frames_provider: IProvideFrames,
    ) -> None:
        self._open_callback = open_callback
        self._close_callback = close_callback
        self._frames_provider = frames_provider

    def open_scene(self) -> None:
        self._open_callback.execute()

    def run_scene(self) -> None:
        for frame in self._frames_provider.items():
            frame.process()

    def close_scene(self) -> None:
        self._close_callback.execute()


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
        return self._providers[scene_id].get()


class SceneProvider(NamedTuple):
    scene_id: GameSceneId
    provider: ServiceProvider[IScene]


class SceneClient(IProvideScenes):

    _next_scene: Queue[GameSceneId]
    _scene_registry: IManageScenes

    def __init__(self, scene_registry: IManageScenes) -> None:
        self._next_scene = Queue(maxsize=1)
        self._scene_registry = scene_registry

    def load_scene(self, scene_id: GameSceneId) -> None:
        self._next_scene.put_nowait(scene_id)

    def get_scenes(self) -> Iterable[IScene]:
        try:
            while True:
                yield self._scene_registry.get(self._next_scene.get_nowait())
        except Empty:
            pass


class GameSceneObjects:
    pass
