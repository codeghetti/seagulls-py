from seagulls.space_shooter._stars_background import SimpleStarsBackground


class TestStarsBackground:
    def test_basics(self):
        SimpleStarsBackground("asset_manager", "fit_to_screen")
