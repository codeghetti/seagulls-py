from seagulls.space_shooter import ScoreOverlay


class TestScoreOverlay:

    def test_basics(self):
        ScoreOverlay(
            "asset_manager",
            "score_tracker",
            "fit_to_screen:"
        )
