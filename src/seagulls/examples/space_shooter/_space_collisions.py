from seagulls.engine import GameObject, Surface


class SpaceCollisions(GameObject):
    _lasers: [GameObject]
    _asteroids: [GameObject]

    def __init__(
            self,
            lasers: [GameObject],
            asteroids: [GameObject]):
        self._lasers = lasers
        self._asteroids = asteroids

    def tick(self) -> None:
        for laser in self._lasers:
            for asteroid in self._asteroids:
                if asteroid._position.x <= laser._position.x <= asteroid._position.x + asteroid._rock_size:
                    if asteroid._position.y <= laser._position.y <= asteroid._position.y + asteroid._rock_size:
                        self._asteroids.pop(asteroid)
                        self._lasers.pop(laser)

    def render(self, surface: Surface) -> None:
        pass
