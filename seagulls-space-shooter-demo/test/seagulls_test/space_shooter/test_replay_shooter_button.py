from seagulls.space_shooter import ReplayButtonFactory, ReplayShooterButton


class TestReplayButtonFactory:

    def test_get_instance(self):

        factory = ReplayButtonFactory(
            "asset_manager",
            "game_controls",
            "active_scene_manager",
            "fit_to_screen")

        assert isinstance(factory.get_instance("scene"), ReplayShooterButton)
