from abc import abstractmethod
from threading import Event
from typing import Iterable, NamedTuple, Protocol

from seagulls.cat_demos.engine.v2.components._service_provider import ServiceProvider
from seagulls.cat_demos.engine.v2.eventing._event_dispatcher import GameEvent, GameEventDispatcher, GameEventId
from seagulls.cat_demos.engine.v2.input._input_toggles import InputTogglesClient
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


class Frame(NamedTuple):
    id: int


class FrameEvents:
    OPEN = GameEventId[Frame]("seagulls:frame.open")
    EXECUTE = GameEventId[Frame]("seagulls:frame.execute")
    CLOSE = GameEventId[Frame]("seagulls:frame.close")


class FrameClient(IFrame):

    _event_client: GameEventDispatcher
    _window_client: WindowClient
    _pygame_input_client: PygameKeyboardInputPublisher
    _toggles: InputTogglesClient

    def __init__(
        self,
        event_client: GameEventDispatcher,
        window_client: WindowClient,
        pygame_input_client: PygameKeyboardInputPublisher,
        toggles: InputTogglesClient,
    ) -> None:
        self._event_client = event_client
        self._window_client = window_client
        self._pygame_input_client = pygame_input_client
        self._toggles = toggles

    def process(self) -> None:
        self._open_frame()
        self._execute_frame()
        self._close_frame()

    def _open_frame(self) -> None:
        self._event_client.trigger(GameEvent(FrameEvents.OPEN, None))
        # self._window_client.get_surface()
        self._pygame_input_client.tick()
        self._toggles.tick()

    def _execute_frame(self) -> None:
        self._event_client.trigger(GameEvent(FrameEvents.EXECUTE, None))

    def _close_frame(self) -> None:
        self._event_client.trigger(GameEvent(FrameEvents.CLOSE, None))
        self._window_client.commit()


class IStopScenes(Protocol):

    @abstractmethod
    def stop(self) -> None:
        pass


class FrameCollection(IFrameCollection, IStopScenes):

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
