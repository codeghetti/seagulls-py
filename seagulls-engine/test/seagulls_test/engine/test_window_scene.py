from typing import Callable, Dict

from seagulls.engine import IGameScene, IProvideActiveScene, WindowScene


class FakeActiveSceneProvider(IProvideActiveScene, IGameScene):

    num_calls: Dict[str, int]

    def __init__(self):
        self.num_calls = {
            "apply": 0,
            "start": 0,
            "should_quit": 0,
            "tick": 0,
        }

    def apply(self, callback: Callable[[IGameScene], None]):
        self.num_calls["apply"] += 1
        callback(self)

    def start(self) -> None:
        self.num_calls["start"] += 1

    def should_quit(self) -> bool:
        self.num_calls["should_quit"] += 1
        return False

    def tick(self) -> None:
        self.num_calls["tick"] += 1


class TestWindowScene:

    _provider: FakeActiveSceneProvider
    _client: WindowScene

    def setup(self) -> None:
        self._provider = FakeActiveSceneProvider()
        self._client = WindowScene(self._provider)

    def test_start(self) -> None:
        assert self._provider.num_calls["apply"] == 0
        assert self._provider.num_calls["start"] == 0
        self._client.start()
        assert self._provider.num_calls["apply"] == 1
        assert self._provider.num_calls["start"] == 1

    def test_tick(self) -> None:
        assert self._provider.num_calls["tick"] == 0
        self._client.start()
        self._client.tick()
        assert self._provider.num_calls["tick"] == 1

    def test_should_quit(self) -> None:
        assert self._provider.num_calls["should_quit"] == 0
        self._client.start()
        self._client.tick()
        self._client.should_quit()
        assert self._provider.num_calls["should_quit"] == 1
