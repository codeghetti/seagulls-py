from seagulls.engine import BasicSceneManager


class FakeScene:
    pass


class TestBasicSceneManager:
    def test_get_scene(self) -> None:
        fake_scene = FakeScene()
        client = BasicSceneManager(fake_scene)  # type: ignore
        assert client.get_scene() == fake_scene
