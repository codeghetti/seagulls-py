from __future__ import annotations

import logging
from abc import abstractmethod
from queue import Empty, Queue
from typing import Iterable, NamedTuple, Optional, Protocol

from seagulls.cat_demos.engine.v2.components._entities import GameSceneId
from seagulls.cat_demos.engine.v2.eventing._event_dispatcher import (
    GameEvent,
    GameEventDispatcher, GameEventId
)

logger = logging.getLogger(__name__)


class IFrame(Protocol):
    @abstractmethod
    def process(self) -> None:
        pass


class IFrameCollection(Protocol):
    @abstractmethod
    def items(self) -> Iterable[IFrame]:
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


class SceneClient:
    _next_scene: Queue[GameSceneId]
    _scene_context: SceneContext
    _frame_collection: IFrameCollection
    _event_client: GameEventDispatcher

    def __init__(
        self,
        scene_context: SceneContext,
        frame_collection: IFrameCollection,
        event_client: GameEventDispatcher,
    ) -> None:
        self._next_scene = Queue(maxsize=1)
        self._scene_context = scene_context
        self._frame_collection = frame_collection
        self._event_client = event_client

    def process(self, scene_id: GameSceneId) -> None:
        self._scene_context.set(scene_id)
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

    def load_scene(self, scene_id: GameSceneId) -> None:
        print(f"loading: {scene_id} ({self})")
        self._next_scene.put_nowait(scene_id)

    def get_scenes(self) -> Iterable[GameSceneId]:
        try:
            while True:
                scene_id = self._next_scene.get_nowait()
                logger.warning(f"getting next scene: {scene_id}")
                yield scene_id
        except Empty:
            logger.warning("no more scenes found")
