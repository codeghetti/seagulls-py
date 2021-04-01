from dataclasses import dataclass

from pygame.surface import Surface
from pygame.math import Vector2
from pygame.time import Clock


@dataclass
class GameObject:
    size: Vector2
    position: Vector2
    velocity: Vector2
    sprite: Surface

    def update(self, tick: int):
        self.position = self.position + (self.velocity * tick / 10)
