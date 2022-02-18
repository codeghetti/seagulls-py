from seagulls.space_shooter._game_over_overlay import GameOverOverlay


class TestGameOverOverlay:

    def test_basics(self):
        game_over_overlay = GameOverOverlay(
            "asset_manager",
            "fit_to_screen"
        )

        game_over_overlay.tick()
