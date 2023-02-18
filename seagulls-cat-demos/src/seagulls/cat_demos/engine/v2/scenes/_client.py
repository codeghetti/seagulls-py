from abc import abstractmethod
from queue import Empty, Queue
from typing import Dict, Iterable, NamedTuple, Protocol, Tuple

from seagulls.cat_demos.engine.v2.components._identity import GameSceneId
from seagulls.cat_demos.engine.v2.frames._client import IProvideFrames
from seagulls.cat_demos.engine.v2._service_provider import ServiceProvider


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
    def items(self) -> Iterable[IScene]:
        pass


class IProvideSessionState(Protocol):
    @abstractmethod
    def is_open(self) -> bool:
        pass


class SceneClient(IScene):

    _frame_collection: IProvideFrames

    def __init__(self, frame_collection: IProvideFrames) -> None:
        self._frame_collection = frame_collection

    def open_scene(self) -> None:
        pass

    def run_scene(self) -> None:
        for frame in self._frame_collection.items():
            frame.open_frame()
            frame.run_frame()
            frame.close_frame()

    def close_scene(self) -> None:
        pass


class SceneProvider(NamedTuple):
    scene_id: GameSceneId
    provider: ServiceProvider[IScene]


class SceneCollection(IProvideScenes):

    _next_scene: Queue[GameSceneId]
    _scene_providers: Dict[GameSceneId, ServiceProvider[IScene]]

    def __init__(self, scene_providers: Tuple[SceneProvider, ...]) -> None:
        self._next_scene = Queue(maxsize=1)
        self._scene_providers = {p.scene_id: p.provider for p in scene_providers}

    def load_scene(self, scene_id: GameSceneId) -> None:
        self._next_scene.put_nowait(scene_id)

    def items(self) -> Iterable[IScene]:
        try:
            while True:
                yield self._scene_providers[self._next_scene.get_nowait()].get_service()
        except Empty:
            pass
