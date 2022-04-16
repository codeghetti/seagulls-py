import logging
from functools import cache
from pathlib import Path

import pygame.display
from pygame import Surface
from pygame.image import load

from seagulls.rendering import (
    Color,
    IPrintSquares,
    Position,
    Size, IPrintSprites,
)

from ._surface import IProvideSurfaces

logger = logging.getLogger(__name__)


class PygameSpritePrinter(IPrintSprites):

    _surface: IProvideSurfaces

    def __init__(self, surface: IProvideSurfaces):
        self._surface = surface

    def print_sprite(self, image_path: Path, size: Size, position: Position) -> None:
        # Pixel Units
        png_surface = self._load_png(image_path)
        s = size.get()
        p = position.get()
        # World Units
        scaled_png = pygame.transform.scale(png_surface, (s["width"], s["height"]))
        self._get_frame().blit(scaled_png, (p["x"], p["y"]))
        logger.warning(f"surface provider in sprite printer: {self._surface}")

    def commit(self) -> None:
        self._surface.update(self._get_frame())

    def clear(self) -> None:
        self._get_frame.cache_clear()

    @cache
    def _get_frame(self) -> Surface:
        frame = self._surface.get()
        frame.blit(self._get_copy(), (0, 0))
        return frame

    @cache
    def _get_copy(self) -> Surface:
        return self._surface.get().copy()

    def _load_png(self, png_path: Path) -> Surface:
        loaded_sprite = load(png_path.resolve())
        if loaded_sprite.get_alpha() is None:
            return loaded_sprite.convert()
        else:
            return loaded_sprite.convert_alpha()


class PygameSquarePrinter(IPrintSquares):

    _surface: IProvideSurfaces

    def __init__(self, surface: IProvideSurfaces):
        self._surface = surface

    def print_square(self, color: Color, size: Size, position: Position):
        c = color.get()
        s = size.get()
        p = position.get()

        square = Surface((s["width"], s["height"]))
        square.fill((c["r"], c["g"], c["b"]))
        self._get_frame().blit(square, (p["x"], p["y"]))

    def commit(self) -> None:
        self._surface.update(self._get_frame())

    def clear(self) -> None:
        self._get_frame.cache_clear()

    @cache
    def _get_frame(self) -> Surface:
        frame = self._surface.get()
        frame.blit(self._get_copy(), (0, 0))
        return frame

    @cache
    def _get_copy(self) -> Surface:
        return self._surface.get().copy()


"""
2022-04-12
What if each frame is a new set of objects that we execute, instead of making it a set of objects
we repeatedly call tick() on? We could "tick" future frames before the current one is done
rendering. Access to physics properties of the current frame from future frames can be turned into a
DAG of operations in order to pre-calculate data for a future frame.

```python
class AwaitableReferencePresenter(Protocol):
    def on_ready(self, val: int) -> None: ...

class AwaitableReference:

    # Whether this class is available for interaction
    _available: Event
    _presenter: AwaitableReferencePresenter
    
    def __init__(self):
        self._available = Event()
    
    @release_reference
    def execute(self) -> None:
        # Do some stuff
        self._presenter.on_ready(random.randint(1, 100))
```

This is almost certainly a bad idea. 
"""
