from pygame import Surface

from seagulls.cat_demos._object_position import Position
from seagulls.cat_demos.engine._rendering import IProvideSurfaces, IProvidePositions


class PlayerSprite(IProvideSurfaces, IProvidePositions):
    def get_position(self) -> Position:
        return Position(x=10, y=10)

    def get_surface(self) -> Surface:
        surface = Surface((20, 20))
        surface.fill((100, 100, 200))
        return surface
