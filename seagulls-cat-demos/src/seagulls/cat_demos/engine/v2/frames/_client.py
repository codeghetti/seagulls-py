from abc import abstractmethod
from threading import Event
from typing import Iterable, Protocol

from seagulls.cat_demos.engine.v2._service_provider import ServiceProvider
from seagulls.cat_demos.engine.v2.eventing._client import GameEvent, GameEventDispatcher, GameEventId
from seagulls.cat_demos.engine.v2.input._pygame import PygameKeyboardInputPublisher
from seagulls.cat_demos.engine.v2.window._window import WindowClient


class IFrame(Protocol):

    @abstractmethod
    def process(self) -> None:
        pass


class IFrameCollection(Protocol):

    @abstractmethod
    def items(self) -> Iterable[IFrame]:
        pass


class FrameEvents:
    OPEN: GameEventId[None] = GameEventId[None]("seagulls:frame.open")
    EXECUTE: GameEventId[None] = GameEventId[None]("seagulls:frame.execute")
    CLOSE: GameEventId[None] = GameEventId[None]("seagulls:frame.close")


class FrameClient(IFrame):

    _event_client: GameEventDispatcher
    _window_client: WindowClient
    _pygame_input_client: PygameKeyboardInputPublisher

    def __init__(
        self,
        event_client: GameEventDispatcher,
        window_client: WindowClient,
        pygame_input_client: PygameKeyboardInputPublisher,
    ) -> None:
        self._event_client = event_client
        self._window_client = window_client
        self._pygame_input_client = pygame_input_client

    def process(self) -> None:
        self._open_frame()
        self._execute_frame()
        self._close_frame()

    def _open_frame(self) -> None:
        self._event_client.trigger(GameEvent(FrameEvents.OPEN, None))
        self._pygame_input_client.tick()

    def _execute_frame(self) -> None:
        self._event_client.trigger(GameEvent(FrameEvents.EXECUTE, None))
        self._window_client.get_surface().fill((20, 120, 20))

    def _close_frame(self) -> None:
        self._event_client.trigger(GameEvent(FrameEvents.CLOSE, None))
        self._window_client.commit()


class IProvideSceneState(Protocol):
    @abstractmethod
    def is_open(self) -> bool:
        pass


class FrameCollection(IFrameCollection):

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
            yield self._frame_factory()
