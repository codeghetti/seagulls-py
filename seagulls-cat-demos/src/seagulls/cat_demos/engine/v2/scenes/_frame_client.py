from abc import abstractmethod
from threading import Event
from typing import Dict, Iterable, NamedTuple, Protocol

from seagulls.cat_demos.engine.v2.components._client_containers import GameClientProvider
from seagulls.cat_demos.engine.v2.components._entities import GameSceneId
from seagulls.cat_demos.engine.v2.eventing._event_dispatcher import (
    GameEvent,
    GameEventDispatcher,
    GameEventId
)
from seagulls.cat_demos.engine.v2.input._input_toggles import (
    InputTogglesClient
)
from seagulls.cat_demos.engine.v2.input._pygame import (
    PygameKeyboardInputPublisher
)
from seagulls.cat_demos.engine.v2.scenes._scene_client import IFrame, IFrameCollection, SceneContext
from seagulls.cat_demos.engine.v2.window._window import WindowClient


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
        self._event_client.trigger(GameEvent(FrameEvents.OPEN, None))
        self._event_client.trigger(GameEvent(FrameEvents.EXECUTE, None))
        self._event_client.trigger(GameEvent(FrameEvents.CLOSE, None))


class IStopScenes(Protocol):
    @abstractmethod
    def stop(self) -> None:
        pass


class FrameCollection(IFrameCollection, IStopScenes):
    _frame_factory: GameClientProvider[IFrame]
    _scene_context: SceneContext
    _stop: Dict[GameSceneId, Event]

    def __init__(
        self,
        frame_factory: GameClientProvider[IFrame],
        scene_context: SceneContext,
    ) -> None:
        self._frame_factory = frame_factory
        self._scene_context = scene_context
        self._stop = {}

    def stop(self) -> None:
        self._stop[self._scene_context.get()].set()

    def items(self) -> Iterable[IFrame]:
        scene_id = self._scene_context.get()
        self._stop[scene_id] = Event()
        while not self._stop[scene_id].is_set():
            yield self._frame_factory()
