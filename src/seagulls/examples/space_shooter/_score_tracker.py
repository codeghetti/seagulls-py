class ScoreTracker:

    def __init__(self):
        self._score = 0

    def add_point(self) -> None:
        self._score += 1

    def get_score(self) -> int:
        return self._score

    def reset(self) -> None:
        self._score = 0
