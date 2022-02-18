from seagulls.space_shooter import ScoreTracker


class TestScoreTracker:

    def test_basics(self):
        score_tracker = ScoreTracker()

        score_tracker.add_point()

    def test_get_score(self):
        score_tracker = ScoreTracker()

        score_tracker.add_point()
        score_tracker.add_point()

        assert score_tracker.get_score() == 2

    def test_reset(self):
        score_tracker = ScoreTracker()

        score_tracker.add_point()
        score_tracker.add_point()

        assert score_tracker.get_score() == 2

        score_tracker.reset()

        assert score_tracker.get_score() == 0
