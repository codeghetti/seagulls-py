from abc import abstractmethod
from typing import Iterable, Protocol

from seagulls.cat_demos.engine.v2._service_provider import ServiceProvider
from seagulls.cat_demos.engine.v2.window._window import WindowClient


class IFrame(Protocol):

    @abstractmethod
    def open_frame(self) -> None:
        pass

    @abstractmethod
    def run_frame(self) -> None:
        pass

    @abstractmethod
    def close_frame(self) -> None:
        pass


class IProvideFrames(Protocol):

    @abstractmethod
    def items(self) -> Iterable[IFrame]:
        pass


class FrameClient(IFrame):

    # _frame_collection: IProvideFrames
    _window_client: WindowClient

    def __init__(self, window_client: WindowClient) -> None:
        self._window_client = window_client

    def open_frame(self) -> None:
        pass

    def run_frame(self) -> None:
        self._window_client.get_surface().fill((20, 20, 40))
        # for frame in self._frame_collection.items():
        #     frame.open_frame()
        #     frame.run_frame()
        #     frame.close_frame()

    def close_frame(self) -> None:
        self._window_client.commit()


class IProvideSceneState(Protocol):
    @abstractmethod
    def is_open(self) -> bool:
        pass


class FrameCollection(IProvideFrames):

    _frame_factory: ServiceProvider[IFrame]
    # _scene_state: IProvideSceneState

    def __init__(
        self,
        frame_factory: ServiceProvider[IFrame],
        # scene_state: IProvideSceneState,
    ) -> None:
        self._frame_factory = frame_factory
        # self._scene_state = scene_state

    def items(self) -> Iterable[IFrame]:
        # while self._scene_state.is_open():
        while True:
            yield self._frame_factory.get_service()
