import logging
import math
import random
from functools import lru_cache

from pygame import mixer

from seagulls.assets import AssetManager
from seagulls.engine import (
    GameClock,
    GameControls,
    GameObject,
    Surface,
    Vector2, GameObjectsCollection
)
from ._collidables import CollidablesCollection

logger = logging.getLogger(__name__)


class Laser(GameObject):
    _clock: GameClock
    _sprite: Surface
    _position: Vector2
    _velocity: Vector2
    _collidables: CollidablesCollection

    _collided: bool

    def __init__(
            self,
            clock: GameClock,
            collidables: CollidablesCollection,
            sprite: Surface,
            ship_position: Vector2):
        self._clock = clock
        self._collidables = collidables
        self._sprite = sprite
        self._position = Vector2(ship_position.x + 52, ship_position.y - 57)
        self._velocity = Vector2(0, 8)

        self._collided = False

    def tick(self) -> None:
        if self._collided:
            return

        for collidables in self._collidables.get_collisions(self._position):
            self._on_collision()
            collidables.collide()

        delta = self._clock.get_time()

        self._position = self._position - (self._velocity * delta / 10)

    def render(self, surface: Surface) -> None:
        if self._collided:
            return

        laser_sprite = self._get_cached_laser()
        surface.blit(laser_sprite, self._position)

    def _on_collision(self) -> None:
        self._collided = True

    @lru_cache()
    def _get_cached_laser(self) -> Surface:
        return self._sprite.copy()


class LaserFactory:
    _clock: GameClock
    _collidables: CollidablesCollection
    _asset_manager: AssetManager

    def __init__(
            self,
            clock: GameClock,
            collidables: CollidablesCollection,
            asset_manager: AssetManager):
        self._clock = clock
        self._collidables = collidables
        self._asset_manager = asset_manager

    def create(self, position: Vector2) -> Laser:
        return Laser(self._clock, self._collidables, self._get_sprite(), position)

    def _get_sprite(self) -> Surface:
        options = ["red", "blue"]
        choice = options[random.randint(0, len(options) - 1)]
        return self._asset_manager.load_sprite(f"space-shooter/laser-{choice}")


class Gun(GameObject):

    _lasers: GameObjectsCollection
    _laser_sound: mixer.Sound

    def __init__(self, laser_factory: LaserFactory):
        self._laser_factory = laser_factory
        self._lasers = GameObjectsCollection()
        mixer.init()
        self._laser_sound = mixer.Sound("assets/sounds/laser-sound.ogg")

    def fire(self, position: Vector2) -> None:
        self._lasers.add(self._laser_factory.create(position))
        self._laser_sound.play()

    def tick(self) -> None:
        self._lasers.apply(lambda x: x.tick())

    def render(self, surface: Surface) -> None:
        self._lasers.apply(lambda x: x.render(surface))


class Ship(GameObject):
    _clock: GameClock
    _asset_manager: AssetManager
    _game_controls: GameControls
    _position: Vector2
    _velocity: Vector2
    _max_velocity: float
    _gun: Gun

    _collided: bool
    _collidables: CollidablesCollection

    def __init__(
            self,
            clock: GameClock,
            collidables: CollidablesCollection,
            asset_manager: AssetManager,
            gun: Gun,
            game_controls: GameControls):
        self._clock = clock
        self._collidables = collidables
        self._asset_manager = asset_manager
        self._gun = gun
        self._game_controls = game_controls
        self._position = Vector2(400, 303)
        self._velocity = Vector2(0, 0)
        self._max_velocity = 7.0
        self._collided = False

    def tick(self) -> None:
        if self._collided:
            return

        self._gun.tick()
        if self._game_controls.is_left_moving():
            if math.floor(abs(self._velocity.x)) <= self._max_velocity:
                self._velocity = self._velocity + Vector2(-0.1, 0)
        elif self._game_controls.is_right_moving():
            if self._velocity.x <= self._max_velocity:
                self._velocity = self._velocity + Vector2(0.1, 0)
        else:
            self._velocity.x = 0.0
        if self._game_controls.is_up_moving():
            if math.floor(abs(self._velocity.y)) <= self._max_velocity:
                self._velocity = self._velocity + Vector2(0, -0.1)
        elif self._game_controls.is_down_moving():
            if self._velocity.y <= self._max_velocity:
                self._velocity = self._velocity + Vector2(0, 0.1)
        else:
            self._velocity.y = 0.0

        if self._game_controls.should_fire():
            self._gun.fire(self._position)

        delta = self._clock.get_time()

        self._position = self._position + (self._velocity * delta / 10)

        if self._position.x < 0:
            self._position.x = 0

        if self._position.x > 1024 - 112:
            self._position.x = 1024 - 112

        if self._position.y < 0:
            self._position.y = 0

        if self._position.y > 600 - 75:
            self._position.y = 600 - 75

        for collidables in self._collidables.get_collisions(self._position):
            self._on_collision()
            collidables.collide()

    def _on_collision(self) -> None:
        self._collided = True
        mixer.init()
        mixer.Sound("assets/sounds/game-over.ogg").play()

    def render(self, surface: Surface) -> None:
        if self._collided:
            return

        self._gun.render(surface)
        ship_sprite = self._get_cached_ship()
        surface.blit(ship_sprite, self._position)

    @lru_cache()
    def _get_cached_ship(self) -> Surface:
        return self._asset_manager.load_sprite("space-shooter/ship-orange").copy()

    def get_ship_position(self) -> Vector2:
        return self._position
