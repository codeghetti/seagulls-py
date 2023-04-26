from __future__ import annotations

import logging
from abc import abstractmethod
from queue import Empty, Queue
from typing import Dict, Iterable, NamedTuple, Optional, Protocol

from seagulls.cat_demos.engine.v2.components._entities import GameSceneId
from seagulls.cat_demos.engine.v2.components._service_provider import (
    ServiceProvider
)
from seagulls.cat_demos.engine.v2.eventing._event_dispatcher import (
    GameEvent,
    GameEventDispatcher,
    GameEventId
)
from seagulls.cat_demos.engine.v2.frames._frames_client import IFrameCollection

logger = logging.getLogger(__name__)


class IScene(Protocol):
    @abstractmethod
    def process(self) -> None:
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


class SceneEvent(NamedTuple):
    scene_id: GameSceneId


class SceneEvents:
    OPEN = GameEventId[SceneEvent]("scene.open")
    EXECUTE = GameEventId[SceneEvent]("scene.execute")
    CLOSE = GameEventId[SceneEvent]("scene.close")

    @staticmethod
    def open_scene(scene_id: GameSceneId) -> GameEventId[SceneEvent]:
        return GameEventId[SceneEvent](f"scene.open:{scene_id.name}")

    @staticmethod
    def execute_scene(scene_id: GameSceneId) -> GameEventId[SceneEvent]:
        return GameEventId[SceneEvent](f"scene.execute:{scene_id.name}")

    @staticmethod
    def close_scene(scene_id: GameSceneId) -> GameEventId[SceneEvent]:
        return GameEventId[SceneEvent](f"scene.close:{scene_id.name}")


class SceneComponent(IScene):
    _frame_collection: IFrameCollection
    _event_client: GameEventDispatcher
    _scene_context: SceneContext

    def __init__(
        self,
        frame_collection: IFrameCollection,
        event_client: GameEventDispatcher,
        scene_context: SceneContext,
    ) -> None:
        self._frame_collection = frame_collection
        self._event_client = event_client
        self._scene_context = scene_context

    def process(self) -> None:
        self._open_scene()
        self._execute_scene()
        self._close_scene()

    def _open_scene(self) -> None:
        scene_id = self._scene_context()
        payload = SceneEvent(scene_id)

        self._event_client.trigger(GameEvent(SceneEvents.open_scene(scene_id), payload))
        self._event_client.trigger(GameEvent(SceneEvents.OPEN, payload))

    def _execute_scene(self) -> None:
        scene_id = self._scene_context()
        payload = SceneEvent(scene_id)

        for frame in self._frame_collection.items():
            frame.process()
        self._event_client.trigger(
            GameEvent(SceneEvents.execute_scene(scene_id), payload)
        )
        self._event_client.trigger(GameEvent(SceneEvents.EXECUTE, payload))

    def _close_scene(self) -> None:
        scene_id = self._scene_context()
        payload = SceneEvent(scene_id)

        self._event_client.trigger(
            GameEvent(SceneEvents.close_scene(scene_id), payload)
        )
        self._event_client.trigger(GameEvent(SceneEvents.CLOSE, payload))


class SceneRegistry:
    _providers: Dict[GameSceneId, ServiceProvider[IScene]]

    def __init__(self) -> None:
        self._providers = {}

    @staticmethod
    def with_providers(*providers: SceneProvider) -> SceneRegistry:
        client = SceneRegistry()
        for p in providers:
            client.register(scene_id=p.scene_id, provider=p.provider)

        return client

    def register(
        self, scene_id: GameSceneId, provider: ServiceProvider[IScene]
    ) -> None:
        self._providers[scene_id] = provider

    def get(self, scene_id: GameSceneId) -> IScene:
        return self._providers[scene_id]()


class SceneProvider(NamedTuple):
    scene_id: GameSceneId
    provider: ServiceProvider[IScene]


class SceneClient(IProvideScenes):
    _next_scene: Queue[GameSceneId]
    _scene_registry: SceneRegistry
    _scene_context: SceneContext

    def __init__(
        self, scene_registry: SceneRegistry, scene_context: SceneContext
    ) -> None:
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
