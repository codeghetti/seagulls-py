import logging
from abc import abstractmethod

from typing import Iterable, Protocol

from seagulls.cat_demos.engine.v2._game_clock import GameClock
from seagulls.cat_demos.engine.v2._input_client import IProcessInputEvents
from seagulls.cat_demos.engine.v2.window._window import WindowClient
from seagulls.cat_demos.engine.v2.scenes._client import IProvideScenes, IScene

logger = logging.getLogger(__name__)


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


class GameSessionInteractors(IScene, IFrame):

    _window: WindowClient
    _scenes: IProvideScenes
    _frames: IProvideFrames
    _clock: GameClock
    _input: IProcessInputEvents

    def __init__(
        self,
        window: WindowClient,
        scenes: IProvideScenes,
        frames: IProvideFrames,
        clock: GameClock,
        input: IProcessInputEvents,
    ) -> None:
        self._window = window
        self._scenes = scenes
        self._frames = frames
        self._clock = clock
        self._input = input

    def open_session(self) -> None:
        self._window.open()

    def run_session(self) -> None:
        logger.warning(f"running session")
        for scene in self._scenes.get_scenes():
            logger.warning(f"processing scene: {scene}")
            scene.open_scene()
            scene.run_scene()
            scene.close_scene()

    def close_session(self) -> None:
        self._window.close()

    def open_scene(self) -> None:
        # self._load_clock_plugin()
        # self._load_input_plugin()
        pass

    def run_scene(self) -> None:
        for frame in self._frames.items():
            frame.open_frame()
            frame.run_frame()
            frame.close_frame()

    def close_scene(self) -> None:
        pass

    def open_frame(self) -> None:
        pass

    def run_frame(self) -> None:
        self._clock.tick()
        self._input.tick()

    def close_frame(self) -> None:
        self._window.commit()
