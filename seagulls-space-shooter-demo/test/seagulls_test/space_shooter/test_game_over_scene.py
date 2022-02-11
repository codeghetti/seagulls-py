from seagulls.space_shooter import GameOverScene, GameOverSceneFactory


class TestGameOverSceneFactory:
    def test_get_instance(self):
        factory = GameOverSceneFactory(
            "surface_renderer",
            "game_controls",
            "asset_manager",
            "active_scene_manager",
            "score_overlay",
            "background",
            "fit_to_screen"
        )

        assert isinstance(factory.get_instance("scene"), GameOverScene)
