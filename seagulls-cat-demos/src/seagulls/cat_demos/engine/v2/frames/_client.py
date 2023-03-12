from abc import abstractmethod
from threading import Event
from typing import Iterable, Protocol

from seagulls.cat_demos.engine.v2._service_provider import ServiceProvider
from seagulls.cat_demos.engine.v2.eventing._client import GameEvent, GameEventDispatcher, GameEventId


class IFrame(Protocol):

    @abstractmethod
    def process(self) -> None:
        pass


class IProvideFrames(Protocol):

    @abstractmethod
    def items(self) -> Iterable[IFrame]:
        pass


class FrameEvents:
    OPEN: GameEventId[None] = GameEventId[None]("seagulls:frame.open")
    EXECUTE: GameEventId[None] = GameEventId[None]("seagulls:frame.execute")
    CLOSE: GameEventId[None] = GameEventId[None]("seagulls:frame.close")


class FrameClient(IFrame):

    _event_client: GameEventDispatcher

    def __init__(self, event_client: GameEventDispatcher) -> None:
        self._event_client = event_client

    def process(self) -> None:
        self._event_client.trigger(GameEvent(FrameEvents.OPEN, None))
        self._event_client.trigger(GameEvent(FrameEvents.EXECUTE, None))
        self._event_client.trigger(GameEvent(FrameEvents.CLOSE, None))


class IProvideSceneState(Protocol):
    @abstractmethod
    def is_open(self) -> bool:
        pass


class FramesProvider(IProvideFrames):

    _frame_factory: ServiceProvider[IFrame]
    _stop: Event

    def __init__(
        self,
        frame_factory: ServiceProvider[IFrame],
    ) -> None:
        self._frame_factory = frame_factory
        self._stop = Event()

    def stop(self) -> None:
        self._stop.set()

    def items(self) -> Iterable[IFrame]:
        while not self._stop.is_set():
            yield self._frame_factory.get()
