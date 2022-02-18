from seagulls.space_shooter._space_rock import SpaceRock


class TestSpaceRock:

    _space_rock_small: SpaceRock
    _space_rock_medium: SpaceRock
    _space_rock_large: SpaceRock

    def setup(self):
        self._space_rock_small = SpaceRock(
            "clock",
            "asset_manager",
            (28, 28),
            (3, 4),
            "fit_to_screen",
        )

        self._space_rock_medium = SpaceRock(
            "clock",
            "asset_manager",
            (45, 40),
            (3, 4),
            "fit_to_screen",
        )

        self._space_rock_large = SpaceRock(
            "clock",
            "asset_manager",
            (70, 70),
            (3, 4),
            "fit_to_screen",
        )

    def test_get_rock_size_x(self) -> None:
        assert self._space_rock_small.get_rock_size_x() == 28
        assert self._space_rock_large.get_rock_size_x() == 70

    def test_get_rock_size_y(self) -> None:
        assert self._space_rock_medium.get_rock_size_y() == 40
        assert self._space_rock_large.get_rock_size_y() == 70
