from seagulls.space_shooter._space_collisions import SpaceCollisions


class TestSpaceCollisions:
    def test_basics(self):
        SpaceCollisions("asset_manager", "ship", "asteroid_field", "rock_collision_callback")
