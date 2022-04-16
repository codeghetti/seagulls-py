"""
Pygame implementation of engine interfaces.

The seagulls.pygame package implements all the engine interfaces to translate them to pygame
concepts. We should see no references to the pygame library outside this package, which should give
us the ability to use other graphical libraries in the future.
"""

from ._printer import PygameSquarePrinter, PygameSpritePrinter
from ._surface import IProvideSurfaces, PygameSurface
from ._window import WindowSurface, DeferredWindowSurface

__all__ = [
    "PygameSquarePrinter",
    "PygameSpritePrinter",
    "IProvideSurfaces",
    "PygameSurface",
    "WindowSurface",
    "DeferredWindowSurface",
]
