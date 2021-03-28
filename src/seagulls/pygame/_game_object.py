from pygame.surface import Surface
from pygame.math import Vector2


class GameObject:
    def __init__(self, position: Vector2, sprite: Surface, velocity: Vector2):
        self.position = position
        self.sprite = sprite
        self.radius = sprite.get_width() / 2
        self.velocity = velocity

    def draw(self, surface: Surface):
        blit_position = self.position - Vector2(self.radius)
        surface.blit(self.sprite, blit_position)  # type: ignore

    def move(self):
        self.position = self.position + self.velocity

    def collides_with(self, other_obj: "GameObject"):
        distance = self.position.distance_to(other_obj.position)
        return distance < self.radius + other_obj.radius
