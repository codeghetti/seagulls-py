import logging
from abc import abstractmethod
from typing import Iterable, Protocol

from seagulls.cat_demos.engine.v2.scenes._client import IProvideScenes
from seagulls.cat_demos.engine.v2.window._window import WindowClient

logger = logging.getLogger(__name__)


class ISession(Protocol):

    @abstractmethod
    def open_session(self) -> None:
        pass

    @abstractmethod
    def run_session(self) -> None:
        pass

    @abstractmethod
    def close_session(self) -> None:
        pass


class SessionClient(ISession):

    _window_client: WindowClient
    _scenes_collection: IProvideScenes

    def __init__(
        self,
        window_client: WindowClient,
        scenes_collection: IProvideScenes,
    ) -> None:
        self._window_client = window_client
        self._scenes_collection = scenes_collection

    def open_session(self) -> None:
        self._window_client.open()

    def run_session(self) -> None:
        logger.warning(f"running session")
        for scene in self._scenes_collection.items():
            logger.warning(f"processing scene: {scene}")
            scene.open_scene()
            scene.run_scene()
            scene.close_scene()

    def close_session(self) -> None:
        self._window_client.close()
