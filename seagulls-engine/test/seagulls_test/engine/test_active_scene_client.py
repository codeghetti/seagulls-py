from seagulls.engine import ActiveSceneClient


class FakeGameScene:
    pass


class TestActiveSceneClient:
    def test_apply(self) -> None:
        fake_scene = FakeGameScene()

        def callback(scene: FakeGameScene) -> None:
            assert scene == fake_scene

        client = ActiveSceneClient(fake_scene)  # type: ignore
        client.apply(callback)  # type: ignore

    def test_set_active_scene(self) -> None:
        initial_fake_scene = FakeGameScene()
        second_fake_scene = FakeGameScene()

        def callback(scene: FakeGameScene) -> None:
            assert scene == second_fake_scene

        client = ActiveSceneClient(initial_fake_scene)  # type: ignore
        client.set_active_scene(second_fake_scene)  # type: ignore
        client.apply(callback)  # type: ignore
