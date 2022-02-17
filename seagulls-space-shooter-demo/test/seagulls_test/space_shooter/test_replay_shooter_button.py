from seagulls.space_shooter import ReplayButtonFactory, ReplayShooterButton


class TestReplayButtonFactory:

    def test_get_instance(self):
        hello = "hello"

        factory = ReplayButtonFactory(
            hello,
            hello,
            hello,
            hello)

        assert isinstance(factory.get_instance(hello), ReplayShooterButton)
