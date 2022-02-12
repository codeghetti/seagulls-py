from typing import Any

from seagulls.engine import BlockingGameSession


class FakeSceneManager:
    counter: int

    def __init__(self):
        self.counter = 0

    def get_scene(self) -> Any:
        return self

    def start(self) -> None:
        pass

    def tick(self) -> None:
        self.counter += 1

    def should_quit(self) -> bool:
        return self.counter == 5


class TestBlockingGameSession:
    _fake_manager: FakeSceneManager
    _client: BlockingGameSession

    def setup(self) -> None:
        self._fake_manager = FakeSceneManager()
        self._client = BlockingGameSession(self._fake_manager)  # type: ignore

    def test_start(self) -> None:
        assert self._fake_manager.counter == 0
        self._client.start()
        assert self._fake_manager.counter == 5

    def test_wait_for_completion(self) -> None:
        assert self._fake_manager.counter == 0
        self._client.start()
        assert self._fake_manager.counter == 5
        # Should return right away in this case
        self._client.wait_for_completion()
        assert self._fake_manager.counter == 5

    def test_stop(self) -> None:
        assert self._fake_manager.counter == 0
        self._client.start()
        assert self._fake_manager.counter == 5
        # Should return right away in this case
        self._client.stop()
        assert self._fake_manager.counter == 5
