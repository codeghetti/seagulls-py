from seagulls.space_shooter import ScoreOverlay


class TestScoreOverlay:

    def test_basics(self):
        score_overlay = ScoreOverlay(
            "asset_manager",
            "score_tracker",
            "fit_to_screen:"
        )

        score_overlay.tick()
